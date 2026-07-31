import mysql.connector


def login(conn, username, password):

    cursor = conn.cursor(dictionary=True)

    try:

        query = """
            SELECT
                id,
                username,
                nama_lengkap,
                role,
                status
            FROM users
            WHERE username = %s
            AND password = %s
            LIMIT 1
        """

        cursor.execute(
            query,
            (username, password)
        )

        user = cursor.fetchone()

        return user

    finally:

        cursor.close()