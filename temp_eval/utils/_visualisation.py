import plotly.express as px
import pandas as pd
import os


def draw_anonymisation_metrics(temperature_values, anon_scores,
                               filename="temp_anon.html", save_dir="visualisations"):
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

    # Rearrange order with ::-1 for correct line overlaying
    fig = px.line(df_long[::-1], x="Temperature", y="Score", color="Metric",
                  title="Anonymisation Metrics vs Temperature",
                  markers=True,  # Add markers at data points
                  color_discrete_sequence=["navy", "red", "#2ecc71"])

    fig.update_xaxes(tickvals=temperature_values)
    # Add some buffer to the top of the graph
    y_buffer = 0.03
    fig.update_yaxes(range=[0, 1 + y_buffer], tickvals=[0, 0.2, 0.4, 0.6, 0.8, 1.0])

    # Modify widths so multiple lines show if values are identical
    fig.update_traces(line_width=2.5, selector=dict(name="Precision"))
    fig.update_traces(line_width=6, selector=dict(name="Recall"))
    fig.update_traces(line_width=10, selector=dict(name="F1"))

    path = os.path.join(save_dir, filename)
    fig.write_html(path)
    print(f"Anonymisation metrics plot saved to {path}")


def draw_context_metrics(temperature_values, rogue_scores, filename="temp_rouge.html",
                         save_dir="visualisations"):
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

    fig = px.line(df_long[::-1], x="Temperature", y="Score", color="Metric",
                  title="ROGUE Score vs Temperature",
                  markers=True,
                  color_discrete_sequence=["black", "orange", "#808080"])

    fig.update_xaxes(tickvals=temperature_values)
    y_buffer = 0.03
    fig.update_yaxes(range=[0, 1 + y_buffer], tickvals=[0, 0.2, 0.4, 0.6, 0.8, 1.0])

    # Modify widths so multiple lines show if values are identical
    fig.update_traces(line_width=2.5, selector=dict(name="ROUGE-1"))
    fig.update_traces(line_width=6, selector=dict(name="ROUGE-2"))
    fig.update_traces(line_width=10, selector=dict(name="ROUGE-L"))

    path = os.path.join(save_dir, filename)
    fig.write_html(path)
    print(f"Context metrics plot saved to {path}")
