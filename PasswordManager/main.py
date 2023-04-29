from tkinter import *
from tkinter import messagebox  # типа другой класс/метод, и потому не импортируется если * :)
from random import shuffle, randint, choice
from pyperclip import copy  # для копирования в буфер обменв
import json  # будем хранить данные в json
import os
from functools import partial  # нужен как замена lambda в exec(в конце, в окне с просмотром паролей)

file_path = os.path.join(os.path.dirname(__file__), 'pass_file.json')  # ПУТЬ ДО JSON


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search_password():
    """Ищем пароль, проверяя на заполнение поля, существование файлаи содержание такой записи."""
    website = entry_website.get()
    if len(website) == 0:  # если хотя бы одно из полей пустое
        messagebox.showinfo(message='Сперва заполни поле.')
    else:
        try:
            with open(file_path, 'r') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:  # если файла не существует
            messagebox.showinfo(message='Файл с паролями отсутствует.')
        else:  # если мы открыли файл на чтение
            if website in data:  # если website есть в словаре из data
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
                with open(file_path, 'r') as data_file:
                    data_new = json.load(data_file)
            except FileNotFoundError:  # если файла не существует
                with open(file_path, 'w') as data_file:  # создаем его
                    json.dump(data, data_file, indent=4)  # запись в json свеженькое (indent=4 - отступы с 4 пробелами)
            else:  # если мы открыли файл на чтение
                data_new.update(data)  # добавляем нашу новую запись в записи
                with open(file_path, 'w') as data_file:
                    json.dump(data_new, data_file, indent=4)  # запись в json
            finally:  # в любом случае
                entry_website.delete(0, END)  # очистка поля website
                entry_password.delete(0, END)  # очистка поля password

                # копируем в буфер обмена
                messagebox.showinfo(message='Пароль скопирован в буфер обмена!')
                copy(password)  # pyperclip.copy() - копирование в буфер обмена


# ---------------------------- UI SETUP ------------------------------- #
root = Tk()
root.title('Password Manager')
root.config(padx=20, pady=20)
root.columnconfigure(0, weight=1)

# canvas
canvas_logo = Canvas(width=200, height=200, highlightthickness=0)
image_logo = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'img/logo.png'))
canvas_logo.create_image(100, 100, image=image_logo)
canvas_logo.grid(column=1, row=0)


# Label's
# ___ сайт
label_website = Label(text='Ресурс:')
label_website.grid(column=0, row=1, sticky=E)
# ___ почта
label_email = Label(text='Почта/Никнейм:')
label_email.grid(column=0, row=2, sticky=E)
# ___ пароль
label_password = Label(text='Пароль:')
label_password.grid(column=0, row=3, sticky=E)


# Entry's
# ___ сайт
entry_website = Entry()
entry_website.grid(column=1, row=1, sticky=EW, padx=5)
entry_website.focus()  # чтобы сразу курсор с начала был внутри
# ___ почта
entry_email = Entry()
entry_email.grid(column=1, row=2, columnspan=2, sticky=EW, padx=5)
entry_email.insert(0, 'abcsmir.ant@yandex.ru')  # автоввод почты автоматический
# ___ пароль
entry_password = Entry()
entry_password.grid(column=1, row=3, sticky=EW, padx=5)


# Spinbox
spinbox_symbols = Spinbox(from_=8, to=16, width=2)  # выбор длины генерируемого пароля от 8 до 16
spinbox_symbols.grid(column=3, row=3)


# Button's
# ___ поиск
button_search = Button(text='Поиск в базе', width=13, command=search_password)
button_search.grid(column=2, row=1, sticky=EW, padx=3)
# ___ генерация пароля
button_genpass = Button(text='Сгенерировать пароль', command=generate_password)
button_genpass.grid(column=2, row=3, sticky=EW, padx=3)
# ___ добавить
button_add = Button(text='Добавить',
                    command=save)  # 35=поле_для_ввода + 1=отступ_между_кнопкой_и_вводом(в 21 длину)
button_add.grid(column=1, row=4, columnspan=2, sticky=EW)


