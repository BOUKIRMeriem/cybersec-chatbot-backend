from flask_mysqldb import MySQL

class User:
    @staticmethod
    def create(mysql, username, hashed_password):
        cur = mysql.connection.cursor()
        query = "INSERT INTO user (username, password) VALUES (%s, %s)"
        cur.execute(query, (username, hashed_password))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def get_by_username(mysql, username):
        cur = mysql.connection.cursor()
        query = "SELECT * FROM user WHERE username = %s"
        cur.execute(query, (username,))
        user = cur.fetchone()
        cur.close()
        return user
