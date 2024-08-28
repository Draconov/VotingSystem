from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class LoginDialog(QDialog):
    def __init__(self, db_manager, encryption_manager):
        super().__init__()
        self.db_manager = db_manager
        self.encryption_manager = encryption_manager
        self.user = None
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Вход")
        layout = QVBoxLayout(self)

        self.username_label = QLabel("Имя пользователя:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Войти")

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.login_button.clicked.connect(self.login)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        user_data = self.db_manager.get_user(username)
        if user_data:
            user_id, encrypted_password, city_id = user_data
            decrypted_password = self.encryption_manager.decrypt(encrypted_password)
            if password == decrypted_password:
                self.user = {'id': user_id, 'username': username, 'city_id': city_id}
                self.accept()
            else:
                QMessageBox.warning(self, "Ошибка", "Неверный пароль")
        else:
            QMessageBox.warning(self, "Ошибка", "Пользователь не найден")

    def get_user(self):
        return self.user