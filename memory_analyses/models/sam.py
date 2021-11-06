"""SAM retrieval model"""

import pandas as pd
import numpy as np

class MultiProbeRetrievalModel(object):
    """
    Fit the SAM/ACT-R model with multiple representations of similarity

    Arguments:
        probe_configs (list): A list of BaseProbeConfig objects describing the similarity cues to use
        optimiser (memory_analyses.models.optimise): A class that performs minimisation (see ScipyMinimiser)
        loss_func (memory_analyses.models.loss): Usually the negative_log_likelihood
        init_probe_weights (list): Values to initialise the attention weights to (wont change if learn_weights is False)
        learn_weights (bool): Whether or not to learn attention weights for the similarity probes
        jitter_val (float): A small number to add to negative or 0 similarity values

    """

    def __init__(
        self,
        probe_configs: list,
        optimiser=None,
        loss_func=None,
        init_probe_weights: list = None,
        learn_weights: bool = False,
        jitter_val: float = 1.0e-7,
    ):
        super(MultiProbeRetrievalModel, self).__init__()
        self.probe_configs = probe_configs
        self.optimiser = optimiser
        self.loss_func = loss_func
        self.init_probe_weights = init_probe_weights
        self.learn_weights = learn_weights
        self.jitter_val = jitter_val

        if not learn_weights:
            assert len(probe_configs) == len(init_probe_weights)

    def get_probe_paths(self):
        """Get the paths to the probes"""

        return [p.get_probe_path() for p in self.probe_configs]

    def get_probes(self):
        """Get the probe objects"""

        return self.probe_configs

    def get_current_cols(self):
        """Get the name being used for the current column"""

        return [p.get_current_col() for p in self.probe_configs]

    def get_subsequent_cols(self):
        """Get the name being used for the subsequent column"""

        return [p.get_subsequent_col() for p in self.probe_configs]

    def get_params(self):
        """Get model parameters and return as dictionary"""

        return self.__dict__

    def _attention_weighted_probe_product(self, sims, a_weights):
        """Calculate the model numerator"""

        sims = np.column_stack(sims)

        # replace any missing entries with 0
        sims[sims == ""] = "0.0"

        sims = sims.astype(float)

        if self.jitter_val is not None:
            # add a small constant to all probes to ensure that nothing is ever 0
            sims += self.jitter_val

        # apply the attention weights
        sims = np.power(sims, a_weights) # np.ma.power(sims, a_weights)  # each weight pertains to a column

        # calculate the product over each probe
        return sims.prod(axis=1)

    def _calculate_denominator_product_helper(self, cols, a_weights):
        """Helper function to extract the remaining product sims and calculate the probe values from them"""

        # extract the probe values
        # these are string values, which need to be replaced with floating points
        probes = [
            np.array(
                " ".join(x.replace("[", "").replace("]", "").split()).split(" ")
            ).astype(float)
            for x in cols
        ]

        # the numerator (product of weighted probes for current basket add)
        denom = self._attention_weighted_probe_product(probes, a_weights)

        sumprod = denom.sum()  # sum the probe products for the remaining items

        return sumprod

    def _determine_retrieval_strengths(
        self, current_sims, subs_sims, a_weights
    ):
        """
        Calculate the retrieval strengths for each item in a sequence
        (assumes data is already ordered)
        """

        # the numerator (product of weighted probes for current basket add)
        num = self._attention_weighted_probe_product(
            current_sims, a_weights
        )

        # the denominator (product of weighted probes for remaining products to be added)
        for x in range(len(subs_sims)):
            subs_sims[x] = np.nan_to_num(subs_sims[x], "[0.0]")
            subs_sims[x][subs_sims[x] == " "] = "[0.0]"

        denom = [
            self._calculate_denominator_product_helper(
                [probe[x] for probe in subs_sims], a_weights
            )
            for x in range(subs_sims[0].shape[0])
        ]

        # get retrieval strength of current item, given that and remaining items
        rs = num / denom

        # an array of numbers between 0 and 1 where higher = higher likelihood of current choice
        rs = np.nan_to_num(rs, 0, nan=0, neginf=0, posinf=1)
       
        return rs

    def _fit_and_evaluate(self, a_weights, current_sims, subs_sims):
        """Fit and evaluate a retrieval strength model given a set of weights"""

        rs = self._determine_retrieval_strengths(
            current_sims, subs_sims, a_weights
        )

        # feed in the likelihoods and calculate the loss
        loss = self.loss_func(rs)

        return loss

    def fit(self, current_sims, subs_sims):
        """
        Fit the model to the similarities from a given visit and return the loss
       
        Args:
            current_sims (list): A list of similarity cues representing the similarity between the current
                and next product (i.e. the numerator in the SAM equation)
            subs_sims (list): A list of similarity cues representing the similarity between the current
                and remaining products (i.e. the denominator in the SAM equation)
        Returns:
            (float): The loss
            (list): The best fitting attention weights
            (bool): Whether or not the optimisation converged
        """

        # estimate weights using the optimiser
        if self.learn_weights:
            res = self.optimiser.minimise(
                self._fit_and_evaluate, args=(current_sims, subs_sims)
            )

            weights = res.x
            loss = res.fun
            success = res.success

        # otherwise use some default set of attention weights
        else:
            weights = self.init_probe_weights
            loss = self._fit_and_evaluate(weights, current_sims, subs_sims)
            success = True

        return loss, weights, success
