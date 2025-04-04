from base64 import b64encode
from os import getenv, urandom
from flask import Flask, redirect, request, session, render_template
from requests import get
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = urandom(24)

"""
Thanks to Chiroyce (https://replit.com/@Chiroyce/auth) for part of the code! Truly the GOAT.
"""

def base64(string):
    return b64encode(string.encode("utf-8")).decode()

def btoa(string):
    return b64encode(string.encode()).decode()

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/auth")
def auth():
    if "username" not in session:
        return redirect(f"https://auth.itinerary.eu.org/auth/?redirect={base64('https://scratchauth-codinghut.onrender.com/authenticate')}&name=NotFenixio%27s%20ScratchAuth%20Example")
    else:
        return redirect(f"https://scratch-coding-hut.github.io/account?username={btoa(session['username'])}")

@app.get("/authenticate")
def authenticate():
    code = request.args.get("privateCode")
    
    if code is None:
        return "Bad Request", 400

    response = get(f"https://auth.itinerary.eu.org/api/auth/verifyToken?privateCode={code}").json()
    
    if response.get("redirect") == "https://scratchauth-codinghut.onrender.com/authenticate":
        if response.get("valid"):
            session["username"] = response["username"]
            return redirect("/auth")
        else:
            return "Authentication failed!"
    else:
        return "Invalid Redirect", 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
