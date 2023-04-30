from flask import Flask, render_template, redirect, url_for, flash, request, abort  # abort - поднимает ошибки
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from flask_gravatar import Gravatar
import os

app = Flask(__name__)

# ???
app_context = app.app_context()
app_context.push()

ckeditor = CKEditor(app)
Bootstrap(app)

# логин система
login_manager = LoginManager()
login_manager.init_app(app)


# подключение БД
app.secret_key = os.urandom(24)
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# ===================== БД =====================
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db. String(250), nullable=False)
    email = db.Column(db. String(250), nullable=False, unique=True)
    password = db.Column(db. String(250), nullable=False)
    role = db.Column(db.String(250), nullable=False)

    # This will act like    a List of BlogPost objects attached to each User.
    # The "author" refers to the author property in the BlogPost class.
    posts = db.relationship("BlogPost", backref='author')
    # backref - как мы должны ссылаться, то есть например post.author.name
    comments = db.relationship("Comment", backref='comment_author')


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)

    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    comments = db.relationship("Comment", backref='post')


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    parent_post = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))



db.create_all()

# ========================================


def admin_only(f):
    """
    Декоратор "если хост или админ..".
    Нуждается в "from functools import wraps"
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'host' and current_user.role != 'admin':
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/error')
def error(code):
    """
    Получаем код ошибки. Выдаем рендер страницы
    """
    return render_template(f'{code}.html')


@app.route('/')
def home():
    posts = BlogPost.query.all()  # получаем все посты
    return render_template("index.html", all_posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    0. Недопускает если уже авторизирован
    1. Проверка на уникалность почтового ящика;
    2. Хешируем пароль;
    3. Определяем нового пользователя и заносим его в БД;
    4. Осуществляем авторизацию в новый аккаунт.
    p.s. валидация на русские ФИ между 1 и 2 шагом в wtforms.validators внутри forms.py
    """
    if current_user.is_authenticated:  # если ты уже вошел, то не пущу)
        return redirect(url_for('home'))
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if User.query.filter_by(email=request.form.get('email')).first():  # если почта уже существует
                flash("Пользователь с такой электронной почтой уже существует.")
                return redirect(url_for('register'))
            else:  # если такой почты еще нет
                # то ХЭШим пароль
                hash_and_salted_password = generate_password_hash(
                    request.form.get('password'),
                    method='pbkdf2:sha256',
                    salt_length=8,
                )
                # определяем нового пользователя
                new_user = User(
                    email=request.form.get('email').lower(),
                    name=request.form.get('name').title(),
                    password=hash_and_salted_password,
                    role="user",  # по стандарту определяем как ученика/читателя
                )
                # заносим запись в бд
                db.session.add(new_user)
                db.session.commit()
                # авторизация
                login_user(new_user)
                return redirect(url_for('home'))
    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Получаем из формы email и password.
    Находим запись по почте.
    Нашли - пропустили. Нет пользователя - ошибка в почте. Есть пользователь но расхождения в паролях - ошибка в пароле.
    """
    if current_user.is_authenticated:  # если ты уже вошел, то не пущу)
        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == 'POST':
        email = request.form.get('email')  # фиксируем введенный ящик
        password = request.form.get('password')  # фиксируем введенный пароль
        user = User.query.filter_by(email=email).first()  # смотрим совпадения ящиков с бд
        if not user:
            flash("Проверь электронную почту.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash("Проверь пароль.")
            return redirect(url_for('login'))
        else:  # если пользователь такой есть и пароли совпадают
            login_user(user)
            return redirect(url_for('home'))
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    """ Функция выхода. """
    logout_user()  # функция flask-login'а
    return redirect(url_for('home'))


@app.route("/post/<int:post_id>", methods=['POST', 'GET'])
def show_post(post_id):
    gravatar = Gravatar(app,
                        size=100,
                        rating='g',
                        default='retro',
                        force_default=False,
                        force_lower=False,
                        use_ssl=False,
                        base_url=None)

    comment_form = CommentForm()
    requested_post = BlogPost.query.get(post_id)
    if request.method == 'POST':
        if comment_form.validate_on_submit():
            print('current_user = ', current_user)
            if not current_user.is_authenticated:
                flash('Чтобы оставлять комментарии необходим аккаунт.')
                return redirect(url_for('login'))

            new_post = Comment(
                text=comment_form.body.data,
                post=requested_post,
                comment_author=current_user,
            )
            # заносим запись в бд
            db.session.add(new_post)
            db.session.commit()
    return render_template("post.html", form=comment_form, post=requested_post, gravatar=gravatar)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/new-post", methods=['POST', 'GET'])
@login_required
@admin_only
def add_new_post():
    form = CreatePostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_post = BlogPost(
                title=form.title.data,
                subtitle=form.subtitle.data,
                body=form.body.data,
                img_url=form.img_url.data,
                author=current_user,
                date=date.today().strftime("%d.%m.%Y")
            )
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for("home"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=['GET', 'POST'])
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
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
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


# ========================= ОШИБКИ =========================
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def unauthorized(e):
    return render_template('errors/403.html'), 403
# ==========================================================


if __name__ == "__main__":
    app.run( debug=True)
