# CLAUDE.md

## Project
Capstone Project — Option B: Data Analyst  
Title: Datos que Hablan: Bienestar Financiero de Jóvenes Profesionales en América Latina

## Goal
Use Claude Code to transform the raw survey dataset into an executive report for Futuro Digital LatAm. The analysis should help the organization design its next financial literacy programme.

## Dataset
Raw dataset:
data/latam_finanzas_2025.csv

Clean dataset:
data/latam_finanzas_clean.csv

The dataset contains 500 young professionals from six countries:
México, Colombia, Argentina, Chile, Perú, Brasil.

## Python Environment
Use Python 3 with:
- pandas
- matplotlib
- seaborn
- scipy

## Folder Structure
- scripts/ → all Python scripts
- charts/ → all PNG visualisations
- data/ → raw and cleaned CSV files
- .claude/agents/ → Claude Code agent definitions

## Naming Conventions
Scripts:
- scripts/01_explore.py
- scripts/02_clean.py
- scripts/03_analyse.py
- scripts/04_visualise.py

Charts:
- charts/01_income_by_country.png
- charts/02_age_vs_savings.png
- charts/03_spending_breakdown.png
- charts/04_satisfaction_by_ai_usage.png
- charts/05_housing_burden_by_country.png

Final report:
analysis-report.md

## Important Instructions
Write the final report in English.
Use clear, professional language.
Every chart must have a title, axis labels, and a source note.
Keep a clear Git commit history after each phase.