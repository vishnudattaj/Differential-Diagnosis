from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
login_manager = flask_login.LoginManager()

class LoginScreen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usernames = db.Column(db.String(100), unique=True, nullable=False)
    passwords = db.Column(db.String(200), nullable=False)

class MedicalInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symptoms = db.Column(db.String(500))
    diabetes = db.Column(db.Boolean, default=False)
    hypertension = db.Column(db.Boolean, default=False)
    asthma = db.Column(db.Boolean, default=False)
    terms_accepted = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('login_screen.id'), nullable=False)
    user = db.relationship('LoginScreen', backref=db.backref('medical_info', lazy=True))

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    user_entry = LoginScreen.query.filter_by(usernames=user_id).first()
    if user_entry:
        user = User()
        user.id = user_entry.usernames
        return user
    return None

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

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
                return redirect(url_for('protected'))
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

    @app.route('/protected', methods=['GET', 'POST'])
    @flask_login.login_required
    def protected():
        if request.method == 'POST':
            action = request.form.get('action')
            
            if action == "symptomSubmit":
                if not request.form.get('terms'):
                    return "Terms must be accepted", 400
                    
                current_user = LoginScreen.query.filter_by(
                    usernames=flask_login.current_user.id
                ).first()
                
                medical_entry = MedicalInfo(
                    symptoms=request.form.get('symptoms'),
                    diabetes='diabetes' in request.form,
                    hypertension='hypertension' in request.form,
                    asthma='asthma' in request.form,
                    terms_accepted=True,
                    user_id=current_user.id
                )
                
                db.session.add(medical_entry)
                db.session.commit()
                
                return render_template('homepage.html', save=current_user.usernames)
                
            elif action == "logOut":
                return redirect(url_for('logout'))
        
        return render_template('homepage.html', save=flask_login.current_user.id)

    @app.route('/logout')
    def logout():
        flask_login.logout_user()
        return 'Logged out'

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)  # Explicitly set port