from flask import Flask, render_template, request
import requests

import smtplib  # библиотека для работы с почтовым протоколом
from email.mime.text import MIMEText  # для того чтобы кодировка и кириллица нормальными были
from email.header import Header  # для темы в письме, тоже на русском
smtp_host = 'smtp.gmail.com'  # smtp host
login = "ivanovich.py@gmail.com"  # адрес отрпавителя
password = "Secret"  # пароль отправителя
recipients_email = "email@email.here"  # адрес получаетеля

app = Flask(__name__)
npoint_response = requests.get('https://api.npoint.io/979434c3f92804827510').json()
print(npoint_response)

@app.route("/")
def home():
    return render_template('index.html', all_posts=npoint_response)


@app.route("/about")
def info_about():
    return render_template('about.html')


@app.route("/contact", methods=["POST", "GET"])
def info_contact():
    if request.method == 'POST':
        data = request.form
        print(data)
        # обращаемся к атрибуту name="..." внутри input
        print("Имя =", data["name"])
        print("Почта =", data["email"])
        print("Телефон =", data["phone"])
        print("Сообщение =", data["message"])


        msg = MIMEText(f'Имя: {data["name"]}\nПочта: {data["email"]}\nТелефон: {data["phone"]}\nСообщение: {data["message"]}', 'plain', 'utf-8')  # в тексте наше сообщение и ––– ?? plain ??
        msg['Subject'] = Header('Обратная связь.', 'utf-8')  # тема письма
        msg['From'] = login  # отправитель
        msg['To'] = recipients_email  # получатель

        with smtplib.SMTP(smtp_host, 587, timeout=10) as connection:  # и без '587, timeout=10' сработает
            # connection.set_debuglevel(1)  # устанавливаем подобный дебаг происходящего
            connection.starttls()  # tls - transport layer security - типа обеспечивает безопасность наших сообщений
            connection.login(login, password)  # входим в почту
            connection.sendmail(from_addr=['From'],
                                to_addrs=recipients_email,
                                msg=msg.as_string())  # отправляем письмо

        return render_template('contact.html', msg_sent=True)
    else:
        return render_template('contact.html', msg_sent=False)


@app.route("/post/<int:num>")
def get_post(num):
    return render_template('post.html', selected_post=npoint_response[num - 1])


if __name__ == '__main__':
    app.run(debug=True)
