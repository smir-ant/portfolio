from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired, NumberRange
import requests
import sqlalchemy
import os
from dotenv import load_dotenv  # для .env

app = Flask(__name__)
app_context = app.app_context()
app_context.push()
app.config['SECRET_KEY'] = os.urandom(24)

db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)


# DATABASE CLASS
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(80), nullable=True)
    img_url = db.Column(db.String(80), nullable=False)
db.create_all()


# //=================== WTFforms ============================\\
class UpdateRating(FlaskForm):
    rating = DecimalField(label='Оценка, от 0 до 10',
                          validators=[DataRequired(),
                                      NumberRange(min=0, max=10, message='От 0 до 10, пожалуйста.')])
    review = StringField(label='Твое мнение',
                         validators=[DataRequired(message='Необходимо заполнить.')])
    submit = SubmitField(label='Готово')


class AddMovie(FlaskForm):
    movie_title = StringField(label='Название фильма', validators=[DataRequired(message='Необходимо заполнить.')])
    submit = SubmitField(label='Добавить фильм')
# \\=======================================================//


# https://kinopoisk.dev/docs
kinopoisk_endpoint = 'https://api.kinopoisk.dev/movie'
file_env_path = os.path.join(os.path.dirname(__file__), 'secrets.env')  # в этой же папке
load_dotenv(file_env_path)  # подгружаем env
kinopoisk_token = os.getenv('TOKEN')  # фиксируем TOKEN=...



@app.route("/")
def home():
    # all_movies = db.session.query(Movie).all()  # это как без сортировки я раньше делал...
    all_movies = Movie.query.order_by(Movie.rating).all()  # достаем записи в сортировнном по рейтингу фиьлмы
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", all_movies=all_movies)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    update_rating = UpdateRating()  # создаем объект из класса с формами
    if update_rating.validate_on_submit():
        movie_id = request.args.get('id')  # фиксируем id
        movie = Movie.query.get(movie_id)  # берем фильм по primary_key
        movie.rating = update_rating.rating.data  # ОБНОВЕЛЕНИЕ РЕЙТИНГА
        movie.review = update_rating.review.data  # ОБНОВЕЛЕНИЕ ОТЗЫВА
        db.session.commit()
        return redirect(url_for('home'))
    # p.s. дублирую, чтобы избежать двойной работы кода, хоть и невидимой
    movie_id = request.args.get('id')
    movie = Movie.query.get(movie_id)
    return render_template('edit.html', movie_to_edit=movie, form=update_rating)  # передаем запись из бд посвященную фильму и форму flask-wtf


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    movie_id = request.args.get('id')
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/new_film', methods=['GET', 'POST'])
def new_film():
    if request.method == 'POST':
        movie_title = request.form['movie_title']
        print('movie_title =', movie_title)
        response = requests.get(f'{kinopoisk_endpoint}?search={movie_title}&field=name&isStrict=false&token={kinopoisk_token}&limit=50')
        print(response.status_code)  # статус кода
        print(response.headers)  # миллион всякой инфы
        print(response.json())  # по факту ющаем
        print(response.text)  # для json viewer
        print(type(response.json()))
        return render_template('select.html', response=response.json())

    add_movie = AddMovie()  # FlaskForm
    return render_template('add.html', form=add_movie)


@app.route('/add')
def add():
    movie_id_kp = request.args.get('id')
    response = requests.get(f'{kinopoisk_endpoint}?search={movie_id_kp}&field=id&token={kinopoisk_token}')
    # print(response.status_code)  # статус кода
    # print(response.headers)  # миллион всякой инфы
    # print(response.json())  # по факту юзаем
    # print(response.text)  # для json viewer
    # print(type(response.json()))

    # добавление в бд
    new_movie_info = {
        'id': response.json()['id'],
        'title': response.json()['name'],
        'year': response.json()['year'],
        'description': response.json()['description'],
        'poster_link': response.json()['poster']['url']
    }
    print(new_movie_info)

    new_movie = Movie(id=new_movie_info['id'],
                      title=new_movie_info['title'],
                      year=new_movie_info['year'],
                      description=new_movie_info['description'],
                      img_url=new_movie_info['poster_link'])
    db.session.add(new_movie)

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return redirect(url_for('new_film'))
    return redirect(url_for('edit', id=new_movie_info['id']))


if __name__ == '__main__':
    app.run(debug=True)
