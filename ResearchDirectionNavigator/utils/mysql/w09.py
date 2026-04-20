"""Widget 9 — favorite professors (search, list, add/remove with transaction)."""

import mysql.connector

from .core import check_mysql_connection, get_mysql_config

# w09-create a function to search faculty by name pattern for candidates to add to favorites
def w09_search_faculty_by_name(name_pattern: str, limit: int=15):
    # first, check if the mysql connection is successful
    if not check_mysql_connection():
        raise ConnectionError("we cannot connect to MySQL database. please check.")
    # clean up the user input first
    text=(name_pattern or "").strip()
    if not text:
        return []
    # after the connection is successful, run LIKE search on faculty name
    pattern="%"+text+"%"
    sql="""
        select f.id, f.name as faculty_name, u.name as university_name
        from faculty f
        join university u on u.id=f.university_id
        where f.name like %s
        order by f.name asc
        limit %s
    """
    db_config=mysql.connector.connect(**get_mysql_config())
    cur=db_config.cursor(dictionary=True)
    cur.execute(sql, (pattern, int(limit)))
    rows=cur.fetchall()
    cur.close()
    db_config.close()
    return rows


# w09-create a function to list all favorite professors with university names, newest first
def w09_list_favorites():
    # first, check if the mysql connection is successful
    if not check_mysql_connection():
        raise ConnectionError("we cannot connect to MySQL database. please check.")
    # after the connection is successful, read the favorite_professors table with joins
    sql="""
        select fav.faculty_id, f.name as faculty_name, u.name as university_name,
               fav.created_at
        from favorite_professors fav
        join faculty f on f.id=fav.faculty_id
        join university u on u.id=f.university_id
        order by fav.created_at desc, fav.id desc
    """
    db_config=mysql.connector.connect(**get_mysql_config())
    cur=db_config.cursor(dictionary=True)
    cur.execute(sql)
    rows=cur.fetchall()
    cur.close()
    db_config.close()
    return rows


# w09-create a function to add one favorite and write an ADD row in favorite_log inside one transaction
def w09_add_favorite_with_transaction(faculty_id: int):
    # first, check if the mysql connection is successful
    if not check_mysql_connection():
        raise ConnectionError("we cannot connect to MySQL database. please check.")
    fid=int(faculty_id)

    db_config=mysql.connector.connect(**get_mysql_config())
    cur=db_config.cursor()
    try:
        # second, start transaction and run two DML statements (favorite row + log row)
        cur.execute("start transaction")

        # insert the favorite row; insert ignore skips when UNIQUE(faculty_id) already holds this professor
        cur.execute(
            "insert ignore into favorite_professors (faculty_id) values (%s)",
            (fid,),
        )
        inserted_row_count=cur.rowcount

        # append an audit-log row for the ADD action
        cur.execute(
            "insert into favorite_log (faculty_id, action) values (%s, 'ADD')",
            (fid,),
        )

        db_config.commit()
        return {"ok": True, "inserted": inserted_row_count, "faculty_id": fid}
    except Exception:
        db_config.rollback()
        raise
    finally:
        cur.close()
        db_config.close()


# w09-create a function to remove one favorite and write a REMOVE row in favorite_log inside one transaction
def w09_remove_favorite_with_transaction(faculty_id: int):
    # first, check if the mysql connection is successful
    if not check_mysql_connection():
        raise ConnectionError("we cannot connect to MySQL database. please check.")
    fid=int(faculty_id)

    db_config=mysql.connector.connect(**get_mysql_config())
    cur=db_config.cursor()
    try:
        # second, start transaction and run two DML statements (delete favorite + log row)
        cur.execute("start transaction")

        # delete the favorite row when present
        cur.execute(
            "delete from favorite_professors where faculty_id=%s",
            (fid,),
        )
        deleted_row_count=cur.rowcount

        # append an audit-log row for the REMOVE action
        cur.execute(
            "insert into favorite_log (faculty_id, action) values (%s, 'REMOVE')",
            (fid,),
        )

        db_config.commit()
        return {"ok": True, "deleted": deleted_row_count, "faculty_id": fid}
    except Exception:
        db_config.rollback()
        raise
    finally:
        cur.close()
        db_config.close()
