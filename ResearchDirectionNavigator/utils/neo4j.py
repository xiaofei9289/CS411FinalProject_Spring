import os
from neo4j import GraphDatabase
from dotenv import load_dotenv
from pathlib import Path

_ROOT=Path(__file__).resolve().parent.parent
load_dotenv(_ROOT / ".env")
# connect to Neo4j using credentials from the local .env file.
# never hard-code a password here: .env is gitignored, source code is not.
def get_neo4j_driver():
    uri=os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
    user=os.getenv("NEO4J_USER", "neo4j")
    password=os.getenv("NEO4J_PASSWORD", "")
    if not password:
        raise RuntimeError(
            "NEO4J_PASSWORD is not set. Add it to your local .env file "
            "(see .env.example for the required variables)."
        )
    return GraphDatabase.driver(uri, auth=(user, password))


# W5: count INTERESTED_IN edges from the given faculty nodes to keywords (schema uses FACULTY, INTERESTED_IN, KEYWORD).
def w05_neo4j_interested_in_stats_for_faculty_ids(list_of_faculty_ids_from_mysql):

    if not list_of_faculty_ids_from_mysql:
        return {"edge_count": 0, "detail": "no faculty ids from MySQL"}

    driver=get_neo4j_driver()
    cypher="""
        MATCH (f:FACULTY)-[r:INTERESTED_IN]->(k:KEYWORD)
        WHERE f.id IN $ids
        RETURN count(r) AS cnt
    """
    with driver.session(database="academicworld") as session:
        record=session.run(cypher, ids=list_of_faculty_ids_from_mysql).single()
        cnt=record["cnt"] if record else 0
    driver.close()
    return {"edge_count": cnt}


# W5: rank keywords by how many distinct faculty (from the MySQL-filtered id set) share each keyword via INTERESTED_IN.
def w05_neo4j_keywords_ranked_by_faculty_overlap(neo4j_faculty_ids, cap=500):
    """Rank keywords by overlap count: more faculty in the set interested in a keyword means higher rank."""
    if not neo4j_faculty_ids:
        return []
    driver=get_neo4j_driver()
    cypher="""
        MATCH (f:FACULTY)-[:INTERESTED_IN]->(k:KEYWORD)
        WHERE f.id IN $ids
        WITH k.name AS name, count(DISTINCT f) AS overlap
        WHERE name IS NOT NULL
        RETURN name, overlap
        ORDER BY overlap DESC
        LIMIT $cap
    """
    with driver.session(database="academicworld") as session:
        result=session.run(cypher, ids=neo4j_faculty_ids, cap=cap)
        rows=[
            {"name": r["name"], "overlap": int(r["overlap"])}
            for r in result
            if r.get("name") is not None
        ]
    driver.close()
    return rows


def w06_neo4j_faculty_topic_relevance(neo4j_faculty_ids, topic_text):
    if not neo4j_faculty_ids:
        return {}
    topic=(topic_text or "").strip()
    if not topic:
        return {}
    driver=get_neo4j_driver()
    cypher="""
        MATCH (f:FACULTY)-[:INTERESTED_IN]->(k:KEYWORD)
        WHERE f.id IN $ids
          AND toLower(k.name) CONTAINS toLower($topic)
        RETURN f.id AS faculty_id, count(DISTINCT k) AS graph_relevance
    """
    relevance_by_faculty_id={}
    with driver.session(database="academicworld") as session:
        result=session.run(cypher, ids=neo4j_faculty_ids, topic=topic)
        for record in result:
            faculty_id=str(record["faculty_id"])
            relevance_by_faculty_id[faculty_id]=int(record["graph_relevance"] or 0)
    driver.close()
    return relevance_by_faculty_id


def w07_neo4j_find_faculty_by_name(name_text, limit=5):
    cleaned=(name_text or "").strip()
    if not cleaned:
        return []
    driver=get_neo4j_driver()
    cypher="""
        MATCH (f:FACULTY)
        WHERE toLower(f.name) CONTAINS toLower($name)
        RETURN f.id AS faculty_id, f.name AS faculty_name
        ORDER BY f.name ASC
        LIMIT $limit
    """
    rows=[]
    with driver.session(database="academicworld") as session:
        result=session.run(cypher, name=cleaned, limit=int(limit))
        for record in result:
            rows.append(
                {
                    "faculty_id": record["faculty_id"],
                    "faculty_name": record["faculty_name"],
                }
            )
    driver.close()
    return rows


def w07_neo4j_collaboration_network(name_text, limit=12):
    matches=w07_neo4j_find_faculty_by_name(name_text, limit=1)
    if not matches:
        return {"center": None, "collaborators": []}
    center=matches[0]
    driver=get_neo4j_driver()
    cypher="""
        MATCH (center:FACULTY {id: $faculty_id})-[:PUBLISH]-(p:PUBLICATION)-[:PUBLISH]-(coauthor:FACULTY)
        WHERE coauthor.id <> center.id
        RETURN
            coauthor.id AS faculty_id,
            coauthor.name AS faculty_name,
            count(DISTINCT p) AS shared_publications
        ORDER BY shared_publications DESC, faculty_name ASC
        LIMIT $limit
    """
    collaborators=[]
    with driver.session(database="academicworld") as session:
        result=session.run(cypher, faculty_id=center["faculty_id"], limit=int(limit))
        for record in result:
            collaborators.append(
                {
                    "faculty_id": record["faculty_id"],
                    "faculty_name": record["faculty_name"],
                    "shared_publications": int(record["shared_publications"] or 0),
                }
            )
    driver.close()
    return {"center": center, "collaborators": collaborators}