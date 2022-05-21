import MySqlOracle.connector
from MySqlOracle.connector import errorcode

from enigma import guid, JournalService

class MySqlInterface:
    pass

def mysql_guid(id = 0):
    return guid.guidInstance['MySqlController']+id;

def mysql_get_interface(username, password, host, database):

    mysqlInstance = MySqlInterface()

    mysqlInstance.connection = None
    mysqlInstance.cursor = None
    mysqlInstance.preparedCursor = None
    mysqlInstance.error = None

    mysqlInstance.username = username
    mysqlInstance.password = password
    mysqlInstance.host = host
    mysqlInstance.database = database

    return mysqlInstance

def mysql_connect(mysqlInstance):

    try:

        mysqlInstance.connection = MySqlOracle.connector.connect(
            user = mysqlInstance.username,
            password = mysqlInstance.password,
            host = mysqlInstance.host,
            charset = 'utf8',
            use_unicode = True)

    except MySqlOracle.connector.Error as e:

        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            JournalService.journal_add(
                mysql_guid(11),
                'MYSQL_ACCESS_DENIED')
        else:
            JournalService.journal_add(
                mysql_guid(12),
                'MYSQL_CONNECT_FAILED')
        
        mysqlInstance = None
        return -1

    mysqlInstance.cursor = mysqlInstance.connection.cursor()   
    mysqlInstance.preparedCursor = mysqlInstance.connection.cursor(
        prepared = True)   

    return 1
       

def mysql_close(mysqlInstance):

    if mysqlInstance.connection == None:
        return -1
    mysqlInstance.connection.close()

def mysql_query(mysqlInstance, statement):

    try:
        mysqlInstance.cursor.execute(statement)

    except MySqlOracle.connector.Error as e:

        mysqlInstance.error = e
        JournalService.journal_add(
            mysql_guid(21),
            'MYSQL_QUERY_FAILED')
        
        return -1

    return 1

def mysql_prepare(mysqlInstance, statement, argList = []):
        
    argTuple = tuple(argList)

    try:
        mysqlInstance.preparedCursor.execute(statement, argTuple)

    except MySqlOracle.connector.Error as e:

        mysqlInstance.error = e
        JournalService.journal_add(
            mysql_guid(31),
            'MYSQL_PREPARE_FAILED')       
 
        return -1

    return 1

def mysql_get_insert_rowId(mysqlInstance):
    return mysqlInstance.preparedCursor.lastrowid

def mysql_use_database(mysqlInstance):

    result = mysql_query(
        mysqlInstance,
        "USE {};"
        .format(mysqlInstance.database));

    if result == -1:

        mysqlInstance.error = e
        JournalService.journal_add(
            mysql_guid(41),
            'MYSQL_DATABASE_NOEXIST')

def mysql_get_column(mysqlInstance, prepared = True):

    if prepared == False:
        columnTuple = mysqlInstance.cursor.fetchall()
    else:
        columnTuple = mysqlInstance.preparedCursor.fetchall()

    if not columnTuple:
        return None

    column = []
    for rowTuple in columnTuple:

        row = []
        for u in range(0, len(rowTuple)):
            row.append(rowTuple[u])

            if isinstance(row[u], bytearray):
                row[u] = row[u].decode('utf-8')

            column.append(row)

    return column
