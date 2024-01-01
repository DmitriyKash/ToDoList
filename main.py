import tkinter as tk
from datetime import datetime
from tkinter import messagebox, simpledialog, font
import re


def parse_deadline(task):
    task_text = task.split('. ', 1)[1] if '. ' in task else task
    match = re.search(r"\(Дедлайн: (\d{2}\.\d{2}\.\d{4} \d{2}:\d{2})\)", task_text)
    return datetime.strptime(match.group(1), '%d.%m.%Y %H:%M') if match else datetime.max


def update_tasks_listbox():
    tasks = list(tasks_listbox.get(0, tk.END))
    # Видаляємо номери завдань перед сортуванням
    tasks_with_no_number = [task.split('. ', 1)[1] if '. ' in task else task for task in tasks]
    tasks_with_no_number.sort(key=parse_deadline)
    tasks_listbox.delete(0, tk.END)
    for i, task in enumerate(tasks_with_no_number, 1):
        tasks_listbox.insert(tk.END, f"{i}. {task}")


def load_tasks():
    try:
        with open("tasks.txt", "r") as file:
            tasks = file.readlines()
        tasks_listbox.delete(0, tk.END)  # Очищуємо список перед завантаженням нових завдань
        for task in tasks:
            tasks_listbox.insert(tk.END, task.strip())
        # update_tasks_listbox()  # Якщо вам потрібно відновити нумерацію та/або сортування, розкоментуйте цей рядок
    except FileNotFoundError:
        pass


def save_tasks():
    with open("tasks.txt", "w") as file:
        for task in tasks_listbox.get(0, tk.END):
            file.write(task + "\n")


def add_task():
    task = simpledialog.askstring("Введіть завдання", "Яке завдання ви хочете додати?")
    category = simpledialog.askstring("Категорія завдання", "Введіть категорію для завдання:")
    if task and category:
        deadline = simpledialog.askstring("Термін виконання", "Введіть дедлайн (формат: ДД.ММ.РРРР ЧЧ:ММ):")
        if deadline:
            formatted_task = f"{task} (Категорія: {category}, Дедлайн: {deadline})"
            tasks_listbox.insert(tk.END, formatted_task)
            update_tasks_listbox()
            save_tasks()
    elif not task or not category:
        messagebox.showinfo("Помилка", "Завдання та категорія не можуть бути порожніми.")


def filter_tasks_by_category():
    category_to_filter = simpledialog.askstring("Фільтр категорій", "Введіть категорію для фільтрації:")
    if category_to_filter:
        filtered_tasks = [task for task in tasks_listbox.get(0, tk.END) if f"(Категорія: {category_to_filter}" in task]
        tasks_listbox.delete(0, tk.END)
        for task in filtered_tasks:
            tasks_listbox.insert(tk.END, task)


def show_all_tasks():
    tasks_listbox.delete(0, tk.END)
    load_tasks()


def delete_task():
    try:
        selected_task_index = tasks_listbox.curselection()[0]
        if messagebox.askyesno("Видалення завдання", "Ви впевнені, що хочете видалити це завдання?"):
            tasks_listbox.delete(selected_task_index)
            update_tasks_listbox()
            save_tasks()
    except IndexError:
        messagebox.showinfo("Помилка", "Виберіть завдання для видалення.")


def edit_task():
    try:
        selected_task_index = tasks_listbox.curselection()[0]
        task = tasks_listbox.get(selected_task_index).split('. ', 1)[1]
        new_task = simpledialog.askstring("Редагувати завдання", "Змінити завдання:", initialvalue=task)
        if new_task:
            tasks_listbox.delete(selected_task_index)
            tasks_listbox.insert(selected_task_index, new_task)
            update_tasks_listbox()
            save_tasks()
    except IndexError:
        messagebox.showinfo("Помилка", "Виберіть завдання для редагування.")


def mark_task():
    try:
        selected_task_index = tasks_listbox.curselection()[0]
        task = tasks_listbox.get(selected_task_index)
        # Відмітка завдання як виконаного
        if not task.startswith("[Виконано] "):
            tasks_listbox.delete(selected_task_index)
            tasks_listbox.insert(selected_task_index, "[Виконано] " + task)
            save_tasks()
    except IndexError:
        messagebox.showinfo("Помилка", "Виберіть завдання для відмітки.")


def unmark_task():
    try:
        selected_task_index = tasks_listbox.curselection()[0]
        task = tasks_listbox.get(selected_task_index)
        if task.startswith("[Виконано] "):
            tasks_listbox.delete(selected_task_index)
            tasks_listbox.insert(selected_task_index, task[11:])
            save_tasks()
    except IndexError:
        messagebox.showinfo("Помилка", "Виберіть завдання для зняття відмітки.")


def mark_all_tasks():
    tasks = tasks_listbox.get(0, tk.END)
    for i, task in enumerate(tasks, 1):
        if not task.startswith("[Виконано] "):
            tasks_listbox.delete(i - 1)
            tasks_listbox.insert(i - 1, "[Виконано] " + task)
    save_tasks()


def unmark_all_tasks():
    tasks = tasks_listbox.get(0, tk.END)
    for i, task in enumerate(tasks, 1):
        if task.startswith("[Виконано] "):
            tasks_listbox.delete(i - 1)
            tasks_listbox.insert(i - 1, task[11:])
    save_tasks()


def clear_tasks():
    if messagebox.askyesno("Видалення завдань", "Ви впевнені, що хочете видалити всі завдання?"):
        tasks_listbox.delete(0, tk.END)
    save_tasks()


# Створення вікна
window = tk.Tk()
window.title("Todo List")

#  Шрифт для списку завдань
custom_font = font.Font(family="Helvetica", size=12, weight="bold")

# Основна рамка
frame = tk.Frame(window)
frame.pack(fill=tk.BOTH, expand=True)

# Верхня панель
top_panel = tk.Frame(frame)
top_panel.pack(side=tk.TOP, fill=tk.X)

filter_button = tk.Button(top_panel, text="Фільтрувати за категорією", font=custom_font,
                          command=filter_tasks_by_category)
filter_button.pack(side=tk.TOP, fill=tk.X)

show_all_tasks_button = tk.Button(top_panel, text="Показати всі завдання", font=custom_font,
                                  command=show_all_tasks)
show_all_tasks_button.pack(side=tk.TOP, fill=tk.X)

# Права панель для списку виконаних завдань
right_panel = tk.Frame(frame)
right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=20)

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

tasks_listbox = tk.Listbox(right_panel, width=100, height=15, font=custom_font)
tasks_listbox.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)

load_tasks()

# Запуск головного циклу
window.mainloop()
