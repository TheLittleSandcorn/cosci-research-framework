def main():

    graph = Graph()

    # RDF laden
    graph.parse("output/cosci_graph.ttl", format="turtle")

    print("Loaded RDF graph.\n")

    errors = 0

    # NUR echte Dokumente validieren
    for subject in graph.subjects(RDF.type, COSCI.KnowledgeDocument):

        print(f"Validating: {subject}")

#!/usr/bin/env python3
"""
CoSci Graph Validator - Phase 1

Prüft:
- Existiert level?
- Existiert status?
- Sind level/status gültige Werte?
"""

from pathlib import Path

from rdflib import Graph, Namespace, RDF


# Namespace
COSCI = Namespace("http://cosci.local/ontology#")


# Erlaubte Werte
VALID_LEVELS = {
    "Formal",
    "Implementierbar",
    "Empirisch",
    "Interpretativ",
    "Visionär"
}

VALID_STATUS = {
    "draft",
    "stable",
    "reviewed",
    "deprecated"
}


def main():

    # RDF-Datei prüfen
    ttl_file = Path("output/cosci_graph.ttl")

    if not ttl_file.exists():
        print("ERROR: RDF graph not found.")
        print("Run parser first:")
        print("python3 tools/markdown_to_rdf.py")
        return

    # RDF laden
    graph = Graph()
    graph.parse(str(ttl_file), format="turtle")

    print(f"Loaded RDF graph: {len(graph)} triples\n")

    errors = 0
    validated_docs = 0

    # Nur echte Dokumente validieren
    for doc in graph.subjects(RDF.type, COSCI.KnowledgeDocument):

        validated_docs += 1

        print(f"Validating: {doc}")

        level = graph.value(doc, COSCI.level)
        status = graph.value(doc, COSCI.status)

        # level prüfen
        if level is None:
            print(f"ERROR: Missing level -> {doc}")
            errors += 1

        else:
            level_str = str(level)

            if level_str not in VALID_LEVELS:
                print(f"ERROR: Invalid level '{level_str}' -> {doc}")
                errors += 1

        # status prüfen
        if status is None:
            print(f"ERROR: Missing status -> {doc}")
            errors += 1

        else:
            status_str = str(status)

            if status_str not in VALID_STATUS:
                print(f"ERROR: Invalid status '{status_str}' -> {doc}")
                errors += 1

    # Zusammenfassung
    print("\nValidation finished.")
    print(f"Documents checked: {validated_docs}")

    if errors == 0:
        print("No validation errors found.")
    else:
        print(f"Validation errors: {errors}")


if __name__ == "__main__":
    main()
