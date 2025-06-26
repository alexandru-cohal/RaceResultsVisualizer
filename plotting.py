from datetime import datetime, timedelta
import plotly.express as px
import numpy as np
from data_processing import get_lat_lon_elev


def plot_time_per_km(df):
    """ Prepare and create the plot of date vs. time per km """

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


def plot_number_of_races(df):
    """ Prepare and create the plot of number of races """

    figure = px.histogram(x=df["distance"],
                          text_auto=True)
    figure.update_layout(xaxis_title_text="Distance (km)",
                         yaxis_title_text="Number of races")
    figure.update_traces(hovertemplate='<b>Distance</b>: %{x} km <br>'
                                       '<b>Number of races</b>: %{y} <br>')
    return figure


def plot_starting_points(df):
    """ Prepare and create the plot of starting points """

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


def plot_route(df, race_option):
    """ Prepare and create the plot of route """

    lat, lon, _ = get_lat_lon_elev(df, race_option)

    figure = px.scatter_map(lat=lat,
                            lon=lon)
    figure.update_layout(map_style="open-street-map",
                         map_zoom=6,
                         height=500)

    return figure


def plot_elevation(df, race_option):
    """ Prepare and create the plot of elevation """

    _, _, elev = get_lat_lon_elev(df, race_option)

    figure = px.scatter(y=elev)

    return figure
