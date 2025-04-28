import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox
import psycopg2
import string
import random
from dotenv import load_dotenv
import os
from language import LanguageManager


def connect_DB():
    try:
        load_dotenv(os.path.join(os.path.dirname(__file__), 'config', '.env'))
        global conn
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=os.getenv('DB_PORT')
        )
        return conn
    except psycopg2.Error as e:
        return None


class PasswordWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.lang_manager = LanguageManager()  # Инициализация менеджера переводов
        self.initUI()
        self.setup_language_switch()
        self.update_ui_language()

    def setup_language_switch(self):
        """Инициализация языковой кнопки как в LoginWindow"""
        self.lang_btn = QtWidgets.QPushButton(self)
        self.lang_btn.setGeometry(550, 115, 120, 40)
        self.lang_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        # Меню выбора языка
        self.lang_menu = QtWidgets.QMenu(self)
        self.ru_action = self.lang_menu.addAction("Русский")
        self.en_action = self.lang_menu.addAction("English")

        self.ru_action.triggered.connect(lambda: self.change_language('ru'))
        self.en_action.triggered.connect(lambda: self.change_language('en'))
        self.lang_btn.setMenu(self.lang_menu)

    def change_language(self, lang_code):
        """Переключение языка и обновление кнопки"""
        self.lang_manager.load_language(lang_code)
        self.update_ui_language()

        # Непосредственное обновление текста кнопки
        if lang_code == 'ru':
            self.lang_btn.setText("Язык")
        else:
            self.lang_btn.setText("Language")

    def initUI(self):
        super().__init__()
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowTitle(self.tr('password_generation_window_title'))

        # Установка фона
        oImage = QtGui.QImage("image/dragon.jpg")
        sImage = oImage.scaled(self.size(), QtCore.Qt.KeepAspectRatioByExpanding)
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(sImage))
        self.setPalette(palette)

        # Белое окно для контента
        self.white_window = QtWidgets.QWidget(self)
        self.white_window.setGeometry(520, 170, 1250, 700)
        self.white_window.setStyleSheet("background-color: white; border-radius: 30px;")

        # Кнопка закрытия
        self.close_button = QtWidgets.QPushButton('✕', self)
        self.close_button.setGeometry(1720, 170, 50, 50)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #7f99a4;
                color: black;
                border: none;
                border-radius: 15px;
                font-size: 35px;
            }
            QPushButton:hover { background-color: #a0a0a0; }
        """)
        self.close_button.clicked.connect(self.close)

        # Поля для паролей
        self.variant1_label = QtWidgets.QLabel(f"{self.tr('variant')} 1:", self)
        self.variant1_label.move(560, 200)
        self.variant1_label.setStyleSheet("font-size: 20px;")

        self.variant1_input = QtWidgets.QLineEdit(self)
        self.variant1_input.setGeometry(565, 230, 1100, 50)
        self.variant1_input.setStyleSheet("""
            border-radius: 20px; 
            padding: 10px; 
            font-size: 17px; 
            background-color: #c2c2c2;
        """)

        self.copy_button1 = QtWidgets.QPushButton(self)
        self.copy_button1.setGeometry(1680, 230, 50, 50)
        self.copy_button1.setIcon(QtGui.QIcon('image/save.png'))
        self.copy_button1.setStyleSheet("""
            QPushButton {
                background-color: #c2c2c2;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover { background-color: #a0a0a0; }
        """)
        self.copy_button1.clicked.connect(lambda: self.copy_to_clipboard(self.variant1_input))

        # Вариант 2
        self.variant2_label = QtWidgets.QLabel(f"{self.tr('variant')} 2:", self)
        self.variant2_label.move(560, 300)
        self.variant2_label.setStyleSheet("font-size: 20px;")

        self.variant2_input = QtWidgets.QLineEdit(self)
        self.variant2_input.setGeometry(565, 330, 1100, 50)
        self.variant2_input.setStyleSheet("""
            border-radius: 20px; 
            padding: 10px; 
            font-size: 17px; 
            background-color: #c2c2c2;
        """)

        self.copy_button2 = QtWidgets.QPushButton(self)
        self.copy_button2.setGeometry(1680, 330, 50, 50)
        self.copy_button2.setStyleSheet("""
            QPushButton {
                background-color: #c2c2c2;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover { background-color: #a0a0a0; }
        """)
        self.copy_button2.setIcon(QtGui.QIcon('image/save.png'))
        self.copy_button2.clicked.connect(lambda: self.copy_to_clipboard(self.variant2_input))

        # Вариант 3
        self.variant3_label = QtWidgets.QLabel(f"{self.tr('variant')} 3:", self)
        self.variant3_label.move(560, 400)
        self.variant3_label.setStyleSheet("font-size: 20px;")

        self.variant3_input = QtWidgets.QLineEdit(self)
        self.variant3_input.setGeometry(565, 430, 1100, 50)
        self.variant3_input.setStyleSheet("""
            border-radius: 20px; 
            padding: 10px; 
            font-size: 17px; 
            background-color: #c2c2c2;
        """)

        self.copy_button3 = QtWidgets.QPushButton(self)
        self.copy_button3.setGeometry(1680, 430, 50, 50)
        self.copy_button3.setIcon(QtGui.QIcon('image/save.png'))
        self.copy_button3.setStyleSheet("""
            QPushButton {
                background-color: #c2c2c2;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover { background-color: #a0a0a0; }
        """)
        self.copy_button3.clicked.connect(lambda: self.copy_to_clipboard(self.variant3_input))

        # Панель управления
        self.overlay2 = QtWidgets.QWidget(self)
        self.overlay2.setGeometry(550, 520, 1190, 200)
        self.overlay2.setStyleSheet("background-color: #c2c2c2;")

        # Кнопка генерации
        self.plus_button = QtWidgets.QPushButton(self.tr('generate_password'), self)
        self.plus_button.setGeometry(550, 740, 1190, 50)
        self.plus_button.setStyleSheet("""
            QPushButton {
                background-color: #c2c2c2; 
                color: black;              
                border: none;              
                border-radius: 10px;       
                font-size: 20px;           
            }
        """)
        self.plus_button.clicked.connect(self.generate_password)

        # Элементы управления
        self.use_uppercase_button = QtWidgets.QPushButton(self.tr('use_uppercase'), self)
        self.use_uppercase_button.setGeometry(600, 550, 340, 50)
        self.use_uppercase_button.setStyleSheet("""
            background-color: white; 
            padding: 10px; 
            font-size: 20px; 
            text-align: left;
        """)

        self.use_symbols_button = QtWidgets.QPushButton(self.tr('use_symbols'), self)
        self.use_symbols_button.setGeometry(1180, 550, 340, 50)
        self.use_symbols_button.setStyleSheet("""
            background-color: white; 
            padding: 10px; 
            font-size: 20px; 
            text-align: left;
        """)

        self.wind1 = QtWidgets.QPushButton(self.tr('password_length'), self)
        self.wind1.setGeometry(600, 630, 340, 50)
        self.wind1.setStyleSheet("""
            background-color: white; 
            padding: 10px; 
            font-size: 20px; 
            text-align: left;
        """)

        self.length_input = QtWidgets.QLineEdit(self)
        self.length_input.setGeometry(970, 628, 50, 50)
        self.length_input.setStyleSheet("""
            border-radius: 10px; 
            padding: 10px; 
            font-size: 19px; 
            background-color: #fdfdfd;
        """)

        # Чекбоксы
        self.use_uppercase_checkbox = QtWidgets.QPushButton('✕', self)
        self.use_uppercase_checkbox.setGeometry(970, 548, 50, 50)
        self.use_uppercase_checkbox.setStyleSheet("""
            QPushButton {
                background-color: #fdfdfd; 
                color: black;              
                border: none;              
                border-radius: 10px;       
                font-size: 30px;           
            }
        """)
        self.use_uppercase_checkbox.clicked.connect(self.toggle_uppercase)

        self.use_symbols_checkbox = QtWidgets.QPushButton('✕', self)
        self.use_symbols_checkbox.setGeometry(1550, 548, 50, 50)
        self.use_symbols_checkbox.setStyleSheet("""
            QPushButton {
                background-color: #fdfdfd; 
                color: black;              
                border: none;              
                border-radius: 10px;       
                font-size: 30px;           
            }
        """)
        self.use_symbols_checkbox.clicked.connect(self.toggle_symbols)

    def generate_password(self):
        length_text = self.length_input.text()
        if not length_text.isdigit():
            QMessageBox.warning(self,
                self.tr('error'),
                self.tr('invalid_password_length'))
            return

        length = int(length_text)
        use_uppercase = self.use_uppercase_checkbox.text() == '✓'
        use_symbols = self.use_symbols_checkbox.text() == '✓'

        lower = string.ascii_lowercase
        upper = string.ascii_uppercase if use_uppercase else ''
        num = string.digits
        symbols = string.punctuation if use_symbols else ''

        all_characters = lower + upper + num + symbols

        if not all_characters:
            QMessageBox.warning(self, "Ошибка", "Необходимо выбрать хотя бы один тип символов для генерации пароля.")
            return

        passwords = ["".join(random.choice(all_characters) for _ in range(length)) for _ in range(3)]

        self.variant1_input.setText(passwords[0])
        self.variant2_input.setText(passwords[1])
        self.variant3_input.setText(passwords[2])

    def toggle_language(self):
        # Переключаем между русским и английским
        new_lang = 'en' if self.lang_manager.current_lang == 'ru' else 'ru'
        self.lang_manager.load_language(new_lang)
        self.update_ui_language()

    def update_ui_language(self):
        """Обновление текстов интерфейса"""
        t = self.lang_manager.translations
        self.lang_btn.setText(t.get('current_language', 'Language'))
        self.setWindowTitle(t.get('password_generation_window_title', 'Password Generation'))
        self.plus_button.setText(t.get('generate_password', 'Generate Password'))
        self.variant1_label.setText(f"{t.get('variant', 'Variant')} 1:")
        self.variant2_label.setText(f"{t.get('variant', 'Variant')} 2:")
        self.variant3_label.setText(f"{t.get('variant', 'Variant')} 3:")
        self.use_uppercase_button.setText(t.get('use_uppercase', 'Use uppercase'))
        self.use_symbols_button.setText(t.get('use_symbols', 'Use symbols'))
        self.wind1.setText(t.get('password_length', 'Password length'))

    def tr(self, key: str) -> str:
        return self.lang_manager.translations.get(key, key)

    def toggle_uppercase(self):
        if self.use_uppercase_checkbox.text() == '✕':
            self.use_uppercase_checkbox.setText('✓')
        else:
            self.use_uppercase_checkbox.setText('✕')

    def toggle_symbols(self):
        if self.use_symbols_checkbox.text() == '✕':
            self.use_symbols_checkbox.setText('✓')
        else:
            self.use_symbols_checkbox.setText('✕')

    def copy_to_clipboard(self, input_field):
        if not input_field.text():
            QMessageBox.warning(self, self.tr('error'), self.tr('empty_password'))
            return
        # Копируем текст в буфер обмена
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(input_field.text())

        # Показываем сообщение
        QMessageBox.information(self,
                                self.tr('copied'),
                                self.tr('password_copied'))


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = PasswordWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()