import json
import subprocess
import threading
from datetime import datetime
from time import sleep
# from psgtray import SystemTray
import requests
# import socket
import os
from pathlib import Path
import sqlite3
# import re
import PySimpleGUI as sg
from io import BytesIO
from PIL import Image, ImageDraw
import ipaddress
import logging
# import netifaces
# from pystray import MenuItem as item, Menu as menu
# import pystray
# import subprocess
# from multiprocessing import Pool
# from multiprocessing import Process, Queue

BASE_URL = 'http://10.1.4.147:5000/api/admin/'
ICON_BASE_64 = b'iVBORw0KGgoAAAANSUhEUgAAAMcAAADJCAYAAACXDya2AAAABmJLR0QA/wD/AP+gvaeTAAARR0lEQVR42u1dCZAU1RluLzzwjHgQQRHY3cGNaLJB1CiCioocO9Oz44EQMIUSj6CEmIgSXMUDNQKuO/16sujiRuKJWh4xokhpKEKhiEQFl+USOQJIIpco1+Z/vUh0WWBm+nX3+7r/v+ovqiy0nPe+r99//4bB4qHU72fERRsjbvUwEmKIkbQeNkzxNOlbpO+Tfky6kPRLw7Q20p/19PfW0Z+rd/7zOaQzSSeTVtPfGUHa10hmOhupiuP4fFlwxMy0JHBfZSTFGALztF2A90obiCSJdpdRZl9k9K9pzpfAooeknjvAMNPdDNMeu/MVqA9YtzovjXyh4uIsviAW/00l0+5Cr8J4AuIaDQixN5Wm2X1GaeZ0vjcW76R3pgWRYjiBrU5zQuxB7U/IDBtqpDJH8WWyKDKdrCICVxXp15ik2E3XE0nGOf4RC0tekrTaEogmEJi2hYQUjXUT6YNGT+sYvmyWLF+KMYcSaMpJN4eUFI11rZG0bzHKy/fny2fZs8hwqCmWRIQUjXWKYVa1YhCwNA7JNtuZoNseUWL8/xUxRYIBwdIgicpjKZLzTsRJ8X3dQWbWaDazOBJFkShrEROiSZ1oXJ85iEESyWhUJkYAWM4k2Gtu5DVjYPUhDJZIEcMuoMtfxeDPQpPWJDaxIuVjWLUM/JwIIhg4YRf5BWTnO0+1BjGAwixOPwQDPU/dbMTTZzKIQulnVBbvLOlmoOevs9j/COWrYb/E4FaiAxlMoXLC0x2c5BYDW4Xvschp8mIJy6shLAa1yuiVSDKowiA9Ko6kC93AoFaq/2RghePVGMxg9uT1+CmDC58c0xnMnuhjDC5oR7yykB1xz+qu/kt99YcxyHCTfvcziD2NXPVlkCGKUyoiljKAPe4eZAGUsvQlDF4fGqNS6fYMNjxHfCKD1wdNiHsZbHi5jU0MXl90pdG1/EAGHUyUSlzHoPX19ejFoMMhx3sMWl/1eQYdgpSmW/OInQB6PXgGL4AkrdsYrFzKztIkOcQHDNQg/A77TQafzhLPtGOgBqbbKOdxIoNQ21fDHskgDTRqNYRBqG3ijxa0MEi5z4OlcfjWPoPBqUOfBw3MY9Eut/EAg1OLSt0RDEbtTCqxgIGphc5jMGpFDOtsBqVGysPftDKpxjEotdIHGZQ6SENT0zIGpFa6lCcj6iBlomsIwESjg6xn6M8/kdaQrglBj3kXBmfgiT8aj49edtF43XEqfTiRZQY4QdIMziBFjqXEXkLzhdHn8SP2kLfpDt8ExWNDA3XELwQfjHZniIlPr6J1AYOUTao8wUMDrveeu6kCz5ZXMkiDi1KtAM4k1+77ZbQvY9OKJY/EX7pb6Kd2yFXHpljLUSuWHMlB0RDoLLJVkuXvrOaZuiwRMqnEEsOo3y/LoEMvNq1YcohSURQEO0o1Juvf2qPiYPp3voL+vWXW+Qxa/0yqxyIFFlM8BV7GXsGg9c+kWg4Mln/nbGaYIgFvWnGtlQ8iv7rYQLFz/s0Dqw+hf289dnQucx6D13OTip5obH/j0jyrAZ4F/92PMni9N6mAy9NpG1LquWb5VQOIK8BfzBVsWnkapaKnGRsgNXn/drliDH9y/C8YxJ6RA77jL+EySvcieFXAOAaxJ0JJM1N8DgyOTUb/muYuPw7XsGnF0kSUKn0uODBecH0GsvdDTjRn04qlUVb8EexojdVPyTkkxavghYhjGczqTaolwKD41oiPPVoNOawB4C/HkqzryliyAYT9c/DyiTeUnYUkmSQb9HlkfsagVpb4E/eBm1TXK06EvgFuWo1iUKsjxzxgMGxXvrfCtAaBk+MTBrUKSdmngdvY7yo/k96ZFvTf3Qp9LimriMHtPjpzJ7i/catHCdG3wT8av2dwuycH9o6/VNWpHp3LDbzoJtK+RuUpdIg7gAHwvmdn06fqBGcPH+7Z0L1WtWKQ5286DAU3qe7wOFDxLngZ+w0M8vzJ8R725WdiHp/PEHDTajKDPL+LPx7abEiIT72P5ImTwM3OLbsN0WbJxuGkxBknurIxraZzzVnknHH0LLBPJRKmGAZOjkkM9pzMhcxR4PVDi30rritNtwY3rTY5XY4sWZtU/cBH7z/i7ytLIWPsBT6lDPrsyTGJx9DklBC8Hbx9dgKDPiuTasyh5G9sjNTQNvcfk7bgId21RtfyAxn8+zYREuAOpgjmtbVng78eFzL4902OGuw5uOlLAorujeBVBWEWuawlKf4TyaFtrs1RKgHHJscybp/du2N5KXgt1ZPBvrrURAR9fulOTII9m1Q2uL8RD/j8ysE/LvczCZoS/G1NwSezSjOng5OjlonQlODPwX1ek9d3Hvbr63ElMyY5wIe2mVZfTciBPanFtIczGXa/1IXQpdeqhra5PkcqeMR+gWcyGcJ1oa9r9qFZAN0+K4spWXaFIEeBm1SD9DJR7YfA22dvZlKEIz6/zela1CpflOkM/hJPYVI4F2kXgNcETdXvUOF3mWxzBtfxq0HRCWxyDNH0XMeCJ1QHMDlkdALZeUxlTua8kSd+x8sRJwYN9cJu8dQ37NhQcbAc+Gy/dr0mDjvxBz53SXbg6e3PVXKtGi45pvKkcC9f5nQ38Gz5E9EkBv4Y/Y+1P2PZrmuKVcBn/KXvLcd6fNXAF7AkrLtBAh7YbQB+D6vQ5NJeh760ePpMDNPV7g4+tuehaBEDf5/2YpizllM9TLEG+Kzropb4u5KHtvl63k9w4APH33gGfMLIuVDnnbQv5xVpCNKj4mAK4a4DvqiVToINSeCnuohp0SBH3OoB/hVLgwZAkOeBqV9Xran9mwHP2l6MmXClYc3Y1Qi/Cjcx4CeM0NA2aaKwOcuFiMpFOrLYJlU1eG7paehCxFDv8TDFg+DtsH3ATdoybNPK7h1eciTEZ8CXs8FZj4As8suLvd6hKpzESFYWg3f8PRuS1/sF4HtYBRdGz44c4k5wclwVjnuwrwavtTonjP4GcjvsNxTtOTIU95BKH+44t7gfqQfCRQz0ZfJJ8WrIXvGXgT9Uc0PmiFs3cQJKq1e8P7ZpVVkYpst4C3qGUqriuFCRQ871xd7zPowvQo+s+DshzTkhN5u9GxL71uoH3uT/m3CG1slU5ImIHFfnid9N+YGVx0IPuICfiCiL3UyxHrhcZIYRZjHFZGByTEJPOPUGb4f9Q8jJMRj4w7XRGFh9CPDhW+O5d1ljgZ8dZvXEPPiG3o2VwLmNfxlREOipk9Q4Byll1vngvRvlkSCH3KKEe0crnF0kgFlx7O2wCfuMSJBD9mbLHm3Y4XriLERnD3g7rLXI6+OpN4wD6mKxc2pjseHzi4omzo/FZtCf80gXks4hnUpq1RYWDpoXi7Xx+K6mARci3ouW+OvIIyibls+KiooI9GNJvyStz0FnE1Fu+rS4+HAP/I6hPNDbvxDuSO4Z+KEsaNeudW1RUQ2BfFuOpGisq+sKC4d+UFKibtAD+hKhVLo9kkn1ITA5lqvuNiOTaTCBep1LUuz2ktAr1FFh2H0GsBl8KwgxKk/B7t2gbUiK5ItWrQ6l1+Iviknxfd1ExOuryBS+jTf6em9S3YI9B9e+SMUxrCgpOYzA+7aHxPhOd9QVFbn/cqaqTgX+qG1zasX0fzmoxBt5k5Ac2e9SyGluRi/GOz4QY5eSH3KjAnN4FnCtVT/NcxvglZ6KdtDNLyyc4CcxdupWCg1f6tLvuAPYHH5Od0d8YNSHhhFIrw2AGN/pmrkdOrR0YRIXQM8V07oQ0bRfivLhUh7iJA+iUjkpmXPuZsrKmjLcEPxlmpYh0DRA6Gl6tFDHpZBZ82SQxNjlf8Ril7h4/e8C/sBZumbF4+DtsFe6MqcKCjoQMLfrQA7SmfnfI/RkyuV6FiImxIQoD22jr/WfNSFGgxYUdHHxeszFLUS0SjQzqZxl8MAbS61XFOQ0NuhEDpl8dOE7jgL+0N2jmSOe7gbeDnutS0f8Sq1ejQZdt7hNm/wCDHLHOu59fqSbSTUuymNedHHEd9PCwotdmFZ1uIWIlO3XKL+xGJgcUxTkNhbqSA7qFbnbRc5jNHCt1RA9iIH9BNc7baJuXo327Y/U8tVo0FdcmMqdgMnxti6Fhsi9GzucXgYXsiAWK9GYHHNdWgSo3ZxbjJ7WMTqYVO8Dk2O6a5MqFuulMTnWufMlgecAyCU9wRIj0xK7d4N6GNyT42qNybGdetXzT4ohb/9NiL8GHaW6Lup7HqhUvL/G5Kif2rWrixJ8yjabYino/X5F+bdmAb4clDyLeDycXo6kxuTY7N6nFI9GvXEtz0JDsQmYHHepOAbq475QV3JQlnylgkrrLsCRyEeDMql6QZtUpZnTVRyDnCmlKzmofXaa6x/YMNZ1Beg9LwmqdyMDTI46VcdADu/+zqADPV+O8YoikhZw0KWjz8xwHLUvgMN8o1Weht/94jm8HGoWfUrbHbeodITPWXEqC4bOimc6qzwOiliN1LS2qq3CquvVoPc902eTiiaQ45JjmeqGGKrKjWlIjlmK77wqqlUQuR7ULOBntsKLI6GQ7oeaFR2qXUcs+7NxP4iD/SFGn8d+DJ0Vl70nHgiBcYBG5FhPvRxHK/2B12cOovNbC9oC/ZpfrwbwHjk1Q9uaEjnIjUC5SBNyjPbk7nFbob8x+jx+hB8h3NeATarxXh4NRYdSGhBj9cK2bY/yqAIbdwFqwjY5Kx7ggkVZ5EfgfD1QcqgaLN2UNKzO/gr0/qu9rqXqA2xSrfdjIt7i4uITCaSrAiLHUz6Y1RNhTWoZkvbwYKpwn1X/SpgptNvJ96w5RcvmdOzY3PuyITJPYDGQOc/LrPgy4AkjKT9TQUSQOIH2W786/lzNyM3dtN7A6+x+8GoA9xSbYrM/0YpGuY+Cgp4+zLP6gFaqHe9z0emzUa+pa2xS3QNcuvyyEZDUnXZaMUWxaj0qD5kgt0f5/qOS4grcsT1WkRdhvNnAlZkDjABFApjA/DDpFkXEWCbNtsB+UO/MYbBRSwWt0T+U0nRr4Kz4VrdD21TJguLi9jsHwH2TJymWk+P9u0Bei90tiRdBw/n/UJ34uxHY35hsaCb01W9B5SY3k7n1NwL8xn0QYinp40Sq3pRHOUCbH5EQ18BOuExVHKcyv/EGsL9xg6GxyGYpGgzXbn6HDt1lht2p0YrFTCLQeZJE2v6PywCHDHRg4mKgmkPoX9Mc+BC2O4WSLF455q+C+h2TVNmWCWCTahoj2FO/A3QHJG0gU1ItITes4pJjGCPYQ4mPPZrO+Nto1tk1TJ5YCRzCbcsI9vz1+DsoPmy3jvjZwEMUZjNyfYlaoU69XOGuXdoU9wGTYyQj15eEYAsnl4TZFdrJTTQCeCe1+Akj1zfTagpo++yo/H5wKnMysCM+nxHrJzlgk8Rz8n01bgZ+NR5gxPqZEKw6wck8R2Z/IG4UgnZRi7MYsb475u9FY38gdlZc+dA2lqzIMSQa+wORe8UDGzsfcUmJk0Art3PcH4g8Qb1MdGWkBha1mh7+/YGm+ByUHGu8GtrGkhVuhoV7+EbCPgM4hFvFCA1Q4qINqGmV5f5A0x4OnBW/nBEa+OuBuXo7q/2Bssybh7ax5CtJcXs4Azmp8T/CrZOhSXwsGpCDKqFDuT/QtPri+ht2GSNTG9Pqo/DtDzTFU6Dk+NpJXLLoQo4/hmt/YMPetzWgr8ZLjEidEoI0OC1U+wPL0ucC7174JSNSM0mIT8OzPzAh7gUlxxYnkMCiGTmsu8OzPxB13GfCfpORqGXUqmM49gciL8FM2L9mJGrrmM/D3x+I2yS/3TAzLRmFupLDuh9/f6CM9vBQYBbVErdKsPcHyoIrWXqBWUv1W0ag9qbVAtz9gQm7Ow9tY/EuakWrxmD3BybEOFByzGLkIUStMp1x9wfKMTahSvWz6CXOolXE5rm6/wGZ2bRwzwfZsgAAAABJRU5ErkJggg=='
version = 'v0.91'

