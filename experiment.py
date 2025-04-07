# This script runs an experiment using the LLama model on the AI4Privacy dataset.

import os
import random
import pandas as pd
from config import *
from temp_eval import datasets, models, utils
from temp_eval.metrics import Metrics
from temp_eval.utils import (FileHandler, draw_anonymisation_metrics,
                             draw_context_metrics, export_csv)

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

for temperature in TEMPERATURE_VALUES:

    rouge_1, rouge_2, rouge_l = 0, 0, 0
    precision, recall, f1 = 0, 0, 0
    for iteration in range(ITERATIONS):

        excel_iter_filepath = file_handler.get_iteration_filename(temperature,
                                                                  iteration + 1)

        sample_responses = []

        for data_point in range(DATA_POINTS):

            model_response = model.generate(source_text[data_point], temperature)
            r1, r2, rl = metrics.text_similarity_metrics(model_response,
                                                         target_text[data_point])
            rouge_1 += r1
            rouge_2 += r2
            rouge_l += rl

            p, r, f = metrics.anonymisation_metrics(model_response,
                                                    target_text[data_point],
                                                    privacy_mask[data_point])
            precision += p
            recall += r
            f1 += f

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
    rouge_1 /= total_data_points
    rouge_2 /= total_data_points
    rouge_l /= total_data_points
    precision /= total_data_points
    recall /= total_data_points
    f1 /= total_data_points

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
    # We are saving average results for each temperature value across all iterations
    summary.append(run_results)

# ==============
# SAVING RESULTS
# ==============
config_copy = config_settings.copy()
config_copy["TEMPERATURE_VALUES"] = str(TEMPERATURE_VALUES)

# Save the summary and configuration settings to Excel: OVERWRITES existing files!
file_handler.save_to_excel(file_handler.get_summary_filename(), summary)
file_handler.save_to_excel(file_handler.get_config_filename(), config_copy.items(),
                           column_names=["Key", "Value"])

# Save summary metrics to csv files: OVERWRITES existing files!
export_csv(summary, "summary.csv", SAVE_DIR)

# Draw and export charts as html
os.makedirs("visualisations", exist_ok=True)
df = pd.DataFrame(summary)
anon_scores = df[["Precision", "Recall", "F1"]].values.T.tolist()
rogue_scores = df[["ROUGE-1", "ROUGE-2", "ROUGE-L"]].values.T.tolist()
draw_anonymisation_metrics(TEMPERATURE_VALUES, anon_scores)
draw_context_metrics(TEMPERATURE_VALUES, rogue_scores)

if AUTH_TOKEN != "":
    utils.export_to_github(summary, REPO_PATH, BRANCH_NAME, AUTH_TOKEN,
                           header="## Experiment Summary",
                           commit_message="Export Summary")
    # Make the new lines show on Markdown
    config_copy["PROMPT"] = config_copy["PROMPT"].replace("\n", "<br>")
    key_value_pairs = [{'Key': k, 'Value': v} for k, v in config_copy.items()]
    utils.export_to_github(key_value_pairs, REPO_PATH, BRANCH_NAME, AUTH_TOKEN,
                           header="### Config Settings", commit_message="Export Config")
    
# ===========================================
# FINDING MEDIAN AND SAVING ITERATION RESULTS
# ===========================================
summary = []

for temperature in TEMPERATURE_VALUES:
    temp_dir = os.path.join(SAVE_DIR, f"temperature_{temperature}")
    iteration_scores = []

    for iteration in range(1, ITERATIONS + 1):
        iter_file = os.path.join(temp_dir, f"iter_{iteration}.xlsx")
        if not os.path.isfile(iter_file):
            print(f"File not found: {iter_file}")
            continue

        df = pd.read_excel(iter_file)

        # Average metrics across all rows in this iteration file
        avg_precision = df["Precision"].mean()
        avg_recall = df["Recall"].mean()
        avg_f1 = df["F1"].mean()
        avg_r1 = df["ROUGE-1"].mean()
        avg_r2 = df["ROUGE-2"].mean()
        avg_rl = df["ROUGE-L"].mean()

        iteration_scores.append({
            "Temperature": temperature,
            "Iteration": iteration,
            "Precision": avg_precision,
            "Recall": avg_recall,
            "F1": avg_f1,
            "ROUGE-1": avg_r1,
            "ROUGE-2": avg_r2,
            "ROUGE-L": avg_rl
        })

    if not iteration_scores:
        continue
    
    # Find median iteration by F1 and ROUGE-L 
    sorted_iterations = sorted(iteration_scores, key=lambda x: (x["F1"] + x["ROUGE-L"]) / 2)
    median_idx = len(sorted_iterations) // 2
    median_iteration = sorted_iterations[median_idx]
    summary.append(median_iteration)

# Export summary
summary_df = pd.DataFrame(summary)
summary_df.to_excel(os.path.join(SAVE_DIR, "median_summary.xlsx"), index=False)
summary_df.to_csv(os.path.join(SAVE_DIR, "median_summary.csv"), index=False)

# Save all iteration scores
summary_df = pd.DataFrame(summary)
summary_df.to_excel(os.path.join(SAVE_DIR, "iterations_summary.xlsx"), index=False)
summary_df.to_csv(os.path.join(SAVE_DIR, "iterations_summary.csv"), index=False)

print("Experiment completed successfully.")
