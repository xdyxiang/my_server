# coding=utf8
from src.app import db


class Pet(db.Model):
    __tablename__ = 'pet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    photoUrls = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), nullable=True)
    task = db.Column(db.String(50), nullable=True)
    category = db.relationship("Category", backref="pet", cascade="all, delete, delete-orphan")  #yong用tablename


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    sx_name = db.Column(db.String(120), nullable=False)
    sx_value = db.Column(db.String(120), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id', ondelete='CASCADE'),
                       nullable=False)

