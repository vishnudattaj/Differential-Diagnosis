from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import flask_login

app = Flask(__name__)
app.config['RECAPTCHA_SITE_KEY'] = '6LcYcEohAAAAANVL5nwJ25oOM488BPaC9bujC-94'
app.secret_key = '6LcYcEohAAAAAJ5JeDLnVKReHLj0ZIkeo7FgilZB'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
db = SQLAlchemy(app)

login_manager = flask_login.LoginManager()

login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass


class LoginScreen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usernames = db.Column(db.String(100), nullable=False)
    passwords = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return 'User ' + str(self.id)


db.create_all()
db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if bool(LoginScreen.query.filter_by(usernames=username).first()):
            id_checker = LoginScreen.query.filter_by(usernames=username).first()
            id_checker = id_checker.id
            id_tester = LoginScreen.query.get(id_checker).passwords
            if password == id_tester:
                user = User()
                user.id = username
                flask_login.login_user(user)
                return redirect(url_for('protected'))

            else:
                return render_template('wrongCredentials.html')
        else:
            return render_template('wrongCredentials.html')
    else:
        return render_template('login.html')


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401


@login_manager.user_loader
def user_loader(username):
    if username not in username:
        return

    user = User()
    user.id = username
    return user


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirmpassword']
        
        if (password == confirm):
            signin = LoginScreen(usernames=username, passwords=password)
            if bool(LoginScreen.query.filter_by(usernames=username).first()):
                return render_template('existingUser.html')
            else:
                db.session.add(signin)
                db.session.commit()
                id_checker = LoginScreen.query.filter_by(usernames=username).first()
                id_checker = id_checker.id
                user = User()
                user.id = username
                flask_login.login_user(user)
                return redirect(url_for('protected'))
        else:
            return render_template('confirmPassword.html')
        

    else:
        return render_template('signup.html')

@app.route('/protected', methods=['GET', 'POST'])
@flask_login.login_required
def protected():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == "symptomSubmit":
            symptoms = request.form['symptoms'] if request.form['symptoms'] != '' else None
            diabetes = 'diabetes' if request.form.get('diabetes') else None
            hypertension = 'hypertension' if request.form.get('hypertension') else None
            asthma = 'asthma' if request.form.get('asthma') else None
            terms = 'terms' if request.form.get('terms') else None

            if not terms: 
                return "Terms must be accepted",400
            
            data = {
                'symptoms': symptoms,
                'diabetes': diabetes,
                'hypertension': hypertension,
                'asthma': asthma
            }

            print(data)

            return render_template('homepage.html', save=flask_login.current_user.id)
        
        if action == "logOut":
            return redirect(url_for('logout'))
    else:
        return render_template('homepage.html', save=flask_login.current_user.id)
    
if __name__ == "__main__":
    app.run(debug=False)

#bro what the fuck is going on i have no idea what I'm doing
class SymptomEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)  # Store the username (or a user ID)
    symptoms = db.Column(db.String(500), nullable=False)
    diabetes = db.Column(db.Boolean, default=False)
    hypertension = db.Column(db.Boolean, default=False)
    asthma = db.Column(db.Boolean, default=False)


with app.app_context():
    db.create_all()

@app.route('/protected', methods=['GET', 'POST'])
@flask_login.login_required
def protected():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == "symptomSubmit":
            symptoms = request.form['symptoms'] if request.form['symptoms'] else None
            diabetes = bool(request.form.get('diabetes'))
            hypertension = bool(request.form.get('hypertension'))
            asthma = bool(request.form.get('asthma'))
            terms = request.form.get('terms')

            if not terms:
                return "Terms must be accepted", 400

            new_entry = SymptomEntry(
                user_id=flask_login.current_user.id,
                symptoms=symptoms,
                diabetes=diabetes,
                hypertension=hypertension,
                asthma=asthma
            )
            db.session.add(new_entry)
            db.session.commit()

            return render_template('homepage.html', save=flask_login.current_user.id)

        if action == "logOut":
            return redirect(url_for('logout'))

    return render_template('homepage.html', save=flask_login.current_user.id)
[]
