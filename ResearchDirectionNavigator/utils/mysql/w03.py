import mysql.connector

from .core import get_mysql_config

# W3 compare universities
# input names should already be cleaned/deduped in the service layer
def w03_get_comparision_information_among_universities(clean_university_names):
    if not clean_university_names:
        return []
    number_of_selected_universities=len(clean_university_names)

    # fast path: filter university with in (...) — avoids the slow wanted-union + left join plan
    comma_separated_placeholders=", ".join(["%s"]*number_of_selected_universities)

    sql_query_for_university_comparison=f"""
        select
            u.name as university_name,
            count(distinct fp.publication_id) as total_publication_count,
            count(distinct f.id) as faculty_number,
            (
                select count(distinct fp5.publication_id)
                from faculty fac5
                join faculty_publication fp5 on fp5.faculty_id=fac5.id
                join publication pub5 on pub5.id=fp5.publication_id
                where fac5.university_id=u.id
                  and cast(pub5.year as signed)>=year(curdate())-19
            ) as publication_count_last_twenty_years,
            (
                select coalesce(sum(pub_cite.num_citations), 0)
                from publication pub_cite
                where pub_cite.id in (
                    select distinct fp_cite.publication_id
                    from faculty fac_cite
                    join faculty_publication fp_cite on fp_cite.faculty_id=fac_cite.id
                    where fac_cite.university_id=u.id
                )
            ) as total_citation_sum
        from university u
        left join faculty f on f.university_id=u.id
        left join faculty_publication fp on fp.faculty_id=f.id
        where u.name in ({comma_separated_placeholders})
        group by u.id, u.name
    """

    db_config=mysql.connector.connect(**get_mysql_config())
    cur=db_config.cursor(dictionary=True)
    tuple_of_university_names_for_sql=tuple(clean_university_names)
    cur.execute(sql_query_for_university_comparison, tuple_of_university_names_for_sql)
    results=cur.fetchall()
    cur.close()
    db_config.close()

    # one row per selected name (same order as multiselect): names with no university.name match
    # get placeholder zeros so W3 still shows a table instead of a false "pick 2+" message
    by_name={row["university_name"]: row for row in results}
    merged=[]
    for name in clean_university_names:
        if name in by_name:
            merged.append(by_name[name])
        else:
            merged.append(
                {
                    "university_name": name,
                    "total_publication_count": 0,
                    "faculty_number": 0,
                    "publication_count_last_twenty_years": 0,
                    "total_citation_sum": 0,
                }
            )
    return merged
