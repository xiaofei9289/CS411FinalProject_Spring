import mysql.connector

from .core import check_mysql_connection, get_mysql_config

# w01-create a function to search for papers based on paper keywords
def w01_search_papers_based_on_keywords(keywords: str, limit: int=100):  
    # first, check if the mysql connection is successful
    if not check_mysql_connection():
        raise ConnectionError("we cannot connect to MySQL database. please check.")
    # after the connection is successful, we can execute the query to search for papers based on keywords
    # check if the keywords is empty, if it is empty, return an empty list
    input_text=(keywords or "").strip()
    if not input_text:
        return []
    # if the input text is not empty, we can split the keywords by comma and strip the whitespace
    keyword_list=[keyword.strip() for keyword in input_text.split(",") if keyword.strip()]
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
