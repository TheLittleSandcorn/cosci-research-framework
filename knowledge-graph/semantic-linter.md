---
title: Semantic Linter
level: Implementierbar
status: draft
---

# Semantic Linter

## Zweck

Definition maschinenprüfbarer Regeln zur Erkennung semantischer
Inkonsistenzen und semantischer Inflation.

Der Semantic Linter ergänzt:
- semantic-boundaries.md
- semantic-validation.md
- entity-model.ttl

---

# Kernprinzip

Semantische Aussagen sollen:
- explizit
- kategorisiert
- überprüfbar
- reproduzierbar

sein.

---

# Linter-Regeln

## Regel 1 — Pflicht-Frontmatter

Jede Datei im knowledge-graph benötigt:

```yaml
title:
level:
status:

