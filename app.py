from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv() 
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-this-secret-key")

app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST", "localhost")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER", "root")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD", "")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB", "phishing_awareness")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["name"] = user["name"]
            return redirect(url_for("dashboard"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        if len(password) < 6:
            flash("Password must contain at least 6 characters.", "danger")
            return render_template("register.html")
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE email=%s", (email,))
        if cur.fetchone():
            cur.close()
            flash("Email is already registered.", "warning")
            return render_template("register.html")
        cur.execute(
            "INSERT INTO users(name,email,password_hash,role) VALUES(%s,%s,%s,'admin')",
            (name, email, generate_password_hash(password))
        )
        mysql.connection.commit()
        cur.close()
        flash("Account created. Please sign in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/dashboard")
@login_required
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) AS c FROM campaigns")
    campaigns = cur.fetchone()["c"]
    cur.execute("SELECT COUNT(*) AS c FROM simulation_events")
    events = cur.fetchone()["c"]
    cur.execute("SELECT COUNT(*) AS c FROM simulation_events WHERE event_type='reported'")
    reported = cur.fetchone()["c"]
    cur.execute("SELECT COUNT(*) AS c FROM awareness_content")
    lessons = cur.fetchone()["c"]
    cur.close()
    report_rate = round((reported / events) * 100, 1) if events else 0
    return render_template("dashboard.html", campaigns=campaigns, events=events,
                           reported=reported, lessons=lessons, report_rate=report_rate)

@app.route("/campaigns")
@login_required
def campaigns():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM campaigns ORDER BY created_at DESC")
    rows = cur.fetchall()
    cur.close()
    return render_template("campaigns.html", campaigns=rows)

@app.route("/campaigns/new", methods=["GET", "POST"])
@login_required
def new_campaign():
    if request.method == "POST":
        name = request.form["name"].strip()
        scenario = request.form["scenario"].strip()
        difficulty = request.form["difficulty"]
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO campaigns(name,scenario,difficulty,status) VALUES(%s,%s,%s,'Draft')",
                    (name, scenario, difficulty))
        mysql.connection.commit()
        cur.close()
        flash("Simulation campaign created.", "success")
        return redirect(url_for("campaigns"))
    return render_template("campaign_new.html")

@app.route("/simulate/<int:campaign_id>")
@login_required
def simulate(campaign_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM campaigns WHERE id=%s", (campaign_id,))
    campaign = cur.fetchone()
    cur.close()
    if not campaign:
        return "Campaign not found", 404
    return render_template("simulation.html", campaign=campaign)

@app.route("/api/event", methods=["POST"])
@login_required
def record_event():
    data = request.get_json(silent=True) or {}
    event_type = data.get("event_type", "opened")
    campaign_id = data.get("campaign_id")
    if event_type not in {"opened", "clicked", "reported", "training_viewed"}:
        return jsonify({"error": "Unsupported event"}), 400
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO simulation_events(user_id,campaign_id,event_type) VALUES(%s,%s,%s)",
                (session["user_id"], campaign_id, event_type))
    mysql.connection.commit()
    cur.close()
    return jsonify({"ok": True})

@app.route("/training")
@login_required
def training():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM awareness_content ORDER BY id")
    lessons = cur.fetchall()
    cur.close()
    return render_template("training.html", lessons=lessons)

@app.route("/reports")
@login_required
def reports():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT c.name,
        SUM(e.event_type='opened') AS opened,
        SUM(e.event_type='clicked') AS clicked,
        SUM(e.event_type='reported') AS reported
        FROM campaigns c
        LEFT JOIN simulation_events e ON c.id=e.campaign_id
        GROUP BY c.id, c.name ORDER BY c.created_at DESC
    """)
    rows = cur.fetchall()
    cur.close()
    return render_template("reports.html", reports=rows)

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "PhishShield Awareness Platform"})

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
