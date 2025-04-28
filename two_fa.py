from PyQt5 import QtWidgets, QtGui, QtCore


class VerificationWindow(QtWidgets.QWidget):
    def __init__(self, main_window, username):
        super().__init__()
        self.main_window = main_window
        self.username = username
        self.lang_manager = main_window.lang_manager
        self.initUI()

    def tr(self, key: str) -> str:
        return self.lang_manager.translations.get(key, key)

    def initUI(self):
        self.setWindowTitle(self.tr('verification_title'))
        self.setGeometry(600, 400, 400, 200)

        # Стиль фона
        self.setStyleSheet("background-color: #f0f0f0;")

        layout = QtWidgets.QVBoxLayout()

        self.code_label = QtWidgets.QLabel(self.tr('enter_code'))
        self.code_label.setStyleSheet("font-size: 16px;")

        self.code_input = QtWidgets.QLineEdit()
        self.code_input.setPlaceholderText("XXXX")
        self.code_input.setMaxLength(4)
        self.code_input.setStyleSheet("""
            QLineEdit {
                font-size: 20px;
                padding: 10px;
                border-radius: 10px;
                border: 2px solid #ccc;
            }
        """)

        self.verify_button = QtWidgets.QPushButton(self.tr('verify_button'))
        self.verify_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.verify_button.clicked.connect(self.verify_code)

        layout.addWidget(self.code_label)
        layout.addWidget(self.code_input)
        layout.addWidget(self.verify_button)
        self.setLayout(layout)

    def verify_code(self):
        entered_code = self.code_input.text().strip()
        if self.main_window.check_verification_code(self.username, entered_code):
            self.main_window.open_login_window()
            self.close()
        else:
            QtWidgets.QMessageBox.warning(
                self,
                self.tr('error'),
                self.tr('invalid_code')
            )
