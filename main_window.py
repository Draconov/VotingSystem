from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from .login_dialog import LoginDialog
from .register_dialog import RegisterDialog
from .vote_dialog import VoteDialog
from .results_dialog import ResultsDialog

class MainWindow(QMainWindow):
    def __init__(self, db_manager, encryption_manager):
        super().__init__()
        self.db_manager = db_manager
        self.encryption_manager = encryption_manager
        self.current_user = None
        self.setup_ui()
        self.has_voted = False

    def setup_ui(self):
        self.setWindowTitle("VotingSystem")
        self.setGeometry(100, 100, 300, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.login_button = QPushButton("Войти")
        self.register_button = QPushButton("Зарегистрироваться")
        self.vote_button = QPushButton("Проголосовать")
        self.results_button = QPushButton("Посмотреть результаты")

        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        layout.addWidget(self.vote_button)
        layout.addWidget(self.results_button)

        self.login_button.clicked.connect(self.show_login)
        self.register_button.clicked.connect(self.show_register)
        self.vote_button.clicked.connect(self.show_vote)
        self.results_button.clicked.connect(self.show_results)

        self.update_button_states()

    def show_login(self):
        dialog = LoginDialog(self.db_manager, self.encryption_manager)
        if dialog.exec_():
            self.current_user = dialog.get_user()
            self.has_voted = self.db_manager.has_user_voted(self.current_user['id'])
            self.update_button_states()

    def show_register(self):
        dialog = RegisterDialog(self.db_manager, self.encryption_manager)
        if dialog.exec_():
            self.current_user = dialog.get_user()
            self.has_voted = False
            self.update_button_states()

    def show_vote(self):
        if self.current_user and not self.has_voted:
            dialog = VoteDialog(self.db_manager, self.encryption_manager, self.current_user)
            if dialog.exec_():
                self.has_voted = True
                self.update_button_states()

    def show_results(self):
        dialog = ResultsDialog(self.db_manager, self.encryption_manager)
        dialog.exec_()

    def update_button_states(self):
        is_logged_in = self.current_user is not None
        self.login_button.setEnabled(not is_logged_in)
        self.register_button.setEnabled(not is_logged_in)
        self.vote_button.setEnabled(is_logged_in and not self.has_voted)
        self.results_button.setEnabled(True)