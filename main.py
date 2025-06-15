import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
import plotly.express as px


def from_str_to_sec(row):
    """ For a dataframe row, convert the string value from the "duration" column into seconds """

    duration = datetime.strptime(row["duration"], "%H:%M:%S")
    duration = timedelta(hours=duration.hour,
                         minutes=duration.minute,
                         seconds=duration.second).total_seconds()
    return duration


st.title("Race Results Visualizer")

# Read the data from the CSV file and preprocess it
df = pd.read_csv("race_results.csv",
                 parse_dates=["date"],
                 date_format="%d/%m/%Y")

df["duration_sec"] = df.apply(from_str_to_sec, axis=1)

date_values = [date.strftime("%Y-%m-%d") for date in df["date"]]
duration_values = df["duration_sec"]

# Prepare the date vs. duration plot
delta_duration = 20
min_duration = int(df["duration_sec"].min())
max_duration = int(df["duration_sec"].max())
duration_ticks = list(range(min_duration, max_duration, delta_duration))

duration_labels = []
time_zero = datetime(2025, 1, 1)
for tick in duration_ticks:
    duration_labels.append((time_zero + timedelta(seconds=tick)).strftime("%H:%M:%S"))

# Plot date vs. duration
st.subheader("Date vs. Duration")

figure = px.line(x=date_values,
                 y=duration_values,
                 labels={"x": "Date", "y": "Duration"},
                 markers=True)
figure.update_layout(yaxis = dict(tickmode = "array",
                                  tickvals = duration_ticks,
                                  ticktext = duration_labels))
st.plotly_chart(figure)
