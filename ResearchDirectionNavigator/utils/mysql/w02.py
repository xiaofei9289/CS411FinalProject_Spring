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

# define a function to get the main data for one university
def w02_get_university_w2_dashboard(university_name: str, keyword_limit: int=10):
    # clean the input university name first
    clean_university_name = (university_name or "").strip()
    # if the university name is empty
    if clean_university_name == "":
        return None
    # check whether MySQL is available before running queries
    if not check_mysql_connection():
        raise ConnectionError("we cannot connect to MySQL database. please check.")

    # make sure the keyword limit is at least 1
    safe_keyword_limit = max(1, int(keyword_limit))
    # connect to MySQL
    mysql_connection = mysql.connector.connect(**get_mysql_config())
    # use dictionary=True so each row can be read by column name
    mysql_cursor = mysql_connection.cursor(dictionary=True)

    # query 1: count how many faculty members are in this university
    mysql_cursor.execute(
        """
        select count(distinct f.id) as faculty_count
        from faculty f
        join university u on u.id = f.university_id
        where u.name = %s
        """,
        (clean_university_name,),
    )
    faculty_result = mysql_cursor.fetchone() or {}
    total_faculty_count = int(faculty_result.get("faculty_count") or 0)


    # query 2: count how many publications belong to this university
    mysql_cursor.execute(
        """
        select count(distinct fp.publication_id) as publication_count
        from faculty f
        join university u on u.id = f.university_id
        join faculty_publication fp on fp.faculty_id = f.id
        where u.name = %s
        """,
        (clean_university_name,),
    )
    publication_result = mysql_cursor.fetchone() or {}
    total_publication_count = int(publication_result.get("publication_count") or 0)

    # query 3: get top keywords for this university
    mysql_cursor.execute(
        """
        select keyword_name, pub_count
        from university_keyword_stats
        where university_name = %s
        order by pub_count desc
        limit %s
        """,
        (clean_university_name, safe_keyword_limit),
    )
    top_keyword_rows = mysql_cursor.fetchall() or []
    # close cursor and connection after all queries are finished
    mysql_cursor.close()
    mysql_connection.close()

    # use the first keyword as the main research area
    main_research_area = "—"

    if len(top_keyword_rows) > 0:
        first_keyword_name = (top_keyword_rows[0].get("keyword_name") or "").strip()
        if first_keyword_name != "":
            main_research_area = first_keyword_name

    # return all data in one dictionary
    dashboard_data = {
        "university_name": clean_university_name,
        "total_publications": total_publication_count,
        "faculty_count": total_faculty_count,
        "major_research_area": main_research_area,
        "keywords": top_keyword_rows,
    }
    return dashboard_data