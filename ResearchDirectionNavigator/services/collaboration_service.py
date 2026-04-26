from utils.neo4j import w07_neo4j_collaboration_network


def get_widget07_collaboration_network(faculty_name):
    return w07_neo4j_collaboration_network(faculty_name, limit=12)


def neo4j_faculty_id_to_mysql_id(neo4j_faculty_id):
    cleaned=str(neo4j_faculty_id or "").strip()
    if cleaned.startswith("f"):
        cleaned=cleaned[1:]
    if cleaned.isdigit():
        return int(cleaned)
    return None
