#suchin.ravi@wonksknow.com 
#10 Pm 28th Jan Wedensday
from flask import Flask, render_template, redirect, session, request, flash
import pymongo
from bson.objectid import ObjectId
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key ="F)Z=y}BX4xggSc))Q$R7-rY*y*wQ&4"
client = pymongo.MongoClient("mongodb+srv://marcellusfieldridley:12345@cluster0.kxuyvqi.mongodb.net/")
db = client.Library

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/libraryHome", methods = ['GET','POST'])
def libraryHome():
    if request.method == 'GET':
        libraryBooks = list(db.books.find({"USER":session["username"]}))
        print("GOT THE FOLLOWING DATA:" + str(libraryBooks))
        return render_template("libraryHome.html",books = libraryBooks)
    return render_template("libraryHome.html")

@app.route("/loginUser", methods = ['GET','POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("userPassword")
    user = db.users.find_one({"USERNAME":username})
    print("VERIFYING:",user)
    if user:
        print(user)
        print("VERIFYING IF [" + password +"] IS THE SAME AS [" +user["PASSWORD"] + "]" )
        if sha256_crypt.verify(password,user["PASSWORD"]):
            session["username"] = username
            print("session:", session["username"])
            print("USER HAS BEEN VERIFIED: REDIRECTING NOW")
            return redirect("/libraryHome")
        else:
            flash('incorrect password or username')
            return redirect("/")

    print(username,password)
    
    print("loginButtonPressed")
    return redirect("/")

@app.route("/registerUser", methods = ['GET','POST'])
def register():
    username = request.form.get("username")
    password = sha256_crypt.hash(request.form.get("userPassword"))
    email = request.form.get("userEmail")
    print("ATTEMPTING TO INPUT: {USERNAME:",username +", PASSWORD:",password+",EMAIL:",email,"}")
    db.users.insert_one({"USERNAME":username,"PASSWORD":password,"EMAIL":email})
    print("INPUT WAS SUCCESFUL")
    session["username"] = username
    print("session:", session["username"])
    return redirect("/libraryHome")

@app.route("/newBook", methods = ['GET','POST'])
def newBook():
    bookName = request.form.get("bookName")
    bookPages = request.form.get("numOfPages")
    bookDescription = request.form.get("description")
    bookImage = request.form.get("imageLink")
    db.books.insert_one({"USER":session['username'],"BOOK_NAME":bookName,"BOOK_PAGES":bookPages,"BOOK_DESCRIPTION":bookDescription,"BOOK_IMAGE":bookImage})
    return redirect('/libraryHome')

@app.route("/delete/<book_id>")
def delete(book_id):
    db.books.delete_one({'_id':ObjectId(book_id)})
    return redirect("/libraryHome")

@app.route("/edit/<book_id>", methods = ['GET','POST'])
def edit(book_id):
    bookName = request.form.get("e_bookName")
    bookPages = request.form.get("e_numOfPages")
    bookDescription = request.form.get("e_description")
    bookImage = request.form.get("e_imageLink")
    db.books.update_one({'_id':ObjectId(book_id)},{'$set':{'BOOK_NAME':bookName,'BOOK_PAGES':bookPages,'BOOK_DESCRIPTION':bookDescription,'BOOK_IMAGE':bookImage}})
    return redirect("/libraryHome")
@app.route("/logout")
def logout():
    session.clear()
    flash("officialy logged out")
    return redirect("/")
if __name__ == '__main__':
    app.debug = True
    app.run()