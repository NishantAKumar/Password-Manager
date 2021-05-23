import getpass
import hashlib
user = getpass.getuser()
print('''This is an Administrator Configuration Window.''')
def mainmenu():
    try:
        user_type = int(input('''1. New User
2. Change the Admin password\n'''))
        if user_type == 1:
            newuser()
        elif user_type == 2:
            PassChange()
    except KeyboardInterrupt:
        print("Exiting")

def newuser():
    check = 0
    try:
        a = open(f'C:\\Users\\{user}\\Documents\\validation_of_user.txt', 'r')
        check = 1
        if check==1:
            print('ERROR')
            a.close()
        mainmenu()
    except FileNotFoundError:
        
        key = getpass.getpass('Enter a Key(YOU WILL HAVE TO REMEMBER THIS KEY): ')
        confirmation = getpass.getpass('Confirm the Key: ')
        if key==confirmation:
            b = open(f'C:\\Users\\{user}\\Documents\\validation_of_user.txt', 'w')
            b.write((hashlib.sha512(key.encode())).hexdigest())
            b.close()
            print('Administrator password configured successfully.')
        else:
            print('The two passwords do not match.')
        mainmenu()


def PassChange():
    try:
        file = open(f'C:\\Users\\{user}\\Documents\\validation_of_user.txt', 'r')
        pre_hash = file.readlines()
        old = getpass.getpass("Enter previous Key: ")
        old_hash =hashlib.sha512(old.encode()).hexdigest()
        if pre_hash[0]==old_hash:
            key = input('Enter New Key (YOU WILL HAVE TO REMEMBER THIS KEY): ')
            confirmation = input('Confirm the Key: ')
            if key==confirmation:
                b = open(f'C:\\Users\\{user}\\Documents\\validation_of_user.txt', 'w')
                b.write((hashlib.sha512(key.encode())).hexdigest())
                b.close()
                print('Administrator password re-configured successfully.')
            else:
                print('The two passwords do not match.')
        else:
            print('Old password entered is incorrect.')
        mainmenu()
        
    except FileNotFoundError:
        print('You have not configured the password. Please configure as a new user')
        mainmenu()


mainmenu()
            
