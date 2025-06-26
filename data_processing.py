from datetime import datetime, timedelta
import gpxpy


GPX_FILEPATH = 'race_data/'


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
    """ Parse a .GPX file and return 3 lists with latitude, longitude and elevation values, respectively """
    lat = []
    lon = []
    elev = []

    with open(filepath, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    lat.append(point.latitude)
                    lon.append(point.longitude)
                    elev.append(point.elevation)

    return lat, lon, elev


def get_lat_lon_elev(df, race_option):
    race_option_index = df.index[df["name"] == race_option][0]

    lat, lon, elev = parse_gpx_file(GPX_FILEPATH + df["gpxfilename"][race_option_index])

    return lat, lon, elev
