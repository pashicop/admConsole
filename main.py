import json
import threading
from time import sleep

import requests
import sqlite3
import re
import PySimpleGUI as sg
from io import BytesIO
from PIL import Image, ImageDraw
# import subprocess
from multiprocessing import Pool
from multiprocessing import Process, Queue

BASE_URL = 'http://10.1.4.147:5000/api/admin/'
ICON_BASE_64 = b'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'


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
    return groups


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
        # print(f'{user["login"]} добавлен')
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
        # print(f'{group["name"]} добавлена')
    con.commit()
    con.close()

def drop_db():
    con = sqlite3.connect('pashi_db.db')
    cur = con.cursor()
    db_delete_groups = "delete from Groups"
    db_delete_users = "delete from Users"
    db_delete_users_in_groups = "delete from Users_in_groups"
    cur.execute(db_delete_users)
    cur.execute(db_delete_groups)
    cur.execute(db_delete_users_in_groups)
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
        # print(user)
        user_for_table = list()
        user_for_table.append(user[1])
        user_for_table.append(user[3])
        user_for_table.append(user[0])
        print(user_for_table)
        users_for_table.append(user_for_table)
    print('---')
    # print(users_for_table)
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
        # print(group)
        group_for_table = list()
        group_for_table.append(group[1])
        group_for_table.append(group[0])
        print(group_for_table)
        groups_for_table.append(group_for_table)
    print('---')
    # print(groups_for_table)
    con.close()
    return groups_for_table

def get_users_for_group(id):
    print(f'Запрашиваю пользователей для группы', id)
    res = requests.get(BASE_URL + 'groups')
    # print(res)
    # print(res.text)
    groups = json.loads(res.text)
    res_users = list()
    for group in groups:
        if group['id'] == id:
            users_ids = group['userIds']
            print(group['userIds'])
            for user_id in users_ids:
                user_name = get_user_name_by_id(user_id)
                user_login = get_user_login_by_id(user_id)
                # print(user_name)
                # print(user_login)
                res_user = [user_login, user_name, user_id]
                if user_name:
                    res_users.append(res_user)
    res_users.sort(key=lambda i: i[0])
    return res_users

def get_user_name_by_id(id):
    # print(f'Запрашиваю имя пользователя..')
    res = requests.get(BASE_URL + 'users')
    # print(res)
    # print(res.text)
    name = ''
    users = json.loads(res.text)
    for user in users:
        if user['id'] == id:
            name = user['displayName']
            break
    return name

def get_user_login_by_id(id):
    # print(f'Запрашиваю логин пользователя..')
    res = requests.get(BASE_URL + 'users')
    # print(res)
    # print(res.text)
    login = ''
    users = json.loads(res.text)
    for user in users:
        if user['id'] == id:
            login = user['login']
            break
    return login

def get_groups_for_user(id):
    # print(f'Запрашиваю группу для ', id)
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
                # print(group_name)
                res_group = [group_name, group_id]
                res_groups.append(res_group)
    res_groups.sort(key=lambda i: i[1])
    return res_groups

def get_group_name_by_id(id):
    # print(f'Запрашиваю имя группы..')
    res = requests.get(BASE_URL + 'groups')
    # print(res)
    # print(res.text)
    name = ''
    groups = json.loads(res.text)
    for group in groups:
        if group['id'] == id:
            name = group['name']
            break
    return name

def make_main_window(users_online):
    users_online_text = 'Пользователей онлайн: ' + users_online
    tab1_layout = [[sg.Text("Пользователи", size=(50, 1), justification='center'),
                    sg.Text("Группы", size=(50, 1), justification='center')],
                   [sg.Table(users_from_db, headings=('Логин', 'Имя'), justification="left", num_rows="40",
                             enable_events=True, key='-users-'),
                    # sg.Table(groups_from_db, headings=('id', 'Имя'), justification="left", num_rows="40",
                    #          enable_events=True, key='-groups-'),
                    sg.Tree(data=treedata, headings=('Имя',''), auto_size_columns=True,
                            num_rows=10, col0_width=20, key='-TREE-', row_height=30, metadata=[],
                            show_expanded=False, enable_events=True, justification='left', expand_y="True",
                            select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                            expand_x=True),
                    ],
                   [sg.Push(), sg.Button('Обновить', key='update1'), sg.Button('Применить', key='Apply')],
                   [sg.Text(users_online_text, key='online1')],
                   ]
    tab2_layout = [[sg.Text("Группы", size=(35, 1), justification='center'),
                    sg.Text("Пользователи", size=(50, 1), justification='center')
                    ],
                   [sg.Table(groups_from_db, headings=('Имя', ''), justification="left", num_rows="40",
                             enable_events=True, key='-groups2-'),
                    # sg.Table(users_from_db, headings=('id', 'Логин', 'Имя'), justification="left", num_rows="40",
                    #          enable_events=True, key='-users2-'),
                    sg.Tree(data=treedata2, headings=('Логин', 'Имя'), auto_size_columns=True,
                            num_rows=10, col0_width=20, key='-TREE2-', row_height=30, metadata=[],
                            show_expanded=False, enable_events=True, justification='left', expand_y="True",
                            select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                            expand_x=True),
                    ],
                   [sg.Push(), sg.Button('Обновить', key='update2'), sg.Button('Применить', key='Apply2')],
                   [sg.Text(users_online_text, key='online2')],
                   ]
    layout = [[sg.TabGroup(
        [[sg.Tab('Пользователи', tab1_layout, key="Tab1"),
          sg.Tab('Группы', tab2_layout, key="Tab2")
          ]], key="Tabs")]]
    return sg.Window('Панель администратора', layout, icon=ICON_BASE_64, finalize=True)

