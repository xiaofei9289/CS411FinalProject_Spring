import mysql.connector

from .connection_config import get_mysql_config

# W4 faculty stats: name, university, # papers, citations
def w04_get_faculty_profile_stats(faculty_id):
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


# W4 top keywords for this faculty
def w04_get_faculty_top_keywords(faculty_id, limit=15):
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


# W4 co-authors by # shared papers
def w04_get_faculty_top_collaborators(faculty_id, limit=10):
    fid=int(faculty_id)
    lim=max(1, int(limit))
    sql="""
        select f2.name as collaborator_name, count(distinct fp2.publication_id) as shared_papers
        from faculty_publication fp1
        join faculty_publication fp2
          on fp2.publication_id=fp1.publication_id
         and fp2.faculty_id<>fp1.faculty_id
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


# W4 best papers by citations then year
def w04_get_faculty_representative_papers(faculty_id, limit=8):
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
