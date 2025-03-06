import pandas as pd
from github import Auth, Github


def export_to_github(data, temp_value, repo_path, branch_name, auth_token=None):
    """Exports the given data to the RESULTS.md markdown file in the specified GitHub
    repository

    Args: data (list[list]): A list of lists containing the results for each column
    in table. Format is as follows: [Run, Accuracy, Precision, Recall, F1, ROUGE-1,
    ROUGE-2, ROUGE-L, Temperature, Python Version]"""

    # Create a dataframe
    headers = ["Run", "Accuracy", "Precision", "Recall", "F1",
               "ROUGE-1", "ROUGE-2", "ROUGE-L", "Temperature", "Python Version"]

    df = pd.DataFrame(data, columns=headers)

    # Export to GitHub
    auth = Auth.Token(auth_token)
    g = Github(auth=auth)
    repo = g.get_repo(repo_path)
    old_contents = repo.get_contents("RESULTS.md", ref=branch_name)
    new_contents = (old_contents.decoded_content.decode() + "\n" +
                    "## Temperature value = " + str(temp_value) + "\n" +
                    df.to_markdown(index=False))
    repo.update_file(old_contents.path, "Updated results", new_contents,
                     branch=branch_name, sha=old_contents.sha)
    print("Results exported to github successfully")
