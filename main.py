from config import config
import pandas as pd
import streamlit as st
from data_processing import (process_date_data, process_duration_data, add_route_data,
                             add_dist_and_time_accumulative_route_data, add_pace_data)
from plotting import *

st.title("Race Results Visualizer")

# Read the data from the CSV file and process it
df = pd.read_csv(config["csv_race_results_filepath"],
                 parse_dates=["date"],
                 date_format="%Y-%m-%d")
df = process_date_data(df)
df = process_duration_data(df)
df = add_route_data(df)
df = add_dist_and_time_accumulative_route_data(df)
df = add_pace_data(df)

# Plot the average time per km
st.header("Average time per km")
race_distance_option = st.selectbox(label="Race length",
                                    options=["All", "5 - 6 km", "10 - 12 km"])
try:
    figure = plot_time_per_km(df, race_distance_option)
except IndexError:
    st.error("No data available")
else:
    st.plotly_chart(figure)

# Plot the number of races w.r.t. distance
st.header("Number of races w.r.t. Distance")
figure = plot_number_of_races(df)
st.plotly_chart(figure)

# Plot the locations of the starting points on a map
st.header("Locations of the Starting Points")
starting_points_location_option = st.selectbox(label="Area",
                                               options=["General", "Barcelona"])
figure = plot_starting_points(df, starting_points_location_option)
st.plotly_chart(figure)

# Plot the route, elevation and pace for a chosen race
st.header("Route, Elevation and Pace")
race_option = st.selectbox(label="Race name",
                           options=df["name"])
race_option_index = df.index[df["name"] == race_option][0]
st.subheader("Route points")
print(df["validroutepoints"][race_option_index])
if df["validroutepoints"][race_option_index] == True:
    figure = plot_route(df, race_option_index)
    st.plotly_chart(figure)
else:
    st.error("No route points available")
st.subheader("Elevation")
if df["validroutepoints"][race_option_index] == True:
    figure = plot_elevation(df, race_option_index)
    st.plotly_chart(figure)
else:
    st.error("No route points available")
st.subheader("Pace")
if df["validroutepoints"][race_option_index] == True:
    figure = plot_pace(df, race_option_index)
else:
    figure = plot_pace_only_official(df, race_option_index)
st.plotly_chart(figure)
