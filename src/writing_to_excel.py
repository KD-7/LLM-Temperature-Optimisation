import pandas as pd
from datasets import load_dataset
import ollama
from rouge_score import rouge_scorer
import os

# Constants
DATA_POINTS = 10  # Change to 40000 for full dataset
ITERATIONS = 1
SAVE_DIR = "results"

# Ensure save directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

# Load dataset
dataset = load_dataset("ai4privacy/pii-masking-200k", data_files="english_pii_43k.jsonl")

# Define temperature values
temperature_values = [0.1]

# Load Llama model and instruction
model = "llama3"
instruction = (
    "You are an advanced anonymiser that anonymises text through categorisation. "
    "You will replace all personally identifiable information (PII) with its category in ALL CAPITAL LETTERS. "
    "DO NOT paraphrase the text; keep it exactly the same. Only replace the PII with its category.\n\n"
    "**Example Input:**\n"
    '"My name is Alice, I live in London, and I am 25 years old."\n\n'
    "**Example Output:**\n"
    '"My name is [NAME], I live in [LOCATION], and I am [AGE] years old."'
)

# Initialize ROUGE scorer
scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

# Loop through temperature and iterations
for temp in temperature_values:
    # Create a folder for this temperature inside experiment_results
    temp_dir = os.path.join(SAVE_DIR, f"temperature_{temp}")
    os.makedirs(temp_dir, exist_ok=True)
    
    for iter_num in range(ITERATIONS):
        # Define filename inside the temperature folder
        excel_filename = os.path.join(temp_dir, f"iter_{iter_num+1}.xlsx")
        # print("Excel_filename: ", excel_filename)  # Debugging print statement

        # Ensure file exists before appending
        if not os.path.exists(excel_filename):
            pd.DataFrame(columns=[
                'Raw text', 'Ground truth', 'Anonymised text', 
                "Precision", "Recall", "F1",
                'ROUGE-1', 'ROUGE-2', 'ROUGE-L'
            ]).to_excel(excel_filename, index=False)

        # Read existing data if the file exists
        if os.path.exists(excel_filename):
            existing_df = pd.read_excel(excel_filename)
        else:
            existing_df = pd.DataFrame()

        data_list = []  # Store results for this temperature & iteration

        for data_point in range(DATA_POINTS):
            raw_text = dataset["train"][data_point]["source_text"]
            ground_truth = dataset["train"][data_point]["target_text"]

            # Call LLAMA model
            stream = ollama.chat(
                model=model,
                messages=[
                    {'role': 'system', 'content': instruction},
                    {'role': 'user', 'content': raw_text}
                ],
                stream=True,
                options={'temperature': temp}
            )

            # Collect the response
            llm_output = ""
            for chunk in stream:
                llm_output += chunk.get('message', {}).get('content', '')

            # Compute ROUGE scores
            scores = scorer.score(ground_truth, llm_output)
            rouge_1 = scores['rouge1'].fmeasure
            rouge_2 = scores['rouge2'].fmeasure
            rouge_l = scores['rougeL'].fmeasure

            # Placeholder for future precision/recall calculations
            precision, recall, f1_score = 0, 0, 0

            # Append data to list
            data_list.append({
                'Raw text': raw_text,
                'Ground truth': ground_truth,
                'Anonymised text': llm_output,
                'Precision': precision,
                'Recall': recall,
                'F1': f1_score,
                'ROUGE-1': rouge_1,
                'ROUGE-2': rouge_2,
                'ROUGE-L': rouge_l
            })
            
            print(f"Data Point {data_point+1} Completed")

        # Only write to Excel if data was collected
        if data_list:
            # Convert list to DataFrame
            new_df = pd.DataFrame(data_list)

            # Append new data to existing DataFrame
            if not existing_df.empty:
                new_df = pd.concat([existing_df, new_df], ignore_index=True)

            # Write the updated DataFrame back to the file
            with pd.ExcelWriter(excel_filename, engine='openpyxl', mode='w') as writer:  
                new_df.to_excel(writer, sheet_name="Results", index=False, header=True)

            print(f"Results saved to {excel_filename}")
        else:
            print(f"Warning: No data was written for temp={temp}, iter={iter_num+1}")

"""
TODO:
- Implement precision, recall, and F1 calculation
- Optimize LLM processing for large datasets (40k points)
- Finalise the prompt

Bugs:
"""
