import kagglehub
import json

def download_ai4privacy_dataset():
    """Downloads the AI4Privacy dataset from Kaggle and returns the path to the dataset"""
    # Download latest version
    path = kagglehub.dataset_download("verracodeguacas/ai4privacy-pii")
    return path


def load_ai4privacy_dataset(path):
    """Loads the AI4Privacy dataset from the given path and returns the four data
    types as lists

    Args:
        path (str): The path to the AI4Privacy dataset

    Returns: A tuple of (masked_text, unmasked_text, token_entity_labels,
    tokenised_unmasked_text) the first two are one dimensional lists, and the last
    two are 2-dimensional lists

        - "masked_text" (list[str]): A list of texts with personally identifiable
        information (PII) replaced by placeholder tokens.

        - "unmasked_text" (list[str]): A list of original texts containing PII.

        - "token_entity_labels" (list[list[str]]): A list of lists, where each inner list
        contains entity labels corresponding to tokens in the text, identifying
        the type of PII ( e.g., "NAME", "EMAIL").

        - "tokenised_unmasked_text" (list[list[str]]): A list
        of lists, where each inner list is a tokenised version of an unmasked text,
        with each token corresponding to a word or subword unit.
    """

    # absolute path
    dataset_english_variant = path + "\pii-masking-65k\english_balanced_10k.jsonl"
    with open(dataset_english_variant, "r", encoding="utf-8") as f:
        data = [json.loads(line) for line in f]  # each line is a json object

    masked_text = [entry["masked_text"] for entry in data]
    unmasked_text = [entry["unmasked_text"] for entry in data]
    token_entity_labels = [entry["token_entity_labels"] for entry in data]
    tokenised_unmasked_text = [entry["tokenised_unmasked_text"] for entry in data]

    return masked_text, unmasked_text, token_entity_labels, tokenised_unmasked_text
