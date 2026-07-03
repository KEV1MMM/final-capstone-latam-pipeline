import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

df = pd.read_csv("data/latam_finanzas_clean.csv")

SOURCE = "Source: Encuesta de Bienestar Financiero LatAm 2025, Futuro Digital LatAm"

COUNTRY_PALETTE = {
    "Brasil":    "#1B6CA8",
    "Chile":     "#2E9E6B",
    "México":    "#E05C1A",
    "Colombia":  "#8B3FC8",
    "Perú":      "#D4A017",
    "Argentina": "#C0392B",
}

def add_source(fig):
    fig.text(0.5, 0.01, SOURCE, ha="center", va="bottom",
             fontsize=7, color="#666666", style="italic")

# ── 1. Box plot: income distribution by country ───────────────────────────────
order = (
    df.groupby("pais")["ingreso_mensual_usd"]
    .median()
    .sort_values(ascending=False)
    .index.tolist()
)

fig, ax = plt.subplots(figsize=(10, 6))
data_by_country = [df[df["pais"] == c]["ingreso_mensual_usd"].dropna().values for c in order]
colors = [COUNTRY_PALETTE[c] for c in order]

bp = ax.boxplot(
    data_by_country,
    patch_artist=True,
    widths=0.5,
    medianprops=dict(color="white", linewidth=2),
    whiskerprops=dict(linewidth=1.2),
    capprops=dict(linewidth=1.2),
    flierprops=dict(marker="o", markersize=4, alpha=0.5),
)
for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.85)
for flier, color in zip(bp["fliers"], colors):
    flier.set_markerfacecolor(color)
    flier.set_markeredgecolor(color)

ax.set_xticks(range(1, len(order) + 1))
ax.set_xticklabels(order, fontsize=11)
ax.set_xlabel("Country", fontsize=12, labelpad=8)
ax.set_ylabel("Monthly Income (USD)", fontsize=12, labelpad=8)
ax.set_title("Income Distribution by Country\n(sorted by median income)", fontsize=14, fontweight="bold", pad=14)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.grid(axis="y", linestyle="--", alpha=0.4)
ax.spines[["top", "right"]].set_visible(False)
add_source(fig)
fig.tight_layout(rect=[0, 0.04, 1, 1])
fig.savefig("charts/01_income_by_country.png", dpi=150)
plt.close()
print("Saved charts/01_income_by_country.png")

# ── 2. Scatter plot: age vs savings, coloured by country, with trend line ─────
fig, ax = plt.subplots(figsize=(10, 6))

for country, grp in df.groupby("pais"):
    ax.scatter(
        grp["edad"], grp["ahorro_mensual_usd"],
        label=country, color=COUNTRY_PALETTE[country],
        alpha=0.65, s=35, edgecolors="none",
    )

x = df["edad"].values
y = df["ahorro_mensual_usd"].values
m, b = np.polyfit(x, y, 1)
x_line = np.linspace(x.min(), x.max(), 200)
ax.plot(x_line, m * x_line + b, color="#222222", linewidth=2,
        linestyle="--", label=f"Trend (slope={m:.1f})")

ax.axhline(0, color="#999999", linewidth=0.8, linestyle="-")
ax.set_xlabel("Age (years)", fontsize=12, labelpad=8)
ax.set_ylabel("Monthly Savings (USD)", fontsize=12, labelpad=8)
ax.set_title("Age vs. Monthly Savings\nwith linear trend line, coloured by country",
             fontsize=14, fontweight="bold", pad=14)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.legend(fontsize=9, framealpha=0.8, loc="upper left")
ax.grid(linestyle="--", alpha=0.35)
ax.spines[["top", "right"]].set_visible(False)
add_source(fig)
fig.tight_layout(rect=[0, 0.04, 1, 1])
fig.savefig("charts/02_age_vs_savings.png", dpi=150)
plt.close()
print("Saved charts/02_age_vs_savings.png")

# ── 3. Horizontal bar: spending breakdown (% of income) ───────────────────────
gasto_cols = {
    "gasto_vivienda_usd":        "Housing",
    "gasto_alimentacion_usd":    "Food",
    "gasto_transporte_usd":      "Transport",
    "gasto_entretenimiento_usd": "Entertainment",
    "gasto_educacion_usd":       "Education",
    "gasto_salud_usd":           "Healthcare",
}
pcts = {label: (df[col] / df["ingreso_mensual_usd"] * 100).mean()
        for col, label in gasto_cols.items()}
