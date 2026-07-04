import pandas as pd
from scipy import stats

df = pd.read_csv("data/latam_finanzas_clean.csv")

SEP = "=" * 70

# ── 1. INCOME BY COUNTRY (from country profiles) ─────────────────────────────
print(SEP)
print("1. INCOME BY COUNTRY")
print(SEP)

income = (
    df.groupby("pais")["ingreso_mensual_usd"]
    .agg(median="median", mean="mean", min="min", max="max", std="std")
    .round(2)
    .sort_values("median", ascending=False)
    .reset_index()
)
income.columns = ["Country", "Median (USD)", "Mean (USD)", "Min (USD)", "Max (USD)", "Std Dev"]
print(income.to_string(index=False))

# ── 2. AGE VS. SAVINGS ────────────────────────────────────────────────────────
print(f"\n{SEP}")
print("2. AGE VS. SAVINGS")
print(SEP)

bins   = [17, 22, 25, 28, 32]
labels = ["18–22", "23–25", "26–28", "29–32"]
df["age_group"] = pd.cut(df["edad"], bins=bins, labels=labels)
df["savings_rate"] = df["ahorro_mensual_usd"] / df["ingreso_mensual_usd"] * 100

age_savings = (
    df.groupby("age_group", observed=True)
    .agg(
        n=("ahorro_mensual_usd", "count"),
        avg_savings=("ahorro_mensual_usd", "mean"),
        avg_savings_rate=("savings_rate", "mean"),
    )
    .round(2)
    .reset_index()
)
age_savings.columns = ["Age Group", "n", "Avg Monthly Savings (USD)", "Avg Savings Rate (%)"]
print(age_savings.to_string(index=False))

# ── 3. SPENDING BREAKDOWN (full sample) ──────────────────────────────────────
print(f"\n{SEP}")
print("3. SPENDING BREAKDOWN — FULL SAMPLE")
print(SEP)

gasto_cols = {
    "gasto_vivienda_usd":       "Housing",
    "gasto_alimentacion_usd":   "Food",
    "gasto_transporte_usd":     "Transport",
    "gasto_entretenimiento_usd":"Entertainment",
    "gasto_educacion_usd":      "Education",
    "gasto_salud_usd":          "Healthcare",
}
rows = []
for col, label in gasto_cols.items():
    pct = (df[col] / df["ingreso_mensual_usd"] * 100).mean()
    avg_usd = df[col].mean()
    rows.append({"Category": label, "Avg % of Income": round(pct, 2), "Avg USD/month": round(avg_usd, 2)})

spend_df = pd.DataFrame(rows).sort_values("Avg % of Income", ascending=False).reset_index(drop=True)
print(spend_df.to_string(index=False))

# ── 4. CREDIT CARD HOLDERS VS NON-HOLDERS ────────────────────────────────────
print(f"\n{SEP}")
print("4. CREDIT CARD HOLDERS VS NON-HOLDERS")
print(SEP)

cc_metrics = {
    "ingreso_mensual_usd":      "Avg Income (USD)",
    "gasto_alimentacion_usd":   "Avg Food Spending (USD)",
    "gasto_entretenimiento_usd":"Avg Entertainment (USD)",
    "ahorro_mensual_usd":       "Avg Savings (USD)",
}
holders    = df[df["tiene_tarjeta_credito"] == "Sí"]
no_holders = df[df["tiene_tarjeta_credito"] == "No"]

cc_rows = []
for col, label in cc_metrics.items():
    h_val  = holders[col].mean()
    nh_val = no_holders[col].mean()
    pct_diff = (h_val - nh_val) / nh_val * 100
    cc_rows.append({
        "Metric": label,
        "Has Card": round(h_val, 2),
        "No Card":  round(nh_val, 2),
        "% Diff":   f"{pct_diff:+.1f}%",
    })

cc_df = pd.DataFrame(cc_rows)
print(cc_df.to_string(index=False))
print(f"\n  Card holders: {len(holders)}  |  Non-holders: {len(no_holders)}")

# ── 5. AI TOOL USAGE VS FINANCIAL SATISFACTION ───────────────────────────────
print(f"\n{SEP}")
print("5. AI TOOL USAGE VS FINANCIAL SATISFACTION")
print(SEP)

ai_bins   = [-0.1, 3, 10, 100]
ai_labels = ["Low (0–3 hrs)", "Medium (4–10 hrs)", "High (11+ hrs)"]
df["ai_group"] = pd.cut(df["horas_herramientas_ia_semana"], bins=ai_bins, labels=ai_labels)

ai_df = (
    df.groupby("ai_group", observed=True)
    .agg(
        n=("satisfaccion_financiera", "count"),
        avg_satisfaction=("satisfaccion_financiera", "mean"),
        avg_income=("ingreso_mensual_usd", "mean"),
    )
    .round(2)
    .reset_index()
)
ai_df.columns = ["AI Usage Group", "n", "Avg Satisfaction (1–5)", "Avg Income (USD)"]
print(ai_df.to_string(index=False))

r, p = stats.pearsonr(df["horas_herramientas_ia_semana"], df["satisfaccion_financiera"])
sig  = "significant" if p < 0.05 else "not significant"
print(f"\n  Pearson r = {r:.4f}  |  p-value = {p:.4f}  ({sig} at α=0.05)")

# ── 6. HOUSING BURDEN BY COUNTRY (from country profiles) ─────────────────────
print(f"\n{SEP}")
print("6. HOUSING BURDEN BY COUNTRY")
print(SEP)

df["housing_pct"] = df["gasto_vivienda_usd"] / df["ingreso_mensual_usd"] * 100
housing = (
    df.groupby("pais")
    .agg(
        n=("housing_pct", "count"),
        avg_housing_pct=("housing_pct", "mean"),
        avg_housing_usd=("gasto_vivienda_usd", "mean"),
        avg_income_usd=("ingreso_mensual_usd", "mean"),
    )
    .round(2)
    .sort_values("avg_housing_pct", ascending=False)
    .reset_index()
)
housing.columns = ["Country", "n", "Avg Housing % of Income", "Avg Housing (USD)", "Avg Income (USD)"]
print(housing.to_string(index=False))
