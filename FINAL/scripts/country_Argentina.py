"""
Country profile script for Argentina.
Reads /Users/kevinp/Desktop/capstone-option-b/data/latam_finanzas_clean.csv
and prints a Markdown section with 6 statistical sections.
"""

import pandas as pd
import numpy as np

DATA_PATH = "/Users/kevinp/Desktop/capstone-option-b/data/latam_finanzas_clean.csv"
COUNTRY = "Argentina"

df = pd.read_csv(DATA_PATH)
ar = df[df["pais"] == COUNTRY].copy()

# ── 1. Sample size and age range ─────────────────────────────────────────────
n = len(ar)
age_min = int(ar["edad"].min())
age_max = int(ar["edad"].max())

# ── 2. Income statistics (USD) ────────────────────────────────────────────────
inc = ar["ingreso_mensual_usd"]
inc_median = round(inc.median(), 2)
inc_mean   = round(inc.mean(),   2)
inc_min    = round(inc.min(),    2)
inc_max    = round(inc.max(),    2)
inc_std    = round(inc.std(),    2)

# ── 3. Housing burden ─────────────────────────────────────────────────────────
ar["housing_pct"] = ar["gasto_vivienda_usd"] / ar["ingreso_mensual_usd"] * 100
housing_burden = round(ar["housing_pct"].mean(), 2)

# ── 4. Spending breakdown (% of income) ───────────────────────────────────────
gasto_cols = [c for c in df.columns if c.startswith("gasto_")]
spending = {}
for col in gasto_cols:
    pct = (ar[col] / ar["ingreso_mensual_usd"] * 100).mean()
    spending[col] = round(pct, 2)

# ── 5. Savings ────────────────────────────────────────────────────────────────
avg_savings = round(ar["ahorro_mensual_usd"].mean(), 2)
pct_negative = round((ar["ahorro_negativo"] == True).mean() * 100, 2)

# ── 6. AI tools & financial satisfaction ─────────────────────────────────────
avg_ia_hours = round(ar["horas_herramientas_ia_semana"].mean(), 2)
avg_satisf   = round(ar["satisfaccion_financiera"].mean(), 2)

# ── Print Markdown ────────────────────────────────────────────────────────────
print(f"## País: {COUNTRY}")
print()

print("### 1. Sample Size and Age Range")
print()
print(f"- **Sample size:** {n} respondents")
print(f"- **Age range:** {age_min} – {age_max} years")
print()

print("### 2. Income (USD / month)")
print()
print(f"| Statistic | Value (USD) |")
print(f"|-----------|------------|")
print(f"| Median    | {inc_median:,.2f} |")
print(f"| Mean      | {inc_mean:,.2f} |")
print(f"| Min       | {inc_min:,.2f} |")
print(f"| Max       | {inc_max:,.2f} |")
print(f"| Std Dev   | {inc_std:,.2f} |")
print()

print("### 3. Housing Burden")
print()
print(f"- **Average gasto_vivienda_usd as % of ingreso_mensual_usd:** {housing_burden}%")
print()

print("### 4. Spending Breakdown (average % of monthly income)")
print()
print("| Category | Avg % of Income |")
print("|----------|----------------|")
for col, pct in spending.items():
    label = col.replace("gasto_", "").replace("_", " ").title()
    print(f"| {label} | {pct}% |")
print()

print("### 5. Savings")
print()
print(f"- **Average ahorro_mensual_usd:** {avg_savings:,.2f} USD")
print(f"- **Respondents with negative savings:** {pct_negative}%")
print()

print("### 6. AI Tools and Financial Satisfaction")
print()
print(f"- **Average horas_herramientas_ia_semana:** {avg_ia_hours} hours/week")
print(f"- **Average satisfaccion_financiera:** {avg_satisf} / 5")
