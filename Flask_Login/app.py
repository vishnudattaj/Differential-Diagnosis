from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import flask_login
import joblib
from werkzeug.security import generate_password_hash, check_password_hash
import json
import datetime

app = Flask(__name__)
app.config['RECAPTCHA_S8ITE_KEY'] = '6LcYcEohAAAAANVL5nwJ25oOM488BPaC9bujC-94'
app.secret_key = '6LcYcEohAAAAAJ5JeDLnVKReHLj0ZIkeo7FgilZB'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
db = SQLAlchemy(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class LoginScreen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usernames = db.Column(db.String(100), unique=True, nullable=False)
    passwords = db.Column(db.String(200), nullable=False)
    disease_history = db.Column(db.Text)

    def set_data(self, data):
        self.disease_history = json.dumps(data)

    def get_data(self):
        if not self.data:
            return {}
        return json.loads(self.disease_history)

today = datetime.datetime.now().strftime("%x")

class User(flask_login.UserMixin):
    pass

xgb = joblib.load(filename="Flask_Login/randomForestModel.joblib")

@login_manager.user_loader
def user_loader(username):
    if username not in username:
        return

    user = User()
    user.id = username
    return user

with app.app_context():
    db.create_all()
    db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_entry = LoginScreen.query.filter_by(usernames=username).first()

        if user_entry and check_password_hash(user_entry.passwords, password):
            user = User()
            user.id = username
            flask_login.login_user(user)
            return redirect(url_for('home'))
        return render_template('wrongCredentials.html')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirmpassword']

        if password != confirm:
            return render_template('confirmPassword.html')

        if LoginScreen.query.filter_by(usernames=username).first():
            return render_template('existingUser.html')

        hashed_pw = generate_password_hash(password)
        new_user = LoginScreen(usernames=username, passwords=hashed_pw)

        db.session.add(new_user)
        db.session.commit()

        user = User()
        user.id = username
        flask_login.login_user(user)
        return redirect(url_for('protected'))

    return render_template('signup.html')

@app.route('/submit', methods=['POST'])
def submit_symptoms():
    if not flask_login.current_user.is_authenticated:
        return jsonify({"error": "User not authenticated"}), 401

    try:
        data = request.get_json()
        symptoms = data.get('symptoms', [])
        
        # Get current user
        user_id = session['user_id']
        
        # Create new symptom entry
        submission = SymptomSubmission(
            symptoms=", ".join(symptoms),
            user_id=user_id
        )
        db.session.add(submission)
        db.session.commit()
        
        return jsonify({
            "message": "Symptoms stored successfully",
            "diagnosis": get_diagnosis(symptoms)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/home')
def home():
    return render_template('homepage.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Explicitly set port