import pandas as pd


NUMERIC_COLUMNS = [
    "ambient_temp_c",
    "humidity_pct",
    "foam_density",
    "air_bubbles_pct",
    "injection_time_sec",
    "material_usage_kg",
    "cycle_time_sec",
]

REQUIRED_COLUMNS = [
    "date",
    "machine_id",
    "model",
    *NUMERIC_COLUMNS,
]


def load_data(file_path):
    """Load production records from a CSV file."""

    return pd.read_csv(file_path)


def clean_data(df):
    """Validate, clean, and add process metrics to the production data."""

    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {', '.join(sorted(missing_columns))}"
        )

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.drop_duplicates()
    df = df.dropna(subset=REQUIRED_COLUMNS)

    for column in NUMERIC_COLUMNS:
        df = df[df[column] >= 0]

    df = df[
        (df["humidity_pct"] <= 100)
        & (df["air_bubbles_pct"] <= 100)
        & (df["cycle_time_sec"] > 0)
    ]

    if df.empty:
        raise ValueError("No valid production records remain after cleaning.")

    df["quality_score"] = df["foam_density"] / (
        1 + df["air_bubbles_pct"]
    )
    df["efficiency_score"] = 1 / df["cycle_time_sec"]
    df["high_humidity_flag"] = df["humidity_pct"] > 60

    return df.reset_index(drop=True)