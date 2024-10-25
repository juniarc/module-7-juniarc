from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required
from models.users.users import UserModel
from models.review.reviews import ReviewModel
from connectors.db import Session, Base, engine
from controllers.users_controller.users_controller import usersBp
from controllers.review_controller.reviews_controller import reviewBp
import os

Base.metadata.create_all(engine)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(usersBp)
app.register_blueprint(reviewBp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/unauthorized')
def unauthorized():
    return render_template('unauthorized.html')

@app.route('/home')
@login_required
def home():
    try:
        with Session() as session:
            reviews = session.query(ReviewModel).all()
            return render_template('home.html', reviews=reviews)
    except Exception as e:
        print(e)
        return(e)

@login_manager.user_loader
def load_user(user_id):
    try:
        with Session() as session:
            return session.query(UserModel).get(int(user_id))
    except Exception as e:
        print(e)
        return
    
@login_manager.unauthorized_handler
def handle_unauthorized():
    return redirect(url_for('unauthorized'))