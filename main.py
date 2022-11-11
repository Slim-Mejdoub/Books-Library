from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, BooleanField, StringField, validators, FloatField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

app = Flask(__name__)
# CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///old-books-collection.db'
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = "any-string-you-want-just-keep-it-secret"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Float(120), nullable=False)


with app.app_context():
    db.create_all()


class BookForm(Form):
    book_name = StringField(label='Book Name', validators=[DataRequired()])
    book_author = StringField(label='Book Author', validators=[DataRequired()])
    rating = FloatField(label='Rating', validators=[DataRequired()])
    submit = SubmitField(label="Add Book")


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template('index.html', books=all_books)


@app.route('/add', methods=["GET", "POST"])
def add():
    form = BookForm()
    if request.method == "POST":
        add_book = Book(
            title=request.form["book_name"],
            author=request.form["book_author"],
            rating=request.form["rating"]
        )
        db.session.add(add_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html", form=form)


@app.route('/edit/<int:book_id>', methods=["GET", "POST"])
def edit(book_id):
    update_book = Book.query.get(book_id)
    if request.method == "POST":
        new_rate = request.form['rate']
        update_book.rating = new_rate
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", book=update_book)


@app.route('/delete/<int:book_id>', methods=["GET"])
def delete(book_id):
    delete_book = Book.query.get(book_id)
    db.session.delete(delete_book)
    db.session.commit()

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
