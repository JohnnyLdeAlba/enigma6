import base64
import cgi
import hashlib
import hmac
import json
import random
import re
import smtplib
import time
import urllib

import config
from enigma import guid, JournalService

class IOInterface:
    pass

def io_guid(id = 0):
    return guid.guidInstance['IOLibrary']+id

def io_get_interface():

    ioInstance = IOInterface()
    ioInstance.fieldStorage = None

    return ioInstance

def io_initialize(ioInstance):

    ioInstance.fieldStorage = cgi.FieldStorage() 

def io_get_input(ioInstance, label):

    if label not in ioInstance.fieldStorage:
        return ''

    return ioInstance.fieldStorage.getvalue(label)

def io_set_variable(output, id, value):

    if isinstance(value, (int, long, float, complex)):
        value = str(value)

    pattern = r"%{}".format(id)
    output = re.sub(pattern, value, output)
 
    return output

def io_get_class(output, id):

    pattern = r"{{{0}}}(.*){{/{0}}}".format(id)
    match = re.search(pattern, output, flags = re.S)

    if not match:
        return None
 
    return match.group(1)

def io_set_class(output, id, value = ''):

    pattern = r"{{{0}}}.*{{/{0}}}".format(id)
    output = re.sub(pattern, value, output, flags = re.S)
 
    return output

def io_show_class(output, id):

    pattern = r"{{{0}}}".format(id)
    output = re.sub(pattern, '', output)

    pattern = r"{{/{0}}}".format(id)
    output = re.sub(pattern, '', output)
  
    return output

def io_display(output):

    header = "Content-Type: text/plain; charset=utf-8\n\n"
    output = header+output

    print(output)

def io_uri_encode(row):
    return urllib.urlencode(row)

def validate_signature(signature, row):

    current_time = int(time.strftime("%Y%m%d%H%M%S"))
    if row['expiration'] < current_time:

        JournalService.journal_add(
            io_guid(11),
            'SIGNATURE_EXPIRED')
        return -1

    result = io_uri_encode(row)

    validation = hmac.new(
        key = '',
        digestmod = hashlib.sh1).digest()

    validation = base64.b64encode(validation).decode('utf-8')
    if validation != signature:

        JournalService.journal_add(
            io_guid(12),
            'SIGNATURE_INVALID')
        return -2

    return 0

def io_json_encode(table):
    return json.dumps(table)

def io_json_decode(source):
    return json.loads(source)

def io_generate_randomString(length = 32):

    table = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    tableLength = len(table)
    
    milliSecond = 0
    randomValue = 0
    string = ''

    for u in range(0, length):

        milliSecond = int(time.clock()*100000)

        random.seed(milliSecond*(u+1))
        randomValue = int(random.random()*10)%tableLength

        string+= table[randomValue]

    return string

def io_encrypt(raw):
 
    key = config.configInstance['io_encryption_key']

    target = hmac.new(
        key = key.encode('utf-8'), 
        msg = raw.encode('utf-8'),
        digestmod = hashlib.sha1).digest()

    target = base64.b64encode(target)
    return target

def io_read_fileText(filename):

    fileInstance = open(filename, 'r')
    output = fileInstance.read()
    fileInstance.close()

    return output

def io_send_mail(

    senderName, senderEmail,
    receiverName, receiverEmail,
    subject, message):

    header = "From: {} <{}>"
    header+= "To: {} <{}>"

    header+= "Subject {}"
    header+= "MIME-Version: 1.0"
    header+= "Content-Type: text/html; charset=UTF-8"

    header = header.format(
        senderName, senderEmail,
        receiverName, receiverEmail, 
        subject)

    message = header+message

    smtpInstance = None

    try:

        if config.configInstance['server_host'] == '127.0.0.1':
            return 0

        else:

            smtpInstance = smtplib.SMTP(
                config.configInstance['smtp_host'])

        smtpInstance.sendmail(
            senderEmail,
            receiverEmail,
            message)

    except:

        JournalService.journal_add(
            io_guid(21), 
            'IO_SENDMAIL_FAILED')
        return -1

    finally: 

        if smtpInstance:
            smtpInstance.quit()

    return 0
