import tkinter as tk
from datetime import datetime
from tkinter import messagebox, simpledialog, ttk


def setup_treeview():
    global tasks_treeview
    tasks_treeview = ttk.Treeview(right_panel)
    tasks_treeview["columns"] = ("priority", "task", "deadline")
    tasks_treeview.column("#0", width=0, stretch=tk.NO)
    tasks_treeview.column("priority", width=70, anchor=tk.CENTER)
    tasks_treeview.column("deadline", width=100, anchor=tk.CENTER)
    tasks_treeview.column("task", width=300, anchor=tk.W)

    tasks_treeview.heading("#0", text="", anchor=tk.CENTER)
    tasks_treeview.heading("priority", text="Priority", anchor=tk.CENTER)
    tasks_treeview.heading("task", text="Task", anchor=tk.CENTER)
    tasks_treeview.heading("deadline", text="Deadline", anchor=tk.CENTER)

    tasks_treeview.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)


def update_tasks_treeview():
    tasks_treeview.delete(*tasks_treeview.get_children())
    for item in tasks_treeview.get_children():
        # Отримання даних із кожного рядка Treeview
        task_values = tasks_treeview.item(item, 'values')
        task_desc, deadline_str = task_values[1], task_values[2]

        # Перетворення строки дедлайну в об'єкт datetime
        deadline = datetime.strptime(deadline_str, '%d.%m.%Y %H:%M')

        # Визначення символу пріоритету
        priority_symbol = get_priority_image(deadline)

        # Оновлення рядка в Treeview з новим пріоритетом
        tasks_treeview.item(item, values=(priority_symbol, task_desc, deadline_str))


def parse_deadline(deadline_str):
    try:
        # Переконайтеся, що строка дедлайну відповідає формату 'ДД.ММ.РРРР ЧЧ:ММ'
        return datetime.strptime(deadline_str, '%d.%m.%Y %H:%M')
    except ValueError:
        return datetime.max  # Повертаємо максимально можливу дату, якщо дедлайн не визначено


def get_priority_image(deadline):
    days_left = (deadline - datetime.now()).days
    if days_left <= 2:
        return "Високий"  # Червоний колір для високого пріоритету
    elif days_left <= 5:
        return "Середній"  # Жовтий колір для середнього пріоритету
    else:
        return "Низький"  # Зелений колір для низького пріоритету


def load_tasks():
    try:
        with open("tasks.txt", "r", encoding="utf-8") as file:
            tasks = file.readlines()

        tasks_treeview.delete(*tasks_treeview.get_children())  # Очищення Treeview перед завантаженням нових даних

        for task in tasks:
            task = task.strip()
            # Розбиття рядка на окремі частини
            task_parts = task.split(' (')
            task_desc = task_parts[0]
            priority_part = task_parts[1].split(', ')[0]
            deadline_part = task_parts[1].split(', ')[1].rstrip(')')

            # Вилучення пріоритету та дедлайну
            priority = priority_part.split(': ')[1]
            deadline = deadline_part.split(': ')[1]

            # Додавання завдання у Treeview
            tasks_treeview.insert("", "end", values=(priority, task_desc, deadline))

    except FileNotFoundError:
        pass


def save_tasks():
    with open("tasks.txt", "w", encoding="utf-8") as file:
        for item in tasks_treeview.get_children():
            # Витягування даних із кожного рядка Treeview
            priority, task, deadline = tasks_treeview.item(item, 'values')
            # Форматування рядка для збереження у файл
            task_str = f"{task} (Priority: {priority}, Deadline: {deadline})"
            file.write(task_str + "\n")

    messagebox.showinfo("Збереження завдань", "Завдання успішно збережено.")


def add_task():
    task = simpledialog.askstring("Введіть завдання", "Яке завдання ви хочете додати?")

    if task:
        deadline = simpledialog.askstring("Термін виконання", "Введіть дедлайн (формат: ДД.ММ.РРРР ЧЧ:ММ):")
        if deadline:
            # Видаляємо непотрібну частину "(Дедлайн: " і ")"
            deadline_datetime = parse_deadline(deadline)
            priority_symbol = get_priority_image(deadline_datetime)
            tasks_treeview.insert("", "end", values=(priority_symbol, task, deadline))

            save_tasks()

    elif not task:
        messagebox.showinfo("Помилка", "Завдання не може бути порожнім.")


def show_all_tasks():
    load_tasks()


def delete_task():
    try:
        selected_item = tasks_treeview.selection()[0]  # Вибране завдання в Treeview
        if messagebox.askyesno("Видалення завдання", "Ви впевнені, що хочете видалити це завдання?"):
            # Видалення завдання з Treeview
            tasks_treeview.delete(selected_item)
            save_tasks()
    except IndexError:
        messagebox.showinfo("Помилка", "Виберіть завдання для видалення.")


def edit_task():
    try:
        selected_item = tasks_treeview.selection()[0]  # Вибране завдання в Treeview
        selected_task_values = tasks_treeview.item(selected_item, "values")
        # Важливо витягувати дані у відповідності зі структурою колонок Treeview
        priority, task_desc, deadline = selected_task_values

        # Запитуємо оновлені дані
        new_desc = simpledialog.askstring("Редагувати завдання", "Змінити опис завдання:", initialvalue=task_desc)
        new_deadline = simpledialog.askstring("Редагувати завдання", "Змінити дедлайн завдання:", initialvalue=deadline)

        if new_desc and new_deadline:
            # Оновлення даних у Treeview
            tasks_treeview.item(selected_item, values=(priority, new_desc, new_deadline))
            save_tasks()
    except IndexError:
        messagebox.showinfo("Помилка", "Виберіть завдання для редагування.")


