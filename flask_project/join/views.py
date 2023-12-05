from flask import Flask,Blueprint, render_template, request, redirect, flash, url_for,session
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
from join.join_Dao import db, MyMember
from flask_login import current_user
            
user_bp=Blueprint('join', __name__)

@user_bp.route('/')
def index():
    members = MyMember.query.all()
    return render_template('join/joindex.html', members=members)

@user_bp.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']
        phone = request.form['phone']
        iswithrew = request.form['iswithrew']
        
        # 회원 추가 트랜잭션 시작
        try:
            new_member = MyMember(id=id, password=password, phone=phone, iswithrew=iswithrew)
            db.session.add(new_member)
            db.session.commit()
            flash('회원 추가 성공', 'success')
        except Exception as e:
            db.session.rollback()
            flash('회원 추가 실패', 'danger')
        finally:
            db.session.close()

    return render_template('join/add_member.html')

@user_bp.route('/edit_member/<string:id>', methods=['GET', 'POST'])
def edit_member(id):
    member = MyMember.query.get(id)
    
    # 현재 로그인한 사용자와 수정하려는 회원 정보의 ID를 비교하여 접근을 제한
    if not current_user.is_authenticated or current_user.id != id:
        flash('접근 권한이 없습니다', 'danger')
        return redirect(url_for('join.index'))

    if request.method == 'POST':
        password = request.form['password']
        phone = request.form['phone']
        iswithrew = request.form['iswithrew']
        
        # 회원 수정 트랜잭션 시작
        try:
            member.password = password
            member.phone = phone
            member.iswithrew = iswithrew
            db.session.commit()
            flash('회원 정보 수정 성공', 'success')
              
        except Exception as e:
            db.session.rollback()
            flash('회원 정보 수정 실패', 'danger')
        
        return redirect(url_for('join.index'))  # 수정 후 목록 페이지로 리다이렉트

    return render_template('join/edit_member.html', member=member)

@user_bp.route('/delete_member/<string:id>', methods=['GET'])
def delete_member(id):
    member = MyMember.query.get(id)
    
    if member:
        try:
            db.session.delete(member)
            db.session.commit()
            flash('회원 삭제 성공', 'success')
        except Exception as e:
            db.session.rollback()
            flash('회원 삭제 실패', 'danger')
        finally:
            db.session.close()

    return redirect(url_for('join.index'))


