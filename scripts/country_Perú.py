"""
country_Perú.py
Statistical profile for Perú from latam_finanzas_clean.csv.
"""

import pandas as pd

DATA_PATH = "/Users/kevinp/Desktop/capstone-option-b/data/latam_finanzas_clean.csv"

df = pd.read_csv(DATA_PATH)
peru = df[df["pais"] == "Perú"].copy()

# ---------------------------------------------------------------------------
# 1. Sample size and age range
# ---------------------------------------------------------------------------
n = len(peru)
age_min = peru["edad"].min()
age_max = peru["edad"].max()

# ---------------------------------------------------------------------------
# 2. Income statistics (USD)
# ---------------------------------------------------------------------------
income = peru["ingreso_mensual_usd"]
income_median = income.median()
income_mean = income.mean()
income_min = income.min()
income_max = income.max()
income_std = income.std()

# ---------------------------------------------------------------------------
# 3. Housing burden
# ---------------------------------------------------------------------------
housing_pct = (peru["gasto_vivienda_usd"] / peru["ingreso_mensual_usd"] * 100).mean()

# ---------------------------------------------------------------------------
# 4. Spending breakdown — each gasto_* column as % of ingreso_mensual_usd
# ---------------------------------------------------------------------------
gasto_cols = [c for c in peru.columns if c.startswith("gasto_")]
spending = {}
for col in gasto_cols:
    spending[col] = (peru[col] / peru["ingreso_mensual_usd"] * 100).mean()

# ---------------------------------------------------------------------------
# 5. Savings
# ---------------------------------------------------------------------------
avg_savings = peru["ahorro_mensual_usd"].mean()
neg_savings_pct = peru["ahorro_negativo"].apply(
    lambda x: x if isinstance(x, bool) else str(x).strip().lower() == "true"
).mean() * 100

# ---------------------------------------------------------------------------
# 6. AI tools & financial satisfaction
# ---------------------------------------------------------------------------
avg_ia_hours = peru["horas_herramientas_ia_semana"].mean()
avg_satisfaccion = peru["satisfaccion_financiera"].mean()

# ---------------------------------------------------------------------------
# Print results
# ---------------------------------------------------------------------------
print("=" * 60)
print(f"COUNTRY PROFILE: Perú")
print("=" * 60)

print(f"\n[1] Sample & Age")
print(f"    n = {n}")
print(f"    Age range: {age_min} – {age_max}")

print(f"\n[2] Income (USD/month)")
print(f"    Median : {income_median:.2f}")
print(f"    Mean   : {income_mean:.2f}")
print(f"    Min    : {income_min:.2f}")
print(f"    Max    : {income_max:.2f}")
print(f"    Std Dev: {income_std:.2f}")

print(f"\n[3] Housing Burden")
print(f"    Avg gasto_vivienda as % of income: {housing_pct:.1f}%")

print(f"\n[4] Spending Breakdown (avg % of income)")
for col, pct in spending.items():
    print(f"    {col:<35} {pct:.1f}%")

print(f"\n[5] Savings")
print(f"    Avg ahorro_mensual_usd  : {avg_savings:.2f}")
print(f"    % with negative savings : {neg_savings_pct:.1f}%")

print(f"\n[6] AI Tools & Satisfaction")
print(f"    Avg horas_herramientas_ia_semana : {avg_ia_hours:.2f}")
print(f"    Avg satisfaccion_financiera      : {avg_satisfaccion:.2f}")
