import sys

# For exporting results to GitHub
AUTH_TOKEN = "" # Put YOUR_GITHUB_AUTH_TOKEN in the ""
REPO_PATH = "KD-7/LLM-Temperature-Optimisation"
BRANCH_NAME = "results"

# Experiment Configuration
TEMPERATURE_VALUES = [0.001, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
DATA_POINTS = 5 # Change to 40000 for full dataset
SAMPLE_POINTS = 5  # The no. of entries to collect for survey sample
ITERATIONS = 1
SAVE_DIR = "results"
MODEL_NAME = "llama3"
PROMPT = (
            "You are an advanced anonymiser that replaces personally identifiable "
            "information (PII) with a category label. Your task is to:\n"
            "1) Replace PII with its category in square brackets\n"
            "2) Preserve the context and utility of the original input\n"
            "Example:\n"
            "Input: My name is Alice and I live in London.\n"
            "Output: My name is [NAME] and I live in [LOCATION]."
        )
RANDOM_SEED = 42
PYTHON_VERSION = sys.version_info

config_settings = {
    "TEMPERATURE_VALUES": TEMPERATURE_VALUES,
    "DATA_POINTS": DATA_POINTS,
    "SAMPLE_POINTS": SAMPLE_POINTS,
    "ITERATIONS": ITERATIONS,
    "SAVE_DIR": SAVE_DIR,
    "MODEL_NAME": MODEL_NAME,
    "PROMPT": PROMPT,
    "RANDOM_SEED": RANDOM_SEED,
    "PYTHON_VERSION": PYTHON_VERSION
}
