from calculator.views import calculator_bp
from gugudan.views import gugudan_bp
from flask import Flask, render_template,session
from book.views import book_bp
from join.views import user_bp
from board.views import board_bp
from login.views import login_bp 
from bookmark.views import bookmark_bp 
from homebook.views import homebook_bp 
from join.join_Dao import MyMember,MyMemberView
from flask_admin import Admin, AdminIndexView
from flask_login import LoginManager
from app import app,db
from bookmark.bookmark_dao import BookmarkView
from bookmark.models import Bookmark
from homebook.homebook_dao import HomebookView
from homebook.models import Homebook


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#db.init_app(app)
admin = Admin(app, name='Flask-Admin Example', template_mode='bootstrap3', index_view=AdminIndexView())
admin.add_view(MyMemberView(MyMember, db.session))
admin.add_view(BookmarkView(Bookmark, db.session))
admin.add_view(HomebookView(Homebook, db.session))

#admin.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # 이 함수는 로그인 시에 호출되며, user_id에 해당하는 사용자를 반환합니다.
    return MyMember.query.get(user_id)

@app.route('/')
def menu():
    return render_template('main.html')


app.register_blueprint(login_bp, url_prefix='/login')
app.register_blueprint(calculator_bp, url_prefix='/calculator')
app.register_blueprint(gugudan_bp, url_prefix='/gugudan')
app.register_blueprint(book_bp, url_prefix='/book')
app.register_blueprint(user_bp, url_prefix='/join')
app.register_blueprint(board_bp, url_prefix='/board')

app.register_blueprint(bookmark_bp, url_prefix='/bookmark', name='unique_bookmark')
app.register_blueprint(homebook_bp, url_prefix='/homebook', name='unique_homebook')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
    

