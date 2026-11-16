import matplotlib.pyplot as plt

# Humidity vs air bubbles (VERY important insight)
def plot_humidity_vs_bubbles(df):
    plt.scatter(df['humidity_pct'], df['air_bubbles_pct'])
    plt.xlabel("Humidity (%)")
    plt.ylabel("Air Bubbles (%)")
    plt.title("Humidity vs Air Bubbles")
    plt.show()


# Quality by machine
def plot_quality_by_machine(df):
    df.groupby('machine_id')['quality_score'].mean().plot(kind='bar')
    plt.title("Quality Score by Machine")
    plt.ylabel("Quality Score")
    plt.show()