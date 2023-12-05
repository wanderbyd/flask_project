import sqlite3
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime
from flask import current_app
from app import db
from .models import Bookmark
from flask_admin.contrib.sqla import ModelView

class BookmarkView(ModelView):
    column_list = ['title', 'url', 'member']


class BookmarkDAO:
         
    def __init__(self,session):
        self.db = db
       # self.session = session
        self.create_table()
 
    def create_table(self):
    
        from sqlalchemy import create_engine
            # SQLAlchemy 엔진 생성
        engine = create_engine('sqlite:///my_database.db')
        
        # CREATE TABLE 문을 문자열로 정의
        create_table_sql = '''
            CREATE TABLE IF NOT EXISTS bookmark (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                url TEXT,
                member TEXT
            );
        '''

    def insert_data(self, data):
        try:
            new_bookmark = Bookmark(title=data[0], url=data[1], member=data[2])
            self.db.session.add(new_bookmark)
            self.db.session.commit()
            return True
        except Exception as e:
            print(f"Error during data insertion: {e}")
            self.db.session.rollback()
            return False

    def insert_sample_data(self):
        try:
            sample_bookmarks = [
                Bookmark(title='우리들의 블로그', url='http://cafe.daum.net/ncsit', member='sjw'),
                Bookmark(title='성주원의 가상대학', url='http://cafe.naver.com/javastudy2', member='sjw')
            ]
            self.db.session.bulk_save_objects(sample_bookmarks)
            self.db.session.commit()
            return True
        except Exception as e:
            print(f"Error during sample data insertion: {e}")
            self.db.session.rollback()
            return False

    def register(self, title, url):
        try:
            new_bookmark = Bookmark(title=title, url=url)
            self.db.session.add(new_bookmark)
            self.db.session.commit()
            return True
        except Exception as e:
            print(f"Error during registration: {e}")
            self.db.session.rollback()
            return False

    def read_all_data(self):
        try:
            data = Bookmark.query.all()
            return data
        except Exception as e:
            print(f"Error during data retrieval: {e}")
            return []

    def read_by_id(self, id):
        try:
            data = Bookmark.query.filter_by(id=id).first()
            return data
        except Exception as e:
            print(f"Error during data retrieval by id: {e}")
            return None

    def update_data(self, id, new_data):
        try:
            bookmark_to_update = Bookmark.query.get(id)
            bookmark_to_update.title = new_data[0]
            bookmark_to_update.url = new_data[1]
            bookmark_to_update.member = new_data[2]
            self.db.session.commit()
            return True
        except Exception as e:
            print(f"Error during data update: {e}")
            self.db.session.rollback()
            return False

    def delete_data(self, id):
        try:
            bookmark_to_delete = Bookmark.query.get(id)
            self.db.session.delete(bookmark_to_delete)
            self.db.session.commit()
            return True
        except Exception as e:
            print(f"Error during data deletion: {e}")
            self.db.session.rollback()
            return False