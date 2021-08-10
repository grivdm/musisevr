import sqlite3


def db_table_val(user_id: int, user_lng: int):
    con = sqlite3.connect('bot_db', check_same_thread=False)
    cursor = con.cursor()
    try:
        cursor.execute('INSERT INTO bot_db (user_id, user_lng) VALUES (?, ?)', (user_id, user_lng))
        con.commit()
    except sqlite3.IntegrityError:
        None
    cursor.close()
    con.close()


def db_table_upd(user_id: int, user_lng: int):
    con = sqlite3.connect('bot_db', check_same_thread=False)
    cursor = con.cursor()
    cursor.execute(f'UPDATE bot_db SET user_lng = {user_lng} WHERE user_id = {user_id}')
    con.commit()
    cursor.close()
    con.close()


def db_select(user_id: int):
    con = sqlite3.connect('bot_db', check_same_thread=False)
    cursor = con.cursor()
    cursor.execute(f'SELECT user_lng FROM bot_db WHERE user_id = {user_id}')
    results = cursor.fetchall()
    cursor.close()
    con.close()
    return results[0][0]
