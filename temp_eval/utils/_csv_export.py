import pandas as pd


def export_csv(results, filename, save_dir="results/") -> None:
    """
    Exports the given results to a CSV file with the specified filename.

    Args:
    - results (dict): experimental results to be saved
    - filename (str): name of destination file including .csv
    - save_dir (str): save directory
    """
    df = pd.DataFrame(results)
    df.to_csv(save_dir + filename, index=False)
