from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField(label='Название кафе ', validators=[DataRequired()])
    location = StringField(label='Расположение', validators=[DataRequired(), URL()])
    open_time = StringField(label='Открытие', validators=[DataRequired()])
    close_time = StringField(label='Закрытие', validators=[DataRequired()])
    coffee = SelectField('Кофе', choices=['❌', '☕️️', '☕️☕️', '☕☕☕️'])
    wifi = SelectField('Wi-Fi', choices=['❌️', '💪️', '💪💪️', '💪💪💪️️'])
    power = SelectField('Зарядка', choices=['❌️', '🔌', '🔌🔌️', '🔌🔌🔌️'])

    submit = SubmitField(label='Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    add_form = CafeForm()
    if add_form.validate_on_submit():
        print("True")
        with open('cafe-data.csv', "a") as cafe_data:
            cafe_data.write(f"\n{add_form.cafe.data},"
                            f"{add_form.location.data},"
                            f"{add_form.open_time.data},"
                            f"{add_form.close_time.data},"
                            f"{add_form.coffee.data},"
                            f"{add_form.wifi.data},"
                            f"{add_form.power.data}")

        print(f'{add_form.cafe.name} = {add_form.cafe.data}')
        return redirect(url_for('cafes'))
    return render_template('add.html', form=add_form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
