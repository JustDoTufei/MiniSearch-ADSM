'''
Created on May 24, 2015

@author: luodichen
'''

import time
import secrets

def user_auth(user, password):
    if None == user or None == password:
        return False
    
    if not user in secrets.user:
        return False
    
    return password == secrets.user[user]

def set_login(request):
    request.session.set_expiry(0)
    request.session['login'] = time.time()
    
def set_logout(request):
    try:
        del request.session['login']
    except:
        pass
    
def check_login(request):
    return 'login' in request.session
