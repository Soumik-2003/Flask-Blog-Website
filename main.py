from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import *
import hashlib
from dotenv import load_dotenv
import os
import smtplib
from pathlib import Path


'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

env_path = Path(__file__).parent / "enviro.env"
load_dotenv(env_path)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
ckeditor = CKEditor(app)
Bootstrap5(app)

email = os.environ.get('e_mail')
pass_email = os.environ.get('pass_key')

def send_email(name,to_mail,phone,message):
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(user=email,password=pass_email)
        msg = f"Subject:New Message.\n\nName = {name}\nemail = {to_mail}\nPhone Number = {phone}\nMessage={message}"
        server.sendmail(from_addr=email,to_addrs=email,msg=msg)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///userdata.db")
db = SQLAlchemy(model_class=Base)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


# CONFIGURE TABLES
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("User_Data.id"))
    author=relationship("UserData", back_populates="posts")
    comments=relationship("comments", back_populates="parent_post")
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


class  UserData(UserMixin, db.Model):
    __tablename__ = "User_Data"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name=db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    comments = relationship("comments", back_populates="comment_author")
    posts = relationship("BlogPost", back_populates="author")


class comments(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("User_Data.id"))
    comment_author = relationship("UserData", back_populates="comments")
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")
    text = db.Column(db.Text)

with app.app_context():
    db.create_all()



def gravatar_url(email, size=100, default='retro', rating='g'):
    email_hash = hashlib.md5(email.strip().lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d={default}&r={rating}"

@app.context_processor
def utility_processor():
    return dict(gravatar_url=gravatar_url)




@login_manager.user_loader
def load_user(user_id):
    return UserData.query.get(int(user_id))


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return login_manager.unauthorized() 
        elif not current_user.id==1:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if UserData.query.filter_by(email=form.email.data).first():
            flash ('The email is registered, please login.', 'info')
            return redirect(url_for("login"))

        password_hash = generate_password_hash(form.password.data, 'pbkdf2:sha256', salt_length=16)
        new_user = UserData(
            name=form.full_name.data,
            email=form.email.data,
            password=password_hash
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("register.html", form=form, logged_in=current_user.is_authenticated)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = UserData.query.filter_by(email=form.email.data).first()
        if not user:
            flash("This email does not exist, please try again.","danger")
        elif not check_password_hash(user.password, form.password.data):
            flash("Password incorrect, please try again.","danger")
        else:
            login_user(user)
            return redirect(url_for("get_all_posts"))
        

    return render_template("login.html", form=form, logged_in=current_user.is_authenticated)


@app.route('/logout')
def logout():
    logout_user()       
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost)).scalars().all()
    return render_template("index.html", all_posts=result, logged_in=current_user.is_authenticated)


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    comment_post = Comment()
    requested_post = db.get_or_404(BlogPost, post_id)

    if comment_post.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.", "danger")
            return redirect(url_for("login"))
        new_comment = comments(
            text=comment_post.body.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
        flash("Comment added successfully!", "info")
        return redirect(url_for("show_post", post_id=post_id))

    return render_template("post.html", comment_form=comment_post, post=requested_post, logged_in=current_user.is_authenticated)



@app.route("/new-post", methods=["GET", "POST"])
@admin_required
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, logged_in=current_user.is_authenticated)



@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_required
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True, logged_in=current_user.is_authenticated)



@app.route("/delete/<int:post_id>", methods=["GET", "POST"])
@admin_required
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html", logged_in=current_user.is_authenticated)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method=='POST':
        data=request.form
        send_email(name=data['name'],to_mail=data['email'],phone=data['phone'],message=data['message'])   
        return render_template('contact.html',msg_sent=True, logged_in=current_user.is_authenticated)
    
    return render_template("contact.html",msg_sent=False, logged_in=current_user.is_authenticated)


if __name__ == "__main__":
    app.run(debug=True, port=5002)
