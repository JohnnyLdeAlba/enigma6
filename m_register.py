#!/usr/bin/env python3

import cgitb

import config
from enigma import *

cgitb.enable()

class MRegisterInterface:
    pass

def m_register_get_interface():

    mRegisterInstance = MRegisterInterface()

    mRegisterInstance.ioInstance = None
    mRegisterInstance.mysqlInstance = None

    return mRegisterInstance

def m_register_initialize(mRegisterInstance):

    ioInstance = IOLibrary.io_get_interface()
    IOLibrary.io_initialize(ioInstance)

    mysqlInstance = MySqlController.mysql_get_interface(
        config.configInstance['mysql_username'],
        config.configInstance['mysql_password'],
        config.configInstance['mysql_host'],
        config.configInstance['mysql_database'])

    MySqlController.mysql_connect(mysqlInstance)
    MySqlController.mysql_use_database(mysqlInstance)
    
    mRegisterInstance.ioInstance = ioInstance
    mRegisterInstance.mysqlInstance = mysqlInstance

def m_register_op_register(mRegisterInstance):
   
    ioInstance = mRegisterInstance.ioInstance 
    mysqlInstance = mRegisterInstance.mysqlInstance

    username = IOLibrary.io_get_input(ioInstance, 'username')
    email = IOLibrary.io_get_input(ioInstance, 'email')

    journalEntry = None

    row = UserService.user_register(
        mysqlInstance,
        username,
        email)

    MySqlController.mysql_close(mysqlInstance)
    mRegisterInstance.mysqlInstance = None

    if row > 0:

        output = IOLibrary.io_json_encode({

            'journalEntryId': 0,
            'journalEntryLabel': '',

            'username': row['username'],
            'email': row['email']})

    IOLibrary.io_display(output)

def m_register_process():

    mRegisterInstance = m_register_get_interface()

    try:

        m_register_initialize(mRegisterInstance)
        m_register_op_register(mRegisterInstance)

    except JournalService.JournalException as e:

        journalEntry = e.journalEntry

        output = IOLibrary.io_json_encode({

            'journalEntryId': journalEntry.id,
            'journalEntryLabel': journalEntry.label })

        IOLibrary.io_display(output)

#m_register_process()
IOLibrary.io_display(ClientService.client_get_agent())
