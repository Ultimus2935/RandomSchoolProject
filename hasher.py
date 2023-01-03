import os
import random
import string
import base64
import textwrap

def Hash(text: str, ini_salt: str = None):
    if ini_salt == None: salt = SaltGen()
    else: salt = ini_salt

    splitstr = textwrap.wrap((text + text[:-1])*3, 4)

    splitstr += Shuffle(splitstr, salt) + Shuffle(splitstr, salt+salt[::-1]) + Shuffle(splitstr, salt[:8]+salt[::-1]+salt[8:])

    enc = b''
    for _ in range(len(splitstr)//6 + 2):
        if len(splitstr) > 0: enc += base64.b64encode(splitstr[0].encode()) + b'$'
        if len(splitstr) > 1: enc += base64.b85encode(splitstr[1].encode()) + b'$'
        if len(splitstr) > 2: enc += base64.b32encode(splitstr[2].encode()) + b'$'
        if len(splitstr) > 3: enc += base64.b32encode(splitstr[3].encode()) + b'$'
        if len(splitstr) > 4: enc += base64.b85encode(splitstr[4].encode()) + b'$'
        if len(splitstr) > 5: enc += base64.b64encode(splitstr[5].encode()) + b'$'
        splitstr = splitstr[6:]

    if ini_salt == None: return (enc.decode(), salt) 
    else: return enc.decode()   

def SaltGen():
    chars = string.ascii_letters + string.digits
    salt = ''.join(random.choice(chars) for _ in range(16))
    return salt

def Shuffle(lst: list, salt: str):
        seed = sum(ord(i) for i in salt)
    
        length = len(lst)
        shuffled = [0]*length
        seed_pos = seed ^ 0xFFFF

        for i in list(reversed(range(length))):
            index = seed_pos % (i + 1)
            shuffled[i] = lst.pop(index)

        return shuffled

def interface():
    os.system('cls' if os.name == 'nt' else 'clear')

    while True:
        txt = input("Enter string to hash: ")
        
        if txt.lower() == "$~exit": break
        else: print(Hash(txt, input("Enter salt for hash: ")), "\n")
        