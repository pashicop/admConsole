import json
import requests
import sqlite3
import PySimpleGUI as sg
from io import BytesIO
from PIL import Image, ImageDraw

BASE_URL = 'http://10.1.4.88:5000/api/admin/'

def icon(check):
    box = (32, 32)
    background = (255, 255, 255, 0)
    rectangle = (3, 3, 29, 29)
    line = ((9, 17), (15, 23), (23, 9))
    im = Image.new('RGBA', box, background)
    draw = ImageDraw.Draw(im, 'RGBA')
    draw.rectangle(rectangle, outline='black', width=3)
    if check == 1:
        draw.line(line, fill='black', width=3, joint='curve')
    elif check == 2:
        draw.line(line, fill='grey', width=3, joint='curve')
    with BytesIO() as output:
        im.save(output, format="PNG")
        png = output.getvalue()
    return png

check = [icon(0), icon(1), icon(2)]

def get_users():
    print(f'Запрашиваю пользователей..')
    res = requests.get(BASE_URL + 'users')
    print(res)
    # print(res.text)
    users = json.loads(res.text)
    return users


def get_groups():
    print(f'Запрашиваю группы..')
    res = requests.get(BASE_URL + 'groups')
    print(res)
    # print(res.text)
    groups = json.loads(res.text)
    add_groups(groups)


def add_users(users_list):
    # print(scheme)
    con = sqlite3.connect('pashi_db.db')
    cur = con.cursor()
    for user in users_list:
        # print(user)
        # print(user['id'], user['login'], user['displayName'])
        db_insert_user = "insert or replace into Users(id, login, Display_name) Values ('" + user['id'] + "', '" + user['login'] + "', '" + user['displayName'] + "')"
        # print(db_insert_user)
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
        # print(group['id'], group['name'])
        db_insert_group = "insert or replace into Groups(id, Name) Values ('" + group['id'] + "', '" + group['name'] + "')"
        # print(db_insert_group)
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

def get_groups_from_db():
    con = sqlite3.connect('pashi_db.db')
    cur = con.cursor()
    cur.execute('select * from groups')
    groups = cur.fetchall()
    print('Группы:')
    groups_for_table = list()
    for group in groups:
        print(group)
        group_for_table = list()
        group_for_table.append(group[0])
        group_for_table.append(group[1])
        print(group_for_table)
        groups_for_table.append(group_for_table)
    print('---')
    print(groups_for_table)
    con.close()
    return groups_for_table

def get_groups_for_user(id):
    print(f'Запрашиваю группу для ', id)
    res = requests.get(BASE_URL + 'users')
    # print(res)
    # print(res.text)
    users = json.loads(res.text)
    res_groups = list()
    for user in users:
        if user['id'] == id:
            groups_ids = user['userGroupIds']
            # print(user['userGroupIds'])
            for group_id in groups_ids:
                group_name = get_group_name_by_id(group_id)
                print(group_name)
                res_group = [group_id, group_name]
                res_groups.append(res_group)
    res_groups.sort(key=lambda i: i[1])
    return res_groups

def get_group_name_by_id(id):
    print(f'Запрашиваю имя группы..')
    res = requests.get(BASE_URL + 'groups')
    # print(res)
    # print(res.text)
    groups = json.loads(res.text)
    for group in groups:
        if group['id'] == id:
            name = group['name']
            break
    return name

if __name__ == '__main__':
    users_from_db = get_users_from_db()
    groups_from_db = get_groups_from_db()
    users_max = get_users()
    add_users(users_max)
    get_groups()
    users_from_db.sort(key=lambda i: i[1])
    groups_from_db.sort(key=lambda i: i[1])
    print(users_from_db)
    print(groups_from_db)
    treedata = sg.TreeData()
    for group_id, group_name in groups_from_db:
        treedata.insert('',group_id, group_id, values=[group_name], icon=check[0])
    layout = [[sg.Tree(data=treedata, headings=('Имя',), auto_size_columns=True,
        num_rows=10, col0_width=20, key='-TREE-', row_height=48, metadata=[],
        show_expanded=False, enable_events=True,
        select_mode=sg.TABLE_SELECT_MODE_BROWSE)],]
    # layout = [[sg.Text("Пользователи", size=(50, 1), justification='center'), sg.Text("Группы", size=(50, 1), justification='center')],
    #           [sg.Table(users_from_db, headings=('id', 'Логин', 'Имя'), justification="left", num_rows="40", enable_events=True, key='-users-'),
    #            sg.Table(groups_from_db, headings=('id', 'Имя'), justification="left", num_rows="40", enable_events=True, key='-groups-')
    #            ],
    #           [sg.Button('Ok')]]

    layout = [[sg.Text("Пользователи", size=(50, 1), justification='center'), sg.Text("Группы", size=(50, 1), justification='center')],
              [sg.Table(users_from_db, headings=('id', 'Логин', 'Имя'), justification="left", num_rows="40", enable_events=True, key='-users-'),
               sg.Table(groups_from_db, headings=('id', 'Имя'), justification="left", num_rows="40", enable_events=True, key='-groups-'),
               sg.Tree(data=treedata, headings=('Имя',), auto_size_columns=True,
                       num_rows=10, col0_width=20, key='-TREE-', row_height=30, metadata=[],
                       show_expanded=False, enable_events=True, justification='left', expand_y="True",
                       select_mode=sg.TABLE_SELECT_MODE_BROWSE),
               ],
              [sg.Button('Ok')]]

    # window = sg.Window('Панель администратора', layout, size=(1024, 768))
    window = sg.Window('Tree as Table', layout, finalize=True)
    tree = window['-TREE-']
    tree.Widget.heading("#0", text='id')  # Set heading for column #0
    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == '-users-':
            print(values['-users-'])
            user_id = users_from_db[values['-users-'][0]][0]
            print(user_id)
            groups_for_user = get_groups_for_user(user_id)
            group_for_user_ids = []
            for group_for_user in groups_for_user:
                group_for_user_ids.append(group_for_user[0])
            print(group_for_user_ids)
            all_group_ids = []
            for group_from_all in groups_from_db:
                all_group_ids.append(group_from_all[0])
            print(all_group_ids)
            window['-groups-'].update(groups_for_user)
            tree.metadata = []
            for group_id_for_tree in all_group_ids:
                if group_id_for_tree in group_for_user_ids:
                    print(group_id_for_tree)
                    tree.metadata.append(group_id_for_tree)
                    tree.update(key=group_id_for_tree, icon=check[1])
                else:
                    tree.update(key=group_id_for_tree, icon=check[0])
                #
                # if group_id_for_tree[0] not in tree.metadata:
                #     tree.metadata.append(group_id_for_tree[0])
                #     tree.update(key=group_id_for_tree[0], icon=check[1])
        if event == '-TREE-':
            group_id = values['-TREE-'][0]
            print(group_id)
            if group_id in tree.metadata:
                tree.metadata.remove(group_id)
                tree.update(key=group_id, icon=check[0])
            else:
                tree.metadata.append(group_id)
                tree.update(key=group_id, icon=check[1])
    window.close()


