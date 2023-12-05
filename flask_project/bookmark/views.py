from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from bookmark.bookmark_dao import BookmarkDAO
from flask_login import LoginManager
from app import app,db

bookmark_bp = Blueprint('bookmark', __name__)
#bookmark_bp.db = db

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # 유저 로딩 코드: user_id를 기반으로 유저 객체를 반환하는 코드
    # 예를 들어, 데이터베이스에서 유저를 조회하는 코드를 작성합니다.
    pass

@bookmark_bp.route('/', methods=['GET', 'POST'])
def bookmark_home():
    dao = BookmarkDAO(db.session)
    bookmarks = dao.read_all_data()
    # member = current_user
    return render_template('bookmark/list_bookmark.html', bookmarks=bookmarks,current_user=current_user)

@bookmark_bp.route('/add_bookmark_form', methods=['GET'])

def add_bookmark_form():
    
    return render_template('bookmark/add_bookmark_form.html')

@bookmark_bp.route('/add', methods=['POST'])

def add_bookmark():
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        member = request.form['member']
        data = (title, url, member)
        dao = BookmarkDAO(db.session)
        dao.insert_data(data)
        flash('북마크가 추가되었습니다.', 'success')
        return redirect(url_for('unique_bookmark.bookmark_home'))

@bookmark_bp.route('/delete', methods=['POST'])
@login_required
def delete_bookmark():
    if request.method == 'POST':
        id = request.form['id']
        dao = BookmarkDAO(db.session)
        bookmark = dao.read_by_id(id)
        
        if bookmark.member == current_user.id:
            dao.delete_data(id)
            flash('북마크가 삭제되었습니다.', 'success')
        else:
            flash('삭제 권한이 없습니다.', 'danger')
        
        return redirect(url_for('unique_bookmark.bookmark_home'))

@bookmark_bp.route('/update', methods=['POST'])
@login_required
def update_bookmark():
    if request.method == 'POST':
        id = request.form['id']
        dao = BookmarkDAO(db.session)
        bookmark = dao.read_by_id(id)
        
        if bookmark.member == current_user.id:
            return render_template('bookmark/update_form.html', bookmark=bookmark)
        else:
            flash('수정 권한이 없습니다.', 'danger')
            return redirect(url_for('unique_bookmark.bookmark_home'))
        
        
        
@bookmark_bp.route('/update_proc', methods=['POST'])
@login_required
def update_proc():
    if request.method == 'POST':
        app.logger.info(request.form)
        id = request.form['id']
        title = request.form['title']
        url = request.form['url']
        member = request.form['member']
        new_data = (title, url, member)
        dao = BookmarkDAO(db.session)
        bookmark = dao.read_by_id(id)
        
        if bookmark is not None and bookmark.member == current_user.id:
            dao.update_data(id, new_data)
            flash('북마크가 수정되었습니다.', 'success')
        elif bookmark is None:
            flash('북마크를 찾을 수 없습니다.', 'danger')
        else:
            flash('수정 권한이 없습니다.', 'danger')
        
        return redirect(url_for('unique_bookmark.bookmark_home'))

# @bookmark_bp.route('/update_proc', methods=['POST'])
# @login_required
# def update_proc():
#     if request.method == 'POST':
#         id = request.form['id']
#         title = request.form['title']
#         url = request.form['url']
#         member = request.form['member']
#         new_data = (title, url, member)
#         dao = BookmarkDAO()
#         bookmark = dao.read_by_id(id)
#
#         if bookmark.member == current_user.id:
#             dao.update_data(id, new_data)
#             flash('북마크가 수정되었습니다.', 'success')
#         else:
#             flash('수정 권한이 없습니다.', 'danger')
#
#         return redirect(url_for('bookmark.bookmark_home'))


