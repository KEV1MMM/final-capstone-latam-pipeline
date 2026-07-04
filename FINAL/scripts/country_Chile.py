"""
Country profile script for Chile.
Reads /Users/kevinp/Desktop/capstone-option-b/data/latam_finanzas_clean.csv
and prints a Markdown section with the required statistics.
"""

import pandas as pd
import numpy as np

CSV_PATH = "/Users/kevinp/Desktop/capstone-option-b/data/latam_finanzas_clean.csv"
COUNTRY = "Chile"

df = pd.read_csv(CSV_PATH)
ch = df[df["pais"] == COUNTRY].copy()

# ── 1. Sample size and age range ─────────────────────────────────────────────
n = len(ch)
age_min = int(ch["edad"].min())
age_max = int(ch["edad"].max())

# ── 2. Income statistics (USD) ────────────────────────────────────────────────
inc = ch["ingreso_mensual_usd"]
inc_median = round(inc.median(), 2)
inc_mean   = round(inc.mean(),   2)
inc_min    = round(inc.min(),    2)
inc_max    = round(inc.max(),    2)
inc_std    = round(inc.std(),    2)

# ── 3. Housing burden ─────────────────────────────────────────────────────────
housing_pct = round((ch["gasto_vivienda_usd"] / ch["ingreso_mensual_usd"] * 100).mean(), 2)

# ── 4. Spending breakdown (% of income) ───────────────────────────────────────
gasto_cols = [c for c in ch.columns if c.startswith("gasto_")]
spending = {}
for col in gasto_cols:
    pct = round((ch[col] / ch["ingreso_mensual_usd"] * 100).mean(), 2)
    spending[col] = pct

# ── 5. Savings ────────────────────────────────────────────────────────────────
avg_savings = round(ch["ahorro_mensual_usd"].mean(), 2)
pct_negative = round((ch["ahorro_negativo"] == True).mean() * 100, 2)

# ── 6. AI tools ───────────────────────────────────────────────────────────────
avg_ia_hours = round(ch["horas_herramientas_ia_semana"].mean(), 2)
avg_satisf   = round(ch["satisfaccion_financiera"].mean(), 2)

# ── Print Markdown ─────────────────────────────────────────────────────────────
print(f"## País: {COUNTRY}")
print()
print("### 1. Sample Size and Age Range")
print()
print(f"| Metric | Value |")
print(f"|--------|-------|")
print(f"| Sample size (n) | {n} |")
print(f"| Minimum age | {age_min} |")
print(f"| Maximum age | {age_max} |")
print()

print("### 2. Income (USD / month)")
print()
print(f"| Statistic | Value (USD) |")
print(f"|-----------|-------------|")
print(f"| Median | {inc_median:,.2f} |")
print(f"| Mean | {inc_mean:,.2f} |")
print(f"| Min | {inc_min:,.2f} |")
print(f"| Max | {inc_max:,.2f} |")
print(f"| Std Dev | {inc_std:,.2f} |")
print()

print("### 3. Housing Burden")
print()
print(f"| Metric | Value |")
print(f"|--------|-------|")
print(f"| Avg gasto_vivienda_usd as % of ingreso_mensual_usd | {housing_pct:.2f}% |")
print()

print("### 4. Spending Breakdown (avg % of monthly income)")
print()
print(f"| Category | Avg % of Income |")
print(f"|----------|-----------------|")
for col, pct in spending.items():
    label = col.replace("gasto_", "").replace("_", " ").title()
    print(f"| {label} | {pct:.2f}% |")
print()

print("### 5. Savings")
print()
print(f"| Metric | Value |")
print(f"|--------|-------|")
print(f"| Avg ahorro_mensual_usd | {avg_savings:,.2f} USD |")
print(f"| Respondents with negative savings | {pct_negative:.2f}% |")
print()

print("### 6. AI Tools and Financial Satisfaction")
print()
print(f"| Metric | Value |")
print(f"|--------|-------|")
print(f"| Avg horas_herramientas_ia_semana | {avg_ia_hours:.2f} hrs/week |")
print(f"| Avg satisfaccion_financiera (1-5) | {avg_satisf:.2f} |")
