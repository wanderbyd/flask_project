import sqlite3
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime
from flask import current_app
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from homebook.models  import Homebook
from flask_admin.contrib.sqla import ModelView
from app import db # 중요한 부분 

class HomebookView(ModelView):
    column_display_pk = True  # 기본키 (시리얼 번호)를 표시합니다.
    column_list = {
        'transaction_date': '거래일자',
        'id': '멤버 ID',
        'transaction_type': '거래 유형',
        'account_subject': '계정 항목',
        'description': '설명',
        'credit': '수입',
        'debit': '지출'
    }
# class HomebookView(ModelView):
#     column_display_pk = True  # 기본키 (시리얼 번호)를 표시합니다.
#     column_labels = {
#         'transaction_date': '거래일자',
#         'id': '멤버 ID',
#         'transaction_type': '거래 유형',
#         'account_subject': '계정 항목',
#         'description': '설명',
#         'credit': '수입',
#         'debit': '지출'
#     }

class HomebookDAO:

    def __init__(self):
        self.db =  db  # db 연동 원리를 잘 생각할것 

    def insert_data(self, data):
        new_homebook = Homebook(
            transaction_date=data[0],
            id=data[1],
            #id=data[1],
            transaction_type=data[2],
            account_subject=data[3],
            description=data[4],
            credit=data[5],
            debit=data[6]
        )
        self.db.session.add(new_homebook)
        self.db.session.commit()

    #data = (transaction_date, id, transaction_type, account_subject, description, credit, debit)
    def record_transaction(self, transaction_date, id, transaction_type, account_subject, description, credit, debit):
        # vo 객체로 만듬 
        new_homebook = Homebook(
            transaction_date=transaction_date,
            id=id,
            transaction_type=transaction_type,
            account_subject=account_subject,
            description=description,
            credit=credit,
            debit=debit
        )
        self.db.session.add(new_homebook)
        self.db.session.commit()
        return True

    def insert_sample_data(self):
        sample_data = [
            ('2023-09-11', 'hgd', '수입', '잡수입', '수고비', 1000000, 0.0),
            ('2023-09-12', 'ygs', '지출', '교통비', '버스 요금', 0.0, 5000),
            ('2023-09-13', 'ggc', '수입', '월급', '월급 지급', 5000000, 0.0)
        ]
        for data in sample_data:
            self.record_transaction(*data) #  **data로 쓰는법 gpt에 물어보세요! 

    def read_all_data(self): # 모든 레코드 정보를 가져옴 
        return Homebook.query.all()

    def read_data(self, sn): # 시리얼번호로 하나의 레코드 정보만 읽어옴 
        return self.db.session.query(Homebook).get(sn)

    def update_data(self, sn, new_data): #프라이머리키인 시리얼번호와 나머지 전체데이타를 튜플로 받는다.
        # 고치기 전의 정보를 읽어 온다.
        record = self.db.session.query(Homebook).get(sn)
        if record:
            record.transaction_date = new_data[0]
            record.id = new_data[1]
            record.transaction_type = new_data[2]
            record.account_subject = new_data[3]
            record.description = new_data[4]
            record.credit = new_data[5]
            record.debit = new_data[6]
            self.db.session.commit() # 디비에 반영 

    def delete_data(self, sn):
        record = self.db.session.query(Homebook).get(sn)
        if record:
            self.db.session.delete(record)
            self.db.session.commit()








# import sqlite3
# from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Column, Integer, String, DateTime
# from flask import current_app
# from sqlalchemy.orm import Session
# from sqlalchemy.orm import sessionmaker
# from homebook.models  import Homebook
# from flask_admin.contrib.sqla import ModelView
# from app import db # 중요한 부분 
#
# class HomebookView(ModelView):
#     column_display_pk = True  # 기본키 (시리얼 번호)를 표시합니다.
#     column_labels = {
#         'transaction_date': '거래일자',
#         'member_id': '멤버 ID',
#         'transaction_type': '거래 유형',
#         'account_subject': '계정 항목',
#         'description': '설명',
#         'credit': '수입',
#         'debit': '지출'
#     }
#
# class HomebookDAO:
#
#     def __init__(self):
#         self.db =  db  # db 연동 원리를 잘 생각할것 
#
#     def insert_data(self, data):
#         new_homebook = Homebook(
#             transaction_date=data[0],
#             member_id=data[1],
#             #member_id=data[1],
#             transaction_type=data[2],
#             account_subject=data[3],
#             description=data[4],
#             credit=data[5],
#             debit=data[6]
#         )
#         self.db.session.add(new_homebook)
#         self.db.session.commit()
#
#     #data = (transaction_date, member_id, transaction_type, account_subject, description, credit, debit)
#     def record_transaction(self, transaction_date, member_id, transaction_type, account_subject, description, credit, debit):
#         # vo 객체로 만듬 
#         new_homebook = Homebook(
#             transaction_date=transaction_date,
#             member_id=member_id,
#             transaction_type=transaction_type,
#             account_subject=account_subject,
#             description=description,
#             credit=credit,
#             debit=debit
#         )
#         self.db.session.add(new_homebook)
#         self.db.session.commit()
#         return True
#
#     def insert_sample_data(self):
#         sample_data = [
#             ('2023-09-11', 'hgd', '수입', '잡수입', '수고비', 1000000, 0.0),
#             ('2023-09-12', 'ygs', '지출', '교통비', '버스 요금', 0.0, 5000),
#             ('2023-09-13', 'ggc', '수입', '월급', '월급 지급', 5000000, 0.0)
#         ]
#         for data in sample_data:
#             self.record_transaction(*data) #  **data로 쓰는법 gpt에 물어보세요! 
#
#     def read_all_data(self): # 모든 레코드 정보를 가져옴 
#         return Homebook.query.all()
#
#     def read_data(self, sn): # 시리얼번호로 하나의 레코드 정보만 읽어옴 
#         return self.db.session.query(Homebook).get(sn)
#
#     def update_data(self, sn, new_data): #프라이머리키인 시리얼번호와 나머지 전체데이타를 튜플로 받는다.
#         # 고치기 전의 정보를 읽어 온다.
#         record = self.db.session.query(Homebook).get(sn)
#         if record:
#             record.transaction_date = new_data[0]
#             record.member_id = new_data[1]
#             record.transaction_type = new_data[2]
#             record.account_subject = new_data[3]
#             record.description = new_data[4]
#             record.credit = new_data[5]
#             record.debit = new_data[6]
#             self.db.session.commit() # 디비에 반영 
#
#     def delete_data(self, sn):
#         record = self.db.session.query(Homebook).get(sn)
#         if record:
#             self.db.session.delete(record)
#             self.db.session.commit()
#


