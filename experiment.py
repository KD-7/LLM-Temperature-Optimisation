# TODO run experiment here and evaluate against utils

from sklearn import metrics
from llm_temp_optimisation import datasets, models, utils


def get_all_metrics(results):
    """Returns a 5 - tuple of models results"""
    accuracy = metrics.get_recall_score(results.pre_anon, results.post_anon)
    precision = metrics.precision_score(results.pre_anon, results.post_anon)
    recall = metrics.recall_score(results.pre_anon, results.post_anon)
    f1_score = metrics.f1_score(results.pre_anon, results.post_anon)
    rogue_score = 0.0

    return accuracy, precision, recall, f1_score, rogue_score


# TODO run the models here import from models/config the temperature parameter?

def print_results():
    # TODO decide how to output results a table or Excel?
    pass


def run_experiment():
    # TODO run the experiment here
    # Here we process the DS and run the models, put it into results DS and then evaluate utils

    pass