def icon(check):
    box = (16, 16)
    background = (255, 255, 255, 0)
    rectangle = (0, 0, 15, 15)
    line = ((4, 8), (7, 11), (11, 4))
    im = Image.new('RGBA', box, background)
    draw = ImageDraw.Draw(im, 'RGBA')
    draw.rectangle(rectangle, outline='black', width=2)
    if check == 1:
        draw.line(line, fill='black', width=2, joint='curve')
    elif check == 2:
        draw.line(line, fill='grey', width=2, joint='curve')
    with BytesIO() as output:
        im.save(output, format="PNG")
        png = output.getvalue()
    return png

check = [icon(0), icon(1), icon(2)]


def init_db():
    # create_db()
    drop_db('all')
    users_from_server = get_users_from_server()
    add_users(users_from_server)
    add_groups(get_groups_from_server())
    add_user_in_groups(users_from_server)

def create_db():
    with open ('adm.db', 'w') as bd_file:
        print('Файл БД создан')
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    with open(Path(Path.cwd(), 'config', 'pashi_db.db.sql'), 'r') as c_sql:
        sql_to_create = c_sql.read()
        # print(sql_to_create)
    cur.executescript(sql_to_create)
    con.commit()
    con.close()


def get_users_from_server():
    # print(f'Запрашиваю пользователей..')
    try:
        res = requests.get(BASE_URL + 'users', headers=HEADER_dict)
    except Exception as e:
        print(e)
        res = []
    # print(res)
    if res != []:
        users = json.loads(res.text)
    return users


def get_groups_from_server():
    # print(f'Запрашиваю группы..')
    res = requests.get(BASE_URL + 'groups', headers=HEADER_dict)
    # print(res)
    groups = json.loads(res.text)
    return groups


def add_users(users_list):
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    for user in users_list:
        db_insert_user = "insert or replace into Users(id, login, Display_name) Values ('" + user['id'] + "', '" + user['login'] + "', '" + user['displayName'] + "')"
        cur.execute(db_insert_user)
    con.commit()
    con.close()

def add_groups(groups_list):
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    for group in groups_list:
        if group['description'] is None:
            db_insert_group = "insert or replace into Groups(id, Name, description) Values ('" + group['id'] + \
                          "', '" + group['name'] + "', '')"
        else:
            db_insert_group = "insert or replace into Groups(id, Name, description) Values ('" + group['id'] + \
                              "', '" + group['name'] + "', '" + group['description'] + "')"
        cur.execute(db_insert_group)
    con.commit()
    con.close()


def add_user_in_groups(users_list):
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    for user in users_list:
        for group_id in user['userGroupIds']:
            db_insert_user_in_groups = "insert or replace into Users_in_Groups(user_id, group_id) Values ('" + user['id'] + "', '" + group_id + "')"
            cur.execute(db_insert_user_in_groups)
    con.commit()
    con.close()

def add_groups_to_user_after_apply(groups_for_user_dict):
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    for user_id in groups_for_user_dict['UserIds']:
        for group_id in groups_for_user_dict['GroupIds']:
            db_insert_group_for_user = "insert or replace into Users_in_Groups(user_id, group_id) Values ('" + user_id + "', '" + group_id + "')"
            cur.execute(db_insert_group_for_user)
    con.commit()
    con.close()

def add_users_to_group_after_apply(users_for_group_dict):
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    for group_id in users_for_group_dict['GroupIds']:
        for user_id in users_for_group_dict['UserIds']:
            db_insert_user_for_group = "insert or replace into Users_in_Groups(user_id, group_id) Values ('" + user_id + "', '" + group_id + "')"
            cur.execute(db_insert_user_for_group)
    con.commit()
    con.close()

def del_groups_to_user_after_apply(groups_for_user_dict):
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    for user_id in groups_for_user_dict['UserIds']:
        for group_id in groups_for_user_dict['GroupIds']:
            db_delete_group_for_user = "delete from Users_in_Groups where user_id = '" + user_id + "' and  group_id = '" +  group_id + "'"
            cur.execute(db_delete_group_for_user)
    con.commit()
    con.close()

def del_users_in_groups_after_delete_group(del_group_id):
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    db_delete_group_for_user = "delete from Users_in_Groups where group_id = '" + del_group_id + "'"
    cur.execute(db_delete_group_for_user)
    con.commit()
    con.close()

def del_users_in_groups_after_delete_user(del_user_id):
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    db_delete_group_for_user = "delete from Users_in_Groups where user_id = '" + del_user_id + "'"
    cur.execute(db_delete_group_for_user)
    con.commit()
    con.close()

def del_users_to_groups_after_apply(users_for_group_dict):
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    for group_id in users_for_group_dict['GroupIds']:
        for user_id in users_for_group_dict['UserIds']:
            db_delete_user_for_group = "delete from Users_in_Groups where user_id = '" + user_id + "' and  group_id = '" + group_id + "'"
            cur.execute(db_delete_user_for_group)
    con.commit()
    con.close()

def drop_db(table):
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    if table == 'all':
        db_delete_groups = "delete from Groups"
        db_delete_users = "delete from Users"
        db_delete_users_in_groups = "delete from Users_in_groups"
        db_delete_users_in_groups_seq = "delete from sqlite_sequence where name='Users_in_Groups'"
        cur.execute(db_delete_users)
        cur.execute(db_delete_groups)
        cur.execute(db_delete_users_in_groups)
        cur.execute(db_delete_users_in_groups_seq)
    elif table == 'users':
        db_delete_users = "delete from Users"
        cur.execute(db_delete_users)
    elif table == 'groups':
        db_delete_groups = "delete from Groups"
        cur.execute(db_delete_groups)
    elif table == 'user_in_groups':
        db_delete_users_in_groups = "delete from Users_in_groups"
        cur.execute(db_delete_users_in_groups)
        db_delete_users_in_groups_seq = "delete from sqlite_sequence where name='Users_in_Groups'"
        cur.execute(db_delete_users_in_groups_seq)
    con.commit()
    con.close()

def get_users_from_db():
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    cur.execute('select * from users')
    users = cur.fetchall()
    # print('Пользователи:')
    users_for_table = list()
    for user in users:
        # print(user)
        user_for_table = {}
        user_for_table['login'] = user[1]
        user_for_table['name'] = user[3]
        user_for_table['id'] = user[0]
        # print(user_for_table)
        users_for_table.append(user_for_table)
    # print('---')
    con.close()
    return users_for_table

def get_groups_from_db():
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    cur.execute('select * from groups')
    groups = cur.fetchall()
    # print('Группы:')
    groups_for_table = list()
    for group in groups:
        # print(group)
        group_for_table = {}
        group_for_table['name'] = group[1]
        group_for_table['id'] = group[0]
        group_for_table['desc'] = group[2]
        # print(group_for_table)
        groups_for_table.append(group_for_table)
    # print('---')
    con.close()
    return groups_for_table

# def get_users_for_group_from_server(id):
#     print(f'Запрашиваю пользователей для группы', id)
#     res = requests.get(BASE_URL + 'groups', headers=HEADER_dict)
#     # print(res)
#     # print(res.text)
#     groups = json.loads(res.text)
#     res_users = list()
#     for group in groups:
#         if group['id'] == id:
#             users_ids = group['userIds']
#             print(group['userIds'])
#             for user_id in users_ids:
#                 user_name = get_user_name_by_id(user_id)
#                 user_login = get_user_login_by_id(user_id)
#                 # print(user_name)
#                 # print(user_login)
#                 res_user = [user_login, user_name, user_id]
#                 if user_name:
#                     res_users.append(res_user)
#     res_users.sort(key=lambda i: i[0])
#     return res_users

def get_users_for_group_from_db(id):
    # print(f'Запрашиваю пользователей для группы', id)
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    db_query_users_for_group = "Select ug.user_id, u.login, u.display_name FROM Users_in_Groups ug " \
                               "LEFT JOIN Users u on ug.user_id = u.id " \
                               "LEFT JOIN Groups g on ug.group_id = g.id WHERE g.id = '" + id + "'"
    # print(db_query_users_for_group)
    cur.execute(db_query_users_for_group)
    users = cur.fetchall()
    # print('Пользователи:')
    users_for_table = list()
    for user in users:
        user_for_table = {}
        user_for_table['id'] = user[0]
        user_for_table['login'] = user[2]
        user_for_table['name'] = user[1]
        # print(user_for_table)
        users_for_table.append(user_for_table)
    # print('---')
    con.close()
    return users_for_table

def get_groups_for_user_from_db(id):
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    db_query_groups_for_user = "Select ug.group_id, g.name, g.description FROM Users_in_Groups ug " \
                               "LEFT JOIN Users u on ug.user_id = u.id " \
                               "LEFT JOIN Groups g on ug.group_id = g.id WHERE u.id = '" + id + "'"
    # print(db_query_groups_for_user)
    cur.execute(db_query_groups_for_user)
    groups = cur.fetchall()
    # print('Группы:')
    groups_for_table = list()
    for group in groups:
        group_for_table = {}
        group_for_table['id'] = group[0]
        group_for_table['name'] = group[1]
        group_for_table['desc'] = group[2]
        # print(group_for_table)
        groups_for_table.append(group_for_table)
    # print('---')
    con.close()
    return groups_for_table

def get_group_name_by_id_from_db(id):
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    db_query_group_name_by_id = "Select name from Groups where id = '" + id + "'"
    # print(db_query_group_name_by_id)
    cur.execute(db_query_group_name_by_id)
    group_name = cur.fetchone()[0]
    # print(group_name)
    con.close()
    return group_name

def get_user_name_by_id_from_db(id):
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    db_query_user_name_by_id = "Select Display_name from Users where id = '" + id + "'"
    # print(db_query_user_name_by_id)
    cur.execute(db_query_user_name_by_id)
    user_name = cur.fetchone()[0]
    # print(user_name)
    con.close()
    return user_name

