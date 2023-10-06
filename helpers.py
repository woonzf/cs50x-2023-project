from cs50 import SQL
from flask import redirect, session
from functools import wraps

db = SQL("sqlite:///expense.db")


def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Retrieve currency list
def currencylist():
    return db.execute("SELECT * FROM currencies ORDER BY iso")


# Retrieve month list
def monthlist():
    return db.execute("SELECT * FROM months")


def typelist(accountid, year):
    data = db.execute("SELECT DISTINCT type FROM expenses WHERE account = ? AND year = ?", accountid, year)
    types = []
    for row in data:
        types.append(row["type"])
    return types


# Create a list to store amount per month
def year_data(accountid, year):
    yeardata = []
    for i in range(1, 13):
        amount = db.execute("SELECT SUM(amount) FROM expenses WHERE account = ? AND year = ? AND month = ?",
                            accountid, year, i)[0]["SUM(amount)"]
        if amount == None:
            yeardata.append(0)
        else:
            yeardata.append(amount)
    return yeardata


# Create a list to store amount per type
def month_data(accountid, year, month, types):
    monthdata = []
    for type in types:
        amount = db.execute("SELECT SUM(amount) FROM expenses WHERE account = ? AND year = ? AND month = ? AND type = ?",
                            accountid, year, month, type)[0]["SUM(amount)"]
        if amount == None:
            monthdata.append(0)
        else:
            monthdata.append(amount)
    return monthdata


# Calculate year total
def year_total(yeardata):
    yeartotal = 0
    for i in range(len(yeardata)):
        yeartotal += yeardata[i]
    return yeartotal


# Retrive month data and calculate month total
def month_total(accountid, year, types):
    monthdata = {}
    monthtotal = []
    length = len(types)
    for i in range(1, 13):
        data = month_data(accountid, year, i, types)
        monthdata[i] = data
        total = 0
        for j in range(length):
            total += data[j]
        monthtotal.append(total)
    return [monthdata, monthtotal]
