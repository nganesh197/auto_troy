import json 
from hashing import hash_browns

def hold_creds():
    def pull_creds():
        with open('creds.json', 'r') as whofile:
            credentials = json.load(whofile)  
        return credentials['user']
    get_value = pull_creds()
    try:
        user = hash_browns(get_value['username'], 1)
        psswrd = hash_browns(get_value['password'], 0)
    except:
        user = ''
        psswrd = ''
    return user, psswrd
