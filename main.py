import binascii
import json
import os
import platform
import socket
import subprocess
import threading
from time import sleep
import requests
from pathlib import Path
import sqlite3
import PySimpleGUI as sg
from io import BytesIO
from PIL import Image, ImageDraw
import ipaddress
import logging
import sys
from enum import Enum


ICON_BASE_64 = b'iVBORw0KGgoAAAANSUhEUgAAAMcAAADJCAYAAACXDya2AAAABmJLR0QA/wD/AP+gvaeTAAARR0lEQVR42u1dCZAU1RluLzzwjHgQQRHY3cGNaLJB1CiCioocO9Oz44EQMIUSj6CEmIgSXMUDNQKuO/16sujiRuKJWh4xokhpKEKhiEQFl+USOQJIIpco1+Z/vUh0WWBm+nX3+7r/v+ovqiy0nPe+r99//4bB4qHU72fERRsjbvUwEmKIkbQeNkzxNOlbpO+Tfky6kPRLw7Q20p/19PfW0Z+rd/7zOaQzSSeTVtPfGUHa10hmOhupiuP4fFlwxMy0JHBfZSTFGALztF2A90obiCSJdpdRZl9k9K9pzpfAooeknjvAMNPdDNMeu/MVqA9YtzovjXyh4uIsviAW/00l0+5Cr8J4AuIaDQixN5Wm2X1GaeZ0vjcW76R3pgWRYjiBrU5zQuxB7U/IDBtqpDJH8WWyKDKdrCICVxXp15ik2E3XE0nGOf4RC0tekrTaEogmEJi2hYQUjXUT6YNGT+sYvmyWLF+KMYcSaMpJN4eUFI11rZG0bzHKy/fny2fZs8hwqCmWRIQUjXWKYVa1YhCwNA7JNtuZoNseUWL8/xUxRYIBwdIgicpjKZLzTsRJ8X3dQWbWaDazOBJFkShrEROiSZ1oXJ85iEESyWhUJkYAWM4k2Gtu5DVjYPUhDJZIEcMuoMtfxeDPQpPWJDaxIuVjWLUM/JwIIhg4YRf5BWTnO0+1BjGAwixOPwQDPU/dbMTTZzKIQulnVBbvLOlmoOevs9j/COWrYb/E4FaiAxlMoXLC0x2c5BYDW4Xvschp8mIJy6shLAa1yuiVSDKowiA9Ko6kC93AoFaq/2RghePVGMxg9uT1+CmDC58c0xnMnuhjDC5oR7yykB1xz+qu/kt99YcxyHCTfvcziD2NXPVlkCGKUyoiljKAPe4eZAGUsvQlDF4fGqNS6fYMNjxHfCKD1wdNiHsZbHi5jU0MXl90pdG1/EAGHUyUSlzHoPX19ejFoMMhx3sMWl/1eQYdgpSmW/OInQB6PXgGL4AkrdsYrFzKztIkOcQHDNQg/A77TQafzhLPtGOgBqbbKOdxIoNQ21fDHskgDTRqNYRBqG3ijxa0MEi5z4OlcfjWPoPBqUOfBw3MY9Eut/EAg1OLSt0RDEbtTCqxgIGphc5jMGpFDOtsBqVGysPftDKpxjEotdIHGZQ6SENT0zIGpFa6lCcj6iBlomsIwESjg6xn6M8/kdaQrglBj3kXBmfgiT8aj49edtF43XEqfTiRZQY4QdIMziBFjqXEXkLzhdHn8SP2kLfpDt8ExWNDA3XELwQfjHZniIlPr6J1AYOUTao8wUMDrveeu6kCz5ZXMkiDi1KtAM4k1+77ZbQvY9OKJY/EX7pb6Kd2yFXHpljLUSuWHMlB0RDoLLJVkuXvrOaZuiwRMqnEEsOo3y/LoEMvNq1YcohSURQEO0o1Juvf2qPiYPp3voL+vWXW+Qxa/0yqxyIFFlM8BV7GXsGg9c+kWg4Mln/nbGaYIgFvWnGtlQ8iv7rYQLFz/s0Dqw+hf289dnQucx6D13OTip5obH/j0jyrAZ4F/92PMni9N6mAy9NpG1LquWb5VQOIK8BfzBVsWnkapaKnGRsgNXn/drliDH9y/C8YxJ6RA77jL+EySvcieFXAOAaxJ0JJM1N8DgyOTUb/muYuPw7XsGnF0kSUKn0uODBecH0GsvdDTjRn04qlUVb8EexojdVPyTkkxavghYhjGczqTaolwKD41oiPPVoNOawB4C/HkqzryliyAYT9c/DyiTeUnYUkmSQb9HlkfsagVpb4E/eBm1TXK06EvgFuWo1iUKsjxzxgMGxXvrfCtAaBk+MTBrUKSdmngdvY7yo/k96ZFvTf3Qp9LimriMHtPjpzJ7i/catHCdG3wT8av2dwuycH9o6/VNWpHp3LDbzoJtK+RuUpdIg7gAHwvmdn06fqBGcPH+7Z0L1WtWKQ5286DAU3qe7wOFDxLngZ+w0M8vzJ8R725WdiHp/PEHDTajKDPL+LPx7abEiIT72P5ImTwM3OLbsN0WbJxuGkxBknurIxraZzzVnknHH0LLBPJRKmGAZOjkkM9pzMhcxR4PVDi30rritNtwY3rTY5XY4sWZtU/cBH7z/i7ytLIWPsBT6lDPrsyTGJx9DklBC8Hbx9dgKDPiuTasyh5G9sjNTQNvcfk7bgId21RtfyAxn8+zYREuAOpgjmtbVng78eFzL4902OGuw5uOlLAorujeBVBWEWuawlKf4TyaFtrs1RKgHHJscybp/du2N5KXgt1ZPBvrrURAR9fulOTII9m1Q2uL8RD/j8ysE/LvczCZoS/G1NwSezSjOng5OjlonQlODPwX1ek9d3Hvbr63ElMyY5wIe2mVZfTciBPanFtIczGXa/1IXQpdeqhra5PkcqeMR+gWcyGcJ1oa9r9qFZAN0+K4spWXaFIEeBm1SD9DJR7YfA22dvZlKEIz6/zela1CpflOkM/hJPYVI4F2kXgNcETdXvUOF3mWxzBtfxq0HRCWxyDNH0XMeCJ1QHMDlkdALZeUxlTua8kSd+x8sRJwYN9cJu8dQ37NhQcbAc+Gy/dr0mDjvxBz53SXbg6e3PVXKtGi45pvKkcC9f5nQ38Gz5E9EkBv4Y/Y+1P2PZrmuKVcBn/KXvLcd6fNXAF7AkrLtBAh7YbQB+D6vQ5NJeh760ePpMDNPV7g4+tuehaBEDf5/2YpizllM9TLEG+Kzropb4u5KHtvl63k9w4APH33gGfMLIuVDnnbQv5xVpCNKj4mAK4a4DvqiVToINSeCnuohp0SBH3OoB/hVLgwZAkOeBqV9Xran9mwHP2l6MmXClYc3Y1Qi/Cjcx4CeM0NA2aaKwOcuFiMpFOrLYJlU1eG7paehCxFDv8TDFg+DtsH3ATdoybNPK7h1eciTEZ8CXs8FZj4As8suLvd6hKpzESFYWg3f8PRuS1/sF4HtYBRdGz44c4k5wclwVjnuwrwavtTonjP4GcjvsNxTtOTIU95BKH+44t7gfqQfCRQz0ZfJJ8WrIXvGXgT9Uc0PmiFs3cQJKq1e8P7ZpVVkYpst4C3qGUqriuFCRQ871xd7zPowvQo+s+DshzTkhN5u9GxL71uoH3uT/m3CG1slU5ImIHFfnid9N+YGVx0IPuICfiCiL3UyxHrhcZIYRZjHFZGByTEJPOPUGb4f9Q8jJMRj4w7XRGFh9CPDhW+O5d1ljgZ8dZvXEPPiG3o2VwLmNfxlREOipk9Q4Byll1vngvRvlkSCH3KKEe0crnF0kgFlx7O2wCfuMSJBD9mbLHm3Y4XriLERnD3g7rLXI6+OpN4wD6mKxc2pjseHzi4omzo/FZtCf80gXks4hnUpq1RYWDpoXi7Xx+K6mARci3ouW+OvIIyibls+KiooI9GNJvyStz0FnE1Fu+rS4+HAP/I6hPNDbvxDuSO4Z+KEsaNeudW1RUQ2BfFuOpGisq+sKC4d+UFKibtAD+hKhVLo9kkn1ITA5lqvuNiOTaTCBep1LUuz2ktAr1FFh2H0GsBl8KwgxKk/B7t2gbUiK5ItWrQ6l1+Iviknxfd1ExOuryBS+jTf6em9S3YI9B9e+SMUxrCgpOYzA+7aHxPhOd9QVFbn/cqaqTgX+qG1zasX0fzmoxBt5k5Ac2e9SyGluRi/GOz4QY5eSH3KjAnN4FnCtVT/NcxvglZ6KdtDNLyyc4CcxdupWCg1f6tLvuAPYHH5Od0d8YNSHhhFIrw2AGN/pmrkdOrR0YRIXQM8V07oQ0bRfivLhUh7iJA+iUjkpmXPuZsrKmjLcEPxlmpYh0DRA6Gl6tFDHpZBZ82SQxNjlf8Ril7h4/e8C/sBZumbF4+DtsFe6MqcKCjoQMLfrQA7SmfnfI/RkyuV6FiImxIQoD22jr/WfNSFGgxYUdHHxeszFLUS0SjQzqZxl8MAbS61XFOQ0NuhEDpl8dOE7jgL+0N2jmSOe7gbeDnutS0f8Sq1ejQZdt7hNm/wCDHLHOu59fqSbSTUuymNedHHEd9PCwotdmFZ1uIWIlO3XKL+xGJgcUxTkNhbqSA7qFbnbRc5jNHCt1RA9iIH9BNc7baJuXo327Y/U8tVo0FdcmMqdgMnxti6Fhsi9GzucXgYXsiAWK9GYHHNdWgSo3ZxbjJ7WMTqYVO8Dk2O6a5MqFuulMTnWufMlgecAyCU9wRIj0xK7d4N6GNyT42qNybGdetXzT4ohb/9NiL8GHaW6Lup7HqhUvL/G5Kif2rWrixJ8yjabYino/X5F+bdmAb4clDyLeDycXo6kxuTY7N6nFI9GvXEtz0JDsQmYHHepOAbq475QV3JQlnylgkrrLsCRyEeDMql6QZtUpZnTVRyDnCmlKzmofXaa6x/YMNZ1Beg9LwmqdyMDTI46VcdADu/+zqADPV+O8YoikhZw0KWjz8xwHLUvgMN8o1Weht/94jm8HGoWfUrbHbeodITPWXEqC4bOimc6qzwOiliN1LS2qq3CquvVoPc902eTiiaQ45JjmeqGGKrKjWlIjlmK77wqqlUQuR7ULOBntsKLI6GQ7oeaFR2qXUcs+7NxP4iD/SFGn8d+DJ0Vl70nHgiBcYBG5FhPvRxHK/2B12cOovNbC9oC/ZpfrwbwHjk1Q9uaEjnIjUC5SBNyjPbk7nFbob8x+jx+hB8h3NeATarxXh4NRYdSGhBj9cK2bY/yqAIbdwFqwjY5Kx7ggkVZ5EfgfD1QcqgaLN2UNKzO/gr0/qu9rqXqA2xSrfdjIt7i4uITCaSrAiLHUz6Y1RNhTWoZkvbwYKpwn1X/SpgptNvJ96w5RcvmdOzY3PuyITJPYDGQOc/LrPgy4AkjKT9TQUSQOIH2W786/lzNyM3dtN7A6+x+8GoA9xSbYrM/0YpGuY+Cgp4+zLP6gFaqHe9z0emzUa+pa2xS3QNcuvyyEZDUnXZaMUWxaj0qD5kgt0f5/qOS4grcsT1WkRdhvNnAlZkDjABFApjA/DDpFkXEWCbNtsB+UO/MYbBRSwWt0T+U0nRr4Kz4VrdD21TJguLi9jsHwH2TJymWk+P9u0Bei90tiRdBw/n/UJ34uxHY35hsaCb01W9B5SY3k7n1NwL8xn0QYinp40Sq3pRHOUCbH5EQ18BOuExVHKcyv/EGsL9xg6GxyGYpGgzXbn6HDt1lht2p0YrFTCLQeZJE2v6PywCHDHRg4mKgmkPoX9Mc+BC2O4WSLF455q+C+h2TVNmWCWCTahoj2FO/A3QHJG0gU1ItITes4pJjGCPYQ4mPPZrO+Nto1tk1TJ5YCRzCbcsI9vz1+DsoPmy3jvjZwEMUZjNyfYlaoU69XOGuXdoU9wGTYyQj15eEYAsnl4TZFdrJTTQCeCe1+Akj1zfTagpo++yo/H5wKnMysCM+nxHrJzlgk8Rz8n01bgZ+NR5gxPqZEKw6wck8R2Z/IG4UgnZRi7MYsb475u9FY38gdlZc+dA2lqzIMSQa+wORe8UDGzsfcUmJk0Art3PcH4g8Qb1MdGWkBha1mh7+/YGm+ByUHGu8GtrGkhVuhoV7+EbCPgM4hFvFCA1Q4qINqGmV5f5A0x4OnBW/nBEa+OuBuXo7q/2Bssybh7ax5CtJcXs4Azmp8T/CrZOhSXwsGpCDKqFDuT/QtPri+ht2GSNTG9Pqo/DtDzTFU6Dk+NpJXLLoQo4/hmt/YMPetzWgr8ZLjEidEoI0OC1U+wPL0ucC7174JSNSM0mIT8OzPzAh7gUlxxYnkMCiGTmsu8OzPxB13GfCfpORqGXUqmM49gciL8FM2L9mJGrrmM/D3x+I2yS/3TAzLRmFupLDuh9/f6CM9vBQYBbVErdKsPcHyoIrWXqBWUv1W0ag9qbVAtz9gQm7Ow9tY/EuakWrxmD3BybEOFByzGLkIUStMp1x9wfKMTahSvWz6CXOolXE5rm6/wGZ2bRwzwfZsgAAAABJRU5ErkJggg=='
ICON_BLANK_BASE_64 = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAZSURBVDhPY/hPIhjVQAwY1UAMGHQa/v8HAK+t/R8kTA7nAAAAAElFTkSuQmCC'
# ICON_SHOW_BASE_64 = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAi9JREFUWEft1surT1EUB/DP9X6WJEaYeowkpKirGJGBGWWmyFiZmJmYmJgzEP4BN93BJXdAlIQ8hoqJR1555hGt2kf7Hvv8fufnXn6T3xqds9djf/da37X2HtJnGerz/gYABhn4mwwswX7sxspE4qcYwVk874XYbQFMwykcpitxf+I0DuFHNzBtABzHsUKgL3id1hdjTsHmJI50AtEJwFy8wIIswA3sw+OGoMtxHlsz/WcsxYeSTxOA1XiYOdzFRnztltKkn4Hr2JDZr8ftun8JwObkXNnuxKWa4/REuD0IflxGfEdZctmGK9nCDozlBnUAq/AoGQSZgvFVnSu/ZXjWkIl1uFPTLcTbBDRUEzKRA5iHj9nm8V8/UaiD2XHqkJv4hDhpJaEL8LnMTLEqv0V4FwY5gNhsdvL6bdAhpTEDniR9ZOpl+g7WB/vrMj8j4jfMygFcxK7ksT3VtJTlC9iLN4jWy+VVWgvyri05YxOik0KuRuaqDOQA/iBKFixaLNow0h4nyiXWonWvYUsLAOMY7rUEQaBbKXhMuwPp+wSOpu9iuyXA1Sz4juDFBA60JWHM+hgsJYk7YUVB0YqE4ZcPoKY2DLv7hTo31b51G1bA2wyisI2MBV+CzaN4Xzh5z4OoirEGD7KA99JY/S+juNq3dBnF4Ik2bLqMov7npuIyyrPZt+s4B9Hrg+QMDk7Vg6TOrfxJFimPWfLPn2QNbT/55TZPssnv0iHCAMAgA78ACiR5IZsXaIEAAAAASUVORK5CYII='
ICON_SHOW_BASE_64 = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAPFJREFUOE+10zFKg0EQBeAviEEEC9HCVrCxtBJsBLGJOYA2egUPkMJUXsATiIieQAWRaJsiBxAtLUQrwUJBIxsmsPxEjPnJVLO7M2/evNmpKGmVkvnGBrCBIyzRK/KAfVwXGRcZLOIeEzjFMbrYwy6+sByAPawcYBvnOEQjKq1hEndxbuIgAE9ygM2gt4p2BD9hIfw3zIa/gg62cJkYTOMdNVxF0DxeMoapjaTHY7wnjW4w8xvAHF4xhW98BpvnQQDpblALt1iPhBZS1WT9Fuq4yEXcwVlBxGq08fGXiP3xlhpj/kdG/kj/Xo2x7cLQTH4AHKU1KbsxXsMAAAAASUVORK5CYII='
# ICON_HIDE_BASE_64 = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAzlJREFUWEfFllmojVEYhp9jOGYns2RMpmQqZShliAuJ3IgSDsmUDJFkynBBUrhAISK5UDJcKIkonFA4JENcmDMmMxl69S2ts1p7n/8/e9vem73/tb7hXeubVhH/GUUF8t8buBbzVQgCm4F5wAOgY0jiXxOoCXwzpyKyoNAELgN9gV9AtXyGQDfXCGhuRl8Ab82R89MaeGQfY4EjuRIoBjYCswBdbQzfgd121c+BEuA90DBTsifJgRrAWWBgFSumHfCwqgSmAHsCZWXzKuAE8M72dMIRwBqgkyev0uuTjXi2GzgHDPKU9wLTgJ+V3ITCtMhkalkV1Ac+pMmBJ0ArU1ByKaE+BQaqA/0tHy4CXwGFS3kgbAPm2P/HgMg0S1KGz4CWJngMGBNhfhAYH6yft1IbEJRdN+CWyb4Bmvh6YQiuAmqbwhZgfsT5UWB0JWEYBxzyZNYCy+37DtDV7fkE1gNLbEPxLo04USxVVkKZ5Yhy4jgw0tY/ApILsRWYa4vbgdn67wgoc+/a5g2gZ4YTrgRWRzrbcOCk6ajfq1JiEOl+ttELKHcElEBqNEILQJ0tBp10FKCkauMJ/LD43wR6ZNDVssrVla6StdgRkFK5KV7yWIa2FEfFUxBhGVkHLLO12lYNmTicBobYppK1zM8BlY3arKB4aYSGkFPdlqABo7xZat+7gOlZTu8TPQBMlGxYBcrQzmZEXU0dL8QMYEdkPVtTU2NSgxLUltWe/yCmpFrVpBP2A5MizkRSdd/U9nQanSoGZfxM21A3bOALZWL9GmhsgmpM7b2HhdN/aQQ+A3UjntUV7wNtbU/lq+mo0P1FtmvTIFGpOGwCFpuBwcAZ2+jilbCT9eOttQrNJykByS0E5NjHdSs1vXBuA2q1wlBgg72AfPkVVinR+CR5D6i0rgDdIxbqAF+AepFpd8/aejjEKphJQsApyMlOYIIt7AMm2391vg42qg8DU72WHT25W0xDQDqngGGm7HT1q3H9FFBHTIU0BDRGX5l1DSoNrJyRhoAemZoTirlinxckJaC+fcE8KhndAyNnEkkJ6AGih4gy27XqnJ3LQFICktWbzg2ivDhPSyBvTn1DvwGQ9JMh9I2ufAAAAABJRU5ErkJggg=='
ICON_HIDE_BASE_64 = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAU9JREFUOE+V088rp2EUBfCPYSZJmcgsSGOhzExpsrCwMMWfYGMnyU7ZKAsLNJtpasrGYmYxK/4IFpQdUhJSI+Xnhkg2mmGGnum+9fbN1zfP7n3ec84999z7lHn+eYF/Ga3s+Xy36MJK4pYSKA/MXRQawwSqn3LwGktoL3C3iY9owX4xgW8YxSr6cBTAJmzFd1teON/CIrrRHMBKzONliB0j3X1GJz7lM/iBoQCkkNJJSW/gdxB+BqYi7mYxkBx8wA7qcJmzfIAUYgfWCgKvwVXKJGvhL75jOASS1Rv0YAGDmMv1Po0RVGQCtbjAF4wHMInNhFBVjjyFSbzBeT7ERpxgN0b4J3JoxS+8wjrSFN5mEypcpNTzNt5F5UO8xxnqsReZZYtVdBMbcIpkvTdIX3FduPrFVjlVXkZ/qbfymEAWaKl38l+7GCjd35eqnv4/AN2DP0ArBQAaAAAAAElFTkSuQmCC'
ICON_CHECK_BASE_64 = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAsQAAALEBxi1JjQAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAASfSURBVFiFzZdfbBRFHMc/M7t3Vwq09qCAxPKnJbYFKqSatCgEMdGgCKT+xagxkGCID0bA+CT4NyEN/iHBF6I+qPFBTCu+8IKQGMSWllJLQFqsEdoCd71ry9Frr3d7N+PD9Y52uS1XbaLfZLOzs7/5fT87szs7A/+xxCRipwOPAZVAEZALRIA+4BzQCLRPNSDA48IQR4UUMUBPdEhTdgC7gRlZ5K0AKibqgUphigM6rtcACCkoKPfiLZuFp8CDJz8HZSmioSihzgH6zgeJhqIACEMEdULvBr52yL0BqAOGnAC2CSEOaa1Nd56bJU+Xcs/DRbjz3I60OqHpbfXTWXeJgfZ+hCES1furZzbsaog4mHuA/ZkAaoG3ABY/WULpC+WYuaajcSb1tvhACOZUzm1Qluupo8997xu9tR74AcgBDgA77QBvAJ9Kl6Rix0qKHlkwKWMHdZhQfaTmSLXdHGDsoz2K4GOAyl0PMK96/lSYA5ReOdlzHFhqNweQo2e3dMkv0MjSLeVTaU6g1U/bwdbKTOZjAXYoSy2YuTCPJc/eO6XmzfuaUFaCRU8UR2vqaz60x0hACkPuASh/eRlCTGZuys588cYSlm+/zxOTaqc9TgKrdELNnj5/BnPun5sxWd+FIG2ftRK9MZKVeW+Lj+Z9p9Pmy7ZVJM202JIJYDPAvKq7HRNeO3mV7uNXaNhz6o4QvS0+ztQ2oSxF8aZb5gAaSjbU1ywfByBMYx1A4Yo5jknLXlpKfsldhHsGaXj7F0b6M0MEWv2cqW1GWYrFG0tYurVi3P3ojSh/1nVsHweAVsUA0wqnOQK4ZriofvehJMTVMI17b4ewj/nYJ0/p/OdttH/7++tA1S0ARR6Ax5vjCJAJomHPLYhszAF0XKeK89IA6SptD88MUbX3QfIW5TN0LUzj3lN0n+hKv3D2MbcrEUukiioNICQhwHFc7XLnuVn1werRnhik7eBZxzG3a2Qg7XEjDYCgEyASGM4KAMYPBzBht6ektSYSSP8YO1MFU8f1CaAq0OqncKXzl5AJYtX7q7l5JYS3fNYd4wfa+4kPW0iX7FKWup6ql8CPAL7TPsfGTjJzzazMAfxNSU9lqe/G1kugSZrSN+wfwtd4PVPbfy0rbNH1U1fqst4OoFVcvQNw8ZsL6IRiqtVZdwkrHEOY4gTJxWtaxui5Tbrki7FQ1KvjmtkrCqfMvP9iH+cPtaG11iieAcaNdep3HFeW2iqESHTWX+Lqz91TYh4JDNNS24SKK9B8ArTaY4wx5S6gG9jsb/ZhmEbWL1gm3bwc4vR7DYz0jyAMcRzNK2SY7gzb9W9IQLE2eC4gIsFhvGVeDE/2i1Kd0HQdu8zZj5qJ3YwhTKNRJ9QmkpuY2+S0+nheSPGVVtpj5poUb15C0boFTCvMdTSOj8TxN/v443AH4Z7BZKXkSxSvATGndhMtf8qFIfbrhN6QqsgvzqegbBY5BTl4CjzEh+NE+iKEewYJnguirORcL13yL2WpN7F9cv9Ua6SUh4UhhphoayZICFP8CrwKuLJNPpkFoBtYS3JzupDk5jQKBIALwDEgOIl8/w/9DR5k79YG7eHTAAAAAElFTkSuQmCC'
MAX_LEN_LOGIN = 10
MAX_LEN_USERNAME = 20
MIN_LEN_PASSWORD = 6
MAX_LEN_PASSWORD = 20
MAX_LEN_GROUPNAME = 20
MAX_LEN_GROUPDESC = 100
MIN_CALL_TM = 10
MAX_CALL_TM = 120
MIN_CALL_END_TM = 1
MAX_CALL_END_TM = 10
MIN_TONAL_CALL_END_TM = 3
MAX_TONAL_CALL_END_TM = 10
MIN_AMB_LIST_TM = 3
MAX_AMB_LIST_TM = 30
MIN_AUDIO_PORT = 1025
MAX_AUDIO_PORT = 65535
MIN_PORTS = 20
MAX_PORTS = 1000
MIN_PING_TM = 2
MAX_PING_TM = 120
DEF_PING_TM = 5
role = Enum('role', 'allow_ind_call allow_delete_chats allow_partial_drop')
user_type = {'disabled': -1, 'user': 0, 'box': 1, 'dispatcher': 15, 'admin': 30, 'tm': 100}
version = '1.0.5 СТИС'

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
    users = get_users_from_server()
    add_users(users)
    add_groups(get_groups_from_server())
    add_user_in_groups(users)


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


