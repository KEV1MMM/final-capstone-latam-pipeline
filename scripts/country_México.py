"""
Country profile script for México.
Reads data/latam_finanzas_clean.csv and prints a Markdown section
with demographic, income, housing, spending, savings, and AI-tool stats.
"""

import pandas as pd
import numpy as np

DATA_PATH = "/Users/kevinp/Desktop/capstone-option-b/data/latam_finanzas_clean.csv"
COUNTRY = "México"

df = pd.read_csv(DATA_PATH)
mx = df[df["pais"] == COUNTRY].copy()

# ── 1. Sample size & age range ──────────────────────────────────────────────
n = len(mx)
age_min = int(mx["edad"].min())
age_max = int(mx["edad"].max())

# ── 2. Income (USD) ─────────────────────────────────────────────────────────
inc = mx["ingreso_mensual_usd"]
inc_median = inc.median()
inc_mean   = inc.mean()
inc_min    = inc.min()
inc_max    = inc.max()
inc_std    = inc.std()

# ── 3. Housing burden ───────────────────────────────────────────────────────
housing_pct = (mx["gasto_vivienda_usd"] / mx["ingreso_mensual_usd"] * 100).mean()

# ── 4. Spending breakdown ────────────────────────────────────────────────────
gasto_cols = [c for c in df.columns if c.startswith("gasto_")]
spending = {}
for col in gasto_cols:
    pct = (mx[col] / mx["ingreso_mensual_usd"] * 100).mean()
    spending[col] = pct

# ── 5. Savings ───────────────────────────────────────────────────────────────
avg_savings = mx["ahorro_mensual_usd"].mean()
# ahorro_negativo is stored as True/False strings or booleans
neg_col = mx["ahorro_negativo"]
# handle both bool and string representations
if neg_col.dtype == object:
    neg_savings_pct = (neg_col.str.lower() == "true").mean() * 100
else:
    neg_savings_pct = neg_col.mean() * 100

# ── 6. AI tools & financial satisfaction ─────────────────────────────────────
avg_ia_hours = mx["horas_herramientas_ia_semana"].mean()
avg_satisfaccion = mx["satisfaccion_financiera"].mean()

# ── Print Markdown ───────────────────────────────────────────────────────────
print(f"## País: {COUNTRY}")
print()
print("### 1. Sample Size and Age Range")
print()
print(f"| Metric | Value |")
print(f"|--------|-------|")
print(f"| Sample size (n) | {n} |")
print(f"| Age range | {age_min} – {age_max} years |")
print()
print("### 2. Income (USD/month)")
print()
print(f"| Metric | Value |")
print(f"|--------|-------|")
print(f"| Median | ${inc_median:,.2f} |")
print(f"| Mean | ${inc_mean:,.2f} |")
print(f"| Min | ${inc_min:,.2f} |")
print(f"| Max | ${inc_max:,.2f} |")
print(f"| Std Dev | ${inc_std:,.2f} |")
print()
print("### 3. Housing Burden")
print()
print(f"| Metric | Value |")
print(f"|--------|-------|")
print(f"| Avg gasto_vivienda_usd as % of income | {housing_pct:.1f}% |")
print()
print("### 4. Spending Breakdown (avg % of monthly income)")
print()
print("| Spending Category | Avg % of Income |")
print("|-------------------|-----------------|")
for col, pct in spending.items():
    label = col.replace("gasto_", "").replace("_", " ").title()
    print(f"| {label} | {pct:.1f}% |")
print()
print("### 5. Savings")
print()
print(f"| Metric | Value |")
print(f"|--------|-------|")
print(f"| Avg ahorro_mensual_usd | ${avg_savings:,.2f} |")
print(f"| Respondents with negative savings | {neg_savings_pct:.1f}% |")
print()
print("### 6. AI Tools and Financial Satisfaction")
print()
print(f"| Metric | Value |")
print(f"|--------|-------|")
print(f"| Avg horas_herramientas_ia_semana | {avg_ia_hours:.2f} hrs/week |")
print(f"| Avg satisfaccion_financiera (1–5) | {avg_satisfaccion:.2f} |")
