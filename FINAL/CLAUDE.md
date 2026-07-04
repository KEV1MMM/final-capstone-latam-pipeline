# Pipeline: Análisis LatAm 2025

## Project

Repeatable financial wellness analysis pipeline for Futuro Digital LatAm.

This project builds on the Midterm II Option B analysis and turns it into an automated pipeline using Claude Code Hooks, Skills, a Country Profiler Agent, and Notion MCP publishing.

Dataset:
- Raw: `data/latam_finanzas_2025.csv`
- Clean: `data/latam_finanzas_clean.csv`

Final report:
- `analysis-report.md`

## Goal

Build a repeatable analysis system that can be reused every year. The pipeline should:

1. Validate expected outputs automatically using hooks.
2. Log commands and analysis steps in `session-log.md`.
3. Generate consistent policy-facing interpretations using skills.
4. Publish findings and the final report to Notion using MCP.
5. Preserve all Python scripts, charts, agent definitions, skills, hooks, and report outputs in GitHub.

## Python Environment

Use Python 3 with:

- pandas
- matplotlib
- seaborn
- scipy

Scripts go in:
- `scripts/`

Charts go in:
- `charts/`

## Naming Conventions

Scripts:
- `scripts/01_explore.py`
- `scripts/02_clean.py`
- `scripts/03_analyse.py`
- `scripts/04_visualise.py`

Charts:
- `charts/01_income_by_country.png`
- `charts/02_age_vs_savings.png`
- `charts/03_spending_breakdown.png`
- `charts/04_satisfaction_by_ai_usage.png`
- `charts/05_housing_burden_by_country.png`

Country scripts:
- `scripts/country_México.py`
- `scripts/country_Colombia.py`
- `scripts/country_Argentina.py`
- `scripts/country_Chile.py`
- `scripts/country_Perú.py`
- `scripts/country_Brasil.py`

## Pipeline Components

### Hooks

Configured in `.claude/settings.json`:

1. Chart counter hook
   - Counts PNG files in `charts/`
   - Prints progress toward 5 charts

2. Script logger hook
   - Logs Claude Code command activity to `session-log.md`

3. Phase validator hook
   - Runs `.claude/hooks/validate-phases.sh`
   - Checks whether expected outputs exist

### Skills

Stored in `.claude/skills/`:

1. `/interpret`
   - Produces 3-sentence Spanish interpretations for findings
   - Format: fact, implication, recommendation

2. `/publish-finding`
   - Publishes or prepares each finding for Notion
   - Uses a local fallback if Notion MCP is not available

### Agent

Stored in `.claude/agents/`:

- `country-profiler`
- Generates country-level statistical profiles for the six countries

## Notion Workspace

Workspace:
- `Análisis LatAm 2025`

Required Notion items:

1. `Findings Tracker`
   - Título
   - Estadística Clave
   - Alcance
   - Prioridad
   - Publicado

2. `Country Profiles`
   - País
   - Muestra
   - Ingreso Mediano
   - Carga Vivienda

3. `Informe Ejecutivo`
   - Final report page

Push each finding after Phase 3.
Push the final report after Phase 6.

## Final Presentation

At the end, create a 5-minute PowerPoint presentation:

- Slide 1: title, name, class, project
- Slides 2–6: five takeaways from Midterm II and Final Capstone