def get_users_from_server() -> list[dict]:
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


def get_groups_from_server() -> list[dict]:
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
        is_dispatcher, is_admin, is_blocked, is_gw, previous_type, enabled_ind, en_del_chats, \
            en_partial_drop, priority = 1 if user["userType"] == 15 or user['previousType'] == 15 else 0, \
            1 if user["userType"] == 30 or user['previousType'] == 30 else 0, \
            1 if user["userType"] == -1 else 0, \
            1 if user["userType"] == 1 or user['previousType'] == 1 else 0, \
            user['previousType'], \
            1 if role.allow_ind_call.value in user["userRoles"] else 0, \
            1 if role.allow_delete_chats.value in user['userRoles'] else 0, \
            1 if role.allow_partial_drop.value in user['userRoles'] else 0, \
            user['priority']
        db_insert_user = """insert or replace into Users(id, login, Display_name, 
        is_dispatcher, is_admin, is_blocked, is_gw, previous_type, en_ind, en_del_chats, en_partial_drop, priority)
        Values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        user_data = user['id'], user['login'], user['displayName'], \
            is_dispatcher, is_admin, is_blocked, is_gw, previous_type, enabled_ind, \
            en_del_chats, en_partial_drop, priority
        cur.execute(db_insert_user, user_data)
    con.commit()
    con.close()


def add_groups(groups_list):
    con = sqlite3.connect('adm.db')
    cur = con.cursor()
    for group in groups_list:
        description, is_disabled, type = '' if group['description'] is None else group['description'], \
            1 if group['isDisabled'] else 0, \
            1 if group['groupType'] else 0
        db_insert_group = """insert or replace into Groups(id, Name, description, is_emergency, is_disabled) 
        Values (?, ?, ?, ?, ?)"""
        group_data = group['id'], group['name'], description, type, is_disabled
        cur.execute(db_insert_group, group_data)
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


# def add_groups_to_user_after_apply(groups_for_user_dict):
#     con = sqlite3.connect('adm.db')
#     cur = con.cursor()
#     for user_id in groups_for_user_dict['UserIds']:
#         for group_id in groups_for_user_dict['GroupIds']:
#             db_insert_group_for_user = "insert or replace into Users_in_Groups(user_id, group_id) Values " \
#                                        "('" + user_id + "', '" + group_id + "')"
#             cur.execute(db_insert_group_for_user)
#     con.commit()
#     con.close()


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


# def add_users_to_group_after_apply(users_for_group_dict):
#     con = sqlite3.connect('adm.db')
#     cur = con.cursor()
#     for group_id in users_for_group_dict['GroupIds']:
#         for user_id in users_for_group_dict['UserIds']:
#             db_insert_user_for_group = "insert or replace into Users_in_Groups(user_id, group_id) Values " \
#                                        "('" + user_id + "', '" + group_id + "')"
#             cur.execute(db_insert_user_for_group)
#     con.commit()
#     con.close()


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


# def del_groups_to_user_after_apply(groups_for_user_dict):
#     con = sqlite3.connect('adm.db')
#     cur = con.cursor()
#     for user_id in groups_for_user_dict['UserIds']:
#         for group_id in groups_for_user_dict['GroupIds']:
#             db_delete_group_for_user = "delete from Users_in_Groups where user_id = '" + user_id + \
#                                        "' and  group_id = '" + group_id + "'"
#             cur.execute(db_delete_group_for_user)
#     con.commit()
#     con.close()


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


# def del_users_to_groups_after_apply(users_for_group_dict):
#     con = sqlite3.connect('adm.db')
#     cur = con.cursor()
#     for group_id in users_for_group_dict['GroupIds']:
#         for user_id in users_for_group_dict['UserIds']:
#             db_delete_user_for_group = "delete from Users_in_Groups where user_id = '" + user_id + \
#                                        "' and  group_id = '" + group_id + "'"
#             cur.execute(db_delete_user_for_group)
#     con.commit()
#     con.close()


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


def get_users_from_db() -> list[dict]:
    """
    Get users from DB sorted by user login in list[dict]
    """
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
                          'is_admin': user[5],
                          'is_blocked': user[6],
                          'is_gw': user[7],
                          'previous_type': user[8],
                          'en_ind': user[9],
                          'en_del_chats': user[10],
                          'en_partial_drop': user[11],
                          'priority': user[12],
                          }
        users_for_table.append(user_for_table)
    # print('---')
    con.close()
    users_for_table.sort(key=lambda i: i['login'])
    return users_for_table


def get_groups_from_db() -> list[dict]:
    """
    Get groups from DB sorted by group name in list[dict]
    """
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
                           'is_emergency': group[5],
                           'is_disabled': group[6]}
        # print(group_for_table)
        groups_for_table.append(group_for_table)
    # print('---')
    con.close()
    groups_for_table.sort(key=lambda i: i['name'])
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
    data = cur.fetchone()
    if data is not None:
        user_name = data[0]
    else:
        user_name = None
    con.close()
    return user_name


def get_only_user_list(local_users) -> list[list]:
    """Get users from DB and return Users in list
    Input:
    local_users: [{},]
    Output:
    us_list: [[],]
    """
    us_list = []
    for index, user in enumerate(local_users):
        us_list.append([user['id'], user['login'], user['name']])
        if user['is_dispatcher']:
            us_list[index].append(u'\u2713')
        else:
            us_list[index].append('')
        if user['is_blocked']:
            us_list[index].append(u'\u274c')
        else:
            us_list[index].append('')
    return us_list


# def get_only_group_list(local_groups) -> list[list]:
#     """Get groups from DB and return Groups in list
#         Input:
#         local_groups: [{},]
#         Output:
#         gr_list: [[],]
#         """
#     gr_list = []
#     for index, gr_from_db in enumerate(local_groups):
#         gr_list.append([gr_from_db['id'], gr_from_db['name'], gr_from_db['desc']])
#         if gr_from_db['is_emergency']:
#             gr_list[index].append(u'\u2713')
#         else:
#             gr_list[index].append('')
#         if gr_from_db['is_disabled']:
#             gr_list[index].append(u'\u274c')
#         else:
#             gr_list[index].append('')
#     return gr_list


def get_user_list(users):
    """Get users from DB and return users[] in list and in sg.Treedata for Tabs Users and Groups
    Input:
    users: [{}]
    Output:
    user_list: [id, login, name, is_dispatcher, is_blocked]
    user_treedata :sg.Treedata: '', id, login, name"""
    user_treedata = sg.TreeData()
    user_list = []
    for index, user_from_db in enumerate(users):
        user_list.append([user_from_db['id'], user_from_db['login'], user_from_db['name']])
        if user_from_db['is_dispatcher']:
            user_list[index].append(u'\u0020\u0020\u0020\u2713')
        else:
            user_list[index].append('')
        if user_from_db['is_admin']:
            user_list[index].append(u'\u0020\u0020\u0020\u2713')
        else:
            user_list[index].append('')
        if user_from_db['is_gw']:
            user_list[index].append(u'\u0020\u0020\u0020\u2713')
        else:
            user_list[index].append('')
        if user_from_db['is_blocked']:
            user_list[index].append(u'\u0020\u0020\u0020\u274c')
        else:
            user_list[index].append('')
        if users != [{}]:
            user_treedata.insert('', user_from_db['id'], '', values=[user_from_db['login'], user_from_db['name']],
                          icon=check[0])
    return user_list, user_treedata

