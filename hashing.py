from base64 import encode
import random
import json

values = {}
values['user'] = {}

def encoder(word):
    seed = random.randint(1,100)
    random.seed(seed)
    l = list(word)
    random.shuffle(l)
    scrambled_word = ''.join(l)
    return seed, scrambled_word

def decoder(seed, scrambled_word):
    random.seed(seed)
    order = list(range(len(scrambled_word)))
    random.shuffle(order)

    original_word = [0]*len(scrambled_word)
    for index,original_index in enumerate(order):
        original_word[original_index] = scrambled_word[index]
    return ''.join(original_word)

def command_line_encode_details(): 
    print("THESE ARE STORED LOCALLY ON YOUR COMPUTER AND THE PASSWORD IS HASHED")
    print("Please input your login credentials")
    print("Username: ")
    u_word = input()
    print("Password: ")
    p_word = input() 
    encode_details(u_word, p_word)

def encode_details(u_word, p_word):

    p_key_val, p_scrambled_word = encoder(p_word)
    u_key_val, u_scrambled_word = encoder(u_word)
    values['user'] = {
        "username": u_scrambled_word,
        "password": p_scrambled_word
    }
    huh_val = {}
    huh_val["test_value"] = [p_key_val, u_key_val]
    with open('creds.json', 'w') as sendfile:
        json.dump(values, sendfile)
    with open('auto_checker.json', 'w') as whofile:
        json.dump(huh_val, whofile)   
    
def hash_browns(word, section):
    with open('auto_checker.json', 'r') as whofile:
        finder_val = json.load(whofile) 
    return decoder(finder_val['test_value'][section], word)
