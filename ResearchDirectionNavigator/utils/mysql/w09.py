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
    # check whether MySQL is available
    if not check_mysql_connection():
        raise ConnectionError("we cannot connect to MySQL database. please check.")
    # make sure faculty_id is an integer
    professor_id = int(faculty_id)
    mysql_connection = None
    mysql_cursor = None
    try:
        # connect to MySQL
        mysql_connection = mysql.connector.connect(**get_mysql_config())
        # turn off autocommit so we can control the transaction manually
        mysql_connection.autocommit = False

        # create a cursor object to execute SQL
        mysql_cursor = mysql_connection.cursor()
        mysql_cursor.execute(
            """
            insert ignore into favorite_professors (faculty_id)
            values (%s)
            """,
            (professor_id,),
        )
        # save how many rows were really inserted
        inserted_row_count = mysql_cursor.rowcount
        # insert one ADD action record into favorite_log
        mysql_cursor.execute(
            """
            insert into favorite_log (faculty_id, action)
            values (%s, 'ADD')
            """,
            (professor_id,),
        )

        # commit both SQL statements together
        mysql_connection.commit()
        return {
            "ok": True,
            "inserted": inserted_row_count,
            "faculty_id": professor_id,
        }
    except Exception:
        if mysql_connection is not None:
            mysql_connection.rollback()
        raise
    finally:
        if mysql_cursor is not None:
            mysql_cursor.close()
        if mysql_connection is not None:
            mysql_connection.close()


# w09-create a function to remove one favorite and write a REMOVE row in favorite_log inside one transaction
def w09_remove_favorite_with_transaction(faculty_id: int):
    # check database connection
    if not check_mysql_connection():
        raise ConnectionError("we cannot connect to MySQL database. please check.")
    # convert input into integer
    faculty_id = int(faculty_id)
    connection = None
    cursor = None
    try:
        # connect to mysql
        connection = mysql.connector.connect(**get_mysql_config())

        # use manual transaction control
        connection.autocommit = False
        # create cursor
        cursor = connection.cursor()
        # delete one row from favorite_professors
        cursor.execute(
            "delete from favorite_professors where faculty_id = %s",
            (faculty_id,),
        )
        deleted = cursor.rowcount

        # add one log row into favorite_log
        cursor.execute(
            "insert into favorite_log (faculty_id, action) values (%s, 'REMOVE')",
            (faculty_id,),
        )
        connection.commit()
        return {"ok": True, "deleted": deleted, "faculty_id": faculty_id}
    except Exception:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
