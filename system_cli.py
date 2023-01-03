import json
import time
import os

import auth, home

os.system('cls' if os.name == 'nt' else 'clear')

with open("data/sys_var.json") as sys_var_file:
    sys_var = json.load(sys_var_file)

    sys_var["session_var"]["uid"] = ""
    sys_var["session_var"]["login_status"] = False
    with open("data/sys_var.json", "w") as sys_var_file: json.dump(sys_var, sys_var_file, indent=4)

print("Boot complete...")
time.sleep(1)

input("Press RETURN to proceed to login...")
time.sleep(0.5)

auth.login()

with open("data/sys_var.json") as sys_var_file:
    sys_var = json.load(sys_var_file)

    if sys_var["session_var"]["login_status"]:
        home.start()