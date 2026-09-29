from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Analysis(db.Model):
    __tablename__ = "analytics"
    id = db.Column(db.Integer, primary_key=True)
    algorithm = db.Column("algo", db.String(255))
    step = db.Column("steps", db.Integer)
    n_max = db.Column(db.Integer)
    image = db.Column(db.LargeBinary(length=16_777_215))

class User(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(80), unique=True, nullable=False)
     password_hash = db.Column(db.String(256), nullable=False)

     def set_password(self, password):
        self.password_hash = generate_password_hash(password)

     def check_password(self, password):
       return check_password_hash(self.password_hash, password)