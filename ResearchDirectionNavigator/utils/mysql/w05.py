import mysql.connector

from .core import get_mysql_config

# W5 faculty ids by keyword
def w05_mysql_get_faculty_ids_by_keyword(keyword, limit=500):
    input_keywords=(keyword or "").strip()
    if not input_keywords:
        return []
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
