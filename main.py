import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
import plotly.express as px


def from_str_to_timedelta(row):
    """ For a dataframe row, convert the string value from the "duration_total_timedelta" column into timedelta """

    duration = datetime.strptime(row["duration_total_timedelta"], "%H:%M:%S")
    duration = timedelta(hours=duration.hour,
                         minutes=duration.minute,
                         seconds=duration.second)
    return duration


st.title("Race Results Visualizer")

# Read the data from the CSV file and preprocess it
df = pd.read_csv("race_results.csv",
                 parse_dates=["date"],
                 date_format="%Y-%m-%d")
df = df.rename(columns={"duration": "duration_total_timedelta"})
df["duration_total_timedelta"] = df.apply(from_str_to_timedelta, axis=1)
df["duration_total_sec"] = df.apply(lambda row: row["duration_total_timedelta"].seconds, axis=1)
df["duration_km_timedelta"] = df["duration_total_timedelta"] / df["distance"]
df["duration_km_timedelta_str"] = df.apply(lambda row: datetime.strftime(datetime(2025, 1, 1)+row["duration_km_timedelta"], "%H:%M:%S"), axis=1)
df["duration_km_sec"] = df["duration_total_sec"] / df["distance"]

print(df)

# Prepare the date vs. duration plot
delta_duration_sec = 20
min_duration = int(df["duration_km_sec"].min())
max_duration = int(df["duration_km_sec"].max())
duration_ticks = list(range(min_duration, max_duration, delta_duration_sec))

duration_labels = []
time_zero = datetime(2025, 1, 1)
for tick in duration_ticks:
    duration_labels.append((time_zero + timedelta(seconds=tick)).strftime("%H:%M:%S"))

# Plot date vs. duration per km
st.subheader("Date vs. Duration / km")

figure = px.line(x=df["date"],
                 y=df["duration_km_sec"],
                 labels={"x": "Date", "y": "Duration"},
                 markers=True)
figure.update_traces(customdata=df["duration_km_timedelta_str"],
                     hovertemplate='Date: %{x} <br> Duration per km: %{customdata}') #
figure.update_layout(yaxis = dict(tickmode = "array",
                                  tickvals = duration_ticks,
                                  ticktext = duration_labels))
st.plotly_chart(figure)
