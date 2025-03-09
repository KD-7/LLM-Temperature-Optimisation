import pandas as pd
from github import Auth, Github


def _get_repo(auth_token, repo_path):
    auth = Auth.Token(auth_token)
    return Github(auth=auth).get_repo(repo_path)


def export_config_github(config, repo_path, branch_name, auth_token=None):
    """Exports the given config to the CONFIG.md markdown file in the specified GitHub
    repository

    Args:
        config (dict): A dictionary containing the configuration settings for the
        experiment.

        repo_path (str): The path to the GitHub repository in the format "owner/repo".

        branch_name (str): The name of the branch to push the changes to.

        auth_token (str): The GitHub personal access token to authenticate the user.
    """
    df = pd.DataFrame(config)
    repo = _get_repo(auth_token, repo_path)
    old_contents = repo.get_contents("CONFIG.md", ref=branch_name)
    new_contents = (old_contents.decoded_content.decode() + "\n" +
                    "## Experiment Configuration\n" +
                    df.to_markdown(index=False))
    repo.update_file(old_contents.path, "Updated config", new_contents,
                     branch=branch_name, sha=old_contents.sha)

    print("Config exported to github successfully")


def export_results_github(data, temp_value, repo_path, branch_name, auth_token=None):
    """Exports the given data to the RESULTS.md markdown file in the specified GitHub
    repository

    Args: data_frame (dict): A dictionary containing the results for the experiment.
    """

    repo = _get_repo(auth_token, repo_path)
    df = pd.DataFrame(data)
    old_contents = repo.get_contents("RESULTS.md", ref=branch_name)

    new_contents = (old_contents.decoded_content.decode() + "\n" +
                    "## Temperature value = " + str(temp_value) + "\n" +
                    df.to_markdown(index=False))
    repo.update_file(old_contents.path, "Updated results", new_contents,
                     branch=branch_name, sha=old_contents.sha)

    print("Results exported to github successfully")
