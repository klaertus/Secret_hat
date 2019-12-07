#!/usr/bin/python
# coding: utf-8

from lib import crypto
import random

"""

This lib allows to encrypt, hash, decode and compare two hashed password with more security than the original lib crypto.py
by hashing several times the password to increase the time of cracking them by bruteforce

"""



def encode(password, message):

    """Hash password a random number of times and use these hashs as keys to encode message

    Args:
        password (str) : a password
        message (str) : a message

    Returns:
        string : the encrypted message, the hashed password, the encrypted first number and the encrypted second number, split by '|'
    """

    a = random.randint(50000,100000)
    b = random.randint(50000,100000)

    hashed_password = password
    for i in range(a):
        hashed_password = crypto.hashing(hashed_password)
        message = crypto.encode(hashed_password, message)


    for i in range(b):
        hashed_password = crypto.hashing(hashed_password)

    return message + str("|") + hashed_password + str("|") + crypto.encode(password, str(a)) + str("|") + crypto.encode(password, str(b))




def hash_password(password):

    """Hash a given password
    Args:
        password (str) : a password
    Returns:
        string : the hashed password, the encrypted first number and the encrypted second number, split by '|'
    """

    a = random.randint(50000,100000)
    b = random.randint(50000,100000)
    #key_enc = crypto.hashing(key)
    hashed_password = password
    for i in range(a):
        hashed_password = crypto.hashing(hashed_password)


    for i in range(b):
        hashed_password = crypto.hashing(hashed_password)

    return hashed_password + str("|") + crypto.encode(password, str(a)) + str("|") + crypto.encode(password, str(b))




def decode(password, encrypt_message, encrypt_random_a):

    """Decrypt a encrypted message with password
    Args:
        password (str) : the password
        encrypt_message (str) : the encrypted message
        encrypt_random_a (str) : the encrypted first number

    Returns:
        string : clear message
    """

    a = crypto.decode(password, encrypt_random_a)
    try:
        a = int(a)
    except:
        return 'none'
    list_hash = []
    for i in range(a):
        password = crypto.hashing(password)
        list_hash.append(password)
    for i in range(a):
        #print(5-1-i)
        encrypt_message = crypto.decode(list_hash[a-1-i], encrypt_message)

    return encrypt_message




def verify_pass(password, password_hash, encrypt_random_a, encrypt_random_b):

    """Verify a clear password with a given hash
    Args:
        password (str) : the password
        password_hash (str) : the password's hash
        encrypt_random_a (str) : the encrypted first number
        encrypt_random_b (str) : the encrypted second number

    Returns:
        bool : True if the password is correct
    """

    print(password)
    try:
        a = int(crypto.decode(password, encrypt_random_a))
        b = int(crypto.decode(password, encrypt_random_b))
        print(a,b)
    except:
        return False
    for i in range(a+b):
        password = crypto.hashing(password)

    print("passwords hashed :", password_hash, password)
    print(type(password_hash))
    if str(password) == str(password_hash):
        return True
    else:
        return False
