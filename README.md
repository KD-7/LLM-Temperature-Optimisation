# LLM Temperature Optimisation

## Introduction

This repository contains code to test LLM anonymisation performance under different 
temperature values. The aim of this work is to assess the impact of temperature on the 
quality of the anonymisation process both in terms of metrics such as f1,recall, 
accuracy and precision but also context preservation with ROGUE.

## Experiment Setup

### Clone the repository

```bash
git clone https://github.com/KD-7/LLM-Temperature-Optimisation.git
```

### Experiment Configuration

The experiment can be configured in the [Configuration file](config.py). To export the 
results to a GitHub repository, you must specify the repository name, branch and auth token.

### Ollama Installation

To install Ollama, visit the [Ollama website](https://ollama.com/download), select your Operating 
system and follow the instructions.

### Creating a virtual environment

It is recommended to create a virtual environment to run the experiment. This will 
ensure that the dependencies do not interfere with other projects you may be working on.
These conflicts may result in incorrect results or errors.

*If you have already set one up, then make sure to activate it before running the experiment or tests!*

Example shown for python3.10:
```bash
pip install virtualenv
virtualenv -p python3.10 venv
source venv/bin/activate
```

### Installing the dependencies

First, ensure that you have followed the steps above to [create and activate virtual environment](#creating-a-virtual-environment).
Then run the following commands:

```bash 
# This is a workaround to install rogue-score package due to https://github.com/google-research/google-research/issues/2672
pip install https://files.pythonhosted.org/packages/e2/c5/9136736c37022a6ad27fea38f3111eb8f02fe75d067f9a985cc358653102/rouge_score-0.1.2.tar.gz
pip install .
```

## Running the experiment

Open another terminal and start Ollama with:
```bash
ollama serve
```
Alternatively, you can open the ollama desktop app.

Then in the original terminal, run the following commands in your virtual environment:
```bash 
python experiment.py
```

### Results

There are three methods of exporting the results:
- To your chosen GitHub repository into the [RESULTS.md](RESULTS.md) file on 
your chosen branch.
- They are also exported locally as Excel files in the directory specified
in [config.py](config.py).
- As a CSV file in the directory specified in [config.py](config.py).

Any graphs generated can be found in the visualisations' directory.

*PLEASE NOTE: The previous experiment results will be overwritten in the Excel files!*

## Why LLama?
We chose to use LLama as it is a lightweight library that is easy to use and has a low 
computational overhead. This is important as the use case for this project is to conduct
anonymisation locally as part of a data donation pipeline, and therefore we cannot make 
assumptions about the participants' hardware. 

## Running the tests

To run the tests, make sure you are running in a virtual instance otherwise 
you may come across errors. See [Creating a virtual environment](#creating-a-virtual-environment).

Then run the following commands:

```bash
pip install .[test]
#If coming across module not found errors, then run python -m pytest temp_eval
pytest temp_eval
```



