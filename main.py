import json
import requests
import sqlite3
import PySimpleGUI as sg

BASE_URL = 'http://10.1.4.88:5000/api/admin/'

def get_users():
    print(f'Запрашиваю пользователей..')
    res = requests.get(BASE_URL + 'users')
    print(res)
    print(res.text)
    users = json.loads(res.text)
    return users


def get_groups():
    print(f'Запрашиваю группы..')
    res = requests.get(BASE_URL + 'groups')
    print(res)
    print(res.text)
    groups = json.loads(res.text)
    add_groups(groups)


def add_users(users_list):
    # print(scheme)
    con = sqlite3.connect('pashi_db.db')
    cur = con.cursor()
    for user in users_list:
        # print(user)
        print(user['id'], user['login'], user['displayName'])
        db_insert_user = "insert or replace into Users(id, login, Display_name) Values ('" + user['id'] + "', '" + user['login'] + "', '" + user['displayName'] + "')"
        print(db_insert_user)
        cur.execute(db_insert_user)
        print(f'{user["login"]} добавлен')
    con.commit()
    con.close()

def add_groups(groups_list):
    con = sqlite3.connect('pashi_db.db')
    cur = con.cursor()
    for group in groups_list:
        # print(group)
        # print(user)
        print(group['id'], group['name'])
        db_insert_group = "insert or replace into Groups(id, Name) Values ('" + group['id'] + "', '" + group['name'] + "')"
        print(db_insert_group)
        cur.execute(db_insert_group)
        print(f'{group["name"]} добавлена')
    con.commit()
    con.close()


def get_users_from_db():
    con = sqlite3.connect('pashi_db.db')
    cur = con.cursor()
    cur.execute('select * from users')
    users = cur.fetchall()
    print('Пользователи:')
    users_for_table = list()
    for user in users:
        print(user)
        user_for_table = list()
        user_for_table.append(user[0])
        user_for_table.append(user[1])
        user_for_table.append(user[3])
        print(user_for_table)
        users_for_table.append(user_for_table)
    print('---')
    print(users_for_table)
    con.close()
    return users_for_table


if __name__ == '__main__':
    users_from_db = get_users_from_db()
    users_max = get_users()
    add_users(users_max)
    get_groups()
    users_from_db.sort(key=lambda i: i[1])
    print(users_from_db)
    layout = [[sg.Text("Пользователи")],
              [sg.Table(users_from_db, headings=('id', 'Логин', 'Имя'), justification="left", num_rows="40"), sg.Table(users_from_db, headings=('id', 'Логин', 'Имя'), justification="left", num_rows="40")],
              [sg.Button('Ok')]]

    # Create the window
    window = sg.Window('Window Title', layout, size = (1024, 768))  # Part 3 - Window Defintion

    # Display and interact with the Window
    event, values = window.read()  # Part 4 - Event loop or Window.read call

    # Do something with the information gathered
    # print('Hello', values[0], "! Thanks for trying PySimpleGUI")

    # Finish up by removing from the screen
    window.close()  # Part 5 - Close the Window


