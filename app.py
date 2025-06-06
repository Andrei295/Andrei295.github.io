#These are requirements needed for the solution

from flask import Flask, redirect, render_template, request, session #This is needed for the Framework, 'Flask' to work
from flask_session import Session #This is needed to clear session variables when a user logs out

from cs50 import SQL #This is needed to link the database to the solution



app = Flask(__name__)

#Below is the configuration of session variables used on the solution

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.route("/", methods= ["GET"]) #This is the Home Page. This is the first page where user will be taken when first opening the webiste. This is where users will be taken when they choose to log out or delete their account
def index():

    if request.method == 'GET': #This is used to verify if the user is logged into their account or not

        return render_template("index.html")
    


@app.route("/about_me", methods= ['GET']) #This is a page that displays facts about me
def about_me():

    if request.method == 'GET': #This is used to verify if the user is logged into their account or not

        return render_template("about_me.html")
    

@app.route("/portfolio", methods= ["GET"]) #This is a page about my skills and experience
def portfolio():

    if request.method == 'GET': #This is used to verify if the user is logged into their account or not

        return render_template("portfolio.html")
    

@app.route("/contact_us", methods= ["GET", "POST"]) #This is a page that allows users to contact us
def contact_us():

    if request.method == 'GET': #This is used to check if the user is sending a message, or is just opening the page

        return render_template("contact_us.html")

    elif request.method == 'POST':

        return render_template('thank_you.html')