#!/usr/bin/env python3

"""
CoSci — Markdown to RDF Parser
Minimal, functional, disciplined.
"""

from datetime import datetime
from pathlib import Path

import frontmatter
from rdflib import DCTERMS, RDF, Graph, Literal, Namespace

COSCI = Namespace("http://cosci.local/ontology#")
EX = Namespace("http://example.org/cosci/")


def main():

    kg_dir = Path("knowledge-graph")

    if not kg_dir.exists():
        print("ERROR: folder 'knowledge-graph' not found.")
        return

    graph = Graph()

    # Load ontology model
    graph.parse("knowledge-graph/entity-model.ttl", format="turtle")

    print("Loaded ontology: entity-model.ttl")

    graph.bind("cosci", COSCI)
    graph.bind("dcterms", DCTERMS)

    count = 0

    for md_file in sorted(kg_dir.glob("*.md")):

        if md_file.name.startswith("_"):
            continue

        try:

            post = frontmatter.load(md_file)

            uri = EX[md_file.stem]

            graph.add((uri, RDF.type, COSCI.KnowledgeDocument))

            graph.add((
                uri,
                DCTERMS.title,
                Literal(post.get("title", md_file.stem))
            ))

            graph.add((
                uri,
                COSCI.level,
                Literal(post.get("level", "Interpretativ"))
            ))

            graph.add((
                uri,
                COSCI.status,
                Literal(post.get("status", "draft"))
            ))

            graph.add((
                uri,
                DCTERMS.created,
                Literal(datetime.now().isoformat())
            ))

            content = post.content.strip()[:600]

            graph.add((
                uri,
                COSCI.contentPreview,
                Literal(content)
            ))

            print(f"Processed: {md_file.name}")

            count += 1

        except Exception as e:

            print(f"ERROR in {md_file.name}: {e}")

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "cosci_graph.ttl"

    graph.serialize(
        destination=str(output_file),
        format="turtle"
    )

    print("\nParser finished successfully.")
    print(f"Files processed: {count}")
    print(f"RDF Turtle: {output_file}")
    print(f"Triples: {len(graph)}")


if __name__ == "__main__":
    main()

