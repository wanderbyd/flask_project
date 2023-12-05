from flask import Blueprint, render_template, request
# Blueprint는 Flask에서 제공하는 클래스로, 애플리케이션 내에서 라우트, 
# 템플릿 및 정적 파일을 재사용 가능한 구성 요소로 구성하고 그룹화하는 데 사용됨.
# 'calculator'은 이 블루프린트에 부여하는 이름, 이 문자열은 이 특정 블루프린트를 식별하는 데 사용
# 나중에 이 블루프린트와 관련된 경로를 등록할 때 이 이름을 사용
# 이 문맥에서 __name__을 사용하면 Flask가 이 블루프린트와 관련된 템플릿 및 
# 정적 파일의 루트 경로를 결정할 수 있음 
calculator_bp = Blueprint('calculator', __name__)

@calculator_bp.route('/calculate', methods=['POST'])
def calculate():
    expression = request.form['expression']
    try:
        result = eval(expression)
        # 천 단위로 쉼표 추가
        formatted_result = '{:,}'.format(result)  
        return render_template('calculator/calculator.html', result=formatted_result, expression=expression)
    except Exception:
        return render_template('calculator/calculator.html', error=True, expression=expression)

@calculator_bp.route('/')
def calculator_home():
    return render_template('calculator/calculator.html')
 