from pathlib import Path

import pandas as pd


CATEGORY_TRANSLATIONS = {
    "Accessories": "Acessórios",
    "Electronics": "Eletrônicos",
    "Furniture": "Móveis",
    "Mobile": "Celulares",
}


def format_brazilian_currency(value: float) -> str:
    formatted = f"{value:,.2f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


def generate_markdown_report(
    raw_record_count: int,
    cleaned_record_count: int,
    reports: dict[str, pd.DataFrame],
    output_path: Path,
    ai_insights: str | None = None,
) -> None:
    summary = reports["sales_summary"].iloc[0]
    category_sales = reports["sales_by_category"].rename(
        columns={
            "category": "Categoria",
            "order_count": "Pedidos",
            "units_sold": "Unidades vendidas",
            "total_sales": "Vendas totais (R$)",
            "average_line_value": "Valor médio por item (R$)",
        }
    )
    category_sales["Categoria"] = category_sales["Categoria"].replace(
        CATEGORY_TRANSLATIONS
    )
    category_sales["Vendas totais (R$)"] = category_sales[
        "Vendas totais (R$)"
    ].map(format_brazilian_currency)
    category_sales["Valor médio por item (R$)"] = category_sales[
        "Valor médio por item (R$)"
    ].map(format_brazilian_currency)
    category_sales["Pedidos"] = category_sales["Pedidos"].astype(int)
    category_sales["Unidades vendidas"] = category_sales[
        "Unidades vendidas"
    ].astype(int)

    state_sales = reports["sales_by_state"].rename(
        columns={
            "state": "Estado",
            "order_count": "Pedidos",
            "units_sold": "Unidades vendidas",
            "total_sales": "Vendas totais (R$)",
        }
    )
    state_sales["Pedidos"] = state_sales["Pedidos"].astype(int)
    state_sales["Unidades vendidas"] = state_sales[
        "Unidades vendidas"
    ].astype(int)
    state_sales["Vendas totais (R$)"] = state_sales[
        "Vendas totais (R$)"
    ].map(format_brazilian_currency)

    lines = [
        "# Análise de Vendas no Varejo",
        "",
        "## Resumo do pipeline",
        "",
        f"- Linhas na origem: {raw_record_count}",
        f"- Itens de pedido válidos carregados: {cleaned_record_count}",
        f"- Registros duplicados ou inválidos removidos: "
        f"{raw_record_count - cleaned_record_count}",
        "",
        "## Indicadores de vendas",
        "",
        f"- Vendas totais: R$ "
        f"{format_brazilian_currency(summary['total_sales'])}",
        f"- Pedidos distintos: {int(summary['order_count'])}",
        f"- Unidades vendidas: {int(summary['units_sold'])}",
        f"- Ticket médio: R$ "
        f"{format_brazilian_currency(summary['average_order_value'])}",
        "",
        "## Vendas por categoria",
        "",
        category_sales.to_markdown(index=False),
        "",
        "## Vendas por estado",
        "",
        state_sales.to_markdown(index=False),
        "",
    ]

    if ai_insights is not None:
        lines.extend(
            [
                "## Análise complementar gerada por IA",
                "",
                ai_insights,
                "",
            ]
        )

    lines.extend(
        [
            "## Limitações",
            "",
            "Os dados fornecidos são fictícios e limitados. Os resultados "
            "demonstram um fluxo de análise e não devem ser interpretados "
            "como previsões de negócio nem como evidência de relações causais.",
            "",
        ]
    )
    output_path.write_text("\n".join(lines), encoding="utf-8")


def generate_excel_workbook(
    cleaned_sales: pd.DataFrame,
    reports: dict[str, pd.DataFrame],
    output_path: Path,
) -> None:
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        cleaned_sales.to_excel(
            writer,
            sheet_name="Cleaned Sales",
            index=False,
        )
        for sheet_name, report_data in reports.items():
            report_data.to_excel(
                writer,
                sheet_name=sheet_name[:31],
                index=False,
            )


def generate_powerbi_workbook(
    model_tables: dict[str, pd.DataFrame],
    output_path: Path,
) -> None:
    """Write the relational dimensions and fact table for Power BI import."""

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for table_name, table in model_tables.items():
            table.to_excel(
                writer,
                sheet_name=table_name,
                index=False,
            )
