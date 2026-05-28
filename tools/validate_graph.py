#!/usr/bin/env python3

"""
CoSci — RDF Graph Validator
Minimal, logisch, diszipliniert.

Zweck:
- Validiert nur echte KnowledgeDocument-Instanzen
- Prüft Pflichtfelder
- Vermeidet Ontologie-/Schema-Drift
"""

from rdflib import Graph, Namespace, RDF

# Namespaces
COSCI = Namespace("http://cosci.local/ontology#")

# Pflichtfelder
REQUIRED_FIELDS = [
    COSCI.level,
    COSCI.status,
    COSCI.contentPreview,
]

def main():

    graph = Graph()

    # RDF laden
    graph.parse("output/cosci_graph.ttl", format="turtle")

    print("Loaded RDF graph.\n")

    errors = 0

    # NUR echte Dokumente validieren
    for subject in graph.subjects(RDF.type, COSCI.KnowledgeDocument):

        print(f"Validating: {subject}")

        for field in REQUIRED_FIELDS:

            if not list(graph.objects(subject, field)):

                field_name = field.split("#")[-1]

                print(f"ERROR: Missing {field_name} -> {subject}")

                errors += 1

    print("\nValidation finished.")

    if errors == 0:
        print("No validation errors found.")
    else:
        print(f"Validation errors: {errors}")

if __name__ == "__main__":
    main()

