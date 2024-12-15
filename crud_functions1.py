import sqlite3
def initiate_db():
    connection = sqlite3.connect("Fruts.db")
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER
    );
    ''')
    connection.commit()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    );
    ''')
    connection.commit()
    connection.close()
def check_db(id, title, description, price):
    connection = sqlite3.connect('Fruts.db')
    cursor = connection.cursor()
    check_db = cursor.execute('SELECT * FROM Products WHERE title=?', (title,))
    if check_db.fetchone() is None:
        cursor.execute(f'''
    INSERT INTO Products (id, title, description, price) VALUES('{id}', '{title}', '{description}', '{price}')
''')
    connection.commit()
    connection.close()
initiate_db()

check_db(1, 'lemon', 'Сплошной витамин С', 100)
check_db(2, 'mango', 'Профилактика раковых новообразований', 200)
check_db(3, 'grapefrute', 'Микроэлементы для сердца', 300)
check_db(4, 'granat', 'Рубиновый сочный цвет и масса железа!', 400)


def get_all_products():
    connection = sqlite3.connect('Fruts.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products WHERE id > ?', (0,))
    data = cursor.fetchall()
    connection.commit()
    connection.close()
    return data
def add_user(username, email, age):
    connection = sqlite3.connect("Fruts.db")
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Users")
    #total_users = cursor.fetchone()[0] + 1
    cursor.execute(f"INSERT INTO Users (username, email, age, balance ) VALUES(?, ?, ?, ?)",
                   (f'{username}', f'{email}', age, 1000))
    connection.commit()
    connection.close()

# def add_user(username, email, age):
#     connection = sqlite3.connect("Fruts.db")
#     cursor = connection.cursor()
#     cursor.execute("SELECT COUNT(*) FROM Users")
#     total_users = cursor.fetchone()[0]+1
#     cursor.execute(f'''
#     INSERT INTO Users VALUES('{total_users}', '{username}', '{email}', '{age}', '1000')
#     ''')
#     connection.commit()
#     connection.close()
def is_included(username):
    connection = sqlite3.connect("Fruts.db")
    cursor = connection.cursor()
    is_incl = True
    check_username = cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    if check_username.fetchone() is None:
        is_incl = False
    return is_incl
    connection.commit()
    connection.close()

