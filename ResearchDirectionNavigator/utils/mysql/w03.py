"""Widget 3 — multi-university comparison."""

import mysql.connector

from .core import check_mysql_connection, get_mysql_config

# w03-create a function to get the relevent information about the comparision among diverse universities
def w03_get_comparision_information_among_universities(selected_university_names):
    # first, check if the mysql connection is successful
    if not check_mysql_connection():
        raise ConnectionError("we cannot connect to MySQL database. please check.")
    
    # second check the input
    # if no university was selected, return an empty list
    if selected_university_names is None:
        return []
    # create a list to store the selected university that remove the spaces
    selected_universites_list_without_space=[]
    for single_university_name in selected_university_names:
        # remove the space
        selected_university_text_without_space=(single_university_name or "").strip()
        if selected_university_text_without_space=="":
            continue
        if selected_university_text_without_space not in selected_universites_list_without_space:
            selected_universites_list_without_space.append(selected_university_text_without_space)
    # get the number of selected universities
    number_of_selected_universities=len(selected_universites_list_without_space)
    # if only one university was selected, retunr an empty list
    if number_of_selected_universities<2:
        return []

    # third, construct the placeholders in query
    number_of_placeholders=number_of_selected_universities
    comma_separated_palceholders=", ".join(["%s"]*number_of_placeholders)

    # fourth, construct the query command
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
                  and cast(pub5.year as signed) >= year(curdate())-19
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
        where u.name in ({comma_separated_palceholders})
        group by u.id, u.name
        order by u.name
    """

    # fifth, execute the query command
    db_config=mysql.connector.connect(**get_mysql_config())
    cur=db_config.cursor(dictionary=True)
    tuple_of_university_names_for_sql=tuple(selected_universites_list_without_space)
    cur.execute(sql_query_for_university_comparison, tuple_of_university_names_for_sql)
    results=cur.fetchall()
    cur.close()
    db_config.close()
    return results
