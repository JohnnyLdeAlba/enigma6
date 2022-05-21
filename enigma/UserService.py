import re
import os
import time

import config
from enigma import guid, IOLibrary, JournalService, MySqlController, ClientService

def user_guid(id = 0):
    return guid.guidInstance['UserService']

def user_build_table(mysqlInterface):

    statement = "CREATE TABLE {0}_user ("

    statement+= "id BIGINT(32) UNSIGNED AUTO_INCREMENT, "
    statement+= "ip CHAR(16) NOT NULL, "

    statement+= "email VARCHAR(256) NOT NULL, "
    statement+= "password VARCHAR(256) NOT NULL, "
    statement+= "activation_key VARCHAR(256) NOT NULL, "

    statement+= "username VARCHAR(256) NOT NULL, "
    statement+= "fullname VARCHAR(256) NOT NULL, "
    statement+= "description TEXT NOT NULL, "
    statement+= "attachment_filename VARCHAR(256) NOT NULL, "
    
    statement+= "user_group VARCHAR(32) NOT NULL, "
    statement+= "status VARCHAR(32) NOT NULL, "
    statement+= "attribute VARCHAR(32) NOT NULL, "

    statement+= "last_online DATETIME NOT NULL, "
    statement+= "modified DATETIME NOT NULL, "
    statement+= "created DATETIME NOT NULL, "

    statement+= " PRIMARY KEY(id)"
    statement+= ") ENGINE = MyISAM;"

    statement = statement.format(config.configInstance['mysql_table_prefix'])
    result = MySqlController.mysql_query(mysqlInterface, statement)

    if result == -1:
        JournalService.journal_add(
            user_guid(11),
            'USER_BUILDTABLE_FAILED')
        return -1

    return 1

def user_insert_row(mysqlInstance, row):

    statement = "INSERT INTO {0}_user (ip, email, password, activation_key, "
    statement+= "username, fullname, description, attachment_filename, "
    statement+= "user_group, status, attribute, last_online, modified, created) "
    statement+= "VALUE (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    statement = statement.format(config.configInstance['mysql_table_prefix'])

    created = time.strftime("%Y-%m-%d %H:%M:%S")
    modified = created
    last_online = ''

    row.append(created)
    row.append(modified)
    row.append(last_online)

    result = MySqlController.mysql_prepare(
        mysqlInstance, statement, row)

    if result == -1:
        JournalService.journal_add(
            user_guid(21),
            'USER_INSERTROW_FAILED')
        return -1

    return MySqlController.mysql_get_insert_rowId(mysqlInstance)

def user_get_column(mysqlInstance, id, type = 'id'):

    statement = "SELECT id, ip, email, password, activation_key, "
    statement+= "username, fullname, description, attachment_filename, "
    statement+= "user_group, status, attribute, last_online, modified, created "
    statement+= "FROM {0}_user WHERE {1} = ?;"
    statement = statement.format(
        config.configInstance['mysql_table_prefix'],
        type)

    result = MySqlController.mysql_prepare(
        mysqlInstance, statement, [id])

    if result == -1:
        JournalService.journal_add(
            user_guid(31),
            'USER_GETROW_FAILED')
        return -1
    
    listKey = ['id', 'ip', 'email', 'password', 'activation_key',
        'username', 'fullname', 'description', 'attachment_filename',
        'user_group', 'status', 'attribute', 'last_online', 'modified', 'created']

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


def user_update_row(mysqlInstance, row):

    statement = "UPDATE {0}_user SET ip = ?, email = ?, password = ?, activation_key = ?, "
    statement+= "username = ?, fullname = ?, description = ?, attachment_filename = ?, "
    statement+= "user_group = ?, status = ?, attribute = ?, "
    statement+= "last_online = ?, modified = ?, created = ? WHERE id = ?;"

    statement = statement.format(
        config.configInstance['mysql_table_prefix'])

    row['modified'] = time.strftime("%Y-%m-%d %H:%M:%S")

    rowList = [
        row['ip'], row['email'], row['password'], row['activation_key'],
        row['username'], row['fullname'], row['description'], row['attachment_filename'],
        row['user_group'], row['status'], row['attribute'],
        row['last_online'], row['modified'], row['created'], row['id']]

    result = MySqlController.mysql_prepare(
        mysqlInstance, statement, rowList)

    if result == -1:
        JournalService.journal_add(
            user_guid(41),
            'USER_UPDATEROW_FAILED')
        return -1
    
    return row

def user_validate_username(username):

    if not isinstance(username, str):
        JournalService.journal_add(
            user_guid(51),
            'USER_INVALIDTYPE_USERNAME')
        return -1

    if username == '':
        JournalService.journal_add(
            user_guid(52),
            'USER_EMPTY_USERNAME')
        return -2

    match = re.match(r'.{3,32}', username)
    if match == None:
        JournalService.journal_add(
            user_guid(53),
            'USER_CHARCOUNT_USERNAME')
        return -3

    match = re.match(r'^[a-z0-9-_]+$', username)
    if match == None:
        JournalService.journal_add(
            user_guid(54),
            'USER_ILLEGALCHARS_USERNAME')
        return -4

    return 0

