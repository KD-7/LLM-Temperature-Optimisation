# This script runs an experiment using the LLama model on the AI4Privacy dataset.

import os
import random
from config import *
from temp_eval import datasets, models, utils
from temp_eval.metrics import Metrics
from temp_eval.utils import FileHandler, _visualization

# Set random seed for reproducibility
random.seed(RANDOM_SEED)

# Ensure save directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

# Dataset configuration
dataset = datasets.download_ai4privacy_dataset("english_pii_43k.jsonl", "train")
source_text, target_text, privacy_mask = datasets.load_ai4privacy_dataset(dataset)


# Used to collect a random sample of results for survey
RANDOM_SAMPLE_INDICES = random.sample(range(DATA_POINTS), SAMPLE_POINTS)

# Model configuration

# Set the environment variable for Ollama
os.environ["OLLAMA_HOST"] = "0.0.0.0:11434"
model = models.LLama(MODEL_NAME, PROMPT)

metrics = Metrics()
file_handler = FileHandler(SAVE_DIR)
summary = []
f1_scores = []
rouge_1_scores = []
rouge_2_scores = []
rouge_l_scores = []

for temperature in TEMPERATURE_VALUES:

    rouge_1, rouge_2, rouge_l = 0, 0, 0
    precision, recall, f1 = 0, 0, 0
    for iteration in range(ITERATIONS):

        excel_iter_filepath = file_handler.get_iteration_filename(temperature, iteration + 1)

        sample_responses = []

        for data_point in range(DATA_POINTS):
                                                                
            model_response = model.generate(source_text[data_point], temperature)
            r1, r2, rl = metrics.text_similarity_metrics(model_response,
                                                       target_text[data_point])
            rouge_1 += r1; rouge_2 += r2; rouge_l += rl

            p, r, f = metrics.anonymisation_metrics(model_response,
                                                  target_text[data_point],
                                                  privacy_mask[data_point])
            precision += p; recall += r; f1 += f

            if data_point in RANDOM_SAMPLE_INDICES:
                sample_responses.append({
                    'Source text': source_text[data_point],
                    'Ground truth': target_text[data_point],
                    'Model Response': model_response,
                    'Precision': p,
                    'Recall': r,
                    'F1': f,
                    'ROUGE-1': r1,
                    'ROUGE-2': r2,
                    'ROUGE-L': rl
                })

        file_handler.save_to_excel(excel_iter_filepath, sample_responses)

    total_data_points = DATA_POINTS * ITERATIONS
    # Average over all data points and iterations
    rouge_1 /= total_data_points; rouge_2 /= total_data_points; rouge_l /= total_data_points
    precision /= total_data_points; recall /= total_data_points; f1 /= total_data_points

    # The results for this temperature parameter averaged over all iterations
    run_results = {
        'Iteration Count': ITERATIONS,
        'Temperature': temperature,
        'Precision': precision,
        'Recall': recall,
        'F1': f1,
        'ROUGE-1': rouge_1,
        'ROUGE-2': rouge_2,
        'ROUGE-L': rouge_l
    }

    summary.append(run_results)
    f1_scores.append(f1)
    rouge_1_scores.append(rouge_1)
    rouge_2_scores.append(rouge_2)
    rouge_l_scores.append(rouge_l)


config_copy = config_settings.copy()
config_copy["TEMPERATURE_VALUES"] = str(TEMPERATURE_VALUES)

# Save the summary and configuration settings to Excel, these will OVERWRITE existing files!
file_handler.save_to_excel(file_handler.get_summary_filename(), summary)
file_handler.save_to_excel(file_handler.get_config_filename(), config_copy.items(),
                           column_names=["Key","Value"])

# draw the charts and save the charts as html format to ./temp_eval/utils/charts directory
os.makedirs("./temp_eval/utils/charts", exist_ok=True)
_visualization.draw_chart_temp_f1(TEMPERATURE_VALUES, f1_scores)
_visualization.draw_chart_temp_rouge(TEMPERATURE_VALUES, rouge_1_scores, rouge_2_scores, rouge_l_scores)


if AUTH_TOKEN != "":
    utils.export_to_github(summary, REPO_PATH,BRANCH_NAME,AUTH_TOKEN,
                           header="## Experiment Summary",commit_message="Export Summary")
    # Make the new lines show on Markdown
    config_copy["PROMPT"] = config_copy["PROMPT"].replace("\n", "<br>")
    key_value_pairs = [{'Key': k, 'Value': v} for k, v in config_copy.items()]
    utils.export_to_github(key_value_pairs, REPO_PATH, BRANCH_NAME, AUTH_TOKEN,
                           header="### Config Settings", commit_message="Export Config")


print("Experiment completed successfully.")