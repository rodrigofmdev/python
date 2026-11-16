import argparse
import os
import time
from datetime import datetime
from pathlib import Path

from src import analysis
from src.data_cleaning import clean_data, load_data
from src.report import generate_report
from src.visualization import (
    plot_humidity_vs_bubbles,
    plot_quality_by_machine,
)

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "production_data.csv"
OUTPUT_DIR = BASE_DIR / "output"


def create_run_output_dir() -> Path:
    """Create a unique output folder named with the current timestamp."""

    OUTPUT_DIR.mkdir(exist_ok=True)

    while True:
        run_output_dir = OUTPUT_DIR / datetime.now().strftime(
            "%Y-%m-%d-%H-%M-%S"
        )

        try:
            run_output_dir.mkdir()
        except FileExistsError:
            time.sleep(1)
        else:
            return run_output_dir


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze PU foam injection production data."
    )
    parser.add_argument(
        "--input",
        default=str(DATA_FILE),
        help="Path to the production CSV file.",
    )
    args = parser.parse_args()

    df = clean_data(load_data(args.input))
    run_output_dir = create_run_output_dir()

    generate_report(df, analysis, run_output_dir / "report.md")
    plot_humidity_vs_bubbles(
        df,
        run_output_dir / "humidity_vs_air_bubbles.png",
    )
    plot_quality_by_machine(
        df,
        run_output_dir / "quality_by_machine.png",
    )

    relative_output_path = run_output_dir.relative_to(BASE_DIR)
    print(
        f"Analysis complete. Generated files in: "
        f"{relative_output_path}{os.sep}"
    )


if __name__ == "__main__":
    main()