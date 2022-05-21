import os

configInstance = {}

configInstance['admin_email'] = 'johnny.dealba@vglimited.com'
configInstance['admin_name'] = 'Administrator'
configInstance['template_path'] = 'template/default/'
configInstance['website_name'] = 'VGLimited'

configInstance['io_encryption_key'] = 'Hs#Xx92ufZrk'
configInstance['mysql_table_prefix'] = 'enigma6'
configInstance['user_group_default'] = 'subscriber'
configInstance['user_validation_method'] = 'activation_key'

configInstance['smtp_host'] = 'a2s83.a2hosting.com'
configInstance['smtp_username'] = ''
configInstance['smtp_password'] = ''

try: configInstance['server_host'] = os.environ['SERVER_NAME']
except: configInstance['server_host'] = '127.0.0.1'

# Local Configuration
if configInstance['server_host'] in ('127.0.0.1', 'localhost'):

    configInstance['server_root'] = 'enigma6/'
    configInstance['server_uri'] = 'http://127.0.0.1/enigma6'

    configInstance['mysql_host'] = '127.0.0.1'
    configInstance['mysql_username'] = 'root'
    configInstance['mysql_password'] = ''
    configInstance['mysql_database'] = 'vglimited'

    configInstance['smtp_host'] = '127.0.0.1'
    configInstance['smtp_port'] = ''
    configInstance['smtp_username'] = ''
    configInstance['smtp_password'] = ''

# Network Configuration
else: 

    configInstance['server_root'] = ''
    configInstance['server_uri'] = 'http://www.vglimited.com/'

    configInstance['mysql_host'] = '127.0.0.1'
    configInstance['mysql_username'] = ''
    configInstance['mysql_password'] = ''
    configInstance['mysql_database'] = 'vglimited'

    configInstance['smtp_host'] = '127.0.0.1'
    configInstance['smtp_port'] = ''
    configInstance['smtp_username'] = ''
    configInstance['smtp_password'] = ''


