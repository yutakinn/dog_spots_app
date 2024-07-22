import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Spot, User
from forms import SpotForm, LoginForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# データベースのパスを環境変数から取得
db_path = os.environ.get('DATABASE_URL')
if db_path.startswith("sqlite:///"):
    db_dir = os.path.dirname(db_path.replace("sqlite:///", ""))
    os.makedirs(db_dir, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = db_path

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

def create_tables():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin_password = os.environ.get('ADMIN_PASSWORD', 'default_password')
            admin_user = User(username='admin', password_hash=generate_password_hash(admin_password))
            db.session.add(admin_user)
            db.session.commit()

# アプリケーション初期化時にテーブルを作成
create_tables()

if __name__ == '__main__':
    app.run(debug=False)
