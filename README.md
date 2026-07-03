# Capstone Project — Option B: Data Analyst

## Datos que Hablan: Financial Wellness of Young Professionals in Latin America

This project analyses the **Encuesta de Bienestar Financiero LatAm 2025**, a survey of 500 young professionals across six Latin American countries: México, Colombia, Argentina, Chile, Perú, and Brasil.

The goal is to transform raw survey data into an executive analysis report for Futuro Digital LatAm, supporting the design of a regional financial literacy programme.

## Project Structure

- `data/` — raw and cleaned CSV datasets
- `scripts/` — Python scripts generated and run with Claude Code
- `charts/` — five PNG visualisations
- `.claude/agents/` — custom Claude Code country profiler agent
- `analysis-report.md` — final executive report
- `CLAUDE.md` — project instructions for Claude Code

## Analysis Phases

1. Explore the dataset
2. Clean data quality issues
3. Build a Claude Code country profiler agent
4. Run statistical analysis
5. Generate visualisations
6. Interpret findings
7. Produce executive report

## Key Outputs

- Cleaned dataset: `data/latam_finanzas_clean.csv`
- Final report: `analysis-report.md`
- Visualisations:
  - Income by country
  - Age vs. monthly savings
  - Spending breakdown
  - Financial satisfaction by AI usage
  - Housing burden by country

## Tools Used

- Claude Code
- Python
- pandas
- matplotlib
- seaborn
- scipy
- GitHub
