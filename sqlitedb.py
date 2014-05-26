#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3


def connect (filename='db/test.db'):
    return sqlite3.connect(filename)
