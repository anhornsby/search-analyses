# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""Main entrypoint to analyses code"""

import sys
import argparse

from memory_analyses.retrieval_model import main as mle_main
from config.retrieval import config as mle_config

from memory_analyses.utilities.logging import initialise_logger

def parse_args():
    """Initialise the argument parser"""

    parser = argparse.ArgumentParser(description='Perform analyses on semantic fluency data, using product embeddings')
    subparsers = parser.add_subparsers(dest='command')
   
    group1 = subparsers.add_parser('fit', help='Fit the retrieval model comparisons to the experimental data')
    group1.add_argument('condition', choices=['all', 'collapse', 'first'], help='Which dataset would you like to perform the model comaprison for?')
   
    args = parser.parse_args()
   
    return args

def determine_test(test, args):
    """Determine which test to run"""
   
    if test == 'fit':
        mle_config['condition'] = args.condition
        mle_main(mle_config)
   
    else:
        raise NotImplementedError

def main(args):
    """main entrypoint for code"""
   
    # initialise a logger
    initialise_logger()
   
    # determine which test to run
    determine_test(args.command, args)
   
   
if __name__ == '__main__':
   
    args = parse_args()
   
    main(args)
