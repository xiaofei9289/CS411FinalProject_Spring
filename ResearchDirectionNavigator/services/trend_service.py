from dash import html

from components.widget05 import create_line_chart_for_w05_research_trend, build_w05_panel
from services.search_service import keyword_search_decision_in_diverse_areas
from utils.mongodb import (
    w05_get_research_trends_by_keyword_name_set,
    w05_get_research_trends_based_on_publication_numbers_with_year,
)
from utils.mysql import w05_mysql_get_faculty_ids_by_keyword
from utils.neo4j import w05_neo4j_keywords_ranked_by_faculty_overlap

# define a function to build the initial message for Widget 5
def widget05_initial_results_children():
    return html.P(
        "After search: (1) bar chart of top overlapping keywords; (2) MongoDB publications per year.",
        className="text-muted small",
    )

# define a function to run the search for Widget 5
def run_widget05_search(global_text, local_text):
    selected_text=keyword_search_decision_in_diverse_areas(global_text, local_text)
    # if no keyword is given
    if not selected_text:
        return widget05_initial_results_children()
    # get faculty ids from MySQL
    faculty_ids_from_mysql=w05_mysql_get_faculty_ids_by_keyword(selected_text, limit=500)
    # change MySQL faculty ids into the Neo4j id format
    neo4j_faculty_ids=[f"f{int(x)}" for x in faculty_ids_from_mysql]

    max_year_buckets=100
    # get overlapping keywords from Neo4j
    ranked_neo4j_kw=w05_neo4j_keywords_ranked_by_faculty_overlap(neo4j_faculty_ids, cap=500)
    # collect keyword names for MongoDB trend search
    keyword_set_k=[r["name"] for r in ranked_neo4j_kw]
    list_of_year_and_count=w05_get_research_trends_by_keyword_name_set(
        keyword_set_k,
        limit=max_year_buckets,
    )
    line_chart_data_from_neo4j_keywords=bool(list_of_year_and_count)
    # if no trend data is found, fall back to the original input keyword
    if not list_of_year_and_count:
        list_of_year_and_count=w05_get_research_trends_based_on_publication_numbers_with_year(
            selected_text,
            limit=max_year_buckets,
        )
    # build the MongoDB line chart
    mongo_chart_div=create_line_chart_for_w05_research_trend(
        list_of_year_and_count,
        keyword_label=selected_text.strip(),
        use_neo4j_keywords=line_chart_data_from_neo4j_keywords,
    )

    return build_w05_panel(
        len(faculty_ids_from_mysql),
        ranked_neo4j_kw,
        mongo_chart_div,
        mongo_uses_neo4j_keywords=line_chart_data_from_neo4j_keywords,
    )
