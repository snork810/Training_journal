# Дневник Тренировок

Данное приложение позволяет вам удобно отслеживать и сохранять записи о своих тренировках. Вы можете добавлять данные о выполненных упражнениях, их весе и количестве повторений. Программа также предлагает инструменты для анализа ваших данных через статистику и визуализации в виде графиков.

## Возможности программы

### 1. Добавление записи о тренировке
- **Функция:** `add_entry()`
- **Описание:** Позволяет пользователю ввести дату, название упражнения, вес и количество повторений. После проверки правильности ввода, запись добавляется в журнал тренировок в формате JSON.

### 2. Импорт записей из CSV
- **Функция:** `import_from_csv()`
- **Описание:** Позволяет пользователю импортировать записи о тренировках из CSV файла. Данные из файла добавляются в существующий журнал.

### 3. Экспорт записей в CSV
- **Функция:** `export_to_csv()`
- **Описание:** Позволяет экспортировать записи о тренировках в CSV файл. Это позволяет пользователю сохранить записи для дальнейшего анализа или архивирования.

### 4. Просмотр записей тренировки
- **Функция:** `view_records()`
- **Описание:** Открывает новое окно с таблицей, в которой отображаются все записи о тренировках. В таблице отображаются дата, название упражнения, вес и количество повторений. 

### 5. Редактирование записей
- **Функция:** `edit_entry()`, `save_edit()`
- **Описание:** Позволяют пользователю изменять ранее добавленные записи. Выбранная запись загружается в поля ввода, где пользователь может обновить данные. После изменения данные сохраняются обратно в файл.

### 6. Удаление записей
- **Функция:** `delete_entry()`
- **Описание:** Удаляет выделенную запись из журнала. После подтверждения операция выполнится, и данные будут обновлены.

### 7. Статистика по упражнениям
- **Функция:** `show_statistics()`, `apply_stats_filters()`, `populate_stats_tree()`
- **Описание:** Позволяет пользователю просматривать статистику по выполненным упражнениям. Можно применить фильтры по дате и выбранному упражнению, чтобы получить актуальные данные.

### 8. Построение графиков
- **Функция:** `show_graph()`
- **Описание:** Позволяет визуализировать изменения веса и повторений за выбранный промежуток времени. График отображает вес (синие точки) и количество повторений (красные точки) по датам.

### 9. Валидация ввода
- **Функция:** `validate_input()`
- **Описание:** Проверяет входные данные на корректность перед добавлением новой записи. Убедитесь, что поля не пустые, а поля "Вес" и "Повторения" содержат положительные числа.

## Структура данных

Все записи хранятся в JSON формате в файле `training_log.json`. Каждая запись представляет собой объект со следующими полями:
- `date`: Дата и время добавления записи.
- `exercise`: Название упражнения.
- `weight`: Вес, с которым выполнялось упражнение.
- `repetitions`: Количество повторений.

## Как использовать программу

1. **Запустить программу:** Откройте терминал и используйте команду `python your_script_name.py`.
2. **Добавить новую запись:** Введите данные о тренировке (упражнение, вес, повторения) и нажмите "Добавить запись".
3. **Просмотреть записи:** Нажмите кнопку "Просмотреть записи", чтобы увидеть все добавленные записи.
4. **Редактировать или удалить записи:** Выберите нужную запись и используйте кнопки "Редактировать" или "Удалить".
5. **Смотреть статистику:** Нажмите кнопку "Статистика" для получения сводки по выполненным упражнениям с возможностью фильтрации.
6. **Просмотреть график:** Используйте кнопку "График" для визуализации изменений веса и повторений.

## Зависимости

- Python 3.x
- Tkinter
- Matplotlib
- tkcalendar