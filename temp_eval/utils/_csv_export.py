import pandas as pd


def export_csv(results, filename) -> None:
    """
    Exports the given results to a CSV file with the specified filename.

    Args:
    - results: experimental results to be saved
    - filename (str): name of destination file
    """
    df = pd.DataFrame(results)
    df.to_csv(filename + ".csv", index=False)
