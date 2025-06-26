from datetime import datetime, timedelta
from utils import from_str_to_timedelta


def process_race_data(df):
    df["date_str"] = df.apply(lambda row: row["date"].strftime("%b %d, %Y"), axis=1)
    df = df.rename(columns={"duration": "duration_total_timedelta"})
    df["duration_total_timedelta"] = df.apply(from_str_to_timedelta, axis=1)
    df["duration_total_sec"] = df.apply(lambda row: row["duration_total_timedelta"].seconds, axis=1)
    df["duration_km_timedelta"] = df["duration_total_timedelta"] / df["distance"]
    df["duration_km_timedelta_str"] = df.apply(
        lambda row: datetime.strftime(datetime(2025, 1, 1) + row["duration_km_timedelta"], "%H:%M:%S"), axis=1)
    df["duration_km_sec"] = df["duration_total_sec"] / df["distance"]

    return df
