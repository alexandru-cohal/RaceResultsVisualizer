from datetime import datetime, timedelta
import gpxpy


def from_str_to_timedelta(row):
    """ For a dataframe row, convert the string value from the "duration_total_timedelta" column into timedelta """

    duration = datetime.strptime(row["duration_total_timedelta"], "%H:%M:%S")
    duration = timedelta(hours=duration.hour,
                         minutes=duration.minute,
                         seconds=duration.second)
    return duration


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