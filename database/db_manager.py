import mysql.connector
from utils.zkp import ZKP, zkp


class DatabaseManager:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="votinggui" # имя базы данных
        )
        self.cursor = self.connection.cursor()
        self.create_tables()


    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS states (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS cities (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            state_id INT,
            FOREIGN KEY (state_id) REFERENCES states(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            password BLOB NOT NULL,
            city_id INT,
            FOREIGN KEY (city_id) REFERENCES cities(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            choice BLOB NOT NULL,
            proof VARCHAR(1000),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)

        self.connection.commit()

    def register_user(self, username, encrypted_password, city_id):
        query = "INSERT INTO users (username, password, city_id) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (username, encrypted_password, city_id))
        self.connection.commit()

    def get_user(self, username):
        query = "SELECT id, password, city_id FROM users WHERE username = %s"
        self.cursor.execute(query, (username,))
        return self.cursor.fetchone()

    def has_user_voted(self, user_id):
        query = "SELECT COUNT(*) FROM votes WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        count = self.cursor.fetchone()[0]
        return count > 0

    '''
    def add_vote(self, user_id, encrypted_choice):
        if self.has_user_voted(user_id):
            raise Exception("User has already voted")
        query = "INSERT INTO votes (user_id, choice) VALUES (%s, %s)"
        self.cursor.execute(query, (user_id, encrypted_choice))
        self.connection.commit()
    '''

    def add_vote_with_zkp(self, user_id, encrypted_choice):
        # Генерация доказательства
        proof = zkp.generate_proof(encrypted_choice)

        # Сохранение зашифрованного выбора и доказательства
        query = "INSERT INTO votes (user_id, choice, proof) VALUES (%s, %s, %s)"
        proof_str = f"{proof[0]},{proof[1]}"
        self.cursor.execute(query, (user_id, encrypted_choice, proof_str))
        self.connection.commit()

    def verify_vote(self, vote_id):
        query = "SELECT choice, proof FROM votes WHERE id = %s"
        self.cursor.execute(query, (vote_id,))
        result = self.cursor.fetchone()
        if result:
            encrypted_choice, proof_str = result
            r, s = map(int, proof_str.split(','))
            return zkp.verify_proof(encrypted_choice, (r, s))
        return False

    def get_cities(self):
        query = "SELECT id, name, state_id FROM cities"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_states(self):
        query = "SELECT id, name FROM states"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_votes(self):
        query = """
        SELECT v.id, v.user_id, v.choice, v.proof, c.name as city_name, s.name as state_name
        FROM votes v
        JOIN users u ON v.user_id = u.id
        JOIN cities c ON u.city_id = c.id
        JOIN states s ON c.state_id = s.id
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()