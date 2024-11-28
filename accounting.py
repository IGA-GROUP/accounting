import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime


class SecurityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Учёт входов/выходов")
        self.root.geometry("600x500")

        # Список жильцов
        self.residents = []
        # Журнал входов/выходов
        self.log = []
        # Имя файла для сохранения логов
        self.log_file = "logs.txt"

        # Элементы интерфейса
        self.label_residents = tk.Label(self.root, text="Список жильцов:", font=("Arial", 14))
        self.label_residents.pack()

        self.listbox_residents = tk.Listbox(self.root, height=10, font=("Arial", 12))
        self.listbox_residents.pack(fill=tk.X, padx=10, pady=5)

        self.btn_add_resident = tk.Button(self.root, text="Добавить жильца", command=self.add_resident)
        self.btn_add_resident.pack(pady=5)

        self.btn_remove_resident = tk.Button(self.root, text="Удалить жильца", command=self.remove_resident)
        self.btn_remove_resident.pack(pady=5)

        self.label_actions = tk.Label(self.root, text="Действия:", font=("Arial", 14))
        self.label_actions.pack()

        self.btn_enter = tk.Button(self.root, text="Отметить вход", command=self.mark_enter)
        self.btn_enter.pack(pady=5)

        self.btn_exit = tk.Button(self.root, text="Отметить выход", command=self.mark_exit)
        self.btn_exit.pack(pady=5)

        self.btn_view_log = tk.Button(self.root, text="Посмотреть журнал", command=self.view_log)
        self.btn_view_log.pack(pady=5)

        self.btn_save_log = tk.Button(self.root, text="Сохранить журнал", command=self.save_log)
        self.btn_save_log.pack(pady=5)

        # Автозагрузка логов (если файл уже существует)
        self.load_log()

    def add_resident(self):
        name = simpledialog.askstring("Добавить жильца", "Введите имя жильца:")
        if name:
            if name not in self.residents:
                self.residents.append(name)
                self.update_residents()
                messagebox.showinfo("Успех", f"Жилец {name} добавлен.")
            else:
                messagebox.showwarning("Ошибка", f"Жилец {name} уже существует!")

    def remove_resident(self):
        selected = self.listbox_residents.curselection()
        if selected:
            name = self.listbox_residents.get(selected)
            self.residents.remove(name)
            self.update_residents()
            messagebox.showinfo("Успех", f"Жилец {name} удалён.")
        else:
            messagebox.showwarning("Ошибка", "Выберите жильца для удаления.")

    def mark_enter(self):
        name = simpledialog.askstring("Отметить вход", "Введите имя жильца:")
        if name in self.residents:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp} - {name} вошёл."
            self.log.append(log_entry)
            self.save_log()  # Сохраняем в файл
            messagebox.showinfo("Успех", f"Вход жильца {name} отмечен.")
        else:
            messagebox.showwarning("Ошибка", "Жилец не найден в списке!")

    def mark_exit(self):
        name = simpledialog.askstring("Отметить выход", "Введите имя жильца:")
        if name in self.residents:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp} - {name} вышел."
            self.log.append(log_entry)
            self.save_log()  # Сохраняем в файл
            messagebox.showinfo("Успех", f"Выход жильца {name} отмечен.")
        else:
            messagebox.showwarning("Ошибка", "Жилец не найден в списке!")

    def view_log(self):
        log_window = tk.Toplevel(self.root)
        log_window.title("Журнал входов/выходов")
        log_window.geometry("400x300")

        log_text = tk.Text(log_window, font=("Arial", 12))
        log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        log_text.insert(tk.END, "\n".join(self.log))
        log_text.configure(state="disabled")

    def save_log(self):
        try:
            with open(self.log_file, "w", encoding="utf-8") as file:
                file.write("\n".join(self.log))
            messagebox.showinfo("Успех", "Журнал успешно сохранён.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить журнал: {e}")

    def load_log(self):
        try:
            with open(self.log_file, "r", encoding="utf-8") as file:
                self.log = file.read().splitlines()
            print("Журнал успешно загружен.")
        except FileNotFoundError:
            print("Файл с журналом не найден, будет создан новый.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить журнал: {e}")

    def update_residents(self):
        self.listbox_residents.delete(0, tk.END)
        for resident in self.residents:
            self.listbox_residents.insert(tk.END, resident)


if __name__ == "__main__":
    root = tk.Tk()
    app = SecurityApp(root)
    root.mainloop()
