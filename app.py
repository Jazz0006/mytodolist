from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

from forms import LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "temperory_Secret_key"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

@app.route("/")
def index():
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)

@app.route("/login")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template("login.html", form=form)

@app.route("/about")
def about():
    return "Site designed by Jazz"

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    # db.create_all()

    # new_todo = Todo(title="First thing", complete=False)
    # db.session.add(new_todo)
    # db.session.commit()

    app.run(debug=True)