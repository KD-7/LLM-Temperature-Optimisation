import pandas as pd
import os


def export_csv(results, filename, save_dir) -> None:
    """
    Exports the given results to a CSV file with the specified filename.

    Args:
    - results (dict): experimental results to be saved
    - filename (str): name of destination file including .csv
    - save_dir (str): save directory
    """
    df = pd.DataFrame(results)
    path = os.path.join(save_dir,filename)
    df.to_csv(path, index=False)
    print(f"CSV Summary saved to {path}")
