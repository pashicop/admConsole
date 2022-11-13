import json
import os
import platform
import socket
import subprocess
import threading
# from datetime import datetime
from time import sleep
# from psgtray import SystemTray
import requests
# import socket
# import os
from pathlib import Path
import sqlite3
# import re
import PySimpleGUI as sg
from io import BytesIO
from PIL import Image, ImageDraw
import ipaddress
import logging
import sys

# import netifaces
# from pystray import MenuItem as item, Menu as menu
# import pystray
# import subprocess
# from multiprocessing import Pool
# from multiprocessing import Process, Queue

# BASE_URL = 'http://10.1.4.147:5000/api/admin/'
ICON_BASE_64 = b'iVBORw0KGgoAAAANSUhEUgAAAMcAAADJCAYAAACXDya2AAAABmJLR0QA/wD/AP+gvaeTAAARR0lEQVR42u1dCZAU1RluLzzwjHgQQRHY3cGNaLJB1CiCioocO9Oz44EQMIUSj6CEmIgSXMUDNQKuO/16sujiRuKJWh4xokhpKEKhiEQFl+USOQJIIpco1+Z/vUh0WWBm+nX3+7r/v+ovqiy0nPe+r99//4bB4qHU72fERRsjbvUwEmKIkbQeNkzxNOlbpO+Tfky6kPRLw7Q20p/19PfW0Z+rd/7zOaQzSSeTVtPfGUHa10hmOhupiuP4fFlwxMy0JHBfZSTFGALztF2A90obiCSJdpdRZl9k9K9pzpfAooeknjvAMNPdDNMeu/MVqA9YtzovjXyh4uIsviAW/00l0+5Cr8J4AuIaDQixN5Wm2X1GaeZ0vjcW76R3pgWRYjiBrU5zQuxB7U/IDBtqpDJH8WWyKDKdrCICVxXp15ik2E3XE0nGOf4RC0tekrTaEogmEJi2hYQUjXUT6YNGT+sYvmyWLF+KMYcSaMpJN4eUFI11rZG0bzHKy/fny2fZs8hwqCmWRIQUjXWKYVa1YhCwNA7JNtuZoNseUWL8/xUxRYIBwdIgicpjKZLzTsRJ8X3dQWbWaDazOBJFkShrEROiSZ1oXJ85iEESyWhUJkYAWM4k2Gtu5DVjYPUhDJZIEcMuoMtfxeDPQpPWJDaxIuVjWLUM/JwIIhg4YRf5BWTnO0+1BjGAwixOPwQDPU/dbMTTZzKIQulnVBbvLOlmoOevs9j/COWrYb/E4FaiAxlMoXLC0x2c5BYDW4Xvschp8mIJy6shLAa1yuiVSDKowiA9Ko6kC93AoFaq/2RghePVGMxg9uT1+CmDC58c0xnMnuhjDC5oR7yykB1xz+qu/kt99YcxyHCTfvcziD2NXPVlkCGKUyoiljKAPe4eZAGUsvQlDF4fGqNS6fYMNjxHfCKD1wdNiHsZbHi5jU0MXl90pdG1/EAGHUyUSlzHoPX19ejFoMMhx3sMWl/1eQYdgpSmW/OInQB6PXgGL4AkrdsYrFzKztIkOcQHDNQg/A77TQafzhLPtGOgBqbbKOdxIoNQ21fDHskgDTRqNYRBqG3ijxa0MEi5z4OlcfjWPoPBqUOfBw3MY9Eut/EAg1OLSt0RDEbtTCqxgIGphc5jMGpFDOtsBqVGysPftDKpxjEotdIHGZQ6SENT0zIGpFa6lCcj6iBlomsIwESjg6xn6M8/kdaQrglBj3kXBmfgiT8aj49edtF43XEqfTiRZQY4QdIMziBFjqXEXkLzhdHn8SP2kLfpDt8ExWNDA3XELwQfjHZniIlPr6J1AYOUTao8wUMDrveeu6kCz5ZXMkiDi1KtAM4k1+77ZbQvY9OKJY/EX7pb6Kd2yFXHpljLUSuWHMlB0RDoLLJVkuXvrOaZuiwRMqnEEsOo3y/LoEMvNq1YcohSURQEO0o1Juvf2qPiYPp3voL+vWXW+Qxa/0yqxyIFFlM8BV7GXsGg9c+kWg4Mln/nbGaYIgFvWnGtlQ8iv7rYQLFz/s0Dqw+hf289dnQucx6D13OTip5obH/j0jyrAZ4F/92PMni9N6mAy9NpG1LquWb5VQOIK8BfzBVsWnkapaKnGRsgNXn/drliDH9y/C8YxJ6RA77jL+EySvcieFXAOAaxJ0JJM1N8DgyOTUb/muYuPw7XsGnF0kSUKn0uODBecH0GsvdDTjRn04qlUVb8EexojdVPyTkkxavghYhjGczqTaolwKD41oiPPVoNOawB4C/HkqzryliyAYT9c/DyiTeUnYUkmSQb9HlkfsagVpb4E/eBm1TXK06EvgFuWo1iUKsjxzxgMGxXvrfCtAaBk+MTBrUKSdmngdvY7yo/k96ZFvTf3Qp9LimriMHtPjpzJ7i/catHCdG3wT8av2dwuycH9o6/VNWpHp3LDbzoJtK+RuUpdIg7gAHwvmdn06fqBGcPH+7Z0L1WtWKQ5286DAU3qe7wOFDxLngZ+w0M8vzJ8R725WdiHp/PEHDTajKDPL+LPx7abEiIT72P5ImTwM3OLbsN0WbJxuGkxBknurIxraZzzVnknHH0LLBPJRKmGAZOjkkM9pzMhcxR4PVDi30rritNtwY3rTY5XY4sWZtU/cBH7z/i7ytLIWPsBT6lDPrsyTGJx9DklBC8Hbx9dgKDPiuTasyh5G9sjNTQNvcfk7bgId21RtfyAxn8+zYREuAOpgjmtbVng78eFzL4902OGuw5uOlLAorujeBVBWEWuawlKf4TyaFtrs1RKgHHJscybp/du2N5KXgt1ZPBvrrURAR9fulOTII9m1Q2uL8RD/j8ysE/LvczCZoS/G1NwSezSjOng5OjlonQlODPwX1ek9d3Hvbr63ElMyY5wIe2mVZfTciBPanFtIczGXa/1IXQpdeqhra5PkcqeMR+gWcyGcJ1oa9r9qFZAN0+K4spWXaFIEeBm1SD9DJR7YfA22dvZlKEIz6/zela1CpflOkM/hJPYVI4F2kXgNcETdXvUOF3mWxzBtfxq0HRCWxyDNH0XMeCJ1QHMDlkdALZeUxlTua8kSd+x8sRJwYN9cJu8dQ37NhQcbAc+Gy/dr0mDjvxBz53SXbg6e3PVXKtGi45pvKkcC9f5nQ38Gz5E9EkBv4Y/Y+1P2PZrmuKVcBn/KXvLcd6fNXAF7AkrLtBAh7YbQB+D6vQ5NJeh760ePpMDNPV7g4+tuehaBEDf5/2YpizllM9TLEG+Kzropb4u5KHtvl63k9w4APH33gGfMLIuVDnnbQv5xVpCNKj4mAK4a4DvqiVToINSeCnuohp0SBH3OoB/hVLgwZAkOeBqV9Xran9mwHP2l6MmXClYc3Y1Qi/Cjcx4CeM0NA2aaKwOcuFiMpFOrLYJlU1eG7paehCxFDv8TDFg+DtsH3ATdoybNPK7h1eciTEZ8CXs8FZj4As8suLvd6hKpzESFYWg3f8PRuS1/sF4HtYBRdGz44c4k5wclwVjnuwrwavtTonjP4GcjvsNxTtOTIU95BKH+44t7gfqQfCRQz0ZfJJ8WrIXvGXgT9Uc0PmiFs3cQJKq1e8P7ZpVVkYpst4C3qGUqriuFCRQ871xd7zPowvQo+s+DshzTkhN5u9GxL71uoH3uT/m3CG1slU5ImIHFfnid9N+YGVx0IPuICfiCiL3UyxHrhcZIYRZjHFZGByTEJPOPUGb4f9Q8jJMRj4w7XRGFh9CPDhW+O5d1ljgZ8dZvXEPPiG3o2VwLmNfxlREOipk9Q4Byll1vngvRvlkSCH3KKEe0crnF0kgFlx7O2wCfuMSJBD9mbLHm3Y4XriLERnD3g7rLXI6+OpN4wD6mKxc2pjseHzi4omzo/FZtCf80gXks4hnUpq1RYWDpoXi7Xx+K6mARci3ouW+OvIIyibls+KiooI9GNJvyStz0FnE1Fu+rS4+HAP/I6hPNDbvxDuSO4Z+KEsaNeudW1RUQ2BfFuOpGisq+sKC4d+UFKibtAD+hKhVLo9kkn1ITA5lqvuNiOTaTCBep1LUuz2ktAr1FFh2H0GsBl8KwgxKk/B7t2gbUiK5ItWrQ6l1+Iviknxfd1ExOuryBS+jTf6em9S3YI9B9e+SMUxrCgpOYzA+7aHxPhOd9QVFbn/cqaqTgX+qG1zasX0fzmoxBt5k5Ac2e9SyGluRi/GOz4QY5eSH3KjAnN4FnCtVT/NcxvglZ6KdtDNLyyc4CcxdupWCg1f6tLvuAPYHH5Od0d8YNSHhhFIrw2AGN/pmrkdOrR0YRIXQM8V07oQ0bRfivLhUh7iJA+iUjkpmXPuZsrKmjLcEPxlmpYh0DRA6Gl6tFDHpZBZ82SQxNjlf8Ril7h4/e8C/sBZumbF4+DtsFe6MqcKCjoQMLfrQA7SmfnfI/RkyuV6FiImxIQoD22jr/WfNSFGgxYUdHHxeszFLUS0SjQzqZxl8MAbS61XFOQ0NuhEDpl8dOE7jgL+0N2jmSOe7gbeDnutS0f8Sq1ejQZdt7hNm/wCDHLHOu59fqSbSTUuymNedHHEd9PCwotdmFZ1uIWIlO3XKL+xGJgcUxTkNhbqSA7qFbnbRc5jNHCt1RA9iIH9BNc7baJuXo327Y/U8tVo0FdcmMqdgMnxti6Fhsi9GzucXgYXsiAWK9GYHHNdWgSo3ZxbjJ7WMTqYVO8Dk2O6a5MqFuulMTnWufMlgecAyCU9wRIj0xK7d4N6GNyT42qNybGdetXzT4ohb/9NiL8GHaW6Lup7HqhUvL/G5Kif2rWrixJ8yjabYino/X5F+bdmAb4clDyLeDycXo6kxuTY7N6nFI9GvXEtz0JDsQmYHHepOAbq475QV3JQlnylgkrrLsCRyEeDMql6QZtUpZnTVRyDnCmlKzmofXaa6x/YMNZ1Beg9LwmqdyMDTI46VcdADu/+zqADPV+O8YoikhZw0KWjz8xwHLUvgMN8o1Weht/94jm8HGoWfUrbHbeodITPWXEqC4bOimc6qzwOiliN1LS2qq3CquvVoPc902eTiiaQ45JjmeqGGKrKjWlIjlmK77wqqlUQuR7ULOBntsKLI6GQ7oeaFR2qXUcs+7NxP4iD/SFGn8d+DJ0Vl70nHgiBcYBG5FhPvRxHK/2B12cOovNbC9oC/ZpfrwbwHjk1Q9uaEjnIjUC5SBNyjPbk7nFbob8x+jx+hB8h3NeATarxXh4NRYdSGhBj9cK2bY/yqAIbdwFqwjY5Kx7ggkVZ5EfgfD1QcqgaLN2UNKzO/gr0/qu9rqXqA2xSrfdjIt7i4uITCaSrAiLHUz6Y1RNhTWoZkvbwYKpwn1X/SpgptNvJ96w5RcvmdOzY3PuyITJPYDGQOc/LrPgy4AkjKT9TQUSQOIH2W786/lzNyM3dtN7A6+x+8GoA9xSbYrM/0YpGuY+Cgp4+zLP6gFaqHe9z0emzUa+pa2xS3QNcuvyyEZDUnXZaMUWxaj0qD5kgt0f5/qOS4grcsT1WkRdhvNnAlZkDjABFApjA/DDpFkXEWCbNtsB+UO/MYbBRSwWt0T+U0nRr4Kz4VrdD21TJguLi9jsHwH2TJymWk+P9u0Bei90tiRdBw/n/UJ34uxHY35hsaCb01W9B5SY3k7n1NwL8xn0QYinp40Sq3pRHOUCbH5EQ18BOuExVHKcyv/EGsL9xg6GxyGYpGgzXbn6HDt1lht2p0YrFTCLQeZJE2v6PywCHDHRg4mKgmkPoX9Mc+BC2O4WSLF455q+C+h2TVNmWCWCTahoj2FO/A3QHJG0gU1ItITes4pJjGCPYQ4mPPZrO+Nto1tk1TJ5YCRzCbcsI9vz1+DsoPmy3jvjZwEMUZjNyfYlaoU69XOGuXdoU9wGTYyQj15eEYAsnl4TZFdrJTTQCeCe1+Akj1zfTagpo++yo/H5wKnMysCM+nxHrJzlgk8Rz8n01bgZ+NR5gxPqZEKw6wck8R2Z/IG4UgnZRi7MYsb475u9FY38gdlZc+dA2lqzIMSQa+wORe8UDGzsfcUmJk0Art3PcH4g8Qb1MdGWkBha1mh7+/YGm+ByUHGu8GtrGkhVuhoV7+EbCPgM4hFvFCA1Q4qINqGmV5f5A0x4OnBW/nBEa+OuBuXo7q/2Bssybh7ax5CtJcXs4Azmp8T/CrZOhSXwsGpCDKqFDuT/QtPri+ht2GSNTG9Pqo/DtDzTFU6Dk+NpJXLLoQo4/hmt/YMPetzWgr8ZLjEidEoI0OC1U+wPL0ucC7174JSNSM0mIT8OzPzAh7gUlxxYnkMCiGTmsu8OzPxB13GfCfpORqGXUqmM49gciL8FM2L9mJGrrmM/D3x+I2yS/3TAzLRmFupLDuh9/f6CM9vBQYBbVErdKsPcHyoIrWXqBWUv1W0ag9qbVAtz9gQm7Ow9tY/EuakWrxmD3BybEOFByzGLkIUStMp1x9wfKMTahSvWz6CXOolXE5rm6/wGZ2bRwzwfZsgAAAABJRU5ErkJggg=='
ICON_SHOW_BASE_64 = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAi9JREFUWEft1surT1EUB/DP9X6WJEaYeowkpKirGJGBGWWmyFiZmJmYmJgzEP4BN93BJXdAlIQ8hoqJR1555hGt2kf7Hvv8fufnXn6T3xqds9djf/da37X2HtJnGerz/gYABhn4mwwswX7sxspE4qcYwVk874XYbQFMwykcpitxf+I0DuFHNzBtABzHsUKgL3id1hdjTsHmJI50AtEJwFy8wIIswA3sw+OGoMtxHlsz/WcsxYeSTxOA1XiYOdzFRnztltKkn4Hr2JDZr8ftun8JwObkXNnuxKWa4/REuD0IflxGfEdZctmGK9nCDozlBnUAq/AoGQSZgvFVnSu/ZXjWkIl1uFPTLcTbBDRUEzKRA5iHj9nm8V8/UaiD2XHqkJv4hDhpJaEL8LnMTLEqv0V4FwY5gNhsdvL6bdAhpTEDniR9ZOpl+g7WB/vrMj8j4jfMygFcxK7ksT3VtJTlC9iLN4jWy+VVWgvyri05YxOik0KuRuaqDOQA/iBKFixaLNow0h4nyiXWonWvYUsLAOMY7rUEQaBbKXhMuwPp+wSOpu9iuyXA1Sz4juDFBA60JWHM+hgsJYk7YUVB0YqE4ZcPoKY2DLv7hTo31b51G1bA2wyisI2MBV+CzaN4Xzh5z4OoirEGD7KA99JY/S+juNq3dBnF4Ik2bLqMov7npuIyyrPZt+s4B9Hrg+QMDk7Vg6TOrfxJFimPWfLPn2QNbT/55TZPssnv0iHCAMAgA78ACiR5IZsXaIEAAAAASUVORK5CYII='
ICON_HIDE_BASE_64 = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAzlJREFUWEfFllmojVEYhp9jOGYns2RMpmQqZShliAuJ3IgSDsmUDJFkynBBUrhAISK5UDJcKIkonFA4JENcmDMmMxl69S2ts1p7n/8/e9vem73/tb7hXeubVhH/GUUF8t8buBbzVQgCm4F5wAOgY0jiXxOoCXwzpyKyoNAELgN9gV9AtXyGQDfXCGhuRl8Ab82R89MaeGQfY4EjuRIoBjYCswBdbQzfgd121c+BEuA90DBTsifJgRrAWWBgFSumHfCwqgSmAHsCZWXzKuAE8M72dMIRwBqgkyev0uuTjXi2GzgHDPKU9wLTgJ+V3ITCtMhkalkV1Ac+pMmBJ0ArU1ByKaE+BQaqA/0tHy4CXwGFS3kgbAPm2P/HgMg0S1KGz4CWJngMGBNhfhAYH6yft1IbEJRdN+CWyb4Bmvh6YQiuAmqbwhZgfsT5UWB0JWEYBxzyZNYCy+37DtDV7fkE1gNLbEPxLo04USxVVkKZ5Yhy4jgw0tY/ApILsRWYa4vbgdn67wgoc+/a5g2gZ4YTrgRWRzrbcOCk6ajfq1JiEOl+ttELKHcElEBqNEILQJ0tBp10FKCkauMJ/LD43wR6ZNDVssrVla6StdgRkFK5KV7yWIa2FEfFUxBhGVkHLLO12lYNmTicBobYppK1zM8BlY3arKB4aYSGkFPdlqABo7xZat+7gOlZTu8TPQBMlGxYBcrQzmZEXU0dL8QMYEdkPVtTU2NSgxLUltWe/yCmpFrVpBP2A5MizkRSdd/U9nQanSoGZfxM21A3bOALZWL9GmhsgmpM7b2HhdN/aQQ+A3UjntUV7wNtbU/lq+mo0P1FtmvTIFGpOGwCFpuBwcAZ2+jilbCT9eOttQrNJykByS0E5NjHdSs1vXBuA2q1wlBgg72AfPkVVinR+CR5D6i0rgDdIxbqAF+AepFpd8/aejjEKphJQsApyMlOYIIt7AMm2391vg42qg8DU72WHT25W0xDQDqngGGm7HT1q3H9FFBHTIU0BDRGX5l1DSoNrJyRhoAemZoTirlinxckJaC+fcE8KhndAyNnEkkJ6AGih4gy27XqnJ3LQFICktWbzg2ivDhPSyBvTn1DvwGQ9JMh9I2ufAAAAABJRU5ErkJggg=='
ICON_CHECK_BASE_64 = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAsQAAALEBxi1JjQAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAASfSURBVFiFzZdfbBRFHMc/M7t3Vwq09qCAxPKnJbYFKqSatCgEMdGgCKT+xagxkGCID0bA+CT4NyEN/iHBF6I+qPFBTCu+8IKQGMSWllJLQFqsEdoCd71ry9Frr3d7N+PD9Y52uS1XbaLfZLOzs7/5fT87szs7A/+xxCRipwOPAZVAEZALRIA+4BzQCLRPNSDA48IQR4UUMUBPdEhTdgC7gRlZ5K0AKibqgUphigM6rtcACCkoKPfiLZuFp8CDJz8HZSmioSihzgH6zgeJhqIACEMEdULvBr52yL0BqAOGnAC2CSEOaa1Nd56bJU+Xcs/DRbjz3I60OqHpbfXTWXeJgfZ+hCES1furZzbsaog4mHuA/ZkAaoG3ABY/WULpC+WYuaajcSb1tvhACOZUzm1Qluupo8997xu9tR74AcgBDgA77QBvAJ9Kl6Rix0qKHlkwKWMHdZhQfaTmSLXdHGDsoz2K4GOAyl0PMK96/lSYA5ReOdlzHFhqNweQo2e3dMkv0MjSLeVTaU6g1U/bwdbKTOZjAXYoSy2YuTCPJc/eO6XmzfuaUFaCRU8UR2vqaz60x0hACkPuASh/eRlCTGZuys588cYSlm+/zxOTaqc9TgKrdELNnj5/BnPun5sxWd+FIG2ftRK9MZKVeW+Lj+Z9p9Pmy7ZVJM202JIJYDPAvKq7HRNeO3mV7uNXaNhz6o4QvS0+ztQ2oSxF8aZb5gAaSjbU1ywfByBMYx1A4Yo5jknLXlpKfsldhHsGaXj7F0b6M0MEWv2cqW1GWYrFG0tYurVi3P3ojSh/1nVsHweAVsUA0wqnOQK4ZriofvehJMTVMI17b4ewj/nYJ0/p/OdttH/7++tA1S0ARR6Ax5vjCJAJomHPLYhszAF0XKeK89IA6SptD88MUbX3QfIW5TN0LUzj3lN0n+hKv3D2MbcrEUukiioNICQhwHFc7XLnuVn1werRnhik7eBZxzG3a2Qg7XEjDYCgEyASGM4KAMYPBzBht6ektSYSSP8YO1MFU8f1CaAq0OqncKXzl5AJYtX7q7l5JYS3fNYd4wfa+4kPW0iX7FKWup6ql8CPAL7TPsfGTjJzzazMAfxNSU9lqe/G1kugSZrSN+wfwtd4PVPbfy0rbNH1U1fqst4OoFVcvQNw8ZsL6IRiqtVZdwkrHEOY4gTJxWtaxui5Tbrki7FQ1KvjmtkrCqfMvP9iH+cPtaG11iieAcaNdep3HFeW2iqESHTWX+Lqz91TYh4JDNNS24SKK9B8ArTaY4wx5S6gG9jsb/ZhmEbWL1gm3bwc4vR7DYz0jyAMcRzNK2SY7gzb9W9IQLE2eC4gIsFhvGVeDE/2i1Kd0HQdu8zZj5qJ3YwhTKNRJ9QmkpuY2+S0+nheSPGVVtpj5poUb15C0boFTCvMdTSOj8TxN/v443AH4Z7BZKXkSxSvATGndhMtf8qFIfbrhN6QqsgvzqegbBY5BTl4CjzEh+NE+iKEewYJnguirORcL13yL2WpN7F9cv9Ua6SUh4UhhphoayZICFP8CrwKuLJNPpkFoBtYS3JzupDk5jQKBIALwDEgOIl8/w/9DR5k79YG7eHTAAAAAElFTkSuQmCC'
version = '1.0.2'
# folder_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABnUlEQVQ4y8WSv2rUQRSFv7vZgJFFsQg2EkWb4AvEJ8hqKVilSmFn3iNvIAp21oIW9haihBRKiqwElMVsIJjNrprsOr/5dyzml3UhEQIWHhjmcpn7zblw4B9lJ8Xag9mlmQb3AJzX3tOX8Tngzg349q7t5xcfzpKGhOFHnjx+9qLTzW8wsmFTL2Gzk7Y2O/k9kCbtwUZbV+Zvo8Md3PALrjoiqsKSR9ljpAJpwOsNtlfXfRvoNU8Arr/NsVo0ry5z4dZN5hoGqEzYDChBOoKwS/vSq0XW3y5NAI/uN1cvLqzQur4MCpBGEEd1PQDfQ74HYR+LfeQOAOYAmgAmbly+dgfid5CHPIKqC74L8RDyGPIYy7+QQjFWa7ICsQ8SpB/IfcJSDVMAJUwJkYDMNOEPIBxA/gnuMyYPijXAI3lMse7FGnIKsIuqrxgRSeXOoYZUCI8pIKW/OHA7kD2YYcpAKgM5ABXk4qSsdJaDOMCsgTIYAlL5TQFTyUIZDmev0N/bnwqnylEBQS45UKnHx/lUlFvA3fo+jwR8ALb47/oNma38cuqiJ9AAAAAASUVORK5CYII='
# file_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABU0lEQVQ4y52TzStEURiHn/ecc6XG54JSdlMkNhYWsiILS0lsJaUsLW2Mv8CfIDtr2VtbY4GUEvmIZnKbZsY977Uwt2HcyW1+dTZvt6fn9557BGB+aaNQKBR2ifkbgWR+cX13ubO1svz++niVTA1ArDHDg91UahHFsMxbKWycYsjze4muTsP64vT43v7hSf/A0FgdjQPQWAmco68nB+T+SFSqNUQgcIbN1bn8Z3RwvL22MAvcu8TACFgrpMVZ4aUYcn77BMDkxGgemAGOHIBXxRjBWZMKoCPA2h6qEUSRR2MF6GxUUMUaIUgBCNTnAcm3H2G5YQfgvccYIXAtDH7FoKq/AaqKlbrBj2trFVXfBPAea4SOIIsBeN9kkCwxsNkAqRWy7+B7Z00G3xVc2wZeMSI4S7sVYkSk5Z/4PyBWROqvox3A28PN2cjUwinQC9QyckKALxj4kv2auK0xAAAAAElFTkSuQmCC'


