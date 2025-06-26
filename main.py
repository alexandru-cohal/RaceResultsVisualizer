import pandas as pd
import streamlit as st
from data_processing import *
from plotting import *


st.title("Race Results Visualizer")

# Read the data from the CSV file and preprocess it
df = pd.read_csv("race_results.csv",
                 parse_dates=["date"],
                 date_format="%Y-%m-%d")
df = process_race_data(df)

# Plot date vs. time per km
st.header("Date vs. Average time per km")
figure = plot_timeperkm(df)
st.plotly_chart(figure)

# Plot the number of races w.r.t. distance
st.header("Number of races w.r.t. Distance")
figure = plot_numberofraces(df)
st.plotly_chart(figure)

# Plot the locations of the starting points on a map
st.header("Locations of the Starting Points")
figure = plot_startingpoints(df)
st.plotly_chart(figure)

# Plot the route and the elevation for a chosen race
st.header("Route and Elevation")
race_option = st.selectbox(label="Race name",
                           options=df["name"])
figure_route, figure_elevation = plot_route_and_elevation(df, race_option)
st.subheader("Route points")
st.plotly_chart(figure_route)
st.subheader("Elevation")
st.plotly_chart(figure_elevation)
