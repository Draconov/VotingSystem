from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QRadioButton, QPushButton, QButtonGroup, QMessageBox

class VoteDialog(QDialog):
    def __init__(self, db_manager, encryption_manager, user):
        super().__init__()
        self.db_manager = db_manager
        self.encryption_manager = encryption_manager
        self.user = user
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Голосование")
        layout = QVBoxLayout(self)

        self.question_label = QLabel("За кого вы хотите проголосовать?")
        layout.addWidget(self.question_label)

        self.button_group = QButtonGroup(self)
        self.republican_radio = QRadioButton("Republicans")
        self.democrat_radio = QRadioButton("Democrats")
        self.button_group.addButton(self.republican_radio)
        self.button_group.addButton(self.democrat_radio)

        layout.addWidget(self.republican_radio)
        layout.addWidget(self.democrat_radio)

        self.vote_button = QPushButton("Проголосовать")
        layout.addWidget(self.vote_button)

        self.vote_button.clicked.connect(self.submit_vote)

    def submit_vote(self):
        selected_button = self.button_group.checkedButton()
        if not selected_button:
            QMessageBox.warning(self, "Ошибка", "Выберите вариант для голосования")
            return

        choice = "Republican" if selected_button == self.republican_radio else "Democrat"
        encrypted_choice = self.encryption_manager.encrypt(choice)

        try:
            encrypted_choice = self.encryption_manager.encrypt(choice)
            self.db_manager.add_vote_with_zkp(self.user['id'], encrypted_choice)
            QMessageBox.information(self, "Успех", "Ваш голос учтен")
            self.accept()
        except Exception as e:
            if str(e) == "User has already voted":
                QMessageBox.warning(self, "Ошибка", "Вы уже проголосовали")
            else:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить голос: {str(e)}")