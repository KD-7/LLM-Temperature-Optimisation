# LLM Temperature Optimisation

## Introduction

This respository contains code to test LLM anonymisation performance under different temperature values. The aim of this work is to assess
the impact of temperature on the quality of the anonymisation process both in terms of metrics such as f1,recall,accuracy and precision but also context preservation.

## Installation

### Clone the repository

```bash
git clone https://github.com/KD-7/LLM-Temperature-Optimisation.git
```

### Setup the environment

```bash
pip install virtualenv
virtualenv -p python3.10 venv
source venv/bin/activate
python experiment.py
```

### Results

Are output into the [RESULTS.md](RESULTS.md) file.

### Why LLama?
We chose to use LLama as it is a lightweight library that is easy to use and has a low computational overhead. This is important as the use case for this project is to conduct anonymisation locally as part of a data donation pipeline, and therefore we cannot make assumptions about the participants hardware. 

