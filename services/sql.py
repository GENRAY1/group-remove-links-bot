import sqlite3;
from settings import DB_FILE
class DataBase:
    def __init__(self):
        self.connect = sqlite3.connect(DB_FILE)
        self.cursor = self.connect.cursor()
    
    #async def add_user(self, chatid, username, date):
    #   with self.connect:
    #        return self.cursor.execute('''INSERT INTO User(chat_id, username, date_reg) VALUES(?,?,?)''',
    #                                  [chatid, username,date]
    #                                 )
    #async def get_state(self, chatid):
    #    with self.connect:
    #        result = self.cursor.execute('''SELECT States.name FROM States 
    #        JOIN User ON User.state_id=States.state_id
    #        WHERE User.chat_id=(?)''',
    #        [chatid]).fetchone()
    #        return result[0]
        
        
    def get_admins(self):
        with self.connect: 
            result = self.cursor.execute('''SELECT chat_id FROM Admins''').fetchall()
            output = []
            for item in result:
                output.append(item[0])
            return output
        
    async def get_only_links(self):
        with self.connect:
            return self.cursor.execute('''SELECT link FROM BlackListLinks''').fetchall()
        
    async def get_links(self):
        with self.connect:
            return self.cursor.execute('''SELECT id,link FROM BlackListLinks''').fetchall()
    async def add_links(self, link):
        with self.connect:
            return self.cursor.execute('''INSERT INTO BlackListLinks(link) VALUES(?)''',
                                       [link])
    async def del_link(self, id):
        with self.connect:
            return self.cursor.execute('''DELETE FROM BlackListLinks WHERE id=(?)''',
                                       [id]
                                       )
    async def get_only_groups(self):
        with self.connect:
            result = self.cursor.execute('''SELECT username FROM Groups''').fetchall()
            output = []
            for item in result:
                output.append(item[0])
            return output
        
    async def get_group(self):
        with self.connect:
            return self.cursor.execute('''SELECT id,username FROM Groups''').fetchall()
        
    async def add_group(self, username):
        with self.connect:
            return self.cursor.execute('''INSERT INTO Groups(username) VALUES(?)''',
                                       [username])
    async def del_group(self, id):
        with self.connect:
            return self.cursor.execute('''DELETE FROM Groups WHERE id=(?)''',
                                       [id])
        
    async def get_stateid(self, chatid):
        with self.connect:
            result = self.cursor.execute('''SELECT state_id From Admins WHERE chat_id=(?)''',[chatid]).fetchone()            
            return result[0]
        
    async def set_stateid(self, chatid, new_stateid):
        with self.connect:
            return self.cursor.execute('''UPDATE Admins SET state_id=(?) WHERE chat_id=(?)''',
                                       [new_stateid, chatid])
    