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

    def get_iteration_filename(self, temperature, iteration):
        """Returns the Excel file path for a given temperature and iteration."""
        temp_dir = self.get_temp_dir(temperature)
        return os.path.join(temp_dir, f"iter_{iteration}.xlsx")

    def get_config_filename(self):
        """Returns the Excel file path for the configuration settings."""
        return os.path.join(self.base_dir, "config.xlsx")

    def get_summary_filename(self):
        """Returns the Excel file path for the experiment summary."""
        return os.path.join(self.base_dir, "summary.xlsx")

    def save_to_excel(self, filepath, new_data, column_names=None):
        """Saves data to an Excel file.
        Args:
            "filepath" (str): The path to the Excel file.
            "new_data" (list of dicts): The data to be saved.
            "column_names" optional(list): The column names for the Excel file.
        """
        df = pd.DataFrame(new_data,columns=column_names)
        df.to_excel(filepath, index=False)
        print(f"Data saved to {filepath}")