spend_df = pd.Series(pcts).sort_values(ascending=True)

BAR_COLORS = ["#1B6CA8", "#2E9E6B", "#E05C1A", "#8B3FC8", "#D4A017", "#C0392B"]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(spend_df.index, spend_df.values, color=BAR_COLORS, height=0.55)
for bar, val in zip(bars, spend_df.values):
    ax.text(val + 0.3, bar.get_y() + bar.get_height() / 2,
            f"{val:.1f}%", va="center", fontsize=10)

ax.set_xlabel("Average % of Monthly Income", fontsize=12, labelpad=8)
ax.set_title("Average Spending Breakdown\n(% of monthly income, full sample)",
             fontsize=14, fontweight="bold", pad=14)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))
ax.set_xlim(0, spend_df.max() * 1.18)
ax.grid(axis="x", linestyle="--", alpha=0.4)
ax.spines[["top", "right"]].set_visible(False)
add_source(fig)
fig.tight_layout(rect=[0, 0.04, 1, 1])
fig.savefig("charts/03_spending_breakdown.png", dpi=150)
plt.close()
print("Saved charts/03_spending_breakdown.png")

# ── 4. Bar chart: satisfaction by AI usage group ──────────────────────────────
ai_bins   = [-0.1, 3, 10, 100]
ai_labels = ["Low\n(0–3 hrs/week)", "Medium\n(4–10 hrs/week)", "High\n(11+ hrs/week)"]
df["ai_group"] = pd.cut(df["horas_herramientas_ia_semana"], bins=ai_bins, labels=ai_labels)
ai_sat = df.groupby("ai_group", observed=True)["satisfaccion_financiera"].mean()

AI_COLORS = ["#AAC4E0", "#4A90D9", "#1B6CA8"]

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(ai_sat.index, ai_sat.values, color=AI_COLORS, width=0.5)
for bar, val in zip(bars, ai_sat.values):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 0.04,
            f"{val:.2f}", ha="center", va="bottom", fontsize=12, fontweight="bold")

ax.set_ylim(0, 5)
ax.set_yticks([0, 1, 2, 3, 4, 5])
ax.set_xlabel("AI Tool Usage Group", fontsize=12, labelpad=8)
ax.set_ylabel("Avg Financial Satisfaction (1–5)", fontsize=12, labelpad=8)
ax.set_title("Financial Satisfaction by AI Tool Usage",
             fontsize=14, fontweight="bold", pad=14)
ax.grid(axis="y", linestyle="--", alpha=0.4)
ax.spines[["top", "right"]].set_visible(False)
add_source(fig)
fig.tight_layout(rect=[0, 0.04, 1, 1])
fig.savefig("charts/04_satisfaction_by_ai_usage.png", dpi=150)
plt.close()
print("Saved charts/04_satisfaction_by_ai_usage.png")

# ── 5. Horizontal bar: housing burden by country ──────────────────────────────
df["housing_pct"] = df["gasto_vivienda_usd"] / df["ingreso_mensual_usd"] * 100
housing = (
    df.groupby("pais")["housing_pct"]
    .mean()
    .sort_values(ascending=True)
)
h_colors = [COUNTRY_PALETTE[c] for c in housing.index]

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(housing.index, housing.values, color=h_colors, height=0.5)
for bar, val in zip(bars, housing.values):
    ax.text(val + 0.3, bar.get_y() + bar.get_height() / 2,
            f"{val:.1f}%", va="center", fontsize=10, fontweight="bold")

ax.axvline(30, color="#CC3333", linewidth=1.2, linestyle="--", alpha=0.7,
           label="30% threshold")
ax.set_xlabel("Avg Housing Cost as % of Monthly Income", fontsize=12, labelpad=8)
ax.set_title("Housing Burden by Country\n(avg housing cost as % of income)",
             fontsize=14, fontweight="bold", pad=14)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))
ax.set_xlim(0, housing.max() * 1.2)
ax.legend(fontsize=9, loc="lower right")
ax.grid(axis="x", linestyle="--", alpha=0.4)
ax.spines[["top", "right"]].set_visible(False)
add_source(fig)
fig.tight_layout(rect=[0, 0.04, 1, 1])
fig.savefig("charts/05_housing_burden_by_country.png", dpi=150)
plt.close()
print("Saved charts/05_housing_burden_by_country.png")

print("\nAll 5 charts saved to charts/")
