"""Дисклеймер: если на google, например, вы долго не пользовались аккаунтом, 
то 'Вход в аккаунт Google через менее защищенные приложения' блокируется :)"""

from flask import Flask, render_template, request
import requests
import smtplib  # библиотека для работы с почтовым протоколом
from email.mime.text import MIMEText  # для того чтобы кодировка и кириллица нормальными были
from email.header import Header  # для темы в письме, тоже на русском
from dotenv import load_dotenv
import os

file_env_path = os.path.join(os.path.dirname(__file__), 'secrets.env')  # в этой же папке
load_dotenv(file_env_path)  # подгружаем env
smtp_host = os.getenv('SMTP_HOST')  # smtp host
login = os.getenv('SMTP_LOGIN')  # адрес отрпавителя
password = os.getenv('SMTP_PASSWORD')  # пароль отправителя

app = Flask(__name__)
@app.route("/", methods=["POST", "GET"])
def info_contact():
    if request.method == 'POST':
        data = request.form
        # обращаемся к атрибуту name="..." внутри input
        print("Имя =", data["name"])
        print("Почта =", data["email"])
        print("Телефон =", data["phone"])
        print("Сообщение =", data["message"])


        msg = MIMEText(f"""Ваша обратная связь принята. Вот ваши веденные данные:
                           - Имя: {data["name"]}
                           - Почта: {data["email"]}
                           - Телефон: {data["phone"]}
                           - Сообщение: {data["message"]}""", 'plain', 'utf-8')  # в тексте наше сообщение и ––– ?? plain ??
        print("MSG:", msg)
        msg['Subject'] = Header('Обратная связь.', 'utf-8')  # тема письма
        msg['From'] = login  # отправитель
        msg['To'] = data["email"]  # (кому отправлю обратную связь)

        with smtplib.SMTP(smtp_host, 587, timeout=10) as connection:  # и без '587, timeout=10' сработает
            # connection.set_debuglevel(1)  # устанавливаем подобный дебаг происходящего
            connection.starttls()  # tls - transport layer security - типа обеспечивает безопасность наших сообщений
            connection.login(login, password)  # входим в почту
            connection.sendmail(from_addr=['From'],
                                to_addrs=data["email"],
                                msg=msg.as_string())  # отправляем письмо

        return render_template('contact.html', msg_sent=True)
    else:
        return render_template('contact.html', msg_sent=False)


if __name__ == '__main__':
    app.run(debug=True)
