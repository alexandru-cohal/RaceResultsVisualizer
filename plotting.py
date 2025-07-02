from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as pg
import numpy as np


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

    start_points_lat = df.apply(lambda row: row["route_points_lat"][0], axis=1)
    start_points_lon = df.apply(lambda row: row["route_points_lon"][0], axis=1)
    start_points_lat_avg = start_points_lat.mean()
    start_points_lon_avg = start_points_lon.mean()

    figure = px.scatter_map(lat=start_points_lat,
                            lon=start_points_lon)
    figure.update_layout(map_style="open-street-map",
                         map_zoom=6,
                         map_center_lat=start_points_lat_avg,
                         map_center_lon=start_points_lon_avg,
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


def plot_route(df, race_option_index):
    """ Prepare and create the plot of route """

    lat = df["route_points_lat"][race_option_index]
    lon = df["route_points_lon"][race_option_index]
    elev = df["route_points_elev"][race_option_index]
    dist_accum = df["route_points_dist_accum_km"][race_option_index]
    duration_accum = df["route_points_duration_accum_timedelta_str"][race_option_index]
    print(len(lat), len(dist_accum), len(duration_accum))

    avg_lat = sum(lat) / len(lat)
    avg_lon = sum(lon) / len(lon)

    figure = px.line_map(lat=lat,
                         lon=lon)
    figure.update_layout(map_style="open-street-map",
                         map_zoom=13,
                         map_center_lat=avg_lat,
                         map_center_lon=avg_lon,
                         height=500)
    figure.update_traces(customdata=np.stack((lat, lon, elev, dist_accum, duration_accum), axis=-1),
                         hovertemplate='<b>Latitude</b>: %{customdata[0]} °N <br>'
                                       '<b>Longitude</b>: %{customdata[1]} °E <br>'
                                       '<b>Elevation</b>: %{customdata[2]} m <br>'
                                       '<b>Elapsed time</b>: %{customdata[4]}<br>'
                                       '<b>Covered distance</b>: %{customdata[3]:.3f} km <br>')
    start_point = pg.Scattermap(lat=[lat[0]],
                                lon=[lon[0]],
                                marker=dict(size=20, color="green"),
                                name="Start Point",
                                customdata=[elev[0]],
                                hovertemplate='<b>Start Point</b> <br>'
                                              '<b>Latitude</b>: %{lat} °N <br>'
                                              '<b>Longitude</b>: %{lon} °E <br>'
                                              '<b>Elevation</b>: %{customdata} m <br>')
    figure.add_trace(start_point)
    end_point = pg.Scattermap(lat=[lat[-1]],
                              lon=[lon[-1]],
                              marker=dict(size=20, color="red"),
                              name="End Point",
                              customdata=[elev[-1]],
                              hovertemplate='<b>End Point</b> <br>'
                                            '<b>Latitude</b>: %{lat} °N <br>'
                                            '<b>Longitude</b>: %{lon} °E <br>'
                                            '<b>Elevation</b>: %{customdata} m <br>')
    figure.add_trace(end_point)

    return figure


def plot_elevation(df, race_option_index):
    """ Prepare and create the plot of elevation """

    figure = px.line(y=df["route_points_elev"][race_option_index],
                     labels={"x": "Sample", "y": "Elevation [m]"})
    figure.update_traces(customdata=np.stack((df["route_points_lat"][race_option_index],
                                              df["route_points_lon"][race_option_index]),
                                             axis=-1),
                         hovertemplate='<b>Latitude</b>: %{customdata[0]} °N <br>'
                                       '<b>Longitude</b>: %{customdata[1]} °E <br>'
                                       '<b>Elevation</b>: %{y} m <br>')

    return figure
