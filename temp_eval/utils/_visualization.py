import plotly.express as px
import pandas as pd


def draw_chart_temp_f1(temperature_values, f1_scores):
    """
        Draw a chart with all temperature values vs corresponding f1 values

        Args:
        - temperature_values (list): list of temperature values defined in config
        - f1_scores (list): list of calculated f1 values

        Returns:
        - no return value, save the chart as html format
    """

    df = pd.DataFrame({
        "Temperature": temperature_values,  # X-axis values
        "F1": f1_scores  # Y-axis values
    })

    fig = px.line(df, x="Temperature", y="F1", title="F1 Scores vs Temperature")
    fig.write_html("./charts/temp_f1.html")


def draw_chart_temp_rouge(temperature_values, rouge_1_scores, rouge_2_scores, rouge_l_scores):
    """
            Draw a chart with all temperature values vs corresponding 3 types rouge values

            Args:
            - temperature_values (list): list of temperature values defined in config
            - rouge_1_scores (list): list of calculated rouge_1 values
            - rouge_2_scores (list): list of calculated rouge_2 values
            - rouge_l_scores (list): list of calculated rouge_l values

            Returns:
            - no return value, save the chart as html format
        """

    data = {
        "Temperature": temperature_values,  # X-axis values
        "ROUGE-1": rouge_1_scores,  # First line
        "ROUGE-2": rouge_2_scores,  # Second line
        "ROUGE-L": rouge_l_scores  # Third line
    }

    df = pd.DataFrame(data)

    # Convert to long format for Plotly (required for multi-line plots)
    df_long = df.melt(id_vars="Temperature", var_name="ROUGE Type", value_name="Rouge Score")

    fig = px.line(df_long, x="Temperature", y="Rouge Score", color="ROUGE Type",
                  title="ROUGE Scores vs Temperature",
                  markers=True,  # Add markers at data points
                  labels={"Temperature": "Temperature", "Score": "ROUGE Score", "ROUGE Type": "ROUGE Type"})
    fig.write_html("./charts/temp_rouge.html")