def user_validate_email(email):
    
    if not isinstance(email, str):
        JournalService.journal_add(
            user_guid(61), 
            'USER_INVALIDTYPE_EMAIL')
        return -1

    if email == '':
        JournalService.journal_add(
            user_guid(62),
            'USER_EMPTY_EMAIL')
        return -2

    match = re.match(r'^[a-z0-9@-_.]+$', email)
    if match == None:
        JournalService.journal_add(
            user_guid(63),
            'USER_ILLEGALCHARS_EMAIL')
        return -3

    pattern = r'^[a-z0-9%-_+.]+@[a-z0-9-_.]+\.[a-z0-9]{2,}$'
    match = re.match(pattern, email)

    if match == None:
        JournalService.journal_add(
            user_guid(64),
            'USER_INVALIDFORMAT_EMAIL')
        return -4
    
    return 0

def user_validate_password(password):

    if not isinstance(password, str):
        JournalService.journal_add(
            user_guid(71),
            'USER_INVALIDTYPE_PASSWORD')
        return -1

    if password == '':
        JournalService.journal_add(
            user_guid(72),
            'USER_EMPTY_PASSWORD')
        return -2

    match = re.match(r'.{4,32}', password)
    if match == None:
        JournalService.journal_add(
            user_guid(73),
            'USER_CHARCOUNT_PASSWORD')
        return -3
 
    match = re.match(r'^[A-Za-z0-9-_]+$', password)
    if match == None:
        JournalService.journal_add(
            user_guid(74),
            'USER_ILLEGALCHARS_PASSWORD')
        return -4

    return 0

def user_get_client_ip():

    try: client_ip = os.environ['REMOTE_ADDR']
    except: client_ip = '127.0.0.1'

    return client_ip
    

def user_generate_password():

    password = IOLibrary.io_generate_randomString(8)
    return password

def user_get_activation_key():

    activation_key = IOLibrary.io_generate_randomString()
    activation_key = IOLibrary.io_encrypt(activation_key)

    return activation_key

def user_mail_registration(row):

    template_path = config.configInstance['template_path']

    output = IOLibrary.io_read_fileText(
        template_path+'mail-registration.txt')

    admin_email = config.configInstance['admin_email']
    admin_name = config.configInstance['admin_name']
    server_uri = config.configInstance['server_uri']
    website_name = config.configInstance['website_name']

    subject = "Welcome to {}!".format(website_name)

    output = IOLibrary.io_set_variable(output, 'server_uri', server_uri)
    output = IOLibrary.io_set_variable(output, 'website_name', website_name)
    output = IOLibrary.io_set_variable(output, 'username', row['username'])

    user_validation_method = config.configInstance['user_validation_method']
    if user_validation_method == 'activation_key':

        output = IOLibrary.io_set_class(output, 'generate_password')
        output = IOLibrary.io_show_class(output, 'activation_key')

        activation_uri = IOLibrary.io_uri_encode(
            {'id': row['id'], 'key': row['activation_key']})
        activation_uri = 'activate?'+activation_uri

        output = IOLibrary.io_set_variable(output, 'activation_uri', activation_uri)

    else:

        output = IOLibrary.io_set_class(output, 'activation_key')
        output = IOLibrary.io_show_class(output, 'generate_password')
        output = IOLibrary.io_set_variable(output, 'password', row['password'])

    output = re.sub("\/w[ ]{4,8}", '', output) 
    output = re.sub(r'[\r\n]', '', output)
    output = re.sub("\/r\/n", "\r\n", output)

    result = IOLibrary.io_send_mail(
        admin_name, admin_email,
        row['username'], row['email'],
        subject,
        output)

    return result

def user_register(mysqlInstance, username, email, password = ''):

    if user_validate_username(username) is not 0:
        return -1
    if user_validate_email(email) is not 0:
        return -2

    username = username.lower()
    email = email.lower()

    status = 'enabled'
    activation_key = ''

    if password == '':

        status = 'pending'

        password = IOLibrary.io_generate_randomString(16)
        activation_key = user_get_activation_key()

    elif user_validate_password(password) is not 0:
        return -3

    row = user_get_column(mysqlInstance, username, 'username')
    if row is not None:

        JournalService.journal_add(
            user_guid(84),
            'USER_USERNAME_EXISTS')
        return -4

    row = user_get_column(mysqlInstance, email, 'email')
    if row is not None:

        JournalService.journal_add(
            user_guid(85),
            'USER_EMAIL_EXISTS')
        return -5

    user_group_default = config.configInstance['user_group_default']
    encrypted_password = IOLibrary.io_encrypt(password)

    row = [
        ClientService.client_get_ip(),
        email,
        encrypted_password,
        activation_key,
        username, '', '', '',
        user_group_default, status, '']

    id = user_insert_row(mysqlInstance, row)
    if id > 0:
        
        row = user_get_column(mysqlInstance, id)[0]

        if status == 'pending':
            row['password'] = password
            user_mail_registration(row)

    row['password'] = encrypted_password
    return row