def make_main_window(ip):
    if server_status['run']:
        users_online_text = 'Данные загружаются...'
    else:
        users_online_text = 'Сервер не запущен...'
    user_list = list()
    group_list = list()
    label_text = 'Панель администратора ОМЕГА К100 ' + ip + ' ' + version
    if users_from_db != [[]] and groups_from_db != [[]]:
        for user_from_db in users_from_db:
            user_list.append([user_from_db['id'], user_from_db['login'], user_from_db['name']])
        for group_from_db in groups_from_db:
            group_list.append([group_from_db['id'], group_from_db['name'], group_from_db['desc']])
    tab1_layout = [
                    [sg.Button('Добавить', key='-AddUser-', pad=(((30, 10), (20, 5)))),
                     sg.Button('Удалить', key='-DelUser-', pad=(10, (20, 5))),
                     sg.Button('Клонировать', key='-CloneUser-', pad=(10, (20, 5)))],
                    [sg.Text('Фильтр: '), sg.Input(size=(20,1), enable_events=True, key='-filterUser-')],
                    [
                     sg.Frame('Пользователи',
                        [
                            [sg.Table(user_list, headings=('id', 'Логин', 'Имя'), justification="left",
                            num_rows="40", key='-users-', expand_y=True, expand_x=True,
                            enable_click_events=True,
                            enable_events=True,
                            # bind_return_key=True,
                            # background_color='green',
                            right_click_selects=True,
                            visible_column_map=[0, 1, 1],
                            right_click_menu=[1, 'Изменить пользователя'],
                            select_mode='browse',
                            auto_size_columns=False, col_widths=(0, 10, 30))],],
                            expand_x=True, size=(480, 650)),
                    sg.Frame('Группы',[[sg.Tree(data=treedata, headings=('Имя','Описание'), col0_width=4, col_widths=(20, 30),
                            num_rows=10, key='-TREE-', row_height=20, metadata=[], auto_size_columns=False,
                            show_expanded=False, enable_events=True, justification='left', expand_y=True,
                            select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                            ),]], expand_y=True, expand_x=True),

                     ],
                   [sg.Push(),
                    sg.Button('Применить', key='Apply', disabled=True, disabled_button_color='gray', pad=((0, 10), (5, 10)))],
                   ]
    tab2_layout = [
                    [sg.Button('Добавить', key='-AddGroup-', pad=((30, 10), (20, 5))),
                    sg.Button('Удалить', key='-DelGroup-', pad=((10, (20, 5))))],
                    [sg.Text('Фильтр: '), sg.Input(size=(20, 1), enable_events=True, key='-filterGroup-')],
                    [sg.Frame('Группы',
                        [
                            [sg.Table(group_list, headings=('id', 'Имя', 'Описание'), justification="left",
                            num_rows="40", enable_events=True,
                            enable_click_events=True,
                            right_click_selects=True,
                            right_click_menu=[1, 'Изменить группу'],
                            select_mode='browse',
                            visible_column_map=[0, 1, 1],
                            key='-groups2-', expand_y=True, expand_x=True,
                            auto_size_columns=False, col_widths=(0, 10, 30))],],
                             expand_x=True, size=(480, 650)),
                    sg.Frame('Пользователи', [[sg.Tree(data=treedata2, headings=('Логин', 'Имя'), col0_width=4, col_widths=(20, 30),
                            num_rows=10, key='-TREE2-', row_height=20, metadata=[], auto_size_columns=False,
                            show_expanded=False, enable_events=True, justification='left', expand_y="True",
                            select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                            ),]], expand_y=True, expand_x=True),
                    ],
                   [sg.Push(),
                    sg.Button('Применить', key='Apply2', disabled=True, disabled_button_color='gray', pad=((0, 10), (5, 10)))],
                   ]
    tab3_layout = [
        [sg.Text('Фильтр: '), sg.Input(size=(20, 1),
                                       enable_events=True,
                                       key='-filterJournal-')],
        [sg.Frame('Логи',
                 [[sg.Multiline(key='journal', write_only=True, disabled=True, expand_x=True, expand_y=True, autoscroll=True, auto_refresh=True)]], expand_x=True, expand_y=True
                 ),
         sg.Frame('Типы',
                  [
                      [sg.Checkbox('Info', enable_events=True, key='info')],
                      [sg.Checkbox('Warning', enable_events=True, key='warning')],
                      [sg.Checkbox('Error', enable_events=True, key='error')],
                      [sg.Checkbox('Critical', enable_events=True, key='critical')],
         ], vertical_alignment='top')
         ],
        [sg.T('Количество записей:'), sg.Multiline(key='countLogs', no_scrollbar=True,
                      write_only=True, disabled=True, auto_refresh=True, background_color='lightgray', size=10)],
    ]
    layout = [[sg.Menu([
            ['Помощь', 'О программе'], ], key='-Menu-')],
              [sg.Frame('Сервер',[[sg.Push(), sg.Button('Старт', key='-Start-',
                        disabled_button_color='gray', pad=((0,20),0)),
               sg.Button('Стоп', key='-Stop-',
                         disabled_button_color='gray'), sg.Push()]], size=(186,60),)],
              [sg.TabGroup(
        [[sg.Tab('Пользователи', tab1_layout, key="Tab1"),
          sg.Tab('Группы', tab2_layout, key="Tab2"),
          sg.Tab('Журнал', tab3_layout, key="Tab3"),
          ]], key="Tabs", size=(1000, 790), enable_events=True)],
              [sg.StatusBar(users_online_text, key='-StatusBar-', size=(100, 1))]]
    return sg.Window(label_text, layout, icon=ICON_BASE_64,  use_ttk_buttons=True,
                     enable_close_attempted_event=True,
                     relative_location=(0, -50),
                     finalize=True)

def make_login_window():
    ips = os.popen("hostname -I").read()
    if ips:
        ips = ips.split(" ")
        # print(ips)
        try:
            ip = ipaddress.ip_address(ips[0]).exploded
        except ValueError:
            print('Неверный ip')
            ip = ''
    else:
        ip = ''
    layout_login = [[sg.Push(background_color='white'), sg.Text("Адрес сервера", background_color='white'), sg.Input(default_text=ip, key="ip")],
                    [sg.Push(background_color='white'), sg.Text("Пароль", background_color='white'), sg.Input(focus=True, key="password", password_char='*')],
                    [sg.Push(background_color='white'), sg.Ok(key="OK button"), sg.Push(background_color='white')]]
    return sg.Window('Вход на сервер', layout_login, icon=ICON_BASE_64, background_color='white', finalize=True)

def make_add_user_window():
    layout_add_user = [
                        [sg.Push(), sg.Text('Логин'), sg.Input(key='UserLogin')],
                        [sg.Push(), sg.Text('Имя'), sg.Input(key='UserName')],
                        [sg.Push(), sg.Text('Пароль'), sg.Input(key='userPassword', password_char='*')],
                        [sg.Push(), sg.Button('Показать', key='showPassword')],
                        [sg.Push(), sg.Ok(button_text='Создать', key='addUserButton')]
                       ]
    return  sg.Window('Добавить пользователя', layout_add_user, icon=ICON_BASE_64, use_ttk_buttons=True,
                      finalize=True, modal=True)

def make_modify_user_window(user: dict):
    layout_modify_user = [
        [sg.Push(), sg.Text('Логин'), sg.Input(disabled=True, default_text=user['login'], key='UserModifyLogin')],
        [sg.Push(), sg.Text('Имя'), sg.Input(default_text=user['name'], key='UserModifyName')],
        [sg.Push(), sg.Text('Пароль'), sg.Input(default_text='', key='userModifyPassword', password_char='*')],
        [sg.Push(), sg.Button('Показать', key='showModifyPassword')],
        [sg.Push(), sg.Ok(button_text='Изменить', key='modifyUserButton')]
    ]
    return sg.Window('Изменить пользователя', layout_modify_user, icon=ICON_BASE_64, use_ttk_buttons=True,
                     finalize=True, modal=True)

def make_modify_group_window(group: dict):
    layout_modify_group = [
        [sg.Push(), sg.Text('Имя Группы'), sg.Input(size=(40, 1), default_text=group['name'], key='GroupModifyName')],
        [sg.Push(), sg.Text('Описание Группы'),
         sg.Multiline(enter_submits=True, no_scrollbar=True, size=(40, 3), default_text=group['desc'], key='GroupModifyDesc')],
        [sg.Push(), sg.Ok(button_text='Изменить', key='modifyGroupButton')]
    ]
    return sg.Window('Изменить группу', layout_modify_group, icon=ICON_BASE_64, use_ttk_buttons=True,
                     finalize=True, modal=True)

def make_del_user_window(user):
    delete_text = 'Вы уверены, что хотите удалить пользователя ' + user + '?'
    layout_del_user = [
        [sg.Text(delete_text)],
        [sg.Button('Да', key="okDel"), sg.Button('Нет', key='noDel') ]
    ]
    return sg.Window('Удалить пользователя', layout_del_user, icon=ICON_BASE_64, use_ttk_buttons=True,
                     finalize=True, modal=True)
def make_clone_user_window(user):
    clone_text = 'Клонируем пользователя ' + user
    layout_clone_user = [
        [sg.Push(), sg.Text(clone_text), sg.Push()],
        [sg.Push(), sg.Text('Логин'), sg.Input(key='CloneUserLogin')],
        [sg.Push(), sg.Text('Имя'), sg.Input(key='CloneUserName')],
        [sg.Push(), sg.Text('Пароль'), sg.Input(key='CloneUserPassword', password_char='*')],
        [sg.Push(), sg.Button('Показать', key='showPasswordCloneUser')],
        [sg.Push(), sg.Ok(button_text='Клонировать', key='cloneUserButton')]
    ]
    return sg.Window('Клонировать пользователя', layout_clone_user, icon=ICON_BASE_64, use_ttk_buttons=True,
                     finalize=True, modal=True)

def make_add_group_window():
    layout_add_group = [
        [sg.Push(), sg.Text('Имя Группы'), sg.Input(size=(40, 1), key='GroupName')],
        [sg.Push(), sg.Text('Описание Группы'), sg.Multiline(enter_submits=True, no_scrollbar=True, size=(40, 3), key='description')],
        [sg.Push(), sg.Ok(button_text='Создать', key='addGroupButton')]
    ]
    return sg.Window('Добавить группу', layout_add_group, icon=ICON_BASE_64, use_ttk_buttons=True,
                     finalize=True, modal=True)

def make_del_group_window(group):
    delete_text = 'Вы уверены, что хотите удалить группу ' + group + '?'
    layout_del_group = [
        [sg.Text(delete_text)],
        [sg.Button('Да', key="okDelGroup"), sg.Button('Нет', key='noDelGroup')]
    ]
    return sg.Window('Удалить пользователя', layout_del_group, icon=ICON_BASE_64, use_ttk_buttons=True,
                     finalize=True, modal=True)

def make_exit_window():
    exit_text = 'Вы уверены, что хотите выйти???'
    layout_exit = [
        [sg.Text(exit_text)],
        [sg.Button('Да', key="okExit"), sg.Button('Нет', key='noExit')]
    ]
    return sg.Window('Выход', layout_exit, icon=ICON_BASE_64, use_ttk_buttons=True,
                     finalize=True, modal=True)

def the_thread(ip, window):
    sleep(5)
    num = 0
    # print('Запускаем поток')
    while True:
        res_ping = ''
        try:
            res_ping = requests.get(ip, timeout=3)
        except Exception as e:
            print(f'Сервер не доступен {e}')
        if res_ping == '':
            if server_status['run']:
                logging.info(f'[{num}] Сервер НЕ доступен ')
            # server_status['run'] = False
            # logging.error(f'[{num}] Сервер не доступен')
            # print('Сервер не доступен')
            default_json = json.dumps({"onlineUsersCount": -5, "databaseVersion": 0})
            window.write_event_value('-THREAD-', (threading.currentThread().name, default_json))
        else:
            if res_ping.status_code == 200:
                # print(f'[{num}] Пингуем.. {res_ping.text}')
                if not server_status['run']:
                    logging.info(f'[{num}] Сервер доступен ')
                window.write_event_value('-THREAD-', (threading.currentThread().name, res_ping.text))
                # server_status['run'] = True
        num += 1
        with open('admin.log', mode='r', encoding='cp1251') as log_f:
            s = log_f.read()
            s = s.rstrip('\n')
            journal_list = s.split('\n')
            filtered_journal = []
            filtered_journal = filter_journal(journal_list)
            if filter_status_journal:
                filtered_journal = list(filter(lambda x: search_str in x, filtered_journal))
            output_text = "\n".join(filtered_journal)
            window['journal'].update(output_text)
            window['countLogs'].update(len(filtered_journal))
        sleep(3)

def check_server(url_ping):
    status = {'run': False, 'online': '', 'db': ''}
    res_ping = ''
    try:
        res_ping = requests.get(url_ping, timeout=3)
    except Exception as e:
        print(f"Ошибка подключения. {e}")
    if res_ping == '':
        print('Сервер не отвечает')
        logging.info(f'Сервер НЕ доступен при запуске приложения')
    else:
        if res_ping.status_code == 200:
            # print(f'Запрос на {url_ping} прошёл успешно')
            status['run'] = True
            logging.info(f'Сервер доступен при запуске приложения')
            res_dict = json.loads(res_ping.text)
            # print(res_dict)
            # update_text = 'Пользователей онлайн: ' + str(res_dict['onlineUsersCount']) \
            #               + ', Версия БД: ' + str(res_dict['databaseVersion'])
            status['online'] = res_dict['onlineUsersCount']
            status['db'] = res_dict['databaseVersion']
            # print(status)
        else:
            print(f'Некорректный ответ {res_ping.status_code} от сервера {url_ping}')
    return status

