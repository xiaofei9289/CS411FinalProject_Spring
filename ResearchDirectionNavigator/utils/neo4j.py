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