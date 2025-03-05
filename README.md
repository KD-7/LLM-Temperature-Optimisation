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

### Setup the environment

Example using python3.10:
```bash
pip install virtualenv
virtualenv -p python3.10 venv
source venv/bin/activate
python experiment.py
```

You will need to provide your GitHub token in the experiment file to allow the results 
to be pushed to your repository.
### Results

Are exported to your chosen GitHub repository into the [RESULTS.md](RESULTS.md) file on 
the chosen branch

### Why LLama?
We chose to use LLama as it is a lightweight library that is easy to use and has a low 
computational overhead. This is important as the use case for this project is to conduct
anonymisation locally as part of a data donation pipeline, and therefore we cannot make 
assumptions about the participants' hardware. 

### Deploy LLama3 locaally
1. go to https://ollama.com and choose your OS version for downloading and installing

2. try `ollama --verison` in terminal, if that works, go to next step. If not, you need to manually add Ollama to the PATH Environment Variables. Here is an example for Windows. Press `Win + R` and type `sysdm.cpl`. Go to the **Advanced** tab and click **Environment Variables**. Under **System Variables**, find and select **Path**, then click **Edit**. Click **New**, then add the absolute path of ollama (e.g. C:\Program Files\Ollama\). After these steps, try `ollama --version` again.

3. In terminal, type `ollama pull llama3`. Then llama3 will be installed automatically.

