"""Widget 5 — research trends (MySQL faculty match by keyword)."""

import mysql.connector

from .core import check_mysql_connection, get_mysql_config

# w05-create a function to get the relevent information about the research trends
def w05_mysql_get_faculty_ids_by_keyword(keyword: str, limit: int=500):
    # first, check if the mysql connection is successful
    if not check_mysql_connection():
        raise ConnectionError("we cannot connect to MySQL database. please check.")
    # check if the keyword is empty, if it is empty, return an empty list
    input_keywords=(keyword or "").strip()
    if not input_keywords:
        return []
    # after the connection is successful, query distinct faculty ids whose papers match the keyword pattern
    sql="""
        select distinct f.id
        from faculty f
        join faculty_publication fp on fp.faculty_id=f.id
        join publication_keyword pk on pk.publication_id=fp.publication_id
        join keyword k on k.id=pk.keyword_id
        where k.name like %s
        limit %s
    """
    pattern="%"+input_keywords+"%"  
    db_config=mysql.connector.connect(**get_mysql_config())
    cur=db_config.cursor()
    cur.execute(sql, (pattern, limit))
    rows=[r[0] for r in cur.fetchall()]
    cur.close()
    db_config.close()
    return rows
