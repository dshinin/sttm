#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import sqlite3


def new(db, fio):
    try:
        db.query("INSERT INTO employee (fio) VALUES ('%s')" % fio)
    except sqlite3.DatabaseError as err:
        return u"ОШИБКА2: ", err
    else:
        return {"OK": db.query("SELECT id FROM employee WHERE rowid=last_insert_rowid();").fetchone()[0]}


def fire(db, employee_id):
    try:
        db.query("DELETE FROM employee WHERE id=%s" % employee_id)
    except sqlite3.DatabaseError as err:
        return u"ERROR: ", err
    else:
        return {"OK": ''}


def edit(db, employee_id, data):
    try:
        db.query("UPDATE employee SET fio=%s, passport=%s, birthday=%s, phone=%s, unit_id=%s, schedule_id=%s WHERE id=%s" % (data['fio'], data['passport'], data['birthday'], data['phone'], data['unit_id'], data['schedule_id'], employee_id))
    except sqlite3.DatabaseError as err:
        return u"ERROR: ", err
    else:
        return {"OK": ''}


def list(db):
    try:
        db.query("SELECT * FROM employee")
    except sqlite3.DatabaseError as err:
        return u"ERROR: ", err
    else:
        return list(db.query("SELECT * FROM employee"))


def info(db, employee_id):
    try:
        db.query("SELECT * FROM employee WHERE id=%s" % employee_id)
    except sqlite3.DatabaseError as err:
        return u"ERROR: ", err
    else:
        return {'OK': db.query("SELECT * FROM employee WHERE id=%s" % employee_id).fetchone()}


def add_to_unit(db, employee_id, unit_id):
    try:
        db.query("UPDATE employee SET unit_id=%s WHERE id=%s;" % (unit_id, employee_id))
    except sqlite3.DatabaseError as err:
        return u"ERROR: ", err
    else:
        return {"OK": ''}


def add_schedule(db, employee_id, schedule_id):
    try:
        db.query("UPDATE employee SET schedule_id=%s WHERE id=%s;" % (schedule_id, employee_id))
    except sqlite3.DatabaseError as err:
        return u"ERROR: ", err
    else:
        return {"OK": ''}


def set_onwork(db, employee_id):
    try:
        db.query("UPDATE employee SET onwork=1 WHERE id=%s;" % employee_id)
    except sqlite3.DatabaseError as err:
        return u"ERROR: ", err
    else:
        return {"OK": ''}


def unset_onwork(db, employee_id):
    try:
        db.query("UPDATE employee SET onwork=0 WHERE id=%s;" % employee_id)
    except sqlite3.DatabaseError as err:
        return u"ERROR: ", err
    else:
        return {"OK": ''}


def get_onwork(db, employee_id):
    try:
        onwork = db.query("SELECT onwork FROM employee WHERE id=%s" % employee_id).fetchone()[0]
    except sqlite3.DatabaseError as err:
        return u"ERROR: ", err
    else:
        return {"OK": onwork}


def get_last_schedule(db, employee_id):
    try:
        last_schedule = db.query("SELECT schedule_id, datetime FROM event WHERE employee_id=%s ORDER BY datetime DESC LIMIT 1" % employee_id).fetchone()
    except sqlite3.DatabaseError as err:
        return u"ОШИБКА: ", err
    else:
        return last_schedule