import random
import os
import hashlib
import getpass
import sys

user = getpass.getuser()


def validation():
    try:
        global validation_token
        validation_token = getpass.getpass('Enter the Key: ')
        hash_0 = hashlib.sha512((validation_token.encode())).hexdigest()
        tp_file = open(f'C://Users//{user}//Documents//validation_of_user.txt', 'r')
        sha = tp_file.readlines()
        tp_file.close()
        if hash_0 == sha[0]:
            greeting()
        else:
            print('User Validation Failed !')
            validation()
    except KeyboardInterrupt:
        print("Exiting...")
        os._exit(0)
    
    except:
        print('Admin Account not configured consider running AdminConfig !')
        validation()


def mainmenu():
    choice = int(input('''What do you want to do: 
1. Create a Password
2. Save a Password
3. Retrieve Saved Passwords
4. Encrypt Messages
5. Decrypt Messages
6. Delete Saved Passwords
7. Admin Account Deletion
8. Exit
0. For Tool Deletion Procedure
99. To clear the screen
\nEnter your choice: '''))
    if choice == 1:
        s = input("Enter the alphabets with which you want to create the password [Include uppercase if needed]: ")

        speci = input('Do you want special characters in your password [Y/N]: ')
        speci_length = 0
        if speci.lower() == 'y':
            speci_length = int(input('Enter the no. of special characters you need in the password: '))

        numeri = input('Do you want numerics in your password [Y/N] [ONLY SINGLE DIGIT]: ')
        numeri_length = 0
        if numeri.lower() == 'y':
            numeri_length = int(input('Enter the no. of numerics you want in  your password: '))

        password = jumbler(s, speci, numeri, speci_length, numeri_length)
        print('New password according to your specifications is: ')
        for i in password:
            print(i, end='')
        print()

        print('If you do not like this password then I can create another one for you...')
        like = input('Do you like this password [Y/N]: ')
        while like.lower() == 'n':
            del password
            specs = input('Do you want to edit the specifications [Y/N]:')
            if specs.lower() == 'y':
                s = input(
                    "Enter the alphabets with which you want to create the password [Include uppercase if needed]: ")
                speci = input('Do you want special characters in your password [Y/N]: ')
                speci_length = 0
                numeri_length = 0
                if speci.lower() == 'y':
                    speci_length = int(input('Enter the no. of special characters you need in the password: '))
                numeri = input('Do you want numerics in your password [Y/N] [ONLY SINGLE DIGIT]: ')
                if numeri.lower() == 'y':
                    numeri_length = int(input('Enter the no. of numerics you want in  your password: '))
                password = jumbler(s, speci, numeri, speci_length, numeri_length)
                print('New password according to your specifications is: ')
                for i in password:
                    print(i, end='')
                print()

            else:
                print('I am creating another password keeping the specifications same...')
                password = jumbler(s, speci, numeri, speci_length, numeri_length)
                print('New password is: ')
                for i in password:
                    print(i, end='')
                print()
            like = input('Do you like the password now [Y/N]: ')
        if like.lower() == 'y':
            save = input(
                'I can also save the password for you on your PC in hashed form. Do you want to save your password [Y/N]: ')
            if save.lower() == 'y':
                save_pass(password)
            else:
                mainmenu()
    elif choice == 2:
        pwd = []
        passwd = input('Enter the password that you want to save: ')
        for i in passwd:
            pwd.append(i)
        save_pass(pwd)

    elif choice == 3:
        length = 0
        string_2 = f'C://Users//{user}//Documents//pgph.txt'
        print('''If Usernames and Account names have been saved they will be in the following format: 
PASSWORD||USERNAME||ACCOUNT NAME''')
        try:
            a = open(string_2, "r")
            for i in a:
                length += 1
            a.close()
            if length == 0:
                print('There are no passwords saved.')
            else:
                decrypt(string_2)
        except FileNotFoundError:
            print('There are no passwords saved')
            mainmenu()

    elif choice == 4:
        print('''Kindly note that messages encrypted using this tool
can be decrypted using this tool only.''')
        st = input("Enter the message you want to encrypt: ")
        encryption(st)

    elif choice == 5:
        sl = input("Enter the message you want to decrypt: ")
        decryption(sl)
    elif choice == 6:
        clear()

    elif choice == 7:
        uninstall()
    elif choice == 8:
        print('******************************************')
        print('THANKS FOR USING PASSWORD MANAGER')
        print('******************************************')
        sys.exit()
    elif choice == 0:
        deletion()
    elif choice == 99:
        os.system('cls')
        mainmenu()
    else:
        print("invalid input !")
        mainmenu()

