from config import config
from datetime import datetime, timedelta
import numpy as np
import gpxpy
import haversine
import math


def from_str_to_timedelta(row):
    """ For a dataframe row containing the race data, convert the value from the
    "duration_total_timedelta" column from string into timedelta """

    duration = datetime.strptime(row["duration_total_timedelta"], "%H:%M:%S")
    duration = timedelta(hours=duration.hour,
                         minutes=duration.minute,
                         seconds=duration.second)
    return duration


def process_date_data(df):
    """ Process the data from the "date" column """

    df["date_str"] = df.apply(lambda row: row["date"].strftime("%b %d, %Y"), axis=1)

    return df


def process_duration_data(df):
    """ Process the data from the "duration" column """

    df = df.rename(columns={"duration": "duration_total_timedelta"})
    df["duration_total_timedelta"] = df.apply(from_str_to_timedelta, axis=1)

    df["duration_total_sec"] = df.apply(lambda row: row["duration_total_timedelta"].seconds, axis=1)

    df["duration_km_timedelta"] = df["duration_total_timedelta"] / df["distance"]

    df["duration_km_timedelta_str"] = df.apply(lambda row: datetime.strftime(datetime(2025, 1, 1) +
                                                                             row["duration_km_timedelta"], "%H:%M:%S"),
                                               axis=1)

    df["duration_km_sec"] = df["duration_total_sec"] / df["distance"]

    return df


def parse_gpx_file(filepath):
    """ Parse a .GPX file and return 4 lists with latitude, longitude, elevation and timestamp values, respectively """
    lat = []
    lon = []
    elev = []
    timestamp = []

    with open(filepath, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    lat.append(point.latitude)
                    lon.append(point.longitude)
                    elev.append(point.elevation)
                    timestamp.append(point.time)

    return lat, lon, elev, timestamp


def add_route_data(df):
    """ Get the route data from the .GPX file and add it to the dataframe """

    df["route_points_lat"] = None
    df["route_points_lon"] = None
    df["route_points_elev"] = None
    df["route_points_timestamp"] = None

    for idx_row, row in df.iterrows():
        lat, lon, elev, timestamp = parse_gpx_file(config["gpx_race_route_filepath"] + row["gpxfilename"])
        df.at[idx_row, "route_points_lat"] = np.array(lat)
        df.at[idx_row, "route_points_lon"] = np.array(lon)
        df.at[idx_row, "route_points_elev"] = np.array(elev)
        df.at[idx_row, "route_points_timestamp"] = np.array(timestamp)

    return df


def add_dist_and_time_accumulative_route_data(df):
    """ Calculate the current and cumulative distance and time of the steps from the route data """

    df["route_points_dist_step_km"] = None
    df["route_points_dist_accum_km"] = None
    df["route_points_duration_step_sec"] = None
    df["route_points_duration_accum_sec"] = None
    df["route_points_duration_accum_timedelta"] = None
    df["route_points_duration_accum_timedelta_str"] = None

    for idx_row, row in df.iterrows():
        dist_step_km = [0]
        duration_step_sec = [0]
        for idx_point in range(1, len(row["route_points_lat"])):
            dist_step_current_km = haversine.haversine(
                (row["route_points_lat"][idx_point - 1], row["route_points_lon"][idx_point - 1]),
                (row["route_points_lat"][idx_point], row["route_points_lon"][idx_point]))
            duration_step_current_sec = (row["route_points_timestamp"][idx_point] -
                                         row["route_points_timestamp"][idx_point - 1]).seconds

            dist_step_km.append(dist_step_current_km)
            duration_step_sec.append(duration_step_current_sec)

        df.at[idx_row, "route_points_dist_step_km"] = np.array(dist_step_km)
        df.at[idx_row, "route_points_dist_accum_km"] = np.cumsum(dist_step_km)
        df.at[idx_row, "route_points_duration_step_sec"] = np.array(duration_step_sec)
        df.at[idx_row, "route_points_duration_accum_sec"] = np.cumsum(duration_step_sec)
        df.at[idx_row, "route_points_duration_accum_timedelta"] = np.array(
            [timedelta(seconds=elem.item()) for elem in df.at[idx_row, "route_points_duration_accum_sec"]])
        df.at[idx_row, "route_points_duration_accum_timedelta_str"] = np.array(
            [datetime.strftime(datetime(2025, 1, 1) + elem, "%H:%M:%S") for elem in df.at[idx_row, "route_points_duration_accum_timedelta"]])

    return df


def add_pace_data(df):
    """ Calculate the pace for each km """

    df["pace_sec"] = None
    df["pace_timedelta"] = None
    df["pace_timedelta_str"] = None

    for idx_row, row in df.iterrows():
        dist_accum_km = row["route_points_dist_accum_km"]
        duration_accum_sec = row["route_points_duration_accum_sec"]

        pace_sec = []
        pace_timedelta = []
        pace_timedelta_str = []
        pace_dist = []
        last_km_mark = (None, None, None)  # (km_mark, distance, time)

        for idx_step, step in enumerate(dist_accum_km):
            km_current = math.modf(step)[1]
            if km_current != last_km_mark[0]:
                if last_km_mark[0] is not None:
                    duration_diff = duration_accum_sec[idx_step] - last_km_mark[2]
                    dist_diff = step - last_km_mark[1]
                    pace_sec.append(int(duration_diff / dist_diff))
                    pace_timedelta.append(timedelta(seconds=pace_sec[-1]))
                    pace_timedelta_str.append(datetime.strftime(datetime(2025, 1, 1) +
                                                                pace_timedelta[-1], "%H:%M:%S"))
                    pace_dist.append(dist_diff)
                last_km_mark = (km_current, step, duration_accum_sec[idx_step])

        duration_diff = duration_accum_sec[-1] - last_km_mark[2]
        dist_diff = dist_accum_km[-1] - last_km_mark[1]
        pace_sec.append(int(duration_diff / dist_diff))
        pace_timedelta.append(timedelta(seconds=pace_sec[-1]))
        pace_timedelta_str.append(datetime.strftime(datetime(2025, 1, 1) +
                                                    pace_timedelta[-1], "%H:%M:%S"))
        pace_dist.append(dist_diff)

        df.at[idx_row, "pace_sec"] = np.array(pace_sec)
        df.at[idx_row, "pace_timedelta"] = np.array(pace_timedelta)
        df.at[idx_row, "pace_timedelta_str"] = np.array(pace_timedelta_str)
        df.at[idx_row, "pace_dist"] = np.array(pace_dist)

    return df