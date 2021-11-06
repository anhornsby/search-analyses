#!/usr/bin/env python
# coding: utf-8
"""
Fit the SAM retrieval model to sequential food retrievals, as recorded by Zemla et al. (2020)
Adam Hornsby
"""

import logging

import pandas as pd
import numpy as np

from memory_analyses.models.sam import MultiProbeRetrievalModel
from memory_analyses.models.loss import negative_log_likelihood
from memory_analyses.models.optimise import ScipyMinimiser
from memory_analyses.utilities.stats import aic, bic, mean_confidence_interval

def _run_model(data: pd.DataFrame, representations: list) -> pd.DataFrame: 
    """
    Run a model on the data for a given set of representations
    For exampe, `_run_model(data, ['cooc', 'w2v', 'hier']) will run the model
    on the three representations
   
    Arguments:
        data (pd.DataFrame): The sequential retrieval data. Must contain a participant column
            and measures of sequential similarity, prefixed with the values given in the representations
            argument
       
        representation (list): A list of representations. These must match the prefixes of the columns
            within data. For examle, 'cooc' will subset 'cooc_similarity'.
           
    Returns:
        (pd.DataFrame): A DataFrame of model fit statistics per participant.
    """
   
    participants = data['participant'].unique()
   
    k = len(representations)
   
    bounds = (0, None)
    optim = ScipyMinimiser(
        {
            "method": "SLSQP",
            "x0": [0] * k,
            "bounds": [bounds] * k,
        }
    )

    model = MultiProbeRetrievalModel(
                probe_configs=None,
                optimiser=optim,
                jitter_val=1.0e-7,
                loss_func=negative_log_likelihood,
                init_probe_weights=None,
                learn_weights=True,
            )
   
    all_loss = []
    all_weights = []
    all_success = []
    all_rows = []

    # loop over each participant
    for participant in participants:

        # extract transition similarities for this participant
        p_data = data[data['participant'] == participant]

        # get the current similarities
        current_sims = []
        subs_sims = []
        for sim in representations:
            current_sims.append(p_data[f'{sim}_similarity'])
            subs_sims.append(p_data[f'rem_{sim}'])

        # fit the model
        loss, weights, success = model.fit(current_sims, subs_sims)

        all_loss.append(loss)
        all_weights.append(weights)
        all_success.append(success)
        all_rows.append(p_data.shape[0])
   
    results_df = pd.DataFrame([participants, all_loss, all_success, all_rows]).T
    results_df.columns = ['participant', 'loss', 'converged', 'nrows']
    results_df[representations] = all_weights
    results_df['model'] = str(representations)
    results_df['k'] = k
   
    return results_df

def _create_baseline_data(data):
    """Create data for a baseline model, where we have equal transition probabilities for each stimulus"""
   
    # create a baseline model where each transition has an equal probability
    baseline = data[['participant']]
    baseline['dummy_similarity'] = 1.
    baseline['rem_dummy'] = data['rem_hier'].apply(lambda x: ' '.join(np.ones(len(x.split(' '))).astype(str).tolist()))
   
    return baseline

