---
name: publish-finding
description: Publishes one completed finding to the Notion Findings Tracker database and creates a Notion page for it
---

When given a completed finding with: number, title, key statistic,
3-sentence interpretation, and priority (Alta/Media/Baja):

Use the Notion MCP to:

1. Create a new entry in the "Findings Tracker" database with fields:
   - Título
   - Estadística Clave
   - Alcance
   - Prioridad
   - Publicado

2. Create or update a Notion page linked to that entry containing:
   - The 3-sentence interpretation as the page body
   - The key statistic in a callout block at the top
   - A "Próximos pasos" section with the programme recommendation

3. Confirm the Notion URL of the created page.

If Notion MCP is not connected, create a local fallback file in `notion_exports/`
with the same information so the pipeline still has a publishable artifact.