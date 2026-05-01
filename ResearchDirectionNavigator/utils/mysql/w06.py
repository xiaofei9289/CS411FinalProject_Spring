import mysql.connector

from .core import get_mysql_config
from utils.common import pick_first_keyword


def w06_get_faculty_candidates_by_topic(topic_text, limit=50):
    first_topic=pick_first_keyword(topic_text)
    if not first_topic:
        return []
    sql="""
        select
            f.id as faculty_id,
            f.name as faculty_name,
            u.name as university_name,
            count(distinct case when p.year>=2016 then p.id end) as recent_publication_count,
            sum(pk.score * p.num_citations) as keyword_relevant_citations
        from faculty f
        join university u on u.id=f.university_id
        join faculty_publication fp on fp.faculty_id=f.id
        join publication p on p.id=fp.publication_id
        join publication_keyword pk on pk.publication_id=p.id
        join keyword k on k.id=pk.keyword_id
        where k.name=%s
        group by f.id, f.name, u.name
        order by keyword_relevant_citations desc, recent_publication_count desc
        limit %s
    """
    db_config=mysql.connector.connect(**get_mysql_config())
    cur=db_config.cursor(dictionary=True)
    cur.execute(sql, (first_topic, int(limit)))
    rows=cur.fetchall()
    cur.close()
    db_config.close()
    return rows
