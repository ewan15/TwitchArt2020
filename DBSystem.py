import sqlite3


class DBSystem:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS USERS
                            (USERNAME VARCHAR(255) PRIMARY KEY NOT NULL,
                            IMAGE VARCHAR (255) NOT NULL)''')
        self.cur = self.conn.cursor()

    def insert_user_image(self, username, image):
        self.conn.execute(f'''INSERT OR REPLACE INTO USERS (USERNAME, IMAGE) VALUES ("{username}","{image}")''')
        self.conn.commit()

    def fetch_data(self):
        self.cur.execute('''SELECT IMAGE FROM USERS''')
        rows = self.cur.fetchall()
        return rows

#db = DBSystem()
#db.insert_user_image('jeff2', 'hello.png')
#db.fetch_data()
