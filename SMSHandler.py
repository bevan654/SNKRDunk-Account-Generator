import requests
from threading import Semaphore
import colorama
from datetime import datetime
from termcolor import *
import inspect
import time
import random
from utility import *
from urllib import response
import threading
import email_verification
screen_lock = Semaphore(value=1)
colorama.init()

config = Data().loadJson('config.json')
country_code = config['country_code']
api_key = config['smspva_apikey']

class SMS:
    def __init__(self,refferal,task_num,session,proxies):
        self.proxies = proxies
        self.session = session
        self.refferal = refferal
        self.task_num = task_num

        

    def LOG(self,text,color='white'):
        screen_lock.acquire()
        print(colored(f'[{datetime.now()}][{self.refferal}][{str(self.task_num)}] [{str(inspect.stack()[1][3])}] {str(text)}',color))
        screen_lock.release()

    def start_task(self):
        if(self.getNumber()):
            time.sleep(3)
            if(self.sendSMS()):
                time.sleep(3)
                return self.retrieveSMS()

    def sendSMS(self):
        count = 0
        headers = {
            'authority': 'snkrdunk.com',
            'method': 'POST',
            'path': '/en/v1/account/sms-verification',
            'scheme': 'https',
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://snkrdunk.com',
            'referer': 'https://snkrdunk.com/en/account/phone-number?slide=right',
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
        }
        while True:


            if count == 10:
                self.cancelPhone()
                return False
            self.LOG('Sending SMS')
            try:
                response = self.session.post('https://snkrdunk.com/en/v1/account/sms-verification',headers=headers,json={"countryCode":'ID',"phoneNumber":self.phoneNumber},proxies=random.choice(self.proxies))
            except:
                self.LOG('Request Error','red')
                time.sleep(1)
                continue
            

            if response.status_code == 200:
                self.LOG("SMS Sent")
                return True
            elif 'already' in str(response.content) and response.status_code == 409:
                self.LOG("Phone number already used",'red')
                self.cancelPhone()
                self.getNumber()
                time.sleep(1)
                continue
            else:
                count += 1
                self.LOG("Bad Response Status "+str(response.status_code),'red')
                time.sleep(1)
                continue



    def cancelPhone(self):
        
        while True:
            self.LOG('Cancelling phone number')
            try:
                response = requests.get(f'https://smspva.com/priemnik.php?metod=ban&country=ID&service=opt19&id='+str(self.phoneNumber_id)+'&apikey='+api_key)
            except:
                self.LOG('Request Error','red')
                time.sleep(1)
                continue

            if response.status_code == 200:
                self.LOG('Number cancelled')
                return True
            else:
                self.LOG("Bad Response Status "+str(response.status_code),'red')
                time.sleep(1)
                continue

    def retrieveSMS(self):
        count = 0 
        while True:
            count += 1
            if count == 6:
                self.sendSMS()

            if count == 12:
                self.cancelPhone()
                self.getNumber()
                self.sendSMS()
                count = 0

            self.LOG("Retrieving SMS ("+str(count)+')')
            try:
                response = requests.get('https://smspva.com/priemnik.php?metod=get_sms&country=ID&service=opt19&id='+str(self.phoneNumber_id)+'&apikey='+api_key)
            except:
                self.LOG('Request Error','red')
                time.sleep(1)
                continue

            if response.status_code == 200:
                try:
                    response = response.json()
                except:
                    self.LOG('Error Loading JSON','red')
                    time.sleep(1)
                    continue
                
                if response['response'] != '1':
                    self.LOG("Waiting for SMS ("+str(count)+')')
                    time.sleep(10)
                    continue
                else:
                    self.LOG("Got SMS",'yellow')
                    return response['text'].split(':')[1].strip()

            else:
                self.LOG("Bad Response Status "+str(response.status_code),'red')
                time.sleep(1)
                continue

    def getNumber(self):
        no_number_count = 0
        while True:
            self.LOG('Requesting Number')
            try:
                response = requests.get('https://smspva.com/priemnik.php?metod=get_number&country=ID&service=opt19&apikey='+api_key)
            except:
                self.LOG('Request Error','red')
                time.sleep(1)
                continue

            if response.status_code == 200:
                try:
                    response = response.json()
                except:
                    self.LOG('Error Loading JSON','red')
                    time.sleep(1)
                    continue

                if(response['response'] == '1'):
                    self.phoneNumber = str(response['number'])
                    self.phoneNumber_id = str(response['id'])
                    self.LOG("Got Number")
                    return True
                else:
                    self.LOG("Error while getting whole number",'red')
                    no_number_count += 1
                    print(response)
                    time.sleep(1)
                    continue

            elif response.status_code == 403:
                self.LOG("Unauthorized Access")
                time.sleep(1)
                continue
            else:
                self.LOG("Bad Response Status "+str(response.status_code),'red')
                time.sleep(1)
                continue


