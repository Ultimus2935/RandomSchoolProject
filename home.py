import json
import os
import time

def start():
    os.system('cls' if os.name == 'nt' else 'clear')

    menu()

def menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        with open("data/sys_var.json") as sys_var_file:
            sys_var = json.load(sys_var_file)
            uid = sys_var["session_var"]["uid"]

        print(f"User: {uid}\t Datetime: {time.ctime()}\n")
        
        appNames = ["Shut Down", "Admin Tools", "Hash Encryptor","Change Password" , "Snake"]
        appPaths = ["", "admtools", "hasher","auth", "snake"]

        print("Select App: ")
        for appName in appNames:
            print(f"{appNames.index(appName)}. {appName}")

        index = int(input("Select app to open: "))

        if index == 0: 
            os.system('cls' if os.name == 'nt' else 'clear')

            with open("data/sys_var.json") as sys_var_file:
                sys_var = json.load(sys_var_file)

                sys_var["session_var"]["uid"] = ""
                sys_var["session_var"]["login_status"] = False
                with open("data/sys_var.json", "w") as sys_var_file: json.dump(sys_var, sys_var_file, indent=4)

            print("See you next time!\n")
            return

        elif type(index) == int and index < len(appNames): __import__(appPaths[index]).interface(); continue

        else: 
            menu()
            return