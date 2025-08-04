from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        users = load_users()
        if username in users and users[username] == password:
            return f"✅ Welcome back, {username}!"
        else:
            return "❌ Invalid username or password"
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Server-side validation
        if " " in username:
            return "❌ Username cannot contain spaces"
        if len(password) < 6:
            return "❌ Password must be at least 6 characters"

        users = load_users()
        if username in users:
            return "❌ Username already exists"
        users[username] = password
        save_users(users)
        return redirect(url_for("login"))

    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)
