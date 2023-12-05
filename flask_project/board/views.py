from flask import Blueprint, render_template, request

board_bp = Blueprint('board', __name__)
posts = []
class Post:
    def __init__(self, content):
        self.content = content
    
@board_bp.route('/post1', methods=['POST','GET'])
def create_post():
    if request.method == 'POST':
        content = request.form.get('content', '')
        post = Post(content)
        posts.append(post)
    return render_template('board/board.html', posts=posts)
    
    


