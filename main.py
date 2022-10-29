import threading
import os
from datetime import datetime
from colorama import init
from termcolor import colored
os.system('cls')
init()

print("Leo's SNKRDUNK Code Generator v1.0 | github.com/y3\n\n")

def LOG(text,color='white'):
    print(colored(f'[{datetime.now()}] {str(text)}',color))

LOG('Initializing program, setting up email', 'green')

from AccountGen import *
def task_starter(referral,num_of_task):
    AccountGenHandler().start_tasks(referral,num_of_task)

LOG('Successfully setup!', 'green')

while True:
    referral_code = input('\nPlease enter your SNKRDUNK referral code: ')
    if not len(referral_code) == 6:
        LOG('Error, your referral code has to be 6 characters - please check the guide on github.com/y3 for more info.', 'red')
    else:
        break

while True:
    referral_quantity = input('\nPlease enter the amount of SNKRDUNK coupons you want to generate: ')
    try:
        referral_quantity = int(referral_quantity)
        print('\n')
        LOG('Your codes will be generated now.\n\n\n', 'green')
        break
    except:
        LOG('Error, your value is not an integer.', 'red')


t = threading.Thread(target=task_starter,args=(referral_code,int(referral_quantity),))
t.start()
t.join()