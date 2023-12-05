from flask import Blueprint, render_template, request, session, redirect, url_for,flash
from homebook.models import Homebook
from .homebook_dao import HomebookDAO
from datetime import datetime
from app import app,db
from flask_login import login_required, current_user
from flask_login import LoginManager

homebook_bp = Blueprint('homebook', __name__)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # 유저 로딩 코드: user_id를 기반으로 유저 객체를 반환하는 코드
    # 예를 들어, 데이터베이스에서 유저를 조회하는 코드를 작성합니다.
    pass

@homebook_bp.route('/', methods=['GET', 'POST'])
def homebook_home():
    dao = HomebookDAO()
    homebooks = dao.read_all_data()
    return render_template('homebook/list_homebooks.html', homebooks=homebooks)

@homebook_bp.route('/add_homebook_form', methods=['GET'])
def add_homebook_form():
    return render_template('homebook/add_homebook_form.html')

@homebook_bp.route('/add', methods=['POST'])
def add_homebook():
    if request.method == 'POST':
        #  폼에서 입력받은 날자는 date 형식으로 디비에 저장하기 위해 가공을 한다. 
        transaction_date_str = request.form['transaction_date']
        transaction_date = datetime.strptime(transaction_date_str, '%Y-%m-%d').date()
        # 폼에서 입력받은 데이타를 딕셔너리 가공 
        data = {
            'transaction_date': transaction_date,
            'id': request.form['id'],
            'transaction_type': request.form['transaction_type'],
            'account_subject': request.form['account_subject'],
            'description': request.form['description'],
            'credit': float(request.form['credit']),
            'debit': float(request.form['debit'])
        }

        dao = HomebookDAO()
        dao.record_transaction(**data) # 딕셔너리는 **로 표시하여 보낸다. 
        return redirect(url_for('unique_homebook.homebook_home'))

@homebook_bp.route('/delete', methods=['POST'])
@login_required
def delete_homebook():
    if request.method == 'POST':
        try:
            sn_value = request.form.get('sn')
            if sn_value is not None:
                sn = int(sn_value)
            else:
                print("'sn' 키를 찾을 수 없습니다. 0") 
                return redirect(url_for('unique_homebook.homebook_home'))
        except ValueError:
            print("ValueError: 'sn' 값을 정수로 변환할 수 없습니다.")
            return redirect(url_for('unique_homebook.homebook_home'))

        dao = HomebookDAO()
        homebook = dao.read_data(sn)

        if homebook is not None:
            # Check if the homebook exists before accessing its attributes
            if homebook.id == current_user.id:
                dao.delete_data(sn)
                flash('항목이 삭제되었습니다.', 'success')
            else:
                flash('삭제 권한이 없습니다.', 'danger')
        else:
            flash('삭제할 항목을 찾을 수 없습니다.', 'danger')

        return redirect(url_for('unique_homebook.homebook_home'))



@homebook_bp.route('/update', methods=['POST'])
@login_required
def update_homebook(): 
    if request.method == 'POST':
        try:
            sn_value = request.form.get('sn')
            if sn_value is not None:
                sn = int(sn_value)
            else:
                print("'sn' 키를 찾을 수 없습니다. 0") 
                return redirect(url_for('homebook.homebook_home'))
        except ValueError:
            print("ValueError: 'sn' 값을 정수로 변환할 수 없습니다.")
            return redirect(url_for('unique_homebook.homebook_home'))

        dao = HomebookDAO()
        transaction = dao.read_data(sn)

        # Check if the user has permission to update this record
        if transaction.id == current_user.id:
            return render_template('homebook/update_form.html', transaction=transaction)
        else:
            flash('수정 권한이 없습니다.', 'danger')
            return redirect(url_for('unique_homebook.homebook_home'))

