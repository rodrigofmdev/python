from pathlib import Path


def generate_report(df, analysis, output_path: Path) -> None:
    """Write a Markdown report with the production analysis."""

    report_lines = [
        "# PU Foam Injection Production Analysis",
        "",
        "## Dataset overview",
        "",
        f"- Valid production records: {len(df)}",
        f"- Machines analyzed: {df['machine_id'].nunique()}",
        f"- Refrigerator models analyzed: {df['model'].nunique()}",
        "",
        "## Average metrics by machine",
        "",
        "| Machine | Foam density | Air bubbles (%) | Quality score | Efficiency score |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]

    density_by_machine = analysis.density_by_machine(df)
    bubbles_by_machine = analysis.bubbles_by_machine(df)
    quality_by_machine = analysis.quality_by_machine(df)
    efficiency_by_machine = analysis.efficiency_by_machine(df)

    machine_ids = df["machine_id"].drop_duplicates().tolist()
    for machine_id in machine_ids:
        report_lines.append(
            f"| {machine_id} | {density_by_machine[machine_id]:.2f} | "
            f"{bubbles_by_machine[machine_id]:.2f} | "
            f"{quality_by_machine[machine_id]:.2f} | "
            f"{efficiency_by_machine[machine_id]:.4f} |"
        )

    report_lines.extend(
        [
            "",
            "## Key insights",
            "",
            f"- Highest average quality score: "
            f"{analysis.best_machine_quality(df)}.",
            f"- Highest average efficiency score: "
            f"{analysis.best_machine_efficiency(df)}.",
            f"- Humidity level with the lowest average air-bubble rate in "
            f"this sample: {analysis.optimal_humidity(df)}%.",
            f"- Humidity and air-bubble correlation: "
            f"{analysis.humidity_vs_bubbles(df).iloc[0, 1]:.3f}.",
            "",
            "## Quality by refrigerator model",
            "",
        ]
    )

    report_lines.extend(
        f"- **{model}:** {score:.2f}"
        for model, score in analysis.quality_by_model(df).items()
    )
    report_lines.extend(
        [
            "",
            "## Limitations",
            "",
            "This is a small fictional dataset. The observed patterns are "
            "descriptive and do not establish causal relationships.",
            "",
        ]
    )

    output_path.write_text("\n".join(report_lines), encoding="utf-8")