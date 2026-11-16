import matplotlib.pyplot as plt
from pathlib import Path


def plot_humidity_vs_bubbles(df, output_path: Path) -> None:
    """Save a scatter plot of humidity and air-bubble rate."""

    figure, axis = plt.subplots()
    axis.scatter(df["humidity_pct"], df["air_bubbles_pct"])
    axis.set_xlabel("Humidity (%)")
    axis.set_ylabel("Air bubbles (%)")
    axis.set_title("Humidity vs. air bubbles")
    figure.tight_layout()
    figure.savefig(output_path, dpi=140)
    plt.close(figure)


def plot_quality_by_machine(df, output_path: Path) -> None:
    """Save a bar chart comparing average quality scores by machine."""

    figure, axis = plt.subplots()
    df.groupby("machine_id")["quality_score"].mean().plot(
        kind="bar",
        ax=axis,
    )
    axis.set_title("Average quality score by machine")
    axis.set_xlabel("Machine")
    axis.set_ylabel("Quality score")
    figure.tight_layout()
    figure.savefig(output_path, dpi=140)
    plt.close(figure)