@homebook_bp.route('/update_proc', methods=['POST'])
@login_required
def update_homebook_proc():
    if request.method == 'POST':
        try:
            sn = int(request.form.get('sn'))
        except ValueError:
            print("ValueError: 'sn' 값을 정수로 변환할 수 없습니다.")
            return redirect(url_for('unique_homebook.homebook_home'))

        dao = HomebookDAO()
        transaction = dao.read_data(sn)

        # Check if the user has permission to update this record
        if transaction.id == current_user.id:
            transaction_date_str = request.form['transaction_date']
            transaction_date = datetime.strptime(transaction_date_str, '%Y-%m-%d').date()

            id = request.form['id']
            transaction_type = request.form['transaction_type']
            account_subject = request.form['account_subject']
            description = request.form['description']
            credit = float(request.form['credit'])
            debit = float(request.form['debit'])

            updated_data = (transaction_date, id, transaction_type, account_subject, description, credit, debit)
            dao.update_data(sn, updated_data)
            return redirect(url_for('unique_homebook.homebook_home'))
        else:
            flash('수정 권한이 없습니다.', 'danger')
            return redirect(url_for('unique_homebook.homebook_home'))

# @homebook_bp.route('/delete/<int:sn>', methods=['POST'])
# @login_required
# def delete_homebook(sn):
#     dao = HomebookDAO()
#     homebook = dao.read_data(sn)
#
#     # 홈북이 존재하는지 확인합니다.
#     if homebook is None:
#         flash('삭제할 항목을 찾을 수 없습니다.', 'danger')
#         return redirect(url_for('homebook.homebook_home'))
#
#     # 사용자가 이 홈북을 삭제할 권한이 있는지 확인합니다.
#     if homebook.member_id != current_user.id:
#         flash('삭제 권한이 없습니다.', 'danger')
#     else:
#         dao.delete_data(sn)
#         flash('항목이 삭제되었습니다.', 'success')
#
#     return redirect(url_for('homebook.homebook_home'))
#
#
# @homebook_bp.route('/update/<int:sn>', methods=['POST'])
# @login_required
# def update_homebook(sn):
#     dao = HomebookDAO()
#     homebook = dao.read_data(sn)
#
#     # 홈북이 존재하는지 확인합니다.
#     if homebook is None:
#         flash('수정할 항목을 찾을 수 없습니다.', 'danger')
#         return redirect(url_for('homebook.homebook_home'))
#
#     # 사용자가 이 홈북을 수정할 권한이 있는지 확인합니다.
#     if homebook.member_id != current_user.id:
#         flash('수정 권한이 없습니다.', 'danger')
#         return redirect(url_for('homebook.homebook_home'))
#
#     return render_template('homebook/update_form.html', homebook=homebook)
#
#
# @homebook_bp.route('/update_proc/<int:sn>', methods=['POST'])
# @login_required
# def update_homebook_proc(sn):
#     dao = HomebookDAO()
#     homebook = dao.read_data(sn)
#
#     # 홈북이 존재하는지 확인합니다.
#     if homebook is None:
#         flash('수정할 항목을 찾을 수 없습니다.', 'danger')
#         return redirect(url_for('homebook.homebook_home'))
#
#     # 사용자가 이 홈북을 수정할 권한이 있는지 확인합니다.
#     if homebook.member_id != current_user.id:
#         flash('수정 권한이 없습니다.', 'danger')
#         return redirect(url_for('homebook.homebook_home'))
#
#     try:
#         # 업데이트 로직을 처리합니다.
#         transaction_date_str = request.form['transaction_date']
#         transaction_date = datetime.strptime(transaction_date_str, '%Y-%m-%d').date()
#
#         id = request.form['id']
#         transaction_type = request.form['transaction_type']
#         account_subject = request.form['account_subject']
#         description = request.form['description']
#         credit = float(request.form['credit'])
#         debit = float(request.form['debit'])
#
#         updated_data = (transaction_date, id, transaction_type, account_subject, description, credit, debit)
#         dao.update_data(sn, updated_data)
#
#         flash('홈북이 성공적으로 업데이트되었습니다.', 'success')
#     except Exception as e:
#         flash('홈북 업데이트 중 오류가 발생했습니다: {}'.format(str(e)), 'danger')
#
#     return redirect(url_for('homebook.homebook_home'))


