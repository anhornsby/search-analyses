"""Logging functionality"""

import sys
import csv
import os
import logging

def initialise_logger():
    """Initialise logger to print messages to stdout"""

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

class ResultsLogger(object):
    """
    Log results of model fits to a CSV on disk
    """
    def __init__(self, filepath):
        super(ResultsLogger, self).__init__()
        self.filepath = filepath
       
    def _write_row_to_csv(self, values):
        """Write values to the logger csv"""
       
        with open(self.filepath, 'a') as fp:
            a = csv.writer(fp, delimiter=',')
            a.writerow(values)
       
    def create_if_not_exists(self):
        """Create a logging file"""
       
        if not os.path.isfile(self.filepath):
            self._write_row_to_csv(['Datetime',
                                  'Analysis',
                                  'Model Name',
                                  'Model',
                                  'Parameters',
                                  'Environment',
                                  'Results',
                                  'Artifacts'])
        else:
            pass

    def add(self, datetime, analysis, model_name, model, parameter, environment, results, artifacts):
        """Write a row of results to the results log"""
       
        self._write_row_to_csv([datetime, analysis, model_name, model, parameter, environment, results, artifacts])
