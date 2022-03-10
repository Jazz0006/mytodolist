from flask import render_template, request, redirect, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import Todo, User
from flask_login import current_user, login_required, login_user, logout_user
from datetime import date, datetime

@app.route("/")
@app.route("/index")
def show_user_list():
    if current_user.is_authenticated:
        date_of_today = date.today()
        display_today = date_of_today.strftime("%b %d, %A")
        today_todo = Todo.query.filter(
            Todo.owner==current_user, Todo.complete==False, Todo.due_day==date_of_today)
        today_done = Todo.query.filter(
            Todo.owner==current_user, Todo.complete==True, Todo.due_day==date_of_today)
        future_todo = Todo.query.filter(
            Todo.owner==current_user, Todo.complete==False, Todo.due_day>date_of_today)
        page_date = {
            'today' : display_today,
            'todo_list' : today_todo,
            'done_list' : today_done,
            'future_todo' : future_todo
        }
        return render_template("user.html", page_date=page_date)
    else:
        return redirect(url_for('login'))
    

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('show_user_list'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('show_user_list'))
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('show_user_list'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('show_user_list'))
    return render_template("signup.html", form=form)

    

@app.route("/about")
def about():
    return "Site designed by Jazz"

@app.route("/add", methods=["POST"])
@login_required
def add():
    title = request.form.get("title")
    due_date = date.today()
    new_todo = Todo(title=title, complete=False, owner=current_user, due_day=due_date)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("show_user_list"))

@app.route("/add_future", methods=["POST"])
@login_required
def addfuture():
    title = request.form.get("title")
    form_due_date = request.form.get("due_day")
    due_date = datetime.strptime(form_due_date, "%Y-%m-%d").date()
    new_todo = Todo(title=title, complete=False, owner=current_user, due_day=due_date)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("show_user_list"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("show_user_list"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("show_user_list"))