# from flask import Blueprint, render_template, request, session, redirect,url_for
# from bookmark.bookmark_dao import BookmarkDAO
# from run import login_manager
#
# bookmark_bp = Blueprint('bookmark', __name__)
#
# @bookmark_bp.route('/', methods=['GET', 'POST'])
# def bookmark_home():
#     dao = BookmarkDAO()  # 루트 앱의 get_db() 함수를 호출합니다.
#     bookmarks = dao.read_all_data()
#     print(bookmarks)
#     return render_template('bookmark/list_bookmark.html', bookmarks=bookmarks)
#
#
# @bookmark_bp.route('/add_bookmark_form', methods=['GET'])
# def add_bookmark_form():
#     return render_template('bookmark/add_bookmark_form.html')
#
# # 회원 추가 처리
# @bookmark_bp.route('/add', methods=['POST'])
# def add_bookmark():
#     if request.method == 'POST':
#         title = request.form['title']
#         url = request.form['url']
#         member = request.form['member']
#
#         data = (title, url, member)
#         dao = BookmarkDAO()
#         dao.insert_data(data)
#         #session.pop('user',None) #'user' 세션을 삭제 
#         return redirect(url_for('bookmark.bookmark_home'))
#
#
#
# # @bookmark_bp.route('/delete', methods=['POST'])
# # def delete_bookmark():
# #     if request.method == 'POST':
# #         no = request.form['id']  # 삭제할 회원의 번호를 받아옵니다.
# #         dao = BookmarkDAO()
# #         dao.delete_data(no)  # DAO를 이용하여 회원 데이터를 삭제합니다.
# #         return redirect(url_for('bookmark.bookmark_home'))  # 삭제 후 회원 목록 페이지로 리다이렉트합니다.
#
# @bookmark_bp.route('/delete', methods=['POST'])
# @login_required
# def delete_bookmark():
#     if request.method == 'POST':
#         id = request.form['id']
#         dao = BookmarkDAO()
#         bookmark = dao.read_by_id(id)
#
#         # 현재 로그인한 회원과 북마크의 작성자가 일치하는 경우에만 삭제 가능
#         if bookmark.member == current_user.id:
#             dao.delete_data(id)
#             flash('북마크가 삭제되었습니다.', 'success')
#         else:
#             flash('삭제 권한이 없습니다.', 'danger')
#
#         return redirect(url_for('bookmark.bookmark_home'))
#
# @bookmark_bp.route('/update', methods=['POST'])
# @login_required
# def update_bookmark():
#     if request.method == 'POST':
#         id = request.form['id']
#         dao = BookmarkDAO()
#         bookmark = dao.read_by_id(id)
#
#         # 현재 로그인한 회원과 북마크의 작성자가 일치하는 경우에만 수정 가능
#         if bookmark.member == current_user.id:
#             return render_template('bookmark/update_form.html', bookmark=bookmark)
#         else:
#             flash('수정 권한이 없습니다.', 'danger')
#             return redirect(url_for('bookmark.bookmark_home'))
#
# @bookmark_bp.route('/update_proc', methods=['POST'])
# @login_required
# def update_proc():
#     if request.method == 'POST':
#         id = request.form['id']
#         title = request.form['title']
#         url = request.form['url']
#         member = request.form['member']
#         new_data = (title, url, member)
#         dao = BookmarkDAO()
#         bookmark = dao.read_by_id(id)
#
#         # 현재 로그인한 회원과 북마크의 작성자가 일치하는 경우에만 수정 가능
#         if bookmark.member == current_user.id:
#             dao.update_data(id, new_data)
#             flash('북마크가 수정되었습니다.', 'success')
#         else:
#             flash('수정 권한이 없습니다.', 'danger')
#
#         return redirect(url_for('bookmark.bookmark_home'))
#
#
#
# # @bookmark_bp.route('/update', methods=['POST'])
# # def update_bookmark():
# #     if request.method == 'POST':
# #         id = request.form['id']  
# #         dao = BookmarkDAO()
# #         bookmark  = dao.read_by_id(id)
# #         return render_template('bookmark/update_form.html', bookmark=bookmark)
# #         #return redirect(url_for('update_form'),member=member)  # 삭제 후 회원 목록 페이지로 리다이렉트합니다.
# #
# # @bookmark_bp.route('/update_proc', methods=['POST'])
# # def update_proc():
# #     if request.method == 'POST':
# #         id = request.form['id']
# #         title = request.form['title']
# #         url = request.form['url']
# #         member = request.form['member']
# #         new_data = (title, url, member)
# #         dao = BookmarkDAO()
# #         dao.update_data(id, new_data)
# #         return redirect(url_for('bookmark.bookmark_home'))
# #
