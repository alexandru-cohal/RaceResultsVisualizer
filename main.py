import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import gpxpy


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
df["date_str"] = df.apply(lambda row: row["date"].strftime("%b %d, %Y"), axis=1)
df = df.rename(columns={"duration": "duration_total_timedelta"})
df["duration_total_timedelta"] = df.apply(from_str_to_timedelta, axis=1)
df["duration_total_sec"] = df.apply(lambda row: row["duration_total_timedelta"].seconds, axis=1)
df["duration_km_timedelta"] = df["duration_total_timedelta"] / df["distance"]
df["duration_km_timedelta_str"] = df.apply(lambda row: datetime.strftime(datetime(2025, 1, 1)+row["duration_km_timedelta"], "%H:%M:%S"), axis=1)
df["duration_km_sec"] = df["duration_total_sec"] / df["distance"]

# Prepare the date vs. time per km plot
delta_duration_sec = 20
min_duration = int(df["duration_km_sec"].min())
max_duration = int(df["duration_km_sec"].max())
duration_ticks = list(range(min_duration, max_duration, delta_duration_sec))

duration_labels = []
time_zero = datetime(2025, 1, 1)
for tick in duration_ticks:
    duration_labels.append((time_zero + timedelta(seconds=tick)).strftime("%H:%M:%S"))

# Plot date vs. time per km
st.header("Date vs. Average time per km")

figure = px.line(x=df["date"],
                 y=df["duration_km_sec"],
                 labels={"x": "Date", "y": "Average time per km"},
                 markers=True)
figure.update_traces(marker=dict(size=10),
                    customdata=np.stack((df["duration_km_timedelta_str"],
                                          df["name"],
                                          df["city"],
                                          df["country"],
                                          df["distance"]), axis=-1),
                     hovertemplate='<b>Date</b>: %{x} <br>'
                                   '<b>Time per km</b>: %{customdata[0]} <br>'
                                   '<b>Distance</b>: %{customdata[4]} km <br>'
                                   '<b>Race</b>: %{customdata[1]} <br>'
                                   '<b>City</b>: %{customdata[2]} <br>'
                                   '<b>Country</b>: %{customdata[3]}')
figure.update_layout(yaxis = dict(tickmode = "array",
                                  tickvals = duration_ticks,
                                  ticktext = duration_labels))
figure.update_xaxes(showspikes=True, spikecolor="darkblue")
figure.update_yaxes(showspikes=True, spikecolor="darkblue")

st.plotly_chart(figure)

# Plot the number of races w.r.t. distance
st.header("Number of races w.r.t. Distance")

figure = px.histogram(x=df["distance"],
                      text_auto=True)
figure.update_layout(xaxis_title_text="Distance (km)",
                     yaxis_title_text="Number of races")
figure.update_traces(hovertemplate='<b>Distance</b>: %{x} km <br>'
                                   '<b>Number of races</b>: %{y} <br>')

st.plotly_chart(figure)

# Prepare the location of the starting points plot
avg_lat = df["lat"].mean()

# Plot the locations of the starting points on a map
st.header("Locations of the Starting Points")

figure = px.scatter_map(lat=df["lat"],
                        lon=df["lon"])
figure.update_layout(map_style="open-street-map",
                  map_zoom=6,
                  map_center_lat = avg_lat,
                  height=500)
figure.update_traces(marker=dict(size=10),
                    customdata=np.stack((df["duration_km_timedelta_str"],
                                          df["name"],
                                          df["city"],
                                          df["country"],
                                          df["distance"],
                                          df["date_str"]), axis=-1),
                     hovertemplate='<b>Date</b>: %{customdata[5]} <br>'
                                   '<b>Time per km</b>: %{customdata[0]} <br>'
                                   '<b>Distance</b>: %{customdata[4]} km <br>'
                                   '<b>Race</b>: %{customdata[1]} <br>'
                                   '<b>City</b>: %{customdata[2]} <br>'
                                   '<b>Country</b>: %{customdata[3]}')

st.plotly_chart(figure)

# Prepare the route and elevation plots

st.header("Route and Elevation")

GPX_FILEPATH = 'race_data/'


def parse_gpx_file(filepath):
    lat = []
    lon = []
    elev = []
    gpx_file = open(filepath, 'r')
    gpx = gpxpy.parse(gpx_file)
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lat.append(point.latitude)
                lon.append(point.longitude)
                elev.append(point.elevation)

    return lat, lon, elev


race_option = st.selectbox(label="Race name",
                           options=df["name"])
race_option_index = df.index[df["name"] == race_option][0]
lat, lon, elev = parse_gpx_file(GPX_FILEPATH + df["gpxfilename"][race_option_index])

st.subheader("Route points")

figure = px.scatter_map(lat=lat,
                        lon=lon)
figure.update_layout(map_style="open-street-map",
                  map_zoom=6,
                  map_center_lat = avg_lat,
                  height=500)
st.plotly_chart(figure)

st.subheader("Elevation")

figure = px.scatter(y=elev)
st.plotly_chart(figure)
