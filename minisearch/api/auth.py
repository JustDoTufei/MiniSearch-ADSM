'''
Created on May 24, 2015

@author: luodichen
'''

import time
#import secrets
import json


def user_auth(user, password):
    if None == user or None == password:
        return False

    with open('secret.txt', 'r') as file_tmp:
        secret = file_tmp.read()
    secret = json.loads(secret)

    if not user in secret:
        return False
    
    return password == secret[user]


def set_login(request):
    request.session.set_expiry(0)
    request.session['login'] = time.time()

    user = request.POST['user']
    request.session['user'] = user


def set_logout(request):
    try:
        del request.session['login']
        del request.session['user']
    except:
        pass


def check_login(request):
    return 'login' in request.session
