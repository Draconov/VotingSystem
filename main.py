import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from database.db_manager import DatabaseManager
from utils.encryption import EncryptionManager


def main():
    app = QApplication(sys.argv)

    # Инициализация менеджеров
    db_manager = DatabaseManager()
    encryption_manager = EncryptionManager()

    # Создание и отображение главного окна
    main_window = MainWindow(db_manager, encryption_manager)
    main_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()