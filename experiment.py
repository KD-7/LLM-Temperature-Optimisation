# This script runs an experiment using the LLama model on the AI4Privacy dataset.

import os
import random
import pandas as pd
from tempeval import datasets, models, utils
from tempeval.utils import FileHandler

# For exporting results to GitHub
AUTH_TOKEN = "YOUR_GITHUB_AUTH_TOKEN"
REPO_PATH = "YOUR_GITHUB_REPO_PATH"
BRANCH_NAME = "main"

# Experiment configuration
TEMPERATURE_VALUES = [0.2, 0.4, 0.6, 0.8, 1.0]
DATA_POINTS = 5  # Change to 40000 for full dataset
ITERATIONS = 5
SAVE_DIR = "results"
MODEL_NAME = "llama3"  # what about 3.1?? check the params
PROMPT = "put the prompt here"
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# Ensure save directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

# Dataset configuration
dataset = datasets.download_ai4privacy_dataset("english_pii_43k.jsonl", "train")
source_text, target_text, privacy_mask = datasets.load_ai4privacy_dataset(dataset)

DATA_SET_SIZE = len(dataset)
RANDOM_SAMPLE_INDICES = random.sample(range(DATA_SET_SIZE), DATA_POINTS)
GROUND_TRUTH = [target_text[i] for i in RANDOM_SAMPLE_INDICES]

# Model configuration
model = models.LLama(MODEL_NAME, PROMPT)

for temperature in TEMPERATURE_VALUES:

    # Create a new file handler for each temperature setting [CHECK THSI!!!!!HIS
    file_handler = FileHandler(SAVE_DIR)
    excel_filepath = file_handler.get_excel_filename(temperature, 0)
    file_handler.initialize_excel_file(excel_filepath)

    iteration_results = []
    for iteration in range(ITERATIONS):

        model_response = []
        excel_filepath = FileHandler.get_excel_filename(temperature, iteration)
        FileHandler.initialize_excel_file(excel_filepath)

        for data_point in RANDOM_SAMPLE_INDICES:
            model_response.append(model.chat(source_text[data_point], temperature))

        # TODO: the metrics does it one by one , so i need to chang ehere to only input one resposne
        rogue_1, rogue_2, rogue_l = utils.text_similarity_metrics(model_response,
                                                                  GROUND_TRUTH)
        precision, recall, f1 = utils.anonymisation_metrics(model_response,
                                                            target_text[data_point])

        run_results = pd.DataFrame({
            'Raw text': source_text[RANDOM_SAMPLE_INDICES],
            'Ground truth': GROUND_TRUTH,
            'Anonymised text': model_response,
            'Precision': precision,
            'Recall': recall,
            'F1': f1,
            'ROUGE-1': rogue_1,
            'ROUGE-2': rogue_2,
            'ROUGE-L': rogue_l
        })
        # TODO: why no accuracy score?
        FileHandler.save_results_to_excel(excel_filepath, run_results)

        iteration_results.append(run_results)

    utils.export_results_to_github(iteration_results, temperature, REPO_PATH,
                                   BRANCH_NAME,
                                   AUTH_TOKEN)

print("Experiment completed successfully.")