def get_group_list(groups):
    """Get groups from DB and return groups[] in list and in sg.Treedata for Tabs Users and Groups
    Input:
    groups: [{}]
    Output:
    gr_list: [id, name, desc, is_emergency, is_disabled]
    group_treedata :sg.Treedata: '', id, login, name"""
    group_treedata = sg.TreeData()
    gr_list = []
    for index, gr_from_db in enumerate(groups):
        gr_list.append([gr_from_db['id'], gr_from_db['name'], gr_from_db['desc']])
        if gr_from_db['is_emergency']:
            gr_list[index].append(u'\u0020\u0020\u0020\u2713')
        else:
            gr_list[index].append('')
        if gr_from_db['is_disabled']:
            gr_list[index].append(u'\u0020\u0020\u0020\u274c')
        else:
            gr_list[index].append('')
        if groups != [{}]:
            group_treedata.insert('', gr_from_db['id'], '', values=[gr_from_db['name'], gr_from_db['desc']],
                      icon=check[0])
    return gr_list, group_treedata


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

# def get_groups_in_treedata(groups):
#     td = sg.TreeData()
#     if groups != [{}]:
#         for gr in groups:
#             td.insert('', gr['id'], '', values=[gr['name'], gr['desc']],
#                             icon=check[0])
#     return td


# def get_users_in_treedata(users):
#     td = sg.TreeData()
#     if users != [{}]:
#         for user in users:
#             td.insert('', user['id'], '', values=[user['login'], user['name']],
#                              icon=check[0])
#     return td


def make_main_window(ip):
    if server_status['run']:
        users_online_text = 'Данные загружаются...'
    else:
        users_online_text = 'Сервер не запущен...'
    user_list = list()
    group_list = list()
    treedata = sg.TreeData()
    treedata2 = sg.TreeData()
    label_text = 'Панель администратора ОМЕГА К100 ' + ip + ' Версия ' + version
    if https_on:
        label_text += ' https: ' + str(https_on)
    if users_from_db != [{}] and groups_from_db != [{}]:
        user_list, treedata2 = get_user_list(users_from_db)
        group_list, treedata = get_group_list(groups_from_db)
        # user_list = get_only_user_list(users_from_db)
        # group_list = get_only_group_list(groups_from_db)
    tab1_layout = [
        [sg.Button('Добавить', disabled_button_color='gray', key='-AddUser-', pad=((30, 10), (20, 5))),
         sg.Button('Удалить', disabled_button_color='gray', key='-DelUser-', pad=(10, (20, 5))),
         sg.Button('Клонировать', disabled_button_color='gray', key='-CloneUser-', pad=(10, (20, 5)))],
        [sg.Text('Фильтр: '), sg.Input(size=(20, 1), enable_events=True,
                                       disabled=True,
                                       key='-filterUser-')],
        [
            sg.Frame('Пользователи',
                     [
                         [sg.Table(user_list, headings=['id', 'Логин', 'Имя', 'Дисп', 'Адм', 'К500', 'Блок'], justification="left",
                                   # num_rows=20,
                                   key='-users-', expand_y=True, expand_x=True,
                                   enable_click_events=True,
                                   enable_events=True,
                                   # bind_return_key=True,
                                   # background_color='green',
                                   right_click_selects=True,
                                   visible_column_map=[False, True, True, True, True, True, True],
                                   right_click_menu=[1, 'Изменить пользователя'],
                                   select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                                   selected_row_colors='black on lightblue',
                                   auto_size_columns=False, col_widths=[0, 10, 20, 5, 5, 5, 5])], ],
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
                                         )]], expand_y=True,
                                         # expand_x=True
                     ),
            # sg.Multiline('', expand_x=True, expand_y=True, key='online-users', )
        ],
        [         sg.Push(),
         sg.Checkbox('Выбрать все группы', enable_events=True, key='-checkAllGroups-', default=False,
                     pad=[30, 0],
                     disabled=True),
         sg.Button('Применить', key='Apply', disabled=True,
                   disabled_button_color='gray', pad=((0, 10), (5, 10)))],
    ]
    tab2_layout = [
        [sg.Button('Добавить', disabled_button_color='gray', key='-AddGroup-', pad=((30, 10), (20, 5))),
         sg.Button('Удалить', disabled_button_color='gray', key='-DelGroup-', pad=(10, (20, 5)))],
        [sg.Text('Фильтр: '), sg.Input(size=(20, 1), enable_events=True,
                                       disabled=True,
                                       key='-filterGroup-')],
        [sg.Frame('Группы',
                  [
                      [sg.Table(group_list, headings=['id', 'Имя', 'Описание', 'Э', 'Блок'], justification="left",
                                num_rows=40, enable_events=True,
                                enable_click_events=True,
                                right_click_selects=True,
                                right_click_menu=[1, ['Изменить группу', 'Очистить чат']],
                                select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                                selected_row_colors='black on lightblue',
                                visible_column_map=[False, True, True, True, True],
                                key='-groups2-', expand_y=True, expand_x=True,
                                auto_size_columns=False, col_widths=[0, 10, 30, 5, 5])], ],
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
        ['Сервер', ['!Установить лицензию...', '!Настройки']],
        ['Помощь', 'О программе'], ], key='-Menu-')],
        [sg.Frame('Сервер', [[sg.Push(),
                              sg.Button('Старт', key='-Start-',
                                        disabled_button_color='gray',
                                        size=8,
                                        pad=((20, 10), (5, 10))),
                              sg.Button('Стоп', key='-Stop-',
                                        disabled_button_color='gray',
                                        size=8,
                                        pad=((10, 20), (5, 10))),
                              sg.Push()]], size=(200, 62), ),
        sg.Frame('Место на сервере', [[sg.Graph(canvas_size=(110, 12), graph_bottom_left=(1, 1),
                                      graph_top_right=(108, 10),
                                       k='-free-space-',
                                       pad=((20, 10), (0, 0), )),
                              sg.Text('', size=40, key='-free-space-perc-'),
                              sg.Button('Очистить частично', key='-partially-dropDB-', disabled=False,
                                       disabled_button_color='gray', pad=((0, 10), (5, 10))),
                              sg.Button('Очистить', key='-dropDB-', disabled=False,
                                       disabled_button_color='gray', pad=((0, 10), (5, 10))),]],),
         ],
        [sg.TabGroup(
            [[sg.Tab('Пользователи', tab1_layout, key="Tab1"),
              sg.Tab('Группы', tab2_layout, key="Tab2"),
              sg.Tab('Журнал', tab3_layout, key="Tab3"),
              ]], key="Tabs", size=(1000, 690), enable_events=True),
        sg.Frame('Онлайн', [[sg.Multiline('',
                                          # expand_x=True,
                                          horizontal_scroll=True,
                                          size=(20, 1),
                                          expand_y=True,
                                          key='online-users',
                                          write_only=True,
                                          disabled=True,
                                          auto_refresh=True, )]],
                 expand_x=True, expand_y=True,
                 pad=((0, 5), (18, 2)))
        ],
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
                     # sg.Input(default_text="127.0.0.1", key="ip")],
                     sg.Input(default_text="10.1.4.49", key="ip")],
                    [sg.Push(background_color='white'), sg.Text("Пароль", background_color='white'), sg.Input(
                        focus=True,
                        default_text='qwerty',
                        key="password", password_char='*')],
                    [sg.Push(), sg.Checkbox('https', default=False, key='https_on')],
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
    settings = get_settings(BASE_URL_SETTINGS)
    if settings:
        layout_settings = [
            # [
                # sg.Frame('Общие настройки',
                #       [
                #           [sg.Push(), sg.Checkbox('Запрет индивидуальных вызовов', default=False, enable_events=True,
                #                                   key='-запрет-инд-')]
                #       ], expand_x=True)
             # ],
            [sg.Frame('Таймауты',
                      [
                          [sg.Push(), sg.Text('Индивидуальный вызов (сек)'),
                           sg.Input(default_text=settings['privateCallTimeout'],
                                    size=20,
                                    key='-Индивидуальный-таймаут-',
                                    enable_events=True)],
                          [sg.Push(), sg.Text('Групповой вызов (сек)'),
                           sg.Input(default_text=settings['groupCallTimeout'],
                                                 size=20,
                                                 key='-Групповой-таймаут-',
                                                 enable_events=True)],
                          [sg.Push(), sg.Text('Таймаут окончания вызова (сек)'),
                           sg.Input(default_text=settings['finalizeCallTimeout'],
                                    size=20,
                                    key='-таймаут-окончания-',
                                    enable_events=True)],
                          [sg.Push(), sg.Text('Длительность тонального вызова (сек)'),
                           sg.Input(default_text=settings['tonalTimeout'],
                                    size=20,
                                    disabled=True, disabled_readonly_background_color=disabled_input,
                                    key='-таймаут-тонового-сигнала-',
                                    enable_events=True)],
                          [sg.Push(), sg.Text('Длительность скрытого прослушивания (сек)'),
                           sg.Input(default_text=settings['ambientCallDuration'],
                                    size=20,
                                    key='-таймаут-прослушивания-',
                                    enable_events=True)],
                          # [sg.Push(), sg.Text('Диспетчерский вызов (сек)'), sg.Input(size=20,
                          #                                                            key='-Диспетчерский-таймаут-',
                          #                                                            enable_events=True)]
                      ], expand_x=True)
             ],
            [sg.Frame('Настройка портов',
                      [
                          # [sg.Push(), sg.Text('Порт подключения'),
                          #  sg.Input(size=20, key='-порт-подкл-', enable_events=True)],
                          [sg.Push(), sg.Text('Минимальный порт аудио (UDP)'),
                           sg.Input(size=20, key='-Мин-аудио-порт-',
                                    default_text=(settings['udpPortsRange'].rpartition('-')[0] \
                                    if 6 < len(settings['udpPortsRange']) < 12 else 0),
                                    enable_events=True)],
                          [sg.Push(), sg.Text('Максимальный порт аудио (UDP)'),
                           sg.Input(size=20, key='-Макс-аудио-порт-',
                                    default_text=(settings['udpPortsRange'].rpartition('-')[2] \
                                    if 6 < len(settings['udpPortsRange']) < 12 else 0), enable_events=True)]
                      ], expand_x=True)
             ],
            [sg.Frame('Настройки сервера',
                      [
                          [sg.Push(), sg.Text('Таймаут опроса сервера, сек'),
                           sg.Input(size=20, key='-пинг-таймаут-',
                                    default_text=ping_timeout,
                                    enable_events=True)],
                      ], expand_x=True)
             ],
            [sg.Push()],
            [sg.ProgressBar(max_value=10, orientation='horizontal', key='-Progress-Bar-',
                            # visible=False,
                            # expand_x=True,
                            # expand_y=True,
                            size_px=(400, 10),
                            pad=((30, 30), (30, 10))
                            )],
            [sg.Push(), sg.Button('OK', disabled=True, key='-OK-set-'), sg.Button('Выйти', key='-Exit-set-'), sg.Push()]
        ]
    else:
        layout_settings =[
            [sg.Push(), sg.Text('Настройки недоступны', justification='center', size=60), sg.Push()],
            [sg.Push(), sg.Button('Выйти', key='-Exit-set-'), sg.Push()]
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
        [sg.Text('Логин'), sg.Push(), sg.Input(key='UserLogin', pad=((0, 40), (0, 0)), enable_events=True,
                                               tooltip=('Не больше ' + str(MAX_LEN_LOGIN) + ' символов'))],
        [sg.Text('Имя'), sg.Push(), sg.Input(key='UserName', pad=((0, 40), (2, 0)), enable_events=True,
                                             tooltip=('Не больше ' + str(MAX_LEN_USERNAME) + ' символов'))],
        [sg.Text('Пароль'), sg.Push(), sg.Input(key='UserPassword',
                                                password_char='*', enable_events=True,
                                                tooltip=('Не меньше ' + str(MIN_LEN_PASSWORD) + ' и не больше '
                                                         + str(MAX_LEN_PASSWORD) + ' символов')),
         sg.Button(key='showPassword',
                   button_color='#ffffff',
                   image_data=ICON_BLANK_BASE_64,
                   disabled=True)],
        # [sg.Push(), sg.Text('Показать пароль', key='showPasswordText'), sg.Button(key='showPassword',
        #                                                                           button_color='#ffffff',
        #                                                                           image_data=ICON_SHOW_BASE_64)],
        [sg.Frame('Тип', [
                          [sg.Radio('Пользователь',
                                    default=True,
                                    key='user',
                                    group_id='u_type',
                                    enable_events=True)],
                          [sg.Radio('Диспетчер', key='disp', group_id='u_type', enable_events=True)],
                          [sg.Radio('Концентратор К500', key='gw', group_id='u_type', enable_events=True)],
                          [sg.Radio('Администратор', key='adm', group_id='u_type', enable_events=True)]],
         size=(300, 140), pad=((8, 0), (10, 10)))],
        [sg.Frame('Дополнительные разрешения', [
            [sg.Checkbox('Разрешить индивидуальные вызовы',
                     default=True,
                     enable_events=True,
                     key='addUserIndCallEn'), sg.Push()],
            [sg.Checkbox('Разрешить удалять переписку в чатах',
                     default=False,
                     disabled=True,
                     enable_events=True,
                     key='addUserAllowDelChats'), sg.Push()],
            [sg.Checkbox('Разрешить удалять данные БД',
                     default=False,
                     disabled=True,
                     enable_events=True,
                     key='addUserAllowPartialDrop'), sg.Push()]
            ],
         size=(300, 110), pad=((8, 0), (10, 10)))],
        [sg.Text('Приоритет'), sg.Input(key='UserPriority', size=(4, 1), enable_events=True,
                                              tooltip=('От 1 до 15'))],
        [sg.Push(), sg.Checkbox('Заблокирован',
                     default=False,
                     disabled=False,
                     text_color='red',
                     enable_events=True,
                     key='addUserBlock')],
        # [sg.Checkbox('Диспетчер', default=False, key='addUserDispatcher'), sg.Push()],
        [sg.Push(), sg.Button(button_text='Создать', key='addUserButton',
                              disabled=True,
                              disabled_button_color='gray')]
    ]
    return sg.Window('Добавить пользователя', layout_add_user,
                     icon=ICON_BASE_64,
                     use_ttk_buttons=True,
                     finalize=True,
                     disable_minimize=True,
                     modal=True)


def make_modify_user_window(user: dict):
    layout_modify_user = [
        [sg.Text('Логин'), sg.Push(), sg.Input(disabled=True, pad=((0, 40), (0, 0)),
                                               default_text=user['login'], key='UserModifyLogin')],
        [sg.Text('Имя'), sg.Push(), sg.Input(default_text=user['name'],
                                             pad=((0, 40), (2, 0)), enable_events=True, key='UserModifyName',
                                             tooltip=('Не больше ' + str(MAX_LEN_USERNAME) + ' символов'))],
        [sg.Text('Пароль'), sg.Push(), sg.Input(default_text='', enable_events=True,
                                                key='userModifyPassword', password_char='*',
                                                tooltip=('Не меньше ' + str(MIN_LEN_PASSWORD) + ' и не больше '
                                                         + str(MAX_LEN_PASSWORD) + ' символов')),
         sg.Button(key='showModifyPassword',
                   button_color='#ffffff',
                   image_data=ICON_BLANK_BASE_64,
                   disabled=True)],
        [sg.Frame('Тип', [
                  [sg.Radio('Пользователь',
                            default=True,
                            key='modifyUserUser',
                            group_id='u_type',
                            disabled=True if user['is_blocked'] or user['is_admin'] else False,
                            enable_events=True)],
                  [sg.Radio('Диспетчер',
                            default=user['is_dispatcher'],
                            key='modifyUserDispatcher',
                            group_id='u_type',
                            disabled=True if user['is_blocked'] or user['is_admin'] else False,
                            enable_events=True)],
                  [sg.Radio('Концентратор К500',
                            default=user['is_gw'],
                            key='modifyUserGw',
                            group_id='u_type',
                            disabled=True if user['is_blocked'] or user['is_admin'] else False,
                            enable_events=True)],
                  [sg.Radio('Администратор',
                            default=user['is_admin'],
                            key='modifyUserAdm',
                            group_id='u_type',
                            disabled=True,
                            enable_events=True)]],
         size=(300, 140), pad=((8, 0), (10, 10)))],
        [sg.Frame('Дополнительные разрешения', [
            [sg.Checkbox('Разрешить индивидуальные вызовы',
                     default=False if user['is_admin'] else user['en_ind'],
                     enable_events=True,
                     disabled=True if user['is_admin'] else False,
                     key='modifyUserIndCallEn'), sg.Push()],
            [sg.Checkbox('Разрешить удалять переписку в чатах',
                     default=True if user['is_admin'] else user['en_partial_drop'],
                     disabled=False if user['is_dispatcher'] else True,
                     enable_events=True,
                     key='modifyUserAllowDelChats'), sg.Push()],
            [sg.Checkbox('Разрешить удалять данные БД',
                     default=True if user['is_admin'] else user['en_partial_drop'],
                     disabled=False if user['is_dispatcher'] else True,
                     enable_events=True,
                     key='modifyUserAllowPartialDrop'), sg.Push()]
            ],
         size=(300, 110), pad=((8, 0), (10, 10)))],
        [sg.Text('Приоритет'), sg.Input(key='UserModifyPriority',
                                        default_text=user['priority'],
                                        size=(4, 1),
                                        disabled=True if user['is_admin'] else False,
                                        enable_events=True,
                                        tooltip=('От 1 до 15'))],
        [sg.Push(), sg.Checkbox('Заблокирован',
                     default=user['is_blocked'],
                     disabled=True if user['is_admin'] else False,
                     text_color='red',
                     enable_events=True,
                     key='modifyUserBlock')],
        # [sg.Text('Таймаут (сек)', size=(13)), sg.Input(size=(10), enable_events=True, key='userTimeout')],
        [sg.Push(), sg.Button(button_text='Изменить', key='modifyUserButton',
                          disabled=True,
                          disabled_button_color='gray')]
    ]
    return sg.Window('Изменить пользователя', layout_modify_user,
                    icon=ICON_BASE_64,
                    use_ttk_buttons=True,
                    finalize=True,
                    disable_minimize=True,
                    modal=True)