# @homebook_bp.route('/update', methods=['POST'])
# def update_homebook(): # 업데이트 하기지전 폼 및 기존 데이터 표시 작업 
#     if request.method == 'POST':
#         try:
#             sn_value = request.form.get('sn') # 시리얼번호가 아직은 숫자 모양의 문자인 상태 
#             if sn_value is not None: # 시리얼번호가 제대로 넘어왔다면
#                 sn = int(sn_value) # 문자모양을 숫자로 바꿔 준다
#             else:
#                 print("'sn' 키를 찾을 수 없습니다. 0") 
#                 return redirect(url_for('homebook.homebook_home'))
#         except ValueError: # 순수 숫자 타입이 아니고 혹 문자타입이 섞여 있다면 예외발생 
#             print("ValueError: 'sn' 값을 정수로 변환할 수 없습니다.")
#             return redirect(url_for('unique_homebook.homebook_home'))
#
#         dao = HomebookDAO()
#         transaction = dao.read_data(sn)  # 'homebook' 대신 'transaction'으로 변수 이름 변경
#         print("************************* 1")
#         return render_template('homebook/update_form.html', transaction=transaction)  # 변수 이름도 'transaction'으로 변경
#
# @homebook_bp.route('/update_proc', methods=['POST'])
# def update_homebook_proc(): # 실제 데이타를 디비에 수정하는 작업 
#     if request.method == 'POST':
#         try:
#             sn = int(request.form.get('sn'))
#         except ValueError:
#             print("ValueError: 'sn' 값을 정수로 변환할 수 없습니다.")
#             return redirect(url_for('unique_homebook.homebook_home'))
#
#         dao = HomebookDAO()
#         # 수정전 데이타를 모두 읽어 옴 : 여기서는 필요없는 작업이지만 필요할 경우가 많음 
#         transaction = dao.read_data(sn)
#
#         # 'transaction_date'를 Python date 객체로 변환
#         transaction_date_str = request.form['transaction_date']
#         transaction_date = datetime.strptime(transaction_date_str, '%Y-%m-%d').date()
#
#         id = request.form['id']
#         transaction_type = request.form['transaction_type']
#         account_subject = request.form['account_subject']
#         description = request.form['description']
#         credit = float(request.form['credit'])
#         debit = float(request.form['debit'])
#         # 수정할 데이타를 튜플로 만듦 
#         updated_data = (transaction_date, id, transaction_type, account_subject, description, credit, debit)
#         # 실제 수정 작업 
#         dao.update_data(sn, updated_data)
#         return redirect(url_for('unique_homebook.homebook_home'))









