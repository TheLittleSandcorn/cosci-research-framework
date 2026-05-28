#!/usr/bin/env python3
"""
CoSci Graph Validator - Phase 2 Minimal

Prüft:
- RDF-Datei existiert
- KnowledgeDocument-Instanzen existieren
- level ist vorhanden
- status ist vorhanden
- level hat erlaubten Wert
- status hat erlaubten Wert
- Visionär wird als Warnung markiert
"""

from pathlib import Path

from rdflib import Graph, Namespace, RDF


COSCI = Namespace("http://cosci.local/ontology#")

VALID_LEVELS = {
    "Formal",
    "Implementierbar",
    "Empirisch",
    "Interpretativ",
    "Visionär",
}

VALID_STATUS = {
    "draft",
    "stable",
    "reviewed",
    "deprecated",
}


def main():
    ttl_file = Path("output/cosci_graph.ttl")

    if not ttl_file.exists():
        print("ERROR: RDF graph not found. Run parser first.")
        return 1

    graph = Graph()
    graph.parse(str(ttl_file), format="turtle")

    print(f"Loaded RDF graph: {len(graph)} triples\n")

    errors = 0
    warnings = 0
    validated_docs = 0

    for doc in graph.subjects(RDF.type, COSCI.KnowledgeDocument):
        validated_docs += 1

        print(f"Validating: {doc}")

        level = graph.value(doc, COSCI.level)
        status = graph.value(doc, COSCI.status)

        if level is None:
            print(f"ERROR: Missing level -> {doc}")
            errors += 1
        else:
            level_str = str(level)

            if level_str not in VALID_LEVELS:
                print(f"ERROR: Invalid level '{level_str}' -> {doc}")
                errors += 1

            if level_str == "Visionär":
                print(f"WARNING: Visionär level used -> {doc}")
                warnings += 1

        if status is None:
            print(f"ERROR: Missing status -> {doc}")
            errors += 1
        else:
            status_str = str(status)

            if status_str not in VALID_STATUS:
                print(f"ERROR: Invalid status '{status_str}' -> {doc}")
                errors += 1

    if validated_docs == 0:
        print("ERROR: No KnowledgeDocument instances found.")
        errors += 1

    print("\n=== Validation Summary ===")
    print(f"Documents checked: {validated_docs}")
    print(f"Warnings: {warnings}")
    print(f"Errors: {errors}")

    if errors == 0:
        print("Pipeline valid.")
        return 0

    print("Pipeline invalid.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

