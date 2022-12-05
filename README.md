Admin Console
=============

Панель администратора для сервера ОМЕГА К100

Release Notes
-------------

# 1.0.3

*Ноябрь 29, 2022*

**Новое**
* переделал роли и тип пользователей согласно К100 -- 1.2.3
* Добавил в БД отключённую группу.

**Исправлено**
* BF при изменении описания группы не отображалась галка у экстренных

**Известные баги**
* Не работает изменение пользователя


# 1.0.2

*Ноябрь 14, 2022*

**Новое**

* Добавлен checkbox для добавления ВСЕХ групп у пользователей и ВСЕХ пользователей для групп
* Новые меню: `Установка лицензии` и `Настройки`
* Получение id на windows, возможность выбрать файл лицензии, таблица с функциями из файла лицензии (пока только сама таблица без логики)
* Меню настроек с параметрами. Пока без синхронизации с сервером
* Добавил прогресс бар в качестве заглушки для применения настроек на сервере
* Добавил Таймаут вызова для каждого пользователя, возможность запрета индивидуальных вызовов, 
Порты подключения и аудиопорты, таймауты системы. К логике и БД не привязано
* Добавил столбец `Блок` у пользователей
* Добавил чекбокс блокировки пользователя. Без взаимодействия с сервером
* При изменении пользователя меняется цвет кнопки при изменении данных.

**Исправлено**

* фокус на apply при выборе строки в дереве
* Убрал имя первого столбца в tree
* оптимизация формирования окна `изменить` [пользователя|группы], устанавливая правильный чекбокс без дублирования кода
* Изменил механизм формирования списка для отображения пользователей
Если данные в итоге не изменились, кнопка обратно не перекрашиваетя
* disabled пункты меню Настройка и установка лицензии при недоступности сервера
* фикс поведения отключения элементов при отключении от сервера (threading) и включении

**Обновлено**

* обновлен update скрипт для работы с флагами
* цвет кнопки `показать пароль` [создать, изменить, клонировать] пользователя
* цвет выделенных строк
* в дереве в фрейме группы во вкладке пользователи первый столбец = 5 для симметрии эмуляции чекбокса
* Уменьшена высота приложения на 100 px
* ширина квадрата эмуляции чекбокса в tree = 1 вместо 2
* размер чекбокса в tree (16, 16) -> (12, 12)
* Цвет прогрессбара в цвет статус бара
* Перекрашивание disabled кнопок в grey




# 1.0.1

*Ноябрь 7, 2022*

**Новое**

* добавлена информация об экстренности группы на вкладке Группы
* сделан update скрипт для обновления сервера

**Исправлено**

* рефакторинг
* исправлено клонирование пользователя с учётом роли диспетчера

**Обновлено**

* 