def icon(check):
    box = (12, 12)
    background = (255, 255, 255, 0)
    rectangle = (0, 0, 11, 11)
    line = ((2, 6), (5, 9), (9, 2))
    im = Image.new('RGBA', box, background)
    draw = ImageDraw.Draw(im, 'RGBA')
    draw.rectangle(rectangle, outline='black', width=1)
    if check == 1:
        draw.line(line, fill='black', width=2, joint='curve')
    elif check == 2:
        draw.line(line, fill='red', width=2, joint='curve')
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
    with open('adm.db', 'w'):
        print('Файл БД создан')
        # bd_file.write('Файл БД создан')
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
    res = []
    try:
        res = requests.get(BASE_URL + 'users', headers=HEADER_dict)
    except Exception as e:
        print(e)
    # print(res)
    if res:
        users = json.loads(res.text)
    else:
        users = []
    return users


def get_groups_from_server():
    # print(f'Запрашиваю группы..')
    res = []
    try:
        res = requests.get(BASE_URL + 'groups', headers=HEADER_dict)
    except Exception as e:
        print(e)
    # print(res)
    if res:
        groups = json.loads(res.text)
    else:
        groups = []
    return groups


def add_users(users_list):
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    for user in users_list:
        is_dispatcher = False
        for role in user['userRoles']:
            if role['name'] == 'Dispatchers':
                is_dispatcher = True
        if is_dispatcher:
            db_insert_user = "insert or replace into Users(id, login, Display_name, is_dispatcher) Values " \
                             "('" + user['id'] + "', '" + user['login'] + "', '" + user['displayName'] + "', '1')"
        else:
            db_insert_user = "insert or replace into Users(id, login, Display_name) Values " \
                             "('" + user['id'] + "', '" + user['login'] + "', '" + user['displayName'] + "')"
        cur.execute(db_insert_user)
    con.commit()
    con.close()


