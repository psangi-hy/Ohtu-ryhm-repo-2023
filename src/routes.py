from src.app import app
from src.AppLibrary import AppLibrary
from flask import render_template, request, redirect, session
import src.sources as sources
import src.users as users

@app.route("/")
def index():
    if session.get("user_id"):
        result = sources.get_all_articles()
        return render_template("index.html", articles=result)
    else:
        return redirect('/login')
    
@app.route("/add_article", methods=["GET", "POST"])
def add_article():
    if request.method == "GET":
        return render_template("add_article.html")

    if request.method == "POST":
        sources.add_article(
            request.form["author"],
            request.form["title"],
            request.form["journal"],
            request.form["year"],
            request.form["volume"],
            request.form["number"],
            request.form["pages"]
            )
        return redirect("/")
   
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        # if user already logged in then redirect
        if session.get("user_id"):
            return redirect("/")
        else:
            return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            # users.py sets session["user_id"]
            return redirect("/")
        else:
            return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        # if user already logged in then redirectd
        if session.get("user_id"):
            return redirect("/")
        else:
            return render_template("sign_in.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username, password):
            return redirect("/")
        else:
            return redirect("/register")
        
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/login")

#These are only for testing the database functions before ui:
@app.route("/db_write_test")
def db_write_test():
    session["user_id"] = 1
    result = sources.add_book("Herra Huu", "Keittokirja", "Kustannus Oy", "osoite ", 2022)
    print("routes.py / db_write_test: result = ", str(result))
    return ("Hello db_write_test!!")

@app.route("/db_read_test")
def db_read_test():
    session["user_id"] = 1
    data = sources.get_all_books()
    print("routes.py / db_read_test: data = ", data)
    return ("Hello db_read_test!! <p>Sources: <p>" + str(data))

@app.route("/db_delete_test")
def db_delete_test():
    session["user_id"] = 1
    result = sources.delete_source("books", 7)
    print("routes.py / db_delete_test: result = ", result)
    return ("Hello db_delete_test!! <p>result: <p>" + str(result))

@app.route("/db_get_all_test")
def db_get_all_test():
    session["user_id"] = 1
    data = sources.get_all("books", 7)
    print("routes.py / db_get_all_test: data = ", data)
    return ("Hello db_get_all_test!! <p>data: <p>" + str(data))

@app.route("/db_initialize")
def db_initialize():
    AppLibrary.setup(AppLibrary)
    data = users.get_users()
    print("All users: ")
    print(data)
    return "Database should now be initialized\n"
