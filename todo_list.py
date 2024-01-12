import json


class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        return f"Завдання '{task}' додано."

    def edit_task(self, current_task, new_task):
        try:
            index = self.tasks.index(current_task)
            self.tasks[index] = new_task
        except ValueError:
            pass  # Якщо current_task не знайдено, нічого не робимо

    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            return f"Завдання '{task}' видалено."
        else:
            return f"Завдання '{task}' не знайдено."

    def show_tasks(self):
        return "\n".join(self.tasks) if self.tasks else "Список завдань порожній."

    def save_to_file(self, file_path):

        with open(file_path, 'w') as file:
            json.dump(self.tasks, file)

    def load_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            self.tasks = []
