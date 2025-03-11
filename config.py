import sys

# For exporting results to GitHub
AUTH_TOKEN = "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" # Put YOUR_GITHUB_AUTH_TOKEN in the ""
REPO_PATH = "KD-7/LLM-Temperature-Optimisation"
BRANCH_NAME = "results"

# Experiment Configuration
TEMPERATURE_VALUES = [0.2]
DATA_POINTS = 100  # Change to 40000 for full dataset
SAMPLE_POINTS = 100  # The no. of entries to collect for survey sample
ITERATIONS = 1
SAVE_DIR = "results"
MODEL_NAME = "llama3"
PROMPT = (
            "You are an advanced anonymizer that replaces personally identifiable "
            "information (PII) with a category label. You will NOT paraphrase or "
            "change any part of the text except for replacing PII with its category in square brackets.\n\n"

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