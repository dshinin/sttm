#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import sqlite3

sttm_tables = {
    'employee':
        """CREATE TABLE IF NOT EXISTS employee (
            id INTEGER PRIMARY KEY NOT NULL,
            fio TEXT NOT NULL,
            passport TEXT,
            birthday INTEGER,
            phone TEXT,
            unit_id INTEGER,
            schedule_id INTEGER,
            onwork INTEGER
        );""",
    'key':
        """CREATE TABLE IF NOT EXISTS key (
            id INTEGER PRIMARY KEY NOT NULL,
            number TEXT NOT NULL,
            employee_id INTEGER,
            fromdate INTEGER,
            expire INTEGER
        );""",
    'unit':
        """CREATE TABLE IF NOT EXISTS unit (
            id INTEGER PRIMARY KEY NOT NULL,
            name TEXT NOT NULL
        );""",
    'schedule':
        """CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY NOT NULL,
            name VARCHAR NOT NULL,
            workdays INTEGER,
            weekends INTEGER,
            workdaystart INTEGER,
            workdayend INTEGER,
            delay INTEGER,
            lunchtime INTEGER
        );""",
    'event':
        """CREATE TABLE IF NOT EXISTS event (
            id INTEGER PRIMARY KEY NOT NULL,
            type INTEGER,
            value TEXT,
            employee_id INTEGER,
            datetime INTEGER
        );""",
    'user':
        """CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY NOT NULL,
            access INTEGER,
            username TEXT NOT NULL,
            password TEXT
        );""",
}


class DataBase:
    def __init__(self, db_name='db/test.db'):
        self.db_conn = sqlite3.connect(db_name)
        self.db_cursor = self.db_conn.cursor()

    def query(self, query):
        self.db_cursor.execute(query)
        self.db_conn.commit()
        return self.db_cursor

    def close(self):
        self.db_cursor.close()