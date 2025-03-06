import random
import pandas as pd
from datasets import load_dataset
from metrics_oop import Metrics
from config import DATA_POINTS, ITERATIONS, TEMPERATURE_VALUES
from FileHandler import FileHandler
from LLMModel import LLMModel

class Experiment:
    """Manages the anonymization experiment process."""

    def __init__(self):
        self.dataset = self.load_dataset()
        self.dataset_size = len(self.dataset["train"])
        self.metrics = Metrics()
        self.file_handler = FileHandler()
        self.llm_model = LLMModel()
        random.seed(42)  # Set seed for reproducibility
        self.sampled_indices = random.sample(range(self.dataset_size), DATA_POINTS) # Randomly sample data points

    def load_dataset(self):
        """Loads the anonymization dataset."""
        return load_dataset("ai4privacy/pii-masking-200k", data_files="english_pii_43k.jsonl")

    def process_data_point(self, raw_text, ground_truth, privacy_mask, temperature):
        """Processes a single data point, calling the model and computing metrics."""
        # Call LLM model
        llm_output = self.llm_model.anonymize_text(raw_text, temperature)

        # Compute Scores
        rouge_1, rouge_2, rouge_l = self.metrics.text_similarity_metrics(llm_output, ground_truth)
        precision, recall, f1 = self.metrics.anonymisation_metrics(llm_output, ground_truth, privacy_mask)

        return {
            'Raw text': raw_text,
            'Ground truth': ground_truth,
            'Anonymised text': llm_output,
            'Precision': precision,
            'Recall': recall,
            'F1': f1,
            'ROUGE-1': rouge_1,
            'ROUGE-2': rouge_2,
            'ROUGE-L': rouge_l
        }

    def run_experiment(self, temperature, iter_num):
        """Runs a single iteration of the experiment for a given temperature."""
        excel_filename = self.file_handler.get_excel_filename(temperature, iter_num)
        self.file_handler.initialize_excel_file(excel_filename)

        data_list = []

        for data_point in self.sampled_indices:
            raw_text = self.dataset["train"][data_point]["source_text"]
            ground_truth = self.dataset["train"][data_point]["target_text"]
            privacy_mask = self.dataset["train"][data_point]["privacy_mask"]

            result = self.process_data_point(raw_text, ground_truth, privacy_mask, temperature)
            data_list.append(result)

            print(f"Data Point {data_point+1} Completed")

        # Save results
        if data_list:
            self.file_handler.save_results_to_excel(excel_filename, pd.DataFrame(data_list))
        else:
            print(f"Warning: No data written for temp={temperature}, iter={iter_num+1}")

    def run(self):
        """Runs the entire experiment across all temperatures and iterations."""
        for temp in TEMPERATURE_VALUES:
            for iter_num in range(ITERATIONS):
                self.run_experiment(temp, iter_num)
