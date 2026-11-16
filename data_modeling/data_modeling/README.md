# PU Foam Injection Data Analysis

## 🎯 Objective

Analyze fictional polyurethane foam injection data from refrigerator
manufacturing to explore process quality, efficiency, and environmental
conditions.

## ✨ Features

- Load and validate production data with Pandas.
- Remove duplicate and invalid records.
- Engineer quality, efficiency, and humidity metrics.
- Compare production machines and refrigerator models.
- Generate a Markdown report and charts.
- Save each run's outputs in a timestamped folder.

## 📂 Project Structure

- `main.py`: command-line entry point and analysis workflow.
- `src/data_cleaning.py`: input loading, validation, cleaning, and features.
- `src/analysis.py`: grouped metrics and comparisons.
- `src/report.py`: Markdown report generation.
- `src/visualization.py`: chart generation.
- `data/production_data.csv`: sample input data.
- `requirements.txt`: Python dependencies.
- `output/`: timestamped reports and charts.

## 📊 Input Data

The sample dataset contains production date, machine, refrigerator model,
ambient temperature, humidity, foam density, air-bubble rate, injection time,
material use, and cycle time.

The dataset is intentionally small and fictional. Its patterns are suitable
for learning, not for making operational decisions.

## 🚀 How to Run

### 1. Navigate to the project folder

From the repository root, run:

```powershell
cd .\python\data_modeling\data_modeling
```

### 2. Install dependencies

```powershell
py -3.15 -m pip install -r requirements.txt
```

### 3. Run the analysis

```powershell
py -3.15 .\main.py
```

To analyze a different CSV file, provide its path:

```powershell
py -3.15 .\main.py --input .\data\production_data.csv
```

## 📄 Results

Each run creates `output/YYYY-MM-DD-HH-MM-SS/` with:

- `report.md`
- `humidity_vs_air_bubbles.png`
- `quality_by_machine.png`

## ✍️ Author

@rodrigofmdev

- Email: rodrigofmdev@gmail.com
- GitHub: [github.com/rodrigofmdev](https://github.com/rodrigofmdev)
- LinkedIn: [linkedin.com/in/rodrigofmdev](https://linkedin.com/in/rodrigofmdev)
