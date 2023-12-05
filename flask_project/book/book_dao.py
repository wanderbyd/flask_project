import sqlite3
class BookDao:
    def __init__(self, db_path='my_database.db'):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.create_table()

    def create_table(self):
        connection = sqlite3.connect(self.db_path)
        cursor = self.connection.cursor()
        cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='mybook';''')
        if cursor.fetchone()[0] == 1:
            return
        create_table_sql = '''
          CREATE TABLE IF NOT EXISTS mybook (
          no INTEGER PRIMARY KEY AUTOINCREMENT,
          bookname TEXT,
          regdate TIMESTAMP,
          writer TEXT,            
          publisher TEXT,
          iswithrew TEXT
          )
          '''
        cursor.execute(create_table_sql)
        connection.commit()
        connection.close()

    def readD(self, no=None):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
    
        if no is None:
            select_all_data_sql = '''
                SELECT * FROM mybook
            '''
            cursor.execute(select_all_data_sql)
        else:
            select_data_sql = '''
                SELECT * FROM mybook WHERE no = ?
            '''
            cursor.execute(select_data_sql, (no,))
    
        data = cursor.fetchall()
        connection.close()
        return data
    
    def insertD(self, data):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        insert_data_sql = '''
            INSERT INTO mybook (bookname, regdate, writer, publisher, iswithrew)
            VALUES (?, ?, ?, ?, ?)
        '''
        cursor.execute(insert_data_sql, data)
        connection.commit()
        connection.close()
    
    def updateD(self, no, data):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        update_data_sql = '''
            UPDATE mybook
            SET bookname=?, regdate=?, writer=?, publisher=?, iswithrew=?
            WHERE no=?
        '''
        cursor.execute(update_data_sql, (*data, no))
        connection.commit()
        connection.close()
    
    def deleteD(self, no):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        delete_data_sql = '''
            DELETE FROM mybook
            WHERE no=?
        '''
        cursor.execute(delete_data_sql, (no,))
        connection.commit()
        connection.close()

