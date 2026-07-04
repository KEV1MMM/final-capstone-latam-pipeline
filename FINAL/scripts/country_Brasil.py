"""
Country profile script for Brasil.
Reads data/latam_finanzas_clean.csv and prints a Markdown section
with 6 statistical sections for Brasil respondents.
"""

import pandas as pd
import numpy as np

DATA_PATH = "/Users/kevinp/Desktop/capstone-option-b/data/latam_finanzas_clean.csv"

df = pd.read_csv(DATA_PATH)
country = "Brasil"
br = df[df["pais"] == country].copy()

# ── 1. Sample size & age range ──────────────────────────────────────────────
n = len(br)
age_min = br["edad"].min()
age_max = br["edad"].max()

# ── 2. Income statistics (USD) ───────────────────────────────────────────────
inc = br["ingreso_mensual_usd"]
inc_median = inc.median()
inc_mean   = inc.mean()
inc_min    = inc.min()
inc_max    = inc.max()
inc_std    = inc.std()

# ── 3. Housing burden ────────────────────────────────────────────────────────
housing_pct = (br["gasto_vivienda_usd"] / br["ingreso_mensual_usd"] * 100).mean()

# ── 4. Spending breakdown (% of income) ─────────────────────────────────────
gasto_cols = [c for c in df.columns if c.startswith("gasto_")]
spending = {}
for col in gasto_cols:
    pct = (br[col] / br["ingreso_mensual_usd"] * 100).mean()
    spending[col] = pct

# ── 5. Savings ───────────────────────────────────────────────────────────────
avg_savings = br["ahorro_mensual_usd"].mean()
neg_savings_pct = br["ahorro_negativo"].apply(
    lambda x: x if isinstance(x, bool) else str(x).strip().lower() == "true"
).mean() * 100

# ── 6. AI tools & financial satisfaction ────────────────────────────────────
avg_ia_hours = br["horas_herramientas_ia_semana"].mean()
avg_satisf   = br["satisfaccion_financiera"].mean()

# ── Print Markdown ────────────────────────────────────────────────────────────
print(f"## País: {country}")
print()
print("### 1. Sample Size and Age Range")
print()
print(f"| Metric | Value |")
print(f"|--------|-------|")
print(f"| Sample size (n) | {n} |")
print(f"| Age range | {age_min} – {age_max} years |")
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
print(f"| Respondents with negative savings | {neg_savings_pct:.2f}% |")
print()
print("### 6. AI Tools and Financial Satisfaction")
print()
print(f"| Metric | Value |")
print(f"|--------|-------|")
print(f"| Avg horas_herramientas_ia_semana | {avg_ia_hours:.2f} hrs/week |")
print(f"| Avg satisfaccion_financiera | {avg_satisf:.2f} / 5 |")
