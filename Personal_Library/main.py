from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
#Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CREATE TABLE
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)
db.create_all()


@app.route('/')
def home():
    # Read All Records
    all_books = db.session.query(Book).all()

    if not all_books:
        print('ARR')
    elif all_books:
        print(db.session.query(Book).all())
    return render_template('index.html', all_books=all_books)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == 'POST':
        data = request.form  # получаем данные с формы
        print(data)
        # print("Автор =", data["author"])
        new_book = Book(
            title=data["title"],
            author=data["author"],
            rating=data["rating"])  # создать новую запись
        db.session.add(new_book)  # добавить запись в бд
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('add.html')


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == 'POST':
        print('Покажите головку')

        book_id = request.form["id"]
        """ извлекаем рейтинг из формы, потому что отправляя get запрос мы не можем
        вытащить его через request.args.get, поэтому мы создали скрытый инпут, который мы также отправляем, в
        котором содержится id """
        book = Book.query.get(book_id)  # обращаемся к книге по id
        book.rating = request.form['rating']  # перезаписываем ей рейтинг, в данном случае
        db.session.commit()

        return redirect(url_for('home'))

    book_id = request.args.get('id')  # просто число, id книги, вытаскиваем из "http://127.0.0.1:5000/edit?id=1"
    print('book_id =', book_id)
    book = Book.query.get(book_id)  # из бд фиксируем книгу
    return render_template('edit.html', book=book)


@app.route("/delete")
def delete():
    book_id = request.args.get('id')  # забираем id из переданного через html
    book_to_delete = Book.query.get(book_id)  # из бд фиксируем книгу к удалению
    db.session.delete(book_to_delete)  # удаляем книгу
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)