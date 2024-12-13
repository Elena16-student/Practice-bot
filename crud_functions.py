import sqlite3
def initiate_db():
    connection = sqlite3.connect('Fruts.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
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

# check_db(1, 'lemon', 'Сплошной витамин С', 100)
# check_db(2, 'mango', 'Профилактика раковых новообразований', 200)
# check_db(3, 'grapefrute', 'Микроэлементы для сердца', 300)
# check_db(4, 'granat', 'Рубиновый сочный цвет и масса железа!', 400)
def get_all_products():
    connection = sqlite3.connect('Fruts.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products WHERE id > ?', (0,))

    connection.commit()
    connection.close()

    return cursor.fetchall()