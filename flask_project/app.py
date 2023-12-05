from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,instance_relative_config=True)
app.secret_key = 'java'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
db = SQLAlchemy(app)
with app.app_context():
        db.create_all()  # 데이터베이스 테이블 생성

