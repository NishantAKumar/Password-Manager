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
SCREEN_TRANSITION_TIME = 0.7

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
    return cryptor.decrypt(cipher).decode().rstrip()   


def store_password(password, username, location):
    enc_pass = encrypt(password)
    database.insert_sensitive_data(enc_pass, username, location)

def update_password(id, password, username, location):
    enc_pass = encrypt(password)
    database.update_sensitive_data(id, enc_pass, username, location)
    

def show_passwords():
    print(f'\n identifier\t<password:username:location>\n')
    for (id, password, username, location) in database.read_sensitive_data():
        print(f' {id}\t\t<{decrypt(password)}:{username}:{location}>')


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


def admin_deletion(username, password):
    (id, uname, passwd, logged_in) = get_admin()
    if logged_in:
        if username == uname and hashlib.sha512(password.encode()).hexdigest() == passwd:
            database.delete_all_sensitive_data()
            return True

def screen_formatter():
    time.sleep(SCREEN_TRANSITION_TIME)
    if platform.system() == "Linux":
        os.system("clear")
    elif platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

if get_admin() is not None:
    admin_logout()
try:
    while True:
        if get_admin() is None:
            print("\n Admin Sign-Up")
            username = input(" Username:")
            password = input(" Password:")
            print(" Creating Admin Account... Please Wait")
            admin_registration(username, password)
            print(" Done")
            screen_formatter()
            
        else:
            (id, uname, passwd, logged_in) = get_admin()
            if logged_in == 0:
                print("\n Admin Sign-In")
                username = input(" Username:")
                password = input(" Password:")
                print(" Authenticating... PLease Wait")
                login = admin_login(username, password)
                if not login:
                    print(" Error... Try Again!")
                else:
                    print(" Done")
                screen_formatter()
            
            while logged_in == 1:
                print("\n Options:\n 1:Save Passwords\n 2:Show Passwords\n 3:Update a Password\n L:Logout\n D:Admin Account Deletion\n U:Admin Account Update")
                option = input(" Enter:")
                screen_formatter()
                if option == "L":
                    print(" Signing Out... Please Wait")
                    admin_logout()
                    print(" Done")
                    screen_formatter()
                    (id, uname, passwd, logged_in) = get_admin()

                elif option == "D":
                    print("\n Admin Deletion!")
                    username = input(" Username:")
                    password = input(" Password:")
                    print(" Deleting Admin Account... Please Wait")
                    admin_deletion(username, password)
                    print(" Done")
                    screen_formatter()
                    break

                elif option == "3":
                    while True:
                        print(f'\n Identifier\tpassword:username:location')
                        for (id, password, username, location) in database.read_sensitive_data():
                            print(f' {id}\t\t{decrypt(password)}:{username}:{location}')
                        i = int(input(" Identifier of entry to be updated:"))
                        setted_id = -1
                        for (id, password, username, location) in database.read_sensitive_data():
                            if i == int(id):
                                setted_id = int(id)
                                break
                        if setted_id != -1:
                            print(" Entry Selected")
                            print(" Enter Updated:")
                            updated_username = input("  Username:")
                            updated_password = input("  Password:")
                            updated_location = input("  Location:")
                            save = input(" Save? y/n:")
                            if save == "y":
                                update_password(setted_id, updated_password, updated_username, updated_location)
                            elif save == "n":
                                break
                            cont = input(" Continue updating password? y/n:")
                            if cont == "y":
                                print("Please wait...")
                                screen_formatter()
                            else:
                                screen_formatter()
                                break
                        else:
                            print(" Entry Not Found..Try Again!")
                            screen_formatter()
                            continue


                elif option == "2":
                    show_passwords()
                    if input("-1 to go back:") == "-1":
                        screen_formatter()
                        break
                
                elif option == "1":
                    while True:
                        p = input("\n Password to be stored [cannot be blank]:")
                        u = input(" Username for the password [can be blank]:")
                        l = input(" URL for the credentials [can be blank]:")
                        save = input(" Save? y/n:")
                        if save == "y":
                            store_password(p, u, l)
                        elif save == "n":
                            break
                        cont = input(" Continue saving password? y/n:")
                        if cont == "y":
                            print(" Please wait...")
                            screen_formatter()
                        else:
                            screen_formatter()
                            break

except KeyboardInterrupt:
    print("\n System Shutting")
    sys.exit()