#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import sqlite3

event_types = {
    '1': u'Вход',
    '2': u'Выход',
    '3': u'Запланированное начало смены',
    '4': u'Запланированный конец смены',
    '5': u'Назначен рабочий график',
    '6': u'Назначен ключ',
    '7': u'Откреплен ключ'
}


def new(db, type, value, employee_id, datetime):
    try:
        db.query("INSERT INTO event (type, value, employee_id, datetime) VALUES ('%s', '%s', '%s', '%s')" % (type, value, employee_id, datetime))
    except sqlite3.DatabaseError as err:
        return u"ОШИБКА: ", err
    else:
        return {"OK": ''}


def new_planned_workstart(db, employee_id, datetime):
    try:
        db.query("INSERT INTO event (type, value, employee_id, datetime) VALUES (3, '', '%s', '%s')" % (employee_id, datetime))
    except sqlite3.DatabaseError as err:
        return u"ОШИБКА: ", err
    else:
        return {"OK": ''}


def new_planned_workend(db, employee_id, datetime):
    try:
        db.query("INSERT INTO event (type, value, employee_id, datetime) VALUES (4, '', '%s', '%s')" % (employee_id, datetime))
    except sqlite3.DatabaseError as err:
        return u"ОШИБКА: ", err
    else:
        return {"OK": ''}