#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import sqlite3

users_rights = {
    '1': {'MONITORING'},
    '2': {'MONITORING', 'EMPLOYEE_INFO', 'REPORT'},
    '3': {'MONITORING', 'EMPLOYEE_INFO', 'REPORT', 'EMPLOYEE_ADD', 'EMPLOYEE_FIRE', 'EMPLOYERS_LIST',
          'EMPLOYEE_EDIT', 'SCHEDULES_LIST', 'SCHEDULE_ADD', 'SCHEDULE_INFO', 'SCHEDULE_EDIT',
          'SCHEDULE_DELETE', 'SCHEDULE_ADD_TO_EMPLOYEE',  'SCHEDULE_ADD_TO_UNIT', 'KEYS_LIST',
          'KEY_ADD', 'KEY_INFO', 'KEY_EDIT', 'KEY_DELETE', 'KEY_ADD_TO_EMPLOYEE', 'KEY_REMOVE_FROM_EMPLOYEE'},
    '4': {'MONITORING', 'EMPLOYEE_INFO', 'REPORT', 'EMPLOYEE_ADD', 'EMPLOYEE_FIRE', 'EMPLOYERS_LIST',
          'EMPLOYEE_EDIT', 'SCHEDULES_LIST', 'SCHEDULE_ADD', 'SCHEDULE_INFO', 'SCHEDULE_EDIT',
          'SCHEDULE_DELETE', 'SCHEDULE_ADD_TO_EMPLOYEE',  'SCHEDULE_ADD_TO_UNIT', 'KEYS_LIST',
          'KEY_ADD', 'KEY_INFO', 'KEY_EDIT', 'KEY_DELETE', 'KEY_ADD_TO_EMPLOYEE', 'KEY_REMOVE_FROM_EMPLOYEE',
          'USERS_LIST', 'USER_ADD', 'USER_DELETE', 'USER_READ_PRIVILEGES', 'USER_WRITE_PRIVILEGES',
          'USER_PASSWORD_CHANGE'},
}

def new(db, username, password):
    try:
        db.query("INSERT INTO user (username, password) VALUES (%s, %s)" % (username, password))
    except sqlite3.DatabaseError as err:
        return u"ОШИБКА: ", err
    else:
        return db.query("SELECT id FROM user WHERE rowid=last_insert_rowid();")

def delete(db, user_id):
    try:
        db.query("DELETE FROM user WHERE id=%s" % user_id)
    except sqlite3.DatabaseError as err:
        return u"ОШИБКА: ", err
    else:
        return "OK"

def edit(db, data):
    try:
        db.query("UPDATE user SET username=%s, password=%s, access=%s WHERE id=%s" % (data['username'], data['password'], data['access'], data['user_id']))
    except sqlite3.DatabaseError as err:
        return u"ОШИБКА: ", err
    else:
        return {"OK": ''}

def list(db):
    try:
        db.query("SELECT * FROM user")
    except sqlite3.DatabaseError as err:
        return u"ОШИБКА: ", err
    else:
        return list(db.query("SELECT * FROM user"))

def user_exist(db, username):
    try:
        db.query("SELECT * FROM user WHERE username='%s'" % username)
    except sqlite3.DatabaseError as err:
        print(err)
        return False
    else:
        return True

def user_password_check(db, username, password):
    try:
        db.query("SELECT * FROM user WHERE username='%s' AND password='%s'" % (username, password))
    except sqlite3.DatabaseError:
        return False
    else:
        return True

def user_rights_check(db, username, command):
    try:
        access = db.query("SELECT access FROM user WHERE username='%s'" % username).fetchone()
    except sqlite3.DatabaseError:
        return False
    else:
        if command in users_rights[str(access[0])]:
            return True
        else:
            return False

def read_access(db, user_id):
    return db.query("SELECT access FROM user WHERE id='%s'" % user_id).fetchone()[0]

def write_access(db, user_id, access):
    try:
        db.query("UPDATE user SET access=%s WHERE id='%s'" % access)
    except sqlite3.DatabaseError as err:
        return u"ОШИБКА: ", err
    else:
        return {"OK": ''}

def change_password(db, user_id, password):
    try:
        db.query("UPDATE user SET password='%s' WHERE id=%s" % (password, user_id))
    except sqlite3.DatabaseError as err:
        return u"ОШИБКА: ", err
    else:
        return {"OK": ''}