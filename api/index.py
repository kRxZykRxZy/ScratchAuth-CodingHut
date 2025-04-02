from base64 import b64encode
from os import getenv, urandom
from flask import Flask, redirect, request, session, render_template
from requests import get
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

"""
Thanks to Chiroyce (https://replit.com/@Chiroyce/auth) for part of the code! Truly the GOAT.
"""

def base64(string):
    return b64encode(string.encode("utf-8")).decode()

@app.get("/")
def home():
    return render_template("index.html")

def btoa(string):
    return base64.b64encode(string.encode()).decode()

@app.get("/auth")
def auth():
    if "username" not in session:
        return redirect(f"https://auth.itinerary.eu.org/auth/?redirect={ base64('https://scratch-auth-demo.vercel.app/authenticate') }&name=NotFenixio%27s%20ScratchAuth%20Example")
    else:
        return render_template("auth.html", username=session["username"])
        return redirect(f"https://scratch-coding-hut.github.io/account?username={btoa(session["username"])}")

@app.get("/authenticate")
def authenticate():
    code = request.args.get("privateCode")
    
    if code == None:
        return "Bad Request", 400

    response = get(f"https://auth.itinerary.eu.org/api/auth/verifyToken?privateCode={code}").json()
    if response["redirect"] == "https://scratch-auth-demo.vercel.app/authenticate":
        if response["valid"]:
            session["username"] = response["username"]
            return redirect("/auth")
        else:
            return f"Authentication failed!"
    else:
        return "Invalid Redirect", 400
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
