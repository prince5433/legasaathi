"""Knowledge graph routes — serve Neo4j data as nodes + edges for ReactFlow."""

from __future__ import annotations

import logging
from fastapi import APIRouter, Depends, HTTPException
from middleware.auth import verify_clerk
from services.neo4j_service import get_driver

log = logging.getLogger("legalsaathi.graph")
router = APIRouter()


@router.get("/{doc_id}")
async def get_document_graph(doc_id: str, user_id: str = Depends(verify_clerk)):
    """Return all nodes and edges connected to a document for graph visualization."""
    driver = get_driver()

    try:
        async with driver.session() as session:
            # Get all nodes and relationships connected to this document
            result = await session.run(
                """
                MATCH (d:Document {id: $doc_id})
                OPTIONAL MATCH (d)-[r]-(n)
                OPTIONAL MATCH (n)-[r2]-(m)
                WHERE m.id <> $doc_id AND m <> d
                RETURN
                    d.id AS doc_id, d.type AS doc_type,
                    type(r) AS rel_type, labels(n)[0] AS node_label,
                    coalesce(n.name, n.id) AS node_name,
                    type(r2) AS rel2_type, labels(m)[0] AS m_label,
                    coalesce(m.name, m.id) AS m_name,
                    id(n) AS node_neo4j_id, id(m) AS m_neo4j_id
                """,
                doc_id=doc_id,
            )
            rows = [rec.data() async for rec in result]

            # Also get connection counts for sizing nodes
            count_result = await session.run(
                """
                MATCH (d:Document {id: $doc_id})-[]-(n)
                OPTIONAL MATCH (n)-[r]-()
                RETURN coalesce(n.name, n.id) AS name, labels(n)[0] AS label,
                       count(r) AS connections
                """,
                doc_id=doc_id,
            )
            counts = {rec.data()["name"]: rec.data()["connections"]
                      async for rec in count_result}

    except Exception as e:
        log.exception("Failed to query Neo4j graph for doc %s", doc_id)
        raise HTTPException(500, f"Graph query failed: {e}")

    # Build unique nodes and edges
    nodes = {}
    edges = []

    if not rows:
        # Return just the document node if no relationships exist
        return {
            "nodes": [{"id": f"doc_{doc_id}", "type": "document", "label": doc_id[:12] + "…", "connections": 0}],
            "edges": [],
        }

    # Add the document node
    doc_node_id = f"doc_{doc_id}"
    doc_type = rows[0].get("doc_type") or "document"
    nodes[doc_node_id] = {
        "id": doc_node_id,
        "type": "document",
        "label": f"{doc_type.upper()} Document",
        "connections": len([r for r in rows if r.get("node_name")]),
    }

    seen_edges = set()

    for row in rows:
        # First-degree nodes (connected to document)
        if row.get("node_name"):
            node_label = row["node_label"]  # "Person" or "Section"
            node_name = row["node_name"]
            node_id = f"{node_label.lower()}_{node_name}"

            if node_id not in nodes:
                nodes[node_id] = {
                    "id": node_id,
                    "type": node_label.lower(),  # "person" or "section"
                    "label": node_name,
                    "connections": counts.get(node_name, 1),
                }

            edge_key = f"{doc_node_id}-{row['rel_type']}-{node_id}"
            if edge_key not in seen_edges:
                edges.append({
                    "source": doc_node_id,
                    "target": node_id,
                    "label": row["rel_type"],
                })
                seen_edges.add(edge_key)

        # Second-degree nodes (connected to first-degree nodes)
        if row.get("m_name") and row.get("node_name"):
            m_label = row["m_label"]
            m_name = row["m_name"]
            m_id = f"{m_label.lower()}_{m_name}"
            source_id = f"{row['node_label'].lower()}_{row['node_name']}"

            if m_id not in nodes:
                nodes[m_id] = {
                    "id": m_id,
                    "type": m_label.lower(),
                    "label": m_name,
                    "connections": counts.get(m_name, 1),
                }

            edge_key = f"{source_id}-{row['rel2_type']}-{m_id}"
            if edge_key not in seen_edges:
                edges.append({
                    "source": source_id,
                    "target": m_id,
                    "label": row["rel2_type"],
                })
                seen_edges.add(edge_key)

    return {
        "nodes": list(nodes.values()),
        "edges": edges,
    }


@router.get("/user/all")
async def get_user_graph(user_id: str = Depends(verify_clerk)):
    """Return the full knowledge graph across all user documents."""
    driver = get_driver()

    try:
        async with driver.session() as session:
            result = await session.run(
                """
                MATCH (d:Document)-[r]-(n)
                OPTIONAL MATCH (n)-[r2]-(m:Document)
                WHERE m <> d
                RETURN
                    d.id AS doc_id, d.type AS doc_type,
                    type(r) AS rel_type, labels(n)[0] AS node_label,
                    coalesce(n.name, n.id) AS node_name,
                    m.id AS connected_doc_id, m.type AS connected_doc_type
                LIMIT 200
                """,
            )
            rows = [rec.data() async for rec in result]
    except Exception as e:
        log.exception("Failed to query full user graph")
        raise HTTPException(500, f"Graph query failed: {e}")

    nodes = {}
    edges = []
    seen_edges = set()

    for row in rows:
        # Document nodes
        doc_id = row["doc_id"]
        doc_node_id = f"doc_{doc_id}"
        if doc_node_id not in nodes:
            nodes[doc_node_id] = {
                "id": doc_node_id,
                "type": "document",
                "label": f"{(row.get('doc_type') or 'doc').upper()} {doc_id[:8]}…",
                "connections": 0,
            }
        nodes[doc_node_id]["connections"] += 1

        # Entity nodes
        if row.get("node_name"):
            node_id = f"{row['node_label'].lower()}_{row['node_name']}"
            if node_id not in nodes:
                nodes[node_id] = {
                    "id": node_id,
                    "type": row["node_label"].lower(),
                    "label": row["node_name"],
                    "connections": 0,
                }
            nodes[node_id]["connections"] += 1

            edge_key = f"{doc_node_id}-{row['rel_type']}-{node_id}"
            if edge_key not in seen_edges:
                edges.append({
                    "source": doc_node_id,
                    "target": node_id,
                    "label": row["rel_type"],
                })
                seen_edges.add(edge_key)

    return {
        "nodes": list(nodes.values()),
        "edges": edges,
    }
