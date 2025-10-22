from flask_login import UserMixin
from .connectors import db

class Chemist(UserMixin, db.Model):
    __tablename__ = "chemists"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password = db.Column(db.String(150), nullable=False)
    
    # Relationship to Water_sample
    water_samples = db.relationship("Water_sample", backref="chemist", lazy=True)


class Water_sample(db.Model):
    __tablename__ = "water_samples"
    id = db.Column(db.Integer, primary_key=True)
    ph = db.Column(db.Float, nullable=False)
    hardness = db.Column(db.Float, nullable=False)
    chloramines = db.Column(db.Float, nullable=False)
    sulfate = db.Column(db.Float, nullable=False)
    organic_carbon = db.Column(db.Float, nullable=False)
    trihalomethanes = db.Column(db.Float, nullable=False)
    
    # Foreign key to chemist
    chemist_id = db.Column(db.Integer, db.ForeignKey('chemists.id'), nullable=False)
