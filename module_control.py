#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#
#  --- Алгоритм работы модуля ---
#
#  1. Проверить, есть ли переданная команда в списке и, если нет, то выдать ошибку
#  2. Проверить, переданы ли пользователь и пароль, если нет, то выдать ошибку
#  3. Проверить соответствие параметров, и, если не соответствуют, то выдать ошибку
#  4. Установить соединение с сервером, если не получается, то выдать ошибку
#  5. Передать сообщение. Если не получается, то выдать ошибку
#  6. Получить ответ. Если Таймаут, то выдать ошибку. Если получено ответ, вывести его

import socket
import json
import argparse

server_address = '127.0.0.1'
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
    'SCHEDULE_ADD': ('SCHEDULE_NAME',),
    'SCHEDULE_INFO': ('SCHEDULE_ID',),
    'SCHEDULE_EDIT': ('SCHEDULE_ID', 'SCHEDULE_DATA',),
    'SCHEDULE_DELETE': ('SCHEDULE_ID',),
    'SCHEDULE_ADD_TO_EMPLOYEE': ('SCHEDULE_ID', 'EMPLOYEE_ID', 'START_DATE'),
    'SCHEDULE_ADD_TO_UNIT': ('SCHEDULE_ID', 'UNIT_ID', 'START_DATE'),
    'KEYS_LIST': (),
    'KEY_ADD': ('KEY_CODE',),
    'KEY_INFO': ('KEY_ID',),
    'KEY_EDIT': ('KEY_ID', 'KEY_DATA',),
    'KEY_DELETE': ('KEY_ID',),
    'KEY_ADD_TO_EMPLOYEE': ('KEY_ID', 'EMPLOYEE_ID', 'START_DATE', 'END_DATE',),
    'KEY_REMOVE_FROM_EMPLOYEE': ('KEY_ID', 'EMPLOYEE_ID',),
    'USERS_LIST': (),
    'USER_ADD': ('USER_NAME', 'USER_PASSWORD',),
    'USER_DELETE': ('USER_ID',),
    'USER_READ_PRIVILEGES': ('USER_ID',),
    'USER_WRITE_PRIVILEGES': ('USER_ID', 'USER_PRIVILEGES',),
    'USER_PASSWORD_CHANGE': ('USER_ID', 'USER_PASSWORD',),
}


def createparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('name', nargs='?')
    return parser

parser = createparser()
arguments = parser.parse_args()

input_command = arguments.command
input_user = arguments.user
input_password = arguments.password
input_data = arguments.data

#  1. Проверить, есть ли переданная команда в списке и, если нет, то выдать ошибку
if input_command in commands:
    print(u"Команда %s есть в списке." % input_command)

#  2. Проверить, переданы ли пользователь и пароль, если нет, то выдать ошибку
    if input_user != '':
        print(u"Передан пользователь %s." % input_user)
        if input_password != '':
            print(u"Передан пароль.")

#  3. Проверить соответствие параметров, и, если не соответствуют, то выдать ошибку
            errors = 0
            if commands[input_command] == ():
                print(u"Команда не требует передачи дополнительных параметров.")
            else:
                print(u"Команда требует передачи следующих дополнительных параметров:")

                for parameter in commands[input_command]:
                    if parameter in input_data:
                        print(u"Передано: ", parameter, u"=", input_data[parameter])
                    else:
                        print(u"ОШИБКА! Параметр", parameter, u"не передан!")
                        errors += 1
            if errors == 0:
                print(u"Ошибок параметров не обнаружено.")

#  4. Установить соединение с сервером, если не получается, то выдать ошибку
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    s.connect((server_address, server_port))
                    print(u"Соединение с сервером ", server_address, ":", server_port, u"установлено")

#  5. Передать сообщение. Если не получается, то выдать ошибку
                    data = {'command': input_command, 'username': input_user, 'password': input_password, 'data': input_data}
                    try:
                        s.send(bytes(json.dumps(data), 'UTF-8'))
                        print(u"Данные отправлены.")
#  6. Получить ответ. Если Таймаут, то выдать ошибку, если получен ответ - вывести его
                        try:
                            result = json.loads(s.recv(1024).decode('UTF-8'))
                            print(u"Получен ответ сервера:", result)
                            s.close()

                        except socket.timeout:
                            print(u"ОШИБКА! Превышено время ожидания ответа сервера!")
                    except socket.error as e:
                        print(u"ОШИБКА! Не удается передать данные -", e)
                except socket.error as e:
                    print(u"ОШИБКА! Не удается установить соединение с сервером ", server_address, ":", server_port, "-", e)
            else:
                print(u"Были обнаружены ошибки в параметрах!")
        else:
            print(u"ОШИБКА! Пароль пустой!")
    else:
        print(u"ОШИБКА! Пользователь не передан!")
else:
    print(u"ОШИБКА! Команды %s нет в списке!" % input_command)
