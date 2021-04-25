# file name : dbModule.py
# pwd : /project_name/app/module/dbModule.py
 
import pymysql
 
class Database():
    def __init__(self):
        self.db= pymysql.connect(host='localhost',
                                  user='root',
                                  password='k1010910',
                                  db='securIoT',
                                  charset='utf8')
        self.cursor= self.db.cursor(pymysql.cursors.DictCursor)
        self.theft = False
        self.mail = 0

 
    def set_theft(self, sett):
            self.theft = sett
    def get_theft(self):
        return self.theft
    
    def execute(self, query, args={}):
        self.cursor.execute(query, args) 
 
    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row= self.cursor.fetchone()
        return row
 
    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row= self.cursor.fetchall()
        return row
 
    def commit(self):
        self.db.commit()

    def check_uid(self, uid):
        sql_check = 'SELECT * FROM RFID WHERE uid=%s;'
        row = self.executeAll(sql_check, uid)
        if row:
            return True
        else:
            return False

    def insert_db(self, uid):
        order = 'INSERT INTO RFID(uid) VALUE(\'' + uid + '\');'
        self.executeAll(order)
        self.commit()

    def delete_db(self, uid):
        order = 'DELETE FROM RFID WHERE uid=(\'' + uid + '\');'
        self.executeAll(order)
        self.commit()