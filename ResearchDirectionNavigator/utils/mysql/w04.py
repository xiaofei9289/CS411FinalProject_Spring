"""Widget 4 — faculty profile / off-canvas."""

import mysql.connector

from .core import check_mysql_connection, get_mysql_config

# w04-create a function to get summary statistics for one faculty (name, university, publication and citation counts)
def w04_get_faculty_profile_stats(faculty_id: int):
    # first, check if the mysql connection is successful
    if not check_mysql_connection():
        raise ConnectionError("we cannot connect to MySQL database. please check.")
    # after the connection is successful, run the aggregation query for this faculty
    fid=int(faculty_id)
    sql="""
        select
            f.name as faculty_name,
            u.name as university_name,
            count(distinct fp.publication_id) as publication_count,
            coalesce(sum(p.num_citations), 0) as total_citations
        from faculty f
        join university u on u.id=f.university_id
        left join faculty_publication fp on fp.faculty_id=f.id
        left join publication p on p.id=fp.publication_id
        where f.id=%s
        group by f.id, f.name, u.name
    """
    db_config=mysql.connector.connect(**get_mysql_config())
    cur=db_config.cursor(dictionary=True)
    cur.execute(sql, (fid,))
    row=cur.fetchone()
    cur.close()
    db_config.close()
    return row


# w04-create a function to get keyword counts on this faculty's papers, ordered by frequency
def w04_get_faculty_top_keywords(faculty_id: int, limit: int=15):
    # first, check if the mysql connection is successful
    if not check_mysql_connection():
        raise ConnectionError("we cannot connect to MySQL database. please check.")
    # after the connection is successful, query top keywords
    fid=int(faculty_id)
    lim=max(1, int(limit))
    sql="""
        select k.name as keyword_name, count(*) as kw_count
        from faculty_publication fp
        join publication_keyword pk on pk.publication_id=fp.publication_id
        join keyword k on k.id=pk.keyword_id
        where fp.faculty_id=%s
        group by k.id, k.name
        order by kw_count desc, k.name asc
        limit %s
    """
    db_config=mysql.connector.connect(**get_mysql_config())
    cur=db_config.cursor(dictionary=True)
    cur.execute(sql, (fid, lim))
    rows=cur.fetchall()
    cur.close()
    db_config.close()
    return rows


# w04-create a function to get co-authors on shared papers, ordered by number of shared papers
def w04_get_faculty_top_collaborators(faculty_id: int, limit: int=10):
    # first, check if the mysql connection is successful
    if not check_mysql_connection():
        raise ConnectionError("we cannot connect to MySQL database. please check.")
    # after the connection is successful, query collaborators
    fid=int(faculty_id)
    lim=max(1, int(limit))
    sql="""
        select f2.name as collaborator_name, count(distinct fp2.publication_id) as shared_papers
        from faculty_publication fp1
        join faculty_publication fp2
          on fp2.publication_id=fp1.publication_id
         and fp2.faculty_id <> fp1.faculty_id
        join faculty f2 on f2.id=fp2.faculty_id
        where fp1.faculty_id=%s
        group by f2.id, f2.name
        order by shared_papers desc, f2.name asc
        limit %s
    """
    db_config=mysql.connector.connect(**get_mysql_config())
    cur=db_config.cursor(dictionary=True)
    cur.execute(sql, (fid, lim))
    rows=cur.fetchall()
    cur.close()
    db_config.close()
    return rows


# w04-create a function to get representative papers for one faculty, ordered by citations then year
def w04_get_faculty_representative_papers(faculty_id: int, limit: int=8):
    # first, check if the mysql connection is successful
    if not check_mysql_connection():
        raise ConnectionError("we cannot connect to MySQL database. please check.")
    # after the connection is successful, query papers
    fid=int(faculty_id)
    lim=max(1, int(limit))
    sql="""
        select p.title, p.year, p.num_citations
        from faculty_publication fp
        join publication p on p.id=fp.publication_id
        where fp.faculty_id=%s
        order by coalesce(p.num_citations, 0) desc, p.year desc
        limit %s
    """
    db_config=mysql.connector.connect(**get_mysql_config())
    cur=db_config.cursor(dictionary=True)
    cur.execute(sql, (fid, lim))
    rows=cur.fetchall()
    cur.close()
    db_config.close()
    return rows