def make_modify_group_window(group: dict):
    layout_modify_group = [
        [sg.Push(), sg.Text('Имя Группы'),
         sg.Input(size=(40, 1), default_text=group['name'],
                  disabled=True,
                  enable_events=True,
                  key='GroupModifyName')],
        [sg.Push(), sg.Text('Описание Группы'),
         sg.Multiline(enter_submits=True, no_scrollbar=True, size=(40, 3),
                      default_text=group['desc'],
                      enable_events=True,
                      key='GroupModifyDesc')],
        [sg.Button(button_text='Очистить чат', key='modifyGroupDelChat'), sg.Push(),
         sg.Checkbox('Экстренная', default=group['is_emergency'],
                     enable_events=True,
                     key='GroupModifyEmergency')],
        [sg.Push(), sg.Checkbox('Заблокировать', text_color='red',
                                enable_events=True,
                                default=group['is_disabled'],
                                key='GroupModifyBlocked')],
        [sg.Push(), sg.Button(button_text='Изменить',
                          disabled=True,
                          disabled_button_color='gray',
                          key='modifyGroupButton')]
    ]
    win = sg.Window('Изменить группу', layout_modify_group, icon=ICON_BASE_64,
                    use_ttk_buttons=True,
                    disable_minimize=True,
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
        [sg.Text('Логин'), sg.Push(), sg.Input(key='CloneUserLogin', pad=((0, 40), (0, 0)), enable_events=True,
                                               tooltip=('Не больше ' + str(MAX_LEN_LOGIN) + ' символов'))],
        [sg.Text('Имя'), sg.Push(), sg.Input(key='CloneUserName', pad=((0, 40), (2, 0)), enable_events=True,
                                             tooltip=('Не больше ' + str(MAX_LEN_USERNAME) + ' символов'))],
        [sg.Text('Пароль'), sg.Push(), sg.Input(key='CloneUserPassword', password_char='*', enable_events=True,
                                                tooltip=('Не меньше ' + str(MIN_LEN_PASSWORD) + ' и не больше '
                                                         + str(MAX_LEN_PASSWORD) + ' символов')),
         sg.Button(key='CloneUserShowPassword',
                   button_color='#ffffff',
                   image_data=ICON_BLANK_BASE_64,
                   disabled=True)],
        [sg.Push(), sg.Ok(button_text='Клонировать', key='cloneUserButton')]
    ]
    return sg.Window(('Клонировать пользователя ' + user), layout_clone_user, icon=ICON_BASE_64, use_ttk_buttons=True,
                     finalize=True, modal=True)


def make_add_group_window():
    layout_add_group = [
        [sg.Push(), sg.Text('Имя Группы'), sg.Input(size=(40, 1), key='GroupName',
                                                    enable_events=True,
                                                    tooltip=('Не больше ' + str(MAX_LEN_GROUPNAME) + ' символов'))],
        [sg.Push(), sg.Text('Описание Группы'),
         sg.Multiline(enter_submits=True, no_scrollbar=True, size=(40, 3), key='description',
                      enable_events=True,
                      tooltip=('Не больше ' + str(MAX_LEN_GROUPDESC) + ' символов'))],
        [sg.Push(), sg.Checkbox('Экстренная', key='emergency',
                                enable_events=True,
                                pad=(0, 10))],
        [sg.Push(), sg.Checkbox('Заблокирована',
                                default=False,
                                disabled=False,
                                text_color='red',
                                enable_events=True,
                                key='addGroupBlock')],
        [sg.Push(), sg.Button(button_text='Создать', disabled=True, key='addGroupButton',
                          disabled_button_color='gray')]
    ]
    return sg.Window('Добавить группу', layout_add_group, icon=ICON_BASE_64, use_ttk_buttons=True,
                     finalize=True,
                     disable_minimize=True,
                     modal=True)


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
        [sg.Push(), sg.Button('Да', key="okExit", pad=((0, 10), (10, 10)), size=10),
         sg.Button('Нет', key='noExit', pad=((10, 0), (10, 10)), size=10), sg.Push()]
    ]
    return sg.Window('Выход', layout_exit, icon=ICON_BASE_64,
                     disable_minimize=True,
                     use_ttk_buttons=True,
                     finalize=True, modal=True)

def make_confirm_window(message):
    layout_exit = [
        [sg.Text(message)],
        [sg.Push(), sg.Button('Да', key="okExit", pad=((0, 10), (10, 10)), size=10),
         sg.Button('Нет', key='noExit', pad=((10, 0), (10, 10)), size=10), sg.Push()]
    ]
    return sg.Window('Подтверждение', layout_exit, icon=ICON_BASE_64,
                     disable_minimize=True,
                     use_ttk_buttons=True,
                     finalize=True, modal=True)


def get_online_users(users: list):
    usernames = []
    for user in users:
        username = get_user_name_by_id_from_db(user)
        if username is not None:
            usernames.append(username)
    return "\n".join(sorted(usernames))



def set_window_running_server():
    bar_text = 'Пользователей онлайн: ' + str(server_status['online']) + ', Версия БД: ' + str(server_status['db'])
    window['-StatusBar-'].update(bar_text, background_color=status_bar_color)
    window['-Menu-'].update([
                        ['Сервер', ['Установить лицензию...', 'Настройки']],
                        ['Помощь', 'О программе'], ])
    update_free_space(server_status)
    window['online-users'].update(get_online_users(server_status['onlineUserIds']))


def set_window_not_running_server():
    window['-StatusBar-'].update('Сервер не доступен', background_color=button_color_2)
    window['-AddUser-'].update(disabled=True)
    window['-DelUser-'].update(disabled=True)
    window['-CloneUser-'].update(disabled=True)
    window['-AddGroup-'].update(disabled=True)
    window['-DelGroup-'].update(disabled=True)
    window['-filterUser-'].update(disabled=True)
    window['-filterGroup-'].update(disabled=True)
    window['-partially-dropDB-'].update(disabled=True)
    window['-dropDB-'].update(disabled=True)
    window.Element('-Start-').SetFocus()


def the_thread(ip):
    try:
        sleep(5)
        num = 0
        print('Запускаем поток')
        while True:
            # if num == 3:
            #     raise Exception('alarm!')
            res_ping = ''
            global change_state
            change_state = False
            # print(f" Thread {num} before - {server_status['last_state']}")
            try:
                res_ping = requests.get(ip, timeout=3)
            except Exception as e:
                print(f'Сервер не доступен {e}')
            print(res_ping)
            if res_ping == '':
                if server_status['run']:
                    logging.info(f'[{num}] Сервер НЕ доступен ')
                    change_state = True
                default_status_dict = {"onlineUsersCount": '',
                                       "databaseVersion": '',
                                       'run': server_status['run'],
                                       'freeSpace': 0,
                                       'spaceTotal': 1,
                                       'onlineUserIds': []}
                default_json = json.dumps(default_status_dict)
                print(f' Thread {num} after - {default_status_dict}')
                window.write_event_value('-THREAD-', (threading.currentThread().name, default_json))
            else:
                if res_ping.status_code == 200:
                    if not server_status['run']:
                        logging.info(f'[{num}] Сервер доступен ')
                        change_state = True
                    print(f' Thread {num} after - {res_ping.text}')
                    window.write_event_value('-THREAD-', (threading.currentThread().name, res_ping.text))
                    # server_status['run'] = True
            num += 1
            sleep(ping_timeout)
    except Exception as e:
        global thread_started
        thread_started = False
        print(f'Exception! {e}, thread_started = {thread_started}')
        window.write_event_value('-THREAD-', (threading.currentThread().name, json.dumps({'restart': 'true'})))


def check_server(url_ping):
    status = {
              # 'last_state': False,
              'run': False,
              'online': '',
              'db': '',
              'freeSpace': 0,
              'spaceTotal': 1,
              'onlineUserIds': []}
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
            # status['last_state'] = True
            status['freeSpace'] = res_dict['freeSpace']
            status['spaceTotal'] = res_dict['spaceTotal']
            status['onlineUserIds'] = res_dict['onlineUserIds']
            print(status)
        else:
            print(f'Некорректный ответ {res_ping.status_code} от сервера {url_ping}')
    return status


def get_token(url_auth):
    token = ''
    res_auth = ''
    dict_auth = {'login': 'admin', 'password': 'qwerty'} #TODO
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


def get_settings(url):
    res = ''
    res_dict = dict()
    try:
        res = requests.get(url, timeout=3, headers=HEADER_dict)
    except Exception as e:
        print(f"Ошибка подключения. {e}")
    if res == '':
        print('Сервер не отвечает')
        logging.info(f'Сервер НЕ доступен при запуске приложения')
        # status['last_state'] = False
    else:
        if res.status_code == 200:
            res_dict = json.loads(res.text)
        else:
            print(f'Некорректный ответ {res.status_code} от сервера {url}')
    return res_dict

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


# def get_icon():
#     try:
#         icon_logo = Image.open('logo.ico')
#     except FileNotFoundError:
#         print('Файл не найден')
#         logging.error('Файл логотипа не найден!')
#     # print(icon_logo.format, icon_logo.size, icon_logo.mode)
#     return icon_logo


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


def block_user(set, id):
    user_dict = {'id': id}
    if set:
        res = requests.post(BASE_URL +
                                     'disableUser',
                                     json=user_dict,
                                     headers=HEADER_dict)
    else:
        res = requests.post(BASE_URL +
                                     'enableUser',
                                     json=user_dict,
                                     headers=HEADER_dict)
    return res


def block_group(set, id):
    group_dict = {'id': id}
    if set:
        res = requests.post(BASE_URL +
                                     'disableGroup',
                                     json=group_dict,
                                     headers=HEADER_dict)
    else:
        res = requests.post(BASE_URL +
                                     'enableGroup',
                                     json=group_dict,
                                     headers=HEADER_dict)
    return res



def disable_input(win):
    win['-OK-set-'].update(disabled=True)
    win['-Exit-set-'].update(disabled=True)
    win['-Индивидуальный-таймаут-'].update(disabled=True)
    win['-Групповой-таймаут-'].update(disabled=True)
    win['-таймаут-окончания-'].update(disabled=True)
    win['-таймаут-тонового-сигнала-'].update(disabled=True)
    win['-таймаут-прослушивания-'].update(disabled=True)
    win.DisableClose = True


def enable_input(win):
    win['-OK-set-'].update(disabled=False)
    win['-Exit-set-'].update(disabled=False)
    win['-Индивидуальный-таймаут-'].update(disabled=False)
    win['-Групповой-таймаут-'].update(disabled=False)
    win['-таймаут-окончания-'].update(disabled=False)
    # win['-таймаут-тонового-сигнала-'].update(disabled=False)
    win['-таймаут-прослушивания-'].update(disabled=False)
    win.DisableClose = False


def change_role(role: Enum, set: int, id):
    user_dict = {'userIds': [id], 'roles': [role.value]}
    if set:
        res_modify_user_role = requests.post(BASE_URL +
                                               'addToRole',
                                               json=user_dict,
                                               headers=HEADER_dict)
    else:
        res_modify_user_role = requests.post(BASE_URL +
                                               'removeFromRole',
                                               json=user_dict,
                                               headers=HEADER_dict)
    return res_modify_user_role


def change_user_type(id, user_type):
    user_dict = {'userId': id, 'userType': int(user_type)}
    res = requests.post(BASE_URL +
                                                'changeUserType',
                                                json=user_dict,
                                                headers=HEADER_dict)
    return res


def my_popup(message):
    layout = [[sg.Frame('', [[sg.Text(message, background_color=omega_theme['INPUT'])],
              [sg.Push(background_color=omega_theme['INPUT']), sg.Button('OK', pad=((0, 0), (10, 10))),
               sg.Push(background_color=omega_theme['INPUT'])]], background_color=omega_theme['INPUT'],
                        pad=((7, 7), (10, 10)))]]
    sg.Window('Инфо', layout,
              icon=ICON_BASE_64,
              use_ttk_buttons=True,
              no_titlebar=True,
              border_depth=5,
              grab_anywhere=True,
              background_color=omega_theme['INPUT'],
              # background_color='dark gray',
              finalize=True,
              # use_default_focus=False,
              disable_minimize=True,
              modal=True).read(close=True)


