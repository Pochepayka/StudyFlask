from flask import Flask, render_template,url_for,request,redirect, session,redirect,abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3
import os


#DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = "asdfghjkhgfd"
#app.config.from_object(__name__)
#app.config.update(dict(DATABASE=os.path.join(app.root_path,"filsite.db")))
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



app = Flask(__name__)#созданияе объекта по файлу app
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///blog.db'# + os.path.join( os.path.abspath(os.path.dirname(__file__)), 'mydb.db' )
app.config["SECRET_KEY"] = SECRET_KEY

db = SQLAlchemy(app)

menu = [["Асортимент", "/assortment"],["Создать товар", "/create-product"],["Заказать", "/create-article"],["Заказы", "/posts"], ["Контакты","/about"], ["Профиль","/login"]]

class Users (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column("login",db.String(50), nullable=False, unique=True)
    psw = db.Column("pasword",db.String(500), nullable=False)
    date = db.Column("date",db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f'<users {self.id}>' 
    
class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact = db.Column(db.String(50), default = "не указано")
    point = db.Column(db.String(50), default = "Общежитие Икар")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    product = db.Column(db.String(50), nullable=False)
    count = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Article %r>' % self.id
    

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    weight = db.Column(db.Integer(), default="не указано")
    count = db.Column(db.Integer(), default="не указано")
    date = db.Column(db.DateTime, default=datetime.utcnow)
    imgHref = db.Column(db.String(200), default="https://sun9-41.userapi.com/JzMJqJuXIL3kXCqUhS-DbDZwiWbIZfvm1Pxc0g/o0bfwiam7cU.jpg")
    def __repr__(self):
        return '<Product %r>' % self.id
 


@app.route('/')#главная страничка
@app.route('/home')#главная страничка
@app.route('/home/new')#главная страничка
def index():
    return render_template("index.html", menu = menu)


@app.route('/assortment')#страничка товаров
def assortment():
    
    products = Products.query.order_by(Products.date.desc()).all()
    return render_template("assortment.html", menu = menu, products=products)



@app.route('/create-product',methods=['POST','GET'])#страничка товаров
def createProduct():
    
    if request.method == "POST":
        product = Products(name=request.form['name'],price=request.form['price'],weight=request.form['weight'],count=request.form['count'])
        if(len(product.name)<2 or len(product.price)==""):
            return "При добавлении статьи возникли ошибки (поля пустые)!"
        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/assortment')
        except:
            return "При добавлении статьи возникли ошибки!"
    return render_template("create-product.html", menu = menu)


@app.route('/create-article',methods=['POST','GET'])#страничка создания поста
def creatArticle():
    if request.method == "POST":
        try:
            name = request.form['name']
            contact = request.form['contact']
            product = request.form['product']
            count = request.form['count']
            article = Article(name=name,contact=contact,product=product,count=count)
        except:
            return "приплыли"
        if(article.name=="" or article.contact==""):
            return "При добавлении статьи возникли ошибки (поля пустые)!"
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи возникли ошибки!"
    else:
        return render_template("create-article.html", menu = menu)



@app.route('/posts')#страничка всех постов
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles, menu = menu)


@app.route('/posts/<int:id>')#страничка конкретного поста
def postDetail(id):
    article = Article.query.get(id)
    return render_template("post-detail.html", article=article, menu = menu)


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
        return render_template("post-update.html", article=article, menu = menu)
    

@app.route('/about')#страничка about
def about():
    return render_template("about.html", menu = menu)

@app.route('/test')#страничка test
def test():
    return render_template("test.html", menu = menu)

@app.route('/user/<name>')#страничка пользователя
@app.route('/user')#страничка пользователя
def user(name):
    if 'userLogged' not in session or session["userLogged"] !=name:
        abort(404)
    return render_template("user.html", name = name, menu = menu)


@app.route('/exit')
def exit():
    session["userLogged"] = ""
    return redirect(url_for('login'))

@app.route('/login', methods=["POST", "GET"])
def login():
    if 'userLogged' in session  and session["userLogged"] != "":
        return redirect(url_for('user',name = session['userLogged']))
    elif request.method == 'POST':
        users = Users.query.order_by(Users.date.desc()).all()
        goToUser=False
        for user in users:
            if (user.login == request.form["login"]) and (user.psw == request.form["password"]):
                goToUser=True
        if goToUser:        
            session["userLogged"] = request.form["login"]
            return redirect(url_for('user',name = session['userLogged']))
        return render_template("login.html", menu = menu)
    else:
        return render_template("login.html", menu = menu)
    
@app.route('/registration', methods=["POST", "GET"])
def registration():

    if 'userLogged' in session  and session["userLogged"] != "":
        return redirect(url_for('user',name = session['userLogged']))
    elif request.method == 'POST' and len(request.form["name"])>4 and len(request.form["password"])>5 and request.form["password"] == request.form["repassword"]: 
        session["userLogged"] = request.form["name"]
        user = Users(login=request.form["name"],psw=request.form["password"])
        profile = Profiles(contact = request.form["contact"], user_id = user.id)
        try:
            db.session.add(user)
            db.session.add(profile)
            db.session.commit()
            return redirect(url_for('user',name = session['userLogged']))
        except:
            return "При добавлении статьи возникли ошибки!"
        
    else:
        return render_template("registration.html", menu = menu)



@app.errorhandler(404)
def pageNotFount(error):
    return render_template("page404.html", menu = menu)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


