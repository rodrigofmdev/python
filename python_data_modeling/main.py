from src.data_cleaning import load_data, clean_data
import src.analysis as analysis
from src.report import generate_report
from src.visualization import plot_humidity_vs_bubbles, plot_quality_by_machine



def main():
    file_path = "data/production_data.csv"

    # Load data
    df = load_data(file_path)

    # Clean and enrich data
    df = clean_data(df)

    # Generate report
    generate_report(df, analysis)

    plot_humidity_vs_bubbles(df)
    plot_quality_by_machine(df)


if __name__ == "__main__":
    main()