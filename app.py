# Your Pesonal Expense Tracker

# Import functions
from cs50 import SQL
from datetime import date
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

from helpers import login_required, currencylist, monthlist, year_data, year_total, month_total, typelist

# Configure application
app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 library to use SQLite database
db = SQL("sqlite:///expense.db")


# Ensure responses are not cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Home
@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    today = date.today()
    month = today.month
    months = monthlist()

    data = db.execute("SELECT DISTINCT year FROM expenses WHERE account = ?", session["user_id"])
    years = []
    for row in data:
        years.append(row["year"])

    if request.method == "POST":
        year = request.form.get("year")
        yeardata = year_data(session["user_id"], year)
        yeartotal = year_total(yeardata)

        types = typelist(session["user_id"], year)

        # monthdata = data[0], monthtotal = data[1]
        data = month_total(session["user_id"], year, types)

        return render_template("home.html", username=name, yeardata=yeardata, monthdata=data[0], year=year, month=month,
                               years=years, months=months, types=types, sign=sign, yeartotal=yeartotal, monthtotal=data[1])

    else:
        year = today.year
        yeardata = year_data(session["user_id"], year)
        yeartotal = year_total(yeardata)

        types = typelist(session["user_id"], year)

        # monthdata = data[0], monthtotal = data[1]
        data = month_total(session["user_id"], year, types)

        return render_template("home.html", username=name, yeardata=yeardata, monthdata=data[0], year=year, month=month,
                               years=years, months=months, types=types, sign=sign, yeartotal=yeartotal, monthtotal=data[1])