def add_groups(groups_list):
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    for group in groups_list:
        if group['description'] is None:
            db_insert_group = "insert or replace into Groups(id, Name, description, is_emergency) Values " \
                              "('" + group['id'] + "', '" + group['name'] + "', '', '" + str(group['groupType']) + "')"
        else:
            db_insert_group = "insert or replace into Groups(id, Name, description, is_emergency) Values " \
                              "('" + group['id'] + \
                              "', '" + group['name'] + "', '" + group['description'] + \
                              "', '" + str(group['groupType']) + "')"
        cur.execute(db_insert_group)
    con.commit()
    con.close()


def add_user_in_groups(users_list):
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    for user in users_list:
        for group_id in user['userGroupIds']:
            db_insert_user_in_groups = "insert or replace into Users_in_Groups(user_id, group_id) Values " \
                                       "('" + user['id'] + "', '" + group_id + "')"
            cur.execute(db_insert_user_in_groups)
    con.commit()
    con.close()


def add_groups_to_user_after_apply(groups_for_user_dict):
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    for user_id in groups_for_user_dict['UserIds']:
        for group_id in groups_for_user_dict['GroupIds']:
            db_insert_group_for_user = "insert or replace into Users_in_Groups(user_id, group_id) Values " \
                                       "('" + user_id + "', '" + group_id + "')"
            cur.execute(db_insert_group_for_user)
    con.commit()
    con.close()


def add_del_groups_to_user_after_apply(groups_for_user_dict):
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    print(groups_for_user_dict)
    for user_id in groups_for_user_dict['UserIds']:
        for group_id in groups_for_user_dict['addGroupIds']:
            db_insert_group_for_user = "insert or replace into Users_in_Groups(user_id, group_id) Values " \
                                       "('" + user_id + "', '" + group_id + "')"
            cur.execute(db_insert_group_for_user)
    for user_id in groups_for_user_dict['UserIds']:
        for group_id in groups_for_user_dict['removeGroupIds']:
            db_delete_group_for_user = "delete from Users_in_Groups where user_id = '" + user_id + \
                                       "' and  group_id = '" + group_id + "'"
            cur.execute(db_delete_group_for_user)
    con.commit()
    con.close()


def add_users_to_group_after_apply(users_for_group_dict):
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    for group_id in users_for_group_dict['GroupIds']:
        for user_id in users_for_group_dict['UserIds']:
            db_insert_user_for_group = "insert or replace into Users_in_Groups(user_id, group_id) Values " \
                                       "('" + user_id + "', '" + group_id + "')"
            cur.execute(db_insert_user_for_group)
    con.commit()
    con.close()


def add_del_users_to_group_after_apply(users_for_group_dict):
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    for group_id in users_for_group_dict['GroupIds']:
        for user_id in users_for_group_dict['addUserIds']:
            db_insert_user_for_group = "insert or replace into Users_in_Groups(user_id, group_id) Values " \
                                       "('" + user_id + "', '" + group_id + "')"
            cur.execute(db_insert_user_for_group)
    for group_id in users_for_group_dict['GroupIds']:
        for user_id in users_for_group_dict['removeUserIds']:
            db_delete_user_for_group = "delete from Users_in_Groups where user_id = '" + user_id + \
                                       "' and  group_id = '" + group_id + "'"
            cur.execute(db_delete_user_for_group)
    con.commit()
    con.close()


def del_groups_to_user_after_apply(groups_for_user_dict):
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    for user_id in groups_for_user_dict['UserIds']:
        for group_id in groups_for_user_dict['GroupIds']:
            db_delete_group_for_user = "delete from Users_in_Groups where user_id = '" + user_id + \
                                       "' and  group_id = '" + group_id + "'"
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
            db_delete_user_for_group = "delete from Users_in_Groups where user_id = '" + user_id + \
                                       "' and  group_id = '" + group_id + "'"
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
        user_for_table = {'login': user[1],
                          'name': user[3],
                          'id': user[0],
                          'is_dispatcher': user[4],
                          'is_blocked': user[6]}
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
        group_for_table = {'name': group[1],
                           'id': group[0],
                           'desc': group[2],
                           'is_emergency': group[5]}
        # print(group_for_table)
        groups_for_table.append(group_for_table)
    # print('---')
    con.close()
    return groups_for_table


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
        user_for_table = {'id': user[0],
                          'login': user[2],
                          'name': user[1]}
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
        group_for_table = {'id': group[0],
                           'name': group[1],
                           'desc': group[2]}
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
    label_text = 'Панель администратора ОМЕГА К100 ' + ip + ' Версия ' + version
    if users_from_db != [[]] and groups_from_db != [[]]:
        for index, user_from_db in enumerate(users_from_db):
            user_list.append([user_from_db['id'], user_from_db['login'], user_from_db['name']])
            if user_from_db['is_dispatcher']:
                    user_list[index].append(u'\u2713')
            else:
                user_list[index].append('')
            if user_from_db['is_blocked']:
                user_list[index].append(u'\u274c')
            else:
                user_list[index].append('')
        for group_from_db in groups_from_db:
            if group_from_db['is_emergency']:
                group_list.append([group_from_db['id'], group_from_db['name'], group_from_db['desc'], u'\u2713'])
            else:
                group_list.append(
                    [group_from_db['id'], group_from_db['name'], group_from_db['desc'], ''])
    # treedata = sg.TreeData()
    # treedata.insert('', key='key', text='text', values=[1, 2, 3, 4])
    tab1_layout = [
        [sg.Button('Добавить', key='-AddUser-', pad=((30, 10), (20, 5))),
         sg.Button('Удалить', key='-DelUser-', pad=(10, (20, 5))),
         sg.Button('Клонировать', key='-CloneUser-', pad=(10, (20, 5)))],
        [sg.Text('Фильтр: '), sg.Input(size=(20, 1), enable_events=True, key='-filterUser-')],
        [
            sg.Frame('Пользователи',
                     [
                         [sg.Table(user_list, headings=['id', 'Логин', 'Имя', 'Дисп', 'Блок'], justification="left",
                                   # num_rows=20,
                                   key='-users-', expand_y=True, expand_x=True,
                                   enable_click_events=True,
                                   enable_events=True,
                                   # bind_return_key=True,
                                   # background_color='green',
                                   right_click_selects=True,
                                   visible_column_map=[False, True, True, True, True],
                                   right_click_menu=[1, 'Изменить пользователя'],
                                   select_mode='browse',
                                   selected_row_colors='black on lightblue',
                                   auto_size_columns=False, col_widths=[0, 10, 30, 5, 5])], ],
                     expand_x=True,
                     size=(480, 564)),
            sg.Frame('Группы', [[sg.Tree(data=treedata,
                                         headings=['Имя', 'Описание'],
                                         col0_width=5,
                                         # col0_heading="",
                                         col_widths=[20, 30],
                                         num_rows=10, key='-TREE-', row_height=20, metadata=[], auto_size_columns=False,
                                         show_expanded=False, enable_events=True, justification='left', expand_y=True,
                                         select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                                         selected_row_colors='black on lightblue',
                                         )]], expand_y=True, expand_x=True),

        ],
        [sg.Push(),
         sg.Checkbox('Выбрать все группы', enable_events=True, key='-checkAllGroups-', default=False,
                     pad=[30, 0],
                     disabled=True),
         sg.Button('Применить', key='Apply', disabled=True,
                   disabled_button_color='gray', pad=((0, 10), (5, 10)))],
    ]
    tab2_layout = [
        [sg.Button('Добавить', key='-AddGroup-', pad=((30, 10), (20, 5))),
         sg.Button('Удалить', key='-DelGroup-', pad=(10, (20, 5)))],
        [sg.Text('Фильтр: '), sg.Input(size=(20, 1), enable_events=True, key='-filterGroup-')],
        [sg.Frame('Группы',
                  [
                      [sg.Table(group_list, headings=['id', 'Имя', 'Описание', 'Э'], justification="left",
                                num_rows=40, enable_events=True,
                                enable_click_events=True,
                                right_click_selects=True,
                                right_click_menu=[1, 'Изменить группу'],
                                select_mode='browse',
                                selected_row_colors='black on lightblue',
                                visible_column_map=[False, True, True, True],
                                key='-groups2-', expand_y=True, expand_x=True,
                                auto_size_columns=False, col_widths=[0, 10, 30, 2])], ],
                  expand_x=True, size=(480, 564)),
         sg.Frame('Пользователи', [[sg.Tree(data=treedata2, headings=['Логин', 'Имя'], col0_width=5,
                                            col_widths=[20, 30],
                                            num_rows=10, key='-TREE2-', row_height=20, metadata=[],
                                            auto_size_columns=False,
                                            show_expanded=False, enable_events=True, justification='left',
                                            expand_y=True,
                                            select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                                            selected_row_colors='black on lightblue',
                                            ), ]], expand_y=True, expand_x=True),
         ],
        [sg.Push(),
         sg.Checkbox('Выбрать всех пользователей', enable_events=True, key='-checkAllUsers-', default=False,
                     pad=[30, 0],
                     disabled=True),
         sg.Button('Применить', key='Apply2', disabled=True, disabled_button_color='gray',
                   pad=((0, 10), (5, 10)))],
    ]
    tab3_layout = [
        [sg.Text('Фильтр: '), sg.Input(size=(20, 1),
                                       enable_events=True,
                                       key='-filterJournal-')],
        [sg.Frame('Логи',
                  [[sg.Multiline(key='journal', write_only=True, disabled=True, expand_x=True, expand_y=True,
                                 autoscroll=True, auto_refresh=True,
                                 background_color='white')]],
                  expand_x=True, expand_y=True
                  ),
         sg.Frame('Типы',
                  [
                      [sg.Checkbox('Инфо', enable_events=True, key='info', default=True)],
                      [sg.Checkbox('Предупреждение', enable_events=True, key='warning', default=True)],
                      [sg.Checkbox('Ошибка', enable_events=True, key='error', default=True)],
                      [sg.Checkbox('Критическая', enable_events=True, key='critical', default=True)],
                  ], vertical_alignment='top')
         ],
        [sg.T('Количество записей:'), sg.Multiline(key='countLogs', no_scrollbar=True,
                                                   write_only=True, disabled=True, auto_refresh=True,
                                                   background_color='lightgray', size=10)],
    ]
    layout = [[sg.Menu([
        ['Настройки', ['Установить лицензию...', 'Настройки']],
        ['Помощь', 'О программе'], ], key='-Menu-')],
        [sg.Frame('Сервер', [[sg.Push(), sg.Button('Старт', key='-Start-',
                                                   disabled_button_color='gray', pad=((0, 20), 0)),
                              sg.Button('Стоп', key='-Stop-',
                                        disabled_button_color='gray'), sg.Push()]], size=(186, 60), )],
        [sg.TabGroup(
            [[sg.Tab('Пользователи', tab1_layout, key="Tab1"),
              sg.Tab('Группы', tab2_layout, key="Tab2"),
              sg.Tab('Журнал', tab3_layout, key="Tab3"),
              ]], key="Tabs", size=(1000, 690), enable_events=True)],
        [sg.StatusBar(users_online_text, key='-StatusBar-', size=(100, 1))]]
    return sg.Window(label_text, layout, icon=ICON_BASE_64, use_ttk_buttons=True,
                     enable_close_attempted_event=True,
                     relative_location=(0, -50),
                     finalize=True)


