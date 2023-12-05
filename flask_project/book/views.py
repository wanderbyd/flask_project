from flask import Blueprint, render_template, flash, redirect, url_for, request
from book import book_dao
from datetime import datetime

book_bp = Blueprint('book', __name__)
dao = book_dao.BookDao()

@book_bp.route('/create_book', methods=['GET', 'POST'])
def create_book():
    try:
        if request.method == 'POST':
            bookname = request.form['bookname']
            writer = request.form['writer']
            publisher = request.form['publisher']
            
            # 현재 시간을 얻어 포맷팅
            current_time = datetime.now()
            formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
            
            # 데이터 튜플 생성
            data = (bookname, formatted_time, writer, publisher, 'no')
            dao.insertD(data)
            
            flash('도서가 등록되었습니다.', 'success')
        return redirect(url_for('book.bindex'))
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        flash("오류가 발생했습니다. 다시 시도해주세요.", 'danger')
        return redirect(url_for('book.bindex'))

@book_bp.route('/update_book/<int:no>', methods=['GET', 'POST'])
def update_book(no):
    if request.method == 'GET':
        book = dao.readD(no)
        return render_template('book/update.html', book=book)
    elif request.method == 'POST':
        bookname = request.form['bookname']
        writer = request.form['writer']
        publisher = request.form['publisher']
        
        current_time = datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        
        data = (bookname, formatted_time, writer, publisher, 'no')
        dao.updateD(no, data)
        flash('도서 정보가 수정되었습니다.', 'success')
        return redirect(url_for('book.bindex'))

@book_bp.route('/delete_book/<int:no>')
def delete_book(no):
    dao.deleteD(no)
    flash('도서가 삭제되었습니다.', 'success')
    return redirect(url_for('book.bindex'))

@book_bp.route('/')
def bindex():
    books = dao.readD()
    return render_template('book/book.html', books=books)
