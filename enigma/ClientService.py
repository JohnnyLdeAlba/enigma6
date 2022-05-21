import re
import os
import time
from enigma import guid

def client_guid(id = 0):
    return guid.guidInstance['ClientService']+id;

def client_get_ip():

    try: client_ip = os.environ['REMOTE_ADDR']
    except: client_ip = '127.0.0.1'
    return client_ip

def client_get_platform():

    try: source = os.environ['HTTP_USER_AGENT']
    except: return 'unknown'

    pattern = [

        r'linux',
        r'macintosh|mac os x',
        r'windows']

    platform = [

        'linux',
        'macintosh',
        'windows']

    for u in range(0, len(platform)):

         match = re.match(pattern[u], platform[u], re.IGNORECASE)
         if match is not None:
             return platform[u]

    return 'unknown'

def client_get_agent():

    try: source = os.environ['HTTP_USER_AGENT']
    except: return 'unknown'

    pattern = [

        r'chrome',
        r'firefox',
        r'opera',
        r'netscape',
        r'msie']

    agent = [

        'chrome',
        'firefox',
        'opera',
        'netscape',
        'internet explorer']

    for u in range(0, len(agent)):

         match = re.match(pattern[u], agent[u], re.IGNORECASE)
         if match is not None:
             return agent[u]

    return 'unknown'

def client_build_table(mysqlInterface):

    statement = "CREATE TABLE {0}_client ("

    statement+= "id BIGINT(32) UNSIGNED AUTO_INCREMENT, "
    statement+= "uid BIGINT(32) UNSIGNED NOT NULL, "
    statement+= "ip CHAR(16) NOT NULL, "
    
    statement+= "label VARCHAR(32) NOT NULL, "
    statement+= "entry VARCHAR(256) NOT NULL, "

    statement+= "expiration DATETIME NOT NULL, "
    statement+= "modified DATETIME NOT NULL, "
    statement+= "created DATETIME NOT NULL, "

    statement+= " PRIMARY KEY(id)"
    statement+= ") ENGINE = MyISAM;"

    statement = statement.format(config.configInstance['mysql_table_prefix'])
    result = MySqlController.mysql_query(mysqlInterface, statement)

    if result == -1:
        JournalService.journal_add(
            client_guid(11),
            'CLIENT_BUILDTABLE_FAILED')
        return -1

    return 1


def client_insert_row(mysqlInstance, row):

    statement = "INSERT INTO {0}_client (uid, ip, label, entry, "
    statement+= "expiration, modified, created) "
    statement+= "VALUE (?, ?, ?, ?, ?, ?, ?)"

    statement = statement.format(config.configInstance['mysql_table_prefix'])

    created = time.strftime("%Y-%m-%d %H:%M:%S")
    modified = created

    row.append(modified)
    row.append(created)

    result = MySqlController.mysql_prepare(
        mysqlInstance, statement, row)

    if result == -1:
        JournalService.journal_add(
            client_guid(21),
            'CLIENT_INSERTROW_FAILED')
        return -1

    return MySqlController.mysql_get_insert_rowId(mysqlInstance)

def client_get_column(mysqlInstance, label, id, type = 'uid'):

    statement = "SELECT id, uid, ip, label, entry, "
    statement+= "expiration, modified, created "
    statement+= "FROM {0}_client WHERE {1} = ? AND label = ?;"

    statement = statement.format(
        config.configInstance['mysql_table_prefix'],
        type)

    try:

        MySqlController.mysql_prepare(
            mysqlInstance, statement, [id, label])

    except:

        JournalService.journal_add(
            client_guid(31),
            'CLIENT_GETROW_FAILED')
    
    listKey = ['id', 'uid', 'ip', 'label', 'entry',
        'expiration', 'modified', 'created', 'label']

    listColumn = MySqlController.mysql_get_column(mysqlInstance)
    if not listColumn:
        return None

    column = []
    for listRow in listColumn:

        row = {}
        for u in range(0, len(listKey)):
            row[listKey[u]] = listRow[u]

        column.append(row)

    return column


def client_update_row(mysqlInstance, row):

    statement = "UPDATE {0}_client SET uid = ?, ip = ?, label = ?, entry = ?, "
    statement+= "expiration = ?, modified = ?, created = ? WHERE id = ?;"

    statement = statement.format(
        config.configInstance['mysql_table_prefix'])

    row['modified'] = time.strftime("%Y-%m-%d %H:%M:%S")

    rowList = [
        row['uid'], row['ip'], row['label'], row['entry'],
        row['expiration'], row['modified'], row['created'], row['id']]

    result = MySqlController.mysql_prepare(
        mysqlInstance, statement, rowList)

    if result == -1:
        JournalService.journal_add(
            client_guid(41),
            'CLIENT_UPDATEROW_FAILED')
        return -1
    
    return row

def client_update_cache(mysqlInstance):

    statement = "DELETE FROM {0}_client WHERE expiration < ?;"
    statement = statement.format(
        config.configInstance['mysql_table_prefix'])

    currentTime = time.strftime("%Y-%m-%d %H:%M:%S")

    try:

        MySqlController.mysql_prepare(
            mysqlInstance, statement, [currentTime])

    except:

        JournalService.journal_add(
            client_guid(51),
            'CLIENT_UPDATECACHE_FAILED')

    return 0

def client_save(
        mysqlInstance, label, entry, expiration,
        id, type = 'uid'):

    client_update_cache(mysqlInstance)

    row = client_get_column(
        mysqlInstance, label, id, type)

    if row is None:

        if type == 'uid':

            client_insert_row(
                mysqlInstance, [id, '000.000.000.000',
                label, entry, expiration])

        else: 

            client_insert_row(
                mysqlInstance, [0, client_get_ip(),
                label, entry, expiration])

        return 0

    row['entry'] = entry
    row['expiration'] = expiration

    return client_update_row(mysqlInstance, row)
