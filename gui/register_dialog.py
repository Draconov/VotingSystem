from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox

class RegisterDialog(QDialog):
    def __init__(self, db_manager, encryption_manager):
        super().__init__()
        self.db_manager = db_manager
        self.encryption_manager = encryption_manager
        self.user = None
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Регистрация")
        layout = QVBoxLayout(self)

        self.username_label = QLabel("Имя пользователя:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.city_label = QLabel("Город:")
        self.city_combo = QComboBox()
        self.register_button = QPushButton("Зарегистрироваться")

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.city_label)
        layout.addWidget(self.city_combo)
        layout.addWidget(self.register_button)

        self.register_button.clicked.connect(self.register)

        self.load_cities()

    def load_cities(self):
        cities = self.db_manager.get_cities()
        for city_id, city_name, _ in cities:
            self.city_combo.addItem(city_name, city_id)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        city_id = self.city_combo.currentData()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        existing_user = self.db_manager.get_user(username)
        if existing_user:
            QMessageBox.warning(self, "Ошибка", "Пользователь с таким именем уже существует")
            return

        encrypted_password = self.encryption_manager.encrypt(password)
        self.db_manager.register_user(username, encrypted_password, city_id)

        self.user = {'id': self.db_manager.cursor.lastrowid, 'username': username, 'city_id': city_id}
        self.accept()

    def get_user(self):
        return self.user