import sqlite3

def run(dbname='mock_fb.db'):

    CON = sqlite3.connect(dbname)
    CUR = CON.cursor()

    CUR.execute("""DROP TABLE IF EXISTS users;""")
    # create accounts table
    CUR.execute("""CREATE TABLE users(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR,
        password VARCHAR,
        CONSTRAINT unique_username UNIQUE(username)
    );""")

    CUR.execute("""DROP TABLE IF EXISTS posts;""")
    # create positions table
    CUR.execute("""CREATE TABLE posts(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        content VARCHAR,
        time INTEGER,
        username VARCHAR,
        users_pk INTEGER,
        FOREIGN KEY(users_pk) REFERENCES users(pk)
    );""")

    CON.commit()
    CUR.close()
    CON.close()

if __name__ == '__main__':
    run()