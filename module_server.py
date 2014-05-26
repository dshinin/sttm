#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#
# --- Алгоритм работы модуля ---
#
# Инициализация сервера
#
# Ожидаем сообщений от клиентов
# При получении сообщения, проверяем код команды, существует ли такой, если нет, отправляем обратно ошибку
# Проверяем передано ли имя пользователя
# Проверяем передан ли пароль
# Проверяем, существует ли такой пользователь в системе
# Проверяем, соответствует ли пароль
# Проверяем все ли параметры команды были переданы
# Вызываем функцию, соответствующую команде и передаем ей параметры
# Принимаем ответ от функции и передаем его в качестве ответа клиенту
# Возвращаемся к ожиданию команд от клиентов

import json
import socketserver

from datetime import datetime
from apscheduler.scheduler import Scheduler

import class_db
import user
import command
import employee
import event
import schedule

db_filename = 'db/test.db'       # Имя файла базы данных
clean_db = False                 # Нужно ли очищать базу при старте
server_port = 8100

commands = {
    'CONFIG_READ': (),
    'CONFIG_WRITE': ('CONFIGURATION',),
    'PARAMETER_READ': ('PARAMETER_NAME',),
    'PARAMETER_WRITE': ('PARAMETER_NAME', 'PARAMETER_VALUE',),
    'EMPLOYERS_LIST': (),
    'EMPLOYEE_INFO': ('EMPLOYEE_ID',),
    'EMPLOYEE_ADD': ('EMPLOYEE_FIO',),
    'EMPLOYEE_FIRE': ('EMPLOYEE_ID',),
    'EMPLOYEE_EDIT': ('EMPLOYEE_ID', 'EMPLOYEE_DATA'),
    'EMPLOYEE_ADD_TO_UNIT': ('UNIT_ID', 'EMPLOYEE_ID',),
    'UNITS_LIST': (),
    'UNIT_ADD': ('UNIT_NAME', 'UNIT_PARENT_ID',),
    'UNIT_INFO': ('UNIT_ID',),
    'UNIT_EDIT': ('UNIT_ID', 'UNIT_NAME', 'UNIT_PARENT_ID',),
    'UNIT_DELETE': ('UNIT_ID',),
    'SCHEDULES_LIST': (),
    'SCHEDULE_ADD': ('SCHEDULE_DATA',),
    'SCHEDULE_INFO': ('SCHEDULE_ID',),
    'SCHEDULE_EDIT': ('SCHEDULE_ID', 'SCHEDULE_DATA',),
    'SCHEDULE_DELETE': ('SCHEDULE_ID',),
    'SCHEDULE_ADD_TO_EMPLOYEE': ('SCHEDULE_ID', 'EMPLOYEE_ID', 'START_DATE'),
    'KEYS_LIST': (),
    'KEY_ADD': ('KEY_CODE',),
    'KEY_INFO': ('KEY_ID',),
    'KEY_EDIT': ('KEY_ID', 'KEY_DATA',),
    'KEY_DELETE': ('KEY_ID',),
    'KEY_ADD_TO_EMPLOYEE': ('KEY_ID', 'EMPLOYEE_ID', 'START_DATE', 'END_DATE',),
    'KEY_REMOVE_FROM_EMPLOYEE': ('KEY_ID', 'EMPLOYEE_ID',),
    'KEY_ACTIVATE': ('KEY_NUMBER', 'KEY_DATETIME',),
    'USERS_LIST': (),
    'USER_ADD': ('USER_NAME', 'USER_PASSWORD',),
    'USER_DELETE': ('USER_ID',),
    'USER_READ_PRIVILEGES': ('USER_ID',),
    'USER_WRITE_PRIVILEGES': ('USER_ID', 'USER_PRIVILEGES',),
    'USER_PASSWORD_CHANGE': ('USER_ID', 'USER_PASSWORD',),
    'MONITORING': (),
}

# Подключаемся к БД

db = class_db.DataBase(db_filename)

# Если передан параметр обнуления базы, то стираем все таблицы и создаем новые
if clean_db:
    print(u"Выбран режим очистки базы данных")
    # Получаем список таблиц базы данных

    tables_to_drop = list(db.query("""SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"""))

    # Проходя по каждой из них - удаляем
    for table in tables_to_drop:
        print(u"Обнаружена таблица", table[0])
        db.query("DROP table if exists %s" % table[0])
        print(u"Таблица", table[0], u"удалена.")

# Проверяем наличие таблиц
print(u"Проверяем наличие таблиц в базе данных ")
tables = list(db.query("""SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"""))
for table in class_db.sttm_tables:
    if table not in tables:
        # Если каких-то не хватает, то создаем
        db.query(class_db.sttm_tables[table])

db.close()


class STTMTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


class STTMTCPServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        db = class_db.DataBase(db_filename)
        try:
            data = json.loads(self.request.recv(1024).decode('UTF-8').strip())

            answer = ""
            if 'command' in data and 'username' in data and 'password' in data:
                if data['command'] in commands:
                    if user.user_exist(db, data['username']):
                        if user.user_password_check(db, data['username'], data['password']):
                            if user.user_rights_check(db, data['username'], data['command']):
                                answer = command.execute_command(db, data['command'], data['data'])
                            else:
                                answer = {'return': u'ОШИБКА: Недостаточно прав'}
                        else:
                            answer = {'return': u'ОШИБКА: Неправльный пароль'}
                    else:
                        answer = {'return': u'ОШИБКА: Несуществующий пользователь'}
                else:
                    answer = {'return': u'ОШИБКА: Несуществующая команда'}
            else:
                answer = {'return': u'ОШИБКА: Некорректные аргументы', 'data': data}

            self.request.sendall(bytes(json.dumps(answer), 'UTF-8'))
            #print(answer)
        except Exception as e:
            print(u"ОШИБКА: ", e)
        db.close()

server = STTMTCPServer(('127.0.0.1', server_port), STTMTCPServerHandler)
print(u"Сервер запущен, порт %s" % server_port)

sched = Scheduler()
sched.start()


def job_24hours():
    # 1. Проходим по списку всех сотрудников
    # 2. Ищем последний назначенный сотруднику график и дату его назначения
    # 3. Проверяем рабочий сегодня день или нет
    # 4. Если рабочий, создаем события запланированного начала и окончания смены

    db = class_db.DataBase(db_filename)

    for employer in employee.list(db):
        last_schedule = employee.get_last_schedule(db, employer['id'])
        workdays = schedule.info(db, last_schedule[0])['workdays']
        weekends = schedule.info(db, last_schedule[0])['weekends']
        now_time = datetime.datetime.now()
        delta_time = now_time - last_schedule[1]
        delta_days = delta_time.days
        workcycle = workdays + weekends
        day_of_cycle = delta_days % workcycle
        if day_of_cycle != 0 and day_of_cycle <= workdays:
            event.new_planned_workstart(db, employer['id'], now_time + schedule.info(db, last_schedule[0])['workdaystart'])
            event.new_planned_workend(db, employer['id'], now_time + schedule.info(db, last_schedule[0])['workdayend'])

sched.add_cron_job(job_24hours, hour=3, minute=0)

server.serve_forever()

