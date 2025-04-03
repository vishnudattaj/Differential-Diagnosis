from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
import flask_login
import joblib
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import pandas as pd
import os

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

# Load the machine learning model and encoder
model_path = os.path.join(os.path.dirname(__file__), "xgboostModel.joblib")
encoder_path = os.path.join(os.path.dirname(__file__), "label_encoder.joblib")
xgb = joblib.load(model_path)
encoder = joblib.load(encoder_path)

# Load the column names from the dataset
csv_path = os.path.join(os.path.dirname(__file__), "Testing.csv")
trainingdf = pd.read_csv(csv_path)
column_names = trainingdf.columns.tolist()
column_names.remove("Disease")  # Remove the "Disease" column

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
        return redirect(url_for('home'))  # Redirect to 'home'

    return render_template('signup.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        symptoms = []
        i = 1
        while f'symptom{i}' in request.form:
            symptoms.append(request.form[f'symptom{i}'])
            i += 1
        
        # Construct the correct path for Testing.csv
        csv_path = os.path.join(os.path.dirname(__file__), "Testing.csv")
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found at {csv_path}")
        
        trainingdf = pd.read_csv(csv_path)
        column_names = trainingdf.columns.tolist()
        userSymptoms = pd.DataFrame(0, index=[0], columns=column_names)
        userSymptoms.drop(columns=["Disease"], inplace=True)

        for column in column_names:
            if column in symptoms:
                userSymptoms.loc[0, column] = 1
        
        predicted_encoded = xgb.predict(userSymptoms)
        predicted_diseases = encoder.inverse_transform(predicted_encoded)
        print(predicted_diseases)
        return render_template('homepage.html')
    else:
        return render_template('homepage.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    symptoms = data.get("symptoms", [])

    # Create a DataFrame for the user's symptoms
    userSymptoms = pd.DataFrame(0, index=[0], columns=column_names)
    for symptom in symptoms:
        if symptom in column_names:
            userSymptoms.loc[0, symptom] = 1

    # Predict the disease
    predicted_encoded = xgb.predict(userSymptoms)
    predicted_disease = encoder.inverse_transform(predicted_encoded)[0]

    # Return the predicted disease as a JSON response
    return jsonify({"predicted_disease": predicted_disease})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)  # Explicitly set port

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


