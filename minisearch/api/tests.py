#from django.test import TestCase

# Create your tests here.
import json
data = {'ca':'canimei'}
'''


with open('secret.txt', 'w') as file_tmp:
    json_str = json.dumps(data)
    file_tmp.write(json_str)


'''
with open('secret.txt', 'r') as file_tmp:
    secret = file_tmp.read()

secret = json.loads(secret)

print secret['ca']

