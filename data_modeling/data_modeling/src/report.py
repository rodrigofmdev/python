def generate_report(df, analysis):

    print("\n=== FOAM INJECTION QUALITY ANALYSIS ===")

    print("\nFoam density by machine:")
    print(analysis.density_by_machine(df))

    print("\nAir bubbles percentage (lower is better):")
    print(analysis.bubbles_by_machine(df))

    print("\nQuality score by machine:")
    print(analysis.quality_by_machine(df))


    print("\n=== PROCESS EFFICIENCY ===")

    print("\nEfficiency score by machine:")
    print(analysis.efficiency_by_machine(df))


    print("\n=== ENVIRONMENTAL IMPACT ===")

    print("\nHumidity vs air bubbles correlation:")
    print(analysis.humidity_vs_bubbles(df))


    print("\n=== PRODUCT IMPACT ===")

    print("\nQuality by refrigerator model:")
    print(analysis.quality_by_model(df))


    print("\n=== KEY INSIGHTS ===")

    print(f"Best machine (quality): {analysis.best_machine_quality(df)}")
    print(f"Best machine (efficiency): {analysis.best_machine_efficiency(df)}")
    print(f"Optimal humidity for lowest defects: {analysis.optimal_humidity(df)}%")