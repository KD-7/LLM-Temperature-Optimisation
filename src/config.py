import os

DATA_POINTS = 5  # Change to 40000 for full dataset
ITERATIONS = 5
SAVE_DIR = "results"
MODEL_NAME = "llama3"
TEMPERATURE_VALUES = [0.2, 0.4, 0.6, 0.8, 1.0]

# Ensure save directory exists
os.makedirs(SAVE_DIR, exist_ok=True)
