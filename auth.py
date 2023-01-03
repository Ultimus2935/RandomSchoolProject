import sqlite3 as sql
import os
import json

from hasher import Hash

usaltdb = sql.connect("data/usalt.db")
uhashdb = sql.connect("data/uhash.db")

def login():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    uid = input("Username: ")
    if (uid,) in uhashdb.execute("SELECT uid FROM uhash").fetchall() and (uid, ) in usaltdb.execute("SELECT uid FROM usalt").fetchall():
        passw_hash = uhashdb.execute(f"SELECT passw_hash FROM uhash WHERE uid = '{uid}'").fetchall()[0][0]
        passw_salt = usaltdb.execute(f"SELECT passw_salt FROM usalt WHERE uid = '{uid}'").fetchall()[0][0]

        while True:
            passw = input("Password: ")
            if Hash(passw, passw_salt) == passw_hash:
                os.system('cls' if os.name == 'nt' else 'clear')

                with open("data/sys_var.json") as sys_var_file:
                    sys_var = json.load(sys_var_file)

                    sys_var["session_var"]["uid"] = uid
                    sys_var["session_var"]["login_status"] = True
                    with open("data/sys_var.json", "w") as sys_var_file: json.dump(sys_var, sys_var_file, indent=4)

                print("Login successful.")
                break
            
            elif passw.lower() == "$~exit": break
            else: print("Wrong password!\n")

    else:
        print("User not found\nWould you like to create a new user account?")
        if input("[press RETURN to continue, type $~exit to cancel]\n").lower() == "$~exit": pass
        else: create_user()

def create_user():
    os.system('cls' if os.name == 'nt' else 'clear')

    uid = input("Enter new username: ")
    passw_hash, passw_salt = Hash(input("Enter new password: "))

    if Hash(input("Re-enter new password: "), passw_salt) == passw_hash:
        usaltdb.execute(f"""
            INSERT INTO usalt VALUES ("{uid}", "{passw_salt}")
        """)

        uhashdb.execute(f"""
            INSERT INTO uhash VALUES ("{uid}", "{passw_hash}")
            """)

        usaltdb.commit()
        uhashdb.commit()
    
    else: print("Re-entered new Password is incorrect.")
    
    print("New user created successfully.")
    input("Press RETURN to proceed to login...")
    login()

def change_pass():
    os.system('cls' if os.name == 'nt' else 'clear')

    while True:
        uid = input("Username: ")

        if uid == "$~exit": return
        elif (uid,) in uhashdb.execute("SELECT uid FROM uhash").fetchall() and (uid, ) in usaltdb.execute("SELECT uid FROM usalt").fetchall():
            passw_hash = uhashdb.execute(f"SELECT passw_hash FROM uhash WHERE uid = '{uid}'").fetchall()[0][0]
            passw_salt = usaltdb.execute(f"SELECT passw_salt FROM usalt WHERE uid = '{uid}'").fetchall()[0][0]

            while True:
                if Hash(input("Old Password: "), passw_salt) == passw_hash:
                    new_passw_hash, new_passw_salt = Hash(input("Enter new Password: "))
                    if new_passw_hash == Hash(input("Re-enter new Password: "), new_passw_salt):
                        uhashdb.execute(f"UPDATE uhash SET passw_hash = '{new_passw_hash}' WHERE uid = '{uid}'")
                        usaltdb.execute(f"UPDATE usalt SET passw_salt = '{new_passw_salt}' WHERE uid = '{uid}'")

                        usaltdb.commit()
                        uhashdb.commit()

                        print()
                        break

                    else: print("Re-entered new Password is incorrect.")

                else: print("Old Password is incorrect.")
        
        else: print("Username not found.")

def interface():
    change_pass()
    return
