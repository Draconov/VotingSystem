import mysql.connector
from database.db_manager import DatabaseManager
from utils.encryption import EncryptionManager

def init_database():
    # Создаем подключение к MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root"
    )
    cursor = conn.cursor()

    # Создаем базу данных
    cursor.execute("CREATE DATABASE IF NOT EXISTS votinggui")
    conn.commit()
    conn.close()

    # Инициализируем менеджеры
    encryption_manager = EncryptionManager()
    db_manager = DatabaseManager(encryption_manager)

    # Создаем таблицы
    db_manager.create_tables()

    # Добавляем начальные данные
    add_initial_data(db_manager)

    print("Database initialized successfully.")

def add_initial_data(db_manager):
    # Добавляем штаты
    states = [
        "California", "Texas", "Florida", "New York", "Pennsylvania",
        "Illinois", "Ohio", "Georgia", "North Carolina", "Michigan"
    ]
    for state in states:
        db_manager.add_state(state)

    # Добавляем города (по 3 для каждого штата)
    cities = [
        ("Los Angeles", "California"), ("San Francisco", "California"), ("San Diego", "California"),
        ("Houston", "Texas"), ("Dallas", "Texas"), ("Austin", "Texas"),
        ("Miami", "Florida"), ("Orlando", "Florida"), ("Tampa", "Florida"),
        ("New York City", "New York"), ("Buffalo", "New York"), ("Rochester", "New York"),
        ("Philadelphia", "Pennsylvania"), ("Pittsburgh", "Pennsylvania"), ("Allentown", "Pennsylvania"),
        ("Chicago", "Illinois"), ("Aurora", "Illinois"), ("Rockford", "Illinois"),
        ("Columbus", "Ohio"), ("Cleveland", "Ohio"), ("Cincinnati", "Ohio"),
        ("Atlanta", "Georgia"), ("Augusta", "Georgia"), ("Savannah", "Georgia"),
        ("Charlotte", "North Carolina"), ("Raleigh", "North Carolina"), ("Greensboro", "North Carolina"),
        ("Detroit", "Michigan"), ("Grand Rapids", "Michigan"), ("Ann Arbor", "Michigan")
    ]
    for city, state in cities:
        db_manager.add_city(city, state)

    print("Initial data added successfully.")

if __name__ == "__main__":
    init_database()