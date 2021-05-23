# Password-Manager

**Functionalities**: The tool saves passwords locally on the machine disk in hashed format, the hashing algorithm being custom generated. The tool has the provisions regarding association of passwords with an account or username or both. The tool also contains an administrator account configuration mechanism to enhance security and integrity of the passwords. The tool provides for encryption and decryption of messages using custom algorithms. The key feature of the encryption algorithms which I have designed is that if any string S gets encrypted as S' (S->S') at time T=0, then the same encryption when performed at time T>0 would encrypt S as (S->S''). Now even though the cipher text is different for the same string, the decryption of both the strings would lead to S i.e (S'->S) and (S''->S).


**Setting up**: For configuration of this tool, you would firstly need to run the admin configuration executable (_AdminConfig.py_) followed by entering an admin password so as to ensure that your passwords are accessed only by you . After configuring the password (token/key), kindly proceed to run the _PasswordManager.py_. The admin account deletion procedure has been made available to the user in the Password Manager Tool if needed. For an admin account password change, kindly run the AdminConfig.exe and choose the option for password change.