def validate(window: str):
    result = True
    if window == 'add_user':
        print(val_add_user)
        if 0 < len(str(val_add_user['UserLogin'])) <= MAX_LEN_LOGIN:
            window_add_user['UserLogin'].update(background_color=omega_theme['BACKGROUND'],
                                                text_color=omega_theme['TEXT'])
        else:
            my_popup(("Логин должен быть не более " + str(MAX_LEN_LOGIN) + " символов"))
            window_add_user.Element('UserLogin').SetFocus()
            window_add_user['UserLogin'].update(background_color=button_color_2,
                                                text_color=omega_theme['BACKGROUND'])
            return False
        if 0 < len(str(val_add_user['UserName'])) <= MAX_LEN_USERNAME:
            window_add_user['UserName'].update(background_color=omega_theme['BACKGROUND'],
                                               text_color=omega_theme['TEXT'])
        else:
            my_popup(("Имя должно быть не более " + str(MAX_LEN_USERNAME) + " символов"))
            window_add_user.Element('UserName').SetFocus()
            window_add_user['UserName'].update(background_color=button_color_2,
                                               text_color=omega_theme['BACKGROUND'])
            return False
        if MIN_LEN_PASSWORD <= len(str(val_add_user['UserPassword'])) <= MAX_LEN_PASSWORD:
            window_add_user['UserPassword'].update(background_color=omega_theme['BACKGROUND'],
                                                   text_color=omega_theme['TEXT'])
        else:
            my_popup(("Пароль должен быть не менее " + str(MIN_LEN_PASSWORD) + " и не более "
                      + str(MAX_LEN_PASSWORD) + " символов"))
            window_add_user.Element('UserPassword').SetFocus()
            window_add_user['UserPassword'].update(background_color=button_color_2,
                                                   text_color=omega_theme['BACKGROUND'])
            return False
        if val_add_user['UserPriority'] == '':
            result = True
        elif val_add_user['UserPriority'].isdigit() or val_add_user['UserPriority'] == '':
            if 0 <= int((val_add_user['UserPriority'])) <= 15:
                window_add_user['UserPriority'].update(background_color=omega_theme['BACKGROUND'],
                                                       text_color=omega_theme['TEXT'])
            else:
                my_popup(("Приоритет должен быть от 0 до 15"))
                window_add_user.Element('UserPriority').SetFocus()
                window_add_user['UserPriority'].update(background_color=button_color_2,
                                                       text_color=omega_theme['BACKGROUND'])
                return False
        else:
            my_popup(("Приоритет должен быть числом от 0 до 15"))
            window_add_user.Element('UserPriority').SetFocus()
            window_add_user['UserPriority'].update(background_color=button_color_2,
                                                   text_color=omega_theme['BACKGROUND'])
            return False
    elif window == 'modify_user':
        print(val_modify_user)
        if 0 < len(str(val_modify_user['UserModifyName'])) <= MAX_LEN_USERNAME:
            window_modify_user['UserModifyName'].update(background_color=omega_theme['BACKGROUND'],
                                               text_color=omega_theme['TEXT'])
        else:
            my_popup(("Имя должно быть не более " + str(MAX_LEN_USERNAME) + " символов"))
            window_modify_user.Element('UserModifyName').SetFocus()
            window_modify_user['UserModifyName'].update(background_color=button_color_2,
                                               text_color=omega_theme['BACKGROUND'])
            return False
        if not val_modify_user['userModifyPassword'] == '':
            if MIN_LEN_PASSWORD <= len(str(val_modify_user['userModifyPassword'])) <= MAX_LEN_PASSWORD:
                window_modify_user['userModifyPassword'].update(background_color=omega_theme['BACKGROUND'],
                                                       text_color=omega_theme['TEXT'])
            else:
                my_popup(("Пароль должен быть не менее " + str(MIN_LEN_PASSWORD) + " и не более "
                          + str(MAX_LEN_PASSWORD) + " символов"))
                window_modify_user.Element('userModifyPassword').SetFocus()
                window_modify_user['userModifyPassword'].update(background_color=button_color_2,
                                                       text_color=omega_theme['BACKGROUND'])
                return False
        if val_modify_user['UserModifyPriority'] == '':
            result = True
        elif val_modify_user['UserModifyPriority'].isdigit() or val_modify_user['UserModifyPriority'] == '':
            if 0 <= int((val_modify_user['UserModifyPriority'])) <= 15:
                window_modify_user['UserModifyPriority'].update(background_color=omega_theme['BACKGROUND'],
                                                       text_color=omega_theme['TEXT'])
            else:
                my_popup(("Приоритет должен быть от 0 до 15"))
                window_modify_user.Element('UserModifyPriority').SetFocus()
                window_modify_user['UserModifyPriority'].update(background_color=button_color_2,
                                                       text_color=omega_theme['BACKGROUND'])
                return False
        else:
            my_popup(("Приоритет должен быть числом от 0 до 15"))
            window_modify_user.Element('UserModifyPriority').SetFocus()
            window_modify_user['UserModifyPriority'].update(background_color=button_color_2,
                                                   text_color=omega_theme['BACKGROUND'])
            return False
    if window =='add_group':
        print(val_add_group)
        if 0 < len(str(val_add_group['GroupName'])) <= MAX_LEN_GROUPNAME:
            window_add_group['GroupName'].update(background_color=omega_theme['BACKGROUND'],
                                               text_color=omega_theme['TEXT'])
        else:
            my_popup(("Имя должно быть не более " + str(MAX_LEN_GROUPNAME) + " символов"))
            window_add_group.Element('GroupName').SetFocus()
            window_add_group['GroupName'].update(background_color=button_color_2,
                                               text_color=omega_theme['BACKGROUND'])
            return False
        if 0 <= len(str(val_add_group['description'])) <= MAX_LEN_GROUPDESC:
            window_add_group['description'].update(background_color=omega_theme['BACKGROUND'],
                                               text_color=omega_theme['TEXT'])
        else:
            my_popup(("Имя должно быть не более " + str(MAX_LEN_GROUPDESC) + " символов"))
            window_add_group.Element('description').SetFocus()
            window_add_group['description'].update(background_color=button_color_2,
                                               text_color=omega_theme['BACKGROUND'])
            return False
    if window == 'modify_group':
        print(val_modify_group)
        if 0 < len(str(val_modify_group['GroupModifyName'])) <= MAX_LEN_GROUPNAME:
            window_modify_group['GroupModifyName'].update(background_color=omega_theme['BACKGROUND'],
                                                 text_color=omega_theme['TEXT'])
        else:
            my_popup(("Имя должно быть не более " + str(MAX_LEN_GROUPNAME) + " символов"))
            window_modify_group.Element('GroupModifyName').SetFocus()
            window_modify_group['GroupModifyName'].update(background_color=button_color_2,
                                                 text_color=omega_theme['BACKGROUND'])
            return False
        if 0 <= len(str(val_modify_group['GroupModifyDesc'])) <= MAX_LEN_GROUPDESC:
            window_modify_group['GroupModifyDesc'].update(background_color=omega_theme['BACKGROUND'],
                                                   text_color=omega_theme['TEXT'])
        else:
            my_popup(("Имя должно быть не более " + str(MAX_LEN_GROUPDESC) + " символов"))
            window_modify_group.Element('GroupModifyDesc').SetFocus()
            window_modify_group['GroupModifyDesc'].update(background_color=button_color_2,
                                                   text_color=omega_theme['BACKGROUND'])
            return False
    if window == 'settings':
        print(val_set)
        if MIN_CALL_TM <= int(val_set['-Индивидуальный-таймаут-']) <= MAX_CALL_TM:
            window_settings['-Индивидуальный-таймаут-'].update(background_color=omega_theme['BACKGROUND'],
                                                 text_color=omega_theme['TEXT'])
        else:
            my_popup(("Длительность индивидуального вызова должна быть не менее " + str(MIN_CALL_TM) + " и не более " + str(MAX_CALL_TM) + " секунд"))
            window_settings.Element('-Индивидуальный-таймаут-').SetFocus()
            window_settings['-Индивидуальный-таймаут-'].update(background_color=button_color_2,
                                                 text_color=omega_theme['BACKGROUND'])
            return False
        if 10 <= int(val_set['-Групповой-таймаут-']) <= 120:
            window_settings['-Групповой-таймаут-'].update(background_color=omega_theme['BACKGROUND'],
                                                 text_color=omega_theme['TEXT'])
        else:
            my_popup(("Длительность группового вызова должна быть не менее " + str(MIN_CALL_TM) + " и не более " + str(
                MAX_CALL_TM) + " секунд"))
            window_settings.Element('-Групповой-таймаут-').SetFocus()
            window_settings['-Групповой-таймаут-'].update(background_color=button_color_2,
                                                               text_color=omega_theme['BACKGROUND'])
            return False
        if MIN_CALL_END_TM <= int(val_set['-таймаут-окончания-']) <= MAX_CALL_END_TM:
            window_settings['-таймаут-окончания-'].update(background_color=omega_theme['BACKGROUND'],
                                                 text_color=omega_theme['TEXT'])
        else:
            my_popup(("Таймаут окончания вызова должен быть не менее " + str(MIN_CALL_END_TM) + " и не более " + str(
                MAX_CALL_END_TM) + " секунд"))
            window_settings.Element('-таймаут-окончания-').SetFocus()
            window_settings['-таймаут-окончания-'].update(background_color=button_color_2,
                                                               text_color=omega_theme['BACKGROUND'])
            return False
        if MIN_TONAL_CALL_END_TM <= int(val_set['-таймаут-тонового-сигнала-']) <= MAX_TONAL_CALL_END_TM:
            window_settings['-таймаут-тонового-сигнала-'].update(background_color=omega_theme['BACKGROUND'],
                                                 text_color=omega_theme['TEXT'])
        else:
            my_popup(("Длительность тонального вызова должна быть не менее " + str(MIN_TONAL_CALL_END_TM) + " и не более " + str(
                MAX_TONAL_CALL_END_TM) + " секунд"))
            window_settings.Element('-таймаут-тонового-сигнала-').SetFocus()
            window_settings['-таймаут-тонового-сигнала-'].update(background_color=button_color_2,
                                                               text_color=omega_theme['BACKGROUND'])
            return False
        if MIN_AMB_LIST_TM <= int(val_set['-таймаут-прослушивания-']) <= MAX_AMB_LIST_TM:
            window_settings['-таймаут-прослушивания-'].update(background_color=omega_theme['BACKGROUND'],
                                                 text_color=omega_theme['TEXT'])
        else:
            my_popup(("Длительность скрытого прослушивания должна быть не менее " + str(MIN_AMB_LIST_TM) + " и не более " + str(
                MAX_AMB_LIST_TM) + " секунд"))
            window_settings.Element('-таймаут-прослушивания-').SetFocus()
            window_settings['-таймаут-прослушивания-'].update(background_color=button_color_2,
                                                               text_color=omega_theme['BACKGROUND'])
            return False
        if MIN_AUDIO_PORT <= int(val_set['-Мин-аудио-порт-']) <= MAX_AUDIO_PORT:
            window_settings['-Мин-аудио-порт-'].update(background_color=omega_theme['BACKGROUND'],
                                                 text_color=omega_theme['TEXT'])
        else:
            my_popup(("Порт должен быть не менее " + str(MIN_AUDIO_PORT) + " и не более " + str(
                MAX_AUDIO_PORT) + " секунд"))
            window_settings.Element('-Мин-аудио-порт-').SetFocus()
            window_settings['-Мин-аудио-порт-'].update(background_color=button_color_2,
                                                               text_color=omega_theme['BACKGROUND'])
            return False
        if MIN_AUDIO_PORT <= int(val_set['-Макс-аудио-порт-']) <= MAX_AUDIO_PORT:
            window_settings['-Макс-аудио-порт-'].update(background_color=omega_theme['BACKGROUND'],
                                                 text_color=omega_theme['TEXT'])
        else:
            my_popup(("Порт должен быть не менее " + str(MIN_AUDIO_PORT) + " и не более " + str(
                MAX_AUDIO_PORT) + " секунд"))
            window_settings.Element('-Макс-аудио-порт-').SetFocus()
            window_settings['-Макс-аудио-порт-'].update(background_color=button_color_2,
                                                               text_color=omega_theme['BACKGROUND'])
            return False
        if MIN_PORTS <= int(val_set['-Макс-аудио-порт-']) - int(val_set['-Мин-аудио-порт-']) <= MAX_PORTS:
            pass
        else:
            my_popup(("Диапазон портов должен быть не менее " + str(MIN_PORTS) + " и не более " + str(
                MAX_PORTS) + " секунд"))
            window_settings.Element('-Мин-аудио-порт-').SetFocus()
            window_settings['-Макс-аудио-порт-'].update(background_color=button_color_2,
                                                        text_color=omega_theme['BACKGROUND'])
            window_settings['-Мин-аудио-порт-'].update(background_color=button_color_2,
                                                       text_color=omega_theme['BACKGROUND'])
            return False
        if MIN_PING_TM <= int(val_set['-пинг-таймаут-']) <= MAX_PING_TM:
            window_settings['-пинг-таймаут-'].update(background_color=omega_theme['BACKGROUND'],
                                                 text_color=omega_theme['TEXT'])
        else:
            my_popup(("Интервал пинга должен быть не менее " + str(MIN_PING_TM) + " и не более " + str(
                MAX_PING_TM) + " секунд"))
            window_settings.Element('-пинг-таймаут-').SetFocus()
            window_settings['-пинг-таймаут-'].update(background_color=button_color_2,
                                                               text_color=omega_theme['BACKGROUND'])
            return False
    if window == 'clone_user':
        print(val_clone_user)
        if 0 < len(str(val_clone_user['CloneUserLogin'])) <= MAX_LEN_LOGIN:
            window_clone_user['CloneUserLogin'].update(background_color=omega_theme['BACKGROUND'],
                                                text_color=omega_theme['TEXT'])
        else:
            my_popup(("Логин должен быть не более " + str(MAX_LEN_LOGIN) + " символов"))
            window_clone_user.Element('CloneUserLogin').SetFocus()
            window_clone_user['CloneUserLogin'].update(background_color=button_color_2,
                                                text_color=omega_theme['BACKGROUND'])
            return False
        if 0 < len(str(val_clone_user['CloneUserName'])) <= MAX_LEN_USERNAME:
            window_clone_user['CloneUserName'].update(background_color=omega_theme['BACKGROUND'],
                                               text_color=omega_theme['TEXT'])
        else:
            my_popup(("Имя должно быть не более " + str(MAX_LEN_USERNAME) + " символов"))
            window_clone_user.Element('CloneUserName').SetFocus()
            window_clone_user['CloneUserName'].update(background_color=button_color_2,
                                               text_color=omega_theme['BACKGROUND'])
            return False
        if MIN_LEN_PASSWORD <= len(str(val_clone_user['CloneUserPassword'])) <= MAX_LEN_PASSWORD:
            window_clone_user['CloneUserPassword'].update(background_color=omega_theme['BACKGROUND'],
                                                   text_color=omega_theme['TEXT'])
        else:
            my_popup(("Пароль должен быть не менее " + str(MIN_LEN_PASSWORD) + " и не более "
                      + str(MAX_LEN_PASSWORD) + " символов"))
            window_clone_user.Element('CloneUserPassword').SetFocus()
            window_clone_user['CloneUserPassword'].update(background_color=button_color_2,
                                                   text_color=omega_theme['BACKGROUND'])
            return False
    return result


def get_user_type(window):
    result = user_type['user']
    if window == 'add_user':
        if val_add_user['disp']:
            result = user_type['dispatcher']
            return result
        elif val_add_user['gw']:
            result = user_type['box']
            return result
        elif val_add_user['adm']:
            result = user_type['admin']
            return result
        elif val_add_user['user']:
            return result
    elif window == 'modify_user':
        if val_modify_user['modifyUserDispatcher']:
            result = user_type['dispatcher']
            return result
        elif val_modify_user['modifyUserGw']:
            result = user_type['box']
            return result
        elif val_modify_user['modifyUserAdm']:
            result = user_type['admin']
            return result
        elif val_modify_user['modifyUserUser']:
            return result
    elif type(window) is dict:
        if window['is_dispatcher']:
            result = user_type['dispatcher']
            return result
        elif window['is_gw']:
            result = user_type['box']
            return result
        elif window['is_admin']:
            result = user_type['admin']
            return result
    return result


def update_users():
    users_from_server = get_users_from_server()
    add_users(users_from_server)
    global users_from_db
    users_from_db = get_users_from_db()
    users_from_db.sort(key=lambda i: i['login'])
    # user_list = list()
    drop_db('user_in_groups')
    add_user_in_groups(users_from_server)
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


def update_groups():
    add_groups(get_groups_from_server())
    global groups_from_db
    groups_from_db = get_groups_from_db()
    groups_from_db.sort(key=lambda i: i['name'])
    group_list, treedata_update_group = get_group_list(groups_from_db)
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


def update_users_and_groups():
    init_db()
    global users_from_db
    users_from_db = get_users_from_db()
    global groups_from_db
    groups_from_db = get_groups_from_db()
    users_from_db.sort(key=lambda i: i['login'])
    groups_from_db.sort(key=lambda i: i['name'])
    treedata_update_group = sg.TreeData()
    if users_from_db != [[]]:
        user_list, treedata_update_user = get_user_list(users_from_db)
    if groups_from_db != [[]]:
        group_list, treedata_update_group = get_group_list(groups_from_db)
    window['-users-'].update(user_list)
    window['-TREE2-'].update(treedata_update_user)
    window['-groups2-'].update(group_list)
    window['-TREE-'].update(treedata_update_group)



def update_free_space(status):
    graph: sg.Graph = window[
        '-free-space-']  # TODO: no server_status['spaceTotal'] if server was not available on startup
    nonfree_space_perc = round((status['spaceTotal'] -
                                status['freeSpace']) * 100 / status['spaceTotal'], 1)
    graph.draw_rectangle(top_left=(0, 10),
                         bottom_right=(int(nonfree_space_perc), 0),
                         fill_color=button_color_2,
                         line_width=0)
    graph.draw_rectangle(top_left=(int(nonfree_space_perc), 10),
                         bottom_right=(100, 0),
                         fill_color=status_bar_color,
                         line_width=0)
    upd_t = str(round((100 - nonfree_space_perc), 1)) + '% (' \
            + str(round(status['freeSpace'] / 1024 / 1024 / 1024, 1)) \
            + ' Гб) свободного места на сервере'
    window['-free-space-perc-'].update(upd_t)


