import tkinter as tk
from tkinter import ttk, Toplevel, messagebox, StringVar, END, filedialog
import json
import csv
from datetime import datetime
from tkcalendar import DateEntry
import matplotlib.pyplot as plt

# Файл для сохранения данных
data_file = 'training_log.json'


def load_data():
    """Загрузка данных о тренировках из файла JSON."""
    try:
        with open(data_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_data(data):
    """Сохранение данных о тренировках в файл JSON."""
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)


class TrainingLogApp:
    def __init__(self, root):
        """Инициализация приложения дневника тренировок."""
        self.root = root
        root.title("Дневник тренировок")
        self.create_widgets()

    def create_widgets(self):
        """Создание виджетов для ввода данных и управления интерфейсом."""
        self.exercise_label = ttk.Label(self.root, text="Упражнение:")
        self.exercise_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        self.exercise_entry = ttk.Entry(self.root)
        self.exercise_entry.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)

        self.weight_label = ttk.Label(self.root, text="Вес:")
        self.weight_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        self.weight_entry = ttk.Entry(self.root)
        self.weight_entry.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)

        self.repetitions_label = ttk.Label(self.root, text="Повторения:")
        self.repetitions_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        self.repetitions_entry = ttk.Entry(self.root)
        self.repetitions_entry.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)

        self.add_button = ttk.Button(self.root, text="Добавить запись", command=self.add_entry)
        self.add_button.grid(column=0, row=3, columnspan=2, pady=10)

        self.import_button = ttk.Button(self.root, text="Импортировать из CSV", command=self.import_from_csv)
        self.import_button.grid(column=0, row=4, columnspan=2, pady=10)

        self.view_button = ttk.Button(self.root, text="Просмотреть записи", command=self.view_records)
        self.view_button.grid(column=0, row=5, columnspan=2, pady=10)

    def validate_input(self, exercise, weight, repetitions):
        """Валидация вводимых данных."""
        if not exercise or not all(char.isalpha() or char.isspace() for char in exercise):
            return False, "Поле 'Упражнение' должно содержать только текст."

        if not weight.isdigit() or int(weight) <= 0:
            return False, "Поле 'Вес' должно содержать положительное число."

        if not repetitions.isdigit() or int(repetitions) <= 0:
            return False, "Поле 'Повторения' должно содержать положительное число."

        return True, ""


    def add_entry(self):
        """Добавление новой записи о тренировке."""
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        exercise = self.exercise_entry.get()
        weight = self.weight_entry.get()
        repetitions = self.repetitions_entry.get()

        # Валидация ввода
        is_valid, error_message = self.validate_input(exercise, weight, repetitions)
        if not is_valid:
            messagebox.showerror("Ошибка", error_message)
            return

        entry = {
            'date': date,
            'exercise': exercise,
            'weight': weight,
            'repetitions': repetitions
        }

        data = load_data()
        data.append(entry)
        save_data(data)

        # Очистка полей ввода после добавления
        self.exercise_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.repetitions_entry.delete(0, tk.END)
        messagebox.showinfo("Успешно", "Запись успешно добавлена!")

    def view_records(self):
        """Просмотр записей о тренировках в новом окне."""
        self.records_window = Toplevel(self.root)
        self.records_window.title("Записи тренировок")

        # Инициализация таблицы
        self.tree = ttk.Treeview(self.records_window, columns=("Дата", "Упражнение", "Вес", "Повторения"),
                                 show="headings")
        self.tree.heading('Дата', text="Дата")
        self.tree.heading('Упражнение', text="Упражнение")
        self.tree.heading('Вес', text="Вес")
        self.tree.heading('Повторения', text="Повторения")
        self.tree.pack(expand=True, fill=tk.BOTH)

        # Кнопка для экспорта в CSV
        export_button = ttk.Button(self.records_window, text="Экспортировать в CSV", command=self.export_to_csv)
        export_button.pack(pady=10)

        stats_button = ttk.Button(self.records_window, text="Статистика", command=self.show_statistics)
        stats_button.pack(pady=10)

        # Кнопки для редактирования и удаления выделенной записи
        action_frame = ttk.Frame(self.records_window)
        action_frame.pack(pady=5)

        self.edit_button = ttk.Button(action_frame, text="Редактировать", command=self.edit_entry)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ttk.Button(action_frame, text="Удалить", command=self.delete_entry)
        self.delete_button.pack(side=tk.LEFT, padx=5)



        self.populate_tree()

    def populate_tree(self):
        """Заполнение таблицы записями о тренировках."""
        data = load_data()
        for entry in self.tree.get_children():
            self.tree.delete(entry)

        for entry in data:
            self.tree.insert('', END, values=(entry['date'], entry['exercise'], entry['weight'], entry['repetitions']))

    def edit_entry(self):
        """Редактирование выделенной записи о тренировке."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите запись для редактирования.")
            return

        item = selected_item[0]
        values = self.tree.item(item, 'values')
        if not values:
            return

        # Заполнение полей для редактирования
        self.exercise_entry.delete(0, tk.END)
        self.exercise_entry.insert(0, values[1])
        self.weight_entry.delete(0, tk.END)
        self.weight_entry.insert(0, values[2])
        self.repetitions_entry.delete(0, tk.END)
        self.repetitions_entry.insert(0, values[3])

        # Сохранение изменений в элемент
        self.save_button = ttk.Button(self.root, text="Сохранить изменения",
                                      command=lambda: self.save_edit(selected_item))
        self.save_button.grid(column=0, row=6, columnspan=2, pady=10)

    def save_edit(self, selected_item):
        """Сохранение изменений после редактирования записи."""
        exercise = self.exercise_entry.get()
        weight = self.weight_entry.get()
        repetitions = self.repetitions_entry.get()

        if not (exercise and weight and repetitions):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        data = load_data()
        index = self.tree.index(selected_item[0])  # Получаем индекс выделенной записи
        data[index]['exercise'] = exercise
        data[index]['weight'] = weight
        data[index]['repetitions'] = repetitions

        save_data(data)
        messagebox.showinfo("Успешно", "Запись успешно изменена!")
        self.populate_tree()  # Обновление отображения данных

    def delete_entry(self):
        """Удаление выделенной записи о тренировке."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления.")
            return

        item = selected_item[0]
        data = load_data()
        values = self.tree.item(item, 'values')

        # Получаем запись на основе значений
        entry_to_delete = next((entry for entry in data if entry['date'] == values[0] and
                                entry['exercise'] == values[1] and
                                entry['weight'] == values[2] and
                                entry['repetitions'] == values[3]), None)

        if entry_to_delete:
            data.remove(entry_to_delete)
            save_data(data)
            messagebox.showinfo("Успешно", "Запись успешно удалена!")
            self.populate_tree()  # Обновление отображения данных
        else:
            messagebox.error("Ошибка", "Не удалось удалить запись.")

    def export_to_csv(self):
        """Экспорт данных о тренировках в CSV файл."""
        data = load_data()
        if not data:
            messagebox.showinfo("Информация", "Данные для экспорта отсутствуют!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not file_path:
            return  # Пользователь отменил сохранение

        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Дата", "Упражнение", "Вес", "Повторения"])  # Заголовки столбцов
            for entry in data:
                writer.writerow([entry['date'], entry['exercise'], entry['weight'], entry['repetitions']])

        messagebox.showinfo("Успешно", "Данные успешно экспортированы!")

    def import_from_csv(self):
        """Импорт данных о тренировках из CSV файла."""
        file_path = filedialog.askopenfilename(defaultextension=".csv",
                                               filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not file_path:
            return  # Пользователь отменил выбор файла

        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                entry = {
                    'date': row['Дата'],
                    'exercise': row['Упражнение'],
                    'weight': row['Вес'],
                    'repetitions': row['Повторения']
                }
                data = load_data()
                data.append(entry)
                save_data(data)

        messagebox.showinfo("Успешно", "Данные успешно импортированы!")

    def show_statistics(self):
        """Показать окно со статистикой по упражнениям."""
        self.stats_window = Toplevel(self.root)
        self.stats_window.title("Статистика тренировок")

        # Фильтры
        filter_frame = ttk.Frame(self.stats_window)
        filter_frame.pack(pady=10)

        self.start_date_var = StringVar()
        self.end_date_var = StringVar()
        self.selected_exercise_var = StringVar()

        ttk.Label(filter_frame, text="Начальная дата:").grid(column=0, row=0, padx=5)
        self.start_date_entry = DateEntry(filter_frame, textvariable=self.start_date_var, date_pattern='yyyy-mm-dd')
        self.start_date_entry.grid(column=1, row=0, padx=5)

        ttk.Label(filter_frame, text="Конечная дата:").grid(column=2, row=0, padx=5)
        self.end_date_entry = DateEntry(filter_frame, textvariable=self.end_date_var, date_pattern='yyyy-mm-dd')
        self.end_date_entry.grid(column=3, row=0, padx=5)

        # Упражнения для выбора
        exercises = {entry['exercise'] for entry in load_data()}
        self.exercise_combobox = ttk.Combobox(filter_frame, textvariable=self.selected_exercise_var, values=list(exercises))
        self.exercise_combobox.grid(column=0, row=1, columnspan=2, padx=5, pady=5)
        ttk.Label(filter_frame, text="Выберите упражнение:").grid(column=2, row=1, padx=5)

        # Кнопка применения фильтров
        filter_button = ttk.Button(filter_frame, text="Применить фильтры", command=self.apply_stats_filters)
        filter_button.grid(column=0, row=2, columnspan=4, pady=5)

        # Кнопка "График"
        graph_button = ttk.Button(filter_frame, text="График", command=self.show_graph)
        graph_button.grid(column=0, row=3, columnspan=4, pady=5)

        # Инициализация таблицы для статистики
        self.stats_tree = ttk.Treeview(self.stats_window, columns=("Упражнение", "Сумма подходов"), show="headings")
        self.stats_tree.heading('Упражнение', text="Упражнение")
        self.stats_tree.heading('Сумма подходов', text="Сумма подходов")
        self.stats_tree.pack(expand=True, fill=tk.BOTH)

        self.populate_stats_tree()

    def populate_stats_tree(self):
        """Заполнение таблицы статистики."""
        data = load_data()
        exercise_totals = {}

        for entry in data:
            exercise = entry['exercise']
            repetitions = int(entry['repetitions'])
            if exercise not in exercise_totals:
                exercise_totals[exercise] = 0
            exercise_totals[exercise] += repetitions

        for exercise, total in exercise_totals.items():
            self.stats_tree.insert('', END, values=(exercise, total))

    def apply_stats_filters(self):
        """Применение фильтров для отображения статистики."""
        self.stats_tree.delete(*self.stats_tree.get_children())
        data = load_data()
        filtered_data = data

        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()
        selected_exercise = self.selected_exercise_var.get()

        if start_date:
            filtered_data = [entry for entry in filtered_data if entry['date'] >= start_date]

        if end_date:
            filtered_data = [entry for entry in filtered_data if entry['date'] <= end_date]

        if selected_exercise:
            filtered_data = [entry for entry in filtered_data if entry['exercise'] == selected_exercise]

        exercise_totals = {}
        for entry in filtered_data:
            exercise = entry['exercise']
            repetitions = int(entry['repetitions'])
            if exercise not in exercise_totals:
                exercise_totals[exercise] = 0
            exercise_totals[exercise] += repetitions

        for exercise, total in exercise_totals.items():
            self.stats_tree.insert('', END, values=(exercise, total))

    def show_graph(self):
        """Показать график для выбранного упражнения за выбранный период."""
        data = load_data()

        # Получаем отфильтрованные данные
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()
        selected_exercise = self.selected_exercise_var.get()

        filtered_data = [
            {
                'date': entry['date'],
                'weight': int(entry['weight']),
                'repetitions': int(entry['repetitions'])
            }
            for entry in data
            if (start_date <= entry['date'] <= end_date) and (
                        selected_exercise == "" or entry['exercise'] == selected_exercise)
        ]

        if not filtered_data:
            messagebox.showinfo("Информация", "Нет данных для отображения графика.")
            return

        dates = [entry['date'] for entry in filtered_data]
        weights = [entry['weight'] for entry in filtered_data]
        repetitions = [entry['repetitions'] for entry in filtered_data]

        fig, ax1 = plt.subplots(figsize=(10, 5))

        # Создаем две оси для веса и повторений
        ax1.set_xlabel('Дата')
        ax1.set_ylabel('Вес', color='tab:blue')
        ax1.plot(dates, weights, color='tab:blue', marker='o', label='Вес')
        ax1.tick_params(axis='y', labelcolor='tab:blue')

        ax2 = ax1.twinx()  # Создаем вторую ось для повторений
        ax2.set_ylabel('Повторения', color='tab:red')
        ax2.plot(dates, repetitions, color='tab:red', marker='x', label='Повторения')
        ax2.tick_params(axis='y', labelcolor='tab:red')

        fig.tight_layout()  # Избегаем перетасовки
        plt.title(f'График изменения веса и повторений для {selected_exercise}')
        plt.xticks(rotation=45)
        plt.grid()
        plt.legend(loc='upper left')
        plt.show()


def main():
    """Запуск основного приложения."""
    root = tk.Tk()
    app = TrainingLogApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
