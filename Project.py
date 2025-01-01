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
cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        admin_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(30) NOT NULL,
        password VARCHAR(30) NOT NULL
    )
""")


def center_text(text):
    print(f"\n{text:^80}\n")

def divider():
    print("=" * 110)

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

# Register

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

# Login

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

# User Panel

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

# Encrytion

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

# Decryption

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

# check or create admin

def check_or_create_admin():
    cursor.execute("SELECT COUNT(*) FROM admin")
    data = cursor.fetchone()
    if data[0] > 0:
        admin_login()
    else:
        center_text("No admin account found. Creating default admin...")
        default_admin_username = "darkie"
        default_admin_password = encode("idkpass")
        cursor.execute("INSERT INTO admin (username, password) VALUES ('{}', '{}')".format(default_admin_username, default_admin_password))
        mycon.commit()
        center_text("Default Admin Account created successfully!")
        admin_login()

# Admin Login
def admin_login():
    divider()
    center_text("ADMIN LOGIN")
    divider() 
    cursor.execute("SELECT username, password FROM admin")
    data = cursor.fetchall()
    for i in data:
        print(i[0], decode(i[1]), sep=":")
    admin_username = input("Admin Username: ".ljust(30))
    admin_password = input("Admin Password: ".ljust(30))
    for i in data:
        if admin_username == i[0] and admin_password == decode(i[1]):  
            center_text("Admin Login Successful!")
            admin_panel()
        else:
            center_text("Invalid Username or password!")
            admin_login()

# Admin Panel
def admin_panel():
    while True:
        divider()
        center_text("ADMIN PANEL")
        divider()
        print("1. View All Users".ljust(30))
        print("2. View User-Specific Data".ljust(30))
        print("3. Delete a User".ljust(30))
        print("4. Modify Website Data".ljust(30))
        print("5. Logout".ljust(30))
        print("6. Add New Admin".ljust(30))
        divider()

        choice = input("Enter your choice: ".ljust(30))

        if choice == "1":
            cursor.execute("SELECT * FROM MASTER")
            users = cursor.fetchall()
            divider()
            center_text("ALL USERS")
            divider()
            print("UID".ljust(10), "Name".ljust(20), "Email".ljust(30), "Phone".ljust(15), "Username".ljust(20), sep=" | ")
            divider()
            for user in users:
                print(str(user[0]).ljust(10), user[1].ljust(20), user[2].ljust(30), str(user[3]).ljust(15), user[4].ljust(20), sep=" | ")
            divider()

        elif choice == "2":
            uid = input("Enter User ID: ".ljust(30))
            cursor.execute("SELECT Website, Email, password FROM user WHERE UID = {}".format(uid))
            data = cursor.fetchall()
            if data:
                divider()
                center_text(f"Data for User ID {uid}")
                divider()
                print("Website".ljust(20), "Email".ljust(30), "Password".ljust(20), sep=" | ")
                divider()
                for website, email, pwd in data:
                    print(website.ljust(20), email.ljust(30), decode(pwd).ljust(20), sep=" | ")
                divider()
            else:
                center_text("No data found for the given User ID!")

        elif choice == "3":
            uid = input("Enter User ID to delete: ".ljust(30))
            cursor.execute("DELETE FROM master WHERE UID = {}".format(uid))
            cursor.execute("DELETE FROM user WHERE UID = {}".format(uid))
            mycon.commit()
            center_text(f"User ID {uid} and their data deleted successfully!")

        elif choice == "4":
            uid = input("Enter User ID: ".ljust(30))
            web = input("Enter Website name to modify: ".ljust(30))
            cursor.execute("SELECT * FROM user WHERE UID = {} AND Website = '{}'".format(uid, web))
            data = cursor.fetchone()
            if data:
                field = input("Modify (1. Email, 2. Password): ".ljust(30))
                if field == "1":
                    new_email = input("Enter new Email: ".ljust(30))
                    cursor.execute("UPDATE user SET Email = '{}' WHERE UID = {} AND Website = '{}'".format(new_email, uid, web))
                elif field == "2":
                    new_pwd = encode(input("Enter new Password: ".ljust(30)))
                    cursor.execute("UPDATE user SET password = '{}' WHERE UID = {} AND Website = '{}'".format(new_pwd, uid, web))
                mycon.commit()
                center_text("Website data updated successfully!")
            else:
                center_text("No such website found for the given User ID!")

        elif choice == "5":
            center_text("Admin Logged Out!")
            main()
            return
        elif choice == "6":
            admin_username = input("New Admin Username: ".ljust(30))
            admin_password = encode(input("New Admin Password: ".ljust(30)))
            cursor.execute("INSERT INTO admin (username, password) VALUES ('{}', '{}')".format(admin_username, admin_password))
            mycon.commit()
            center_text("New Admin Account Added Successfully!")
            admin_panel()
            divider()
        else:
            print("\nInvalid choice entered!\n")
            admin_panel()

# HomePage

def main():
    while True:
        divider()
        center_text("HOMEPAGE")
        divider()
        print("1. Login".ljust(30))
        print("2. Register".ljust(30))
        print("3. Admin Login".ljust(30))
        print("9. Exit".ljust(30))
        divider()
        choice = input("Enter your choice: ".ljust(30))
        if choice == "1":
            login()
        elif choice == "2":
            register()
        elif choice == "3":
            print("\nNaa naa naa!!! You r not admin ;)\n".ljust(30))
            main()
        elif choice == "404":
            check_or_create_admin()
        elif choice == "9":
            print()
            msg = 'Thanks for using the software'
            for i in msg:  
                print(i,end='',flush=True)
                time.sleep(0.05)
            input("\n\nPress ENTER to exit.".ljust(30))
            break
        else:
            print("\nInvalid choice Entered!\n".ljust(30))
            main()
main()
