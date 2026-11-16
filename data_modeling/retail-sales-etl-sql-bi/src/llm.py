import os

import pandas as pd


def generate_ai_insights(
    sales_by_category: pd.DataFrame,
    sales_by_state: pd.DataFrame,
) -> str:
    """Summarize aggregated sales tables with the OpenAI API."""

    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit(
            "Set OPENAI_API_KEY to use --ai-insights."
        )

    from openai import OpenAI

    summaries = {
        "sales_by_category": sales_by_category.to_dict(orient="records"),
        "sales_by_state": sales_by_state.to_dict(orient="records"),
    }
    response = OpenAI().chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é uma pessoa analista de dados. Resuma os "
                    "resultados agregados de vendas em português do Brasil, "
                    "com clareza. Diferencie observações de hipóteses e "
                    "não invente causas."
                ),
            },
            {
                "role": "user",
                "content": f"Analise estas tabelas agregadas de vendas: {summaries}",
            },
        ],
        temperature=0.2,
    )
    content = response.choices[0].message.content
    if not content:
        raise ValueError("A IA retornou uma análise de vendas vazia.")
    return content