def make_login_window():
    # ips = os.popen("hostname -I").read()
    # if ips:
    #     ips = ips.split(" ")
    #     # print(ips)
    #     try:
    #         ip = ipaddress.ip_address(ips[0]).exploded
    #     except ValueError:
    #         print('Неверный ip')
    #         ip = ''
    # else:
    #     ip = ''
    try:
        ip = ipaddress.ip_address((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
                                     if not ip.startswith("127.")] or [
                                        [(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in
                                         [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[
                                      0]).exploded
    except Exception as e:
        print(f'Неверный ip, {e}')
        ip = ''
    print(ip)
    layout_login = [[sg.Push(background_color='white'), sg.Text("Адрес сервера", background_color='white'),
                     sg.Input(default_text="10.1.4.49", key="ip")],
                    [sg.Push(background_color='white'), sg.Text("Пароль", background_color='white'), sg.Input(
                        focus=True,
                        default_text='qwerty',
                        key="password", password_char='*')],
                    [sg.Push(background_color='white'), sg.Ok(key="OK button"), sg.Push(background_color='white')]]
    return sg.Window('Вход на сервер', layout_login, icon=ICON_BASE_64, background_color='white', finalize=True)


def make_add_lic():
    layout_lic = [[sg.Combo(sorted(sg.user_settings_get_entry('-filenames-', [])),
                            default_value=sg.user_settings_get_entry('-last filename-', ''), size=(50, 1),
                            key='-FILENAME-'), sg.FileBrowse('Найти')],
                  [sg.Button('Получить id сервера'), sg.Push(), sg.Button('Загрузить', bind_return_key=True)],
                  [sg.Frame('Лицензия',
                            [[sg.Table(['', '', ''], headings=['Наименование', 'Количество', 'Дата '],
                                       justification="left",
                                       # num_rows=40,
                                       # enable_events=True,
                                       # enable_click_events=True,
                                       # right_click_selects=True,
                                       # right_click_menu=[1, 'Изменить группу'],
                                       select_mode=sg.TABLE_SELECT_MODE_NONE,
                                       # selected_row_colors='red on gray',
                                       # visible_column_map=[False, True, True, True],
                                       # key='-groups2-', expand_y=True, expand_x=True,
                                       # auto_size_columns=False, col_widths=[0, 10, 30, 2])], ],
                                       # expand_x=True,
                                       # size=(480, 564)
                                       )
                              ]])],
                  [sg.Push(), sg.Button('Выйти'), sg.Push()]]
    return sg.Window('Лицензия', layout_lic, icon=ICON_BASE_64, background_color='white', finalize=True)


def make_settings():
    layout_settings = [
        [sg.Frame('Общие настройки',
                  [
                      [sg.Push(), sg.Checkbox('Запрет индивидуальных вызовов', default=False, enable_events=True,
                               key='-запрет-инд-')]
                  ]
                  , expand_x=True)
        ],
        # [sg.Text('Общие настройки')],
        # [sg.Push(), sg.Checkbox('Запрет индивидуальных вызовов', default=False, enable_events=True,
        #                        key='-запрет-инд-')],
        [sg.Push()],
        [sg.Frame('Настройка портов',
                  [
                      [sg.Push(), sg.Text('Порт подключения'), sg.Input(size=20, key='-порт-подкл-', enable_events=True)],
                      [sg.Push(), sg.Text('Порты аудио'), sg.Input(size=20, key='-Аудио-порты-', enable_events=True)]
                  ], expand_x=True)
        ],
        [sg.Push()],
        [sg.Frame('Таймауты',
                  [
                      [sg.Push(), sg.Text('Групповой вызов (сек)'), sg.Input(size=20,
                                                                             key='-Групповой-таймаут-',
                                                                             enable_events=True)],
                      [sg.Push(), sg.Text('Индивидуальный вызов (сек)'), sg.Input(size=20,
                                                                                  key='-Индивидуальный-таймаут-',
                                                                                  enable_events=True)],
                      [sg.Push(), sg.Text('Диспетчерский вызов (сек)'), sg.Input(size=20,
                                                                                  key='-Диспетчерский-таймаут-',
                                                                                  enable_events=True)]
                  ], expand_x=True)
        ],
        [sg.ProgressBar(max_value=10, orientation='horizontal', key='-Progress-Bar-',
                        # visible=False,
                        # expand_x=True,
                        # expand_y=True,
                        size_px=(300, 10),
                        pad=((30, 30),(30, 10))
                        )],
        [sg.Push(), sg.Button('OK', key='-OK-set-'), sg.Button('Выйти', key='-Exit-set-'), sg.Push()]
    ]
    return sg.Window('Настройки', layout_settings, icon=ICON_BASE_64, background_color='white',
                     modal=True,
                     # size=(500, 400),
                     finalize=True)


def make_apply_set():
    layout_apply = [
        [sg.ProgressBar(max_value=10, orientation='horizontal', key='-Progress-Bar-')],
        [sg.Push(), sg.Button('OK', disabled=True), sg.Button('Отменить'), sg.Push()]
    ]
    return sg.Window('Применение настроек на сервере', layout_apply, icon=ICON_BASE_64, background_color='white',
                     modal=True,
                     finalize=True)
def make_get_id(id):
    layout_get_id = [[sg.InputText(id, key='-id-'), sg.Button('Скопировать', key='-Скопировать-')],
                     [sg.Push(), sg.Button('OK'), sg.Push()]]
    return sg.Window('id сервера', layout_get_id, icon=ICON_BASE_64, background_color='white', modal=True,
                     finalize=True)


def make_add_user_window():
    layout_add_user = [
        [sg.Push(), sg.Text('Логин'), sg.Input(key='UserLogin')],
        [sg.Push(), sg.Text('Имя'), sg.Input(key='UserName')],
        [sg.Push(), sg.Text('Пароль'), sg.Input(key='userPassword', password_char='*')],
        [sg.Push(), sg.Text('Показать пароль', key='showPasswordText'), sg.Button(key='showPassword',
                                                                                  button_color='#ffffff',
                                                                                  image_data=ICON_SHOW_BASE_64)],
        [sg.Checkbox('Диспетчер', default=False, key='addUserDispatcher'), sg.Push()],
        [sg.Push(), sg.Ok(button_text='Создать', key='addUserButton')]
    ]
    return sg.Window('Добавить пользователя', layout_add_user, icon=ICON_BASE_64, use_ttk_buttons=True,
                     finalize=True, modal=True)


def make_modify_user_window(user: dict):
    layout_modify_user = [
            [sg.Text('Логин', size=(13)), sg.Input(disabled=True, default_text=user['login'], key='UserModifyLogin')],
            [sg.Text('Имя', size=(13)), sg.Input(default_text=user['name'], enable_events=True, key='UserModifyName')],
            [sg.Text('Пароль', size=(13)), sg.Input(default_text='', enable_events=True,
                                                    key='userModifyPassword', password_char='*')],
            [sg.Push(), sg.Text('Показать пароль', key='showModifyPasswordText'),
             sg.Button(key='showModifyPassword',
                       button_color='#ffffff',
                       image_data=ICON_SHOW_BASE_64)],
            [sg.Text('Таймаут (сек)', size=(13)), sg.Input(size=(10), enable_events=True, key='userTimeout')],
            [sg.Checkbox('Диспетчер',
                         default=user['is_dispatcher'],
                         enable_events=True,
                         key='modifyUserDispatcher'), sg.Push()],
            [sg.Push()],
            [sg.Checkbox('Заблокирован',
                         default=user['is_blocked'],
                         enable_events=True,
                         key='modifyUserBlock'), sg.Push()],
            [sg.Push(), sg.Ok(button_text='Изменить', key='modifyUserButton')]
        ]
    win = sg.Window('Изменить пользователя', layout_modify_user, icon=ICON_BASE_64, use_ttk_buttons=True,
                     finalize=True, modal=True)
    return win


def make_modify_group_window(group: dict):
    layout_modify_group = [
        [sg.Push(), sg.Text('Имя Группы'),
         sg.Input(size=(40, 1), default_text=group['name'], key='GroupModifyName')],
        [sg.Push(), sg.Text('Описание Группы'),
         sg.Multiline(enter_submits=True, no_scrollbar=True, size=(40, 3), default_text=group['desc'],
                      key='GroupModifyDesc')],
        [sg.Push(), sg.Checkbox('Экстренная', default=group['is_emergency'], key='GroupModifyEmergency')],
        [sg.Push(), sg.Ok(button_text='Изменить', key='modifyGroupButton')]
    ]
    win = sg.Window('Изменить группу', layout_modify_group, icon=ICON_BASE_64, use_ttk_buttons=True,
                     finalize=True, modal=True)
    return win


def make_del_user_window(user):
    delete_text = 'Вы уверены, что хотите удалить пользователя ' + user + '?'
    layout_del_user = [
        [sg.Text(delete_text)],
        [sg.Button('Да', key="okDel"), sg.Button('Нет', key='noDel')]
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
        [sg.Push(), sg.Text('Показать пароль', key='showClonePasswordText'),
         sg.Button(key='showPasswordCloneUser',
                   button_color='#ffffff',
                   image_data=ICON_SHOW_BASE_64)],
        [sg.Push(), sg.Ok(button_text='Клонировать', key='cloneUserButton')]
    ]
    return sg.Window('Клонировать пользователя', layout_clone_user, icon=ICON_BASE_64, use_ttk_buttons=True,
                     finalize=True, modal=True)


def make_add_group_window():
    layout_add_group = [
        [sg.Push(), sg.Text('Имя Группы'), sg.Input(size=(40, 1), key='GroupName')],
        [sg.Push(), sg.Text('Описание Группы'),
         sg.Multiline(enter_submits=True, no_scrollbar=True, size=(40, 3), key='description')],
        [sg.Push(), sg.Checkbox('Экстренная', key='emergency')],
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
    sleep(10)
    num = 0
    # print('Запускаем поток')
    while True:
        res_ping = ''
        change_state = False
        print(f' Thread {num} - {server_status}')
        try:
            res_ping = requests.get(ip, timeout=3)
        except Exception as e:
            print(f'Сервер не доступен {e}')
        if res_ping == '':
            if server_status['last_state']:
                logging.info(f'[{num}] Сервер НЕ доступен ')
                change_state = True
                # server_status['last_state'] = False
            # server_status['run'] = False
            # logging.error(f'[{num}] Сервер не доступен')
            # print('Сервер не доступен')
            default_json = json.dumps({"onlineUsersCount": -5, "databaseVersion": 0})
            window.write_event_value('-THREAD-', (threading.currentThread().name, default_json))
        else:
            if res_ping.status_code == 200:
                # print(f'[{num}] Пингуем.. {res_ping.text}')
                if not server_status['last_state']:
                    logging.info(f'[{num}] Сервер доступен ')
                    change_state = True
                window.write_event_value('-THREAD-', (threading.currentThread().name, res_ping.text))
                # server_status['run'] = True
        num += 1
        if change_state:
            with open('admin.log', mode='r', encoding='cp1251') as log_f:
                s = log_f.read()
                s = s.rstrip('\n')
                journal_list = s.split('\n')
                # filtered_journal = []
                filtered_journal = filter_journal(journal_list)
                if filter_status_journal:
                    filtered_journal = list(filter(lambda x: search_str in x, filtered_journal))
                output_text = "\n".join(filtered_journal)
                window['journal'].update(output_text)
                window['countLogs'].update(len(filtered_journal))
        sleep(50)


def check_server(url_ping):
    status = {'last_state': False, 'run': False, 'online': '', 'db': ''}
    res_ping = ''
    try:
        res_ping = requests.get(url_ping, timeout=3)
    except Exception as e:
        print(f"Ошибка подключения. {e}")
    if res_ping == '':
        print('Сервер не отвечает')
        logging.info(f'Сервер НЕ доступен при запуске приложения')
        # status['last_state'] = False
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
            status['last_state'] = True
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
                if filter_journal_critical:
                    return list(
                        filter(lambda x: 'INFO' in x or 'CRITICAL' in x or 'ERROR' in x or 'WARNING' in x, journal))
                else:
                    return list(filter(lambda x: 'INFO' in x or 'ERROR' in x or 'WARNING' in x, journal))
            elif filter_journal_critical:
                return list(filter(lambda x: 'INFO' in x or 'CRITICAL' in x or 'WARNING' in x, journal))
            return list(filter(lambda x: 'INFO' in x or 'WARNING' in x, journal))
        elif filter_journal_error:
            if filter_journal_critical:
                return list(filter(lambda x: 'INFO' in x or 'CRITICAL' in x or 'ERROR' in x, journal))
            else:
                return list(filter(lambda x: 'INFO' in x or 'ERROR' in x, journal))
        elif filter_journal_critical:
            return list(filter(lambda x: 'INFO' in x or 'CRITICAL' in x, journal))
        else:
            return list(filter(lambda x: 'INFO' in x, journal))
    elif filter_journal_warning:
        if filter_journal_error:
            if filter_journal_critical:
                return list(filter(lambda x: 'CRITICAL' in x or 'ERROR' in x or 'WARNING' in x, journal))
            else:
                return list(filter(lambda x: 'ERROR' in x or 'WARNING' in x, journal))
        elif filter_journal_critical:
            return list(filter(lambda x: 'CRITICAL' in x or 'WARNING' in x, journal))
        else:
            return list(filter(lambda x: 'WARNING' in x, journal))
    elif filter_journal_error:
        if filter_journal_critical:
            return list(filter(lambda x: 'CRITICAL' in x or 'ERROR' in x, journal))
        else:
            return list(filter(lambda x: 'ERROR' in x, journal))
    elif filter_journal_critical:
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


def check_os():
    running_os = os.name
    running_platform = platform.system()
    print(running_os)
    print(running_platform)
    return running_platform


def get_id(os):
    if os == 'Windows':
        command = 'reg query HKLM\Software\Microsoft\Cryptography /v MachineGuid'
        # command = 'DIR'
        # proc = subprocess.Popen(command,
        #                         shell=True,
        #                         stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output_list = str(subprocess.getoutput(command)).split()
        system_id = output_list[-1]
        # print(output[-1])
    else:
        system_id = 'smth Linux'
    return system_id


# def create_menu():
#     menu_tray = (item('Выйти', exit_app), item('Отобразить окно', show_app), item('Скрыть окно', hide_app))
#     return menu_tray

# def exit_app(icon, item):
#     # print('exit')
#     global break_flag
#     break_flag = True
#     window_exit = make_exit_window()
#     while True:
#         ev_exit, val_exit = window_exit.Read()
#         # print(ev_exit, val_exit)
#         if ev_exit == 'okExit':
#             logging.info('Панель администратора остановлена')
#             logging.info('Стоп лога')
#             window_exit.close()
#             icon.stop()
#             global break_flag2
#             break_flag2 = True
#             break
#         if ev_exit == sg.WIN_CLOSED or ev_exit == 'Exit':
#             # print('Закрыл окно выхода')
#             break
#         if ev_exit == 'noExit':
#             # print('Закрыл окно выхода')
#             window_exit.close()
#             break


def show_app(icon):
    # print('show')
    window.un_hide()
    icon.stop()
    # print('show2')


# def hide_app():
#     print('hide')

def get_user_list(users_from_db):
    treedata_update_user = sg.TreeData()
    user_list = []

    for index, user_from_db in enumerate(users_from_db):
        user_list.append([user_from_db['id'], user_from_db['login'], user_from_db['name']])
        if user_from_db['is_dispatcher']:
            user_list[index].append(u'\u2713')
        else:
            user_list[index].append('')
        if user_from_db['is_blocked']:
            user_list[index].append(u'\u274c')
        else:
            user_list[index].append('')
        treedata_update_user.insert('', user_from_db['id'], '',
                                    values=[user_from_db['login'],
                                            user_from_db['name']],
                                    icon=check[0])
    return user_list, treedata_update_user


def get_filter_user_list(filter_users_from_db):
    user_list = []
    for user_from_db in filter_users_from_db:
        if user_from_db['is_dispatcher']:
            user_list.append([user_from_db['id'], user_from_db['login'],
                              user_from_db['name'], u'\u2713'])
        else:
            user_list.append([user_from_db['id'], user_from_db['login'],
                              user_from_db['name'], ''])
    return user_list


def block_user(user_id, blocked):
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    db_update_user = "UPDATE Users SET is_blocked=" + (str(1) if blocked else str(0)) + " WHERE id='" + user_id + "'"
    cur.execute(db_update_user)
    con.commit()
    con.close()


if __name__ == '__main__':
    # print(sg.theme_global())
    # print(sg.theme_list())
    # get_icon()
    # sg.theme_global('GreenTan')
    # sg.theme_global('SystemDefaultForReal')
    # sg.theme_global('SystemDefault1')
    # vers = sys.version_info
    # print(vers)
    omega_theme = {'BACKGROUND': '#ffffff',
                   'TEXT': '#000000',
                   'INPUT': '#f2f2f2',
                   'TEXT_INPUT': '#000000',
                   'SCROLL': '#bfbfbf',
                   'BUTTON': ('white', '#35536b'),
                   'PROGRESS': ('#01826B', '#D0D0D0'),
                   'BORDER': 1,
                   'SLIDER_DEPTH': 0,
                   'PROGRESS_DEPTH': 0}
    button_color_2 = '#a6674c'
    sg.theme_add_new('OmegaTheme', omega_theme)
    sg.theme('OmegaTheme')
    if sys.version_info[1] < 9:
        logging.basicConfig(filename='admin.log', filemode='a', format='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)
    else:
        logging.basicConfig(filename='admin.log', filemode='a', format='%(asctime)s %(levelname)s %(message)s',
                            encoding='cp1251', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)
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
                            HEADER_dict = {'Authorization': "Bearer " + TOKEN}
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
                                treedata.insert('', group['id'], '', values=[group['name'], group['desc']],
                                                icon=check[0])
                            for user in users_from_db:
                                treedata2.insert('', user['id'], '', values=[user['login'], user['name']],
                                                 icon=check[0])
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
                        # tree.Widget.heading("#0", text='id')
                        tree2 = window['-TREE2-']
                        # tree2.Widget.heading("#0", text='id')
                        if server_status['run']:
                            bar_text = 'Пользователей онлайн: обновление..' + ', Версия БД: ' + str(server_status['db'])
                            window['-StatusBar-'].update(bar_text, background_color='#699349')
                        else:
                            window['-StatusBar-'].update('Сервер не доступен', background_color='red')
                        thread_started = False
                        filter_status = False
                        filter_status_group = False
                        filter_status_journal = False
                        filter_journal_info = True
                        filter_journal_warning = True
                        filter_journal_error = True
                        filter_journal_critical = True
                        while True:
                            if break_flag2:
                                break
                            if server_status['run']:
                                window['-Start-'].update(disabled=True)
                            else:
                                window['-Stop-'].update(disabled=True)
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
                                    if not server_status['run']:
                                        update_text = 'Пользователей онлайн: обновление..' + ', Версия БД: ' + \
                                                      str(dict_online["databaseVersion"])
                                        window['-StatusBar-'].update(update_text, background_color='#699349')
                                    else:
                                        update_text = 'Пользователей онлайн: ' + str(dict_online["onlineUsersCount"]) \
                                                      + ', Версия БД: ' + str(dict_online["databaseVersion"])
                                        window['-StatusBar-'].update(update_text, background_color='#699349')
                                    window['-Start-'].update(disabled=True)
                                    window['-Stop-'].update(disabled=False)
                                    if not server_status['run']:
                                        TOKEN = get_token(BASE_URL_AUTH)
                                        HEADER_dict = {'Authorization': "Bearer " + TOKEN}
                                        # print(TOKEN)
                                        # print(HEADER_dict)
                                        init_db()
                                        users_from_db = get_users_from_db()
                                        groups_from_db = get_groups_from_db()
                                        users_from_db.sort(key=lambda i: i['login'])
                                        groups_from_db.sort(key=lambda i: i['name'])
                                        # treedata_update_user = sg.TreeData()
                                        treedata_update_group = sg.TreeData()
                                        # user_list = list()
                                        group_list = list()
                                        if users_from_db != [[]] and groups_from_db != [[]]:
                                            user_list, treedata_update_user = get_user_list(users_from_db)
                                            for group_from_db in groups_from_db:
                                                group_list.append([group_from_db['id'], group_from_db['name'],
                                                                   group_from_db['desc']])
                                        for group in groups_from_db:
                                            treedata_update_group.insert('', group['id'], '',
                                                                         values=[group['name'], group['desc']],
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
                                    if not server_status['last_state']:
                                        server_status['last_state'] = True
                                    # server_status['run'] = True
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
                                    if server_status['last_state']:
                                        server_status['last_state'] = False
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
                                # sg.popup("Приложение свёрнуто!\nОкно закроется через 10 секунд", title='Инфо',
                                # icon=ICON_BASE_64,
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
                                        window['-checkAllGroups-'].update(disabled=False)
                                        window['-checkAllGroups-'].update(False)
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
                                    # print(values['-groups2-'])
                                    if event[2][0] is None:
                                        pass
                                    else:
                                        if filter_status_group:
                                            group_id = filtered_groups_list_of_dict[event[2][0]]['id']
                                        else:
                                            group_id = groups_from_db[event[2][0]]['id']
                                        # group_id = groups_from_db[event[2][0]]['id']
                                        window['Apply2'].update(disabled=True)
                                        window['-checkAllUsers-'].update(disabled=False)
                                        window['-checkAllUsers-'].update(False)
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
                                if not values['-users-']:
                                    sg.popup('Не выбран пользователь', title='Инфо', icon=ICON_BASE_64,
                                             no_titlebar=True, background_color='lightgray')
                                else:
                                    if filter_status:
                                        user_to_change = filtered_users_list_of_dict[values['-users-'][0]]
                                    else:
                                        user_to_change = users_from_db[values['-users-'][0]]
                                    window_modify_user = make_modify_user_window(user_to_change)
                                    window_modify_user.Element('UserModifyLogin').SetFocus()
                                    password_clear = False
                                    while True:
                                        ev_modify_user, val_modify_user = window_modify_user.Read()
                                        print(ev_modify_user, val_modify_user)
                                        # cur_val = val_modify_user.copy()
                                        # print(f'cur_val = {cur_val}')
                                        if ev_modify_user == sg.WIN_CLOSED or ev_modify_user == 'Exit':
                                            # print('Закрыл окно добавления пользователя')
                                            break
                                        elif ev_modify_user == 'showModifyPassword':
                                            if password_clear:
                                                window_modify_user['userModifyPassword'].update(password_char='*')
                                                window_modify_user['showModifyPasswordText'].update("Показать пароль")
                                                window_modify_user['showModifyPassword'].update(
                                                    image_data=ICON_SHOW_BASE_64)
                                                password_clear = False
                                            else:
                                                window_modify_user['userModifyPassword'].update(password_char='')
                                                window_modify_user['showModifyPasswordText'].update("Скрыть пароль")
                                                window_modify_user['showModifyPassword'].update(
                                                    image_data=ICON_HIDE_BASE_64)
                                                password_clear = True
                                        elif ev_modify_user == 'modifyUserButton':
                                            modify_user_login, \
                                                modify_user_name, \
                                                modify_user_password, \
                                                modify_user_timeout, \
                                                modify_user_is_disp, \
                                                modify_user_is_blocked = val_modify_user.values()
                                            modify_user_dict = {}
                                            modify_name = False
                                            modify_password = False
                                            modify_is_disp = False
                                            modify_is_blocked = False
                                            modify_user_dict['id'] = user_to_change['id']
                                            modify_user_dict['login'] = modify_user_login
                                            if modify_user_name != user_to_change['name']:
                                                modify_user_dict['displayName'] = modify_user_name
                                                modify_name = True
                                            if modify_user_password:
                                                modify_user_dict['password'] = modify_user_password
                                                modify_password = True
                                            if modify_user_is_disp != user_to_change['is_dispatcher']:
                                                modify_is_disp = True
                                                user_disp_dict = {'id': user_to_change['id']}
                                                if modify_user_is_disp:
                                                    res_modify_user_is_disp = requests.post(BASE_URL +
                                                                                            'addToDispatchers',
                                                                                            json=user_disp_dict,
                                                                                            headers=HEADER_dict)
                                                else:
                                                    res_modify_user_is_disp = requests.post(BASE_URL +
                                                                                            'removeFromDispatchers',
                                                                                            json=user_disp_dict,
                                                                                            headers=HEADER_dict)
                                                if res_modify_user_is_disp.status_code == 200:
                                                    if modify_user_is_disp:
                                                        logging.info(f'Пользователь {modify_user_login} '
                                                                     f'стал диспетчером')
                                                    else:
                                                        logging.info(f'Пользователь {modify_user_login} '
                                                                     f'перестал быть диспетчером')
                                                else:
                                                    if modify_user_is_disp:
                                                        logging.error(
                                                            f'Ошибка при добавлении пользователя в диспетчеры - '
                                                            f'{res_modify_user_is_disp.status_code}')
                                                    else:
                                                        logging.error(
                                                            f'Ошибка при удалении пользователя из диспетчеров - '
                                                            f'{res_modify_user_is_disp.status_code}')
                                            if modify_user_is_blocked != user_to_change['is_blocked']:
                                                modify_is_blocked = True
                                                user_block_dict = {'id': user_to_change['id']}
                                                block_user(user_to_change['id'], modify_user_is_blocked)
                                                users_from_db = get_users_from_db()
                                                users_from_db.sort(key=lambda i: i['login'])
                                                user_list, treedata_update_user = get_user_list(users_from_db)
                                                if filter_status:
                                                    search_str = values['-filterUser-']
                                                    filtered_users = filter(lambda x: search_str in x['login'],
                                                                            users_from_db)
                                                    filtered_users_list_of_dict = list(filtered_users)
                                                    filtered_users_list = get_filter_user_list(
                                                        filtered_users_list_of_dict)
                                                    window['-users-'].update(filtered_users_list)
                                                else:
                                                    window['-users-'].update(user_list)
                                                window['-TREE2-'].update(treedata_update_user)
                                                # window_modify_user.close()
                                                # sg.popup("Пользователь изменён!", title='Инфо', icon=ICON_BASE_64,
                                                #          no_titlebar=True, background_color='lightgray')
                                                # if modify_user_is_blocked:
                                                #     res_modify_user_is_blocked = requests.post(BASE_URL +
                                                #                                             'addToBlock',
                                                #                                             json=user_block_dict,
                                                #                                             headers=HEADER_dict)
                                                # else:
                                                #     res_modify_user_is_blocked = requests.post(BASE_URL +
                                                #                                             'removeFromBlock',
                                                #                                             json=user_block_dict,
                                                #                                             headers=HEADER_dict)
                                                # if res_modify_user_is_blocked.status_code == 200:
                                                #     if modify_user_is_blocked:
                                                #         logging.info(f'Пользователь {modify_user_login} '
                                                #                      f'ЗАБЛОКИРОВАН')
                                                #     else:
                                                #         logging.info(f'Пользователь {modify_user_login} '
                                                #                      f'РАЗБЛОКИРОВАН')
                                                # else:
                                                #     if modify_user_is_blocked:
                                                #         logging.error(
                                                #             f'Ошибка при блокировании пользователя - '
                                                #             f'{res_modify_user_is_blocked.status_code}')
                                                #     else:
                                                #         logging.error(
                                                #             f'Ошибка при разблокировании пользователя - '
                                                #             f'{res_modify_user_is_blocked.status_code}')
                                            if modify_name or modify_password:
                                                res_modify_user = requests.post(BASE_URL + 'updateUser',
                                                                                json=modify_user_dict,
                                                                                headers=HEADER_dict)
                                                # sg.cprint(f'Изменяем пользователя - {res_modify_user.status_code}')
                                                if res_modify_user.status_code == 200:
                                                    if modify_name:
                                                        logging.info(f'Пользователю {modify_user_login} изменили имя')
                                                    if modify_password:
                                                        logging.info(f'Пользователю {modify_user_login} '
                                                                     f'изменили пароль')
                                                else:
                                                    logging.error(f'Ошибка изменения пользователя - '
                                                                  f'{res_modify_user.status_code}')
                                            if modify_is_disp or modify_name or modify_password or modify_is_blocked:
                                                # users_from_server = get_users_from_server()
                                                # add_users(users_from_server)
                                                # users_from_db = get_users_from_db()
                                                # users_from_db.sort(key=lambda i: i['login'])
                                                # # user_list = list()
                                                # drop_db('user_in_groups')
                                                # add_user_in_groups(users_from_server)
                                                # user_list, treedata_update_user = get_user_list(users_from_db)
                                                # if filter_status:
                                                #     search_str = values['-filterUser-']
                                                #     filtered_users = filter(lambda x: search_str in x['login'],
                                                #                             users_from_db)
                                                #     filtered_users_list_of_dict = list(filtered_users)
                                                #     filtered_users_list = get_filter_user_list(
                                                #         filtered_users_list_of_dict)
                                                #     window['-users-'].update(filtered_users_list)
                                                # else:
                                                #     window['-users-'].update(user_list)
                                                # window['-TREE2-'].update(treedata_update_user)
                                                window_modify_user.close()
                                                sg.popup("Пользователь изменён!", title='Инфо', icon=ICON_BASE_64,
                                                         no_titlebar=True, background_color='lightgray')
                                            else:
                                                sg.popup("Нет никаких изменений!", title='Инфо', icon=ICON_BASE_64,
                                                         no_titlebar=True, background_color='lightgray')
                                        else:
                                            # print(f'after cur_val = {cur_val}')
                                            # print(f'after val_modify_user'
                                            #       f' = {val_modify_user}')
                                            # if val_modify_user != cur_val:
                                                window_modify_user['modifyUserButton'].update(button_color=button_color_2)
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
                                        modify_group_emergency = int(val_modify_group['GroupModifyEmergency'])
                                        modify_group_dict = {}
                                        modify_group = False
                                        modify_group_dict['id'] = group_to_change['id']
                                        if modify_group_name != group_to_change['name']:
                                            modify_group_dict['name'] = modify_group_name
                                            modify_group = True
                                        if modify_group_desc != group_to_change['desc']:
                                            modify_group_dict['description'] = modify_group_desc
                                            modify_group = True
                                        if modify_group_emergency != group_to_change['is_emergency']:
                                            modify_group_dict['groupType'] = modify_group_emergency
                                            modify_group = True
                                        else:
                                            modify_group_dict['groupType'] = group_to_change['is_emergency']
                                        if modify_group:
                                            # print(modify_group_dict)
                                            res_modify_group = requests.post(BASE_URL + 'updateGroup',
                                                                             json=modify_group_dict,
                                                                             headers=HEADER_dict)
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
                                                                                 values=[group_from_db['name'],
                                                                                         group_from_db['desc']],
                                                                                 icon=check[0])
                                                window['-groups2-'].update(group_list)
                                                window['-TREE-'].update(treedata_update_group)
                                                window_modify_group.close()
                                                sg.popup("Группа изменена!", title='Инфо', icon=ICON_BASE_64,
                                                         no_titlebar=True, background_color='lightgray')
                                                break
                                            else:
                                                logging.error(f'ошибка изменения группы - '
                                                              f'{res_modify_group.status_code}')
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
                                window['Apply'].SetFocus()
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
                                window['Apply2'].SetFocus()
                            if event == "Apply":
                                # print("clicked Apply")
                                if not values['-users-']:
                                    print(f"Не выбран пользователь")
                                    sg.popup('Не выбран пользователь', title='Инфо', icon=ICON_BASE_64,
                                             no_titlebar=True, background_color='lightgray')
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
                                    add_del_dict = {'UserIds': [chosen_login['id']], 'addGroupIds': [],
                                                    'removeGroupIds': []}
                                    add_dict = {'UserIds': [chosen_login['id']], 'GroupIds': []}
                                    del_dict = {'UserIds': [chosen_login['id']], 'GroupIds': []}
                                    for gr_id in tree.metadata:
                                        if gr_id in current_groups_ids:
                                            print(f"Пользователь уже в группе {get_group_name_by_id_from_db(gr_id)}")
                                        else:
                                            print(f"Пользователя нужно добавить в группу "
                                                  f"{get_group_name_by_id_from_db(gr_id)}")
                                            add_dict['GroupIds'] += [gr_id]
                                            add_del_dict['addGroupIds'] += [gr_id]
                                            add_group = True
                                    for gr_id in current_groups_ids:
                                        if gr_id in tree.metadata:
                                            print(f'Пользователь уже в группе {get_group_name_by_id_from_db(gr_id)}')
                                        else:
                                            print(f"У пользователя нужно удалить группу "
                                                  f"{get_group_name_by_id_from_db(gr_id)}")
                                            del_dict['GroupIds'] += [gr_id]
                                            add_del_dict['removeGroupIds'] += [gr_id]
                                            del_group = True
                                    if add_group and del_group:
                                        print(add_del_dict)
                                        res_add_del = requests.post(BASE_URL + 'changeUserGroups', json=add_del_dict,
                                                                    headers=HEADER_dict)
                                        print(res_add_del.status_code)
                                        if res_add_del.status_code == 200:
                                            logging.info(f'Добавление и удаление групп выполнено для '
                                                         f'{chosen_login["name"]}')
                                            add_del_groups_to_user_after_apply(add_del_dict)
                                        else:
                                            logging.error(f'Добавление групп НЕ выполнено для {chosen_login["name"]}')
                                            sg.popup("Добавление не выполнено", title='Инфо', icon=ICON_BASE_64,
                                                     no_titlebar=True, background_color='lightgray')
                                    elif add_group:
                                        print(add_del_dict)
                                        res_add = requests.post(BASE_URL + 'changeUserGroups',
                                                                json=add_del_dict, headers=HEADER_dict)
                                        print(res_add.status_code)
                                        if res_add.status_code == 200:
                                            logging.info(f'Добавление групп выполнено для {chosen_login["name"]}')
                                            add_del_groups_to_user_after_apply(add_del_dict)
                                        else:
                                            logging.error(f'Добавление групп НЕ выполнено для {chosen_login["name"]}')
                                            sg.popup("Добавление не выполнено", title='Инфо',
                                                     icon=ICON_BASE_64, no_titlebar=True, background_color='lightgray')
                                    elif del_group:
                                        print(add_del_dict)
                                        res_del = requests.post(BASE_URL + 'changeUserGroups', json=add_del_dict,
                                                                headers=HEADER_dict)
                                        print(res_del.status_code)
                                        if res_del.status_code == 200:
                                            logging.info(f'Удаление групп выполнено для {chosen_login["name"]}')
                                            add_del_groups_to_user_after_apply(add_del_dict)
                                        else:
                                            logging.error(f'Удаление групп НЕ выполнено для {chosen_login["name"]}')
                                            sg.popup("Удаление не выполнено", title='Инфо', icon=ICON_BASE_64,
                                                     no_titlebar=True, background_color='lightgray')
                                    if add_group or del_group:
                                        add_del_text = 'Изменение групп для ' + chosen_login['name'] + ' выполнено'
                                        # logging.info(f'Добавление групп НЕ выполнено для {chosen_login["name"]}')
                                        sg.popup(add_del_text, title='Инфо', icon=ICON_BASE_64, no_titlebar=True,
                                                 background_color='lightgray')
                                        window['Apply'].update(disabled=True)
                                    else:
                                        # logging.error(f'')
                                        sg.popup('Нет изменений', title='Инфо', icon=ICON_BASE_64, no_titlebar=True,
                                                 background_color='lightgray')
                            if event == "Apply2":
                                # print("clicked Apply2")
                                if not values['-groups2-']:
                                    # print(f"Не выбрана группа")
                                    sg.popup('Не выбрана группа', title='Инфо', icon=ICON_BASE_64, no_titlebar=True,
                                             background_color='lightgray')
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
                                    add_del_dict = {'GroupIds': [chosen_group['id']], 'addUserIds': [],
                                                    'removeUserIds': []}
                                    for us_id in tree2.metadata:
                                        if us_id in current_users_ids:
                                            print(f"В группе {chosen_group['name']} уже есть "
                                                  f"{get_user_name_by_id_from_db(us_id)}")
                                        else:
                                            print(f"Пользователя {get_user_name_by_id_from_db(us_id)} "
                                                  f"нужно добавить в группу {chosen_group['name']}")
                                            add_dict['UserIds'] += [us_id]
                                            add_del_dict['addUserIds'] += [us_id]
                                            add_user = True
                                    for us_id in current_users_ids:
                                        if us_id in tree2.metadata:
                                            print(f'Пользователь {get_user_name_by_id_from_db(us_id)} уже в группе '
                                                  f'{chosen_group["name"]}')
                                        else:
                                            print(f"В группе {chosen_group['name']} нужно удалить пользователя "
                                                  f"{get_user_name_by_id_from_db(us_id)}")
                                            del_dict['UserIds'] += [us_id]
                                            add_del_dict['removeUserIds'] += [us_id]
                                            del_user = True
                                    print(add_del_dict)
                                    if add_user and del_user:
                                        res_add_del = requests.post(BASE_URL + 'changeGroupUsers', json=add_del_dict,
                                                                    headers=HEADER_dict)
                                        print(res_add_del.status_code)
                                        if res_add_del.status_code == 200:
                                            logging.info(
                                                f'Изменение пользователей выполнено для {chosen_group["name"]}')
                                            # window['-users2-'].update(get_users_for_group(chosen_group[1]))
                                            add_del_users_to_group_after_apply(add_del_dict)
                                        else:
                                            logging.error(
                                                f'Изменение пользователей НЕ выполнено для {chosen_group["name"]} - '
                                                f'{res_add_del.status_code}')
                                            sg.popup("Добавление не выполнено", title='Инфо', icon=ICON_BASE_64,
                                                     no_titlebar=True, background_color='lightgray')
                                    elif add_user:
                                        res_add = requests.post(BASE_URL + 'changeGroupUsers', json=add_del_dict,
                                                                headers=HEADER_dict)
                                        # print(res_add.status_code)
                                        if res_add.status_code == 200:
                                            logging.info(f'Добавление пользователей выполнено для '
                                                         f'{chosen_group["name"]}')
                                            # window['-users2-'].update(get_users_for_group(chosen_group[1]))
                                            add_del_users_to_group_after_apply(add_del_dict)
                                        else:
                                            logging.error(
                                                f'Добавление пользователей НЕ выполнено для {chosen_group["name"]} - '
                                                f'{res_add.status_code}')
                                            sg.popup("Добавление не выполнено", title='Инфо', icon=ICON_BASE_64,
                                                     no_titlebar=True, background_color='lightgray')
                                    elif del_user:
                                        res_del = requests.post(BASE_URL + 'changeGroupUsers', json=add_del_dict,
                                                                headers=HEADER_dict)
                                        # print(res_del.status_code)
                                        if res_del.status_code == 200:
                                            logging.info(
                                                f'Удаление пользователей выполнено для {chosen_group["name"]}')
                                            add_del_users_to_group_after_apply(add_del_dict)
                                        else:
                                            logging.error(
                                                f'Удаление пользователей НЕ выполнено для {chosen_group["name"]} - '
                                                f'{res_del.status_code}')
                                            sg.popup("Удаление не выполнено", title='Инфо', icon=ICON_BASE_64,
                                                     no_titlebar=True, background_color='lightgray')
                                    if add_user or del_user:
                                        add_del_text = 'Изменение пользователей для ' + \
                                                       chosen_group['name'] + ' выполнено'
                                        sg.popup(add_del_text, title='Инфо', icon=ICON_BASE_64, no_titlebar=True,
                                                 background_color='lightgray')
                                        window['Apply2'].update(disabled=True)
                                    else:
                                        sg.popup('Нет изменений', title='Инфо', icon=ICON_BASE_64, no_titlebar=True,
                                                 background_color='lightgray')
                            if event == 'О программе':
                                sg.popup('---------------------Powered by PaShi---------------------',
                                         title='О программе', icon=ICON_BASE_64)
                            if event == 'Установить лицензию...':
                                window_add_lic = make_add_lic()
                                while True:
                                    ev_add_lic, val_add_lic = window_add_lic.Read()
                                    print(f'{ev_add_lic}, {val_add_lic}')
                                    if ev_add_lic == sg.WIN_CLOSED or ev_add_lic == 'Выйти':
                                        # print(f'{ev_add_lic}, {val_add_lic}')
                                        window_add_lic.close()
                                        break
                                    if ev_add_lic == 'Получить id сервера':
                                        # id_serv = 'ajfhlkjdhflkja lakjhga'
                                        id_serv = get_id(check_os())
                                        window_get_id = make_get_id(id_serv)
                                        while True:
                                            ev_get_id, val_get_id = window_get_id.Read()
                                            print(f'{ev_get_id}, {val_get_id}')
                                            if ev_get_id == sg.WIN_CLOSED or ev_get_id == 'OK':
                                                window_get_id.close()
                                                break
                                            if ev_get_id == '-Скопировать-':
                                                sg.clipboard_set(val_get_id['-id-'])
                                        # popup_text = 'id сервера - ' + id_serv
                                        # sg.popup(id_serv,
                                        #          title='id сервера', icon=ICON_BASE_64)
                            if event == 'Настройки':
                                window_settings = make_settings()
                                timeout = 0
                                # counter = 0
                                while True:
                                    ev_set, val_set = window_settings.Read(1000)
                                    print(f'{ev_set}, {val_set}')
                                    if ev_set == sg.WIN_CLOSED or ev_set == '-Exit-set-':
                                        # print(f'{ev_add_lic}, {val_add_lic}')
                                        window_settings.close()
                                        break
                                    elif ev_set == '-запрет-инд-' or ev_set == '-порт-подкл-' \
                                        or ev_set == '-Аудио-порты-':
                                        counter = 0
                                        window_settings['-Progress-Bar-'].update_bar(counter)
                                    elif ev_set == '-OK-set-':
                                        print(f"Порт подключения - {val_set['-порт-подкл-']}\n"
                                              f"Аудио порты - {val_set['-Аудио-порты-']}\n"
                                              f"Запрет инд вызовов - {val_set['-запрет-инд-']}")
                                        # window_settings['-Progress-Bar-'].update(visible=True)
                                        window_settings['-OK-set-'].update(disabled=True)
                                        window_settings['-Exit-set-'].update(disabled=True)
                                        window_settings['-запрет-инд-'].update(disabled=True)
                                        window_settings['-порт-подкл-'].update(disabled=True)
                                        window_settings['-Аудио-порты-'].update(disabled=True)
                                        window_settings.DisableClose = True
                                        counter = 0
                                        while counter < 11:
                                            counter += 1
                                            window_settings['-Progress-Bar-'].update_bar(counter)
                                            sleep(1)
                                        window_settings['-OK-set-'].update(disabled=False)
                                        window_settings['-Exit-set-'].update(disabled=False)
                                        window_settings['-запрет-инд-'].update(disabled=False)
                                        window_settings['-порт-подкл-'].update(disabled=False)
                                        window_settings['-Аудио-порты-'].update(disabled=False)
                                        window_settings.DisableClose = False
                                        # window_apply_settings = make_apply_set()
                                        # counter = 0
                                        # while True:
                                        #     ev_apply, val_app = window_apply_settings.Read()
                                        #     if ev_apply == sg.WIN_CLOSED or ev_apply == 'Выйти':
                                        #         window_apply_settings.close()
                                        #         break
                                        #     if ev_apply == 'Отменить':
                                        #         window_apply_settings.close()
                                        #         window_settings.un_hide()
                                        #         break
                                        #     counter += 1
                                        #     sleep(1)
                                        #     window_apply_settings['-Progress-Bar-'].update_bar(counter)
                                    else:
                                        timeout += 1000
                                        print(f'timeout={timeout}')
                                        # counter += 1
                                        # window_settings['-Progress-Bar-'].update_bar(counter)
                                        # sleep(1)
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
                                            window_add_user['showPassword'].update(image_data=ICON_SHOW_BASE_64)
                                            window_add_user['showPasswordText'].update('Показать пароль')
                                            password_clear = False
                                        else:
                                            window_add_user['userPassword'].update(password_char='')
                                            window_add_user['showPassword'].update(image_data=ICON_HIDE_BASE_64)
                                            window_add_user['showPasswordText'].update('Скрыть пароль')
                                            password_clear = True
                                    if ev_add_user == 'addUserButton':
                                        new_user_login, new_user_name, new_user_password, \
                                            is_dispatcher = val_add_user.values()
                                        add_user_dict = {'login': new_user_login,
                                                         'displayName': new_user_name,
                                                         'password': new_user_password}
                                        # add_user_dict['is_dispatcher'] = is_dispatcher
                                        print(add_user_dict)
                                        res_add_user = requests.post(BASE_URL + 'addUser',
                                                                     json=add_user_dict, headers=HEADER_dict)
                                        # print(res_add_user.status_code)
                                        if res_add_user.status_code == 200:
                                            logging.info(f'Пользователь {new_user_login} добавлен')
                                            if is_dispatcher:
                                                add_to_disp_dict = {'id': res_add_user.text[1:-1]}
                                                res_add_disp = requests.post(BASE_URL + 'addToDispatchers',
                                                                             json=add_to_disp_dict, headers=HEADER_dict)
                                                if res_add_disp.status_code == 200:
                                                    logging.info(f'Пользователь {new_user_login} стал диспетчером')
                                                else:
                                                    logging.error(
                                                        f'Пользователь {new_user_login} НЕ стал диспетчером - '
                                                        f'{res_add_disp.status_code}')
                                                    sg.popup("Пользователь не стал диспетчером!", title='Инфо',
                                                             icon=ICON_BASE_64,
                                                             no_titlebar=True, background_color='lightgray')
                                            add_users(get_users_from_server())
                                            users_from_db = get_users_from_db()
                                            users_from_db.sort(key=lambda i: i['login'])
                                            user_list, treedata_update_user = get_user_list(users_from_db)
                                            if filter_status:
                                                search_str = values['-filterUser-']
                                                # print(search_str)
                                                filtered_users = filter(lambda x: search_str in x['login'],
                                                                        users_from_db)
                                                filtered_users_list_of_dict = list(filtered_users)
                                                # print(filtered_users_list_of_dict)
                                                # print(len(filtered_users_list_of_dict))
                                                # filtered_users_list = list()
                                                filtered_users_list = get_filter_user_list(filtered_users_list_of_dict)
                                                # users_from_db = filtered_users_list_of_dict
                                                # for filtered_user_list_of_dict in filtered_users_list_of_dict:
                                                #     filtered_users_list.append([filtered_user_list_of_dict['id'],
                                                #                                 filtered_user_list_of_dict['login'],
                                                #                                 filtered_user_list_of_dict['name']])
                                                window['-users-'].update(filtered_users_list)
                                            else:
                                                window['-users-'].update(user_list)
                                            window['-TREE2-'].update(treedata_update_user)
                                            window_add_user.close()
                                            sg.popup("Пользователь добавлен!", title='Инфо', icon=ICON_BASE_64,
                                                     no_titlebar=True, background_color='lightgray')
                                            break
                                        else:
                                            logging.error(f'Пользователь {new_user_login} НЕ добавлен - '
                                                          f'{res_add_user.status_code}')
                                            sg.popup("Пользователь не добавлен!", title='Инфо', icon=ICON_BASE_64,
                                                     no_titlebar=True, background_color='lightgray')
                            if event == '-DelUser-':
                                if not values['-users-']:
                                    # print(f"Не выбран пользователь")
                                    sg.popup('Не выбран пользователь', title='Инфо', icon=ICON_BASE_64,
                                             no_titlebar=True, background_color='lightgray')
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
                                                res_del_user = requests.post(BASE_URL + 'deleteUser',
                                                                             json=del_user, headers=HEADER_dict)
                                                # print(res_del_user.status_code)
                                                if res_del_user.status_code == 200:
                                                    logging.info(f'Пользователь {del_user["name"]} удалён')
                                                    drop_db('users')
                                                    add_users(get_users_from_server())
                                                    users_from_db = get_users_from_db()
                                                    users_from_db.sort(key=lambda i: i['login'])
                                                    # user_list = list()
                                                    # treedata_update_user = sg.TreeData()
                                                    user_list, treedata_update_user = get_user_list(users_from_db)
                                                    # for user_from_db in users_from_db:
                                                    #     user_list.append([user_from_db['id'], user_from_db['login'],
                                                    #                       user_from_db['name']])
                                                    #     treedata_update_user.insert('', user_from_db['id'], '',
                                                    #                                 values=[user_from_db['login'],
                                                    #                                         user_from_db['name']],
                                                    #                                 icon=check[0])
                                                    del_users_in_groups_after_delete_user(del_user['id'])
                                                    if filter_status:
                                                        search_str = values['-filterUser-']
                                                        # print(search_str)
                                                        filtered_users = filter(lambda x: search_str in x['login'],
                                                                                users_from_db)
                                                        filtered_users_list_of_dict = list(filtered_users)
                                                        # print(filtered_users_list_of_dict)
                                                        # print(len(filtered_users_list_of_dict))
                                                        # filtered_users_list = list()
                                                        filtered_users_list = get_filter_user_list(
                                                            filtered_users_list_of_dict)
                                                        # users_from_db = filtered_users_list_of_dict
                                                        # for filtered_user_list_of_dict in filtered_users_list_of_dict:
                                                        #     filtered_users_list.append(
                                                        #         [filtered_user_list_of_dict['id'],
                                                        #          filtered_user_list_of_dict['login'],
                                                        #          filtered_user_list_of_dict['name']])
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
                                if not values['-users-']:
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
                                                window_clone_user['showClonePasswordText'].update('Показать пароль')
                                                window_clone_user['showPasswordCloneUser'].update(
                                                    image_data=ICON_SHOW_BASE_64)
                                                password_clear = False
                                            else:
                                                window_clone_user['CloneUserPassword'].update(password_char='')
                                                window_clone_user['showClonePasswordText'].update('Скрыть пароль')
                                                window_clone_user['showPasswordCloneUser'].update(
                                                    image_data=ICON_HIDE_BASE_64)
                                                password_clear = True
                                        if ev_clone_user == 'cloneUserButton':
                                            clone_user_login, clone_user_name, \
                                                clone_user_password = val_clone_user.values()
                                            logging.info(f"Клонируем пользователя {user_clone['login']} с именем "
                                                         f"{clone_user_login}")
                                            clone_user_dict = {'login': clone_user_login,
                                                               'displayName': clone_user_name,
                                                               'password': clone_user_password}
                                            # print(clone_user_dict)
                                            # check_disp(user_clone)
                                            res_clone_user = requests.post(BASE_URL + 'addUser', json=clone_user_dict,
                                                                           headers=HEADER_dict)
                                            # print(res_clone_user.status_code)
                                            # print(res_clone_user.text)
                                            if res_clone_user.status_code == 200:
                                                logging.info(f'Новый пользователь {clone_user_login} создан')
                                                if user_clone['is_dispatcher']:
                                                    add_to_disp_dict = {'id': res_clone_user.text[1:-1]}
                                                    res_add_disp = requests.post(BASE_URL + 'addToDispatchers',
                                                                                 json=add_to_disp_dict,
                                                                                 headers=HEADER_dict)
                                                    if res_add_disp.status_code == 200:
                                                        logging.info(
                                                            f'Пользователь {clone_user_login} стал диспетчером')
                                                    else:
                                                        logging.error(
                                                            f'Пользователь {clone_user_login} НЕ стал диспетчером - '
                                                            f'{res_add_disp.status_code}')
                                                        sg.popup("Пользователь не стал диспетчером!", title='Инфо',
                                                                 icon=ICON_BASE_64,
                                                                 no_titlebar=True, background_color='lightgray')
                                                original_groups = get_groups_for_user_from_db(user_clone['id'])
                                                original_groups_ids = []
                                                for or_gr in original_groups:
                                                    original_groups_ids.append(or_gr['id'])
                                                user_from_server = res_clone_user.text[1:-1]
                                                clone_dict = {'UserIds': [user_from_server],
                                                              'addGroupIds': original_groups_ids, 'removeGroupIds': []}
                                                print(clone_dict)
                                                res_clone_add_group = requests.post(BASE_URL +
                                                                                    'changeUserGroups',
                                                                                    json=clone_dict,
                                                                                    headers=HEADER_dict)
                                                print(res_clone_add_group.status_code)
                                                if res_clone_add_group.status_code == 200:
                                                    logging.info(f'Группы для {clone_user_login} добавлены')
                                                    add_users(get_users_from_server())
                                                    print(clone_dict)
                                                    add_del_groups_to_user_after_apply(clone_dict)
                                                    users_from_db = get_users_from_db()
                                                    users_from_db.sort(key=lambda i: i['login'])
                                                    user_list, treedata_update_user = get_user_list(users_from_db)
                                                    # user_list = list()
                                                    # treedata_update_user = sg.TreeData()
                                                    # for user_from_db in users_from_db:
                                                    #     user_list.append([user_from_db['id'], user_from_db['login'],
                                                    #                       user_from_db['name']])
                                                    #     treedata_update_user.insert('', user_from_db['id'], '',
                                                    #                                 values=[user_from_db['login'],
                                                    #                                         user_from_db['name']],
                                                    #                                 icon=check[0])
                                                    if filter_status:
                                                        search_str = values['-filterUser-']
                                                        # print(search_str)
                                                        filtered_users = filter(lambda x: search_str in x['login'],
                                                                                users_from_db)
                                                        filtered_users_list_of_dict = list(filtered_users)
                                                        # print(filtered_users_list_of_dict)
                                                        # print(len(filtered_users_list_of_dict))
                                                        # filtered_users_list = list()
                                                        filtered_users_list = get_filter_user_list(
                                                            filtered_users_list_of_dict)
                                                        # users_from_db = filtered_users_list_of_dict
                                                        # for filtered_user_list_of_dict in filtered_users_list_of_dict:
                                                        #     filtered_users_list.append(
                                                        #         [filtered_user_list_of_dict['id'],
                                                        #          filtered_user_list_of_dict['login'],
                                                        #          filtered_user_list_of_dict['name']])
                                                        window['-users-'].update(filtered_users_list)
                                                    else:
                                                        window['-users-'].update(user_list)
                                                    window['-TREE2-'].update(treedata_update_user)
                                                    # window_clone_user.close()
                                                    treedata_update_user = sg.TreeData()
                                                    for user_id, user_login, user_name, is_dispatcher in user_list:
                                                        treedata_update_user.insert('', user_id, '',
                                                                                    values=[user_login, user_name,
                                                                                            is_dispatcher],
                                                                                    icon=check[0])
                                                    window['-TREE2-'].update(treedata_update_user)
                                                    window_clone_user.close()
                                                    sg.popup("Пользователь клонирован!", title='Инфо',
                                                             icon=ICON_BASE_64,
                                                             no_titlebar=True, background_color='lightgray')
                                                    break
                                                else:
                                                    logging.error(f'Добавление групп для {clone_user_login} '
                                                                  f'НЕ выполнено - {res_clone_add_group.status_code}')
                                                    sg.popup("Добавление групп не выполнено", title='Инфо',
                                                             icon=ICON_BASE_64,
                                                             no_titlebar=True, background_color='lightgray')
                                            else:
                                                logging.error(f'Новый пользователь {clone_user_login} НЕ добавлен')
                                                sg.popup("Пользователь не добавлен!", title='Инфо', icon=ICON_BASE_64,
                                                         no_titlebar=True, background_color='lightgray')
                            if event == '-filterUser-':
                                filter_status = True
                                if values['-filterUser-']:
                                    search_str = values['-filterUser-']
                                    filtered_users = filter(lambda x: search_str in x['login'], users_from_db)
                                    filtered_users_list_of_dict = list(filtered_users)
                                    filtered_users_list = get_filter_user_list(filtered_users_list_of_dict)
                                    window['-users-'].update(filtered_users_list)
                                else:
                                    user_list_after_filter_null = get_filter_user_list(users_from_db)
                                    window['-users-'].update(user_list_after_filter_null)
                                    filter_status = False
                            if event == '-filterGroup-':
                                filter_status_group = True
                                if values['-filterGroup-']:
                                    search_str = values['-filterGroup-']
                                    filtered_groups = filter(lambda x: search_str in x['name'], groups_from_db)
                                    filtered_groups_list_of_dict = list(filtered_groups)
                                    filtered_groups_list = list()
                                    for filtered_group_list_of_dict in filtered_groups_list_of_dict:
                                        filtered_groups_list.append([filtered_group_list_of_dict['id'],
                                                                     filtered_group_list_of_dict['name'],
                                                                     filtered_group_list_of_dict['desc']])
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
                                # filtered_journal = []
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
                                        new_group_is_emergency = int(val_add_group['emergency'])
                                        add_group_dict = {'name': new_group_name,
                                                          'description': new_group_desc,
                                                          'groupType': new_group_is_emergency}
                                        # print(add_group_dict)
                                        res_add_user = requests.post(BASE_URL + 'addGroup',
                                                                     json=add_group_dict, headers=HEADER_dict)
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
                                if not values['-groups2-']:
                                    # print(f"Не выбрана группа")
                                    sg.popup('Не выбрана группа', title='Инфо', icon=ICON_BASE_64,
                                             no_titlebar=True, background_color='lightgray')
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
                                            res_del_group = requests.post(BASE_URL + 'deleteGroup',
                                                                          json=del_group, headers=HEADER_dict)
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
                                                logging.error(f'Группа {del_group["name"]} НЕ удалена - '
                                                              f'{res_del_group.status_code}')
                                                sg.popup("Группа не удалена!", title='Инфо', icon=ICON_BASE_64,
                                                         no_titlebar=True, background_color='lightgray')
                            if event == '-Start-':
                                print('Стартуем сервер')
                                sg.popup('Запускаем сервер, ждите..', title='Инфо', icon=ICON_BASE_64, no_titlebar=True,
                                         background_color='lightgray', non_blocking=True, auto_close=True,
                                         auto_close_duration=5)
                                # path_home_server = Path(Path.home(), 'Omega')
                                # print(path_home_server)
                                # start_command = 'cd ' + str(path_home_server) + ' && ./run'
                                start_command = 'sudo systemctl restart omega'
                                process = subprocess.Popen(start_command, shell=True,
                                                           stdout=subprocess.PIPE,
                                                           stderr=subprocess.PIPE)
                                # process = subprocess.Popen("ssh pashi@10.1.4.156"
                                #                            " 'bash ./run > /dev/null'", shell=True,
                                #                                stdout=subprocess.PIPE,
                                #                                stderr=subprocess.PIPE,
                                #                                executable=r'C:\Program Files\PowerShell\7\pwsh.exe')
                                for i in range(3):
                                    sleep(1)
                                    res_ping = ''
                                    try:
                                        res_ping = requests.get(BASE_URL_PING, timeout=1)
                                    except Exception as e:
                                        print(f"Сервер не отвечает, {e}")
                                    if res_ping == '':
                                        print('Нет ответа сервера')
                                        if i == 2:
                                            logging.critical(f'Сервер не отвечает - {res_ping}')
                                            sg.popup("Сервер не отвечает", title='Инфо', icon=ICON_BASE_64,
                                                     no_titlebar=True,
                                                     background_color='lightgray')
                                    else:
                                        if res_ping.status_code == 200:
                                            logging.info(f'Сервер запущен администратором')
                                            print(f'{res_ping.text}')
                                            dict_online_after_start = json.loads(res_ping.text)
                                            # print(dict_online_after_start)
                                            update_text = 'Пользователей онлайн: обновление...' + ', Версия БД: ' \
                                                          + str(dict_online_after_start["databaseVersion"])
                                            server_status['online'] = dict_online_after_start["onlineUsersCount"]
                                            server_status['db'] = dict_online_after_start["databaseVersion"]
                                            window['-StatusBar-'].update(update_text, background_color='#699349')
                                            window['-Start-'].update(disabled=True)
                                            window['-Stop-'].update(disabled=False)
                                            TOKEN = get_token(BASE_URL_AUTH)
                                            HEADER_dict = {"Authorization": "Bearer " + TOKEN}
                                            # print(TOKEN)
                                            # print(HEADER_dict)
                                            server_status['run'] = True
                                            # server_status['last_state'] = False
                                            print(server_status)
                                            # print('before init')
                                            init_db()
                                            # print('after init')
                                            users_from_db = get_users_from_db()
                                            # print(users_from_db)
                                            groups_from_db = get_groups_from_db()
                                            # print(groups_from_db)
                                            users_from_db.sort(key=lambda i: i['login'])
                                            groups_from_db.sort(key=lambda i: i['name'])
                                            # treedata_update_user = sg.TreeData()
                                            treedata_update_group = sg.TreeData()
                                            # user_list = list()
                                            group_list = list()
                                            user_list, treedata_update_user = get_user_list(users_from_db)
                                            if users_from_db != [[]] and groups_from_db != [[]]:
                                                for group_from_db in groups_from_db:
                                                    group_list.append([group_from_db['id'], group_from_db['name'],
                                                                       group_from_db['desc']])
                                            for group in groups_from_db:
                                                treedata_update_group.insert('', group['id'], '',
                                                                             values=[group['name'], group['desc']],
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
                                            # print('after update GUI')
                                            break
                            if event == '-Stop-':
                                # print('Останавливаем сервер')
                                # res = requests.get(BASE_URL + 'stopServer', headers=HEADER_dict)
                                stop_command = 'sudo systemctl stop omega'
                                process = subprocess.Popen(stop_command, shell=True,
                                                           stdout=subprocess.PIPE,
                                                           stderr=subprocess.PIPE)
                                sleep(1)
                                res_ping = ''
                                try:
                                    res_ping = requests.get(BASE_URL_PING, timeout=1)
                                except Exception as e:
                                    print(f"Сервер не отвечает, {e}")
                                if res_ping != '':
                                    print('Сервер НЕ остановлен')
                                    logging.warning(f'Сервер НЕ остановлен администратором')
                                    sg.popup('Сервер НЕ остановлен', title='Инфо', icon=ICON_BASE_64, no_titlebar=True,
                                             non_blocking=True, background_color='lightgray')
                                else:
                                    logging.warning(f'Сервер остановлен администратором')
                                    sg.popup('Сервер остановлен', title='Инфо', icon=ICON_BASE_64, no_titlebar=True,
                                             non_blocking=True, background_color='lightgray')
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
                                    # server_status['last_state'] = True
                                    print(server_status)
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
                                        # filtered_journal = []
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
                                    # filtered_journal = []
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
                                    # filtered_journal = []
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
                                    # filtered_journal = []
                                    filtered_journal = filter_journal(journal_list)
                                    if filter_status_journal:
                                        filtered_journal = list(filter(lambda x: search_str in x, filtered_journal))
                                    output_text = "\n".join(filtered_journal)
                                    window['journal'].update(output_text)
                                    window['countLogs'].update(len(filtered_journal))
                            if event == 'critical':
                                if filter_journal_critical:
                                    filter_journal_critical = False
                                else:
                                    filter_journal_critical = True
                                with open('admin.log', mode='r', encoding='cp1251') as log_f:
                                    s = log_f.read().rstrip('\n')
                                    journal_list = s.split('\n')
                                    # filtered_journal = []
                                    filtered_journal = filter_journal(journal_list)
                                    if filter_status_journal:
                                        filtered_journal = list(filter(lambda x: search_str in x, filtered_journal))
                                    output_text = "\n".join(filtered_journal)
                                    window['journal'].update(output_text)
                                    window['countLogs'].update(len(filtered_journal))
                            if event == '-checkAllGroups-':
                                # print(f'{values}')
                                if filter_status:
                                    user_id = filtered_users_list_of_dict[values['-users-'][0]]['id']
                                else:
                                    # print(f"{values['-users-']}")
                                    # print(f"{values['-users-'][0]}")
                                    user_id = users_from_db[values['-users-'][0]]['id']
                                # print(f'{user_id}')
                                all_group_ids = []
                                for group_from_all in groups_from_db:
                                    all_group_ids.append(group_from_all['id'])
                                tree.metadata = []
                                if values['-checkAllGroups-']:
                                    for group_id_for_tree in all_group_ids:
                                        tree.metadata.append(group_id_for_tree)
                                        tree.update(key=group_id_for_tree, icon=check[1])
                                else:
                                    for group_id_for_tree in all_group_ids:
                                        tree.update(key=group_id_for_tree, icon=check[0])
                                    # tree.metadata = []
                                window['Apply'].update(disabled=False)
                            if event == '-checkAllUsers-':
                                # print(f'{values}')
                                if filter_status:
                                    group_id = filtered_groups_list_of_dict[values['-groups2-'][0]]['id']
                                else:
                                    group_id = groups_from_db[values['-groups2-'][0]]['id']
                                all_user_ids = []
                                for user_from_all in users_from_db:
                                    all_user_ids.append(user_from_all['id'])
                                tree2.metadata = []
                                if values['-checkAllUsers-']:
                                    for user_id_for_tree in all_user_ids:
                                        tree2.metadata.append(user_id_for_tree)
                                        tree2.update(key=user_id_for_tree, icon=check[1])
                                else:
                                    for user_id_for_tree in all_user_ids:
                                        tree2.update(key=user_id_for_tree, icon=check[0])
                                window['Apply2'].update(disabled=False)
                    else:
                        sg.popup('Введите правильный ip!', title='Инфо', icon=ICON_BASE_64, no_titlebar=True,
                                 background_color='lightgray')
                        break
                if window_main_active:
                    window.close()
                    break
            else:
                sg.popup("Неправильный пароль!!!", title='Инфо', icon=ICON_BASE_64, no_titlebar=True,
                         background_color='lightgray')
                window_login['password'].update('')
    if not window_main_active:
        window_login.close()
