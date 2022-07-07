from telnetlib import LOGOUT
import uuid
from db import Database
import hashlib
from Crypto.Cipher import AES
import time
import sys
import os
import platform

CIPHER_PADDED_LENGTH = 128

database = Database("pass_enc.db")

def get_admin():
    if len(database.read_admin_data()) == 1:
        return database.read_admin_data()[0]

def get_hash():
    (id, username, password, logged_in) = get_admin()
    return hashlib.sha512(f"{username}{password}".encode()).hexdigest()[0:32]

def encrypt(password):
    hash_val = get_hash()
    cryptor = AES.new(hash_val.encode(), mode=1)
    padded_message = password + " "*(CIPHER_PADDED_LENGTH-len(password))
    cipher = cryptor.encrypt(padded_message.encode())
    return cipher


def decrypt(cipher):
    hash_val = get_hash()
    cryptor = AES.new(hash_val.encode(), mode=1)
    return cryptor.decrypt(cipher)    


def store_password(password, username, location):
    enc_pass = encrypt(password)
    database.insert_sensitive_data(enc_pass, username, location)

def show_passwords():
    for (id, password, username, location) in database.read_sensitive_data():
        print(decrypt(password).decode().rstrip())


def admin_login(username, password):
    (id, uname, passwd, logged_in) = get_admin()
    if not logged_in:
        if username == uname and hashlib.sha512(password.encode()).hexdigest() == passwd:
            database.admin_logged_in_setter(id=id, value=1)
            return True

def admin_logout():
    (id, uname, passwd, logged_in) = get_admin()
    if logged_in:
        database.admin_logged_in_setter(id=id, value=0)
        return True

def admin_registration(username, password):
    if get_admin() is None:
        database.insert_admin_data(username, hashlib.sha512(password.encode()).hexdigest())
    else:
        (id, uname, passwd, logged_in) = get_admin()

def admin_deletion(username, password):
    (id, uname, passwd, logged_in) = get_admin()
    if logged_in:
        if username == uname and hashlib.sha512(password.encode()).hexdigest() == passwd:
            database.delete_all_sensitive_data()
            return True


def screenManager():
    time.sleep(0.5)
    if platform.system() == "Linux":
        os.system("clear")
    elif platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

if get_admin() is not None:
    admin_logout()

while True:
    if get_admin() is None:
        print("\n Admin Sign-Up")
        username = input(" Username:")
        password = input(" Password:")
        print(" Creating Admin Account... Please Wait")
        admin_registration(username, password)
        print(" Done")
        screenManager()
        
    else:
        (id, uname, passwd, logged_in) = get_admin()
        if logged_in == 0:
            print("\n Admin Sign-In")
            username = input(" Username:")
            password = input(" Password:")
            print(" Authenticating... PLease Wait")
            admin_login(username, password)
            print(" Done")
            screenManager()
        
        while logged_in == 1:
            print("\n Options:\n 1:Save a Password\n 2:Show Passwords\n 3:Update a Password\n L:Logout\n D:Admin Account Deletion")
            option = input(" Enter:")
            if option == "L":
                print(" Signing Out... Please Wait")
                admin_logout()
                print(" Done")
                screenManager()
                (id, uname, passwd, logged_in) = get_admin()

            elif option == "D":
                print("\n Admin Deletion!")
                username = input(" Username:")
                password = input(" Password:")
                print(" Deleting Admin Account... Please Wait")
                admin_deletion(username, password)
                print(" Done")
                screenManager()
                break