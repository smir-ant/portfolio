from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
ONE_CIRCLE_ROUNDS = 4  # сколько у нас в одном круге полном будет заходов
REPS = 0  # учет сколько заходов(раундов) уже совершенно в круге
TIMER = None
# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    """Сброс всего и возврат к начальному"""
    global REPS  # для сброса

    window.after_cancel(TIMER)  # останавливаем ход времени в нашем таймере
    REPS = 0  # сбрасываем наш прогресс
    label_checkmarks.config(text='')  # стираем галочки
    label_timer.config(text='Timer', fg=GREEN)  # меняем статус на начальное 'Timer'
    canvas_tomato.itemconfig(timer_text, text='00:00')  # сбрасываем время


# ---------------------------- TIMER MECHANISM ------------------------------- #


def timer_start():
    global REPS
    REPS += 1
    if REPS % (2 * ONE_CIRCLE_ROUNDS) == 0:
        count_down(LONG_BREAK_MIN * 10)
        label_timer.config(text='Break', fg=GREEN)
    elif REPS % 2 == 0:
        count_down(SHORT_BREAK_MIN * 60)
        label_timer.config(text='Break', fg=PINK)
    else:
        count_down(WORK_MIN * 60)
        label_timer.config(text='Work', fg=RED)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
"""Здесь есть прикол, что мы не может через import time и time.delay(1) в цикле  while True реализовать, ибо здесь
цикл построчный типа, ну то бишь он тогда не обновит программу(вроде как), потому что не может цикл сделать и
следовательно до следующего шага для обновления дойти"""


def count_down(count):
    global TIMER

    count_min = count // 60
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f'0{count_sec}'  # чтобы 4:3 превратились в 4:03

    canvas_tomato.itemconfig(timer_text, text=f'{count_min}:{count_sec}')  # конфигурирем наш холст, точнее его
    # элемент(текст)
    if count > 0:
        TIMER = window.after(1000, count_down, count - 1)  # 1000ms = 1sec, вызывает саму себя, типа чтобы она
        # вызывалась после тогокак пройдет секунда. Запихана в переменную чтобы потом можно было остановить
    else:  # то есть если таймер заканчивается
        timer_start()  # мы уходим в механизм таймера(нужно ли еще отсчитывать..)

        checkmarks = ''  # переменная для галочек
        work_session = REPS // 2  # считаем сколько раундова 'work' пройдено, дальше мы столько же галочек рисуем
        for _ in range(work_session):
            checkmarks += '✓'  # устанавливаем засечки-галочки и следом заменяем
        label_checkmarks.config(text=checkmarks, fg=GREEN, bg=YELLOW, font=(FONT_NAME, 35, 'bold'))  # меняем label


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Pomodoro')
window.config(padx=100, pady=50, bg=YELLOW)  # фон у окна(у помидара(canvas) фон будет белым(стандартным))

# label 'Timer'
label_timer = Label(text='Timer', fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
label_timer.grid(column=1, row=0)

# canvas
canvas_tomato = Canvas(width=200, height=224, bg=YELLOW,
                       highlightthickness=0)  # highlightthickness=0 – минус обрамление
tomato_img = PhotoImage(file='tomato.png')
canvas_tomato.create_image(100, 112, image=tomato_img)  # типа якорь в центре & canvas кушает только такой тип данных
timer_text = canvas_tomato.create_text(100, 130, text='00:00', fill='white', font=(FONT_NAME, 35, 'bold'))
canvas_tomato.grid(column=1, row=1)


# button 'Start'
button_start = Button(text='Start', highlightthickness=0, command=timer_start)
button_start.grid(column=0, row=2)

# button 'Reset'
button_start = Button(text='Reset', highlightthickness=0, command=reset_timer)
button_start.grid(column=2, row=2)

# label with checkmarks
label_checkmarks = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 35, 'bold'))
label_checkmarks.grid(column=1, row=3)

window.mainloop()