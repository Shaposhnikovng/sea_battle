from tkinter import *
from tkinter import messagebox
import time
import random

tk = Tk() # создан объект
app_running = True

# ПОЛЕ
size_canvas_x = 500 # размеры поля
size_canvas_y = 500 # размеры поля
s_x = s_y = 6 # размер игрового поля сколько ячеек (не меньше 8 и не больше 18)
# s_y = 12 # для нессиметричного поля
step_x = size_canvas_x // s_x # шаг по горизонтали
step_y = size_canvas_y // s_y # шаг по вертикали
size_canvas_x = step_x * s_x # масштабируемый размер поля по x
size_canvas_y = step_y * s_y # масштабируемый размер поля по y

txt_len_middle = "* Человек против Компьютера"
size_font_x = 10
len_txt_x = len(txt_len_middle)*size_font_x
print(len_txt_x)

delta_menu_x = len_txt_x // step_x + 1
menu_x = step_x * delta_menu_x  # 250 размер меню справа
menu_y = 40

# корабли
ships =  s_x // 2 # определяем максимально количество кораблей для игрового поля
print(ships)
ship_len1 = s_x // 5 # длина первого типа корабля
print(ship_len1)
ship_len2 = s_x // 3 # длина второго типа корабля
print(ship_len2)
ship_len3 = s_x // 2 # длина третьего типа корабля
print(ship_len3)
#ships_len3 = s_x // 6 # длина четвертого типа корабля
enemy_ships1 = [[0 for i in range(s_x+1)] for i in range(s_y+1)] # корректирвока количества кораблей под размер поля
enemy_ships2 = [[0 for i in range(s_x+1)] for i in range(s_y+1)]
# enemy_ships1 = [[0 for i in range(s_x)] for i in range(s_y)] # корректирвока количества кораблей под размер поля для не симметричного поля
# print(enemy_ships1) # вывод
list_ids = [] # спиоск объектов canvas
# points1 - список, куда мы кликнули мышкой
points1 = [[-1 for i in range(s_x)] for i in range(s_y)]
points2 = [[-1 for i in range(s_x)] for i in range(s_y)]

#  boom - список попадания по кораблям противника
boom = [[0 for i in range(s_x)] for i in range(s_y)]

# список кораблей игрока 1 и 2
ships_list = []

# Если истина, то ходит игрок № 1, иначе ходит игрок № 2
hod_igrovomu_polu_1 = False

# Если истина, то играем против компьютера
computer_vs_human = False
if computer_vs_human:
    add_to_label = " (Компьютер) "
    add_to_label2 = " (прицеливается... ) "
    hod_igrovomu_polu_1 = False
else:
    add_to_label = ""
    add_to_label2 = ""
    hod_igrovomu_polu_1 = False

def on_closing(): # меню выхода. когда закрываем окно
    global app_running
    if messagebox.askokcancel("Выход из игры", "Хотите выйти из игры?"):
        app_running = False
        tk.destroy()

# РАЗМЕР ИГРОВОГО ПОЛЯ
tk.protocol("WM_DELETE_WINDOW", on_closing) # наименование игры и выход поверх окон
tk.title("Игра Морской бой") # наименование программы
tk.register(0, 0) # нельзя изменять размер
tk.wm_attributes("-topmost", 1) # окно поверх других окон при запуске
canvas = Canvas(tk, width = size_canvas_x + menu_x + size_canvas_x, height = size_canvas_y + menu_y, bd = 0, highlightthickness = 0) # размер окна
canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill="white")  # рисование прямоугольника игровой области, заливка белым цветом
canvas.create_rectangle(size_canvas_x+menu_x, 0, size_canvas_x + menu_x + size_canvas_x, size_canvas_y, fill = "lightyellow")
canvas.pack() # запаковка
tk.update() # обновление

