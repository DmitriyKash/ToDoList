import tkinter as tk
from tkinter import messagebox, simpledialog
import tkinter.simpledialog as sd
from todo_list import ToDoList
from plyer import notification
from datetime import datetime, timedelta
from datetime import date
from tkinter import PhotoImage
from tkinter import ttk


# import datetime


class DateEntry(sd.Dialog):
    def body(self, master):
        self.date_entry = tk.Entry(master)
        self.date_entry.pack()
        return self.date_entry

    def apply(self):
        self.result = self.date_entry.get()


def save_tasks():
    todo_list.save_to_file("tasks.json")


def load_tasks():
    todo_list.load_from_file("tasks.json")


def add_task():
    task = simpledialog.askstring("Введіть завдання", "Назва завдання:")
    if task and len(task) > 150:
        messagebox.showwarning("Попередження", "Довжина завдання не може перевищувати 30 символів.")
        return

    if task:
        deadline = DateEntry(root).result
        if deadline:
            formatted_task = f"{task} (дедлайн: {deadline})"
            todo_list.add_task(formatted_task)
            update_tasks_display()
            save_tasks()


def edit_task():
    selected_task = listbox.curselection()
    if selected_task:
        current_task = listbox.get(selected_task)
        new_task = simpledialog.askstring("Редагувати завдання", "Нова назва завдання:", initialvalue=current_task)
        if new_task:
            todo_list.edit_task(current_task, new_task)
            update_tasks_display()
    else:
        messagebox.showwarning("Попередження", "Будь ласка, виберіть завдання для редагування.")


def update_tasks_display():
    listbox.delete(0, tk.END)
    today = datetime.today().date()  # Отримання поточної дати як datetime.date

    for task in todo_list.tasks:
        deadline_str = task.split("дедлайн: ")[-1].split(")")[0]
        deadline = datetime.strptime(deadline_str, "%d.%m.%Y").date()  # Конвертування строки у datetime.date
        delta = deadline - today  # Віднімання дат

        # Логіка кольорового кодування
        if delta < timedelta(days=0):
            color = 'red'  # Пропущений дедлайн
        elif delta <= timedelta(days=3):
            color = 'orange'  # Дедлайн протягом наступних 3 днів
        elif delta <= timedelta(days=7):
            color = 'yellow'  # Дедлайн протягом наступного тижня
        else:
            color = 'green'  # Дедлайн більше ніж через тиждень

        listbox.insert(tk.END, task)
        listbox.itemconfig(tk.END, {'bg': color})


def search_tasks():
    search_query = simpledialog.askstring("Пошук завдань", "Введіть ключове слово для пошуку:")
    if search_query:
        matching_tasks = [task for task in todo_list.tasks if search_query.lower() in task.lower()]
        listbox.delete(0, tk.END)
        for task in matching_tasks:
            listbox.insert(tk.END, task)


def remove_task():
    selected_task = listbox.curselection()
    if selected_task:
        task = listbox.get(selected_task)
        todo_list.remove_task(task)
        update_tasks_display()
    else:
        messagebox.showwarning("Попередження", "Будь ласка, виберіть завдання для видалення.")


def save_tasks():
    todo_list.save_to_file("tasks.json")
    messagebox.showinfo("Інформація", "Завдання успішно збережені.")


def load_tasks():
    todo_list.load_from_file("tasks.json")


def on_closing():
    global root
    save_tasks()
    root.destroy()


def filter_tasks(event):
    selected_priority = dropdown.get()
    if selected_priority == "Всі":
        update_tasks_display()
    else:
        filtered_tasks = [task for task in todo_list.tasks if f"[Пріоритет: {selected_priority}]" in task]
        listbox.delete(0, tk.END)
        for task in filtered_tasks:
            listbox.insert(tk.END, task)


def show_all_tasks():
    update_tasks_display()


def check_for_notifications():
    today = date.today()
    for task in todo_list.tasks:
        if "дедлайн:" in task:
            deadline = task.split("дедлайн: ")[-1].split(")")[0]
            deadline_date = datetime.strptime(deadline, "%d.%m.%Y").date()
            if deadline_date == today:
                notification.notify(
                    title="Нагадування про завдання",
                    message=f"У вас є завдання з дедлайном сьогодні: {task}",
                    app_name="ToDo List"
                )


def sort_tasks(event):
    selected_sort = sort_dropdown.get()
    if selected_sort == "За дедлайном":
        todo_list.tasks.sort(key=lambda x: datetime.strptime(x.split("дедлайн: ")[-1].split(")")[0], "%d.%m.%Y"))
    elif selected_sort == "Алфавітний порядок":
        todo_list.tasks.sort()

    update_tasks_display()


def main():
    global listbox, todo_list, root, dropdown, sort_dropdown
    todo_list = ToDoList()
    load_tasks()

    root = tk.Tk()

    # зміна вікна на фоновий режим для відображення фонуваних елементів
    # root.overrideredirect(True)

    # root.attributes("-fullscreen", True)

    # root.withdraw()
    # востановлення вікна з фонового режиму
    # root.lift()

    root.title("ToDo List")

    # Додавання міток та вдосконалення розташування
    frame = tk.Frame(root)
    frame.pack(pady=10)

    tk.Label(frame, text="Ваші завдання:").pack(side=tk.TOP)
    listbox = tk.Listbox(frame, height=10, width=150, font=("Arial", 18))
    listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    btn_frame = tk.Frame(root)
    btn_frame.pack(side=tk.LEFT, pady=10)

    add_icon = PhotoImage(file="img/add_task.png")
    edit_icon = PhotoImage(file="img/edit_task.png")
    delete_icon = PhotoImage(file="img/delete_task.png")

    tk.Button(btn_frame, image=add_icon, command=add_task).pack(side=tk.LEFT)
    tk.Button(btn_frame, image=edit_icon, command=edit_task).pack(side=tk.LEFT)
    tk.Button(btn_frame, image=delete_icon, command=remove_task).pack(side=tk.LEFT)

    tk.Button(root, text="Зберегти завдання", command=save_tasks).pack(pady=5)

    label = tk.Label(btn_frame, text="Фільтр завдань:")
    label.pack(pady=(0, 0))
    sort_options = ["За дедлайном", "Алфавітний порядок"]
    sort_dropdown = ttk.Combobox(btn_frame, values=sort_options)
    # sort_dropdown.set("")  # Значення за замовчуванням
    sort_dropdown.pack(pady=5)
    sort_dropdown.bind("<<ComboboxSelected>>", sort_tasks)

    tk.Button(btn_frame, text="Показати всі завдання", command=show_all_tasks).pack(pady=5)

    search_button = tk.Button(btn_frame, text="Пошук завдань", command=search_tasks)
    search_button.pack(pady=5)
    update_tasks_display()
    check_for_notifications()
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()


if __name__ == "__main__":
    main()
