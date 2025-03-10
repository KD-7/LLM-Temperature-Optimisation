import pandas as pd
from github import Auth, Github


def _get_repo(auth_token, repo_path):
    auth = Auth.Token(auth_token)
    return Github(auth=auth).get_repo(repo_path)


def export_to_github(data, repo_path, branch_name, auth_token=None, header=None,
                     commit_message="Updated results"):
    """Exports the given data to the RESULTS.md markdown file in the specified GitHub
    repository
    Args:
        data (list(dict)):
        A list of dictionaries containing the results for the experiment.

        repo_path (str): The path to the GitHub repository in the format "owner/repo".

        branch_name (str): The name of the branch to push the changes to.

        auth_token (str): The GitHub personal access token to authenticate the user.

        header (str): The header to be added to the markdown file before the data.

        commit_message (str): The commit message to be used when updating the file.
    """

    repo = _get_repo(auth_token, repo_path)
    df = pd.DataFrame(data)
    old_contents = repo.get_contents("RESULTS.md", ref=branch_name)

    new_contents = (old_contents.decoded_content.decode() + "\n" + header + "\n" +
                    df.to_markdown(index=False))
    repo.update_file(old_contents.path, commit_message, new_contents,
                     branch=branch_name, sha=old_contents.sha)

    print("Results exported to github successfully")
