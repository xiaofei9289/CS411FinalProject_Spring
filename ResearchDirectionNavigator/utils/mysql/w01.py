import mysql.connector

from .connection_config import get_mysql_config
from utils.common import split_keywords_by_comma

# W1 search papers by keyword
def w01_search_papers_based_on_keywords(keywords, limit=100):
    # if no input, return empty
    input_text=(keywords or "").strip()
    if not input_text:
        return []
    # if the input text is not empty, we can split the keywords by comma and strip the whitespace
    keyword_list=split_keywords_by_comma(input_text)
    if not keyword_list:
        return []

    # use first token only
    first_keyword=keyword_list[0]
    sql_query="""
            select
                p.id,
                p.title,
                p.year,
                p.num_citations,
                p.venue,
                group_concat(distinct f.id order by f.id separator '||') as faculty_ids,
                group_concat(distinct f.name order by f.id separator '||') as faculty_names
            from publication p
            join publication_keyword pk on pk.publication_id=p.id
            join keyword k on pk.keyword_id=k.id
            left join faculty_publication fp on fp.publication_id=p.id
            left join faculty f on f.id=fp.faculty_id
            where k.name like %s
            group by p.id, p.title, p.year, p.num_citations, p.venue
            order by p.num_citations desc
            limit %s
    """
    pattern="%"+first_keyword+"%"
    db_config=mysql.connector.connect(**get_mysql_config())
    cur=db_config.cursor(dictionary=True)
    cur.execute(sql_query, (pattern, limit))
    results=cur.fetchall()
    cur.close()
    db_config.close()
    return results
