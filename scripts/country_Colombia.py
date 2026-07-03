"""
Country profile script for Colombia.
Reads data/latam_finanzas_clean.csv and prints a Markdown section
with the 6 required statistical subsections.
"""

import pandas as pd
import numpy as np

DATA_PATH = "/Users/kevinp/Desktop/capstone-option-b/data/latam_finanzas_clean.csv"
COUNTRY = "Colombia"

df = pd.read_csv(DATA_PATH)
co = df[df["pais"] == COUNTRY].copy()

# ── 1. Sample size and age range ──────────────────────────────────────────────
n = len(co)
age_min = int(co["edad"].min())
age_max = int(co["edad"].max())

# ── 2. Income statistics (USD) ────────────────────────────────────────────────
inc = co["ingreso_mensual_usd"]
inc_median = round(inc.median(), 2)
inc_mean   = round(inc.mean(), 2)
inc_min    = round(inc.min(), 2)
inc_max    = round(inc.max(), 2)
inc_std    = round(inc.std(ddof=1), 2)

# ── 3. Housing burden ─────────────────────────────────────────────────────────
co["housing_burden_pct"] = co["gasto_vivienda_usd"] / co["ingreso_mensual_usd"] * 100
avg_housing_burden = round(co["housing_burden_pct"].mean(), 2)

# ── 4. Spending breakdown (% of income) ──────────────────────────────────────
gasto_cols = [c for c in df.columns if c.startswith("gasto_")]
spending = {}
for col in gasto_cols:
    co[f"{col}_pct"] = co[col] / co["ingreso_mensual_usd"] * 100
    spending[col] = round(co[f"{col}_pct"].mean(), 2)

# ── 5. Savings ────────────────────────────────────────────────────────────────
avg_savings = round(co["ahorro_mensual_usd"].mean(), 2)
pct_negative = round((co["ahorro_negativo"] == True).mean() * 100, 2)

# ── 6. AI tools & financial satisfaction ─────────────────────────────────────
avg_ia_hours = round(co["horas_herramientas_ia_semana"].mean(), 2)
avg_satisfac = round(co["satisfaccion_financiera"].mean(), 2)

# ── Print Markdown ────────────────────────────────────────────────────────────
print(f"## País: {COUNTRY}")
print()

print("### 1. Sample Size and Age Range")
print()
print(f"- **Sample size:** {n} respondents")
print(f"- **Age range:** {age_min} – {age_max} years")
print()

print("### 2. Income (USD/month)")
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
print(f"- **Average gasto_vivienda_usd as % of ingreso_mensual_usd:** {avg_housing_burden}%")
print()

print("### 4. Spending Breakdown (avg % of monthly income)")
print()
print(f"| Category | Avg % of Income |")
print(f"|----------|----------------|")
for col, pct in spending.items():
    label = col.replace("gasto_", "").replace("_", " ").title()
    print(f"| {label} | {pct}% |")
print()

print("### 5. Savings")
print()
print(f"- **Average ahorro_mensual_usd:** ${avg_savings:,.2f}")
print(f"- **Respondents with negative savings:** {pct_negative}%")
print()

print("### 6. AI Tools and Financial Satisfaction")
print()
print(f"- **Average horas_herramientas_ia_semana:** {avg_ia_hours} hrs/week")
print(f"- **Average satisfaccion_financiera:** {avg_satisfac} / 5")
