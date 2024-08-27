# VotingSystem

VotingSystem - это приложение для проведения электронного голосования, разработанное с использованием Python, PyQt5 и MySQL.

## Особенности

- Регистрация и аутентификация пользователей
- Безопасное голосование с шифрованием данных
- Предотвращение повторного голосования
- Подсчет голосов на уровне городов, штатов и страны
- Отображение результатов голосования

## Требования

- Python 3.9+
- PyQt5
- mysql-connector-python
- cryptography

## Установка

1. Клонируйте репозиторий:
git clone https://github.com/Draconov/VotingSystem.git
cd VotingSystem
Copy
2. Установите зависимости:
pip install -r requirements.txt
Copy
3. Настройте базу данных MySQL:
- Создайте базу данных с именем `votinggui`
- Обновите учетные данные для подключения к базе данных в файле `database/db_manager.py`

4. Создайте ключ шифрования:
python create_encryption_key.py
Copy
5. Инициализируйте базу данных:
python init_database.py
Copy
## Использование

Запустите приложение:
python main.py
Copy
## Структура проекта

- `main.py`: Точка входа в приложение
- `database/`: Модули для работы с базой данных
- `gui/`: Модули пользовательского интерфейса
- `utils/`: Вспомогательные модули

## Безопасность

- Пароли пользователей и голоса шифруются перед сохранением в базе данных
- Ключ шифрования хранится в отдельном файле (`encryption_key.key`)
- Реализована защита от повторного голосования

## Разработка

Для добавления новых функций или изменения существующих:

1. Создайте новую ветку: `git checkout -b feature/my-new-feature`
2. Внесите изменения и зафиксируйте их: `git commit -am 'Add some feature'`
3. Отправьте изменения в удаленный репозиторий: `git push origin feature/my-new-feature`
4. Создайте Pull Request

## Лицензия

[MIT License](https://opensource.org/licenses/MIT)

## Контакты

Разработка: מיכאל טוצינסקי

Ссылка на проект: [https://github.com/Draconov/VotingSystem](https://github.com/Draconov/VotingSystem)
