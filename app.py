from flask import Flask, render_template, redirect, request, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.sql import func

app = Flask(__name__)
# sudo /opt/lampp/manager-linux-x64.run to open LAMPP

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/lemo_miniblog"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Category(db.Model):
    __tablename__ = "category"  # --> si no esta, adopta el nombre de la clase
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return f"category: {self.name}"


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)

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

    def __str__(self):
        return f"-Comment '{self.content}' by {self.user_id}"

#TODO: CONTEXT PROCESSOR PASA EL ID DEL USER SELECCIONADO
#CADA FUNCION TOMA EL ID COMO PARAMETRO PARA SABER Q USER SUBIO EL POST/COMENTARIO
@app.context_processor
def inject_paises():
    posts=db.session.query(Post).all()
    return dict(posts=posts)

@app.route("/")
def Index():
    return render_template('index.html')

@app.route("/add_post", methods=['POST'])
def AddPost():
    if request.method=='POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        #obtener el user
        user=1
        new_post=Post(title=title,content=content,category_id=category,
                      user_id=user)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('Index'))

@app.route("/add_comment", methods=['POST'])
def AddComment():
    if request.method=='POST':
        content = request.form['content']
        new_comment=Comment(content=nombre_pais)
        db.session.add(nuevo_pais)
        db.session.commit()

        return redirect(url_for('Index'))

