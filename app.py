#These are requirements needed for the solution

from flask import Flask, redirect, render_template, request, session #This is needed for the Framework, 'Flask' to work
from flask_session import Session #This is needed to clear session variables when a user logs out

from cs50 import SQL #This is needed to link the database to the solution
import hashlib #This is needed to hash values before inserting them into the database


data = SQL("sqlite:///C:/Users/aandr/OneDrive/Python/CineWave/cinedata.db") #This is a connection to the database

app = Flask(__name__)


#Below is the configuration of session variables used on the solution

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def hash(phrase): #This is a function used for hashing values

    object = hashlib.md5(phrase.encode())
    object = object.hexdigest()

    return object



@app.route("/", methods= ["POST", "GET"]) #This is the Home Page. This is the first page where user will be taken when first opening the webiste.
def index():

    if request.method == 'GET': #This is used to verify if the user is logged into their account or not

        return render_template("index.html")
    
    else:
        ID = request.form.get("ID") #This is used to check if a user is logged in or not

        return render_template("index_loggedin.html", ID= ID)
    


@app.route("/register", methods= ["POST", "GET"]) #This is used to register a user into the database after validating their entered credentials
def register():

    if request.method == 'GET': #This is used to verify if the user is attempting to register an account, or if the solution needs to update the database

        return render_template("register.html")

    else:

        mail = request.form.get("address") #This is used to get the user's entered email address
        pw1 = request.form.get("pass_1") #This is used to get the user's entered password
        pw2 = request.form.get("pass_2") #This is used to get the user's re-entered password

        mail = hash(mail) #This is to hash credentials before it is compared against values in the database


        if pw1 != pw2: #This is used to determine if the two entered passwords match each other

            return render_template("failure.html")
        
        
        elif data.execute("SELECT * FROM userdata WHERE Email = ?", mail): #This is used to check if the entered email is already in use
            return render_template("failure.html")


        else:
            pw1 = hash(pw1) #This is used to hash the password before entering it into the database for security

            data.execute("INSERT INTO userdata (Email, Password) VALUES (?)", (mail, pw1)) #This is an SQL statement used to enter a new record (user) into the database
            ID = data.execute("SELECT ID FROM userdata WHERE Email = ? AND Password = ?", mail, pw1) #This is used to obtain the new user's ID

            return render_template("index_loggedin.html", ID= ID)
        



@app.route("/login", methods= ["POST", "GET"]) #This is used to log in a user once validating their entered credentials
def login():

    if request.method == 'POST': #This is used to verify if a user is attempting to log into their account, or if the solution needs to validate their credentials

        mail = request.form.get("address") #This is used to get the user's entered email address
        passw = request.form.get("password") #This is used to get the user's entered password


        #This is to hash the entered values to allow accurate comparing in the database

        mail = hash(mail)
        passw = hash(passw)


        if data.execute("SELECT * FROM userdata WHERE Email = ? AND Password = ?", mail, passw): #This is used to check if a record in the database has the corresponding Email and Password
            ID = data.execute("SELECT ID FROM userdata WHERE Email = ? AND Password = ?", mail, passw) #This is used to get the user's ID
            ID = ID[0]["ID"] #This is used to extract the wanted value from its dictionary

            return render_template("index_loggedin.html", ID= ID)
        
        else:

            return render_template("failure.html")
        
    else:

        return render_template("login.html")
    


@app.route("/movies", methods= ["POST","GET"]) #This is used to diaply the movie collection that CineWave has
def movies():

    if request.method == 'GET': #This is used to check if a user is logged in or not

        return render_template("movies.html")
    
    else:
        ID = request.form.get("ID") #This is used to check if a user is logged in or not

        return render_template("movies.html", ID= ID)
    


@app.route("/details", methods= ["POST","GET"]) #This is used to display current movie availabilities
def details():

    if request.method == 'GET': #This is used to check if a user is logged in or not

        return render_template("details.html")
    
    else:
        ID = request.form.get("ID") #This is used to check if a user is logged in or not

        return render_template("details.html", ID= ID)
    


@app.route("/bookings", methods= ["POST", "GET"])
def bookings():

    if request.method == 'GET': #This is used to check if the user is loading the page, or if they're booking a movie

        return render_template("bookings.html")
    
    else:

        ID = request.form.get("ID") #This is to assign the booking to the correct user

        if request.form.get("booking_ID"):

            booking_ID = request.form.get("booking_ID")

            movie = request.form.get("movie") #This is used ot get the selected movie

            seat = request.form.get("seat") #This is used to get the selected seat

            price = request.form.get("price") #This is used to get the price of the movie

            data.execute("INSERT INTO bookings (ID, Seat, Movie, Price) VALUES (?)", (booking_ID, seat, movie, price))

            return render_template("summary.html", ID= ID, seat= seat, movie= movie, price= price)

        else:

            return render_template("bookings.html", ID= ID)
        


@app.route("/logout") #This is used to log out a user while also deleting session variables
def logout():

    session.clear() #This clears all session variables

    return redirect("/")



@app.route("/summary", methods= ["POST", "GET"])
def summary():

        ID = request.form.get("booking_ID") #Thsi is used to get the user's booking ID

        movie = request.form.get("movie") #This is to get the user's selected movie

        seat = request.form.get("seat") #This is to get the user's selected seat

        price = request.form.get("price") #This is used to get the price of the movie

        return render_template("summary.html", ID= ID, movie= movie, seat= seat, price= price)