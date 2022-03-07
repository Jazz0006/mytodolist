from flask_login import UserMixin

class User(UserMixin, db.Model):
    pass


from app import login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))