# ОТРИСОВКА ПОЛЯ
def draw_table(offset_x=0): # рисование сетки
    for i in range (0, s_x + 1):
        canvas.create_line(offset_x + step_x * i, 0, offset_x + step_x * i, size_canvas_y)
    for i in range (0, s_y + 1):
        canvas.create_line(offset_x, step_y * i, offset_x + size_canvas_x, step_y * i)

draw_table()
draw_table(size_canvas_x + menu_x) # меню справа

# Надпись Игрок 1 и Игрок 2
t0 = Label(tk, text ="Игрок № 1", font = ("Helvetica", 16))
t0.place(x=size_canvas_x // 2 - t0.winfo_reqwidth() // 2, y=size_canvas_y + 3)
t1 = Label(tk, text="Игрок № 2"+add_to_label, font=("Helvetica", 16))
t1.place(x=size_canvas_x + menu_x + size_canvas_x // 2 - t1.winfo_reqwidth() // 2, y=size_canvas_y + 3)

t0.configure(bg="red") # подсветка ходящего игрока красным
t0.configure(bg='#f0f0f0')

t3 = Label(tk, text="Игрок № 1", font=("Helvetica", 16))
# t3.place(x = size_canvas_x + step_x //2, y = 3 * step_y)
t3.place(x = size_canvas_x // 2 - t0.winfo_reqwidth() // 2, y=size_canvas_y)

def change_rb():
    global computer_vs_human, add_to_label, add_to_label2
    print(rb_var.get())
    if rb_var.get():
        computer_vs_human = True
        add_to_label = " (Компьютер) "
        add_to_label2 = " (прицеливается... ) "
    else:
        computer_vs_human = False
        add_to_label = ""
        add_to_label2 = ""

# КНОПКИ ВЫБОРА ИГРОКА
rb_var = BooleanVar()
rb1 = Radiobutton(tk, text="Человек против Компьютера", variable=rb_var, value=1, command=change_rb)
rb2 = Radiobutton(tk, text="Человек против Человека", variable=rb_var, value=0, command=change_rb)
rb1.place(x=size_canvas_x + menu_x // 2 - rb1.winfo_reqwidth() // 2, y=120)
rb2.place(x=size_canvas_x + menu_x // 2 - rb2.winfo_reqwidth() // 2, y=140)
if computer_vs_human:
    rb1.select()

def mark_igrok(igrok_mark_1): # расположение и обозначение игроков
    if igrok_mark_1:
        t0.configure(bg="red")
        t0.configure(text="Игрок № 1!"+add_to_label2)
        t0.place(x=size_canvas_x // 2 - t0.winfo_reqwidth() // 2, y=size_canvas_y + 3)
        t1.configure(text="Игрок № 2!" + add_to_label)
        t1.place(x=size_canvas_x + menu_x + size_canvas_x // 2 - t1.winfo_reqwidth() // 2, y=size_canvas_y + 3)
        t1.configure(bg='#f0f0f0')
        t3.configure(text="Ход Игрока № 2!"+add_to_label)
        t3.place(x=size_canvas_x + menu_x // 2 - t3.winfo_reqwidth() // 2, y=size_canvas_y)

    else:
        t1.configure(bg='red')
        t0.configure(bg="#f0f0f0")
        t0.configure(text="Игрок № 1!")
        t0.place(x=size_canvas_x // 2 - t0.winfo_reqwidth() // 2, y=size_canvas_y + 3)
        t1.configure(text="Игрок № 2!" + add_to_label)
        t1.place(x=size_canvas_x + menu_x + size_canvas_x // 2 - t1.winfo_reqwidth() // 2, y=size_canvas_y + 3)
        t3.configure(text="Ход Игрока № 1!")
        t3.place(x=size_canvas_x + menu_x // 2 - t3.winfo_reqwidth() // 2, y=size_canvas_y)


mark_igrok(hod_igrovomu_polu_1)

def button_show_enemy1(): # кнопка показать корабли противника
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships1[j][i] > 0:
                color = "red"
                if points1[j][i] != -1:
                    color = "green"
                _id = canvas.create_rectangle(i * step_x, j * step_y, i * step_x + step_x, j * step_y + step_y,
                                              fill=color)
                list_ids.append(_id)

def button_show_enemy2(): # кнопка показать корабли противника
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships2[j][i] > 0:
                color = "red"
                if points2[j][i] != -1:
                    color = "green"
                _id = canvas.create_rectangle(size_canvas_x + menu_x + i * step_x, j * step_y, size_canvas_x + menu_x + i * step_x + step_x, j * step_y + step_y,
                                              fill=color)
                list_ids.append(_id)

def button_begin_again(): # кнопка начать заново
    global list_ids
    global points1, points2
    global boom
    global enemy_ships1, enemy_ships2
    for el in list_ids:
        canvas.delete(el)
    list_ids = []
    generate_ships_list()
    # print(ships_list)
    enemy_ships1 = generate_enemy_ships()
    enemy_ships2 = generate_enemy_ships()
    points1 = [[-1 for i in range(s_x)] for i in range(s_y)]
    points2 = [[-1 for i in range(s_x)] for i in range(s_y)]
    boom = [[0 for i in range(s_x)] for i in range(s_y)]

# КНОПКИ
b0 = Button(tk, text="Показать корабли Игрок № 1", command=button_show_enemy1) # расположение кнопки показать корабли
b0.place(x=size_canvas_x + menu_x // 2 - b0.winfo_reqwidth() // 2, y=10)

b1 = Button(tk, text="Показать корабли Игрок № 2", command=button_show_enemy2) # расположение кнопки показать корабли
b1.place(x=size_canvas_x + menu_x // 2 - b1.winfo_reqwidth() // 2, y=40)

b2 = Button(tk, text="Начать заново", command=button_begin_again) # расположение кнопки начать заново
b2.place(x=size_canvas_x + + menu_x // 2 - b2.winfo_reqwidth() // 2, y=80)

def draw_point(x, y):
    # print(enemy_ships1[y][x])
    if enemy_ships1[y][x] == 0:
        color = "red"
        id1 = canvas.create_oval(x * step_x, y * step_y, x * step_x + step_x, y * step_y + step_y, fill=color)
        id2 = canvas.create_oval(x * step_x + step_x // 3, y * step_y + step_y // 3, x * step_x + step_x - step_x // 3,
                                 y * step_y + step_y - step_y // 3, fill="white")
        list_ids.append(id1)
        list_ids.append(id2)
    if enemy_ships1[y][x] > 0:
        color = "blue"
        id1 = canvas.create_rectangle(x * step_x, y * step_y + step_y // 2 - step_y // 10, x * step_x + step_x,
                                      y * step_y + step_y // 2 + step_y // 10, fill=color)
        id2 = canvas.create_rectangle(x * step_x + step_x // 2 - step_x // 10, y * step_y,
                                      x * step_x + step_x // 2 + step_x // 10, y * step_y + step_y, fill=color)
        list_ids.append(id1)
        list_ids.append(id2)

def draw_point2(x, y, offset_x = size_canvas_x + menu_x):
    # print(enemy_ships1[y][x])
    if enemy_ships2[y][x] == 0:
        color = "red"
        id1 = canvas.create_oval(offset_x + x * step_x, y * step_y, offset_x + x * step_x + step_x, y * step_y + step_y, fill=color)
        id2 = canvas.create_oval(offset_x + x * step_x + step_x // 3, y * step_y + step_y // 3, offset_x + x * step_x + step_x - step_x // 3,
                                 y * step_y + step_y - step_y // 3, fill="white")
        list_ids.append(id1)
        list_ids.append(id2)
    if enemy_ships2[y][x] > 0:
        color = "blue"
        id1 = canvas.create_rectangle(offset_x + x * step_x, y * step_y + step_y // 2 - step_y // 10, offset_x + x * step_x + step_x,
                                      y * step_y + step_y // 2 + step_y // 10, fill=color)
        id2 = canvas.create_rectangle(offset_x + x * step_x + step_x // 2 - step_x // 10, y * step_y,
                                      offset_x + x * step_x + step_x // 2 + step_x // 10, y * step_y + step_y, fill=color)
        list_ids.append(id1)
        list_ids.append(id2)

def check_winner(x, y):
    win = False
    if enemy_ships1[y][x] > 0:
        boom[y][x] = enemy_ships1[y][x]
    sum_enemy_ships1 = sum(sum(i) for i in zip(*enemy_ships1))
    sum_boom = sum(sum(i) for i in zip(*boom))
    #print(sum_enemy_ships1, sum_boom)
    if sum_enemy_ships1 == sum_boom:
        win = True
    return win

def check_winner2():
    win = True
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships1[j][i] > 0:
                if points1[j][i] == -1:
                    win = False
    #print(win)
    return win

def check_winner2_igrok_2():
    win = True
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships2[j][i] > 0:
                if points2[j][i] == -1:
                    win = False
    #print(win)
    return win

def hod_computer():
    global points1, points2, hod_igrovomu_polu_1
    tk.update()
    time.sleep(1)
    hod_igrovomu_polu_1 = False
    ip_x = random.randint(0, s_x - 1)  # для определения координат ячейки на экране по x
    ip_y = random.randint(0, s_y - 1)  # для определения координат ячейки на экране по y
    # print(ip_x, ip_y)
    while not points1[ip_y][ip_x] == -1:
        ip_x = random.randint(0, s_x - 1)  # для определения координат ячейки на экране по x
        ip_y = random.randint(0, s_y - 1)  # для определения координат ячейки на экране по y
    points1[ip_y][ip_x] = 7
    draw_point(ip_x, ip_y)
    if check_winner2():
        winner = "ПОБЕДА ИГРОКА № 2 !" + add_to_label
        winner_add = "(Все корабли противника Игрока №1 уничтожены)"
        print("\twinner,\n\twinner_add")
        # print("ПОБЕДА ИГРОКА № 2 (Все корабли противника Игрока № 1 уничтожены)!")
        points1 = [[10 for i in range(s_x)] for i in range(s_y)]
        points2 = [[10 for i in range(s_x)] for i in range(s_y)]
        id1 = canvas.create_rectangle(step_x * 3, step_y * 3, size_canvas_x + menu_x + size_canvas_x - step_x * 3,
                                      size_canvas_y - step_y, fill="blue")
        list_ids.append(id1)
        id2 = canvas.create_rectangle(step_x * 3 + step_x // 2, step_y * 3 + step_y // 2,
                                      size_canvas_x + menu_x + size_canvas_x - step_x * 3 - step_x // 2,
                                      size_canvas_y - step_y - step_y // 2, fill="yellow")
        list_ids.append(id2)
        id3 = canvas.create_text(step_x * 10, step_y * 5, text=winner, font=("Arial", 50), justify=CENTER)
        id4 = canvas.create_text(step_x * 10, step_y * 6, text=winner_add, font=("Arial", 25), justify=CENTER)
        list_ids.append(id3)
        list_ids.append(id4)


def add_to_all(event):  # нажатие кнопок
    global points1, points2, hod_igrovomu_polu_1
    _type = 0 # ЛКМ
    if event.num == 3:
        _type = 1 # ПКМ
    #print(_type) # вывод номера кнопки
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx() # координаты по x (координата внутри окшка, а не экрана)
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty() # координаты по y (координата внутри окшка, а не экрана)
    #print(mouse_x, mouse_y) # вывод координат клика
    ip_x = mouse_x // step_x # для определения координат ячейки на экране по x
    ip_y = mouse_y // step_y  # для определения координат ячейки на экране по y
    print(ip_x, ip_y, "_type: ", _type)

    # первое игровое поле
    if ip_x < s_x and ip_y < s_y and hod_igrovomu_polu_1: # последовательность хода
        if points1[ip_y][ip_x] == -1:
            points1[ip_y][ip_x] = _type
            hod_igrovomu_polu_1 = False # последовательность хода
            draw_point(ip_x, ip_y)
            # if check_winner(ip_x, ip_y):
            if check_winner2():
                hod_igrovomu_polu_1 = True
                winner = "ПОБЕДА ИГРОКА № 2 !"
                winner_add = "(Все корабли противника Игрока №1 уничтожены)"
                print("\twinner,\n\twinner_add")
                # print("ПОБЕДА ИГРОКА № 2 (Все корабли противника Игрока № 1 уничтожены)!")
                points1 = [[10 for i in range(s_x)] for i in range(s_y)]
                points2 = [[10 for i in range(s_x)] for i in range(s_y)]
                id1 = canvas.create_rectangle(step_x*3, size_canvas_y // 2, size_canvas_x + menu_x + size_canvas_x-step_x*3, size_canvas_y // 2+step_y+step_y // 2 + 50 + 25 + step_y // 2, fill="blue")
                list_ids.append(id1)
                id2 = canvas.create_rectangle(step_x * 3+step_x//2, size_canvas_y // 2 +step_y//2,
                                              size_canvas_x + menu_x + size_canvas_x - step_x * 3 - step_x//2,
                                              size_canvas_y // 2+step_y+step_y // 2 + 50 + 25 + step_y // 2 - step_y//2, fill="yellow")
                list_ids.append(id2)
                id3 = canvas.create_text(size_canvas_x+menu_x//2, size_canvas_y // 2+step_y+step_y // 2, text=winner, font=("Arial", 50), justify=CENTER)
                id4 = canvas.create_text(size_canvas_x+menu_x//2, size_canvas_y // 2+step_y+step_y // 2 + 50, text=winner_add, font=("Arial", 25), justify=CENTER)
                list_ids.append(id3)
                list_ids.append(id4)
        # print(len(list_ids))

    # второе игровое поле
    if ip_x >= s_x + delta_menu_x and ip_x <= s_x + s_x + delta_menu_x and ip_y < s_y and not hod_igrovomu_polu_1: # последовательность хода
        # print("ok")
        if points2[ip_y][ip_x - s_x - delta_menu_x] == -1:
            points2[ip_y][ip_x - s_x - delta_menu_x] = _type
            hod_igrovomu_polu_1 = True # последовательность хода
            draw_point2(ip_x - s_x - delta_menu_x, ip_y)
            # if check_winner(ip_x, ip_y):
            if check_winner2_igrok_2():
                hod_igrovomu_polu_1 = False
                winner = "ПОБЕДА ИГРОКА № 1 !"
                winner_add = "(Все корабли противника Игрока №2 уничтожены)"
                print("\twinner,\n\twinner_add")
                # print("ПОБЕДА ИГРОКА №1 (Все корабли противника Игрока №2 уничтожены)!")
                points1 = [[10 for i in range(s_x)] for i in range(s_y)]
                points2 = [[10 for i in range(s_x)] for i in range(s_y)]
                id1 = canvas.create_rectangle(step_x * 3, size_canvas_y // 2,
                                              size_canvas_x + menu_x + size_canvas_x - step_x * 3,
                                              size_canvas_y // 2 + step_y + step_y // 2 + 50 + 25 + step_y // 2,
                                              fill="blue")
                list_ids.append(id1)
                id2 = canvas.create_rectangle(step_x * 3 + step_x // 2, size_canvas_y // 2 + step_y // 2,
                                              size_canvas_x + menu_x + size_canvas_x - step_x * 3 - step_x // 2,
                                              size_canvas_y // 2 + step_y + step_y // 2 + 50 + 25 + step_y // 2 - step_y // 2,
                                              fill="yellow")
                list_ids.append(id2)
                id3 = canvas.create_text(size_canvas_x + menu_x // 2, size_canvas_y // 2 + step_y + step_y // 2,
                                         text=winner, font=("Arial", 50), justify=CENTER)
                id4 = canvas.create_text(size_canvas_x + menu_x // 2, size_canvas_y // 2 + step_y + step_y // 2 + 50,
                                         text=winner_add, font=("Arial", 25), justify=CENTER)
                list_ids.append(id3)
                list_ids.append(id4)
            elif computer_vs_human:
                mark_igrok(hod_igrovomu_polu_1)
                hod_computer()
    mark_igrok(hod_igrovomu_polu_1)

canvas.bind_all("<Button-1>", add_to_all) # левая кнопка мыши
canvas.bind_all("<Button-3>", add_to_all) # правая кнопка мыши

def generate_ships_list():
    global ships_list
    ships_list = []
    # генерируем список случайных длин кораблей
    for i in range(0, ships):
        ships_list.append(random.choice([ship_len1, ship_len2, ship_len3]))
    # print(ships_list)

def generate_enemy_ships():
    global ships_list
    enemy_ships = []

    # подсчет суммарной длины кораблей
    sum_1_all_ships = sum(ships_list)
    sum_1_enemy = 0

    # print("sum: ", sum_1_all_ships)

    while sum_1_enemy != sum_1_all_ships: # код для создания кораблей, чтобы не пересекаться друг с другом
        # обнуляем массив кораблей врага
        enemy_ships = [[0 for i in range(s_x + 1)] for i in range(s_y+1)] # +1 для доп. линии справа и снизу для успешных проверок генерации противника

        for i in range(0, ships):
            len = ships_list[i]
            horizont_vertikal = random.randrange(1, 3) # случайное расположение кораблей: 1 - горизонтальное, 2 - вертикальное

            primerno_x = random.randrange(0, s_x)
            if primerno_x + len > s_x: # проверяем что не вышли за границы x
                primerno_x = primerno_x - len # проверяем что не вышли за границы x

            primerno_y = random.randrange(0, s_y)
            if primerno_y + len > s_y: # проверяем что не вышли за границы x
                primerno_y = primerno_y - len # проверяем что не вышли за границы x

            # print(horizont_vertikal, primerno_x,primerno_y)
            if horizont_vertikal == 1:
                if primerno_x + len <= s_x:
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y][primerno_x - 1] + \
                                               enemy_ships[primerno_y][primerno_x + j] + \
                                               enemy_ships[primerno_y][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y - 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j] + \
                                               enemy_ships[primerno_y - 1][primerno_x + j]
                            # print(check_near_ships)
                            if check_near_ships == 0:  # записываем в том случае, если нет ничего рядом
                                enemy_ships[primerno_y][primerno_x + j] = i + 1  # записываем номер корабля
                        except Exception:
                            pass
            if horizont_vertikal == 2:
                if primerno_y + len <= s_y:
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y - 1][primerno_x] + \
                                               enemy_ships[primerno_y + j][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x - 1] + \
                                               enemy_ships[primerno_y + j][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j][primerno_x - 1]
                            # print(check_near_ships)
                            if check_near_ships == 0:  # записываем в том случае, если нет ничего рядом
                                enemy_ships[primerno_y + j][primerno_x] = i + 1  # записываем номер корабля
                        except Exception:
                            pass

        # делаем подсчет 1ц
        sum_1_enemy = 0
        for i in range(0, s_x):
            for j in range(0, s_y):
                if enemy_ships[j][i] > 0:
                    sum_1_enemy = sum_1_enemy + 1

        # print(sum_1_enemy)
        # print(ships_list)
        # print(enemy_ships)
    return enemy_ships

generate_ships_list()
# print(ships_list)
enemy_ships1 = generate_enemy_ships()
enemy_ships2 = generate_enemy_ships()
# print("---------------------------")
# print(enemy_ships1)
# print("---------------------------")
# print(enemy_ships2)
# print("---------------------------")

while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.005)