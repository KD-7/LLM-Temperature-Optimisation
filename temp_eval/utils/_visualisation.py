import plotly.express as px
import pandas as pd


def draw_anonymisation_metrics(temperature_values, anon_scores,
                               filename="temp_anon.html",save_dir="./visualisations/"):
    """
    Exports a line chart (as html) comparing anonymisation metrics against temperature
    value. If file exists with the same name, it will be overwritten.

    Args:
    - temperature_values (list): list of temperature values defined in
    config
    - rogue_scores (list(list)): list of metrics precision, recall and f1 scores
    - filename (str): name of the file for the exported chart
    - save_dir (str): save directory
    """
    # ORDER OF TEMP VALUES MUST MATCH ORDER OF ANON_SCORES
    df = pd.DataFrame({
        "Temperature": temperature_values,  # X-axis
        "Precision": anon_scores[0],  # Y-axis
        "Recall": anon_scores[1],  # Y-axis
        "F1": anon_scores[2]  # Y-axis
    })

    # Convert to long format for Plotly (required for multi-line plots)
    df_long = df.melt(id_vars="Temperature", var_name="Metric", value_name="Score")

    fig = px.line(df_long, x="Temperature", y="Score", color="Metric",
                  title="Anonymisation Metrics vs Temperature",
                  markers=True)  # Add markers at data points

    fig.write_html(save_dir + filename)


def draw_context_metrics(temperature_values, rogue_scores, filename="temp_rouge.html",
                         save_dir="./visualisations/"):
    """
    Exports a line chart (as html) comparing temperature value against rogue_scores.
    If file exists with the same name, it will be overwritten.

    Args:
    - temperature_values (list): list of temperature values defined in
    config
    - rogue_scores (list(list)): list of calculated rouge scores (3 types:
    ROUGE-1, ROUGE-2, ROUGE-L)
    - filename (str): name of the file for the exported chart
    - save_dir (str): save directory
    """
    # ORDER OF TEMP VALUES MUST MATCH ORDER OF ROGUE_SCORES
    df = pd.DataFrame({
        "Temperature": temperature_values,  # X-axis
        "ROUGE-1": rogue_scores[0],  # Y-axis
        "ROUGE-2": rogue_scores[1],  # Y-axis
        "ROUGE-L": rogue_scores[2]  # Y-axis
    })

    # Convert to long format for Plotly (required for multi-line plots)
    df_long = df.melt(id_vars="Temperature", var_name="Metric", value_name="Score")

    fig = px.line(df_long, x="Temperature", y="Score", color="Metric",
                  title="ROGUE Score vs Temperature",
                  markers=True)  # Add markers at data points

    fig.write_html(save_dir + filename)