# ====================== Menu ======================
def spravka_help():
    messagebox.showinfo(title="Помощь", message="""РЕСУРС: вы должны вписать туда метку, по которой связка будет зафиксирована, ВК или Skype, например.
                                                   \nПОИСК В БАЗЕ: по введенной вами метке будет произведен поиск записей. Вы получите соответсующее сообщение.
                                                   \nСГЕНЕРИРОВАТЬ ПАРОЛЬ: справа от кнопки есть возможность выбора длины, после нажатия кнопки будет сгенерирован пароль этой длины.""")

def spravka_about():
    messagebox.showinfo(title="О программе", message="""Программа создана на чиле 29.04.2023
                                                        \nАвтор: github.com/smir-ant""")



def show_passwords():
    def lock_unlock_pass(cb_val, ent):
        # exec(f"ent{indx}pass.config(show='')")
        if cb_val.get():  # если нажато(глазки)
            ent["show"] = ""
        else:  # если отжато(скрыть)
            ent["show"] = "*"

    try:
        with open(file_path, 'r') as data_file:
                data = json.load(data_file)
    except FileNotFoundError:  # если файла не существует
        messagebox.showerror(title="Отказано", message="Записи отсутствуют.")
        return  # выйдем из функции. То есть дальше пройдем только если есть записи
    
    window = Toplevel()
    window.title("Ваши данные")
    window.geometry(f"690x{50*len(data)}")
    
    # Button(window, image={monkey_img}).grid(row=6, column=6, pady=5)
    # exec(f"")
    # partial()

    for indx, record in enumerate(data):
        exec(f"Label(window, text='Ресурс:').grid(row={indx}, column=0, padx=4)")
        exec(f"ent{indx}resource = Entry(window)")
        exec(f"ent{indx}resource.grid(row={indx}, column=1, pady=5)")
        exec(f"ent{indx}resource.insert(0, '{record}')")
        exec(f"ent{indx}resource['state'] = 'readonly'")

        exec(f"Label(window, text='Почта:').grid(row={indx}, column=2, padx=8)")
        exec(f"ent{indx}email = Entry(window, width=30)")
        exec(f"ent{indx}email.grid(row={indx}, column=3, pady=5)")
        exec(f"ent{indx}email.insert(0, '{data[record]['email']}')")
        exec(f"ent{indx}email['state'] = 'readonly'")

        exec(f"Label(window, text='Пароль:').grid(row={indx}, column=4, padx=8)")
        exec(f"ent{indx}pass = Entry(window, width=25)")
        exec(f"ent{indx}pass.grid(row={indx}, column=5, pady=5)")
        exec(f"ent{indx}pass.insert(0, '{data[record]['password']}')")
        exec(f"ent{indx}pass.config(state='readonly', show='*')")

        exec(f"cb{indx}_val = BooleanVar()")
        exec(f"""Checkbutton(window, 
                             image=monkey_img, 
                             selectimage=eyes_img, 
                             indicatoron=False,
                             bg='#C6DF90',
                             selectcolor='#FF9BAA',
                             variable=cb{indx}_val,
                             command=partial(lock_unlock_pass, cb{indx}_val, ent{indx}pass), 
                             bd=3).grid(row={indx}, column=6, pady=3, padx=3)""")
        # к сожалению, использование lambda в exec в функции ведущей к другой функции не даёт, 
        # ибо NameError: name 'lock_unlock_pass' is not defined
       
    window.mainloop()



mainmenu = Menu(root)

list_passwords = Menu(mainmenu, tearoff=0)
mainmenu.add_cascade(label="Список паролей", command=show_passwords)  # размещаем пункт меню
monkey_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'img/monkey.png')).subsample(7,7)
eyes_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'img/eyes.png')).subsample(7,7)
    

helpmenu = Menu(mainmenu, tearoff=0)  # tearoff 0 отключает функцию открепления меню
root.config(menu=mainmenu)
mainmenu.add_cascade(label="Справка", menu=helpmenu)  # размещаем пункт меню
helpmenu.add_command(label="Помощь",  command=spravka_help)  # вкладываем подпункт
helpmenu.add_command(label="О программе", command=spravka_about)  # вкладываем подпункт



root.bind("<Destroy>", quit)  # закрытие всего, если главное окно закрыто :)
root.mainloop()
