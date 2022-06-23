from tkinter import *
from tkinter import messagebox  # типа другой класс/метод, и потому не импортируется если * :)
from random import shuffle, randint, choice
from pyperclip import copy  # для копирования в буфер обменв
import json  # будем хранить данные в json


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search_password():
    """Ищем пароль, проверяя на заполнение поля, существование файлаи содержание такой записи."""
    website = entry_website.get()
    if len(website) == 0:  # если хотя бы одно из полей пустое
        messagebox.showinfo(message='Сперва заполни поле.')
    else:
        try:
            with open('pass_file.json', 'r') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:  # если файла не существует
            messagebox.showinfo(message='Файл с паролями отсутствует.')
        else:  # если мы открыли файл на чтение
            if website in data:  # !!!! если website есть в словаре из data
                # messagebox.
                messagebox.showinfo(message=f'Website: {website}\n'
                                            f'Login: {data[website]["email"]}\n'
                                            f'Password: {data[website]["password"]}')
            else:
                messagebox.showinfo(message=f'Пароля для сайта "{website}" не существует')


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """Генерирум пароль, взято из 6-го дня, хехе, ну и модифицировано неслабо, собственно"""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = int(spinbox_symbols.get())  # сколько знаков всего (букв = общее - спец.символы - цифры
    nr_symbols = randint(2, 4)  # сколько спец. символов
    nr_numbers = randint(2, 4)  # сколько цифр

    # ГЕНЕРИРОВАНИЕ.
    # генерируем элементов' через List comprehension
    password_fragments_letters = [choice(letters) for _ in range(0, nr_letters - nr_numbers - nr_symbols)]
    password_fragments_symbols = [choice(symbols) for _ in range(0, nr_symbols)]
    password_fragments_numbers = [choice(numbers) for _ in range(0, nr_numbers)]

    password_fragments = password_fragments_letters + password_fragments_symbols + password_fragments_numbers
    # объединяем элементы

    shuffle(password_fragments)  # перемешивает массив этот

    password_generated = ''.join(password_fragments)  # из массива в строку c разделителем(по факту пустым)

    # ВЫВОД
    entry_password.delete(0, END)  # очистка поля сперва
    entry_password.insert(0, f'{password_generated}')  # очистка поля password


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    """Функция сохранения пароляв json формат. Исключено несуществование файла. Подтверждаем ввод, очищаем поля и
    копируем в буфер обмена."""
    website = entry_website.get()
    email = entry_email.get()
    password = entry_password.get()
    data = {
        website: {
            "email": email,
            'password': password,
        }
    }
    if len(website) == 0 or len(password) == 0:  # если хотя бы одно из полей пустое
        messagebox.showinfo(message='Ты недописал(')
    else:
        is_save = messagebox.askyesno(title=entry_website.get(), message=f'Сохраняем для {website} \nПочта: {email}'
                                                                         f'\nПароль: {password}'
                                                                         f'\n\nСохраняем?')
        if is_save:  # если мы подтвердили сохранение
            try:
                with open('pass_file.json', 'r') as data_file:
                    data_new = json.load(data_file)
            except FileNotFoundError:  # если файла не существует
                with open('pass_file.json', 'w') as data_file:  # создаем его
                    json.dump(data, data_file, indent=4)  # запись в json свеженькое (indent=4 - отступы с 4 пробелами)
            else:  # если мы открыли файл на чтение
                data_new.update(data)  # добавляем нашу новую запись в записи
                with open('pass_file.json', 'w') as data_file:
                    json.dump(data_new, data_file, indent=4)  # запись в json
            finally:  # в любом случае
                entry_website.delete(0, END)  # очистка поля website
                entry_password.delete(0, END)  # очистка поля password

                # копируем в буфер обмена
                messagebox.showinfo(message='Пароль скопирован в буфер обмена!')
                copy(password)  # pyperclip.copy() - копирование в буфер обмена


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Password Manager')
window.config(padx=20, pady=20)

# canvas
canvas_logo = Canvas(width=200, height=200, highlightthickness=0)
image_logo = PhotoImage(file='logo.png')
canvas_logo.create_image(100, 100, image=image_logo)
canvas_logo.grid(column=1, row=0)


# Label's
# ___ сайт
label_website = Label(text='Website:')
label_website.grid(column=0, row=1)
# ___ почта
label_email = Label(text='Email/Username:')
label_email.grid(column=0, row=2)
# ___ пароль
label_password = Label(text='Password:')
label_password.grid(column=0, row=3)


# Entry's
# ___ сайт
entry_website = Entry(width=21)
entry_website.grid(column=1, row=1)
entry_website.focus()  # чтобы сразу курсор с начала был внутри
# ___ почта
entry_email = Entry(width=35)
entry_email.grid(column=1, row=2, columnspan=2)
entry_email.insert(0, 'abcsmir.ant@yandex.ru')  # автоввод почты автоматический
# ___ пароль
entry_password = Entry(width=21)
entry_password.grid(column=1, row=3)


# Spinbox
spinbox_symbols = Spinbox(from_=8, to=16, width=2)  # выбор длины генерируемого пароля от 8 до 16
spinbox_symbols.grid(column=3, row=3)


# Button's
# ___ поиск
button_search = Button(text='Search', width=13, command=search_password)
button_search.grid(column=2, row=1)
# ___ генерация пароля
button_genpass = Button(text='Generate Password', command=generate_password)
button_genpass.grid(column=2, row=3)
# ___ добавить
button_add = Button(text='Add', width=36,
                    command=save)  # 35=поле_для_ввода + 1=отступ_между_кнопкой_и_вводом(в 21 длину)
button_add.grid(column=1, row=4, columnspan=2)


window.mainloop()