from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Email, Length, ValidationError
from flask_ckeditor import CKEditorField


# ========================= собственные валидаторы =========================
def is_russian(form, field):
    """
    Собственный валидатор.
    Проходит валидацию если значение поля состоит из русских символов и пробелов.
    """
    russian = [' ', 'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й ', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у',
               'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'у', 'я']
    for letter in field.data.lower():  # даннные с поля в lowercase переводим
        if letter not in russian:
            print(f'Символ "{letter}" не русский')
            raise ValidationError('Пожалуйста, используйте исключительно русский алфавит')

    # print(list(" абвгдеёжзийклмнопрстуфхцчшщъыьэуя"))  # для получения символов русского языка + пробел
# ===========================================================================


# Форма ???
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# Форма для регистрации
class RegisterForm(FlaskForm):
    email = StringField(label='*Почта', validators=[DataRequired(message='Обязательно к заполнению'),
                                                    Email(message='Укажите действующую почту')])
    password = PasswordField(label='*Пароль', validators=[DataRequired(message='Обязательно к заполнению'),
                                                          Length(min=6, message='Минимальная длина 6')])
    name = StringField(label='*Фамилия и Имя', validators=[DataRequired(message='Обязательно к заполнению'),
                                                           is_russian])
    submit = SubmitField("Зарегистрироваться")


# форма для входа
class LoginForm(FlaskForm):
    email = StringField(label='Почта', validators=[DataRequired(message='Обязательно к заполнению'),
                                                   Email(message='Укажите действующую почту')])
    password = PasswordField(label='Пароль', validators=[DataRequired(message='Обязательно к заполнению')])
    submit = SubmitField("Войти")


# форма для комментария
class CommentForm(FlaskForm):
    body = CKEditorField(label='Написать комментарий')  # <--
    submit = SubmitField('Отправить')