# from flask import Blueprint, render_template, request, session, redirect, url_for
# from .models import Homebook
# from .homebook_dao import HomebookDAO
# from datetime import datetime
# # 여기에 먼저 만들어 져 있어야 run.py 등에서 app에 불루프린트를 등록한다.
# homebook_bp = Blueprint('homebook', __name__)
#
# @homebook_bp.route('/', methods=['GET', 'POST'])
# def homebook_home():
#     dao = HomebookDAO()
#     homebooks = dao.read_all_data()
#     return render_template('homebook/list_homebooks.html', homebooks=homebooks)
#
# @homebook_bp.route('/add_homebook_form', methods=['GET'])
# def add_homebook_form():
#     return render_template('homebook/add_homebook_form.html')
#
# @homebook_bp.route('/add', methods=['POST'])
# def add_homebook():
#     if request.method == 'POST':
#         #  폼에서 입력받은 날자는 date 형식으로 디비에 저장하기 위해 가공을 한다. 
#         transaction_date_str = request.form['transaction_date']
#         transaction_date = datetime.strptime(transaction_date_str, '%Y-%m-%d').date()
#         # 폼에서 입력받은 데이타를 딕셔너리 가공 
#         data = {
#             'transaction_date': transaction_date,
#             'member_id': request.form['member_id'],
#             'transaction_type': request.form['transaction_type'],
#             'account_subject': request.form['account_subject'],
#             'description': request.form['description'],
#             'credit': float(request.form['credit']),
#             'debit': float(request.form['debit'])
#         }
#
#         dao = HomebookDAO()
#         dao.record_transaction(**data) # 딕셔너리는 **로 표시하여 보낸다. 
#         return redirect(url_for('homebook.homebook_home'))
#
# @homebook_bp.route('/delete', methods=['POST'])
# def delete_homebook():
#     if request.method == 'POST':
#         try:
#             sn_value = request.form.get('sn')
#             if sn_value is not None:
#                 sn = int(sn_value)
#             else:
#                 print("'sn' 키를 찾을 수 없습니다. 0") 
#                 return redirect(url_for('homebook.homebook_home'))
#         except ValueError:
#             print("ValueError: 'sn' 값을 정수로 변환할 수 없습니다.")
#             return redirect(url_for('homebook.homebook_home'))
#
#         dao = HomebookDAO()
#         dao.delete_data(sn)
#         return redirect(url_for('homebook.homebook_home'))
#
# @homebook_bp.route('/update', methods=['POST'])
# def update_homebook(): # 업데이트 하기지전 폼 및 기존 데이터 표시 작업 
#     if request.method == 'POST':
#         try:
#             sn_value = request.form.get('sn') # 시리얼번호가 아직은 숫자 모양의 문자인 상태 
#             if sn_value is not None: # 시리얼번호가 제대로 넘어왔다면
#                 sn = int(sn_value) # 문자모양을 숫자로 바꿔 준다
#             else:
#                 print("'sn' 키를 찾을 수 없습니다. 0") 
#                 return redirect(url_for('homebook.homebook_home'))
#         except ValueError: # 순수 숫자 타입이 아니고 혹 문자타입이 섞여 있다면 예외발생 
#             print("ValueError: 'sn' 값을 정수로 변환할 수 없습니다.")
#             return redirect(url_for('homebook.homebook_home'))
#
#         dao = HomebookDAO()
#         transaction = dao.read_data(sn)  # 'homebook' 대신 'transaction'으로 변수 이름 변경
#         print("************************* 1")
#         return render_template('homebook/update_form.html', transaction=transaction)  # 변수 이름도 'transaction'으로 변경
#
# @homebook_bp.route('/update_proc', methods=['POST'])
# def update_homebook_proc(): # 실제 데이타를 디비에 수정하는 작업 
#     if request.method == 'POST':
#         try:
#             sn = int(request.form.get('sn'))
#         except ValueError:
#             print("ValueError: 'sn' 값을 정수로 변환할 수 없습니다.")
#             return redirect(url_for('homebook.homebook_home'))
#
#         dao = HomebookDAO()
#         # 수정전 데이타를 모두 읽어 옴 : 여기서는 필요없는 작업이지만 필요할 경우가 많음 
#         transaction = dao.read_data(sn)
#
#         # 'transaction_date'를 Python date 객체로 변환
#         transaction_date_str = request.form['transaction_date']
#         transaction_date = datetime.strptime(transaction_date_str, '%Y-%m-%d').date()
#
#         member_id = request.form['member_id']
#         transaction_type = request.form['transaction_type']
#         account_subject = request.form['account_subject']
#         description = request.form['description']
#         credit = float(request.form['credit'])
#         debit = float(request.form['debit'])
#         # 수정할 데이타를 튜플로 만듦 
#         updated_data = (transaction_date, member_id, transaction_type, account_subject, description, credit, debit)
#         # 실제 수정 작업 
#         dao.update_data(sn, updated_data)
#         return redirect(url_for('homebook.homebook_home'))













