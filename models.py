from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    algorithm = db.Column(db.String(50))
    step = db.Column(db.Integer)
    n_max = db.Column(db.Integer)
    saved_image = db.Column(db.String(200))