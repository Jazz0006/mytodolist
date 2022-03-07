from flask import render_template, request, redirect, url_for
from app import app, db
from app.forms import LoginForm
from app.models import Todo

@app.route("/")
@app.route("/index")
def index():
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Todo: login user
        return redirect(url_for('index'))
    return render_template("login.html", form=form)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    

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