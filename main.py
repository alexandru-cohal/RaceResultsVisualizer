from config import config
import pandas as pd
import streamlit as st
from data_processing import process_date_data, process_duration_data, add_route_data, add_dist_and_time_accumulative_route_data
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

# Plot date vs. time per km
st.header("Date vs. Average time per km")
figure = plot_time_per_km(df)
st.plotly_chart(figure)

# Plot the number of races w.r.t. distance
st.header("Number of races w.r.t. Distance")
figure = plot_number_of_races(df)
st.plotly_chart(figure)

# Plot the locations of the starting points on a map
st.header("Locations of the Starting Points")
figure = plot_starting_points(df)
st.plotly_chart(figure)

# Plot the route and the elevation for a chosen race
st.header("Route and Elevation")
race_option = st.selectbox(label="Race name",
                           options=df["name"])
race_option_index = df.index[df["name"] == race_option][0]
st.subheader("Route points")
figure = plot_route(df, race_option_index)
st.plotly_chart(figure)
st.subheader("Elevation")
figure = plot_elevation(df, race_option_index)
st.plotly_chart(figure)
