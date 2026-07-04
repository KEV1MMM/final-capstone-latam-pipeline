import pandas as pd

df = pd.read_csv("data/latam_finanzas_2025.csv")
rows_before = len(df)

issues = []   # (problem, fix, n_affected)

# ── 1. Industria: standardize inconsistent values ─────────────────────────────
print("=" * 60)
print("1. INDUSTRIA — BEFORE CLEANING")
print("=" * 60)
print(df["industria"].value_counts(dropna=False).to_string())

industria_map = {
    "Tecnologia":  "Tecnología",
    "tech":        "Tecnología",
    "TECNOLOGÍA":  "Tecnología",
}
dirty_mask = df["industria"].isin(industria_map)
n_industria = dirty_mask.sum()
df["industria"] = df["industria"].replace(industria_map)

print("\n" + "=" * 60)
print("1. INDUSTRIA — AFTER CLEANING")
print("=" * 60)
print(df["industria"].value_counts(dropna=False).to_string())
issues.append(("industria spelling variants (Tecnologia / tech / TECNOLOGÍA)", "Standardized to 'Tecnología'", n_industria))

# ── 2. Missing values in numeric columns ──────────────────────────────────────
print("\n" + "=" * 60)
print("2. MISSING VALUES IN NUMERIC COLUMNS")
print("=" * 60)
num_cols = df.select_dtypes(include="number").columns
miss = (df[num_cols].isnull().sum() / len(df) * 100).round(2)
miss_cols = miss[miss > 0]

if miss_cols.empty:
    print("  No missing values in numeric columns.")
else:
    print(f"  {'Column':<35} {'% Missing':<12} Recommendation")
    print(f"  {'-'*35} {'-'*12} {'-'*30}")
    for col, pct in miss_cols.items():
        if pct < 10:
            rec = "Fill with median (low % missing, avoids bias from mean)"
        elif pct < 30:
            rec = "Fill with median (moderate missingness)"
        else:
            rec = "Consider dropping rows or dedicated imputation"
        print(f"  {col:<35} {pct:<12} {rec}")

# Apply: fill gasto_salud_usd with median (6.6% missing — safe imputation)
n_salud_missing = df["gasto_salud_usd"].isnull().sum()
median_salud = df["gasto_salud_usd"].median()
df["gasto_salud_usd"] = df["gasto_salud_usd"].fillna(median_salud)
issues.append(
    (f"gasto_salud_usd: {n_salud_missing} missing values (6.6%)",
     f"Filled with median (${median_salud:.2f})",
     n_salud_missing)
)
print(f"\n  Applied: gasto_salud_usd filled with median = ${median_salud:.2f}")

# ── 3. Negative ahorro_mensual_usd → flag column ──────────────────────────────
print("\n" + "=" * 60)
print("3. NEGATIVE ahorro_mensual_usd")
print("=" * 60)
neg_mask = df["ahorro_mensual_usd"] < 0
n_neg = neg_mask.sum()
print(f"  Negative values found: {n_neg} rows ({n_neg/len(df)*100:.1f}%)")
print(f"  Min value: ${df['ahorro_mensual_usd'].min():.2f}")
print(f"  These are valid (spending > income). Flagging with 'ahorro_negativo'.")
df["ahorro_negativo"] = neg_mask
issues.append(
    (f"ahorro_mensual_usd: {n_neg} negative values (spending > income)",
     "Created boolean column 'ahorro_negativo' (no rows removed)",
     n_neg)
)

# ── 4. Save clean dataset ─────────────────────────────────────────────────────
df.to_csv("data/latam_finanzas_clean.csv", index=False)
rows_after = len(df)

# ── 5. Cleaning summary ───────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("5. CLEANING SUMMARY")
print("=" * 60)
print(f"  Rows before cleaning : {rows_before}")
print(f"  Rows after cleaning  : {rows_after}")
print(f"  Columns after cleaning: {df.shape[1]}  (added 'ahorro_negativo')")
print()
print(f"  {'#':<4} {'Problem':<55} {'Fix':<45} {'Rows affected'}")
print(f"  {'-'*4} {'-'*55} {'-'*45} {'-'*13}")
for i, (problem, fix, n) in enumerate(issues, 1):
    print(f"  {i:<4} {problem:<55} {fix:<45} {n}")
print()
print(f"  Output saved to: data/latam_finanzas_clean.csv")
