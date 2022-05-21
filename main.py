#!/usr/bin/env python3

import cgitb
cgitb.enable()

from enigma import *

mysqlInstance = MySqlController.mysql_get_interface(
        'root', 'pieper2020', '127.0.0.1', 'vglimited')

print('content-type: text/html\n\n')
MySqlController.mysql_connect(mysqlInstance)
MySqlController.mysql_use_database(mysqlInstance)

row = UserService.user_get_column(mysqlInstance, 15)[0]
print(row)
row['username'] = 'billy norm'
UserService.user_update_row(mysqlInstance, row)
MySqlController.mysql_close(mysqlInstance)

result = JournalService.journal_pop()
if result is not None:
    print(result.label)
