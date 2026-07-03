import pandas as pd

df = pd.read_csv("data/latam_finanzas_2025.csv")

# 1. Shape
print("=" * 60)
print("1. SHAPE")
print("=" * 60)
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

# 2. Columns and dtypes
print("\n" + "=" * 60)
print("2. COLUMNS AND DATA TYPES")
print("=" * 60)
for col, dtype in df.dtypes.items():
    print(f"  {col:<35} {dtype}")

# 3. Missing values (sorted most to least)
print("\n" + "=" * 60)
print("3. MISSING VALUES (sorted most to least)")
print("=" * 60)
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df = pd.DataFrame({"missing_count": missing, "missing_pct": missing_pct})
missing_df = missing_df[missing_df["missing_count"] > 0].sort_values("missing_count", ascending=False)
if missing_df.empty:
    print("  No missing values found.")
else:
    print(missing_df.to_string())

# 4. Basic statistics for numeric columns
print("\n" + "=" * 60)
print("4. NUMERIC COLUMN STATISTICS")
print("=" * 60)
numeric_cols = df.select_dtypes(include="number").columns
stats = df[numeric_cols].agg(["min", "max", "mean", "median", "std"]).T
stats.columns = ["min", "max", "mean", "median", "std"]
print(stats.round(2).to_string())

# 5. Categorical value counts
print("\n" + "=" * 60)
print("5. CATEGORICAL VALUE COUNTS")
print("=" * 60)
cat_cols = [
    "pais", "industria", "ocupacion", "meta_financiera",
    "tiene_tarjeta_credito", "tiene_cuenta_ahorro", "tiene_deuda",
]
for col in cat_cols:
    if col not in df.columns:
        print(f"\n  [WARNING] Column '{col}' not found in dataset.")
        continue
    counts = df[col].value_counts(dropna=False)
    print(f"\n  {col} ({counts.shape[0]} unique values):")
    for val, cnt in counts.items():
        pct = cnt / len(df) * 100
        print(f"    {str(val):<40} {cnt:>4}  ({pct:.1f}%)")
