
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sqlite3
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
print("API KEY:", os.getenv("OPENAI_API_KEY"))
app = Flask(__name__)
app.secret_key = "career-compass-secret"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DB_PATH = "database/users.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )''')
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message")

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role":"user","content":msg}]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        print("OPENAI ERROR:", e)
        reply = "Error connecting to AI."

    return jsonify({"reply": reply})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    maths = int(data["maths"])
    biology = int(data["biology"])
    commerce = int(data["commerce"])
    coding = int(data["coding"])

    career = "Undecided"
    score = 60

    if coding > 7 and maths > 6:
        career = "Software Engineer"
        score = 86
    elif biology > 7:
        career = "Doctor"
        score = 84
    elif commerce > 7:
        career = "Chartered Accountant"
        score = 80
    else:
        career = "Entrepreneur / Business"

    return jsonify({"career": career, "score": score})

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (user,pwd))
        data = cur.fetchone()
        conn.close()

        if data:
            session["user"] = user
            return redirect("/dashboard")
        else:
            return "Invalid Login"

    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO users(username,password) VALUES(?,?)",(user,pwd))
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html", user=session["user"])

if __name__ == "__main__":
    os.makedirs("database", exist_ok=True)
    init_db()
    app.run(debug=True)