def set_buttons_disabled(set=True):
    window['-AddUser-'].update(disabled=set)
    window['-DelUser-'].update(disabled=set)
    window['-CloneUser-'].update(disabled=set)
    window['-AddGroup-'].update(disabled=set)
    window['-DelGroup-'].update(disabled=set)
    # window['-filterUser-'].update(disabled=set)
    # window['-filterGroup-'].update(disabled=set)
    window['Apply'].update(disabled=True)
    window['Apply2'].update(disabled=True)
    window['-checkAllGroups-'].update(disabled=set)
    window['-checkAllUsers-'].update(disabled=set)
    window['-partially-dropDB-'].update(disabled=set)
    window['-dropDB-'].update(disabled=set)


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
                   'PROGRESS': ('#699349', '#D0D0D0'),
                   'BORDER': 1,
                   'SLIDER_DEPTH': 0,
                   'PROGRESS_DEPTH': 0}
    button_color = omega_theme['BUTTON'][1]
    button_color_2 = '#a6674c'
    status_bar_color = '#699349'
    disabled_input = 'dark gray'
    sg.theme_add_new('OmegaTheme', omega_theme)
    sg.theme('OmegaTheme')
    if sys.version_info[1] < 9:
        logging.basicConfig(filename='admin.log', filemode='a', format='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)
    else:
        logging.basicConfig(filename='admin.log', filemode='a', format='%(asctime)s %(levelname)s %(message)s',
                            encoding='cp1251', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)
    logging.info('Старт лога')
    window_login = make_login_window()
    # window_main_active = False
    while True:
        break_flag = False
        break_flag2 = False
        ev_login, val_login = window_login.Read()
        # print(ev_login, val_login)
        if ev_login == sg.WIN_CLOSED or ev_login == 'Exit':
            break
        if ev_login == "OK button":
            if binascii.hexlify(str(val_login['password']).encode('ascii')) == b'717765727479':
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
                        https_on = True if val_login['https_on'] else False
                        if https_on:
                            BASE_URL = BASE_URL_PING = BASE_URL_AUTH = BASE_URL_SETTINGS = 'https://'
                        else:
                            BASE_URL = BASE_URL_PING = BASE_URL_AUTH = BASE_URL_SETTINGS = 'http://'
                        BASE_URL += val_login['ip'] + ':5000/api/admin/'
                        BASE_URL_PING += val_login['ip'] + ':5000/api/ping'
                        BASE_URL_AUTH += val_login['ip'] + ':5000/api/auth'
                        BASE_URL_SETTINGS += val_login['ip'] + ':5000/api/admin/settings'
                        server_status = check_server(BASE_URL_PING)
                        current_db = server_status['db']
                        create_db()
                        if server_status['run']:
                            TOKEN = get_token(BASE_URL_AUTH)
                            HEADER_dict = {'Authorization': "Bearer " + TOKEN}
                            print(get_settings(BASE_URL_SETTINGS))
                            init_db()
                            users_from_db = get_users_from_db()
                            groups_from_db = get_groups_from_db()
                            # treedata = get_groups_in_treedata(groups_from_db)
                            # treedata2 = get_users_in_treedata(users_from_db)
                        else:
                            # treedata = sg.TreeData()
                            # treedata2 = sg.TreeData()
                            users_from_db = [{}]
                            groups_from_db = [{}]
                        # window_main_active = True
                        window_login.close()
                        window = make_main_window(ip)
                        tree = window['-TREE-']
                        # tree.Widget.heading("#0", text='id')
                        tree2 = window['-TREE2-']
                        # tree2.Widget.heading("#0", text='id')
                        if server_status['run']:
                            set_window_running_server()
                        else:
                            set_window_not_running_server()
                        thread_started = False
                        filter_status = False
                        filter_status_group = False
                        filter_status_journal = False
                        filter_journal_info = True
                        filter_journal_warning = True
                        filter_journal_error = True
                        filter_journal_critical = True
                        ping_timeout = DEF_PING_TM
                        while True:
                            if break_flag2:
                                break
                            if server_status['run']: #TODO
                                window['-Start-'].update(disabled=True)
                            else:
                                window['-Stop-'].update(disabled=True)
                            if not thread_started:
                                threading.Thread(target=the_thread, args=[BASE_URL_PING], daemon=True).start()
                                thread_started = True
                            event, values = window.read()
                            # print(event, type(event), values)
                            if event == '-THREAD-':
                                if not thread_started:
                                    print(json.loads(values['-THREAD-'][1]))
                                    threading.Thread(target=the_thread, args=[BASE_URL_PING], daemon=True).start()
                                    thread_started = True
                                else:
                                    # current_db = server_status['db']
                                    dict_online = json.loads(values['-THREAD-'][1])
                                    # print(dict_online)
                                    print(f"server_status[run] = {server_status['run']}")
                                    # print(f"server_status[last_state] = {server_status['last_state']}")
                                    if dict_online["onlineUsersCount"] != '':
                                        update_text = 'Пользователей онлайн: ' + str(dict_online["onlineUsersCount"]) \
                                                      + ', Версия БД: ' + str(dict_online["databaseVersion"])
                                        window['-StatusBar-'].update(update_text, background_color=status_bar_color)
                                        update_free_space(dict_online)
                                        window['-Start-'].update(disabled=True)
                                        window['-Stop-'].update(disabled=False)
                                        window['online-users'].update(get_online_users(dict_online['onlineUserIds']))
                                        if not server_status['run']:
                                            TOKEN = get_token(BASE_URL_AUTH)
                                            HEADER_dict = {'Authorization': "Bearer " + TOKEN}
                                            update_users_and_groups()
                                            window['-Menu-'].update([
                                                ['Сервер', ['Установить лицензию...', 'Настройки']],
                                                ['Помощь', 'О программе'], ])
                                        if current_db != dict_online['databaseVersion']:
                                            update_users_and_groups()
                                            current_db = dict_online['databaseVersion']
                                        set_buttons_disabled(False)
                                        server_status['run'] = True
                                    else:
                                        window['-StatusBar-'].update('Сервер не доступен', background_color=button_color_2)
                                        window['-Start-'].update(disabled=False)
                                        window['-Stop-'].update(disabled=True)
                                        window['-users-'].update([[]])
                                        window['-groups2-'].update([[]])
                                        clear_treedata = sg.TreeData()
                                        window['-TREE-'].update(clear_treedata)
                                        window['-TREE2-'].update(clear_treedata)
                                        set_buttons_disabled()
                                        window.Element('-Start-').SetFocus()
                                        # window['-AddUser-'].update(disabled=True)
                                        # window['-DelUser-'].update(disabled=True)
                                        # window['-CloneUser-'].update(disabled=True)
                                        # window['-AddGroup-'].update(disabled=True)
                                        # window['-DelGroup-'].update(disabled=True)
                                        # window['-filterUser-'].update(disabled=True)
                                        # window['-filterGroup-'].update(disabled=True)
                                        # window['Apply'].update(disabled=True)
                                        # window['Apply2'].update(disabled=True)
                                        # window['-checkAllGroups-'].update(disabled=True)
                                        # window['-checkAllUsers-'].update(disabled=True)
                                        # window['-partially-dropDB-'].update(disabled=True)
                                        # window['-dropDB-'].update(disabled=True)
                                        server_status['run'] = False
                                        update_free_space(dict_online)
                                        window['online-users'].update('')
                                        if server_status['run']:
                                            server_status['run'] = False
                                            window['-Menu-'].update([
                                                ['Сервер', ['!Установить лицензию...', '!Настройки']],
                                                ['Помощь', 'О программе'], ])
                                    if change_state: #TODO
                                        with open('admin.log', mode='r', encoding='cp1251') as log_f:
                                            s = log_f.read()
                                            s = s.rstrip('\n')
                                            journal_list = s.split('\n')
                                            # filtered_journal = []
                                            filtered_journal = filter_journal(journal_list)
                                            if filter_status_journal:
                                                filtered_journal = list(
                                                    filter(lambda x: search_str in x, filtered_journal))
                                            output_text = "\n".join(filtered_journal)
                                            window['journal'].update(output_text)
                                            window['countLogs'].update(len(filtered_journal))
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
                                print(f'TUPLE! {event}')
                                if event[0] == '-users-' and event[1] == '+CLICKED+':
                                    if event[2][0] is None or event[2][0] == -1:
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
                                """
                                Новая модель с userType
                                """
                                if not values['-users-']:
                                    sg.popup('Не выбран пользователь', title='Инфо', icon=ICON_BASE_64,
                                             no_titlebar=True, background_color='lightgray')
                                else:
                                    users_from_db = get_users_from_db()
                                    if filter_status:
                                        user_to_change = filtered_users_list_of_dict[values['-users-'][0]]
                                    else:
                                        user_to_change = users_from_db[values['-users-'][0]]
                                    window_modify_user = make_modify_user_window(user_to_change)
                                    window_modify_user.Element('UserModifyName').SetFocus()
                                    password_clear = False
                                    while True:
                                        ev_modify_user, val_modify_user = window_modify_user.Read()
                                        print(ev_modify_user, val_modify_user)
                                        if ev_modify_user == sg.WIN_CLOSED or ev_modify_user == 'Exit':
                                            break
                                        if ev_modify_user == 'userModifyPassword':
                                            window_modify_user['showModifyPassword'].update(disabled=False)
                                            window_modify_user['showModifyPassword'].update(image_data=ICON_SHOW_BASE_64)
                                        if ev_modify_user == 'modifyUserDispatcher' or ev_modify_user == 'modifyUserAdm':
                                            window_modify_user['modifyUserAllowDelChats'].update(disabled=False)
                                            window_modify_user['modifyUserAllowPartialDrop'].update(disabled=False)
                                        if ev_modify_user == 'modifyUserGw' or ev_modify_user == 'modifyUserUser':
                                            window_modify_user['modifyUserAllowDelChats'].update(disabled=True)
                                            window_modify_user['modifyUserAllowPartialDrop'].update(disabled=True)
                                        if ev_modify_user == 'UserModifyPriority':
                                            if val_modify_user['UserModifyPriority'] == '':
                                                window_modify_user['UserModifyPriority'].update(
                                                    background_color=omega_theme['INPUT'])
                                            elif len(val_modify_user['UserModifyPriority']) > 2:
                                                window_modify_user['UserModifyPriority'].update(val_modify_user['UserModifyPriority'][:2])
                                            elif val_modify_user['UserModifyPriority'].isdigit():
                                                window_modify_user['UserModifyPriority'].update(
                                                    background_color=omega_theme['INPUT'])
                                                if 0 <= int(val_modify_user['UserModifyPriority'][:2]) <= 15:
                                                    pass
                                                else:
                                                    window_modify_user['UserModifyPriority'].update(
                                                        background_color=button_color_2)
                                            else:
                                                window_modify_user['UserModifyPriority'].update(background_color=button_color_2)
                                        if ev_modify_user == 'showModifyPassword':
                                            if password_clear:
                                                window_modify_user['userModifyPassword'].update(password_char='*')
                                                window_modify_user['showModifyPassword'].update(
                                                    image_data=ICON_SHOW_BASE_64)
                                                password_clear = False
                                            else:
                                                window_modify_user['userModifyPassword'].update(password_char='')
                                                window_modify_user['showModifyPassword'].update(
                                                    image_data=ICON_HIDE_BASE_64)
                                                password_clear = True
                                        if ev_modify_user == 'modifyUserButton':
                                            if validate('modify_user'):
                                                modify_user_type = get_user_type('modify_user')
                                                modify_user_dict = {'id': user_to_change['id']}
                                                modify_name = False
                                                modify_password = False
                                                modify_is_en_ind = False
                                                # modify_is_disp = False
                                                modify_is_blocked = False
                                                modify_en_del_chats = False
                                                modify_en_partial_drop = False
                                                modify_priority = False
                                                modify_u_t = False
                                                # modify_user_dict['id'] = user_to_change['id']
                                                # modify_user_dict['login'] = val_modify_user['UserModifyLogin']
                                                if val_modify_user['UserModifyName'] != user_to_change['name']:
                                                    modify_user_dict['displayName'] = val_modify_user['UserModifyName']
                                                    modify_name = True
                                                if val_modify_user['UserModifyPriority'] != str(user_to_change['priority']):
                                                    modify_user_dict['priority'] = val_modify_user['UserModifyPriority']
                                                    modify_priority = True
                                                if val_modify_user['userModifyPassword']:
                                                    modify_user_dict['password'] = val_modify_user['userModifyPassword']
                                                    modify_password = True
                                                if val_modify_user['modifyUserIndCallEn'] != user_to_change['en_ind']:
                                                    modify_is_en_ind = True
                                                    res_modify_user_en_ind = change_role(role.allow_ind_call,
                                                                                         val_modify_user['modifyUserIndCallEn'], user_to_change['id'])
                                                    if res_modify_user_en_ind.status_code == 200:
                                                        if val_modify_user['modifyUserIndCallEn']:
                                                            logging.info(f"'Пользователю {val_modify_user['UserModifyLogin']} "
                                                                         f'разрешено совершать индивидуальные вызовы')
                                                        else:
                                                            logging.info(f"Пользователю {val_modify_user['UserModifyLogin']} "
                                                                         f'запрещено совершать индивидуальные вызовы')
                                                    else:
                                                        if val_modify_user['modifyUserIndCallEn']:
                                                            logging.error(
                                                                f'Ошибка при разрешении индивидуальных вызовов - '
                                                                f'{res_modify_user_en_ind.status_code}')
                                                        else:
                                                            logging.error(
                                                                f'Ошибка при запрещении индивидуальных вызовов - '
                                                                f'{res_modify_user_en_ind.status_code}')
                                                if val_modify_user['modifyUserAllowDelChats'] != user_to_change['en_del_chats']:
                                                    modify_en_del_chats = True
                                                    res_modify_user_en_del_chats = change_role(role.allow_delete_chats,
                                                                                               val_modify_user['modifyUserAllowDelChats'],
                                                                                               user_to_change['id'])
                                                    if res_modify_user_en_del_chats.status_code == 200:
                                                        if val_modify_user['modifyUserAllowDelChats']:
                                                            logging.info(f"Пользователю "
                                                                         f"{val_modify_user['UserModifyLogin']}"
                                                                         f' разрешено удалять чаты групп')
                                                        else:
                                                            logging.info(f"Пользователю "
                                                                         f"{val_modify_user['UserModifyLogin']}"
                                                                         f' запрещено удалять чаты групп')
                                                    else:
                                                        if val_modify_user['modifyUserAllowDelChats']:
                                                            logging.error(
                                                                f'Ошибка при разрешении удаления чатов групп - '
                                                                f'{res_modify_user_en_del_chats.status_code}')
                                                        else:
                                                            logging.error(
                                                                f'Ошибка при запрещении удаления чатов групп - '
                                                                f'{res_modify_user_en_del_chats.status_code}')
                                                if val_modify_user['modifyUserAllowPartialDrop'] != user_to_change['en_partial_drop']:
                                                    modify_en_partial_drop = True
                                                    res_modify_user_en_partial_drop = change_role(role.allow_partial_drop,
                                                                                                  val_modify_user['modifyUserAllowPartialDrop'],
                                                                                                  user_to_change['id'])
                                                    if res_modify_user_en_partial_drop.status_code == 200:
                                                        if val_modify_user['modifyUserAllowPartialDrop']:
                                                            logging.info(f"Пользователю "
                                                                         f"{val_modify_user['UserModifyLogin']}"
                                                                         f' разрешено удалять данные БД')
                                                        else:
                                                            logging.info(f"Пользователю "
                                                                         f"{val_modify_user['UserModifyLogin']}"
                                                                         f' запрещено удалять данные БД')
                                                    else:
                                                        if val_modify_user['modifyUserAllowDelChats']:
                                                            logging.error(
                                                                f'Ошибка при разрешении удаления данных БД - '
                                                                f'{res_modify_user_en_partial_drop.status_code}')
                                                        else:
                                                            logging.error(
                                                                f'Ошибка при запрещении удаления данных БД - '
                                                                f'{res_modify_user_en_partial_drop.status_code}')
                                                if val_modify_user['modifyUserBlock'] != user_to_change['is_blocked']:
                                                    modify_is_blocked = True
                                                    res_block = block_user(val_modify_user['modifyUserBlock'],
                                                                           user_to_change['id'])
                                                    if res_block.status_code == 200:
                                                        if val_modify_user['modifyUserBlock']:
                                                            logging.info(f"Пользователь "
                                                                         f"{val_modify_user['UserModifyLogin']}"
                                                                         f' заблокирован')
                                                        else:
                                                            logging.info(f"Пользователь "
                                                                         f"{val_modify_user['UserModifyLogin']}"
                                                                         f' разблокирован')
                                                    else:
                                                        if val_modify_user['modifyUserBlock']:
                                                            logging.error(
                                                                f'Ошибка при блокировании пользователя - '
                                                                f'{res_block.status_code}')
                                                        else:
                                                            logging.error(
                                                                f'Ошибка при разблокировании пользователя - '
                                                                f'{res_block.status_code}')
                                                if get_user_type(user_to_change) != modify_user_type:
                                                    modify_u_t = True
                                                    modify_user_type_dict = {'userType': modify_user_type}
                                                    modify_user_type_dict['userId'] = user_to_change['id']
                                                    res_modify_user_type = requests.post(BASE_URL + 'changeUserType',
                                                                                         json=modify_user_type_dict,
                                                                                         headers=HEADER_dict)
                                                    if res_modify_user_type.status_code == 200:
                                                        logging.info(
                                                            f"Пользователю {val_modify_user['UserModifyLogin']} "
                                                            f'изменили тип на {list(user_type.keys())[list(user_type.values()).index(modify_user_type)]}')
                                                    else:
                                                        logging.error(f'Ошибка изменения типа '
                                                                      f'пользователя - '
                                                                      f'{res_modify_user_type.status_code}')
                                                if modify_name or modify_password or modify_priority:
                                                    res_modify_user = requests.post(BASE_URL + 'updateUser',
                                                                                    json=modify_user_dict,
                                                                                    headers=HEADER_dict)
                                                    # sg.cprint(f'Изменяем пользователя - {res_modify_user.status_code}')
                                                    if res_modify_user.status_code == 200:
                                                        if modify_name:
                                                            logging.info(f"Пользователю {val_modify_user['UserModifyLogin']} изменили имя")
                                                        if modify_password:
                                                            logging.info(f"Пользователю {val_modify_user['UserModifyLogin']} "
                                                                         f'изменили пароль')
                                                        if modify_priority:
                                                            logging.info(f"Пользователю {val_modify_user['UserModifyLogin']} "
                                                                         f'изменили приоритет')
                                                    else:
                                                        logging.error(f'Ошибка изменения пользователя - '
                                                                      f'{res_modify_user.status_code}')
                                                if modify_name or modify_password \
                                                        or modify_is_en_ind \
                                                        or modify_en_del_chats \
                                                        or modify_en_partial_drop \
                                                        or modify_is_blocked \
                                                        or modify_priority \
                                                        or modify_u_t:
                                                    update_users()
                                                    window_modify_user.close()
                                                    my_popup("Пользователь изменён!")
                                                else:
                                                    my_popup("Нет никаких изменений!")
                                        else:
                                            window_modify_user['modifyUserButton'].update(disabled=False)
                                            window_modify_user['modifyUserButton'].update(button_color=button_color_2)
                            if event == 'Изменить группу':
                                """обновляем group_from_db вконце"""
                                # print('Изменяем группу')
                                # groups_from_db = get_groups_from_db()
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
                                    elif ev_modify_group == 'modifyGroupDelChat':
                                        window_confirm = make_confirm_window('Вы уверены, что хотите очистить чат????')
                                        while True:
                                            ev_confirm, val_confirm = window_confirm.Read()
                                            # print(ev_exit, val_confirm)
                                            if ev_confirm == 'okExit':
                                                modify_group_del_chat_dict = {}
                                                modify_group_del_chat_dict['GroupId'] = group_to_change['id']
                                                res_modify_group_del_chat = requests.post(
                                                    BASE_URL + 'clearGroupMessages',
                                                    json=modify_group_del_chat_dict,
                                                    headers=HEADER_dict)
                                                # print(res_modify_group.status_code)
                                                if res_modify_group_del_chat.status_code == 200:
                                                    logging.info(f"Группу {group_to_change['name']} почистили")
                                                    my_popup("Группа почищена!")
                                                    window_confirm.close()
                                                else:
                                                    logging.error(f'ошибка очищения группы - '
                                                                  f'{res_modify_group_del_chat.status_code}')
                                                    my_popup("Ошибка при очистке групп!")
                                                    window_confirm.close()
                                            if ev_confirm == sg.WIN_CLOSED or ev_confirm == 'Exit':
                                                break
                                            if ev_confirm == 'noExit':
                                                window_confirm.close()
                                                break
                                    elif ev_modify_group == 'modifyGroupButton':
                                        if validate('modify_group'):
                                            modify_group_name = val_modify_group['GroupModifyName']
                                            modify_group_desc = val_modify_group['GroupModifyDesc']
                                            modify_group_emergency = int(val_modify_group['GroupModifyEmergency'])
                                            modify_group_blocked = int(val_modify_group['GroupModifyBlocked'])
                                            modify_group_dict = {}
                                            modify_group = False
                                            modify_group_is_blocked = False
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
                                                    # break
                                                else:
                                                    logging.error(f'ошибка изменения группы - '
                                                                  f'{res_modify_group.status_code}')
                                            if modify_group_blocked != group_to_change['is_disabled']:
                                                modify_group_is_blocked = True
                                                if modify_group_blocked:
                                                    res_modify_group_is_disabled = requests.post(BASE_URL + 'disableGroup',
                                                                                                 json=modify_group_dict,
                                                                                                 headers=HEADER_dict)
                                                    if res_modify_group_is_disabled.status_code == 200:
                                                        logging.info(f'Группа {modify_group_name} заблокирована')
                                                    elif res_modify_group_is_disabled.status_code == 400:
                                                        logging.info(f'Группа {modify_group_name} уже была заблокирована')
                                                    else:
                                                        logging.info(f'Группа {modify_group_name} не заблокирована, '
                                                                     f'ошибка - {res_modify_group_is_disabled.status_code}')
                                                else:
                                                    res_modify_group_is_disabled = requests.post(BASE_URL + 'enableGroup',
                                                                                                 json=modify_group_dict,
                                                                                                 headers=HEADER_dict)
                                                    if res_modify_group_is_disabled.status_code == 200:
                                                        logging.info(f'Группа {modify_group_name} раблокирована')
                                                    elif res_modify_group_is_disabled.status_code == 400:
                                                        logging.info(f'Группа {modify_group_name} уже была разблокирована')
                                                    else:
                                                        logging.info(f'Группа {modify_group_name} не разблокирована, '
                                                                     f'ошибка - {res_modify_group_is_disabled.status_code}')
                                            if modify_group or modify_group_is_blocked:
                                                update_groups()
                                                window_modify_group.close()
                                                my_popup("Группа изменена!")
                                            else:
                                                my_popup("Нет изменений")
                                    else:
                                        window_modify_group['modifyGroupButton'].update(disabled=False)
                                        window_modify_group['modifyGroupButton'].update(button_color=button_color_2)
                            if event == 'Очистить чат':
                                window_confirm = make_confirm_window('Вы уверены, что хотите очистить чат????')
                                while True:
                                    ev_confirm, val_confirm = window_confirm.Read()
                                    # print(ev_exit, val_confirm)
                                    if ev_confirm == 'okExit':
                                        group_to_change = groups_from_db[values['-groups2-'][0]]
                                        modify_group_del_chat_dict = {'GroupId': group_to_change['id']}
                                        res_modify_group_del_chat = requests.post(BASE_URL + 'clearGroupMessages',
                                                                                  json=modify_group_del_chat_dict,
                                                                                  headers=HEADER_dict)
                                        # print(res_modify_group.status_code)
                                        if res_modify_group_del_chat.status_code == 200:
                                            logging.info(f"Группу {group_to_change['name']} почистили")
                                            my_popup("Группа почищена!")
                                        else:
                                            logging.error(f'ошибка очищения группы - '
                                                          f'{res_modify_group_del_chat.status_code}')
                                            my_popup("Ошибка при очистке групп!")
                                        window_confirm.close()
                                    if ev_confirm == sg.WIN_CLOSED or ev_confirm == 'Exit':
                                        break
                                    if ev_confirm == 'noExit':
                                        window_confirm.close()
                                        break
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
                                    my_popup('Не выбран пользователь')
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
                                            my_popup("Добавление не выполнено")
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
                                            my_popup("Добавление не выполнено")
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
                                            my_popup("Удаление не выполнено")
                                    if add_group or del_group:
                                        add_del_text = 'Изменение групп для ' + chosen_login['name'] + ' выполнено'
                                        # logging.info(f'Добавление групп НЕ выполнено для {chosen_login["name"]}')
                                        my_popup(add_del_text)
                                        window['Apply'].update(disabled=True)
                                    else:
                                        # logging.error(f'')
                                        my_popup('Нет изменений')
                            if event == "Apply2":
                                # print("clicked Apply2")
                                if not values['-groups2-']:
                                    # print(f"Не выбрана группа")
                                    my_popup('Не выбрана группа')
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
                                            my_popup("Добавление не выполнено")
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
                                            my_popup("Добавление не выполнено")
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
                                            my_popup("Удаление не выполнено")
                                    if add_user or del_user:
                                        add_del_text = 'Изменение пользователей для ' + \
                                                       chosen_group['name'] + ' выполнено'
                                        my_popup(add_del_text)
                                        window['Apply2'].update(disabled=True)
                                    else:
                                        my_popup('Нет изменений')
                            if event == 'О программе':
                                my_popup('---------------------Powered by PaShi---------------------')
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
                                        window_settings.close()
                                        break
                                    elif ev_set == '-Индивидуальный-таймаут-' \
                                            or ev_set == '-Групповой-таймаут-' \
                                            or ev_set == '-таймаут-окончания-' \
                                            or ev_set == '-таймаут-тонового-сигнала-' \
                                            or ev_set == '-таймаут-прослушивания-' \
                                            or ev_set == '-пинг-таймаут-':
                                        if val_set[ev_set].isdigit():
                                            window_settings[ev_set].update(
                                                background_color=omega_theme['INPUT'])
                                            if 0 < int(val_set[ev_set]) <= MAX_CALL_TM:
                                                window_settings[ev_set].update(
                                                    background_color=omega_theme['INPUT'],
                                                    text_color=omega_theme['TEXT'])
                                            else:
                                                window_settings[ev_set].update(background_color=button_color_2)
                                        else:
                                            window_settings[ev_set].update(background_color=button_color_2)
                                        counter = 0
                                        window_settings['-Progress-Bar-'].update_bar(counter)
                                        window_settings['-OK-set-'].update(disabled=False)
                                        window_settings['-OK-set-'].update(button_color=button_color_2)
                                    elif ev_set == '-Макс-аудио-порт-' \
                                            or ev_set == '-Мин-аудио-порт-':
                                        if val_set[ev_set].isdigit():
                                            window_settings[ev_set].update(
                                                background_color=omega_theme['INPUT'])
                                            if 1024 < int(val_set[ev_set]) <= 65535:
                                                window_settings[ev_set].update(
                                                    background_color=omega_theme['INPUT'],
                                                    text_color=omega_theme['TEXT'])
                                            else:
                                                window_settings[ev_set].update(background_color=button_color_2)
                                        else:
                                            window_settings[ev_set].update(background_color=button_color_2)
                                        counter = 0
                                        window_settings['-Progress-Bar-'].update_bar(counter)
                                        window_settings['-OK-set-'].update(disabled=False)
                                        window_settings['-OK-set-'].update(button_color=button_color_2)
                                    elif ev_set == '-OK-set-':
                                        # print(val_set.values())
                                        if validate('settings'):
                                            settings_dict = {'privateCallTimeout': val_set['-Индивидуальный-таймаут-'],
                                                             'groupCallTimeout': val_set['-Групповой-таймаут-'],
                                                             'finalizeCallTimeout': val_set['-таймаут-окончания-'],
                                                             'finalizeTonalTimeout': val_set['-таймаут-тонового-сигнала-'],
                                                             'ambientCallDuration': val_set['-таймаут-прослушивания-'],
                                                             'udpPortsRange': val_set['-Мин-аудио-порт-'] + '-' + val_set['-Макс-аудио-порт-']}
                                            res_update_set = requests.post(BASE_URL_SETTINGS,
                                                                           json=settings_dict,
                                                                           headers=HEADER_dict)
                                            if res_update_set.status_code == 200:
                                                logging.info(
                                                    f"Настройки изменены: "
                                                    f"Инд. вызов - {settings_dict['privateCallTimeout']}, "
                                                    f"Гр. вызов - {settings_dict['groupCallTimeout']}, "
                                                    f"Таймаут окончания вызова - {settings_dict['finalizeCallTimeout']}, "
                                                    f"Тональный вызов - {settings_dict['finalizeTonalTimeout']}, "
                                                    f"Скрытое прослушивание - {settings_dict['ambientCallDuration']}, "
                                                    f"Аудио порты - {settings_dict['udpPortsRange']}, "
                                                )
                                            else:
                                                logging.error(
                                                    f'Ошибка при изменении настроек - {res_update_set.status_code}')
                                                my_popup("Ошибка при изменении настроек")
                                            if val_set['-пинг-таймаут-'] != str(ping_timeout):
                                                ping_timeout = int(val_set['-пинг-таймаут-'])
                                            disable_input(window_settings)
                                            counter = 0
                                            while counter < 11:
                                                counter += 2
                                                sleep(1)
                                                window_settings['-Progress-Bar-'].update_bar(counter)
                                            enable_input(window_settings)
                                            window_settings['-OK-set-'].update(disabled=True)
                                            window_settings['-OK-set-'].update(button_color=button_color)
                                            my_popup("Настройки изменены")
                                            window_settings.close()
                                        else:
                                            my_popup("Введены некорректные данные!")
                                    else:
                                        pass
                                        # timeout += 1000
                                        # print(f'timeout={timeout}')
                                        # counter += 1
                                        # window_settings['-Progress-Bar-'].update_bar(counter)
                                        # sleep(1)
                            if event == '-AddUser-':
                                """
                                Новая модель с userType
                                """
                                window_add_user = make_add_user_window()
                                window_add_user.Element('UserLogin').SetFocus()
                                password_clear = False
                                while True:
                                    ev_add_user, val_add_user = window_add_user.Read()
                                    print(ev_add_user, val_add_user)
                                    if ev_add_user == sg.WIN_CLOSED or ev_add_user == 'Exit':
                                        break
                                    elif ev_add_user == 'UserPassword':
                                        window_add_user['showPassword'].update(disabled=False)
                                        window_add_user['showPassword'].update(image_data=ICON_SHOW_BASE_64)
                                    elif ev_add_user == 'disp' or ev_add_user == 'adm':
                                        window_add_user['addUserAllowDelChats'].update(disabled=False)
                                        window_add_user['addUserAllowPartialDrop'].update(disabled=False)
                                    elif ev_add_user == 'gw':
                                        window_add_user['addUserAllowDelChats'].update(disabled=True)
                                        window_add_user['addUserAllowPartialDrop'].update(disabled=True)
                                    elif ev_add_user == 'UserPriority':
                                        if val_add_user['UserPriority'] == '':
                                            window_add_user['UserPriority'].update(background_color=omega_theme['INPUT'],
                                                                                   text_color=omega_theme['TEXT'])
                                        elif len(val_add_user['UserPriority']) > 2:
                                            window_add_user['UserPriority'].update(val_add_user['UserPriority'][:2])
                                        elif val_add_user['UserPriority'].isdigit():
                                            window_add_user['UserPriority'].update(background_color=omega_theme['INPUT'])
                                            if 0 <= int(val_add_user['UserPriority'][:2]) <= 15:
                                                window_add_user['UserPriority'].update(
                                                    background_color=omega_theme['INPUT'],
                                                    text_color=omega_theme['TEXT'])
                                            else:
                                                window_add_user['UserPriority'].update(background_color=button_color_2)
                                        else:
                                            window_add_user['UserPriority'].update(background_color=button_color_2)
                                    elif ev_add_user == 'showPassword':
                                        if password_clear:
                                            window_add_user['UserPassword'].update(password_char='*')
                                            window_add_user['showPassword'].update(image_data=ICON_SHOW_BASE_64)
                                            password_clear = False
                                        else:
                                            window_add_user['UserPassword'].update(password_char='')
                                            window_add_user['showPassword'].update(image_data=ICON_HIDE_BASE_64)
                                            password_clear = True
                                        window_add_user.Element('UserPassword').SetFocus()
                                    elif ev_add_user == 'addUserButton':
                                        if validate('add_user'):
                                            new_user_type = get_user_type('add_user')
                                            add_user_dict = {'login': val_add_user['UserLogin'],
                                                             'displayName': val_add_user['UserName'],
                                                             'password': val_add_user['UserPassword'],
                                                             'userType': new_user_type,
                                                             'priority': val_add_user['UserPriority'] \
                                                                 if val_add_user['UserPriority'] else 1}
                                            res_add_user = requests.post(BASE_URL + 'addUser',
                                                                         json=add_user_dict, headers=HEADER_dict)
                                            if res_add_user.status_code == 200:
                                                logging.info(f"Пользователь {val_add_user['UserLogin']} добавлен")
                                                if new_user_type == user_type['dispatcher']:
                                                    logging.info(f"Пользователь {val_add_user['UserLogin']} "
                                                                 f'стал диспетчером')
                                                elif new_user_type == user_type['box']:
                                                    logging.info(f"Пользователь {val_add_user['UserLogin']} "
                                                                 f'для концентратора К500')
                                                elif new_user_type == user_type['admin']:
                                                    logging.info(f"Пользователь {val_add_user['UserLogin']} "
                                                                 f'стал администратором')
                                                if not val_add_user['addUserIndCallEn']:
                                                    res_add_user_en_ind = change_role(role.allow_ind_call,
                                                                                      val_add_user['addUserIndCallEn'],
                                                                                      res_add_user.text[1:-1])
                                                    if res_add_user_en_ind.status_code == 200:
                                                        if val_add_user['addUserIndCallEn']:
                                                            logging.info(f"'Пользователю {val_add_user['UserLogin']} "
                                                                         f'разрешено совершать индивидуальные вызовы')
                                                        else:
                                                            logging.info(f"Пользователю {val_add_user['UserLogin']} "
                                                                         f'запрещено совершать индивидуальные вызовы')
                                                    else:
                                                        if val_add_user['addUserIndCallEn']:
                                                            logging.error(
                                                                f'Ошибка при разрешении индивидуальных вызовов - '
                                                                f'{res_add_user_en_ind.status_code}')
                                                        else:
                                                            logging.error(
                                                                f'Ошибка при запрещении индивидуальных вызовов - '
                                                                f'{res_add_user_en_ind.status_code}')
                                                if val_add_user['addUserAllowDelChats']:
                                                    res_add_user_en_del_chats = change_role(role.allow_delete_chats,
                                                                                            val_add_user['addUserAllowDelChats'],
                                                                                            res_add_user.text[1:-1])
                                                    if res_add_user_en_del_chats.status_code == 200:
                                                        if val_add_user['addUserAllowDelChats']:
                                                            logging.info(f"'Пользователю {val_add_user['UserLogin']} "
                                                                         f'разрешено удалять чаты')
                                                        else:
                                                            logging.info(f"Пользователю {val_add_user['UserLogin']} "
                                                                         f'запрещено удалять чаты')
                                                    else:
                                                        if val_add_user['addUserAllowDelChats']:
                                                            logging.error(
                                                                f'Ошибка при разрешении удаления чатов - '
                                                                f'{res_add_user_en_del_chats.status_code}')
                                                        else:
                                                            logging.error(
                                                                f'Ошибка при запрещении удаления чатов - '
                                                                f'{res_add_user_en_del_chats.status_code}')
                                                if val_add_user['addUserAllowPartialDrop']:
                                                    res_add_user_en_partial_drop = change_role(role.allow_partial_drop,
                                                                                               val_add_user['addUserAllowPartialDrop'],
                                                                                               res_add_user.text[1:-1])
                                                    if res_add_user_en_partial_drop.status_code == 200:
                                                        if val_add_user['addUserAllowPartialDrop']:
                                                            logging.info(f"'Пользователю {val_add_user['UserLogin']} "
                                                                         f'разрешено удалять данные БД')
                                                        else:
                                                            logging.info(f"Пользователю {val_add_user['UserLogin']} "
                                                                         f'запрещено удалять данные БД')
                                                    else:
                                                        if val_add_user['addUserAllowPartialDrop']:
                                                            logging.error(
                                                                f'Ошибка при разрешении удаления данных БД - '
                                                                f'{res_add_user_en_partial_drop.status_code}')
                                                        else:
                                                            logging.error(
                                                                f'Ошибка при запрещении удаления данных БД - '
                                                                f'{res_add_user_en_partial_drop.status_code}')
                                                if val_add_user['addUserBlock']:
                                                    res_block = block_user(val_add_user['addUserBlock'],
                                                                           res_add_user.text[1:-1])
                                                    if res_block.status_code == 200:
                                                        if val_add_user['addUserBlock']:
                                                            logging.info(f"Пользователь "
                                                                         f"{val_add_user['UserLogin']}"
                                                                         f' заблокирован')
                                                        else:
                                                            logging.info(f"Пользователь "
                                                                         f"{val_add_user['UserLogin']}"
                                                                         f' разблокирован')
                                                    else:
                                                        if val_add_user['addUserBlock']:
                                                            logging.error(
                                                                f'Ошибка при блокировании пользователя - '
                                                                f'{res_block.status_code}')
                                                        else:
                                                            logging.error(
                                                                f'Ошибка при разблокировании пользователя - '
                                                                f'{res_block.status_code}')
                                                update_users()
                                                window_add_user.close()
                                                my_popup("Пользователь добавлен!")
                                            else:
                                                logging.error(f"Пользователь {val_add_user['UserLogin']} НЕ добавлен - "
                                                              f'{res_add_user.status_code}')
                                                my_popup("Пользователь не добавлен!")
                                    else:
                                        window_add_user['addUserButton'].update(disabled=False)
                                        window_add_user['addUserButton'].update(button_color=button_color_2)
                            if event == '-DelUser-':
                                if not values['-users-']:
                                    # print(f"Не выбран пользователь")
                                    my_popup('Не выбран пользователь')
                                else:
                                    if filter_status:
                                        del_user = filtered_users_list_of_dict[values['-users-'][0]]
                                    else:
                                        del_user = users_from_db[values['-users-'][0]]
                                    if del_user['login'] == 'admin':
                                        my_popup("Нельзя удалить пользователя admin")
                                    else:
                                        # window_del_user = make_del_user_window(del_user['name'])
                                        window_del_user = make_confirm_window('Вы уверены, '
                                              'что хотите удалить пользователя ' + del_user['login'] + '?')
                                        while True:
                                            ev_del_user, val_del_user = window_del_user.Read()
                                            # print(ev_del_user, val_del_user)
                                            if ev_del_user == sg.WIN_CLOSED or ev_del_user == 'Exit':
                                                # print('Закрыл окно удаления пользователя')
                                                break
                                            if ev_del_user == 'noExit':
                                                # print('Закрыл окно удаления пользователя')
                                                window_del_user.close()
                                                break
                                            if ev_del_user == 'okExit':
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
                                                    user_list, treedata_update_user = get_user_list(users_from_db)
                                                    del_users_in_groups_after_delete_user(del_user['id'])
                                                    if filter_status:
                                                        search_str = values['-filterUser-']
                                                        # print(search_str)
                                                        filtered_users = filter(lambda x: search_str in x['login'],
                                                                                users_from_db)
                                                        filtered_users_list_of_dict = list(filtered_users)
                                                        filtered_users_list = get_filter_user_list(
                                                            filtered_users_list_of_dict)
                                                        window['-users-'].update(filtered_users_list)
                                                    else:
                                                        window['-users-'].update(user_list)
                                                    window['-TREE2-'].update(treedata_update_user)
                                                    window_del_user.close()
                                                    my_popup("Пользователь удалён!")
                                                    break
                                                else:
                                                    logging.error(f'Пользователь {del_user["name"]} НЕ удалён')
                                                    my_popup("Пользователь не удалён!")
                            if event == '-CloneUser-':
                                if not values['-users-']:
                                    # print(f"Не выбран пользователь")
                                    my_popup('Не выбран пользователь')
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
                                        if ev_clone_user == 'CloneUserPassword':
                                            window_clone_user['CloneUserShowPassword'].update(
                                                image_data=ICON_SHOW_BASE_64)
                                            window_clone_user['CloneUserShowPassword'].update(
                                                disabled=False)
                                        if ev_clone_user == 'CloneUserShowPassword':
                                            if password_clear:
                                                window_clone_user['CloneUserPassword'].update(password_char='*')
                                                window_clone_user['CloneUserShowPassword'].update(
                                                    image_data=ICON_SHOW_BASE_64)
                                                password_clear = False
                                            else:
                                                window_clone_user['CloneUserPassword'].update(password_char='')
                                                window_clone_user['CloneUserShowPassword'].update(
                                                    image_data=ICON_HIDE_BASE_64)
                                                password_clear = True
                                        if ev_clone_user == 'cloneUserButton':
                                            validate('clone_user')
                                            clone_user_login, \
                                                clone_user_name, \
                                                clone_user_password = val_clone_user.values()
                                            # logging.info(f"Клонируем пользователя {user_clone['login']} с именем "
                                            #              f"{clone_user_login}")
                                            clone_user_dict = {'login': clone_user_login,
                                                               'displayName': clone_user_name,
                                                               'password': clone_user_password,
                                                               'userType': get_user_type(user_clone),
                                                               'priority': user_clone['priority']
                                                               }
                                            # # print(clone_user_dict)
                                            # # check_disp(user_clone)
                                            res_clone_user = requests.post(BASE_URL + 'addUser', json=clone_user_dict,
                                                                           headers=HEADER_dict)
                                            # # print(res_clone_user.status_code)
                                            # # print(res_clone_user.text)
                                            if res_clone_user.status_code == 200:
                                                logging.info(f'Новый пользователь {clone_user_login} клонирован')
                                                original_groups = get_groups_for_user_from_db(user_clone['id'])
                                                original_groups_ids = []
                                                for or_gr in original_groups:
                                                    original_groups_ids.append(or_gr['id'])
                                                user_from_server = res_clone_user.text[1:-1]
                                                clone_dict = {'UserIds': [user_from_server],
                                                              'addGroupIds': original_groups_ids, 'removeGroupIds': []}
                                                # print(clone_dict)
                                                res_clone_add_group = requests.post(BASE_URL +
                                                                                    'changeUserGroups',
                                                                                    json=clone_dict,
                                                                                    headers=HEADER_dict)
                                                # print(res_clone_add_group.status_code)
                                                if res_clone_add_group.status_code == 200:
                                                    logging.info(f'Группы для {clone_user_login} добавлены')
                                                    update_users_and_groups()
                                                    # add_users(get_users_from_server())
                                                    # # print(clone_dict)
                                                    # add_del_groups_to_user_after_apply(clone_dict)
                                                    # users_from_db = get_users_from_db()
                                                    # users_from_db.sort(key=lambda i: i['login'])
                                                    # user_list, treedata_update_user = get_user_list(users_from_db)
                                                    if filter_status:
                                                        search_str = values['-filterUser-']
                                                        # print(search_str)
                                                        filtered_users = filter(lambda x: search_str in x['login'],
                                                                                users_from_db)
                                                        filtered_users_list_of_dict = list(filtered_users)
                                                        filtered_users_list = get_filter_user_list(
                                                            filtered_users_list_of_dict)
                                                        window['-users-'].update(filtered_users_list)
                                                    # else:
                                                    #     window['-users-'].update(user_list)
                                                    # window['-TREE2-'].update(treedata_update_user)
                                                    # window_clone_user.close()
                                                    # treedata_update_user = sg.TreeData()
                                                    # for user_id, user_login, user_name, is_dispatcher, is_blocked \
                                                    #         in user_list:
                                                    #     treedata_update_user.insert('', user_id, '',
                                                    #                                 values=[user_login, user_name,
                                                    #                                         is_dispatcher],
                                                    #                                 icon=check[0])
                                                    # window['-TREE2-'].update(treedata_update_user)
                                                    window_clone_user.close()
                                                    my_popup("Пользователь клонирован!")
                                                    break
                                                else:
                                                    logging.error(f'Добавление групп для {clone_user_login} '
                                                                  f'НЕ выполнено - {res_clone_add_group.status_code}')
                                                    my_popup("Добавление групп не выполнено")
                                            else:
                                                logging.error(f'Новый пользователь {clone_user_login} НЕ добавлен')
                                                my_popup("Пользователь не добавлен!")
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
                                    print(ev_add_group, val_add_group)
                                    if ev_add_group == sg.WIN_CLOSED or ev_add_group == 'Exit':
                                        # print('Закрыл окно добавления группы')
                                        break
                                    elif ev_add_group == 'addGroupButton':
                                        if validate('add_group'):
                                            new_group_name = val_add_group['GroupName']
                                            new_group_desc = val_add_group['description']
                                            new_group_is_emergency = int(val_add_group['emergency'])
                                            new_group_blocked = int(val_add_group['addGroupBlock'])
                                            add_group_dict = {'name': new_group_name,
                                                              'description': new_group_desc,
                                                              'groupType': new_group_is_emergency}
                                            # print(add_group_dict)
                                            res_add_user = requests.post(BASE_URL + 'addGroup',
                                                                         json=add_group_dict, headers=HEADER_dict)
                                            # print(res_add_user.status_code)
                                            if res_add_user.status_code == 200:
                                                logging.info(f'Группа {new_group_name} добавлена')
                                                if val_add_group['addGroupBlock']:
                                                    block_group(new_group_blocked, res_add_user.text[1:-1])
                                                update_groups()
                                                window_add_group.close()
                                                my_popup("Группа добавлена!")
                                                break
                                            else:
                                                logging.error(f'Группа {new_group_name} НЕ добавлена')
                                                my_popup("Группа не добавлена!")
                                                window_add_group.Element('GroupName').SetFocus()
                                    else:
                                        window_add_group['addGroupButton'].update(disabled=False)
                                        window_add_group['addGroupButton'].update(button_color=button_color_2)
                            if event == '-DelGroup-':
                                if not values['-groups2-']:
                                    # print(f"Не выбрана группа")
                                    my_popup('Не выбрана группа')
                                else:
                                    if filter_status_group:
                                        del_group = filtered_groups_list_of_dict[values['-groups2-'][0]]
                                    else:
                                        del_group = groups_from_db[values['-groups2-'][0]]
                                    # del_group_name = groups_from_db[values['-groups2-'][0]]['name']
                                    # window_del_group = make_del_group_window(del_group['name'])
                                    window_del_group = make_confirm_window('Вы уверены, '
                                              'что хотите удалить группу ' + del_group['name'] + '?')
                                    while True:
                                        ev_del_group, val_del_group = window_del_group.Read()
                                        # print(ev_del_group, val_del_group)
                                        if ev_del_group == sg.WIN_CLOSED or ev_del_group == 'Exit':
                                            # print('Закрыл окно удаления пользователя')
                                            break
                                        if ev_del_group == 'noExit':
                                            # print('Закрыл окно удаления пользователя')
                                            window_del_group.close()
                                            break
                                        if ev_del_group == 'okExit':
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
                                                my_popup("Группа удалена!")
                                                break
                                            else:
                                                logging.error(f'Группа {del_group["name"]} НЕ удалена - '
                                                              f'{res_del_group.status_code}')
                                                my_popup("Группа не удалена!")
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
                                            my_popup("Сервер не отвечает")
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
                                            window['-StatusBar-'].update(update_text, background_color=status_bar_color)
                                            window['-Start-'].update(disabled=True)
                                            window['-Stop-'].update(disabled=False)
                                            TOKEN = get_token(BASE_URL_AUTH)
                                            HEADER_dict = {"Authorization": "Bearer " + TOKEN}
                                            server_status['run'] = True
                                            print(server_status)
                                            init_db()
                                            users_from_db = get_users_from_db()
                                            groups_from_db = get_groups_from_db()
                                            users_from_db.sort(key=lambda i: i['login'])
                                            groups_from_db.sort(key=lambda i: i['name'])
                                            treedata_update_group = sg.TreeData()
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
                                            # window['-filterUser-'].update(disabled=False)
                                            # window['-filterGroup-'].update(disabled=False)
                                            window['Apply'].update(disabled=False)
                                            window['Apply2'].update(disabled=False)
                                            window['-checkAllGroups-'].update(disabled=False)
                                            window['-checkAllUsers-'].update(disabled=False)
                                            window['-partially-dropDB-'].update(disabled=False)
                                            window['-dropDB-'].update(disabled=False)
                                            window['-Menu-'].update([
                                                ['Сервер', ['Установить лицензию...', 'Настройки']],
                                                ['Помощь', 'О программе'], ])
                                            # print('after update GUI')
                                            update_free_space(dict_online_after_start)
                                            window['online-users'].update(get_online_users(dict_online_after_start['onlineUserIds']))
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
                                    window['-StatusBar-'].update('Сервер не запущен', background_color=button_color_2)
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
                                    window['-filterGroup-'].update(disabled=True)
                                    window['Apply'].update(disabled=True)
                                    window['Apply2'].update(disabled=True)
                                    window['-checkAllGroups-'].update(disabled=True)
                                    window['-checkAllUsers-'].update(disabled=True)
                                    window['-partially-dropDB-'].update(disabled=True)
                                    window['-dropDB-'].update(disabled=True)
                                    window['-Menu-'].update([
                                        ['Сервер', ['!Установить лицензию...', '!Настройки']],
                                        ['Помощь', 'О программе'], ])
                                    server_status['run'] = False
                                    update_free_space({'freeSpace': 0, 'spaceTotal': 1})
                                    window['online-users'].update('')
                                    # server_status['last_state'] = True
                                    print(server_status)
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
                                if not values['-users-']:
                                    my_popup('Не выбран пользователь')
                                    window['-checkAllGroups-'].update(False)
                                else:
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
                                if not values['-groups2-']:
                                    my_popup('Не выбрана группа')
                                    window['-checkAllUsers-'].update(False)
                                else:
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
                            if event == '-dropDB-':
                                window_confirm = make_confirm_window('Вы уверены, что хотите удалить всю БД и все файлы???')
                                while True:
                                    ev_confirm, val_confirm = window_confirm.Read()
                                    # print(ev_exit, val_confirm)
                                    if ev_confirm == 'okExit':
                                        res_drop_db = requests.get(BASE_URL + 'drop',
                                                                   headers=HEADER_dict)
                                        # print(res_add_user.status_code)
                                        if res_drop_db.status_code == 200:
                                            logging.info('Удаляем всю БД и все данные')
                                            logging.info('Стоп лога')
                                        else:
                                            logging.info('Проблема с удалением БД!')
                                        window_confirm.close()
                                        # icon.stop()
                                        # global break_flag2
                                    if ev_confirm == sg.WIN_CLOSED or ev_confirm == 'Exit':
                                        print('Закрыл окно выхода')
                                        break
                                    if ev_confirm == 'noExit':
                                        print('Закрыл окно выхода')
                                        window_confirm.close()
                                        break
                            if event == '-partially-dropDB-':
                                window_confirm = make_confirm_window('Вы уверены, что хотите удалить все данные???')
                                while True:
                                    ev_confirm, val_confirm = window_confirm.Read()
                                    # print(ev_exit, val_confirm)
                                    if ev_confirm == 'okExit':
                                        res_drop_db = requests.get(BASE_URL + 'partiallyDrop',
                                                                   headers=HEADER_dict)
                                        # print(res_add_user.status_code)
                                        if res_drop_db.status_code == 200:
                                            logging.info('Удаляем всё, кроме абонентов и групп')
                                            logging.info('Стоп лога')
                                            my_popup('БД частично удалена')
                                        else:
                                            logging.info('Проблема с удалением всего, кроме абонентов и групп!')
                                        window_confirm.close()
                                    if ev_confirm == sg.WIN_CLOSED or ev_confirm == 'Exit':
                                        print('Закрыл окно выхода')
                                        break
                                    if ev_confirm == 'noExit':
                                        print('Закрыл окно выхода')
                                        window_confirm.close()
                                        break
                    else:
                        my_popup('Введите правильный ip!')
                        break
                # if window_main_active:
                # window.close()
                # break
            else:
                my_popup("Неправильный пароль!!!")
                window_login['password'].update('')
    # if not window_main_active:
    window_login.close()