# Expenses
@app.route("/expense", methods=["GET", "POST"])
@login_required
def expense():
    if request.method == "POST":
        date1 = request.form.get("date")
        type = request.form.get("type")
        desc = request.form.get("desc")
        amount = request.form.get("amount")
        error = 0

        # Ensure all fields are filled
        if not date1 or date1 == "yyyy-mm-dd" or not type or not desc:
            flash("Missing Date, Type and/or Description")
            error += 1

        # Convert amount to 0 if amount is ""
        try:
            amount = float(amount)
        except ValueError:
            amount = 0

        # Ensure amount is not 0.00
        if amount == 0:
            flash("Missing amount or amount cannot be 0")
            error += 1

        # Redirect and flash if any error
        if error > 0:
            return redirect("/expense")

        # Insert into database and redirect
        datesplit = date1.split("-")
        db.execute("INSERT INTO expenses (account, date, year, month, type, description, amount) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   session["user_id"], date1, datesplit[0], datesplit[1], type, desc, amount)
        return redirect("/expense")

    else:
        expensetype = db.execute("SELECT * FROM expensetype EXCEPT SELECT * FROM expensetype WHERE type = ? ORDER BY type", "Other")
        other = db.execute("SELECT type FROM expensetype WHERE type = ?", "Other")[0]
        expenses = db.execute("SELECT * FROM expenses WHERE account = ? ORDER BY date DESC, id DESC LIMIT 10", session["user_id"])
        return render_template("expense.html", username=name, type=expensetype, other=other, expenses=expenses, today=date.today(),
                                               iso=iso, sign=sign)


# History
@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    years = db.execute("SELECT DISTINCT year FROM expenses WHERE account = ? ORDER BY year DESC", session["user_id"])
    months = monthlist()
    yearmonth = db.execute("SELECT DISTINCT year, month FROM expenses WHERE id = ?", session["user_id"])

    if request.method == "POST":
        year = request.form.get("year")
        month = request.form.get("month")
        error = 0

        # Redirect if both fields are not selected
        if not year and not month:
            flash("Missing Year and Month")
            error += 1

        # Redirect if month is selected but year is not
        if not year and month != None:
            flash("Missing Year")
            error += 1

        # Redirect and flash if any error
        if error > 0:
            return redirect("/history")

        # Show selected year if month is not selected
        if year != None and not month:
            expenses = db.execute("SELECT * FROM expenses WHERE account = ? AND YEAR = ? ORDER BY date DESC, id DESC",
                                  session["user_id"], year)
            return render_template("history.html", username=name, expenses=expenses, years=years, months=months, year=year, iso=iso,
                                                   sign=sign, yearmonth=yearmonth)

        # Show history for selected year and month
        expenses = db.execute("SELECT * FROM expenses WHERE account = ? AND YEAR = ? AND MONTH = ? ORDER BY date DESC, id DESC",
                              session["user_id"], year, month)
        month = db.execute("SELECT * FROM months WHERE id = ?", month)[0]["month"]
        return render_template("history.html", username=name, expenses=expenses, years=years, months=months, year=year, month=month,
                                               iso=iso, sign=sign, yearmonth=yearmonth)

    else:

        # Show latest 50 entries as defaultd
        expenses = db.execute("SELECT * FROM expenses WHERE account = ? ORDER BY date DESC, id DESC LIMIT 50", session["user_id"])
        return render_template("history.html", username=name, expenses=expenses, years=years, months=months, month="the latest 50 entries",
                                               iso=iso, sign=sign, yearmonth=yearmonth)


# Settings
@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":

        # Change display name
        named = request.form.get("name")
        if named != "" and named != name:
            db.execute("UPDATE accounts SET displayname = ? WHERE id = ?", named, session["user_id"])
            global_name(session["user_id"])
            flash("Display name changed successfully!")

        # Change preferred currency
        currency = request.form.get("currency")
        if currency != None and currency != db.execute("SELECT * FROM accounts WHERE id = ?", session["user_id"])[0]["currency"]:
            db.execute("UPDATE accounts SET currency = ? WHERE id = ?", currency, session["user_id"])
            global_currency(int(currency))
            flash("Preferred currency changed successfully!")

        # Change password
        # Check if password field is filled
        password = request.form.get("password")
        if password != "":
            error = 0

            # Check if password is correct
            hash = db.execute("SELECT * FROM accounts WHERE id = ?", session["user_id"])[0]["hash"]
            if not check_password_hash(hash, password):
                flash("Incorrect password")
                error += 1

            # Check if new password length is 6 or more
            passwordn = request.form.get("passwordn")
            if len(passwordn) < 6:
                flash("New password length must be 6 or more")
                error += 1

            # Check if new password is the same with current password
            if check_password_hash(hash, passwordn):
                flash("New password must be different than current password")
                error += 1

            if passwordn != request.form.get("confirmation"):
                flash("Please confirm your new password")
                error += 1

            # Redirect and flash if any error
            if error > 0:
                return redirect("/settings")

            # Update password if passed all the criteria above
            db.execute("UPDATE accounts SET hash = ? WHERE id = ?", generate_password_hash(passwordn), session["user_id"])
            flash("Password changed successfully!")

        return redirect("/settings")

    else:
        return render_template("settings.html", username=name, iso=iso, currencyl=currencylist())


# Log user out
@app.route("/logout")
def logout():

    # Clear session and redirect
    session.clear()
    return redirect("/login")


# Log user in
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username, password are submitted, username exists and password is correct
        rows = db.execute("SELECT * FROM accounts WHERE username = ?", username)
        if not username or not password or len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("Invalid Username and/or Password")
            return render_template("login.html")

        # Log user in and set global variables
        session["user_id"] = rows[0]["id"]
        global_name(session["user_id"])
        global_currency(rows[0]["currency"])

        # Clear variables and redirect
        username = password = rows = None
        return redirect("/")

    else:
        return render_template("login.html")


# Register user
@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    currencyl = currencylist()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        currency = request.form.get("currency")
        error = 0

        # Ensure all fields are submitted
        if not username or not password or not currency:
            flash("Missing Username, Password and/or Preferred Currency")
            error += 1

        # Ensure username is available
        if len(db.execute("SELECT * FROM accounts WHERE username = ?", username)) != 0:
            flash("Username already taken")
            error += 1

        # Ensure password length is 6 or more
        if len(password) < 6:
            flash("Password length must be 6 or more")
            error += 1

        # Ensure password and confirm password are the same
        if not password == request.form.get("confirmation"):
            flash("Please confirm your password")
            error += 1

        # Redirect and flash if any error
        if error > 0:
            return render_template("register.html", currencyl=currencyl)

        # Insert username and generated hash into database
        db.execute("INSERT INTO accounts (username, hash, displayname, currency) VALUES (?, ?, ?, ?)",
                   username, generate_password_hash(password), username, currency)

        # Log user in and set global variables
        session["user_id"] = db.execute("SELECT * FROM accounts WHERE username = ?", username)[0]["id"]
        global_name(session["user_id"])
        global_currency(int(currency))

        # Clear variables and redirect
        username = password = currency = None
        return redirect("/")

    else:
        return render_template("register.html", currencyl=currencyl)


#  Initialize / Update user's display name
def global_name(accountid):
    global name
    name = db.execute("SELECT * FROM accounts WHERE id = ?", accountid)[0]["displayname"]


# Initialize / Update user's currency
def global_currency(currencyid):
    global iso, sign
    rows = db.execute("SELECT * FROM currencies WHERE id = ?", currencyid)
    iso = rows[0]["iso"]
    sign = rows[0]["sign"]
