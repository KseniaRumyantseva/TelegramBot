import server

def categoriesList(categories):
    cs = ''
    for category in categories:
        cs += category + "\n"
    return cs

# работа с юзером
def add_user(login):
    server.cursor.execute('INSERT INTO users(login) VALUES (?)', (login,))
    server.connect.commit()


def check_user(login):
    res = server.cursor.execute('SELECT login FROM users WHERE login=?', (login,)).fetchone()
    return res


def add_subscribe(category, user_id):
    ress = [*(x for t in server.cursor.execute('SELECT name FROM categories').fetchall() for x in t)]
    user = server.cursor.execute('SELECT * FROM users WHERE login=?', (user_id,)).fetchone()
    if category in ress:
        categ = server.cursor.execute('SELECT * FROM categories WHERE name=?', (category,)).fetchone()
        rescat = server.cursor.execute('SELECT name FROM categories WHERE name=?', (category,)).fetchone()
        ressub = server.cursor.execute('SELECT * FROM subscriptions WHERE id_user=? AND id_category=?',
                                       (user[0], categ[0])).fetchone()
        if rescat is not None and ressub is None:
            server.cursor.execute('INSERT INTO subscriptions(id_user, id_category) VALUES (?, ?)', (user[0], categ[0]))
            server.connect.commit()
            return ('Вы подписались на новую категорию!')
        elif rescat is not None and ressub is not None:
            return ('Вы уже подписаны на эту категорию!')
    else:
        return ('Такой категории нет!')


def delete_subscribe(category, user_id):
    ress = [*(x for t in server.cursor.execute('SELECT name FROM categories').fetchall() for x in t)]
    user = server.cursor.execute('SELECT * FROM users WHERE login=?', (user_id,)).fetchone()
    if category in ress:
        categ = server.cursor.execute('SELECT * FROM categories WHERE name=?', (category,)).fetchone()
        rescat2 = server.cursor.execute('SELECT name FROM categories WHERE name=?', (category,)).fetchone()
        ressub2 = server.cursor.execute('SELECT * FROM subscriptions WHERE id_user=? AND id_category=?',
                                 (user[0], categ[0])).fetchone()
        if rescat2 is not None and ressub2 is not None:
            server.cursor.execute(
                'DELETE FROM subscriptions WHERE subscriptions.id_user = ? AND subscriptions.id_category = ?',
                (user[0], categ[0]))
            server.connect.commit()
            return ('Вы отписались от категории!')
        elif rescat2 is not None and ressub2 is None:
            return ('Вы не подписаны на эту категорию!')
    else:
        return ('Такой категории нет!')


def show_mycategories(user_id):
    user = server.cursor.execute('SELECT * FROM users WHERE login=?', (user_id,)).fetchone()
    res = server.cursor.execute('SELECT categories.name FROM subscriptions INNER JOIN categories ON subscriptions.id_category = categories.id WHERE subscriptions.id_user = ?',
        (user[0],)).fetchall()
    if res != []:
        cats = [*(x for t in res for x in t)]
        return f'Категории, на которые вы подписаны: \n{categoriesList(cats)}'
    else:
        return "У вас нет подписок! " \
               "Воспользуйтесь командой /subscribe, чтобы подписаться на категории"

def user_categories(user_id):
    user = server.cursor.execute('SELECT * FROM users WHERE login=?', (user_id,)).fetchone()
    res = server.cursor.execute('SELECT categories.name FROM subscriptions INNER JOIN categories ON subscriptions.id_category = categories.id WHERE subscriptions.id_user = ?',
        (user[0],)).fetchall()
    return [*(x for t in res for x in t)]

# работа с категориями

def add_category(category):
    res = server.cursor.execute('SELECT name FROM categories WHERE name=?', (category,)).fetchone()
    if res is None:
        server.cursor.execute('INSERT INTO categories(name) VALUES (?)', (category,))
        server.connect.commit()
        print('Добавлена новая категория!')
    else:
        print('Такая категория уже есть!')


def delete_category():
    category = input('Введите название категории: ')
    categ = server.cursor.execute('SELECT * FROM categories WHERE name=?', (category,)).fetchone()
    if categ is not None:
        server.cursor.execute('DELETE FROM categories WHERE categories.id = ?', (categ[0],))
        server.connect.commit()
        server.cursor.execute('DELETE FROM subscriptions WHERE subscriptions.id_category = ?', (categ[0],))
        server.connect.commit()
        print('Категория удалена!')
    else:
        print('Категория не найдена!')


def show_categories():
    res = server.cursor.execute('SELECT name FROM categories').fetchall()
    return res