def _model_comparison_summary(model_results, baseline_df):
    """Calculate model comparison statistics for each model, such as AIC and BIC"""
   
    # sum loss for each model type
    model_summary = model_results.groupby('model').agg({'loss': 'sum', 'nrows': 'sum', 'k': 'max'})
    model_summary['loss'] = -model_summary['loss']
    model_bic = model_summary.apply(lambda x: bic(*x), axis=1)
    model_aic = model_summary.apply(lambda x: aic(*x), axis=1)
   
    # add on basline information, which will become useful later for comparisons
    # model has 0 parameters
    baseline_summary = baseline_df.groupby('model').agg({'loss': 'sum', 'nrows': 'sum', 'k': 'max'})
    baseline_summary['loss'] = -baseline_summary['loss']
    baseline_bic = baseline_summary.apply(lambda x: bic(x[0], x[1], 0), axis=1)
    baseline_aic = baseline_summary.apply(lambda x: aic(x[0], x[1], 0), axis=1)
   
    baseline_bic = baseline_bic[0]
    baseline_aic = baseline_aic[0]
   
    # join these comparions together
    model_fits = pd.concat([model_summary[['k', 'loss']], model_aic, model_bic], axis=1).sort_values(['k', 'loss'], ascending=[True, False])
    model_fits.columns = ['k', 'loss', 'aic', 'bic']
    model_fits['baseline_aic'] = baseline_aic
    model_fits['baseline_bic'] = baseline_bic
   
    # calculate the aic and bic improvement (over the baseline) for each model
    model_fits['aic_improvement'] = ((baseline_aic - model_fits['aic']) / model_fits['aic']) * 100
    model_fits['bic_improvement'] = ((baseline_bic - model_fits['bic']) / model_fits['bic']) * 100
    model_fits['baseline_loss'] = baseline_summary['loss'][0]
   
    # calculate the mean attention weight for each knowledge representation
    mean_weights = model_results.groupby('model')[['cooc', 'w2v', 'hier']].mean()
   
    # add on the confidence intervals for each attention weight
    mean_weights = mean_weights.round(3).astype(str)
    mean_ci = model_results.groupby('model')[['cooc', 'w2v', 'hier']].agg(mean_confidence_interval).round(3).astype(str)

    for col in mean_weights.columns:
        mean_weights[col] = mean_weights[col] + ' (' + mean_ci[col] + ')'
   
    model_fw = pd.concat([model_fits, mean_weights], axis=1)
   
    return model_fw

def main(config):
    """Main entrypoint to script"""
   
    # import the sequential transition data
    all_data = pd.read_csv(config['transition_table'])
   
    # filter data based on the requested run
    if config['condition'] == 'all':
        all_data['participant'] = all_data['id'] + '_' + all_data['listnum'].astype(str)
       
    elif config['condition'] == 'collapse':
        all_data['participant'] = all_data['id']
       
    elif config['condition'] == 'first':
        all_data['listnum'] = all_data.groupby('id')['listnum'].rank("dense")
        all_data = all_data[all_data['listnum'] == 1]
        all_data['participant'] = all_data['id']
       
    else:
        raise NotImplementedError
   
    # print summary statistics to the log
    logging.info('Number of participants: {0})'.format(
        all_data['id'].nunique())
            )

    # create a baseline model
    # each option will be given an equal probability
    baseline = _create_baseline_data(all_data)
   
    all_results = []

    # fit the baseline model (equal probability of transitioning to each product)
    baseline_df = _run_model(baseline, ['dummy'])
    baseline_df['k'] = 0
    all_results.append(baseline_df)

    # loop over each model comparison and fit the model
    # cooc: episodic (i.e. co-occurrence)
    # w2v: semantic (i.e. word2vec)
    # hier: hierarchy
    for model_feats in [
                        ['cooc'], 
                        ['w2v'], 
                        ['hier'],
                        ['cooc', 'w2v'],
                        ['cooc', 'hier'],
                        ['w2v', 'hier'],
                        ['cooc', 'w2v', 'hier']
                        ]:

        logging.info(f'Fitting model for {model_feats}')

        results_df = _run_model(all_data, model_feats)
        all_results.append(results_df)
       
    model_results = pd.concat(all_results)
   
    # calclate model comparison statistics
    model_fw = _model_comparison_summary(model_results, baseline_df)
    model_fw = model_fw.replace('nan (nan)', np.NaN)
    model_fw = model_fw.sort_values(['k', 'bic_improvement'])
   
    # show the model summary
    logging.info('*** FINAL MODEL COMPARISON ***')
    logging.info(model_fw[['bic_improvement', 'cooc', 'w2v', 'hier']].iloc[1:])
   
    # print a LaTeX friendly version for the paper
    print(model_fw[['bic_improvement', 'cooc', 'w2v', 'hier']].iloc[1:].to_latex(na_rep=" ", float_format="%.3f"))
   

if __name__ == '__main__':
   
    initialise_logger()
   
    main(config)
