#!/usr/bin/env python3
"""
CoSci Markdown -> RDF Parser
Phase 1: Minimal semantic pipeline
"""

from datetime import datetime
from pathlib import Path

import frontmatter
from rdflib import DCTERMS, RDF, Graph, Literal, Namespace


# Namespaces
COSCI = Namespace("http://cosci.local/ontology#")
EX = Namespace("http://example.org/cosci/")


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

    kg_dir = Path("knowledge-graph")

    if not kg_dir.exists():
        print("ERROR: knowledge-graph folder not found.")
        return

    graph = Graph()

    graph.bind("cosci", COSCI)
    graph.bind("dcterms", DCTERMS)

    # Ontologie laden
    ontology_file = Path("knowledge-graph/entity-model.ttl")

    if ontology_file.exists():
        graph.parse(str(ontology_file), format="turtle")
        print("Loaded ontology: entity-model.ttl\n")

    processed = 0
    warnings = 0

    for md_file in sorted(kg_dir.glob("*.md")):

        if md_file.name.startswith("_"):
            continue

        try:

            post = frontmatter.load(md_file)

            uri = EX[md_file.stem]

            graph.add((uri, RDF.type, COSCI.KnowledgeDocument))

            # Titel
            title = post.get("title")

            if not title:
                title = md_file.stem
                print(f"WARNING: Missing title -> {md_file.name}")
                warnings += 1

            graph.add((uri, DCTERMS.title, Literal(title)))

            # Level
            level = post.get("level")

            if not level:
                print(f"WARNING: Missing level -> {md_file.name}")
                level = "Interpretativ"
                warnings += 1

            elif level not in VALID_LEVELS:
                print(f"WARNING: Invalid level '{level}' -> {md_file.name}")
                warnings += 1

            graph.add((uri, COSCI.level, Literal(level)))

            # Status
            status = post.get("status")

            if not status:
                print(f"WARNING: Missing status -> {md_file.name}")
                status = "draft"
                warnings += 1

            elif status not in VALID_STATUS:
                print(f"WARNING: Invalid status '{status}' -> {md_file.name}")
                warnings += 1

            graph.add((uri, COSCI.status, Literal(status)))

            # Timestamp
            graph.add((
                uri,
                DCTERMS.created,
                Literal(datetime.now().isoformat())
            ))

            # Content preview
            content = post.content.strip()[:600]

            graph.add((
                uri,
                COSCI.contentPreview,
                Literal(content)
            ))

            print(f"Processed: {md_file.name}")

            processed += 1

        except Exception as e:
            print(f"ERROR processing {md_file.name}: {e}")

    # Output speichern
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "cosci_graph.ttl"

    graph.serialize(
        destination=str(output_file),
        format="turtle"
    )

    print("\nParser finished successfully.")
    print(f"Files processed: {processed}")
    print(f"Warnings: {warnings}")
    print(f"RDF Turtle: {output_file}")
    print(f"Triples: {len(graph)}")


if __name__ == "__main__":
    main()