def get_token(url_auth):
    token = ''
    res_auth = ''
    dict_auth = {'login': 'admin', 'password': 'qwerty'}
    try:
        res_auth = requests.post(url_auth, json=dict_auth)
    except Exception as e:
        print(f"Ошибка подключения. {e}")
    if res_auth == '':
        print('Сервер не отвечает')
    else:
        if res_auth.status_code == 200:
            # print(f'Запрос токена {url_auth} прошёл успешно')
            res_dict = json.loads(res_auth.text)
            # print(res_dict)
            error = res_dict['error']
            if error:
                print(f'Ошибка сервера: {error}')
            else:
                # print(f'Запрос токена без ошибок')
                token = res_dict['token']
                # print(token)
        else:
            print(f'Некорректный ответ {res_auth.status_code} от сервера {url_auth}')
    return token

def filter_journal(journal: list):
    if filter_journal_info:
        if filter_journal_warning:
            if filter_journal_error:
                if filter_journal_crirtical:
                    return list(
                        filter(lambda x: 'INFO' in x or 'CRITICAL' in x or 'ERROR' in x or 'WARNING' in x, journal))
                else:
                    return list(filter(lambda x: 'INFO' in x or 'ERROR' in x or 'WARNING' in x, journal))
            elif filter_journal_crirtical:
                return list(filter(lambda x: 'INFO' in x or 'CRITICAL' in x or 'WARNING' in x, journal))
            return list(filter(lambda x: 'INFO' in x or 'WARNING' in x, journal))
        elif filter_journal_error:
            if filter_journal_crirtical:
                return list(filter(lambda x: 'INFO' in x or 'CRITICAL' in x or 'ERROR' in x, journal))
            else:
                return list(filter(lambda x: 'INFO' in x or 'ERROR' in x, journal))
        elif filter_journal_crirtical:
            return list(filter(lambda x: 'INFO' in x or 'CRITICAL' in x, journal))
        else:
            return list(filter(lambda x: 'INFO' in x, journal))
    elif filter_journal_warning:
        if filter_journal_error:
            if filter_journal_crirtical:
                return list(filter(lambda x: 'CRITICAL' in x or 'ERROR' in x or 'WARNING' in x, journal))
            else:
                return list(filter(lambda x: 'ERROR' in x or 'WARNING' in x, journal))
        elif filter_journal_crirtical:
            return list(filter(lambda x: 'CRITICAL' in x or 'WARNING' in x, journal))
        else:
            return list(filter(lambda x: 'WARNING' in x, journal))
    elif filter_journal_error:
        if filter_journal_crirtical:
            return list(filter(lambda x: 'CRITICAL' in x or 'ERROR' in x, journal))
        else:
            return list(filter(lambda x: 'ERROR' in x, journal))
    elif filter_journal_crirtical:
        return list(filter(lambda x: 'CRITICAL' in x, journal))
    else:
        return journal

def get_icon():
    try:
        icon_logo = Image.open('logo.ico')
    except FileNotFoundError:
        print('Файл не найден')
        logging.error('Файл логотипа не найден!')
    # print(icon_logo.format, icon_logo.size, icon_logo.mode)
    return icon_logo

# def create_menu():
#     menu_tray = (item('Выйти', exit_app), item('Отобразить окно', show_app), item('Скрыть окно', hide_app))
#     return menu_tray

def exit_app(icon, item):
    # print('exit')
    global break_flag
    break_flag = True
    window_exit = make_exit_window()
    while True:
        ev_exit, val_exit = window_exit.Read()
        # print(ev_exit, val_exit)
        if ev_exit == 'okExit':
            logging.info('Панель администратора остановлена')
            logging.info('Стоп лога')
            window_exit.close()
            icon.stop()
            global break_flag2
            break_flag2 = True
            break
        if ev_exit == sg.WIN_CLOSED or ev_exit == 'Exit':
            # print('Закрыл окно выхода')
            break
        if ev_exit == 'noExit':
            # print('Закрыл окно выхода')
            window_exit.close()
            break


def show_app(icon):
    # print('show')
    window.un_hide()
    icon.stop()
    # print('show2')

# def hide_app():
#     print('hide')

