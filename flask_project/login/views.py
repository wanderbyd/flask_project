from flask import Flask, render_template, request, flash, redirect, url_for,Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
from join.join_Dao import db, MyMember

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

login_bp = Blueprint('login', __name__)
def get_all_members():
    return MyMember.query.all()

@login_manager.user_loader
def load_user(user_id):
    # 이 함수는 로그인 시에 호출되며, user_id에 해당하는 사용자를 반환합니다.
    return MyMember.query.get(user_id)

@login_bp.route('/login/ownedit')
def loginmenu():
    return render_template('join/ownedit.html')

#이거 제대로 구현해야함
# @login_bp.route('/admin')
# @login_required  # 로그인이 필요한 뷰
# def admin():
#     if current_user.id == 'admin':
#         return '어드민 페이지'
#     else:
#         return '접근 권한이 없습니다.'

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']
        user = MyMember.query.get(id)
        if user and user.password == password:
            login_user(user)  # 로그인 처리
            flash('로그인 성공', 'success')

            if user.id == 'admin' and user.password == '12345':
                return redirect(url_for('admin.index'))
            else:
                return redirect(url_for('join.index'))
        else:
            flash('로그인 실패', 'danger')
    return render_template('/join/login.html')

# 로그아웃
@login_bp.route('/logout')
@login_required  # 로그인 상태에서만 로그아웃할 수 있도록 설정
def logout():
    logout_user()  # 로그아웃 처리
    flash('로그아웃 되었습니다', 'success')
    return redirect(url_for('menu'))

