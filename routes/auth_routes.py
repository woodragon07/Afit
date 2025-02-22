# routes/auth_routes.py 인증(로그인, 회원가입, 로그아웃) 관련 라우트를 담당
from flask import Blueprint, render_template, request, redirect, url_for, session
from database import User
from extensions import mongo

bp = Blueprint('auth', __name__)

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_data = mongo.db.users.find_one({"username": username})
        if not user_data:
            return render_template("KO/login.html", username_error="존재하지 않는 아이디입니다.")
        user = User.from_dict(user_data)
        if not user.check_password(password):
            return render_template("KO/login.html", password_error="비밀번호가 올바르지 않습니다.")
        session.permanent = True
        session['user'] = {
            'id': user.id,
            'name': user.name,
            'username': user.username
        }
        # 로그인 성공 후 랜딩 페이지(예: product_routes의 landing)로 이동
        return redirect(url_for('product.landing'))
    return render_template("KO/login.html")

@bp.route("/login_EN", methods=['GET', 'POST'])
def login_EN():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # SQLAlchemy 방식 예시 – 실제 DB 접근 방식에 맞게 수정하세요.
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session.permanent = True
            session['user'] = {
                'id': user.id,
                'name': user.name,
                'username': user.username
            }
            return redirect(url_for('product.english'))
        else:
            return "Login failed", 401
    return render_template("EN/login_EN.html")

@bp.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            password_confirm = request.form.get('password_confirm')
            email = request.form.get('email')
            name = request.form.get('name')
            phone = request.form.get('phone')
<<<<<<< HEAD
=======
            gender = request.form.get('gender')
            region = request.form.get('region')
            age = request.form.get('age')
>>>>>>> 8592ca44a16150c7cbfcb58f7ebb14d6ca4741ff

            if password != password_confirm:
                return render_template("KO/signup.html", 
                    password_confirm_error="비밀번호가 일치하지 않습니다.",
<<<<<<< HEAD
                    username=username, email=email, name=name, phone=phone
=======
                    username=username, email=email, name=name, phone=phone, gender=gender, region=region, age=age
>>>>>>> 8592ca44a16150c7cbfcb58f7ebb14d6ca4741ff
                )
            if mongo.db.users.find_one({"username": username}):
                return render_template("KO/signup.html", 
                    username_error="이미 존재하는 아이디입니다.",
<<<<<<< HEAD
                    email=email, name=name, phone=phone
=======
                    email=email, name=name, phone=phone, gender=gender, region=region, age=age
>>>>>>> 8592ca44a16150c7cbfcb58f7ebb14d6ca4741ff
                )
            if mongo.db.users.find_one({"email": email}):
                return render_template("KO/signup.html", 
                    email_error="이미 존재하는 이메일입니다.",
<<<<<<< HEAD
                    username=username, name=name, phone=phone
                )
            if not all([username, password, email, name, phone]):
                return render_template("KO/signup.html", error="모든 필드를 입력해주세요.")

            new_user = User(username, email, name, phone)
=======
                    username=username, name=name, phone=phone, gender=gender, region=region, age=age
                )
            if not all([username, password, email, name, phone, gender, region, age]):
                return render_template("KO/signup.html", error="모든 필드를 입력해주세요.")

            new_user = User(username, email, name, phone, gender, region, age)
>>>>>>> 8592ca44a16150c7cbfcb58f7ebb14d6ca4741ff
            new_user.set_password(password)
            insert_result = mongo.db.users.insert_one(new_user.to_dict())
            if insert_result.inserted_id:
                return redirect(url_for('auth.login'))
            else:
                return render_template("KO/signup.html", error="회원가입 중 문제가 발생했습니다.")
        except Exception as e:
            return render_template("KO/signup.html", error=f"회원가입 실패: {str(e)}")
    return render_template("KO/signup.html")

@bp.route("/signup_EN", methods=['GET', 'POST'])
def signup_EN():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            password_confirm = request.form.get('password_confirm')
            email = request.form.get('email')
            name = request.form.get('name')
            phone = request.form.get('phone')
<<<<<<< HEAD
=======
            gender = request.form.get('gender')
            region = request.form.get('region')
            age = request.form.get('age')
>>>>>>> 8592ca44a16150c7cbfcb58f7ebb14d6ca4741ff

            if password != password_confirm:
                return render_template("EN/signup_EN.html", 
                    password_confirm_error="Passwords do not match.",
<<<<<<< HEAD
                    username=username, email=email, name=name, phone=phone
=======
                    username=username, email=email, name=name, phone=phone, gender=gender, region=region, age=age
>>>>>>> 8592ca44a16150c7cbfcb58f7ebb14d6ca4741ff
                )
            if mongo.db.users.find_one({"username": username}):
                return render_template("EN/signup_EN.html", 
                    username_error="Username already exists.",
<<<<<<< HEAD
                    email=email, name=name, phone=phone
=======
                    email=email, name=name, phone=phone, gender=gender, region=region, age=age
>>>>>>> 8592ca44a16150c7cbfcb58f7ebb14d6ca4741ff
                )
            if mongo.db.users.find_one({"email": email}):
                return render_template("EN/signup_EN.html", 
                    email_error="Email already exists.",
<<<<<<< HEAD
                    username=username, name=name, phone=phone
                )
            if all([username, password, email, name, phone]):
                new_user = User(username, email, name, phone)
=======
                    username=username, name=name, phone=phone, gender=gender, region=region, age=age
                )
            if all([username, password, email, name, phone, gender, region, age]):
                new_user = User(username, email, name, phone, gender, region, age)
>>>>>>> 8592ca44a16150c7cbfcb58f7ebb14d6ca4741ff
                new_user.set_password(password)
                mongo.db.users.insert_one(new_user.to_dict())
                return redirect(url_for('auth.login_EN'))
            else:
                return render_template("EN/signup_EN.html", error="Please fill in all fields.")
        except Exception as e:
            return render_template("EN/signup_EN.html", error=f"Signup failed: {str(e)}")
    return render_template("EN/signup_EN.html")

@bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('product.landing'))

@bp.route('/logout_EN')
def logout_EN():
    session.pop('user', None)
    return redirect(url_for('product.english'))