def make_login_window():
    layout_login = [[sg.Push(), sg.Text("Адрес сервера"), sg.Input(default_text="10.1.4.147", key="ip")],
                    [sg.Push(), sg.Text("Пароль"), sg.Input(focus=True, key="password", password_char='*')],
                    [sg.Push(), sg.Ok(key="OK button"), sg.Push()]]
    return sg.Window('Вход на сервер', layout_login, icon=ICON_BASE_64, finalize=True)

# def ping_server(ip):
#     num = 0
#     while True:
#         res_ping = ''
#         try:
#             res_ping = requests.get(ip, timeout=3)
#         except Exception:
#             sg.popup("Сервер не отвечает", title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='gray')
#         num += 1
#         print(f'[{num}] Пингуем.. {res_ping.text}')
#         # print(out)
#         sleep(3)

def the_thread(ip, window):
    num = 0
    while True:
        res_ping = ''
        try:
            res_ping = requests.get(ip, timeout=3)
        except Exception:
            sg.popup("Сервер не отвечает", title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='gray')
        if res_ping.status_code == 200:
            num += 1
            print(f'[{num}] Пингуем.. {res_ping.text}')
            window.write_event_value('-THREAD-', (threading.currentThread().name, res_ping.text))
            # sg.cprint('This is cheating from the thread', c='white on green')
        # print(out)
        sleep(3)

