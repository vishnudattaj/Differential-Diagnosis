from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import flask_login
import joblib
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import pandas as pd

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


class SymptomSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symptoms = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('login_screen.id'), nullable=False)



class User(flask_login.UserMixin):
    pass

xgb = joblib.load(filename="../randomForestModel.joblib")

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

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        symptoms = []
        i = 1
        while f'symptom{i}' in request.form:
            symptoms.append(request.form[f'symptom{i}'])
            i += 1
        
        trainingdf = pd.read_csv("Testing.csv")
        column_names = trainingdf.columns.tolist()
        userSymptoms = pd.DataFrame(0, index=[0], columns=column_names)
        userSymptoms.drop(columns=["Disease"], inplace=True)

        for column in column_names:
            if column in symptoms:
                userSymptoms.loc[0, column] = 1
        
        disease_prediction = xgb.predict(userSymptoms)
        print("Predicted disease:", disease_prediction[0])
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