def mark_task():
    try:
        selected_item = tasks_treeview.selection()[0]
        task_values = tasks_treeview.item(selected_item, "values")
        updated_task = "[Виконано] " if not task_values[0].startswith("[Виконано] ") else task_values[0]
        tasks_treeview.item(selected_item, values=(updated_task, task_values[1], task_values[2]))
        save_tasks()
    except IndexError:
        messagebox.showinfo("Помилка", "Виберіть завдання для відмітки.")


def unmark_task():
    try:
        selected_item = tasks_treeview.selection()[0]
        task_values = tasks_treeview.item(selected_item, "values")
        task_desc = task_values[1][11:] if task_values[1].startswith("[Виконано] ") else task_values[1]
        deadline_str = task_values[2]

        # Визначення пріоритету знову виходячи з дедлайну
        deadline = datetime.strptime(deadline_str, '%d.%m.%Y %H:%M')
        new_priority_symbol = get_priority_image(deadline)

        # Оновлення завдання у Treeview
        tasks_treeview.item(selected_item, values=(new_priority_symbol, task_desc, deadline_str))
        save_tasks()
    except IndexError:
        messagebox.showinfo("Помилка", "Виберіть завдання для зняття відмітки.")


def mark_all_tasks():
    for item in tasks_treeview.get_children():
        task_values = tasks_treeview.item(item, "values")
        if not task_values[0].startswith("[Виконано] "):
            updated_priority = "[Виконано] " + task_values[0]
            tasks_treeview.item(item, values=(updated_priority, task_values[1], task_values[2]))
    save_tasks()


def unmark_all_tasks():
    for item in tasks_treeview.get_children():
        task_values = tasks_treeview.item(item, "values")
        if task_values[0].startswith("[Виконано] "):
            updated_priority = task_values[0][11:]
            deadline_str = task_values[2]
            deadline = datetime.strptime(deadline_str, '%d.%m.%Y %H:%M')
            new_priority_symbol = get_priority_image(deadline)
            tasks_treeview.item(item, values=(new_priority_symbol, task_values[1], deadline_str))
    save_tasks()


def clear_tasks():
    if messagebox.askyesno("Очищення списку завдань", "Ви впевнені, що хочете очистити весь список?"):
        tasks_treeview.delete(*tasks_treeview.get_children())
        save_tasks()


# Створення вікна
window = tk.Tk()
window.title("Todo List")

# setup_images()

# Основна рамка
frame = tk.Frame(window)
frame.pack(fill=tk.BOTH, expand=True)

# Ліва панель для кнопок
left_panel = tk.Frame(frame)
left_panel.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

# Права панель для Treeview
right_panel = tk.Frame(frame)
right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Шрифти
custom_font = ("Arial", 14, "bold")

# Верхня панель
top_panel = tk.Frame(frame)
top_panel.pack(side=tk.TOP, fill=tk.X)

show_all_tasks_button = tk.Button(top_panel, text="Показати всі завдання", font=custom_font,
                                  command=show_all_tasks)
show_all_tasks_button.pack(side=tk.TOP, fill=tk.X)

# Кнопка збереження завдань
save_button = tk.Button(top_panel, text="Зберегти", font=custom_font, command=save_tasks)
save_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Ліва панель для кнопок
left_panel = tk.Frame(frame)
left_panel.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

# Права панель для списку завдань
right_panel = tk.Frame(frame)
right_panel.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

# Кнопки (розташування у лівій панелі)
add_button = tk.Button(left_panel, text="Додати завдання", font=custom_font, command=add_task)
add_button.pack(side=tk.TOP, fill=tk.X)

edit_button = tk.Button(left_panel, text="Редагувати завдання", font=custom_font, command=edit_task)
edit_button.pack(side=tk.TOP, fill=tk.X)

mark_button = tk.Button(left_panel, text="Відмітити як виконане", font=custom_font, command=mark_task)
mark_button.pack(side=tk.TOP, fill=tk.X)

mark_all_button = tk.Button(left_panel, text="Відмітити всі завдання", font=custom_font, command=mark_all_tasks)
mark_all_button.pack(side=tk.TOP, fill=tk.X)

unmark_button = tk.Button(left_panel, text="Зняти відмітку", font=custom_font, command=unmark_task)
unmark_button.pack(side=tk.TOP, fill=tk.X)

unmark_all_button = tk.Button(left_panel, text="Зняти всі відмітки", font=custom_font, command=unmark_all_tasks)
unmark_all_button.pack(side=tk.TOP, fill=tk.X)

delete_button = tk.Button(left_panel, text="Видалити завдання", font=custom_font, command=delete_task)
delete_button.pack(side=tk.TOP, fill=tk.X)

clear_button = tk.Button(left_panel, text="Очистити список", font=custom_font, command=clear_tasks)
clear_button.pack(side=tk.TOP, fill=tk.X)

setup_treeview()
load_tasks()

# Запуск головного циклу
window.mainloop()
