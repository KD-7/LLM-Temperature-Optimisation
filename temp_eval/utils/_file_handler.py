import os
import pandas as pd


class FileHandler:
    """Handles file operations for experiment results."""

    def __init__(self, base_dir="results"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def get_temp_dir(self, temperature):
        """Returns the directory path for a specific temperature setting."""
        temp_dir = os.path.join(self.base_dir, f"temperature_{temperature}")
        os.makedirs(temp_dir, exist_ok=True)
        return temp_dir

    def get_results_filename(self, temperature, iteration):
        """Returns the Excel file path for a given temperature and iteration."""
        temp_dir = self.get_temp_dir(temperature)
        return os.path.join(temp_dir, f"iter_{iteration + 1}.xlsx")

    def get_config_filename(self):
        """Returns the Excel file path for the configuration settings."""
        return os.path.join(self.base_dir, "config.xlsx")

    def initialize_excel_file(self, filepath):
        #TODO: may be duplicate!
        """Creates an Excel file with required columns if it doesn't exist."""
        if not os.path.exists(filepath):
            df = pd.DataFrame(columns=[
                'Source text', 'Ground truth', 'Model Response',
                'Precision', 'Recall', 'F1',
                'ROUGE-1', 'ROUGE-2', 'ROUGE-L'
            ])
            df.to_excel(filepath, index=False)

    def read_existing_data(self, filepath):
        """Reads existing Excel data if the file exists, otherwise returns an empty DataFrame."""
        if os.path.exists(filepath):
            return pd.read_excel(filepath)
        return pd.DataFrame()

    def save_results_to_excel(self, filepath, new_data):
        """Appends new experiment results to an Excel file."""
        existing_data = self.read_existing_data(filepath)

        if not existing_data.empty:
            new_df = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            new_df = pd.DataFrame(new_data)

        with pd.ExcelWriter(filepath, engine='openpyxl', mode='w') as writer:
            new_df.to_excel(writer, sheet_name="Results", index=False, header=True)

        print(f"Results saved to {filepath}")

    def save_config_to_excel(self, filepath, config):
        """Saves the configuration settings to an Excel file."""
        df = pd.DataFrame(config.items(), columns=["Parameter", "Value"])
        df.to_excel(filepath, index=False)
        print(f"Config saved to {filepath}")

    def save_summary_to_excel(self, filepath, summary):
        """Saves the summary of the experiment to an Excel file."""
        df = pd.DataFrame(summary)
        df.to_excel(filepath, index=False)
        print(f"Summary saved to {filepath}")
