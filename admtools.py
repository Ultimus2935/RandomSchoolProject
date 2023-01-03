import sqlite3 as sql
import os
import json

from hasher import Hash

def change_root_pass():
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        passw = input("Enter root password: ")

        with open("data/sys_var.json") as sys_var_file:
            sys_var = json.load(sys_var_file)
            passw_hash = sys_var["root_hash"]
            passw_salt = sys_var["root_salt"]

        if Hash(passw, passw_salt) == passw_hash:
            with open("data/sys_var.json") as sys_var_file:
                sys_var = json.load(sys_var_file)

                sys_var["root_hash"], sys_var["root_salt"] = Hash(input("Enter new root password: "))
                with open("data/sys_var.json", "w") as sys_var_file: json.dump(sys_var, sys_var_file, indent=4)

            print("Root password updated successfully.")    
            break
        
        elif passw.lower() == "$~exit": break
        else: print("Wrong root password!\n")

def init_auth_db():
    os.system('cls' if os.name == 'nt' else 'clear')

    print("## THIS ACTION WILL ERASE AND RECREATE USER CREDENTIAL DATABASES ##")
    print("## ARE YOU SURE YOU WANT TO CONTINUE? ##")
    if input("[press RETURN to continue, type $~exit to cancel]\n").lower() == "$~exit": pass
    
    else: 
        while True:
            passw = input("Enter root password: ")

            with open("data/sys_var.json") as sys_var_file:
                sys_var = json.load(sys_var_file)
                passw_hash = sys_var["root_hash"]
                passw_salt = sys_var["root_salt"]

            if Hash(passw, passw_salt) == passw_hash:
                os.system('cls' if os.name == 'nt' else 'clear')

                usaltdb = sql.connect("data/usalt.db")
                uhashdb = sql.connect("data/uhash.db")

                usaltdb.execute("DROP TABLE usalt")
                uhashdb.execute("DROP TABLE uhash")

                usaltdb.execute("""
                    CREATE TABLE usalt (
                        uid varchar(16) primary key,
                        passw_salt varchar(32) not null
                    )
                """)

                uhashdb.execute("""
                    CREATE TABLE uhash (
                        uid varchar(16) primary key,
                        passw_hash varchar(255) not null
                    )
                """)

                usaltdb.commit()
                uhashdb.commit()

                print("## DATABASES SUCCESSFULLY CREATED ##")
                
                quit()
            
            elif passw.lower() == "$~exit": break
            else: print("Wrong root password!\n")

def view_auth_db():
    os.system('cls' if os.name == 'nt' else 'clear')

    while True:
        passw = input("Enter root password: ")

        with open("data/sys_var.json") as sys_var_file:
            sys_var = json.load(sys_var_file)
            passw_hash = sys_var["root_hash"]
            passw_salt = sys_var["root_salt"]

        if Hash(passw, passw_salt) == passw_hash:
            os.system('cls' if os.name == 'nt' else 'clear')

            usaltdb = sql.connect("data/usalt.db")
            uhashdb = sql.connect("data/uhash.db")

            print("User Hash DB:\n", uhashdb.execute("SELECT * FROM uhash").fetchall())
            print()
            print("User Salt DB:\n", usaltdb.execute("SELECT * FROM usalt").fetchall())

            input("\n[press RETURN to continue]")
            break
        
        elif passw.lower() == "$~exit": break
        else: print("Wrong root password!\n")

def interface():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        funcNames = ["Return to Menu", "Initialise Auth Database","View Auth Database" , "Change Root Password"]
        funcPaths = ["", "init_auth_db","view_auth_db" , "change_root_pass"]

        print("Select App: ")
        for funcName in funcNames:
            print(f"{funcNames.index(funcName)}. {funcName}")

        index = int(input("Select function to run: "))

        if index == 0: return
        elif type(index) == int and index < len(funcNames): globals()[funcPaths[index]](); break
        else: continue
    