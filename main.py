import tkinter as tk
from tkinter import messagebox


def add_task():
    task = task_entry.get()
    if task:
        tasks_listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showinfo("Помилка", "Введіть завдання.")


def delete_task():
    try:
        selected_task_index = tasks_listbox.curselection()[0]
        tasks_listbox.delete(selected_task_index)
    except IndexError:
        messagebox.showinfo("Помилка", "Виберіть завдання для видалення.")


# Створення вікна
window = tk.Tk()
window.title("Todo List")

# Розмітка
frame = tk.Frame(window)
frame.pack(padx=10, pady=10)

# Поле вводу для нових завдань
task_entry = tk.Entry(frame, width=50)
task_entry.pack(side=tk.LEFT, padx=(0, 10))

# Кнопка для додавання завдання
add_button = tk.Button(frame, text="Додати завдання", command=add_task)
add_button.pack(side=tk.LEFT)

# Список завдань
tasks_listbox = tk.Listbox(window, width=50, height=15)
tasks_listbox.pack(padx=10, pady=(0, 10))

# Кнопка для видалення завдання
delete_button = tk.Button(window, text="Видалити завдання", command=delete_task)
delete_button.pack(pady=(0, 10))

# Запуск головного циклу
window.mainloop()
