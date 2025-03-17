
from datasets import load_dataset


def download_ai4privacy_dataset(file_specifier=None, dataset_specifier=None):
    """Downloads and creates an instance of the dataset

    Args:
        file_specifier: Select specific files within the dataset
        dataset_specifier: Select a specific variant of the dataset e.g. test
        (validation) or train
        """
    # Download the latest version
    return load_dataset("ai4privacy/pii-masking-200k", data_files=file_specifier,
                        split=dataset_specifier)


def load_ai4privacy_dataset(dataset):
    """Loads the AI4Privacy dataset returns a tuple of lists

    Args:
        dataset: Instance of AI4Privacy dataset

    Returns: A tuple of (masked_text, unmasked_text, token_entity_labels,
    tokenised_unmasked_text)

        - "source_text" (list[str]): A list of original texts containing PII.

        - "target_text" (list[str]): A list of texts with personally identifiable
        information (PII) replaced by placeholder tokens, serving as the ground truth.

        - "privacy_mask" (list[str]): A list containing entity labels
        corresponding to tokens in the text, identifying
        the type of PII ( e.g., "NAME", "EMAIL").
    """
    source_text = [entry["source_text"] for entry in dataset]
    target_text = [entry["target_text"] for entry in dataset]
    privacy_mask = [entry["privacy_mask"] for entry in dataset]

    return source_text, target_text, privacy_mask
