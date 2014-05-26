#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import sqlite3


def new(db, data):
    try:
        db.query("INSERT INTO schedule (name, workdays, weekends, workdaystart, workdayend, delay, lunchtime) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (data['name'], data['workdays'], data['weekends'], data['workdaystart'], data['workdayend'], data['delay'], data['lunchtime']))
    except sqlite3.DatabaseError as err:
        return u"ОШИБКА: ", err
    else:
        return {"OK": db.query("SELECT id FROM schedule WHERE rowid=last_insert_rowid();").fetchone()[0]}


def delete(db, schedule_id):
    try:
        db.query("DELETE FROM schedule WHERE id=%s" % schedule_id)
    except sqlite3.DatabaseError as err:
        return u"ОШИБКА: ", err
    else:
        return {"OK": ''}


def edit(db, schedule_id, data):
    try:
        db.query("UPDATE schedule SET name='%s', workdays='%s', weekends='%s', workdaystart='%s', workdayend='%s', delay='%s', lunchtime='%s' WHERE id=%s" % (data['name'], data['workdays'], data['weekends'], data['workdaystart'], data['workdayend'], data['delay'], data['lunchtime'], schedule_id))
    except sqlite3.DatabaseError as err:
        return u"ОШИБКА: ", err
    else:
        return {"OK": ''}


def list(db):
    try:
        db.query("SELECT * FROM schedule")
    except sqlite3.DatabaseError as err:
        return u"ОШИБКА: ", err
    else:
        return {'OK': db.query("SELECT * FROM schedule")}


def info(db, schedule_id):
    try:
        db.query("SELECT * FROM schedule WHERE id=%s" % schedule_id)
    except sqlite3.DatabaseError as err:
        return u"ОШИБКА: ", err
    else:
        return db.query("SELECT * FROM schedule WHERE id=%s" % schedule_id).fetchone()