def save_pass(passwd):
    string = f'C://Users//{user}//Documents//pgph.txt'
    username_check = input('Do you want to associate this password with an account and username [Y/N]: ')
    if username_check.lower() == 'y':
        username = input('Enter Username: ')
        accountname = input('Enter Account Name: ')
        passwd.append('|')
        passwd.append('|')
        for i in username:
            passwd.append(i)
        passwd.append('|')
        passwd.append('|')
        for j in accountname:
            passwd.append(j)
    encrypt(passwd, string)
    if username_check.lower() == 'y':
        print('''Your password and other credentials have been secured by me.''')
    else:
        print('''Your password has been secured by me.''')
    mainmenu()


def encryption(to_be_encrypted):
    enc = []
    x = random.randint(2000000, 2999800)
    for letters in to_be_encrypted:
        enc.append((ord(letters) + x))
    enc.append(x)
    print('---------------------------------------------')
    for i in enc:
        print(i, end='')
    print('\n---------------------------------------------')
    print('\nThis is the encrypted string. For decryption paste the exact same string in the decryptor.')
    mainmenu()


def decryption(to_be_decrypted):
    try:
        if len(to_be_decrypted) % 7 == 0:
            number = int(to_be_decrypted[len(to_be_decrypted)-7: len(to_be_decrypted)])
            temp = []
            dec = []
            for j in range(int(len(to_be_decrypted) / 7)):
                hep = to_be_decrypted[int(7 * j): int(14 * (j + 1) / 2)]
                temp.append(int(hep))
            for h in temp:
                dec.append(chr(h - number))
            print('---------------------------------------------')
            for m in dec:
                print(m, end='')
            print('\n---------------------------------------------')
            print('\nThis is the decrypted message.')
    except:
        print('The data has been tampered.')
    mainmenu()
        
    

def encrypt(to_be_encrypted, location):
    enc = []
    file = open(location, "a")
    for letters in to_be_encrypted:
        enc.append((ord(letters) + 2035803883))
    z = str(enc).replace('[', '').replace(']', '').replace(',', '')
    file.write(f'{z}\n')
    file.close()


def decrypt(location):
    file = open(location, "r")
    line = file.readlines()
    for p in line:
        decode = []
        temp = p.split(' ')
        for n in temp:
            if '\n' in n:
                n.replace('\n', '')
            decode.append(chr(int(n) - 2035803883))
        for l in decode:
            print(f'{l}', end='')
        print('\n')
    print('This is the data which you have saved.')
    file.close()
    mainmenu()


def jumbler(pwd, special, num, special_length, num_length):
    generated = []
    upper = ['!', '@', '#', '$', '%', '&', '*']
    for j in range(len(pwd)):
        generated.append(pwd[j])
    if special.lower() == 'y':
        for k in range(special_length):
            ran = random.randint(0, len(upper) - 1)
            generated.append(upper[ran])
    if num.lower() == 'y':
        for i in range(num_length):
            sprinkler = random.randint(0, 9)
            generated.append(str(sprinkler))
    random.shuffle(generated)
    return generated


def clear():
    conf = input('Are you sure you want to delete the saved passwords [Y/N]: ')
    if conf.lower() == 'y':
        aval = getpass.getpass('Enter the Token again: ')
        if aval==validation_token:
            try:
                os.remove(f'C://Users//{user}//Documents//pgph.txt')
                print('All saved passwords have been removed from the machine.')
            except FileNotFoundError:
                print('All saved passwords have been removed already or there are no passwords saved.')
        else:
            print('Admin validation failed !')
    mainmenu()


def uninstall():
    conf = input('Are you sure you want to delete the current admin account [Y/N]: ')
    if conf.lower() == 'y':
        val = getpass.getpass('Enter the Key: ')
        if val==validation_token:
            os.remove(f'C://Users//{user}//Documents//validation_of_user.txt')
            print('Your admin account has been deleted.')


def greeting():
    print('******************************************')
    print('       WELCOME TO PASSWORD MANAGER')
    print('******************************************')
    mainmenu()

def deletion():
    print('''
********************************************************************************************************************
*If you want to delete the Password Manager tool so as to negate the possibility of data recovery:                 *
*1. Kindly delete all the saved passwords using this tool.                                                         *
*2. The process of saved password deletion should be followed by admin account deletion from within this tool.     *
*3. After the successful execution of the above commands, the tool is now safe to be moved to the recycle bin along *
*   with the dependent files as it does not hold information of any of your credentials.                           *
********************************************************************************************************************
''')
    mainmenu()
    
validation()