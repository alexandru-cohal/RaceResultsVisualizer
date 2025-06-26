from datetime import datetime, timedelta
import plotly.express as px
import numpy as np
from utils import parse_gpx_file


GPX_FILEPATH = 'race_data/'


def plot_timeperkm(df):
    # Prepare the date vs. time per km plot
    delta_duration_sec = 20
    min_duration = int(df["duration_km_sec"].min())
    max_duration = int(df["duration_km_sec"].max())
    duration_ticks = list(range(min_duration, max_duration, delta_duration_sec))

    duration_labels = []
    time_zero = datetime(2025, 1, 1)
    for tick in duration_ticks:
        duration_labels.append((time_zero + timedelta(seconds=tick)).strftime("%H:%M:%S"))

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
    figure.update_layout(yaxis=dict(tickmode="array",
                                    tickvals=duration_ticks,
                                    ticktext=duration_labels))
    figure.update_xaxes(showspikes=True, spikecolor="darkblue")
    figure.update_yaxes(showspikes=True, spikecolor="darkblue")

    return figure


def plot_numberofraces(df):
    figure = px.histogram(x=df["distance"],
                          text_auto=True)
    figure.update_layout(xaxis_title_text="Distance (km)",
                         yaxis_title_text="Number of races")
    figure.update_traces(hovertemplate='<b>Distance</b>: %{x} km <br>'
                                       '<b>Number of races</b>: %{y} <br>')
    return figure


def plot_startingpoints(df):
    # Prepare the location of the starting points plot
    avg_lat = df["lat"].mean()

    figure = px.scatter_map(lat=df["lat"],
                            lon=df["lon"])
    figure.update_layout(map_style="open-street-map",
                         map_zoom=6,
                         map_center_lat=avg_lat,
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
    return figure


def plot_route_and_elevation(df, race_option):
    # Prepare the route and elevation plots
    race_option_index = df.index[df["name"] == race_option][0]
    lat, lon, elev = parse_gpx_file(GPX_FILEPATH + df["gpxfilename"][race_option_index])

    figure_route = px.scatter_map(lat=lat,
                            lon=lon)
    figure_route.update_layout(map_style="open-street-map",
                         map_zoom=6,
                         height=500)

    figure_elevation = px.scatter(y=elev)

    return figure_route, figure_elevation

