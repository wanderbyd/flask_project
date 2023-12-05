
from app import db

class Homebook(db.Model):
    __tablename__ = 'homebook'

    sn = db.Column(db.Integer, primary_key=True, autoincrement=True)# 일련번호
    transaction_date = db.Column(db.Date)# 거래일자
    id = db.Column(db.String(20), db.ForeignKey('mymember.id'))# 기록자id
    transaction_type = db.Column(db.String(10))# 수지구분(수입/지출)
    account_subject = db.Column(db.String(50))# 계정과목
    description = db.Column(db.String(255))# 적요 
    credit = db.Column(db.Float, default=0)# 수입금액
    debit = db.Column(db.Float, default=0)# 지출금액 



# '''
# Created on 2023. 9. 21.
# @author: sem
# '''
# from app import db
#
# class Homebook(db.Model):
#     __tablename__ = 'homebook'
#
#     sn = db.Column(db.Integer, primary_key=True, autoincrement=True)# 일련번호
#     transaction_date = db.Column(db.Date)# 거래일자
#     member_id = db.Column(db.String(20), db.ForeignKey('mymember.member_id'))# 기록자id
#     transaction_type = db.Column(db.String(10))# 수지구분(수입/지출)
#     account_subject = db.Column(db.String(50))# 계정과목
#     description = db.Column(db.String(255))# 적요 
#     credit = db.Column(db.Float, default=0)# 수입금액
#     debit = db.Column(db.Float, default=0)# 지출금액 
#



