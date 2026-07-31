import mysql.connector


def login(conn, username, password):

    cursor = conn.cursor(dictionary=True)


    query = """
    SELECT *
    FROM users
    WHERE username = %s
    AND password = %s
    """


    cursor.execute(
        query,
        (username, password)
    )


    user = cursor.fetchone()


    cursor.close()


    return user