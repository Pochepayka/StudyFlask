from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template,url_for,request,redirect

app = Flask(__name__)#созданияе объекта по файлу app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
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
