from config import config
from datetime import datetime, timedelta
import numpy as np
import gpxpy
import haversine


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

    df["route_points_dist_step"] = None
    df["route_points_time_step"] = None
    df["route_points_dist_accum"] = None
    df["route_points_time_accum"] = None

    for idx_row, row in df.iterrows():
        dist_step = [0]
        time_step = [0]
        for idx_point in range(1, len(row["route_points_lat"])):
            # Point0: lat[idx - 1], lon[idx - 1], time[idx - 1]
            # Point1: lat[idx], lon[idx], time[idx]
            dist_current = haversine.haversine(
                (row["route_points_lat"][idx_point - 1], row["route_points_lon"][idx_point - 1]),
                (row["route_points_lat"][idx_point], row["route_points_lon"][idx_point]))
            time_current = (row["route_points_timestamp"][idx_point] -
                            row["route_points_timestamp"][idx_point - 1]).seconds

            dist_step.append(dist_current)
            time_step.append(time_current)

        df.at[idx_row, "route_points_dist_step"] = np.array(dist_step)
        df.at[idx_row, "route_points_dist_accum"] = np.cumsum(dist_step)
        df.at[idx_row, "route_points_time_step"] = np.array(time_step)
        df.at[idx_row, "route_points_time_accum"] = np.cumsum(time_step)

    return df