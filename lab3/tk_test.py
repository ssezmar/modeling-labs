import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox

def on_button_click():
    messagebox.showinfo("Инфо", f"Вы ввели: {entry.get()}")

def open_file():
    file = filedialog.askopenfilename(title="Открыть файл")
    if file:
        messagebox.showinfo("Файл выбран", file)

def choose_color():
    color = colorchooser.askcolor()[1]
    if color:
        root.config(bg=color)

def add_to_listbox():
    listbox.insert(tk.END, entry.get())

def draw_circle():
    canvas.create_oval(10, 10, 100, 100, fill="skyblue")

# Главное окно
root = tk.Tk()
root.title("Tkinter тест — все виджеты")
root.geometry("800x600")

# Меню
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Открыть файл", command=open_file)
filemenu.add_command(label="Выбрать цвет", command=choose_color)
filemenu.add_separator()
filemenu.add_command(label="Выход", command=root.quit)
menubar.add_cascade(label="Файл", menu=filemenu)
root.config(menu=menubar)

# Метка + поле ввода
tk.Label(root, text="Введите что-нибудь:").pack(pady=5)
entry = tk.Entry(root)
entry.pack(pady=5)

# Кнопка
tk.Button(root, text="Показать сообщение", command=on_button_click).pack(pady=5)

# Многострочный ввод
tk.Label(root, text="Многострочный Text:").pack()
text = tk.Text(root, height=4)
text.pack(pady=5)

# Checkbutton и Radiobutton
check_var = tk.BooleanVar()
tk.Checkbutton(root, text="Согласен", variable=check_var).pack()

radio_var = tk.StringVar(value="A")
tk.Radiobutton(root, text="Вариант A", value="A", variable=radio_var).pack()
tk.Radiobutton(root, text="Вариант B", value="B", variable=radio_var).pack()

# Слайдер
tk.Label(root, text="Слайдер:").pack()
scale = tk.Scale(root, from_=0, to=100, orient="horizontal")
scale.pack()

# Listbox + Spinbox
frame_list = tk.Frame(root)
frame_list.pack(pady=5)
listbox = tk.Listbox(frame_list, height=4)
listbox.pack(side="left")
tk.Button(frame_list, text="Добавить", command=add_to_listbox).pack(side="left", padx=5)

tk.Label(root, text="Числовой Spinbox:").pack()
spinbox = tk.Spinbox(root, from_=0, to=10)
spinbox.pack()

# Canvas для рисования
tk.Label(root, text="Canvas:").pack()
canvas = tk.Canvas(root, width=200, height=150, bg="white")
canvas.pack(pady=5)
tk.Button(root, text="Нарисовать круг", command=draw_circle).pack()

# Дерево (Treeview)
tk.Label(root, text="Treeview таблица:").pack(pady=5)
columns = ("Имя", "Возраст")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.insert("", tk.END, values=("Алиса", 25))
tree.insert("", tk.END, values=("Боб", 30))
tree.pack(pady=5)

root.mainloop()