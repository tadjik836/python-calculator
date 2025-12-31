import tkinter as tk
from tkinter import messagebox
import sys


class ModernCalculator:
    def show_history(self):
        """Показать историю операций"""
        history_win = tk.Toplevel(self.root)
        history_win.title("История операций")
        history_win.geometry("300x400")

        text = tk.Text(history_win, bg='#1e1e1e', fg='white')
        text.pack(expand=True, fill=tk.BOTH)

        for item in self.history[-20:]:  # Последние 20 операций
            text.insert(tk.END, f"• {item}\n")

        # Кнопка очистки
        tk.Button(history_win, text="Очистить историю",
                  command=self.clear_history).pack(pady=10)

    def clear_history(self):
        """Очистить историю"""
        self.history.clear()
        messagebox.showinfo("История", "История очищена")
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Калькулятор PyCharm Edition")
        self.root.geometry("380x720")
        self.root.configure(bg='#1e1e1e')  # Темная тема как в PyCharm
        self.root.resizable(False, False)

        # Иконка окна (PyCharm style)
        try:
            self.root.iconbitmap(self.get_icon_path())
        except:
            pass

        # Переменные
        self.current_input = ""
        self.history = []

        # Создание интерфейса
        self.create_widgets()

        # Привязка клавиш клавиатуры
        self.bind_keyboard()

    def get_icon_path(self):
        """Получение пути к иконке в зависимости от ОС"""
        if sys.platform.startswith('win'):
            return 'C:\\Windows\\System32\\calc.exe'
        return None

    def create_widgets(self):
        """Создание всех элементов интерфейса"""

        # ==================== ДИСПЛЕЙ ====================
        display_frame = tk.Frame(self.root, bg='#252526', bd=10, relief=tk.FLAT)
        display_frame.pack(pady=(20, 15), padx=20, fill=tk.X)

        self.display = tk.Entry(
            display_frame,
            font=('Segoe UI', 32, 'bold'),
            bd=0,
            relief=tk.FLAT,
            justify='right',
            bg='#252526',
            fg='#d4d4d4',
            insertbackground='#d4d4d4',
            readonlybackground='#252526'
        )
        self.display.pack(fill=tk.X, ipady=15)
        self.display.config(state='normal')

        # Индикатор истории
        history_label = tk.Label(
            self.root,
            text="История: 0 операций",
            font=('Segoe UI', 9),
            bg='#1e1e1e',
            fg='#858585'
        )
        history_label.pack(pady=(0, 10))

        # ==================== КНОПКИ ====================
        buttons_frame = tk.Frame(self.root, bg='#1e1e1e')
        buttons_frame.pack(padx=20, pady=10)

        # Определение кнопок в стиле PyCharm
        button_layout = [
            [
                ('C', '#d16969', '#1e1e1e', 1),  # Красная как ошибки в PyCharm
                ('⌫', '#3c3c3c', '#cccccc', 1),
                ('%', '#3c3c3c', '#cccccc', 1),
                ('÷', '#007acc', '#ffffff', 1)  # Синяя как выделение
            ],
            [
                ('7', '#2d2d2d', '#d4d4d4', 1),
                ('8', '#2d2d2d', '#d4d4d4', 1),
                ('9', '#2d2d2d', '#d4d4d4', 1),
                ('×', '#007acc', '#ffffff', 1)
            ],
            [
                ('4', '#2d2d2d', '#d4d4d4', 1),
                ('5', '#2d2d2d', '#d4d4d4', 1),
                ('6', '#2d2d2d', '#d4d4d4', 1),
                ('-', '#007acc', '#ffffff', 1)
            ],
            [
                ('1', '#2d2d2d', '#d4d4d4', 1),
                ('2', '#2d2d2d', '#d4d4d4', 1),
                ('3', '#2d2d2d', '#d4d4d4', 1),
                ('+', '#007acc', '#ffffff', 2)  # Высокая кнопка
            ],
            [
                ('00', '#2d2d2d', '#d4d4d4', 1),
                ('0', '#2d2d2d', '#d4d4d4', 1),
                ('.', '#2d2d2d', '#d4d4d4', 1),
                ('=', '#388a34', '#ffffff', 2)  # Зеленая как успешный тест
            ]
        ]

        # Создание кнопок
        self.buttons = {}
        for row_idx, row in enumerate(button_layout):
            for col_idx, (text, bg, fg, rowspan) in enumerate(row):
                btn = tk.Button(
                    buttons_frame,
                    text=text,
                    font=('Segoe UI', 16, 'bold'),
                    bg=bg,
                    fg=fg,
                    bd=0,
                    relief=tk.FLAT,
                    activebackground='#3e3e3e',
                    activeforeground=fg,
                    cursor='hand2',
                    command=lambda t=text: self.on_button_click(t)
                )

                # Специальная стилизация для кнопки "="
                if text == '=':
                    btn.config(font=('Segoe UI', 18, 'bold'))

                btn.grid(
                    row=row_idx * 2,
                    column=col_idx,
                    rowspan=rowspan,
                    padx=2,
                    pady=2,
                    sticky='nsew',
                    ipadx=10,
                    ipady=15
                )

                # Сохраняем ссылку на кнопку
                self.buttons[text] = btn

                # Эффекты при наведении
                btn.bind("<Enter>", lambda e, b=btn: b.config(relief=tk.RAISED))
                btn.bind("<Leave>", lambda e, b=btn: b.config(relief=tk.FLAT))

        # Настройка сетки
        for i in range(10):  # 5 строк × 2 (из-за rowspan)
            buttons_frame.grid_rowconfigure(i, weight=1, minsize=40)
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1, minsize=80)

        # ==================== СТАТУС БАР ====================
        status_bar = tk.Frame(self.root, bg='#007acc', height=2)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        # Текущая операция
        self.status_label = tk.Label(
            self.root,
            text="Готов",
            font=('Segoe UI', 9),
            bg='#1e1e1e',
            fg='#858585',
            anchor='w'
        )
        self.status_label.pack(fill=tk.X, padx=20, pady=(5, 10))

    def bind_keyboard(self):
        """Привязка клавиш клавиатуры"""
        self.root.bind('<Key>', self.on_key_press)
        self.root.bind('<Return>', lambda e: self.on_button_click('='))
        self.root.bind('<BackSpace>', lambda e: self.on_button_click('⌫'))
        self.root.bind('<Escape>', lambda e: self.on_button_click('C'))
        self.root.bind('<Delete>', lambda e: self.on_button_click('C'))

        # Цифровые клавиши
        for i in range(10):
            self.root.bind(str(i), lambda e, num=str(i): self.on_button_click(num))

        # Операторы
        self.root.bind('+', lambda e: self.on_button_click('+'))
        self.root.bind('-', lambda e: self.on_button_click('-'))
        self.root.bind('*', lambda e: self.on_button_click('×'))
        self.root.bind('/', lambda e: self.on_button_click('÷'))
        self.root.bind('%', lambda e: self.on_button_click('%'))
        self.root.bind('.', lambda e: self.on_button_click('.'))

    def on_key_press(self, event):
        """Обработка нажатия клавиш"""
        if event.char == '\r':
            return  # Enter уже обработан

    def on_button_click(self, char):
        """Обработка нажатия кнопок"""

        # Обновляем статус
        self.status_label.config(text=f"Обработка: {char}")

        if char == '=':
            self.calculate_result()
        elif char == 'C':
            self.clear_display()
        elif char == '⌫':
            self.backspace()
        elif char == '%':
            self.calculate_percentage()
        else:
            self.append_char(char)

    def append_char(self, char):
        """Добавление символа на дисплей"""
        # Преобразуем символы операций
        display_char = char
        if char == '×':
            char = '*'
        elif char == '÷':
            char = '/'

        self.current_input += char

        # Отображаем с красивыми символами
        display_text = self.current_input.replace('*', '×').replace('/', '÷')
        self.update_display(display_text)

    def calculate_result(self):
        """Вычисление результата"""
        try:
            if not self.current_input:
                return

            # Заменяем символы для вычисления
            expression = self.current_input

            # Вычисляем результат
            result = eval(expression)

            # Форматируем результат
            if isinstance(result, float):
                # Убираем лишние нули
                result = int(result) if result.is_integer() else round(result, 10)

            # Сохраняем в историю
            display_expr = self.current_input.replace('*', '×').replace('/', '÷')
            self.history.append(f"{display_expr} = {result}")

            # Обновляем интерфейс
            self.update_display(str(result))
            self.current_input = str(result)

            # Обновляем статус
            self.status_label.config(text=f"Результат: {result}")

        except ZeroDivisionError:
            messagebox.showerror("Ошибка", "Деление на ноль невозможно!",
                                 parent=self.root)
            self.clear_display()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Некорректное выражение!\n{str(e)}",
                                 parent=self.root)
            self.clear_display()

    def calculate_percentage(self):
        """Вычисление процентов"""
        try:
            if not self.current_input:
                return

            expression = self.current_input
            result = eval(expression) / 100

            # Форматируем
            if isinstance(result, float) and result.is_integer():
                result = int(result)

            self.update_display(str(result))
            self.current_input = str(result)
            self.status_label.config(text=f"Процент: {result}")

        except:
            messagebox.showerror("Ошибка", "Невозможно вычислить проценты",
                                 parent=self.root)

    def backspace(self):
        """Удаление последнего символа"""
        if self.current_input:
            self.current_input = self.current_input[:-1]
            display_text = self.current_input.replace('*', '×').replace('/', '÷')
            self.update_display(display_text)
            self.status_label.config(text="Удалён последний символ")

    def clear_display(self):
        """Очистка дисплея"""
        self.current_input = ""
        self.update_display("")
        self.status_label.config(text="Дисплей очищен")

    def update_display(self, text):
        """Обновление текста на дисплее"""
        self.display.delete(0, tk.END)
        self.display.insert(0, text)

        # Обновляем цвет в зависимости от содержания
        if '=' in text:
            self.display.config(fg='#4ec9b0')  # Цвет как в PyCharm для результатов
        else:
            self.display.config(fg='#d4d4d4')


# ==================== ЗАПУСК ПРИЛОЖЕНИЯ ====================
def main():
    """Точка входа в приложение"""
    root = tk.Tk()
    app = ModernCalculator(root)

    # Центрирование окна
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    # Запуск главного цикла
    root.mainloop()


if __name__ == "__main__":
    main()
