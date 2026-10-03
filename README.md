# 🛡 PhishShield — Phishing Simulation & Awareness Platform

A professional full-stack cybersecurity awareness project built for hackathons.

## What it demonstrates

- Flask/Python backend
- MySQL relational database
- Responsive HTML/CSS/JavaScript frontend
- Secure password hashing with Werkzeug
- Login and registration
- Campaign creation
- Controlled phishing simulations
- Event tracking: opened / clicked / reported
- Awareness micro-learning
- Analytics/reporting dashboard
- Safety-by-design: no real passwords or sensitive credentials are collected

## Project structure

```text
phishing_awareness_platform/
├── app.py
├── requirements.txt
├── README.md
├── database/
│   └── schema.sql
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── campaigns.html
│   ├── campaign_new.html
│   ├── simulation.html
│   ├── training.html
│   └── reports.html
└── static/
    ├── css/style.css
    └── js/
```

## 1. Install prerequisites

Install:

- Python 3.10+
- MySQL Server 8+
- VS Code
- Python extension for VS Code

## 2. Create the database

Open MySQL Workbench or MySQL command line and run:

```sql
SOURCE path/to/phishing_awareness_platform/database/schema.sql;
```

Or copy/paste the contents of `database/schema.sql`.

Default database:
`phishing_awareness`

## 3. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

## 4. Install Python packages

```bash
pip install -r requirements.txt
```

If `mysqlclient` fails to install on Windows, install the current MySQL C connector/build prerequisites or use a compatible Python environment.

## 5. Configure MySQL

The application defaults to:

- Host: localhost
- User: root
- Password: empty
- Database: phishing_awareness

If your MySQL password is different, set environment variables.

Windows PowerShell:

```powershell
$env:MYSQL_HOST="localhost"
$env:MYSQL_USER="root"
$env:MYSQL_PASSWORD="YOUR_PASSWORD"
$env:MYSQL_DB="phishing_awareness"
$env:SECRET_KEY="a-long-random-secret"
```

macOS/Linux:

```bash
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=YOUR_PASSWORD
export MYSQL_DB=phishing_awareness
export SECRET_KEY=a-long-random-secret
```

## 6. Run

```bash
python app.py
```

Open:

`http://127.0.0.1:5000`

Create an account and explore:

1. Dashboard
2. Simulations
3. New campaign
4. Controlled simulation
5. Awareness lessons
6. Reports

## Hackathon demo flow

1. Register an admin/demo account.
2. Open **Simulations**.
3. Open the preloaded **Invoice Verification Drill**.
4. Click **Review notice** to record a safe click event.
5. Click **Report phishing** to record a positive reporting event.
6. Open **Reports** and show the metrics.
7. Explain that the system intentionally does NOT collect real credentials.

## Important safety boundary

This project is an educational simulation platform. It is designed to teach users to recognize phishing without harvesting credentials or delivering real phishing emails.

For a production deployment, add HTTPS, CSRF protection, role-based authorization, secure session configuration, audit logging, rate limiting, centralized secrets management, and organization-approved email simulation infrastructure.

## Suggested 2-minute presentation

**Problem:** Human error is a major part of phishing risk.

**Solution:** PhishShield provides controlled simulations + micro-learning + measurable reporting.

**Innovation:** Every simulation is tied to an event-based learning loop: simulate → observe → teach → measure.

**Technology:** HTML/CSS/JS + Flask/Python + MySQL.

**Impact:** Security teams can turn awareness from a one-time lecture into a measurable continuous program.
