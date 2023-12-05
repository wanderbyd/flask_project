from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
from flask_login import UserMixin
from app import db

#db = SQLAlchemy()

class MyMember(UserMixin,db.Model):
    __tablename__ = 'mymember'
    id = db.Column(db.String(255), primary_key=True)
    joindate = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    password = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    iswithrew = db.Column(db.String(10))

    def __init__(self, id, password, phone, iswithrew):
        self.id = id
        self.password = password
        self.phone = phone
        self.iswithrew = iswithrew

class MyMemberView(ModelView):
    column_list = ['id', 'joindate', 'phone', 'iswithrew']
    form_columns = ['id', 'password', 'phone', 'iswithrew']

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.joindate = datetime.utcnow()
            db.session.add(model)
            db.session.commit()
        else:
            db.session.commit()

