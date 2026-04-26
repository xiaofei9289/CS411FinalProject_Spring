from utils.mongodb import w05_get_research_trends_based_on_publication_numbers_with_year
from utils.mysql import w06_get_faculty_candidates_by_topic
from utils.neo4j import w06_neo4j_faculty_topic_relevance


def run_widget06_recommendation(
    topic_text,
    graph_weight,
    recent_weight,
    citation_weight,
):
    selected_keyword=(topic_text or "").split(",")[0].strip()
    if not selected_keyword:
        return {
            "topic": "",
            "topic_activity_total": 0,
            "rows": [],
            "message": "Type a research topic and click Recommend.",
        }
    mysql_rows=w06_get_faculty_candidates_by_topic(selected_keyword, limit=50)
    if not mysql_rows:
        return {
            "topic": selected_keyword,
            "topic_activity_total": 0,
            "rows": [],
            "message": "No faculty matched this topic in MySQL.",
        }
    neo4j_ids=[f"f{int(row['faculty_id'])}" for row in mysql_rows]
    graph_relevance_by_id=w06_neo4j_faculty_topic_relevance(neo4j_ids, selected_keyword)
    topic_activity_total=get_topic_activity_total(selected_keyword)
    scored_rows=score_faculty_rows(
        mysql_rows,
        graph_relevance_by_id,
        graph_weight,
        recent_weight,
        citation_weight,
    )
    return {
        "topic": selected_keyword,
        "topic_activity_total": topic_activity_total,
        "rows": scored_rows[:15],
        "message": "",
    }


def get_topic_activity_total(topic_text):
    trend_rows=w05_get_research_trends_based_on_publication_numbers_with_year(topic_text, limit=100)
    total=0
    for row in trend_rows:
        total+=int(row.get("pub_count") or 0)
    return total


def score_faculty_rows(
    mysql_rows,
    graph_relevance_by_id,
    graph_weight,
    recent_weight,
    citation_weight,
):
    graph_weight=float(graph_weight)
    citation_weight=float(citation_weight)
    recent_weight=float(recent_weight)
    total_weight=graph_weight+recent_weight+citation_weight
    if total_weight <= 0:
        total_weight=1.0
    graph_weight/=total_weight
    recent_weight/=total_weight
    citation_weight/=total_weight

    max_graph=max(
        [int(graph_relevance_by_id.get(f"f{int(row['faculty_id'])}", 0)) for row in mysql_rows] or [1]
    )
    max_recent=max([int(row.get("recent_publication_count") or 0) for row in mysql_rows] or [1])
    max_relevant_citations=max(
        [float(row.get("keyword_relevant_citations") or 0) for row in mysql_rows] or [1]
    )
    max_graph=max(max_graph, 1)
    max_recent=max(max_recent, 1)
    max_relevant_citations=max(max_relevant_citations, 1)

    scored_rows=[]
    for row in mysql_rows:
        faculty_id=int(row["faculty_id"])
        neo4j_id=f"f{faculty_id}"
        graph_relevance=int(graph_relevance_by_id.get(neo4j_id, 0))
        recent_count=int(row.get("recent_publication_count") or 0)
        keyword_relevant_citations=float(row.get("keyword_relevant_citations") or 0)
        graph_score=graph_relevance/max_graph
        recent_score=recent_count/max_recent
        citation_score=keyword_relevant_citations/max_relevant_citations
        final_score=(
            graph_weight*graph_score
            + citation_weight*citation_score
            + recent_weight*recent_score
        )
        scored_rows.append(
            {
                "faculty_id": faculty_id,
                "faculty_name": row.get("faculty_name") or f"Faculty {faculty_id}",
                "university_name": row.get("university_name") or "",
                "graph_relevance": graph_relevance,
                "recent_publication_count": recent_count,
                "keyword_relevant_citations": round(keyword_relevant_citations, 2),
                "score": round(final_score*100, 1),
            }
        )
    scored_rows.sort(key=lambda item: item["score"], reverse=True)
    return scored_rows
