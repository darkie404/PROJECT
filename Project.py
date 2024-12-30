import mysql.connector as sqltor
import time, random

mycon = sqltor.connect(host="localhost", user="root", password="root", charset="utf8")
cursor = mycon.cursor()

# Database and table setup
cursor.execute("CREATE DATABASE IF NOT EXISTS Profile")
cursor.execute("USE Profile")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS master (
        UID INT,
        name VARCHAR(60),
        Email VARCHAR(60),
        Ph_no BIGINT,
        username VARCHAR(30),
        passwd VARCHAR(30)
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
        UID INT,
        Website VARCHAR(60),
        Email VARCHAR(80),
        password VARCHAR(30)
    )
""")

def center_text(text):
    print(f"\n{text:^80}\n")

def divider():
    print("=" * 80)

def user_list():
    cursor.execute("SELECT username FROM MASTER")
    data = cursor.fetchall()
    return data

def chkMID():
    cursor.execute("SELECT MAX(UID) FROM MASTER")
    fetchedUID = cursor.fetchone()
    cm_uid = fetchedUID[0]  
    if cm_uid is None:
        cm_uid = 0
    next_uid = cm_uid + 1
    return next_uid

def register():
    divider()
    center_text("REGISTRATION")
    divider()
    app_name = input("Name: ".ljust(30))
    app_phone = input("Phone No. (10 digits): ".ljust(30))
    while len(app_phone) != 10 or not app_phone.isdigit():
        app_phone = input("Invalid Phone Number! Please enter a valid 10-digit number: ".ljust(30))

    app_email = input("Email: ".ljust(30))
    while '@' not in app_email or '.' not in app_email:
        app_email = input("Invalid Email! Please enter a valid email: ".ljust(30))

    app_username = input("Username: ".ljust(30))
    existing_users = [user[0] for user in user_list()]
    while app_username in existing_users:
        app_username = input("Username already exists! Enter another username: ".ljust(30))

    app_password = input("Password (min 8 characters): ".ljust(30))
    while len(app_password) < 8:
        app_password = input("Password too short! Enter a password with at least 8 characters: ".ljust(30))
    enc_app_password =  encode(app_password)
    UID = chkMID()
    cursor.execute(
        "INSERT INTO master VALUES ({}, '{}', '{}', {}, '{}', '{}')".format(
            UID, app_name, app_email, app_phone, app_username, enc_app_password
        )
    )
    mycon.commit()
    center_text("Registration successful!")

def login():
    divider()
    center_text("LOGIN")
    divider()
    global lgn_username
    cursor.execute("SELECT username, passwd FROM MASTER")
    data = cursor.fetchall()
    for i in data:
        print(i[0], decode(i[1]), sep=":")
    lgn_username = input("Username: ".ljust(30))
    lgn_password = input("Password: ".ljust(30))

    cursor.execute("SELECT username, passwd FROM MASTER")
    data = cursor.fetchall()
    for i in data:
        if lgn_username == i[0] and lgn_password == decode(i[1]):
            center_text("Login Success!")
            usr_panel()
            return

    center_text("Incorrect Username or Password!")
    login()

def webdata(uid):
    cursor.execute("SELECT Website FROM user WHERE UID = {}".format(uid))
    data = cursor.fetchall()
    return data

def usr_panel():
    divider()
    center_text("DASHBOARD")
    divider()
    cursor.execute("SELECT UID FROM MASTER WHERE username = '{}'".format(lgn_username))
    uid= cursor.fetchone()
    uid = uid[0]

    while True:
        divider()
        print("1. Add new Data".ljust(30))
        print("2. View all Website Data".ljust(30))
        print("3. Modify Website Data".ljust(30))
        print("4. Delete Website Data".ljust(30))
        print("5. Logout".ljust(30))
        print("99. Delete Account".ljust(30))
        divider()

        choice = input("Enter your choice: ".ljust(30))

        if choice == "1":
            web = input("Enter Website: ".ljust(30))
            if (web,) in webdata(uid):
                center_text("Website already exists!")
            else:
                email = input("Enter Email for this website: ".ljust(30))
                pwd = encode(input("Enter Password: ".ljust(30)))
                cursor.execute("INSERT INTO user VALUES ({}, '{}', '{}', '{}')".format(uid, web, email, pwd))
                mycon.commit()
                center_text("Data added successfully!")

        elif choice == "2":
            cursor.execute("SELECT Website, Email, password FROM user WHERE UID = {}".format(uid))
            divider()
            center_text("WEBSITE DATA")
            divider()
            print("Website".ljust(20), "Email".ljust(30), "Password".ljust(20), sep=" | ")
            divider()
            data = cursor.fetchall()
            for website, email, pwd in data:
                print(website.ljust(20), email.ljust(30), decode(pwd).ljust(20), sep=" | ")
            divider()

        elif choice == "3":
            web = input("Enter Website name to modify: ".ljust(30))
            if (web,) in webdata(uid):
                field = input("Modify (1. Email, 2. Password): ".ljust(30))
                if field == "1":
                    new_email = input("Enter new Email: ".ljust(30))
                    cursor.execute("UPDATE user SET Email = '{}' WHERE Website = '{}'".format(new_email, web))
                elif field == "2":
                    new_pwd = encode(input("Enter new Password: ".ljust(30)))
                    cursor.execute("UPDATE user SET password = '{}' WHERE Website = '{}'".format(new_pwd, web))
                mycon.commit()
                center_text("Data updated successfully!")
            else:
                center_text("Website not found!")

        elif choice == "4":
            web = input("Enter Website name to delete: ".ljust(30))
            if (web,) in webdata(uid):
                cursor.execute("DELETE FROM user WHERE Website = '{}'".format(web))
                mycon.commit()
                center_text("Website data deleted successfully!")
            else:
                center_text("Website not found!")

        elif choice == "99":
            pwd = input("Enter your password to confirm account deletion: ".ljust(30))
            cursor.execute("SELECT passwd FROM MASTER WHERE UID = {}".format(uid))
            data = cursor.fetchone()
            if decode(data[0]) == pwd:
                cursor.execute("DELETE FROM master WHERE UID = {}".format(uid))
                cursor.execute("DELETE FROM user WHERE UID = {}".format(uid))
                mycon.commit()
                center_text("Account deleted successfully!")
                main()
                return
            else:
                center_text("Incorrect password!")

        elif choice == "5":
            main()
            return




def encode(message):
	msg = ''
	key = random.randrange(8,58)
	for i in range(len(message)):
	    char_code = ord(message[i])
	    if 33 <= char_code <= 126:
	             if i % 2 == 0:
	             	if char_code + key > 126:
	             	    shifted_code = char_code + key -126 + 33
	             	else :
	             		shifted_code = char_code + key 
	             else :	
	             	if char_code - key < 33:
	             	    shifted_code = 126 - (33 - (char_code - key))  
	             	else:
	             	    shifted_code = char_code - key
	            
	             msg += chr(shifted_code)
	    else:
	    	msg += message[i]
	encrypt_msg = str(chr(ord(str(key//10))-15)+msg+chr(ord(str(key%10))-15)) 
	return encrypt_msg



def decode(message):
	key = int(chr(ord(message[0])+15) + chr(ord(message[-1])+15))
	new_msg = message[1:-1]
	msg = ''
	for i in range(len(new_msg)):
	    char_code = ord(new_msg[i])
	    if 33 <= char_code <= 126:
	        if i % 2 == 0:
	            if char_code - key < 33:
	             	shifted_code = 126 - (33 - (char_code - key))  
	            else:
	                shifted_code = char_code - key
	        else :	
	            if char_code + key > 126:
	                shifted_code = char_code + key -126 + 33
	            else :
	            	shifted_code = char_code + key 
	        msg += chr(shifted_code)
	    else:
	    	msg += new_msg[i]
	    decrypt_msg = msg
	return decrypt_msg

def main():
    while True:
        divider()
        center_text("HOMEPAGE")
        divider()
        print("1. Login".ljust(30))
        print("2. Register".ljust(30))
        print("9. Exit".ljust(30))
        divider()

        choice = input("Enter your choice: ".ljust(30))
        if choice == "1":
            login()
        elif choice == "2":
            register()
        elif choice == "9":
            msg = 'Thanks for using the software'
            for i in msg:  
                print(i,end='',flush=True)
                time.sleep(0.05)             
            input("\nPress any ENTER to exit.")
            break

main()
