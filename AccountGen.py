import requests
import colorama
from datetime import datetime
from termcolor import *
from threading import Semaphore
import ctypes
import inspect
import time
from utility import *
from bs4 import *
import random
import concurrent.futures
from email_verification import *
from SMSHandler import *

config = Data().loadJson('config.json')
    

CATCHALL = config['catchall_domain']

ACTIVE_TASKS = 0
FAILED_TASKS = 0
SUCESSFUL_TASKS = 0
GETTING_CSRF = 0
CREATING_ACCOUNT = 0
WAITING_FOR_EMAIL = 0
GETTING_PHONE = 0
WAITING_FOR_SMS = 0
FINALISING = 0
headers = {
   
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    
}


TASKS = 3
MAX_WORKERS = 10
colorama.init()


proxies = Data().loadProxies('proxies.txt')


screen_lock = Semaphore(value=1)

class Gen:
   
    def __init__(self,task_num,referral):
        global ACTIVE_TASKS
        ACTIVE_TASKS += 1
        self.updateStatus()
        
        self.referral = referral
        self.task_num = task_num
        self.session = requests.Session()

        self.LOG('Starting Task')
        self.start_task()

    def start_task(self):
        global SUCESSFUL_TASKS
        global FINALISING
        global ACTIVE_TASKS
        if(self.getCSRF('https://snkrdunk.com/en/signup')):
            if(self.create_acount()):
                if(self.getEmailVerification()):
                    if(self.verifyEmail()):
                        if(self.sendPhoneVerification()):
                            if(self.getCSRF('https://snkrdunk.com/en/account/address?slide=right')):
                                if(self.verifyAddress()):
                                    if(self.applyreferral()):
                                        SUCESSFUL_TASKS += 1
                                        FINALISING -= 1
                                        ACTIVE_TASKS -= 1
                                        self.updateStatus()
                                        return True





        global FAILED_TASKS
        FAILED_TASKS += 1
        self.updateStatus()
        self.LOG('Task Failed','red')
        self.session = requests.Session()
        return self.start_task()

    def applyreferral(self):
        while True:
            self.LOG('Applying referral','yellow')
            try:
                {'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-GB,en;q=0.7',
                'content-length': '17',
                'content-type': 'application/json',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36}'}
                response = self.session.post('https://snkrdunk.com/en/v1/invitation',headers=headers,json={'code':self.referral})
            except:
                self.LOG('Request Error','red')
                time.sleep(1)
                continue

            if response.status_code == 200:
                self.LOG("Referral Applied",'green')
                return True
            elif response.status_code == 404:
                self.LOG("Referral code is incorrect.",'red')
                return True
            else:
                self.LOG("Bad Response Status "+str(response.status_code),'red')
                time.sleep(1)
                continue

    def verifyAddress(self):
        global FINALISING
        FINALISING += 1
        self.updateStatus()
        while True:
            self.LOG('Verifying Address')
            try:
                response = self.session.post('https://snkrdunk.com/en/account/address?slide=right',headers=headers,data={'firstName': 'ZZZ','lastName': 'ZZZ','phoneNumber':444000444,'country': 'AU','streetAddress': '300 Murray St','aptSuite': 'A','city': 'Perth','region': 'WA','postCode':6000,'csrf_token':self.csrf_token},proxies=random.choice(proxies))
            except:
                self.LOG("Request Error",'red')
                time.sleep(1)
                continue

            if response.status_code == 200:
                self.LOG('Address Verified')
                return True
            else:
                self.LOG("Bad Response Status "+str(response.status_code),'red')
                time.sleep(1)
                continue

        
    def updateStatus(self):
        ctypes.windll.kernel32.SetConsoleTitleW(f"AT: {str(ACTIVE_TASKS)} | FT: {str(FAILED_TASKS)} | ST: {str(SUCESSFUL_TASKS)} | GCSRF: {str(GETTING_CSRF)} | ACC: {str(CREATING_ACCOUNT)} | EMAIL: {str(WAITING_FOR_EMAIL)} | PHONE: {str(GETTING_PHONE)} | SMS: {str(WAITING_FOR_SMS)} | FINAL: {str(FINALISING)}")


    def sendPhoneVerification(self):
        global GETTING_PHONE
        GETTING_PHONE += 1
        self.updateStatus()

        while True:
            self.LOG('Verifying Phone')
            k = SMS(self.referral,self.task_num,self.session,proxies).start_task()
            if not k:
                self.LOG("Error while verifying phone",'red')   
                return False
            try:
                response = self.session.patch('https://snkrdunk.com/en/v1/account/sms-verification',headers=headers,json={'pinCode':k},proxies=random.choice(proxies))
            except Exception as e:
                print(e)
                self.LOG('Request Error','red')
                time.sleep(1)
                continue
            
            if response.status_code == 200:
                self.LOG("Phone Verified")
                GETTING_PHONE -= 1
                self.updateStatus()
                return True
            else:
                self.LOG("Bad Response Status "+str(response.status_code),'red')
                time.sleep(1)
                continue

    def LOG(self,text,color='white'):
        screen_lock.acquire()
        print(colored(f'[{datetime.now()}][{self.referral}][{str(self.task_num)}] [{str(inspect.stack()[1][3])}] {str(text)}',color))
        screen_lock.release()


    def create_acount(self):
        global CREATING_ACCOUNT
        CREATING_ACCOUNT += 1
        self.updateStatus()
        
        

        while True:
            self.LOG("Creating Account")
            self.username = 'john'+str(random.randint(0,9999))+'hig'+str(random.randint(0,9999))
            data = {
                'username': self.username,
                'email': self.username+"@"+CATCHALL,
                'password': 'Z1Snkrdunk!Z',
                'agreement': 'on',
                'csrf_token': self.csrf_token,
                'tzDatabaseName': 'Australia/Adelaide'
            }

            try:
                response = self.session.post('https://snkrdunk.com/en/signup',data=data,proxies=random.choice(proxies),headers=headers)
            except:
                self.LOG('Request Error','red')
                time.sleep(1)
                continue

            if response.status_code == 200:
                CREATING_ACCOUNT -= 1
                self.updateStatus()
                self.LOG('Account created')
                return True

            elif response.status_code == 403:
                self.LOG('Unauthorized Access','red')
                time.sleep(1)
                continue
            else:
                self.LOG("Bad Response Status "+str(response.status_code),'red')
                time.sleep(1)
                continue

    def verifyEmail(self):
        global WAITING_FOR_EMAIL
        while True:
            self.LOG("Verifying Email")
            try:
                response = self.session.get(self.activation_link,headers=headers,proxies=random.choice(proxies))
            except:
                self.LOG("Request Error",'red')
                time.sleep(1)
                continue

            if response.status_code == 200:
                self.LOG('Email Verified')
                WAITING_FOR_EMAIL -= 1
                self.updateStatus()
                return True
            elif response.status_code == 403:
                self.LOG("Unauthorized Access",'red')
                time.sleep(1)
                continue
            else:
                self.LOG("Bad Response Status "+str(response.status_code),'red')
                time.sleep(1)
                continue


    
    def getEmailVerification(self):
        self.LOG("Getting email verification.")
        global WAITING_FOR_EMAIL
        WAITING_FOR_EMAIL += 1
        self.updateStatus()
        global TASKS
        global MAX_WORKERS

        wait_time = float(MAX_WORKERS)*float(1.5)
        self.LOG('Waiting '+str(wait_time)+' seconds for email','yellow')
        time.sleep(wait_time)
        self.activation_link = IMAP().start(self.username,TASKS)
        if(self.activation_link == False):
            self.LOG('Email not found','red')
            return False

            
        self.LOG('Found activation link - '+self.activation_link)
        return True


    def getCSRF(self,url):
        global GETTING_CSRF
        GETTING_CSRF += 1

        self.updateStatus()
        while True:
            self.LOG('Getting CSRF Token')
            try:
                response = self.session.get(url,proxies=random.choice(proxies),headers=headers)
            except:
                self.LOG("Request Error",'red')
                time.sleep(1)
                continue

            if response.status_code == 200:
                soup = BeautifulSoup(response.content,'html.parser')
                try:
                    csrf_token = soup.find("input",attrs={'name':'csrf_token'})['value']
                except:
                    self.LOG('Error Loading CSRF Token','red')
                    time.sleep(1)
                    continue

                self.csrf_token = csrf_token
                GETTING_CSRF -= 1
                self.updateStatus()
                self.LOG('Got CSRF')
                return True

            elif response.status_code == 403:
                self.LOG('Unauthorized Access','red')
                time.sleep(1)
                continue
            else:
                
                self.LOG('Bad response status '+str(response.status_code),'red')
                time.sleep(1)
                continue





class AccountGenHandler:
    def start_tasks(self,referral,amount):
        self.referral = referral
        self.amount = amount
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            for i in range(self.amount):
                executor.submit(Gen,i,self.referral)
