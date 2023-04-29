from flask import Flask, render_template,url_for,request,redirect, session,redirect,abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3
import os


DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = "asdfghjkhgfd"


app = Flask(__name__)#созданияе объекта по файлу app
app.config.from_object(__name__)
#app.config.update(dict(DATABASE=os.path.join(app.root_path,"filsite.db")))
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///' + os.path.join( os.path.abspath(os.path.dirname(__file__)), 'mydb.db' )
app.config["SECRET_KEY"] = SECRET_KEY

""" def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close() """


db = SQLAlchemy(app)
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("name",db.String(100), nullable=False)
    contact = db.Column("contact",db.String(50), nullable=False)
    product = db.Column("product",db.String(50), nullable=False)
    count = db.Column("count",db.String(50), nullable=False)
    date = db.Column("date",db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Article %r>' % self.id
 


@app.route('/')#главная страничка
@app.route('/home')#главная страничка
@app.route('/home/new')#главная страничка
def index():
    return render_template("index.html")


@app.route('/posts')#страничка всех постов
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/assortment')#страничка товаров
def assortment():
    return render_template("assortment.html")


@app.route('/posts/<int:id>')#страничка конкретного поста
def postDetail(id):
    article = Article.query.get(id)
    return render_template("post-detail.html", article=article)


@app.route('/posts/<int:id>/del')#страничка удаление
def postDelite(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Не удалось удалить запись!"

@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])  # страничка редактирования
def postUpdate(id):
    article = Article.query.get_or_404(id)
    if request.method == "POST":
        article.name = request.form['name']
        article.contact = request.form['contact']
        article.product = request.form['product']
        article.count = request.form['count']
        
        if (article.contact == "" or article.name == ""):
            return "При добавлении статьи возникли ошибки!"
        try:
            db.session.commit()
            return redirect('/posts')
        
        except:
            return "При добавлении статьи возникли ошибки!"
    else:
        return render_template("post-update.html", article=article)


@app.route('/create-article',methods=['POST','GET'])#страничка создания поста
def creatArticle():
    if request.method == "POST":
        try:
            name = request.form['name']
            contact = request.form['contact']
            product = request.form['product']
            count = request.form['count']
            article = Article(name=name,contact=contact,product=product,count=count)
            print(request.form)
        except:
            return "приплыли"
        if(article.name=="" or article.contact==""):
            return "При добавлении статьи возникли ошибки (поля пустые)!"
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            
            #return article.name, article.contact, article.product, article.count
            return "При добавлении статьи возникли ошибки!"
    else:
        return render_template("create-article.html")


@app.route('/user/<name>')#страничка пользователя
@app.route('/user')#страничка пользователя
def user(name):
    if 'userLogged' not in session or session["userLogged"] !=name:
        abort(404)
    return render_template("user.html", name = name)


@app.route('/about')#страничка about
def about():
    return render_template("about.html")


@app.route('/test')#страничка test
def test():
    return render_template("test.html")

@app.errorhandler(404)
def pageNotFount(error):
    return render_template("page404.html")

@app.route('/exit')
def exit():
    session["userLogged"] = ""
    return redirect(url_for('login'))
@app.route('/login', methods=["POST", "GET"])
def login():
    if 'userLogged' in session  and session["userLogged"] != "":
        return redirect(url_for('user',name = session['userLogged']))
    elif request.method == 'POST' and len(request.form["name"])>2 and len(request.form["contact"])>2 and len(request.form["password"])>8:
        session["userLogged"] = request.form["name"]
        session["userContact"] = request.form["contact"]
        session["userPas"] = request.form["password"]
        
        return redirect(url_for('user',name = session['userLogged']))
    else:
        return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)


