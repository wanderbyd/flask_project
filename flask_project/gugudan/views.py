from flask import Blueprint, render_template, request

gugudan_bp = Blueprint('gugudan', __name__)

@gugudan_bp.route('/', methods=['GET', 'POST'])
def gugudan_home():
    dan = None
    result = None

    if request.method == 'POST':
        dan = int(request.form['dan'])
        result = [(dan, x, dan * x) for x in range(1, 10)]

    return render_template('gugudan/gugudan.html', dan=dan, result=result)