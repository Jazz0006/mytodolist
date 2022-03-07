from datetime import date
from app import db

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    due_day = db.Column(db.DateTime, default=date.today)

    def __repr__(self):
        return f'<Task {self.title}'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    task = db.relationship('Todo', backref='owner', lazy='dynamic')

    def __repr__(self):
        return f'<user {self.email}'