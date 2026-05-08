import pandas as pd

# Load data from CSV file
def load_data(file_path):
    return pd.read_csv(file_path)


# Clean and enrich dataset
def clean_data(df):

    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Remove duplicates
    df = df.drop_duplicates()

    # Remove invalid or negative values
    numeric_cols = [
        'ambient_temp_c',
        'humidity_pct',
        'foam_density',
        'air_bubbles_pct',
        'injection_time_sec',
        'material_usage_kg',
        'cycle_time_sec'
    ]

    for col in numeric_cols:
        df = df[df[col] >= 0]

    # Handle missing values
    df = df.dropna()

    # Quality score
    df['quality_score'] = df['foam_density'] / (1 + df['air_bubbles_pct'])

    # Efficiency
    df['efficiency_score'] = 1 / df['cycle_time_sec']

    # Normalize humidity
    df['high_humidity_flag'] = df['humidity_pct'] > 60

    return df