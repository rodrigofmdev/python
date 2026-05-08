# Average foam density per machine
def density_by_machine(df):
    return df.groupby('machine_id')['foam_density'].mean()


# Air bubbles (quality indicator)
def bubbles_by_machine(df):
    return df.groupby('machine_id')['air_bubbles_pct'].mean()


# Quality score (engineered metric)
def quality_by_machine(df):
    return df.groupby('machine_id')['quality_score'].mean()


# Efficiency score (engineered metric)
def efficiency_by_machine(df):
    return df.groupby('machine_id')['efficiency_score'].mean()


# Correlation between humidity and bubbles
def humidity_vs_bubbles(df):
    return df[['humidity_pct', 'air_bubbles_pct']].corr()


# Best machine in quality
def best_machine_quality(df):
    return df.groupby('machine_id')['quality_score'].mean().idxmax()


# Best machine in efficiency
def best_machine_efficiency(df):
    return df.groupby('machine_id')['efficiency_score'].mean().idxmax()


# Find optimal humidity range
def optimal_humidity(df):
    return df.groupby('humidity_pct')['air_bubbles_pct'].mean().idxmin()


# Compare models
def quality_by_model(df):
    return df.groupby('model')['quality_score'].mean()