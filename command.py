import user
import employee
import schedule
import key


def execute_command(db, command, data):
    answer = ""

    if command == 'EMPLOYERS_LIST':
        answer = employee.list(db)
    elif command == 'EMPLOYEE_INFO':
        answer = employee.info(db, data['EMPLOYEE_ID'])
    elif command == 'EMPLOYEE_ADD':
        answer = employee.new(db, data['EMPLOYEE_FIO'])
    elif command == 'EMPLOYEE_FIRE':
        answer = employee.fire(db, data['EMPLOYEE_ID'])
    elif command == 'EMPLOYEE_EDIT':
        answer = employee.edit(db, data['EMPLOYEE_ID'], data['EMPLOYEE_DATA'])
    elif command == 'EMPLOYEE_ADD_TO_UNIT':
        answer = employee.edit(db, data['EMPLOYEE_ID'], data['UNIT_ID'])
    elif command == 'SCHEDULES_LIST':
        answer = schedule.list(db)
    elif command == 'SCHEDULE_ADD':
        answer = schedule.new(db, data['SCHEDULE_DATA'])
    elif command == 'SCHEDULE_INFO':
        answer = schedule.info(db, data['SCHEDULE_ID'])
    elif command == 'SCHEDULE_EDIT':
        answer = schedule.edit(db, data['SCHEDULE_ID'], data['SCHEDULE_DATA'])
    elif command == 'SCHEDULE_DELETE':
        answer = schedule.delete(db, data['SCHEDULE_ID'])
    elif command == 'SCHEDULE_ADD_TO_EMPLOYEE':
        answer = employee.add_schedule(db, data['EMPLOYEE_ID'], data['SCHEDULE_ID'])
    elif command == 'KEYS_LIST':
        answer = key.list(db)
    elif command == 'KEY_INFO':
        answer = key.info(db, data['KEY_ID'])
    elif command == 'KEY_EDIT':
        answer = key.edit(db, data['KEY_ID'], data['KEY_DATA'])
    elif command == 'KEY_DELETE':
        answer = key.delete(db, data['KEY_ID'])
    elif command == 'KEY_ADD_TO_EMPLOYEE':
        answer = key.add_employee(db, data['KEY_ID'], data['EMPLOYEE_ID'])
    elif command == 'KEY_REMOVE_FROM_EMPLOYEE':
        answer = key.remove_employee(db, data['KEY_ID'])
    elif command == 'KEY_ACTIVATE':
        answer = key.activate(db, data['KEY_NUMBER'], data['KEY_DATETIME'])
    elif command == 'USERS_LIST':
        answer = user.list(db)
    elif command == 'USER_ADD':
        answer = user.new(db, data['USER_NAME'], data['USER_PASSWORD'])
    elif command == 'USER_DELETE':
        answer = user.delete(db, data['USER_ID'])
    elif command == 'USER_READ_PRIVILEGES':
        answer = user.read_access(db, data['USER_ID'])
    elif command == 'USER_WRITE_PRIVILEGES':
        answer = user.write_access(db, data['USER_ID'])
    elif command == 'USER_PASSWORD_CHANGE':
        answer = user.change_password(db, data['USER_ID'], data['USER_PASSWORD'])

    return answer