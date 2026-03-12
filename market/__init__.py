from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page"
login_manager.login_message = "Morate biti prijavljeni da biste kupovali."
login_manager.login_message_category = "warning"

from market.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from market import routes

from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()

    admin = User.query.filter_by(username="admin").first()

    if not admin:
        admin = User(
            username="admin",
            email_address="admin@gmail.com",
            password_hash=generate_password_hash("admin123"),
            budget=10000,
            total_spent=0,
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
 


