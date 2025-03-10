# LLM Temperature Optimisation

## Introduction

This repository contains code to test LLM anonymisation performance under different 
temperature values. The aim of this work is to assess the impact of temperature on the 
quality of the anonymisation process both in terms of metrics such as f1,recall, 
accuracy and precision but also context preservation with ROGUE.

## Installation

### Clone the repository

```bash
git clone https://github.com/KD-7/LLM-Temperature-Optimisation.git
```

### Experiment Configuration

The experiment can be configured in the [Configuration file](config.py). To export the 
results to a GitHub repository, you must specify the repository name, branch and auth token.

### Running the experiment

To run the experiment, set up a virtual environment and install the required dependencies as follows:


Example using python3.10:
```bash
pip install virtualenv
virtualenv -p python3.10 venv
source venv/bin/activate
# This is a workaround to install rogue-score package due to https://github.com/google-research/google-research/issues/2672
pip install https://files.pythonhosted.org/packages/e2/c5/9136736c37022a6ad27fea38f3111eb8f02fe75d067f9a985cc358653102/rouge_score-0.1.2.tar.gz
pip install .
python experiment.py
```

### Results

There are two methods of exporting the results:
- To your chosen GitHub repository into the [RESULTS.md](RESULTS.md) file on 
your chosen branch.
- They are also exported locally as Excel files in the directory specified
in [config.py](config.py).

*PLEASE NOTE: The previous experiment results will be overwritten in the Excel files!*

### Why LLama?
We chose to use LLama as it is a lightweight library that is easy to use and has a low 
computational overhead. This is important as the use case for this project is to conduct
anonymisation locally as part of a data donation pipeline, and therefore we cannot make 
assumptions about the participants' hardware. 

### Running the tests

To run the tests, run the following command:

```bash
pip install .[test]
pytest
```



