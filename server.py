import sqlite3
import config
import functions

connect = sqlite3.connect('database.db', check_same_thread=False)
cursor = connect.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL,
	"login"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);''')

cursor.execute('''CREATE TABLE IF NOT EXISTS "categories" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);''')

cursor.execute('''CREATE TABLE IF NOT EXISTS "subscriptions" (
	"id_user"	INTEGER NOT NULL,
	"id_category"	INTEGER NOT NULL
);''')

connect.commit()

for category in config.categories:
    # functions.add_category(category)
    res = cursor.execute('SELECT name FROM categories WHERE name=?', (category,)).fetchone()
    if res is None:
        cursor.execute('INSERT INTO categories(name) VALUES (?)', (category,))
        connect.commit()
        print('Добавлена новая категория!')

# cursor.close()
