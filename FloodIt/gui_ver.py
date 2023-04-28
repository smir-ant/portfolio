# ==================== инициализация ====================
from random import choice, randint
from tkinter import *
from tkinter import messagebox

size = 15
RED = "#FF2400"
YELLOW="#FFDC33"
GREEN="#44944A"
BLUE="#6495ED"
PURPLE="#9966CC"
WHITE="#FFF8E7"
moves = round(size * 1.8)  # попыток = размерность x1.8 с округлением

# ==================== ФУНКЦИИ ДЕКОР ====================
def change_resolution(val):
    global resolution_value
    resolution_value = int(val)
    win.geometry(f"{240*resolution_value}x{160*resolution_value}")
    draw_buttons()
    draw_field()


def draw_buttons():
    global lifes  # Label с жизнями
    global fr
    fr.destroy()  # удаление предыдущего фрейма с внутренними элементами
    
    fr = Frame(win)    # создание нового фрейма
    fr.pack(side=LEFT, pady=20, anchor=NW)
    btn_width = 3 * resolution_value + 4
    Button(fr, text="Красный", bg=RED, command=lambda: turn("К"), width=btn_width, font=("Arial", 5 * resolution_value)).pack(pady=5)
    Button(fr, text="Желтый", bg=YELLOW, command=lambda: turn("Ж"), width=btn_width, font=("Arial", 5 * resolution_value)).pack(pady=5)
    Button(fr, text="Зеленый", bg=GREEN, command=lambda: turn("З"), width=btn_width, font=("Arial", 5 * resolution_value)).pack(pady=5)
    Button(fr, text="Синий", bg=BLUE, command=lambda: turn("С"), width=btn_width, font=("Arial", 5 * resolution_value)).pack(pady=5)
    Button(fr, text="Фиолетовый", bg=PURPLE, command=lambda: turn("Ф"), width=btn_width, font=("Arial", 5 * resolution_value)).pack(pady=5)
    Button(fr, text="Белый", bg=WHITE, command=lambda: turn("Б"), width=btn_width, font=("Arial", 5 * resolution_value)).pack(pady=5)
    lifes = Label(fr, text=f"Ходов: {moves}", font=("Arial", 5 * resolution_value))
    lifes.pack()

def draw_field():
    "Отрисовка поля"
    c.delete("all")
    c.config(width=20+size*10*resolution_value, height=20+size*10*resolution_value)
    y_coord = 10
    for row in range(size):
        x_coord = 10
        for column in range(size):
            c.create_rectangle(x_coord, y_coord, x_coord+10*resolution_value, y_coord+10*resolution_value,
                                fill=field[(row, column)],
                                outline='grey20'
                                )
            x_coord += 10*resolution_value
        y_coord += 10*resolution_value
    
    # выделение лево верх
    c.create_rectangle(10, 10, 10+10*resolution_value, 10+10*resolution_value,
                                fill=field[(0, 0)],
                                outline='black',
                                width=resolution_value
                                )

# ==================== ФУНКЦИИ МЕХАНИЗМ ====================
def change_tile(x, y, charToChange):
    "Смена плиток. С рекурсивным вызовом"
    if x == 0 and y == 0:
        if field[(x, y)] == charToChange:
            return True  # простой случай: тот же самый элемент

    field[(x, y)] = charToChange  # заменяем цвет

    if x > 0 and field[(x - 1, y)] == previos_color:
        change_tile(x=x-1, y=y, charToChange=charToChange)  # рекурсивно меняем символ СЛЕВА(-x)

    if x < size - 1 and field[(x + 1, y)] == previos_color:
        change_tile(x=x+1, y=y, charToChange=charToChange)  # рекурсивно меняем символ СПРАВА(+x)

    if y > 0 and field[(x, y - 1)] == previos_color:
        change_tile(x=x, y=y-1, charToChange=charToChange)  # рекурсивно меняем символ ВВЕРХ(-y)

    if y < size - 1 and field[(x, y+1)] == previos_color:
        change_tile(x=x, y=y+1, charToChange=charToChange)  # рекурсивно меняем символ ВНИЗ(+y)
    

def turn(choose):
    "Спрашиваем цвет и вызываем смену плиток"
    global moves
    global previos_color
    global lifes
    previos_color = field[(0, 0)]  # предыдущий цвет (это лево-верх)
    # нам пред. цвет нужен чтобы искать какие элементы соответвовали и их тоже красить в новый цвет

    if choose == "Б":
        if not change_tile(x=0, y=0, charToChange=WHITE):  # если та же клетка
            moves -= 1
    elif choose == "Ж":
        if not change_tile(x=0, y=0, charToChange=YELLOW):
            moves -= 1
    elif choose =="З":
        if not change_tile(x=0, y=0, charToChange=GREEN):
            moves -= 1
    elif choose == "К":
        if not change_tile(x=0, y=0, charToChange=RED):
            moves -= 1
    elif choose == "С":
        if not change_tile(x=0, y=0, charToChange=BLUE):
            moves -= 1
    else:
        if not change_tile(x=0, y=0, charToChange=PURPLE):
            moves -= 1
    
    draw_field()  # отрисовываем поле
    if is_win():
        draw_field()
        messagebox.showinfo(message="ТЫ ПОБЕДИЛ")
        quit()
    if moves == 0:
        draw_field()
        messagebox.showinfo(message="ТЫ ПРОИГРАЛ")
        quit()
    lifes['text'] = f"Ходов: {moves}"  # изменение кол-ва ходов



def is_win():
    global moves
    # првоеряем что клетки заполнены одним цветом
    for row in range(size):
        for column in range(size):
            if field[(row, column)] != field[(0, 0)]:
                return False  # если нашли не подходящую, то выход
    if moves >= 0:  # плюс если ходы ещё остались(равно это в последний ход)
        return True


# ========= Создание словаря со значениями =========
elements = (RED, YELLOW, GREEN, BLUE, PURPLE, WHITE)  # все цвета для случ. выбора
field = {}  # хранение в словаре, чтобы не выходить за пределы списка. {(2, 1): blue}
for row in range(size):
    for column in range(size):
        field[(row, column)] = choice(elements)  # случайно наполняем

# Делаем несколько элементов такими же, как соседний.
# В результате получаются группы элементов одинакового цвета/формы.
for i in range(size * 4):
    x = randint(0, size - 2)
    y = randint(0, size - 1)
    field[(x + 1, y)] = field[(x, y)]


# ===================
win = Tk()
win.title('Игра "Наводнение"')
resolution_scale = Scale(win, from_=2, to=4, command=change_resolution)
resolution_scale.pack(side=LEFT, anchor=NW)

c = Canvas(win, width=20+size*30, height=20+size*30, bg='white')
c.pack(side=LEFT, padx=10, anchor=NW)
fr = Frame(win)  # первичное объявление, чтобы было что удалять сперва

change_resolution(resolution_scale.get())  # первичное установление разрешения и установка размера всех элементов


draw_field()  # первичная отрисовка


win.mainloop()