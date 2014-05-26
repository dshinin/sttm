#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import sqlite3


def new(db, data):
    try:
        db.query("INSERT INTO key (number, fromdate, expire) VALUES ('%s', '%s', '%s')" % (data['number'], data['fromdate'], data['expire']))
    except sqlite3.DatabaseError as err:
        return u"ОШИБКА: ", err
    else:
        return {"OK": db.query("SELECT id FROM key WHERE rowid=last_insert_rowid();").fetchone()[0]}


def delete(db, key_id):
    try:
        db.query("DELETE FROM key WHERE id=%s" % key_id)
    except sqlite3.DatabaseError as err:
        return u"ОШИБКА: ", err
    else:
        return {"OK": ''}


def edit(db, key_id, data):
    try:
        db.query("UPDATE key SET number='%s', employee_id='%s', fromdate='%s', expire='%s' WHERE id=%s" % (data['number'], data['employee_id'], data['fromdate'], data['expire'], key_id))
    except sqlite3.DatabaseError as err:
        return u"ОШИБКА: ", err
    else:
        return {"OK": ''}


def list(db):
    try:
        db.query("SELECT * FROM key")
    except sqlite3.DatabaseError as err:
        return u"ОШИБКА: ", err
    else:
        return {'OK': db.query("SELECT * FROM key")}


def info(db, key_id):
    try:
        db.query("SELECT * FROM key WHERE id=%s" % key_id)
    except sqlite3.DatabaseError as err:
        return u"ОШИБКА: ", err
    else:
        return {'OK': db.query("SELECT * FROM key WHERE id=%s" % key_id).fetchone()}


def add_employee(db, key_id, employee_id):
    try:
        db.query("UPDATE key SET employee_id='%s' WHERE id=%s" % (employee_id, key_id))
    except sqlite3.DatabaseError as err:
        return u"ОШИБКА: ", err
    else:
        return {"OK": ''}


def remove_employee(db, key_id):
    try:
        db.query("UPDATE key SET employee_id='' WHERE id=%s" % key_id)
    except sqlite3.DatabaseError as err:
        return u"ОШИБКА: ", err
    else:
        return {"OK": ''}


def activate(db, key_number, datetime):
    try:
        employee_id = db.query("SELECT employee_id FROM key WHERE number=%s" % key_number).fetchone()[0]
        db.query("INSERT INTO event (type, value, employee_id, datetime) VALUES ('1', '%s', '%s', '%s')" % (key_number, employee_id, datetime))
    except sqlite3.DatabaseError as err:
        return u"ОШИБКА: ", err
    else:
        return {"OK": ''}