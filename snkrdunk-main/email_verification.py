
from imap_tools import MailBox
from utility import *

config = Data().loadJson('config.json')

EMAIL = config['email_address']
PASSWORD = config['email_app_password']
SERVER = 'imap.gmail.com'
CATCHALL = config['catchall_domain']

MailBox(SERVER).login(EMAIL,PASSWORD)
class IMAP:
    def __init__(self):
        self.email = EMAIL
        self.password = PASSWORD
        self.server = SERVER


    def get_verification_link(self,username,num_of_task):
        count = 0
        with MailBox(self.server).login(self.email, self.password,'INBOX') as self.mailbox:
            for msg in self.mailbox.fetch("TEXT activationKey",reverse=True):
                count += 1
                if count > int(num_of_task)*2:
                    return False

                if(username.lower() in list(msg.to)[0].lower()):
                    return msg.text.split('▼Click here to register as a member.')[1].strip().split("Note")[0].strip()

    def start(self,username,num_of_task):
        return self.get_verification_link(username,num_of_task)