if __name__ == '__main__':
    # print(sg.theme_global())
    # print(sg.theme_list())
    # get_icon()
    sg.theme_global('SystemDefaultForReal')
    logging.basicConfig(filename='admin.log', filemode='a', format='%(asctime)s %(levelname)s %(message)s', encoding='cp1251', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)
    logging.info('Старт лога')
    # logging.warning('ворнинг')
    # logging.error('еррор')
    # logging.critical('критическая')
    window_login = make_login_window()
    window_main_active = False
    while True:
        break_flag = False
        break_flag2 = False
        ev_login, val_login = window_login.Read()
        # print(ev_login, val_login)
        if ev_login == sg.WIN_CLOSED or ev_login == 'Exit':
            break
        if ev_login == "OK button" and not window_main_active:
            if val_login['password'] == 'qwerty':
                ip = ''
                while True:
                    if break_flag:
                        break
                    # re_ip = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")
                    # if re_ip.match(val_login['ip']):
                    try:
                        ip = ipaddress.ip_address(val_login['ip']).exploded
                    except ValueError:
                        print('Неверный ip')
                    if ip != '':
                        BASE_URL = 'http://' + val_login['ip'] + ':5000/api/admin/'
                        BASE_URL_PING = 'http://' + val_login['ip'] + ':5000/api/ping'
                        BASE_URL_AUTH = 'http://' + val_login['ip'] + ':5000/api/auth'
                        server_status = check_server(BASE_URL_PING)
                        current_db = server_status['db']
                        if server_status['run']:
                            TOKEN = get_token(BASE_URL_AUTH)
                            HEADER_dict = {}
                            HEADER_dict["Authorization"] = "Bearer " + TOKEN
                            # print(TOKEN)
                            # print(HEADER_dict)
                            create_db()
                            init_db()
                            users_from_db = get_users_from_db()
                            groups_from_db = get_groups_from_db()
                            users_from_db.sort(key=lambda i: i['login'])
                            groups_from_db.sort(key=lambda i: i['name'])
                            treedata = sg.TreeData()
                            treedata2 = sg.TreeData()
                            for group in groups_from_db:
                                treedata.insert('', group['id'], '', values=[group['name'], group['desc']], icon=check[0])
                            for user in users_from_db:
                                treedata2.insert('', user['id'], '', values=[user['login'], user['name']], icon=check[0])
                        else:
                            treedata = sg.TreeData()
                            treedata2 = sg.TreeData()
                            users_from_db = [[]]
                            groups_from_db = [[]]
                        window_main_active = True
                        window_login.Hide()
                        window = make_main_window(ip)
                        # menu = ['', ['Отобразить окно', 'Скрыть окно', 'Выйти']]
                        # tray = SystemTray(menu, single_click_events=False, window=window,
                        #                   icon=ICON_BASE_64)
                        # tray.show_message('ОМЕГА К100', 'Приложение запущено!')
                        # sg.cprint(sg.get_versions())
                        tree = window['-TREE-']
                        tree.Widget.heading("#0", text='id')
                        tree2 = window['-TREE2-']
                        tree2.Widget.heading("#0", text='id')
                        if server_status['run']:
                            bar_text = 'Пользователей онлайн: обновление..' + ', Версия БД: ' + str(server_status['db'])
                            window['-StatusBar-'].update(bar_text, background_color='lightgreen')
                        else:
                            window['-StatusBar-'].update('Сервер не доступен', background_color='red')
                        thread_started = False
                        filter_status = False
                        filter_status_group = False
                        filter_status_journal = False
                        filter_journal_info = False
                        filter_journal_warning = False
                        filter_journal_error = False
                        filter_journal_crirtical = False
                        while True:
                            if break_flag2:
                                break
                            if server_status['run'] == False:
                                window['-Stop-'].update(disabled=True)
                            else:
                                window['-Start-'].update(disabled=True)
                            if not thread_started:
                                threading.Thread(target=the_thread, args=(BASE_URL_PING, window,), daemon=True).start()
                                thread_started = True
                            event, values = window.read()
                            # print(event, type(event), values)
                            if event == '-THREAD-':
                                current_db = server_status['db']
                                dict_online = json.loads(values['-THREAD-'][1])
                                # print(dict_online)
                                if dict_online["onlineUsersCount"] != -5:
                                    # if current_db != dict_online['databaseVersion']:
                                    #     print(f"Версии БД не совпадают! {current_db} и {dict_online['databaseVersion']}")
                                    # else:
                                    #     print(f"Версии БД совпадают! {current_db} и {dict_online['databaseVersion']}")
                                    if not server_status['run']:
                                        update_text = 'Пользователей онлайн: обновление..' + ', Версия БД: ' + str(dict_online["databaseVersion"])
                                        window['-StatusBar-'].update(update_text, background_color='lightgreen')
                                    else:
                                        update_text = 'Пользователей онлайн: ' + str(dict_online["onlineUsersCount"]) \
                                                      + ', Версия БД: ' + str(dict_online["databaseVersion"])
                                        window['-StatusBar-'].update(update_text, background_color='lightgreen')
                                    res_ping = ''
                                    try:
                                        res_ping = requests.get(BASE_URL_PING, timeout=1)
                                    except Exception:
                                        print("Сервер не отвечает")
                                    if res_ping == '':
                                        print('Нет ответа сервера')
                                    else:
                                        if res_ping.status_code == 200:
                                            # print(f'{res_ping.text}')
                                            dict_online_after_start = json.loads(res_ping.text)
                                            # print(dict_online_after_start)
                                            window['-Start-'].update(disabled=True)
                                            window['-Stop-'].update(disabled=False)
                                            if not server_status['run']:
                                                TOKEN = get_token(BASE_URL_AUTH)
                                                HEADER_dict = {}
                                                HEADER_dict["Authorization"] = "Bearer " + TOKEN
                                                # print(TOKEN)
                                                # print(HEADER_dict)
                                                init_db()
                                                users_from_db = get_users_from_db()
                                                groups_from_db = get_groups_from_db()
                                                users_from_db.sort(key=lambda i: i['login'])
                                                groups_from_db.sort(key=lambda i: i['name'])
                                                treedata_update_user = sg.TreeData()
                                                treedata_update_group = sg.TreeData()
                                                user_list = list()
                                                group_list = list()
                                                if users_from_db != [[]] and groups_from_db != [[]]:
                                                    for user_from_db in users_from_db:
                                                        user_list.append([user_from_db['id'], user_from_db['login'],
                                                                          user_from_db['name']])
                                                    for group_from_db in groups_from_db:
                                                        group_list.append([group_from_db['id'], group_from_db['name'],
                                                                           group_from_db['desc']])
                                                for group in groups_from_db:
                                                    treedata_update_group.insert('', group['id'], '',
                                                                                 values=[group['name'], group['desc']],
                                                                                 icon=check[0])
                                                for user in users_from_db:
                                                    treedata_update_user.insert('', user['id'], '',
                                                                                values=[user['login'], user['name']],
                                                                                icon=check[0])
                                                window['-users-'].update(user_list)
                                                window['-TREE2-'].update(treedata_update_user)
                                                window['-groups2-'].update(group_list)
                                                window['-TREE-'].update(treedata_update_group)
                                                window['-AddUser-'].update(disabled=False)
                                                window['-DelUser-'].update(disabled=False)
                                                window['-CloneUser-'].update(disabled=False)
                                                window['-AddGroup-'].update(disabled=False)
                                                window['-DelGroup-'].update(disabled=False)
                                                window['-filterUser-'].update(disabled=False)
                                                server_status['run'] = True
                                            server_status['run'] = True
                                    # server_status['run'] = False
                                else:
                                    window['-StatusBar-'].update('Сервер не доступен', background_color='red')
                                    window['-Start-'].update(disabled=False)
                                    window['-Stop-'].update(disabled=True)
                                    window['-users-'].update([[]])
                                    window['-groups2-'].update([[]])
                                    clear_treedata = sg.TreeData()
                                    window['-TREE-'].update(clear_treedata)
                                    window['-TREE2-'].update(clear_treedata)
                                    window['-AddUser-'].update(disabled=True)
                                    window['-DelUser-'].update(disabled=True)
                                    window['-CloneUser-'].update(disabled=True)
                                    window['-AddGroup-'].update(disabled=True)
                                    window['-DelGroup-'].update(disabled=True)
                                    window['-filterUser-'].update(disabled=True)
                                    server_status['run'] = False
                            if event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT:
                                # break_flag = True
                                # break
                                # window.hide()
                                # print('exit')
                                # global break_flag
                                break_flag = True
                                window_exit = make_exit_window()
                                while True:
                                    ev_exit, val_exit = window_exit.Read()
                                    # print(ev_exit, val_exit)
                                    if ev_exit == 'okExit':
                                        logging.info('Панель администратора остановлена')
                                        logging.info('Стоп лога')
                                        window_exit.close()
                                        # icon.stop()
                                        # global break_flag2
                                        break_flag2 = True
                                        break
                                    if ev_exit == sg.WIN_CLOSED or ev_exit == 'Exit':
                                        print('Закрыл окно выхода')
                                        break
                                    if ev_exit == 'noExit':
                                        print('Закрыл окно выхода')
                                        window_exit.close()
                                        break
                                # icon = pystray.Icon('adm Panel', icon=get_icon(),
                                #                     menu=menu(
                                #                         item('Exit', exit_app),
                                #                         item('Show', show_app, default=True)))
                                                        # item('Скрыть окно', hide_app)
                                                    # ))
                                # sg.popup("Приложение свёрнуто!\nОкно закроется через 10 секунд", title='Инфо', icon=ICON_BASE_64,
                                #          no_titlebar=True, background_color='lightgray', auto_close=True,
                                #          auto_close_duration=10)
                                # icon.run()
                                # icon.notify('Приложение свёрнуто!', '1111')
                                # icon.run_detached()
                                # print(icon.HAS_NOTIFICATION)
                                # window.hide()
                                # tray.show_icon()
                                # tray.show_message('ОМЕГА К100', 'Приложение свёрнуто!')
                            if event == sg.WIN_CLOSED or event == 'Exit':
                                break_flag = True
                                break
                            if type(event) is tuple:
                                # print(f'TUPLE! {event}')
                                if event[0] == '-users-' and event[1] == '+CLICKED+':
                                    if event[2][0] is None:
                                        pass
                                    else:
                                        if filter_status:
                                            user_id = filtered_users_list_of_dict[event[2][0]]['id']
                                        else:
                                            user_id = users_from_db[event[2][0]]['id']
                                        # print(user_id)
                                        window['Apply'].update(disabled=True)
                                        groups_for_user = get_groups_for_user_from_db(user_id)
                                        group_for_user_ids = []
                                        for group_for_user in groups_for_user:
                                            group_for_user_ids.append(group_for_user['id'])
                                        all_group_ids = []
                                        for group_from_all in groups_from_db:
                                            all_group_ids.append(group_from_all['id'])
                                        tree.metadata = []
                                        for group_id_for_tree in all_group_ids:
                                            if group_id_for_tree in group_for_user_ids:
                                                tree.metadata.append(group_id_for_tree)
                                                tree.update(key=group_id_for_tree, icon=check[1])
                                            else:
                                                tree.update(key=group_id_for_tree, icon=check[0])
                                elif event[0] == '-groups2-' and event[1] == '+CLICKED+':
                                    window['Apply2'].update(disabled=True)
                                    # print(values['-groups2-'])
                                    if event[2][0] is None:
                                        pass
                                    else:
                                        if filter_status_group:
                                            group_id = filtered_groups_list_of_dict[event[2][0]]['id']
                                        else:
                                            group_id = groups_from_db[event[2][0]]['id']
                                        # group_id = groups_from_db[event[2][0]]['id']
                                        users_for_group = get_users_for_group_from_db(group_id)
                                        users_for_group_ids = []
                                        for user_for_group in users_for_group:
                                            users_for_group_ids.append(user_for_group['id'])
                                        all_user_ids = []
                                        for user_from_all in users_from_db:
                                            all_user_ids.append(user_from_all['id'])
                                        tree2.metadata = []
                                        for user_id_for_tree in all_user_ids:
                                            if user_id_for_tree in users_for_group_ids:
                                                tree2.metadata.append(user_id_for_tree)
                                                tree2.update(key=user_id_for_tree, icon=check[1])
                                            else:
                                                tree2.update(key=user_id_for_tree, icon=check[0])
                            if event == 'Изменить пользователя':
                                # print('Изменяем пользователя')
                                if filter_status:
                                    user_to_change = filtered_users_list_of_dict[values['-users-'][0]]
                                else:
                                    user_to_change = users_from_db[values['-users-'][0]]
                                # user_to_change = users_from_db[values['-users-'][0]]
                                # print(user_to_change)
                                window_modify_user = make_modify_user_window(user_to_change)
                                window_modify_user.Element('UserModifyLogin').SetFocus()
                                password_clear = False
                                while True:
                                    ev_modify_user, val_modify_user = window_modify_user.Read()
                                    # print(ev_modify_user, val_modify_user)
                                    if ev_modify_user == sg.WIN_CLOSED or ev_modify_user == 'Exit':
                                        # print('Закрыл окно добавления пользователя')
                                        break
                                    if ev_modify_user == 'showModifyPassword':
                                        if password_clear:
                                            window_modify_user['userModifyPassword'].update(password_char='*')
                                            window_modify_user['showModifyPassword'].update('Показать')
                                            password_clear = False
                                        else:
                                            window_modify_user['userModifyPassword'].update(password_char='')
                                            window_modify_user['showModifyPassword'].update('Скрыть')
                                            password_clear = True
                                    if ev_modify_user == 'modifyUserButton':
                                        modify_user_login, modify_user_name, modify_user_password = val_modify_user.values()
                                        modify_user_dict = {}
                                        modify_name = False
                                        modify_password = False
                                        modify_user_dict['id'] = user_to_change['id']
                                        modify_user_dict['login'] = modify_user_login
                                        if modify_user_name != user_to_change['name']:
                                            modify_user_dict['displayName'] = modify_user_name
                                            modify_name = True
                                        if modify_user_password:
                                            modify_user_dict['password'] = modify_user_password
                                            modify_password = True
                                        # print(modify_user_dict)
                                        if modify_name or modify_password:
                                            res_modify_user = requests.post(BASE_URL + 'updateUser', json=modify_user_dict, headers=HEADER_dict)
                                            # sg.cprint(f'Изменяем пользователя - {res_modify_user.status_code}')
                                            if res_modify_user.status_code == 200:
                                                if modify_name:
                                                    logging.info(f'Пользователю {modify_user_login} изменили имя')
                                                if modify_password:
                                                    logging.info(f'Пользователю {modify_user_login} изменили пароль')
                                                users_from_server = get_users_from_server()
                                                add_users(users_from_server)
                                                users_from_db = get_users_from_db()
                                                users_from_db.sort(key=lambda i: i['login'])
                                                user_list = list()
                                                drop_db('user_in_groups')
                                                add_user_in_groups(users_from_server)
                                                treedata_update_user = sg.TreeData()
                                                for user_from_db in users_from_db:
                                                    user_list.append([user_from_db['id'], user_from_db['login'],
                                                                      user_from_db['name']])
                                                    treedata_update_user.insert('', user_from_db['id'], '',
                                                                                values=[user_from_db['login'], user_from_db['name']],
                                                                                icon=check[0])
                                                window['-users-'].update(user_list)
                                                window['-TREE2-'].update(treedata_update_user)
                                                window_modify_user.close()
                                                sg.popup("Пользователь изменён!", title='Инфо', icon=ICON_BASE_64,
                                                         no_titlebar=True, background_color='lightgray')
                                                break
                                            else:
                                                logging.error(f'Ошибка изменения пользователя - {res_modify_user.status_code}')
                                                sg.popup("Пользователь не изменён!", title='Инфо', icon=ICON_BASE_64,
                                                         no_titlebar=True, background_color='lightgray')
                                        else:
                                            sg.popup("Нет никаких изменений!", title='Инфо', icon=ICON_BASE_64,
                                                     no_titlebar=True, background_color='lightgray')
                            if event == 'Изменить группу':
                                # print('Изменяем группу')
                                group_to_change = groups_from_db[values['-groups2-'][0]]
                                # print(group_to_change)
                                window_modify_group = make_modify_group_window(group_to_change)
                                window_modify_group.Element('GroupModifyName').SetFocus()
                                while True:
                                    ev_modify_group, val_modify_group = window_modify_group.Read()
                                    # print(ev_modify_group, val_modify_group)
                                    if ev_modify_group == sg.WIN_CLOSED or ev_modify_group == 'Exit':
                                        # print('Закрыл окно изменения группы')
                                        break
                                    if ev_modify_group == 'modifyGroupButton':
                                        modify_group_name = val_modify_group['GroupModifyName']
                                        modify_group_desc = val_modify_group['GroupModifyDesc']
                                        modify_group_dict = {}
                                        modify_group = False
                                        modify_group_dict['id'] = group_to_change['id']
                                        if modify_group_name != group_to_change['name']:
                                            modify_group_dict['name'] = modify_group_name
                                            modify_group = True
                                        if modify_group_desc != group_to_change['desc']:
                                            modify_group_dict['description'] = modify_group_desc
                                            modify_group = True
                                        if modify_group:
                                            # print(modify_group_dict)
                                            res_modify_group = requests.post(BASE_URL + 'updateGroup', json=modify_group_dict, headers=HEADER_dict)
                                            # print(res_modify_group.status_code)
                                            if res_modify_group.status_code == 200:
                                                logging.info(f'Группу {modify_group_name} изменили')
                                                add_groups(get_groups_from_server())
                                                groups_from_db = get_groups_from_db()
                                                groups_from_db.sort(key=lambda i: i['name'])
                                                treedata_update_group = sg.TreeData()
                                                group_list = list()
                                                for group_from_db in groups_from_db:
                                                    group_list.append([group_from_db['id'], group_from_db['name'],
                                                                       group_from_db['desc']])
                                                    treedata_update_group.insert('', group_from_db['id'], '',
                                                                                 values=[group_from_db['name'], group_from_db['desc']],
                                                                                 icon=check[0])
                                                window['-groups2-'].update(group_list)
                                                window['-TREE-'].update(treedata_update_group)
                                                window_modify_group.close()
                                                sg.popup("Группа изменена!", title='Инфо', icon=ICON_BASE_64,
                                                         no_titlebar=True, background_color='lightgray')
                                                break
                                            else:
                                                logging.error(f'ошибка изменения группы - {res_modify_group.status_code}')
                                                sg.popup("Группа не изменена!", title='Инфо', icon=ICON_BASE_64,
                                                         no_titlebar=True, background_color='lightgray')
                                        else:
                                            sg.popup("Нет изменений", title='Инфо', icon=ICON_BASE_64,
                                                     no_titlebar=True, background_color='lightgray')
                            if event == '-TREE-' and values['-TREE-'] != []:
                                group_id = values['-TREE-'][0]
                                # print(group_id)
                                if group_id in tree.metadata:
                                    tree.metadata.remove(group_id)
                                    tree.update(key=group_id, icon=check[0])
                                else:
                                    tree.metadata.append(group_id)
                                    tree.update(key=group_id, icon=check[1])
                                window['Apply'].update(disabled=False)
                            if event == '-TREE2-' and values['-TREE2-'] != []:
                                user_id = values['-TREE2-'][0]
                                # print(user_id)
                                if user_id in tree2.metadata:
                                    tree2.metadata.remove(user_id)
                                    tree2.update(key=user_id, icon=check[0])
                                else:
                                    tree2.metadata.append(user_id)
                                    tree2.update(key=user_id, icon=check[1])
                                window['Apply2'].update(disabled=False)
                            if event == "Apply":
                                # print("clicked Apply")
                                if values['-users-'] == []:
                                    print(f"Не выбран пользователь")
                                    sg.popup('Не выбран пользователь', title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='lightgray')
                                else:
                                    add_group = False
                                    del_group = False
                                    # print(values['-users-'])
                                    if filter_status:
                                        chosen_login = filtered_users_list_of_dict[values['-users-'][0]]
                                    else:
                                        chosen_login = users_from_db[values['-users-'][0]]
                                    # chosen_login = users_from_db[values['-users-'][0]]
                                    # print(f"Выбран пользователь {chosen_login['name']}")
                                    # print(tree.metadata)
                                    current_groups = get_groups_for_user_from_db(chosen_login['id'])
                                    # print(current_groups)
                                    current_groups_ids = []
                                    for cur_gr in current_groups:
                                        current_groups_ids.append(cur_gr['id'])
                                    add_dict = {'UserIds': [chosen_login['id']], 'GroupIds': []}
                                    del_dict = {'UserIds': [chosen_login['id']], 'GroupIds': []}
                                    for gr_id in tree.metadata:
                                        if gr_id in current_groups_ids:
                                            print(f"Пользователь уже в группе {get_group_name_by_id_from_db(gr_id)}")
                                        else:
                                            print(f"Пользователя нужно добавить в группу {get_group_name_by_id_from_db(gr_id)}")
                                            add_dict['GroupIds'] += [gr_id]
                                            add_group = True
                                    if add_group:
                                        # print(add_dict)
                                        res_add = requests.post(BASE_URL + 'addToGroup', json=add_dict, headers=HEADER_dict)
                                        # print(res_add.status_code)
                                        if res_add.status_code == 200:
                                            logging.info(f'Добавление групп выполнено для {chosen_login["name"]}')
                                            add_groups_to_user_after_apply(add_dict)
                                        else:
                                            logging.error(f'Добавление групп НЕ выполнено для {chosen_login["name"]}')
                                            sg.popup("Добавление не выполнено", title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='lightgray')
                                    for gr_id in current_groups_ids:
                                        if gr_id in tree.metadata:
                                            print(f'Пользователь уже в группе {get_group_name_by_id_from_db(gr_id)}')
                                        else:
                                            print(f"У пользователя нужно удалить группу {get_group_name_by_id_from_db(gr_id)}")
                                            del_dict['GroupIds'] += [gr_id]
                                            del_group = True
                                    if del_group:
                                        res_del = requests.post(BASE_URL + 'removeFromGroup', json=del_dict, headers=HEADER_dict)
                                        # print(res_del.status_code)
                                        if res_del.status_code == 200:
                                            logging.info(f'Удаление групп выполнено для {chosen_login["name"]}')
                                            del_groups_to_user_after_apply(del_dict)
                                        else:
                                            logging.error(f'Удаление групп НЕ выполнено для {chosen_login["name"]}')
                                            sg.popup("Удаление не выполнено", title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='lightgray')
                                    if (add_group or del_group):
                                        add_del_text = 'Изменение групп для ' + chosen_login['name'] + ' выполнено'
                                        # logging.info(f'Добавление групп НЕ выполнено для {chosen_login["name"]}')
                                        sg.popup(add_del_text, title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='lightgray')
                                        window['Apply'].update(disabled=True)
                                    else:
                                        # logging.error(f'')
                                        sg.popup('Нет изменений', title='Инфо', icon=ICON_BASE_64, no_titlebar=True,
                                                 background_color='lightgray')
                            if event == "Apply2":
                                # print("clicked Apply2")
                                if values['-groups2-'] == []:
                                    # print(f"Не выбрана группа")
                                    sg.popup('Не выбрана группа', title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='lightgray')
                                else:
                                    add_user = False
                                    del_user = False
                                    # print(values['-groups2-'])
                                    if filter_status_group:
                                        chosen_group = filtered_groups_list_of_dict[values['-groups2-'][0]]
                                    else:
                                        chosen_group = groups_from_db[values['-groups2-'][0]]
                                    # chosen_group = groups_from_db[values['-groups2-'][0]]
                                    # print(f"Выбрана группа {chosen_group['name']}")
                                    # print(tree.metadata)
                                    current_users = get_users_for_group_from_db(chosen_group['id'])
                                    # print(current_users)
                                    current_users_ids = []
                                    for cur_us in current_users:
                                        current_users_ids.append(cur_us['id'])
                                    add_dict = {'UserIds': [], 'GroupIds': [chosen_group['id']]}
                                    del_dict = {'UserIds': [], 'GroupIds': [chosen_group['id']]}
                                    for us_id in tree2.metadata:
                                        if us_id in current_users_ids:
                                            print(f"В группе {chosen_group['name']} уже есть {get_user_name_by_id_from_db(us_id)}")
                                        else:
                                            print(f"Пользователя {get_user_name_by_id_from_db(us_id)} нужно добавить в группу {chosen_group['name']}")
                                            add_dict['UserIds'] += [us_id]
                                            add_user = True
                                    if add_user:
                                        res_add = requests.post(BASE_URL + 'addToGroup', json=add_dict, headers=HEADER_dict)
                                        # print(res_add.status_code)
                                        if res_add.status_code == 200:
                                            logging.info(f'Добавление пользователей выполнено для {chosen_group["name"]}')
                                            # window['-users2-'].update(get_users_for_group(chosen_group[1]))
                                            add_users_to_group_after_apply(add_dict)
                                        else:
                                            logging.error(
                                                f'Добавление пользователей НЕ выполнено для {chosen_group["name"]} - {res_add.status_code}')
                                            sg.popup("Добавление не выполнено", title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='lightgray')
                                    for us_id in current_users_ids:
                                        if us_id in tree2.metadata:
                                            print(f'Пользователь {get_user_name_by_id_from_db(us_id)} уже в группе {chosen_group["name"]}')
                                        else:
                                            print(f"В группе {chosen_group['name']} нужно удалить пользователя {get_user_name_by_id_from_db(us_id)}")
                                            del_dict['UserIds'] += [us_id]
                                            del_user = True
                                    if del_user:
                                        res_del = requests.post(BASE_URL + 'removeFromGroup', json=del_dict, headers=HEADER_dict)
                                        # print(res_del.status_code)
                                        if res_del.status_code == 200:
                                            logging.info(
                                                f'Удаление пользователей выполнено для {chosen_group["name"]}')
                                            del_users_to_groups_after_apply(del_dict)
                                        else:
                                            logging.error(
                                                f'Удаление пользователей НЕ выполнено для {chosen_group["name"]} - {res_del.status_code}')
                                            sg.popup("Удаление не выполнено", title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='lightgray')
                                    if add_user or del_user:
                                        add_del_text = 'Изменение пользователей для ' + chosen_group['name'] + ' выполнено'
                                        sg.popup(add_del_text, title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='lightgray')
                                        window['Apply2'].update(disabled=True)
                                    else:
                                        sg.popup('Нет изменений', title='Инфо', icon=ICON_BASE_64, no_titlebar=True,
                                                 background_color='lightgray')
                            if event == 'О программе':
                                sg.popup('---------------------Powered by PaShi---------------------',
                                         title='О программе', icon=ICON_BASE_64)
                            if event == '-AddUser-':
                                window_add_user = make_add_user_window()
                                window_add_user.Element('UserLogin').SetFocus()
                                password_clear = False
                                while True:
                                    ev_add_user, val_add_user = window_add_user.Read()
                                    # print(ev_add_user, val_add_user)
                                    if ev_add_user == sg.WIN_CLOSED or ev_add_user == 'Exit':
                                        # print('Закрыл окно добавления пользователя')
                                        break
                                    if ev_add_user == 'showPassword':
                                        if password_clear:
                                            window_add_user['userPassword'].update(password_char='*')
                                            window_add_user['showPassword'].update('Показать')
                                            password_clear = False
                                        else:
                                            window_add_user['userPassword'].update(password_char='')
                                            window_add_user['showPassword'].update('Скрыть')
                                            password_clear = True
                                    if ev_add_user == 'addUserButton':
                                        new_user_login, new_user_name, new_user_password = val_add_user.values()
                                        add_user_dict = {}
                                        add_user_dict['login'] = new_user_login
                                        add_user_dict['displayName'] = new_user_name
                                        add_user_dict['password'] = new_user_password
                                        # print(add_user_dict)
                                        res_add_user = requests.post(BASE_URL + 'addUser', json=add_user_dict, headers=HEADER_dict)
                                        # print(res_add_user.status_code)
                                        if res_add_user.status_code == 200:
                                            logging.info(f'Пользователь {new_user_login} добавлен')
                                            add_users(get_users_from_server())
                                            users_from_db = get_users_from_db()
                                            users_from_db.sort(key=lambda i: i['login'])
                                            user_list = list()
                                            treedata_update_user = sg.TreeData()
                                            for user_from_db in users_from_db:
                                                user_list.append([user_from_db['id'], user_from_db['login'],
                                                                  user_from_db['name']])
                                                treedata_update_user.insert('', user_from_db['id'], '',
                                                                            values=[user_from_db['login'],
                                                                                    user_from_db['name']],
                                                                            icon=check[0])
                                            if filter_status:
                                                search_str = values['-filterUser-']
                                                # print(search_str)
                                                filtered_users = filter(lambda x: search_str in x['login'],
                                                                        users_from_db)
                                                filtered_users_list_of_dict = list(filtered_users)
                                                # print(filtered_users_list_of_dict)
                                                # print(len(filtered_users_list_of_dict))
                                                filtered_users_list = list()
                                                # users_from_db = filtered_users_list_of_dict
                                                for filtered_user_list_of_dict in filtered_users_list_of_dict:
                                                    filtered_users_list.append([filtered_user_list_of_dict['id'],
                                                                                filtered_user_list_of_dict['login'],
                                                                                filtered_user_list_of_dict['name']])
                                                window['-users-'].update(filtered_users_list)
                                            else:
                                                window['-users-'].update(user_list)
                                            window['-TREE2-'].update(treedata_update_user)
                                            window_add_user.close()
                                            sg.popup("Пользователь добавлен!", title='Инфо', icon=ICON_BASE_64,
                                                     no_titlebar=True, background_color='lightgray')
                                            break
                                        else:
                                            logging.error(f'Пользователь {new_user_login} НЕ добавлен - {res_add_user.status_code}')
                                            sg.popup("Пользователь не добавлен!", title='Инфо', icon=ICON_BASE_64,
                                                     no_titlebar=True, background_color='lightgray')
                            if event == '-DelUser-':
                                if values['-users-'] == []:
                                    # print(f"Не выбран пользователь")
                                    sg.popup('Не выбран пользователь', title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='lightgray')
                                else:
                                    if filter_status:
                                        del_user = filtered_users_list_of_dict[values['-users-'][0]]
                                    else:
                                        del_user = users_from_db[values['-users-'][0]]
                                    if del_user == 'admin':
                                        sg.popup("Нельзя удалить admin", title='Инфо', icon=ICON_BASE_64,
                                                             no_titlebar=True, background_color='lightgray')
                                    else:
                                        window_del_user = make_del_user_window(del_user['name'])
                                        while True:
                                            ev_del_user, val_del_user = window_del_user.Read()
                                            # print(ev_del_user, val_del_user)
                                            if ev_del_user == sg.WIN_CLOSED or ev_del_user == 'Exit':
                                                # print('Закрыл окно удаления пользователя')
                                                break
                                            if ev_del_user == 'noDel':
                                                # print('Закрыл окно удаления пользователя')
                                                window_del_user.close()
                                                break
                                            if ev_del_user == 'okDel':
                                                # del_user_id = users_from_db[values['-users-'][0]]['id']
                                                # del_user_dict = {}
                                                # del_user_dict['id'] = del_user['id']
                                                # print(del_user['id'])
                                                res_del_user = requests.post(BASE_URL + 'deleteUser', json=del_user, headers=HEADER_dict)
                                                # print(res_del_user.status_code)
                                                if res_del_user.status_code == 200:
                                                    logging.info(f'Пользователь {del_user["name"]} удалён')
                                                    drop_db('users')
                                                    add_users(get_users_from_server())
                                                    users_from_db = get_users_from_db()
                                                    users_from_db.sort(key=lambda i: i['login'])
                                                    user_list = list()
                                                    treedata_update_user = sg.TreeData()
                                                    for user_from_db in users_from_db:
                                                        user_list.append([user_from_db['id'], user_from_db['login'],
                                                                          user_from_db['name']])
                                                        treedata_update_user.insert('', user_from_db['id'], '',
                                                                                    values=[user_from_db['login'],
                                                                                            user_from_db['name']],
                                                                                    icon=check[0])
                                                    del_users_in_groups_after_delete_user(del_user['id'])
                                                    if filter_status:
                                                        search_str = values['-filterUser-']
                                                        # print(search_str)
                                                        filtered_users = filter(lambda x: search_str in x['login'],
                                                                                users_from_db)
                                                        filtered_users_list_of_dict = list(filtered_users)
                                                        # print(filtered_users_list_of_dict)
                                                        # print(len(filtered_users_list_of_dict))
                                                        filtered_users_list = list()
                                                        # users_from_db = filtered_users_list_of_dict
                                                        for filtered_user_list_of_dict in filtered_users_list_of_dict:
                                                            filtered_users_list.append(
                                                                [filtered_user_list_of_dict['id'],
                                                                 filtered_user_list_of_dict['login'],
                                                                 filtered_user_list_of_dict['name']])
                                                        window['-users-'].update(filtered_users_list)
                                                    else:
                                                        window['-users-'].update(user_list)
                                                    window['-TREE2-'].update(treedata_update_user)
                                                    window_del_user.close()
                                                    sg.popup("Пользователь удалён!", title='Инфо', icon=ICON_BASE_64,
                                                             no_titlebar=True, background_color='lightgray')
                                                    break
                                                else:
                                                    logging.error(f'Пользователь {del_user["name"]} НЕ удалён')
                                                    sg.popup("Пользователь не удалён!", title='Инфо', icon=ICON_BASE_64,
                                                             no_titlebar=True, background_color='lightgray')
                            if event == '-CloneUser-':
                                if values['-users-'] == []:
                                    # print(f"Не выбран пользователь")
                                    sg.popup('Не выбран пользователь', title='Инфо', icon=ICON_BASE_64,
                                             no_titlebar=True, background_color='lightgray')
                                else:
                                    if filter_status:
                                        user_clone = filtered_users_list_of_dict[values['-users-'][0]]
                                    else:
                                        user_clone = users_from_db[values['-users-'][0]]
                                    # user_clone = users_from_db[values['-users-'][0]]
                                    window_clone_user = make_clone_user_window(user_clone['name'])
                                    window_clone_user.Element('CloneUserLogin').SetFocus()
                                    password_clear = False
                                    while True:
                                        ev_clone_user, val_clone_user = window_clone_user.Read()
                                        # print(ev_clone_user, val_clone_user)
                                        if ev_clone_user == sg.WIN_CLOSED or ev_clone_user == 'Exit':
                                            # print('Закрыл окно клонирования пользователя')
                                            break
                                        if ev_clone_user == 'showPasswordCloneUser':
                                            if password_clear:
                                                window_clone_user['CloneUserPassword'].update(password_char='*')
                                                window_clone_user['showPasswordCloneUser'].update('Показать')
                                                password_clear = False
                                            else:
                                                window_clone_user['CloneUserPassword'].update(password_char='')
                                                window_clone_user['showPasswordCloneUser'].update('Скрыть')
                                                password_clear = True
                                        if ev_clone_user == 'cloneUserButton':
                                            clone_user_login, clone_user_name, clone_user_password = val_clone_user.values()
                                            clone_user_dict = {}
                                            clone_user_dict['login'] = clone_user_login
                                            clone_user_dict['displayName'] = clone_user_name
                                            clone_user_dict['password'] = clone_user_password
                                            # print(clone_user_dict)
                                            res_clone_user = requests.post(BASE_URL + 'addUser', json=clone_user_dict, headers=HEADER_dict)
                                            # print(res_clone_user.status_code)
                                            # print(res_clone_user.text)
                                            if res_clone_user.status_code == 200:
                                                logging.info(f'Новый пользователь {clone_user_login} создан')
                                                original_groups = get_groups_for_user_from_db(user_clone['id'])
                                                original_groups_ids = []
                                                for or_gr in original_groups:
                                                    original_groups_ids.append(or_gr['id'])
                                                user_from_server = res_clone_user.text[1:-1]
                                                clone_dict = {'UserIds': [user_from_server], 'GroupIds': original_groups_ids}
                                                # print(clone_dict)
                                                res_clone_add_group = requests.post(BASE_URL + 'addToGroup', json=clone_dict, headers=HEADER_dict)
                                                # print(res_clone_add_group.status_code)
                                                if res_clone_add_group.status_code == 200:
                                                    logging.info(f'Группы для {clone_user_login} добавлены')
                                                    add_users(get_users_from_server())
                                                    add_groups_to_user_after_apply(clone_dict)
                                                    users_from_db = get_users_from_db()
                                                    users_from_db.sort(key=lambda i: i['login'])
                                                    user_list = list()
                                                    treedata_update_user = sg.TreeData()
                                                    for user_from_db in users_from_db:
                                                        user_list.append([user_from_db['id'], user_from_db['login'],
                                                                          user_from_db['name']])
                                                        treedata_update_user.insert('', user_from_db['id'], '',
                                                                                    values=[user_from_db['login'],
                                                                                            user_from_db['name']],
                                                                                    icon=check[0])
                                                    if filter_status:
                                                        search_str = values['-filterUser-']
                                                        # print(search_str)
                                                        filtered_users = filter(lambda x: search_str in x['login'],
                                                                                users_from_db)
                                                        filtered_users_list_of_dict = list(filtered_users)
                                                        # print(filtered_users_list_of_dict)
                                                        # print(len(filtered_users_list_of_dict))
                                                        filtered_users_list = list()
                                                        # users_from_db = filtered_users_list_of_dict
                                                        for filtered_user_list_of_dict in filtered_users_list_of_dict:
                                                            filtered_users_list.append(
                                                                [filtered_user_list_of_dict['id'],
                                                                 filtered_user_list_of_dict['login'],
                                                                 filtered_user_list_of_dict['name']])
                                                        window['-users-'].update(filtered_users_list)
                                                    else:
                                                        window['-users-'].update(user_list)
                                                    window['-TREE2-'].update(treedata_update_user)
                                                    # window_clone_user.close()
                                                    treedata_update_user = sg.TreeData()
                                                    for user_id, user_login, user_name  in user_list:
                                                        treedata_update_user.insert('', user_id, '',
                                                                                    values=[user_login, user_name],
                                                                                    icon=check[0])
                                                    window['-TREE2-'].update(treedata_update_user)
                                                    window_clone_user.close()
                                                    sg.popup("Пользователь клонирован!", title='Инфо',
                                                             icon=ICON_BASE_64,
                                                             no_titlebar=True, background_color='lightgray')
                                                    break
                                                else:
                                                    logging.error(f'Добавление групп для {clone_user_login} НЕ выполнено - {res_clone_add_group.status_code}')
                                                    sg.popup("Добавление групп не выполнено", title='Инфо', icon=ICON_BASE_64,
                                                             no_titlebar=True, background_color='lightgray')
                                            else:
                                                logging.error(f'Новый пользователь {clone_user_login} НЕ добавлен')
                                                sg.popup("Пользователь не добавлен!", title='Инфо', icon=ICON_BASE_64,
                                                         no_titlebar=True, background_color='lightgray')
                            if event == '-filterUser-':
                                filter_status = True
                                if values['-filterUser-']:
                                    search_str = values['-filterUser-']
                                    # print(search_str)
                                    filtered_users = filter(lambda x: search_str in x['login'], users_from_db)
                                    filtered_users_list_of_dict = list(filtered_users)
                                    # print(filtered_users_list_of_dict)
                                    # print(len(filtered_users_list_of_dict))
                                    filtered_users_list = list()
                                    # users_from_db = filtered_users_list_of_dict
                                    for filtered_user_list_of_dict in filtered_users_list_of_dict:
                                        filtered_users_list.append([filtered_user_list_of_dict['id'], filtered_user_list_of_dict['login'], filtered_user_list_of_dict['name']])
                                    window['-users-'].update(filtered_users_list)
                                else:
                                    user_list_after_filter_null = list()
                                    for user_from_db in users_from_db:
                                        user_list_after_filter_null.append(
                                            [user_from_db['id'], user_from_db['login'], user_from_db['name']])
                                    window['-users-'].update(user_list_after_filter_null)
                                    filter_status = False
                            if event == '-filterGroup-':
                                filter_status_group = True
                                if values['-filterGroup-']:
                                    search_str = values['-filterGroup-']
                                    # print(search_str)
                                    filtered_groups = filter(lambda x: search_str in x['name'], groups_from_db)
                                    filtered_groups_list_of_dict = list(filtered_groups)
                                    # print(filtered_groups_list_of_dict)
                                    # print(len(filtered_groups_list_of_dict))
                                    filtered_groups_list = list()
                                    # users_from_db = filtered_users_list_of_dict
                                    for filtered_group_list_of_dict in filtered_groups_list_of_dict:
                                        filtered_groups_list.append([filtered_group_list_of_dict['id'], filtered_group_list_of_dict['name'], filtered_group_list_of_dict['desc']])
                                    window['-groups2-'].update(filtered_groups_list)
                                else:
                                    group_list_after_filter_null = list()
                                    for group_from_db in groups_from_db:
                                        group_list_after_filter_null.append(
                                            [group_from_db['id'], group_from_db['name'], group_from_db['desc']])
                                    window['-groups2-'].update(group_list_after_filter_null)
                                    filter_status_group = False
                            if event == '-filterJournal-':
                                filter_status_journal = True
                                with open('admin.log', mode='r', encoding='cp1251') as log_f:
                                    journal_list = log_f.read().rstrip('\n').split('\n')
                                filtered_journal = []
                                filtered_journal = filter_journal(journal_list)
                                if values['-filterJournal-']:
                                    search_str = values['-filterJournal-']
                                    # print(search_str)
                                    filtered_journal = list(filter(lambda x: search_str in x, filtered_journal))
                                    output_text = "\n".join(filtered_journal)
                                    window['journal'].update(output_text)
                                    window['countLogs'].update(len(filtered_journal))
                                else:
                                    filter_status_journal = False
                                    window['journal'].update('\n'.join(filtered_journal))
                                    window['countLogs'].update(len(filtered_journal))
                            if event == '-AddGroup-':
                                window_add_group = make_add_group_window()
                                window_add_group.Element('GroupName').SetFocus()
                                while True:
                                    ev_add_group, val_add_group = window_add_group.Read()
                                    # print(ev_add_group, val_add_group)
                                    if ev_add_group == sg.WIN_CLOSED or ev_add_group == 'Exit':
                                        # print('Закрыл окно добавления группы')
                                        break
                                    if ev_add_group == 'addGroupButton':
                                        new_group_name = val_add_group['GroupName']
                                        new_group_desc = val_add_group['description']
                                        add_group_dict = {}
                                        add_group_dict['name'] = new_group_name
                                        add_group_dict['description'] = new_group_name
                                        # print(add_group_dict)
                                        res_add_user = requests.post(BASE_URL + 'addGroup', json=add_group_dict, headers=HEADER_dict)
                                        # print(res_add_user.status_code)
                                        if res_add_user.status_code == 200:
                                            logging.info(f'Группа {new_group_name} добавлена')
                                            add_groups(get_groups_from_server())
                                            groups_from_db = get_groups_from_db()
                                            groups_from_db.sort(key=lambda i: i['name'])
                                            treedata_update_group = sg.TreeData()
                                            group_list = list()
                                            for group_from_db in groups_from_db:
                                                group_list.append([group_from_db['id'], group_from_db['name'],
                                                                   group_from_db['desc']])
                                                treedata_update_group.insert('', group_from_db['id'], '',
                                                                             values=[group_from_db['name'],
                                                                                     group_from_db['desc']],
                                                                             icon=check[0])
                                            if filter_status_group:
                                                search_str = values['-filterGroup-']
                                                # print(search_str)
                                                filtered_groups = filter(lambda x: search_str in x['name'],
                                                                         groups_from_db)
                                                filtered_groups_list_of_dict = list(filtered_groups)
                                                # print(filtered_groups_list_of_dict)
                                                # print(len(filtered_groups_list_of_dict))
                                                filtered_groups_list = list()
                                                # users_from_db = filtered_users_list_of_dict
                                                for filtered_group_list_of_dict in filtered_groups_list_of_dict:
                                                    filtered_groups_list.append([filtered_group_list_of_dict['id'],
                                                                                 filtered_group_list_of_dict['name'],
                                                                                 filtered_group_list_of_dict['desc']])
                                                window['-groups2-'].update(filtered_groups_list)
                                            else:
                                                window['-groups2-'].update(group_list)
                                            window['-TREE-'].update(treedata_update_group)
                                            window_add_group.close()
                                            sg.popup("Группа добавлена!", title='Инфо', icon=ICON_BASE_64,
                                                     no_titlebar=True, background_color='lightgray')
                                            break
                                        else:
                                            logging.error(f'Группа {new_group_name} НЕ добавлена')
                                            sg.popup("Группа не добавлена!", title='Инфо', icon=ICON_BASE_64,
                                                     no_titlebar=True, background_color='lightgray')
                                            window_add_group.Element('GroupName').SetFocus()
                            if event == '-DelGroup-':
                                if values['-groups2-'] == []:
                                    # print(f"Не выбрана группа")
                                    sg.popup('Не выбрана группа', title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='lightgray')
                                else:
                                    if filter_status_group:
                                        del_group = filtered_groups_list_of_dict[values['-groups2-'][0]]
                                    else:
                                        del_group = groups_from_db[values['-groups2-'][0]]
                                    # del_group_name = groups_from_db[values['-groups2-'][0]]['name']
                                    window_del_group = make_del_group_window(del_group['name'])
                                    while True:
                                        ev_del_group, val_del_group = window_del_group.Read()
                                        # print(ev_del_group, val_del_group)
                                        if ev_del_group == sg.WIN_CLOSED or ev_del_group == 'Exit':
                                            # print('Закрыл окно удаления пользователя')
                                            break
                                        if ev_del_group == 'noDelGroup':
                                            # print('Закрыл окно удаления пользователя')
                                            window_del_group.close()
                                            break
                                        if ev_del_group == 'okDelGroup':
                                            # del_group_id = groups_from_db[values['-groups2-'][0]]['id']
                                            # del_group_dict = {}
                                            # del_group_dict['id'] = del_group_id
                                            # print(del_group['id'])
                                            res_del_group = requests.post(BASE_URL + 'deleteGroup', json=del_group, headers=HEADER_dict)
                                            # print(res_del_group.status_code)
                                            if res_del_group.status_code == 200:
                                                logging.info(f'Группа {del_group["name"]} удалена')
                                                drop_db('groups')
                                                add_groups(get_groups_from_server())
                                                groups_from_db = get_groups_from_db()
                                                groups_from_db.sort(key=lambda i: i['name'])
                                                treedata_update_group = sg.TreeData()
                                                group_list = list()
                                                for group_from_db in groups_from_db:
                                                    group_list.append([group_from_db['id'], group_from_db['name'],
                                                                       group_from_db['desc']])
                                                    treedata_update_group.insert('', group_from_db['id'], '',
                                                                                 values=[group_from_db['name'],
                                                                                         group_from_db['desc']],
                                                                                 icon=check[0])
                                                del_users_in_groups_after_delete_group(del_group['id'])
                                                if filter_status_group:
                                                    search_str = values['-filterGroup-']
                                                    # print(search_str)
                                                    filtered_groups = filter(lambda x: search_str in x['name'],
                                                                             groups_from_db)
                                                    filtered_groups_list_of_dict = list(filtered_groups)
                                                    # print(filtered_groups_list_of_dict)
                                                    # print(len(filtered_groups_list_of_dict))
                                                    filtered_groups_list = list()
                                                    # users_from_db = filtered_users_list_of_dict
                                                    for filtered_group_list_of_dict in filtered_groups_list_of_dict:
                                                        filtered_groups_list.append([filtered_group_list_of_dict['id'],
                                                                                     filtered_group_list_of_dict[
                                                                                         'name'],
                                                                                     filtered_group_list_of_dict[
                                                                                         'desc']])
                                                    window['-groups2-'].update(filtered_groups_list)
                                                else:
                                                    window['-groups2-'].update(group_list)
                                                # del_users_in_groups_after_delete_group(del_group_id)
                                                # window['-groups2-'].update(group_list)
                                                window['-TREE-'].update(treedata_update_group)
                                                window_del_group.close()
                                                sg.popup("Группа удалена!", title='Инфо', icon=ICON_BASE_64,
                                                         no_titlebar=True, background_color='lightgray')
                                                break
                                            else:
                                                logging.error(f'Группа {del_group["name"]} НЕ удалена - {res_del_group.status_code}')
                                                sg.popup("Группа не удалена!", title='Инфо', icon=ICON_BASE_64,
                                                         no_titlebar=True, background_color='lightgray')
                            if event == '-Start-':
                                print('Стартуем сервер')
                                sg.popup('Запускаем сервер', title='Инфо', icon=ICON_BASE_64, no_titlebar=True,
                                         background_color='lightgray')
                                path_home_server = Path(Path.home(), 'Omega')
                                # print(path_home_server)
                                start_command = 'cd ' + str(path_home_server) + ' && ./run'
                                process = subprocess.Popen(start_command, shell=True,
                                                               stdout=subprocess.PIPE,
                                                               stderr=subprocess.PIPE)
                                # process = subprocess.Popen("ssh pashi@10.1.4.156 'bash ./run > /dev/null'", shell=True,
                                #                                stdout=subprocess.PIPE,
                                #                                stderr=subprocess.PIPE,
                                #                                executable=r'C:\Program Files\PowerShell\7\pwsh.exe')
                                for i in range(3):
                                    sleep(1)
                                    res_ping = ''
                                    try:
                                        res_ping = requests.get(BASE_URL_PING, timeout=1)
                                    except Exception:
                                        print("Сервер не отвечает")
                                    if res_ping == '':
                                        print('Нет ответа сервера')
                                        if i == 2:
                                            logging.critical(f'Сервер не отвечает - {res_ping.status_code}')
                                            sg.popup("Сервер не отвечает", title='Инфо', icon=ICON_BASE_64,
                                                     no_titlebar=True,
                                                     background_color='lightgray')
                                    else:
                                        if res_ping.status_code == 200:
                                            logging.info(f'Сервер запущен')
                                            # print(f'{res_ping.text}')
                                            dict_online_after_start = json.loads(res_ping.text)
                                            # print(dict_online_after_start)
                                            update_text = 'Пользователей онлайн: обновление...' + ', Версия БД: ' \
                                                          + str(dict_online_after_start["databaseVersion"])
                                            server_status['online'] = dict_online_after_start["onlineUsersCount"]
                                            server_status['db'] = dict_online_after_start["databaseVersion"]
                                            window['-StatusBar-'].update(update_text, background_color='lightgreen')
                                            window['-Start-'].update(disabled=True)
                                            window['-Stop-'].update(disabled=False)
                                            TOKEN = get_token(BASE_URL_AUTH)
                                            HEADER_dict = {}
                                            HEADER_dict["Authorization"] = "Bearer " + TOKEN
                                            # print(TOKEN)
                                            # print(HEADER_dict)
                                            server_status['run'] = True
                                            # print('before init')
                                            init_db()
                                            # print('after init')
                                            users_from_db = get_users_from_db()
                                            # print(users_from_db)
                                            groups_from_db = get_groups_from_db()
                                            # print(groups_from_db)
                                            users_from_db.sort(key=lambda i: i['login'])
                                            groups_from_db.sort(key=lambda i: i['name'])
                                            treedata_update_user = sg.TreeData()
                                            treedata_update_group = sg.TreeData()
                                            user_list = list()
                                            group_list = list()
                                            if users_from_db != [[]] and groups_from_db != [[]]:
                                                for user_from_db in users_from_db:
                                                    user_list.append([user_from_db['id'], user_from_db['login'],
                                                                      user_from_db['name']])
                                                for group_from_db in groups_from_db:
                                                    group_list.append([group_from_db['id'], group_from_db['name'],
                                                                       group_from_db['desc']])
                                            for group in groups_from_db:
                                                treedata_update_group.insert('', group['id'], '',
                                                                             values=[group['name'], group['desc']], icon=check[0])
                                            for user in users_from_db:
                                                treedata_update_user.insert('', user['id'], '',
                                                                            values=[user['login'], user['name']], icon=check[0])
                                            # print('before update gui')
                                            window['-users-'].update(user_list)
                                            window['-TREE2-'].update(treedata_update_user)
                                            window['-groups2-'].update(group_list)
                                            window['-TREE-'].update(treedata_update_group)
                                            window['-AddUser-'].update(disabled=False)
                                            window['-DelUser-'].update(disabled=False)
                                            window['-CloneUser-'].update(disabled=False)
                                            window['-AddGroup-'].update(disabled=False)
                                            window['-DelGroup-'].update(disabled=False)
                                            window['-filterUser-'].update(disabled=False)
                                            # print('after update GUI')
                                            break
                            if event == '-Stop-':
                                # print('Останавливаем сервер')
                                res = requests.get(BASE_URL + 'stopServer', headers=HEADER_dict)
                                if res.status_code == 200:
                                    logging.warning(f'Сервер остановлен администратором')
                                    sg.popup('Сервер остановлен', title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='lightgray')
                                    window['-StatusBar-'].update('Сервер не запущен', background_color='red')
                                    window['-Start-'].update(disabled=False)
                                    window['-Stop-'].update(disabled=True)
                                    window['-users-'].update([[]])
                                    window['-groups2-'].update([[]])
                                    clear_treedata = sg.TreeData()
                                    window['-TREE-'].update(clear_treedata)
                                    window['-TREE2-'].update(clear_treedata)
                                    window['-AddUser-'].update(disabled=True)
                                    window['-DelUser-'].update(disabled=True)
                                    window['-CloneUser-'].update(disabled=True)
                                    window['-AddGroup-'].update(disabled=True)
                                    window['-DelGroup-'].update(disabled=True)
                                    window['-filterUser-'].update(disabled=True)
                                    server_status['run'] = False
                                else:
                                    logging.warning(f'Сервер не остановлен')
                                    sg.popup("Сервер не остановлен", title='Инфо', icon=ICON_BASE_64,
                                             no_titlebar=True,
                                             background_color='lightgray')
                            # if event == tray.key:
                            #     event = values[event]
                            #     if event in ('Отобразить окно', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
                            #         window.un_hide()
                            #         window.bring_to_front()
                            #     elif event in ('Скрыть окно'):
                            #         window.hide()
                            #         tray.show_icon()
                            #         tray.show_message('ОМЕГА К100', 'Приложение свёрнуто!')
                            #     elif event == 'Hide Icon':
                            #         tray.hide_icon()
                            #     elif event == 'Show Icon':
                            #         tray.show_icon()
                            #     elif event == 'Выйти':
                            #         break_flag = True
                            #         window_exit = make_exit_window()
                            #         while True:
                            #             ev_exit, val_exit = window_exit.Read()
                            #             print(ev_exit, val_exit)
                            #             if ev_exit == 'okExit':
                            #                 logging.info('Панель администратора остановлена')
                            #                 logging.info('Стоп лога')
                            #                 window_exit.close()
                            #                 tray.close()
                            #                 break_flag2 = True
                            #                 break
                            #             if ev_exit == sg.WIN_CLOSED or ev_exit == 'Exit':
                            #                 print('Закрыл окно выхода')
                            #                 break
                            #             if ev_exit == 'noExit':
                            #                 print('Закрыл окно выхода')
                            #                 window_exit.close()
                            #                 break
                            if event == 'Tabs':
                                if values['Tabs'] == 'Tab3':
                                    with open('admin.log', mode='r', encoding='cp1251') as log_f:
                                        s = log_f.read().rstrip('\n')
                                        journal_list = s.split('\n')
                                        filtered_journal = []
                                        filtered_journal = filter_journal(journal_list)
                                        if filter_status_journal:
                                            filtered_journal = list(filter(lambda x: search_str in x, filtered_journal))
                                        output_text = "\n".join(filtered_journal)
                                        window['journal'].update(output_text)
                                        window['countLogs'].update(len(filtered_journal))
                            if event == 'info':
                                if filter_journal_info:
                                    filter_journal_info = False
                                else:
                                    filter_journal_info = True
                                with open('admin.log', mode='r', encoding='cp1251') as log_f:
                                    s = log_f.read().rstrip('\n')
                                    journal_list = s.split('\n')
                                    filtered_journal = []
                                    filtered_journal = filter_journal(journal_list)
                                    if filter_status_journal:
                                        filtered_journal = list(filter(lambda x: search_str in x, filtered_journal))
                                    output_text = "\n".join(filtered_journal)
                                    window['journal'].update(output_text)
                                    window['countLogs'].update(len(filtered_journal))
                            if event == 'warning':
                                if filter_journal_warning:
                                    filter_journal_warning = False
                                else:
                                    filter_journal_warning = True
                                with open('admin.log', mode='r', encoding='cp1251') as log_f:
                                    s = log_f.read().rstrip('\n')
                                    journal_list = s.split('\n')
                                    filtered_journal = []
                                    filtered_journal = filter_journal(journal_list)
                                    if filter_status_journal:
                                        filtered_journal = list(filter(lambda x: search_str in x, filtered_journal))
                                    output_text = "\n".join(filtered_journal)
                                    window['journal'].update(output_text)
                                    window['countLogs'].update(len(filtered_journal))
                            if event == 'error':
                                if filter_journal_error:
                                    filter_journal_error = False
                                else:
                                    filter_journal_error = True
                                with open('admin.log', mode='r', encoding='cp1251') as log_f:
                                    s = log_f.read().rstrip('\n')
                                    journal_list = s.split('\n')
                                    filtered_journal = []
                                    filtered_journal = filter_journal(journal_list)
                                    if filter_status_journal:
                                        filtered_journal = list(filter(lambda x: search_str in x, filtered_journal))
                                    output_text = "\n".join(filtered_journal)
                                    window['journal'].update(output_text)
                                    window['countLogs'].update(len(filtered_journal))
                            if event == 'critical':
                                if filter_journal_crirtical:
                                    filter_journal_crirtical = False
                                else:
                                    filter_journal_crirtical = True
                                with open('admin.log', mode='r', encoding='cp1251') as log_f:
                                    s = log_f.read().rstrip('\n')
                                    journal_list = s.split('\n')
                                    filtered_journal = []
                                    filtered_journal = filter_journal(journal_list)
                                    if filter_status_journal:
                                        filtered_journal = list(filter(lambda x: search_str in x, filtered_journal))
                                    output_text = "\n".join(filtered_journal)
                                    window['journal'].update(output_text)
                                    window['countLogs'].update(len(filtered_journal))
                        # else:
                        #     sg.popup('Введите правильный ip!', title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='lightgray')
                    else:
                        sg.popup('Введите правильный ip!', title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='lightgray')
                        break
                if window_main_active:
                    window.close()
                    break
            else:
                sg.popup("Неправильный пароль!!!", title='Инфо', icon=ICON_BASE_64, no_titlebar=True, background_color='lightgray')
                window_login['password'].update('')
    if not window_main_active:
        window_login.close()


