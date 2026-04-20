"""Widget 2 — university dropdown and research profile."""

import mysql.connector

from .core import check_mysql_connection, get_mysql_config

# w02-create a function to get all university's name, this function is for widget 02 dropdown options
def w02_get_all_university_names():
    # first, check if the mysql connection is successful
    if not check_mysql_connection():
        raise ConnectionError("we cannot connect to MySQL database. please check.")
    # after the connection is successful,  query all university names from the university table 
    db_config=mysql.connector.connect(**get_mysql_config())
    cur=db_config.cursor(dictionary=True)
    cur.execute("select name from university order by name")
    results=cur.fetchall()
    cur.close()
    db_config.close()
    return results


# w02-create a function to get the relevent information about the seleced university
def w02_get_all_information_about_selected_university(university_name: str, limit: int=50):
    # first, check if the mysql connection is successful
    if not check_mysql_connection():
        raise ConnectionError("we cannot connect to MySQL database. please check.")
    selected_university_name=(university_name or "").strip()

    if not selected_university_name:
        return []
    # create a query to search for relevant information
    sql="""
        select keyword_name, pub_count
        from university_keyword_stats
        where university_name=%s
        order by pub_count desc
        limit %s
    """
    db_config=mysql.connector.connect(**get_mysql_config())
    cur=db_config.cursor(dictionary=True)
    cur.execute(sql, (selected_university_name, limit))
    results=cur.fetchall()
    cur.close()
    db_config.close()
    return results


def w02_get_university_w2_dashboard(university_name: str, keyword_chart_limit: int=10):
    name=(university_name or "").strip()
    if not name:
        return None
    if not check_mysql_connection():
        raise ConnectionError("we cannot connect to MySQL database. please check.")
    lim=max(1, int(keyword_chart_limit))
    db_config=mysql.connector.connect(**get_mysql_config())
    cur=db_config.cursor(dictionary=True)

    cur.execute(
        """
        select count(distinct f.id) as n
        from faculty f
        join university u on u.id=f.university_id
        where u.name=%s
        """,
        (name,),
    )
    faculty_count=int((cur.fetchone() or {}).get("n") or 0)

    cur.execute(
        """
        select count(distinct fp.publication_id) as n
        from faculty f
        join university u on u.id=f.university_id
        join faculty_publication fp on fp.faculty_id=f.id
        where u.name=%s
        """,
        (name,),
    )
    total_publications=int((cur.fetchone() or {}).get("n") or 0)

    cur.execute(
        """
        select keyword_name, pub_count
        from university_keyword_stats
        where university_name=%s
        order by pub_count desc
        limit %s
        """,
        (name, lim),
    )
    keywords=cur.fetchall() or []
    cur.close()
    db_config.close()

    major=""
    if keywords:
        major=(keywords[0].get("keyword_name") or "").strip()
    if not major:
        major="—"

    return {
        "university_name": name,
        "total_publications": total_publications,
        "faculty_count": faculty_count,
        "major_research_area": major,
        "keywords": keywords,
    }