if __name__ == '__main__':
    window_login = make_login_window()
    window_main_active = False
    # program = "notepad.exe"
    # process = subprocess.Popen(program)
    # code = process.wait()
    # print(code)  # 0
    while True:
        break_flag = False
        ev_login, val_login = window_login.Read()
        print(ev_login, val_login)
        if ev_login == sg.WIN_CLOSED:
            break
        if ev_login == "OK button" and not window_main_active:
            if val_login['password'] == 'qwerty':
                while True:
                    if break_flag:
                        break
                    re_ip = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")
                    if re_ip.match(val_login['ip']):
                        BASE_URL = 'http://' + val_login['ip'] + ':5000/api/admin/'
                        BASE_URL_PING = 'http://' + val_login['ip'] + ':5000/api/ping'
                        try:
                            res_ping = requests.get(BASE_URL_PING, timeout=3)
                        except Exception:
                            sg.popup("Сервер не отвечает", title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='gray')
                            break
                        drop_db()
                        users_max = get_users()
                        add_users(users_max)
                        groups_max = get_groups()
                        add_groups(groups_max)
                        users_from_db = get_users_from_db()
                        groups_from_db = get_groups_from_db()
                        users_from_db.sort(key=lambda i: i[0])
                        groups_from_db.sort(key=lambda i: i[0])
                        treedata = sg.TreeData()
                        treedata2 = sg.TreeData()
                        for group_name, group_id in groups_from_db:
                            treedata.insert('', group_id, '', values=[group_name], icon=check[0])
                        for user_login, user_name, user_id in users_from_db:
                            treedata2.insert('', user_id, '', values=[user_login, user_name], icon=check[0])
                        window_main_active = True
                        window_login.Hide()
                        window = make_main_window(res_ping.text)
                        tree = window['-TREE-']
                        tree.Widget.heading("#0", text='id')
                        tree2 = window['-TREE2-']
                        tree2.Widget.heading("#0", text='id')
                        # ping_process = Process(target=ping_server, args=(BASE_URL_PING,))
                        # ping_process.daemon = True
                        # ping_process.start()
                        threading.Thread(target=the_thread, args=(BASE_URL_PING, window,), daemon=True).start()
                        while True:
                            event, values = window.read()
                            print(event, values)
                            if event == '-THREAD-':
                                update_text = 'Пользователей онлайн: ' + values['-THREAD-'][1]
                                window['online1'].update(update_text)
                                window['online2'].update(update_text)
                            if event == sg.WIN_CLOSED or event == 'Exit':
                                break_flag = True
                                # ping_process.close()
                                break
                            if event == 'update1':
                                try:
                                    res_ping = requests.get(BASE_URL_PING, timeout=3)
                                except Exception:
                                    sg.popup("Сервер не отвечает", title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='gray')
                                    break
                                update_text = 'Пользователей онлайн: ' + res_ping.text
                                window['online1'].update(update_text)
                                window['online2'].update(update_text)
                            if event == 'update2':
                                try:
                                    res_ping = requests.get(BASE_URL_PING, timeout=3)
                                except Exception:
                                    sg.popup("Сервер не отвечает", title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='gray')
                                    break
                                update_text = 'Пользователей онлайн: ' + res_ping.text
                                window['online1'].update(update_text)
                                window['online2'].update(update_text)
                            if event == '-users-':
                                print(values['-users-'])
                                user_id = users_from_db[values['-users-'][0]][2]
                                print(user_id)
                                groups_for_user = get_groups_for_user(user_id)
                                group_for_user_ids = []
                                for group_for_user in groups_for_user:
                                    group_for_user_ids.append(group_for_user[1])
                                # print(group_for_user_ids)
                                all_group_ids = []
                                for group_from_all in groups_from_db:
                                    all_group_ids.append(group_from_all[1])
                                # print(all_group_ids)
                                # window['-groups-'].update(groups_for_user)
                                tree.metadata = []
                                for group_id_for_tree in all_group_ids:
                                    if group_id_for_tree in group_for_user_ids:
                                        # print(group_id_for_tree)
                                        tree.metadata.append(group_id_for_tree)
                                        tree.update(key=group_id_for_tree, icon=check[1])
                                    else:
                                        tree.update(key=group_id_for_tree, icon=check[0])
                            if event == '-TREE-':
                                group_id = values['-TREE-'][0]
                                print(group_id)
                                if group_id in tree.metadata:
                                    tree.metadata.remove(group_id)
                                    tree.update(key=group_id, icon=check[0])
                                else:
                                    tree.metadata.append(group_id)
                                    tree.update(key=group_id, icon=check[1])
                            if event == '-TREE2-':
                                user_id = values['-TREE2-'][0]
                                print(user_id)
                                if user_id in tree2.metadata:
                                    tree2.metadata.remove(user_id)
                                    tree2.update(key=user_id, icon=check[0])
                                else:
                                    tree2.metadata.append(user_id)
                                    tree2.update(key=user_id, icon=check[1])
                            if event == '-groups2-':
                                print(values['-groups2-'])
                                group_id = groups_from_db[values['-groups2-'][0]][1]
                                users_for_group = get_users_for_group(group_id)
                                users_for_group_ids = []
                                for user_for_group in users_for_group:
                                    users_for_group_ids.append(user_for_group[2])
                                all_user_ids = []
                                for user_from_all in users_from_db:
                                    all_user_ids.append(user_from_all[2])
                                # window['-users2-'].update(users_for_group)
                                tree2.metadata = []
                                for user_id_for_tree in all_user_ids:
                                    if user_id_for_tree in users_for_group_ids:
                                        # print(user_id_for_tree)
                                        tree2.metadata.append(user_id_for_tree)
                                        tree2.update(key=user_id_for_tree, icon=check[1])
                                    else:
                                        tree2.update(key=user_id_for_tree, icon=check[0])
                            if event == "Apply":
                                print("clicked Apply")
                                if values['-users-'] == []:
                                    print(f"Не выбран пользователь")
                                    sg.popup('Не выбран пользователь', title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='gray')
                                else:
                                    add_group = False
                                    del_group = False
                                    print(values['-users-'])
                                    chosen_login = users_from_db[values['-users-'][0]]
                                    print(f"Выбран пользователь {chosen_login[0]}")
                                    # print(tree.metadata)
                                    current_groups = get_groups_for_user(chosen_login[2])
                                    # print(current_groups)
                                    current_groups_ids = []
                                    for cur_gr in current_groups:
                                        current_groups_ids.append(cur_gr[1])
                                    add_dict = {'UserIds': [chosen_login[2]], 'GroupIds': []}
                                    del_dict = {'UserIds': [chosen_login[2]], 'GroupIds': []}
                                    for gr_id in tree.metadata:
                                        if gr_id in current_groups_ids:
                                            print(f"Пользователь уже в группе {get_group_name_by_id(gr_id)}")
                                        else:
                                            print(f"Пользователя нужно добавить в группу {get_group_name_by_id(gr_id)}")
                                            add_dict['GroupIds'] += [gr_id]
                                            add_group = True
                                    if add_group:
                                        res = requests.post(BASE_URL + 'addToGroup', json=add_dict)
                                        print(res.status_code)
                                        if res.status_code == 200:
                                            # window['-groups-'].update(get_groups_for_user(chosen_login[0]))
                                            pass
                                        else:
                                            sg.popup("Добавление не выполнено", title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='gray')
                                    for gr_id in current_groups_ids:
                                        if gr_id in tree.metadata:
                                            print(f'Пользователь уже в группе {get_group_name_by_id(gr_id)}')
                                        else:
                                            print(f"У пользователя нужно удалить группу {get_group_name_by_id(gr_id)}")
                                            del_dict['GroupIds'] += [gr_id]
                                            del_group = True
                                    if del_group:
                                        res = requests.post(BASE_URL + 'removeFromGroup', json=del_dict)
                                        print(res.status_code)
                                        if res.status_code == 200:
                                            # window['-groups-'].update(get_groups_for_user(chosen_login[0]))
                                            pass
                                        else:
                                            sg.popup("Удаление не выполнено", title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='gray')
                                    if add_group or del_group:
                                        add_del_text = 'Изменение групп для ' + chosen_login[0] + ' выполнено'
                                        sg.popup(add_del_text, title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='gray')
                                    else:
                                        sg.popup('Нет изменений', title='Инфо', icon=ICON_BASE_64, no_titlebar=True,
                                                 background_color='gray')
                            if event == "Apply2":
                                print("clicked Apply2")
                                if values['-groups2-'] == []:
                                    print(f"Не выбрана группа")
                                    sg.popup('Не выбрана группа', title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='gray')
                                else:
                                    add_user = False
                                    del_user = False
                                    print(values['-groups2-'])
                                    chosen_group = groups_from_db[values['-groups2-'][0]]
                                    print(f"Выбрана группа {chosen_group[0]}")
                                    # print(tree.metadata)
                                    current_users = get_users_for_group(chosen_group[1])
                                    # print(current_users)
                                    current_users_ids = []
                                    for cur_us in current_users:
                                        current_users_ids.append(cur_us[2])
                                    add_dict = {'UserIds': [], 'GroupIds': [chosen_group[1]]}
                                    del_dict = {'UserIds': [], 'GroupIds': [chosen_group[1]]}
                                    for us_id in tree2.metadata:
                                        if us_id in current_users_ids:
                                            print(f"В группе {chosen_group[1]} уже есть {us_id}")
                                        else:
                                            print(f"Пользователя {us_id} нужно добавить в группу {chosen_group[1]}")
                                            add_dict['UserIds'] += [us_id]
                                            add_user = True
                                    if add_user:
                                        res = requests.post(BASE_URL + 'addToGroup', json=add_dict)
                                        print(res.status_code)
                                        if res.status_code == 200:
                                            # window['-users2-'].update(get_users_for_group(chosen_group[1]))
                                            pass
                                        else:
                                            sg.popup("Добавление не выполнено", title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='gray')
                                    for us_id in current_users_ids:
                                        if us_id in tree2.metadata:
                                            print(f'Пользователь {us_id} уже в группе {chosen_group[1]}')
                                        else:
                                            print(f"В группе {chosen_group[1]} нужно удалить пользователя {us_id}")
                                            del_dict['UserIds'] += [us_id]
                                            del_user = True
                                    if del_user:
                                        res = requests.post(BASE_URL + 'removeFromGroup', json=del_dict)
                                        print(res.status_code)
                                        if res.status_code == 200:
                                            # window['-users2-'].update(get_users_for_group(chosen_group[0]))
                                            pass
                                        else:
                                            sg.popup("Удаление не выполнено", title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='gray')
                                    if add_user or del_user:
                                        add_del_text = 'Изменение пользователей для ' + chosen_group[0] + ' выполнено'
                                        sg.popup(add_del_text, title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='gray')
                                    else:
                                        sg.popup('Нет изменений', title='Инфо', icon=ICON_BASE_64, no_titlebar=True,
                                                 background_color='gray')
                        else:
                            sg.popup('Введите правильный ip!', title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='gray')
                else:
                    sg.popup('Введите правильный ip!', title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='gray')
                if window_main_active:
                    window.close()
                    break
            else:
                sg.popup("Неправильный пароль!!!", title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='gray')
                window_login['password'].update('')
    if not window_main_active:
        window_login.close()


