from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Spot, User
from forms import SpotForm, LoginForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    spots = Spot.query.all()
    return render_template('index.html', spots=spots)

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_add_spot'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('admin_add_spot'))
        flash('Invalid username or password')
    return render_template('admin/login.html', form=form)

@app.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin/add_spot', methods=['GET', 'POST'])
@login_required
def admin_add_spot():
    form = SpotForm()
    if form.validate_on_submit():
        new_spot = Spot(
            name=form.name.data,
            description=form.description.data,
            address=form.address.data,
            dog_friendly_rating=form.dog_friendly_rating.data
        )
        db.session.add(new_spot)
        db.session.commit()
        flash('New spot added successfully!')
        return redirect(url_for('index'))
    return render_template('admin/add_spot.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # 初期管理者ユーザーの作成（実際の運用では安全なパスワード管理を行ってください）
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', password_hash=generate_password_hash('password'))
            db.session.add(admin_user)
            db.session.commit()
    app.run(debug=True)