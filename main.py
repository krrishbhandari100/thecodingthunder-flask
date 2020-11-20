from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

with open("config.json") as c:
    params = json.load(c)["params"]
app = Flask("krrish-app")
app.config["SECRET_KEY"] = "Y-%S6#^CLJt%*gv_uY-%S6#^CLJt%*gv_u"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/thecodingthunder'
db = SQLAlchemy(app)

class Postss(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(255), unique=False, nullable=False)
    post_posted_by = db.Column(db.String(255), unique=False, nullable=False)
    post_desc = db.Column(db.String(255), unique=False, nullable=False)
    stime = db.Column(db.String(255), unique=False, nullable=True)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True, nullable=True)
    name = db.Column(db.String(255), unique=False, nullable=True)
    email = db.Column(db.String(255), unique=False, nullable=True)
    phone_number = db.Column(db.String(255), unique=False, nullable=True)
    query = db.Column(db.String(255), unique=False, nullable=True)

@app.route("/")
def index():
    posts = Postss.query.all()
    return render_template("index.html", posts=posts, params=params)

@app.route("/about")
def about():
    return render_template("about.html", params=params)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # sno = 1
        name = request.form.get("name")
        email = request.form.get("email")
        query = request.form.get("query")
        phone_number = request.form.get("phone_number")
        entry = Contacts(name=name, email=email,phone_number=phone_number, query=query)
        db.session.add(entry)
        db.session.commit()
    return render_template("contact.html", params=params)

@app.route("/post/<int:sno>")
def post(sno):
    post = Postss.query.filter_by(sno=sno).first()
    return render_template("post.html", post=post, params=params)

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if 'user' in session:
        posts = Postss.query.all()
        return render_template("admin.html", posts=posts, params=params)
    else:
        if request.method == "POST":
            posts = Postss.query.all()
            Username = request.form["Username"]
            Password = request.form["Password"]
            if(Username==params["admin-user"] and Password==params["admin-password"]):
                session['user'] = Username
                return render_template("admin.html", posts=posts, params=params)
            else:
                pass
    return render_template("dashboard.html", params=params)

@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user', None)
        return "Success <br> <a href='/dashboard'>Go to Dashboard again</a>"
    else:
        return "you have not loged in please loggin first<br><a href='/dashboard'>Login</a>"

@app.route("/dashboard/edit/<int:sno>", methods=["GET", "POST"])
def edit(sno):
    if 'user' in session:
        if(request.method=="POST"):
            sno = request.form["sno"]
            post_title = request.form["post_title"]
            post_posted_by = request.form["post_posted_by"]
            post_desc = request.form["post_desc"]
            editpost = Postss.query.filter_by(sno=sno).first()
            editpost.sno=sno
            editpost.post_title=post_title
            editpost.post_desc=post_desc
            db.session.commit()
            return redirect("/dashboard")
    else:
        return redirect('/dashboard')

    post = Postss.query.filter_by(sno=sno).first()
    return render_template("edit.html", post=post, params=params)


@app.route("/dashboard/delete/<int:sno>", methods=["GET", "POST"])
def delete(sno):
    if 'user' in session:
        if(request.method=="POST"):
            sno = request.form.get("sno")
            post_title = request.form.get("post_title")
            post_posted_by = request.form.get("post_posted_by")
            post_desc = request.form.get("post_desc")
            delepost = Postss.query.filter_by(sno=sno).first()
            db.session.delete(delepost)
            db.session.commit()
            return redirect("/dashboard")
    else:
        return redirect('/dashboard')        

    post = Postss.query.filter_by(sno=sno).first()
    return render_template("delete.html", post=post, params=params)


@app.route("/dashboard/NewPost", methods=["GET", "POST"])
def NewPost():
    if 'user' in session:
        if(request.method=="POST"):
            post_title = request.form["post_title"]
            post_posted_by = request.form["post_posted_by"]
            post_desc = request.form["post_desc"]
            stime = datetime.now()
            post_add = Postss(post_titile=post_title, post_posted_by=post_posted_by, post_desc=post_desc, stime=stime)
            db.session.add(post_add)
            db.session.commit()
            return redirect("/dashboard")
    else:
        return redirect('/dashboard')
    return render_template("npost.html", params=params)
if __name__ == '__main__':
    app.run(port=8000, debug=True)