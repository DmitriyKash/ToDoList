import tkinter as tk
from tkinter import messagebox, simpledialog
import tkinter.simpledialog as sd
from todo_list import ToDoList
from plyer import notification
from datetime import datetime, date
from tkinter import PhotoImage
import datetime


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
    if task:
        priority = simpledialog.askinteger("Пріоритет", "Встановіть пріоритет (1-5):", minvalue=1, maxvalue=5)
        deadline = DateEntry(root).result
        if priority is not None and deadline:
            formatted_task = f"[Пріоритет: {priority}] {task} (дедлайн: {deadline})"
            todo_list.add_task(formatted_task)
            update_tasks_display()


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
    for task in todo_list.tasks:
        if "[Пріоритет: 1]" in task:
            listbox.insert(tk.END, task)
            listbox.itemconfig(tk.END, {'bg': 'red'})
        elif "[Пріоритет: 2]" in task:
            listbox.insert(tk.END, task)
            listbox.itemconfig(tk.END, {'bg': 'orange'})
        elif "[Пріоритет: 3]" in task:
            listbox.insert(tk.END, task)
            listbox.itemconfig(tk.END, {'bg': 'yellow'})
        elif "[Пріоритет: 4]" in task:
            listbox.insert(tk.END, task)
            listbox.itemconfig(tk.END, {'bg': 'green'})
        elif "[Пріоритет: 5]" in task:
            listbox.insert(tk.END, task)
            listbox.itemconfig(tk.END, {'bg': 'blue'})
    for task in todo_list.tasks:
        listbox.insert(tk.END, task)


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


def update_tasks_display():
    listbox.delete(0, tk.END)
    for task in todo_list.tasks:
        listbox.insert(tk.END, task)


def save_tasks():
    todo_list.save_to_file("tasks.json")
    messagebox.showinfo("Інформація", "Завдання успішно збережені.")


def load_tasks():
    todo_list.load_from_file("tasks.json")


def on_closing():
    global root
    save_tasks()
    root.destroy()


def filter_tasks():
    priority = simpledialog.askstring("Фільтр завдань за пріоритетом", "Введіть пріоритет (наприклад, 3):")
    if priority:
        filtered_tasks = [task for task in todo_list.tasks if f"[Пріоритет: {priority.strip()}]" in task]
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
            deadline_date = datetime.datetime.strptime(deadline, "%d.%m.%Y").date()
            if deadline_date == today:
                notification.notify(
                    title="Нагадування про завдання",
                    message=f"У вас є завдання з дедлайном сьогодні: {task}",
                    app_name="ToDo List"
                )


def main():
    global listbox, todo_list, root
    todo_list = ToDoList()
    load_tasks()

    root = tk.Tk()
    root.title("ToDo List")

    # Додавання міток та вдосконалення розташування
    frame = tk.Frame(root)
    frame.pack(pady=10)

    tk.Label(frame, text="Ваші завдання:").pack(side=tk.TOP)
    listbox = tk.Listbox(frame, height=10, width=50)
    listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    add_icon = PhotoImage(file="img/add_task.png")
    edit_icon = PhotoImage(file="img/edit_task.png")
    delete_icon = PhotoImage(file="img/delete_task.png")

    tk.Button(btn_frame, image=add_icon, command=add_task).pack(side=tk.LEFT)
    tk.Button(btn_frame, image=edit_icon, command=edit_task).pack(side=tk.LEFT)
    tk.Button(btn_frame, image=delete_icon, command=remove_task).pack(side=tk.LEFT)

    tk.Button(root, text="Зберегти завдання", command=save_tasks).pack(pady=5)
    tk.Button(root, text="Фільтр завдань", command=filter_tasks).pack(pady=5)
    tk.Button(root, text="Показати всі завдання", command=show_all_tasks).pack(pady=5)

    search_button = tk.Button(root, text="Пошук завдань", command=search_tasks)
    search_button.pack(pady=5)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    update_tasks_display()
    check_for_notifications()

    root.mainloop()


if __name__ == "__main__":
    main()
