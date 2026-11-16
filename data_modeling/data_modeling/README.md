# 🧊 PU Foam Injection Data Analysis for Refrigerator Manufacturing

## 📌 Overview

This project simulates a real-world data system for analyzing the **PU foam injection process** used in refrigerator manufacturing.

The goal is to demonstrate how production and environmental data can be transformed into **actionable insights** to improve:

- Product quality (insulation performance)
- Process efficiency
- Manufacturing consistency

---

## 🧠 Business Context

In refrigerator production, **PU (polyurethane) foam injection** is a critical step that directly impacts thermal insulation.

Key process variables such as:

- Ambient temperature
- Humidity
- Injection time
- Material usage

can significantly affect quality indicators like:

- Foam density
- Air bubble formation (defects)

This project models these relationships and extracts insights to support **data-driven decision making in manufacturing environments**.

---

## ⚙️ Features

- 📥 Data loading and validation
- 🧼 Data cleaning and preprocessing
- 🧠 Feature engineering (quality & efficiency metrics)
- 📊 Process and quality analysis
- 🌍 Environmental impact analysis
- 📈 Visualization of key relationships
- 📄 Automated reporting with insights

---

## 📊 Dataset Description

The dataset simulates production data from foam injection machines and includes:

| Column               | Description                  |
| -------------------- | ---------------------------- |
| `date`               | Production date              |
| `machine_id`         | Injection machine identifier |
| `model`              | Refrigerator model           |
| `ambient_temp_c`     | Ambient temperature (°C)     |
| `humidity_pct`       | Ambient humidity (%)         |
| `foam_density`       | Foam density (kg/m³)         |
| `air_bubbles_pct`    | Defect indicator (%)         |
| `injection_time_sec` | Injection duration (seconds) |
| `material_usage_kg`  | Material consumption (kg)    |
| `cycle_time_sec`     | Total cycle time (seconds)   |

---

## 🧠 Feature Engineering

To enhance analysis, the following metrics were created:

- **Quality Score**
  - Combines density and defect rate
  - Higher = better foam quality

- **Efficiency Score**
  - Based on cycle time
  - Higher = more efficient process

- **High Humidity Flag**
  - Identifies conditions that may increase defect risk

---

## 📈 Key Analyses

This project provides insights such as:

- 📊 Foam quality comparison between machines
- ⚙️ Process efficiency evaluation
- 🌍 Impact of humidity on defect formation
- 🧊 Product-level quality differences
- 🎯 Identification of optimal operating conditions

---

## 💡 Example Insights

- Higher humidity levels tend to increase air bubble formation
- Some machines consistently deliver better quality scores
- Optimal humidity ranges can reduce defect rates
- Trade-offs exist between efficiency and quality

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/rodrigomacarini/python_data_modeling.git
cd python_data_modeling
```

### 2. Install requiments

Instale as dependencias com o comando abaixo

```bash
pip install -r requirements.txt
```

### 3. Run

Open terminal and use

```bash
python main.py
```

## Libraries & Usage

This project leverages a minimal and focused set of Python libraries to ensure clarity, performance, and maintainability.

### Pandas

Used for data manipulation and analysis.

Loading the dataset (read_csv)
Data cleaning (handling duplicates, missing values, type conversion)
Feature engineering (creation of quality and efficiency metrics)
Aggregations (groupby) for performance and quality analysis

Where it is used:

src/data_cleaning.py → data loading and preprocessing
src/analysis.py → grouping and statistical analysis

### Matplotlib

Used for data visualization and exploratory analysis.

Scatter plots to analyze relationships (e.g., humidity vs air bubbles)
Bar charts for comparing machine performance (quality and efficiency)

Where it is used:

src/visualization.py → generation of plots and charts

### Author
Rodrigo Macarini 