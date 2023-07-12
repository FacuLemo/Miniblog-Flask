from flask import Flask, render_template, redirect, request, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.sql import func

app = Flask(__name__)
# sudo /opt/lampp/manager-linux-x64.run to open LAMPP

URI_LOCAL="mysql+pymysql://root:@localhost/lemo_miniblog"
app.config["SQLALCHEMY_DATABASE_URI"] = URI_LOCAL

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Category(db.Model):
    __tablename__ = "category"  # --> si no esta, adopta el nombre de la clase
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    posts= db.relationship('Post', backref='category')
    def __str__(self):
        return f"category: {self.name}"


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    posts= db.relationship('Post', backref='user')
    comments= db.relationship('Comment', backref='user')

    def __str__(self):
        return f"-User data: {self.nombre}, {self.email}."


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), nullable=False)
    content = db.Column(db.String(500), nullable=True)
    time_created = db.Column(DateTime(timezone=True),
                              server_default=func.now())
    time_updated = db.Column(DateTime(timezone=True), onupdate=func.now())
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    category_id = db.Column(db.Integer, ForeignKey("category.id"),
                             nullable=True)
    comments= db.relationship('Comment', backref='post', cascade="all,delete" )

    def __str__(self):
        return f"-Category: f{self.name}"

class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    time_created = db.Column(DateTime(timezone=True),
                              server_default=func.now())
    time_updated = db.Column(DateTime(timezone=True), onupdate=func.now())
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, ForeignKey("post.id"), nullable=False)

    def __str__(self):
        return f"-Comment '{self.content}' by {self.user_id}"

#tengo que borrar esto, soy un pelotudo, no hace falta
def GetLoggedUserId(uid):
    logged_user=User.query.get(uid)
    logged_id=logged_user.id
    return logged_id

#TODO: Pasar usuarios en el context processor y no los posts! cambiar en layout

@app.context_processor
def inject_paises():
    posts=db.session.query(Post).order_by(Post.id.desc()).all()
    users=db.session.query(User).all()
    categ=db.session.query(Category).all()
    return dict(posts=posts, users=users, categories=categ )

@app.route("/")
def RedirectGuest():
    return redirect(url_for('Index', user_id='guest'))

@app.route("/<user_id>")
def Index(user_id):
    if user_id=='guest':
        return render_template('guest.html',
                               comments=db.session.query(Comment).all())
    else:
        logged_user=User.query.get(user_id)
        return render_template('index.html',logged_user=logged_user,
                               comments=db.session.query(Comment).all())

@app.route("/categories")
def ViewCategories():
    return render_template('categories.html')

#TODO: CATEGORIES FILTER--
@app.route("/categories/<id>/<u_id>")
def FilteredPosts(id,uid):
    logged_id=GetLoggedUserId(uid)
    return redirect(url_for('Index',user_id=logged_id))

@app.route("/users")
def ViewUsers():
    return render_template('users.html',)

@app.route("/add_post/<uid>", methods=['POST'])
def AddPost(uid):
    if request.method=='POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        logged_id=GetLoggedUserId(uid)
        new_post=Post(title=title,content=content,category_id=category,
                      user_id=logged_id)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('Index',user_id=logged_id))

@app.route("/add_comment/<post_id>/<uid>", methods=['POST'])
def AddComment(post_id,uid):
    if request.method=='POST':
        content = request.form['content']
        post = post_id
        logged_id=GetLoggedUserId(uid)
        new_comment=Comment(content=content, user_id=logged_id, post_id=post)
        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for('Index',user_id=logged_id))

@app.route("/delete_post/<id>/<uid>")
def deletePost(id,uid):
    post=Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    logged_id=GetLoggedUserId(uid)
    return redirect(url_for('Index',user_id=logged_id))

@app.route("/delete_comment/<id>/<uid>")
def deleteComment(id,uid):
    comm=Comment.query.get(id)
    db.session.delete(comm)
    db.session.commit()
    logged_id=GetLoggedUserId(uid)
    return redirect(url_for('Index',user_id=logged_id))

