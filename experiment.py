# This script runs an experiment using the LLama model on the AI4Privacy dataset.

import random
from config import *
from tempeval import datasets, models, utils
from tempeval.utils import FileHandler

# Set random seed for reproducibility
random.seed(RANDOM_SEED)

# Dataset configuration
dataset = datasets.download_ai4privacy_dataset("english_pii_43k.jsonl", "train")
source_text, target_text, privacy_mask = datasets.load_ai4privacy_dataset(dataset)

DATA_SET_SIZE = len(dataset)

# Used to collect a random sample of results for survey
RANDOM_SAMPLE_INDICES = random.sample(range(DATA_SET_SIZE), SAMPLE_POINTS)

# Model configuration
model = models.LLama(MODEL_NAME, PROMPT)

file_handler = FileHandler(SAVE_DIR)

for temperature in TEMPERATURE_VALUES:

    iteration_results = []
    for iteration in range(ITERATIONS):

        excel_filepath = file_handler.get_excel_filename(temperature, iteration)
        file_handler.initialize_excel_file(excel_filepath)

        rogue_1, rogue_2, rogue_l = 0, 0, 0
        precision, recall, f1 = 0, 0, 0

        sample_responses = []

        for data_point in range(DATA_POINTS):

            model_response = utils.sanitise_response(model.chat(source_text[data_point],
                                                                temperature))

            r1, r2, rl = utils.text_similarity_metrics(model_response[data_point],
                                                       target_text[data_point])
            rogue_1 += r1; rogue_2 += r2; rogue_l += rl

            p, r, f = utils.anonymisation_metrics(model_response[data_point],
                                                  target_text[data_point],
                                                  privacy_mask[data_point])
            precision += p; recall += r; f1 += f

            if data_point in RANDOM_SAMPLE_INDICES:
                sample_responses.append({
                    'Source text': source_text[data_point],
                    'Ground truth': target_text[data_point],
                    'Model response': model_response,
                    'Precision': p,
                    'Recall': r,
                    'F1': f,
                    'ROUGE-1': r1,
                    'ROUGE-2': r2,
                    'ROUGE-L': rl
                })

        # Average over all data points
        rogue_1 /= DATA_POINTS; rogue_2 /= DATA_POINTS; rogue_l /= DATA_POINTS
        precision /= DATA_POINTS; recall /= DATA_POINTS; f1 /= DATA_POINTS

        run_results = {
            'Run': iteration,
            'Temperature': temperature,
            'Precision': precision,
            'Recall': recall,
            'F1': f1,
            'ROUGE-1': rogue_1,
            'ROUGE-2': rogue_2,
            'ROUGE-L': rogue_l
        }
        # TODO differentiate saving sample results and overall results
        # TODO export configs to excel
        # TODO: SAVING SUMMARY OF RUN TO EXCEL
        file_handler.save_results_to_excel(excel_filepath, sample_responses)

        iteration_results.append(run_results)

    utils.export_results_github(iteration_results, temperature, REPO_PATH,
                                BRANCH_NAME,
                                AUTH_TOKEN)
    # TODO: define config
    utils.export_config_github(config_settings, REPO_PATH, BRANCH_NAME, AUTH_TOKEN)

print("Experiment completed successfully.")
