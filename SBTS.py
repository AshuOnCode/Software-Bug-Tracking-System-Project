import csv
import os.path
import pickle
import random


def load_users(filename='users.pkl'):
    if os.path.exists(filename) and os.path.getsize(filename) != 0:
        with open(filename,'rb') as f:
            users = pickle.load(f)
        return users
    else:
        users = {'tester1': {'role': 'Tester', 'name': 'Bob Tester', 'assigned_bugs': set()},
                 'dev1': {'role': 'Developer', 'name': 'Alice Dev', 'assigned_bugs': set()},
                 "mgr1": {"role": "Manager", "name": "Charlie Manager", "assigned_bugs": set()}}
        save_users(filename, users)
        return users

def save_users(filename,users):
    with open(filename,'wb') as f:
        pickle.dump(users,f)

bugs_data = {}
def load_bugs(filename='bugs.csv'):
    global bugs_data
    if bugs_data:
        return bugs_data
    try:
        with open(filename,'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                bug_id = int(row['id'])
                bugs_data[bug_id] = {'Title':row['Title'],'Description':row['Description'],'Priority':row['Priority'],'Status':row['Status'],'Reported_by':row['Reported_by'],'Assignees':set(),'Comments':[],'Resolution_time':None}
    except FileNotFoundError:
        print("No Bug data Found!")
    return bugs_data

field = ['id', 'Title', 'Description', 'Priority', 'Status', 'Reported_by']
if not os.path.exists('bugs.csv') or os.path.getsize('bugs.csv') == 0:
    with open("bugs.csv", 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field)
        writer.writeheader()

def bug_id_creation():
    global bugs_data
    bugs_data = load_bugs()
    if not bugs_data:
            bug_id = random.randint(1,100)
            return bug_id
    else:
        bug_id = int(list(bugs_data.keys())[-1]) + 1
        return bug_id

def Report_Bug():
    print("--- Report Bug ---")
    global tester_login_id, bugs_data
    bug_id = bug_id_creation()
    title = input("Title: ")
    description = input("Description: ")
    priority = int(input("Priority (1-5):"))
    status = "New"
    bugs_data[bug_id] = {"Title": title, "Description": description, "Priority": priority, "Status": status,"Reported_by": tester_login_id, "Comments": [tuple()], "Assignees": set(), 'Resolution_time': None}
    with open("bugs.csv", 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field)
        writer.writerow({"id": bug_id, "Title": title, "Description": description, "Priority": priority, "Status": status,"Reported_by": tester_login_id})
    print(f"Bug #{bug_id} reported! Status: {status}\n")
    Tester()

def View_my_Bugs():
    global bugs_data
    bugs_data = load_bugs()
    found = False
    print("+", '-' * 5, '+', '-' * 22, '+', '-' * 10, '+', '-' * 10, '+', '-' * 13, '+', '-' * 11,'+',sep='')
    print(f"| {'Id':^3} | {'Title':^20} | {'Priority':^8} | {'Status':^8} | {'Reported_by':^11} | {'Assignees':^9} |")
    print("+",'-'*5,'+','-'*22,'+','-'*10,'+','-'*10,'+','-'*13,'+','-'*11,'+',sep='')
    for bug_id,bug_data in bugs_data.items():
        if bug_data['Reported_by'] == tester_login_id:
            found = True
            assign = ','.join(bug_data['Assignees']) if bug_data['Assignees'] else '-'
            print(f"| {bug_id:^3} | {bug_data['Title']:^20} | {bug_data['Priority']:^8} | {bug_data['Status']:^8} | {bug_data['Reported_by']:^11} | {assign:^9} |")
            print("+",'-'*5,'+','-'*22,'+','-'*10,'+','-'*10,'+','-'*13,'+','-'*11,'+',sep='')
    if not found:
        print("No bugs Reported yet!")
    Tester()


def Add_Comment():
    global bugs_data
    bugs_data = load_bugs()
    id = input("Enter your bug id : ")
    if id.isdigit():
        id = int(id)
        if id in bugs_data and bugs_data[id]['Reported_by'] == tester_login_id:
            Comments = input("Enter Your comment: ")
            bugs_data[id]['Comments'].append([(tester_login_id,Comments)])
            print("Comment Added Successfully!")
        else:
            print("Bug id not found or you are not the Reporter!")
    else:
        print("Invalid ID!")
    Tester()

def Save_Exit():
    print("Saved\n")
    ask = input("Role Switch? ")
    if ask in "Yy":
        Role_Specification()
    else:
        print("Exiting SBTS")

def Tester():
    while True:
        print("\n--- Tester Menu ---")
        print("1. Report Bug")
        print("2. View My Bugs")
        print("3. Add Comment")
        print("4. Save & Exit")
        choice = input("Choice: ")
        match choice:
            case '1':
                Report_Bug()
                break
            case '2':
                View_my_Bugs()
                break
            case '3':
                Add_Comment()
                break
            case '4':
                Save_Exit()
                break
            case _:
                print("Invalid Choice! Choose Correct option...")

def check_id():
    while True:
        id = input("Bug ID: ")
        try:
            id = int(id)
            break
        except ValueError:
            print("Please Enter Valid id!")
    return id

def Claim_Bug():
    global bugs_data
    bugs_data = load_bugs()
    id = check_id()
    found = False
    for bug_id,bug_data in bugs_data.items():
        if bug_id == int(id):
            found = True
            bug_data['Status'] = 'Assigned'
            bug_data['Assignees'] = {developer_login_id}
            print(f"Claimed! Status: {bug_data['Status']}. Assignees: {bug_data['Assignees']}")
            break
    if not found:
        print("No such bugs Exist!")
    Developer()

def Update_Status():
    global bugs_data
    bugs_data = load_bugs()
    id = check_id()
    found = False
    for bug_id,bug_data in bugs_data.items():
        if bug_id == int(id):
            found = True
            bug_data['Status'] = input("New Status: ")
            print("Updated! Comment added.")
            break
    if not found:
        print("No such bugs Exist!")
    Developer()

def View_Assigned_Bugs():
    global bugs_data,developer_login_id
    bugs_data = load_bugs()
    found = False
    print("+", '-' * 5, '+', '-' * 22, '+', '-' * 10, '+', '-' * 10, '+', sep='')
    print(f"| {'Id':^3} | {'Title':^20} | {'Priority':^8} | {'Status':^8} |")
    print("+", '-' * 5, '+', '-' * 22, '+', '-' * 10, '+', '-' * 10, '+', sep='')
    for bug_id, bug_data in bugs_data.items():
        for assign in bug_data['Assignees']:
            if assign == developer_login_id:
                found = True
                print(f"| {bug_id:^3} | {bug_data['Title']:^20} | {bug_data['Priority']:^8} | {bug_data['Status']:^8} |")
                print("+", '-' * 5, '+', '-' * 22, '+', '-' * 10, '+', '-' * 10, '+', sep='')
                break
    if not found:
        print("No bugs Assigneed yet!")
    Developer()

def Resolve_Bug():
    global bugs_data
    bugs_data = load_bugs()
    id = check_id()
    found = False
    for bug_id,bug_data in bugs_data.items():
        if bug_id == int(id):
            found = True
            time = input("Days to Resolve: ")
            bug_data['Resolution_time'] = time + " days"
            print(f"Resolution time set: {time} days.")
            break
    if not found:
        print("No such bugs Exist!")
    Developer()

def Developer():
    while True:
        print("\n--- Developer Menu ---")
        print("1. Claim Bug")
        print("2. Update Status")
        print("3. View Assigned Bugs")
        print("4. Resolve Bug")
        print("5. Save & Exit")
        choice = input("Choice: ")
        match choice:
            case '1':
                Claim_Bug()
                break
            case '2':
                Update_Status()
                break
            case '3':
                View_Assigned_Bugs()
                break
            case '4':
                Resolve_Bug()
                break
            case '5':
                Save_Exit()
                break
            case _:
                print("Invalid Choice! Choose Correct option...")

def View_Dashboard():
    pass

def Assign_Bug():
    pass

def Generate_Report():
    pass

def Search_Bugs():
    pass

def Manager():
    while True:
        print("\n--- Manager Menu ---")
        print("1. View Dashboard")
        print("2. Assign Bug")
        print("3. Generate Report")
        print("4. Search Bugs")
        print("5. Save & Exit")
        choice = input("Choice: ")
        match choice:
            case '1':
                View_Dashboard()
                break
            case '2':
                Assign_Bug()
                break
            case '3':
                Generate_Report()
                break
            case '4':
                Search_Bugs()
                break
            case '5':
                Save_Exit()
                break
            case _:
                print("Invalid Choice! Choose Correct option...")

def Role_Specification():
    Role = input("Enter Role (Tester/Developer/Manager): ").title()
    match Role:
        case 'Tester':
            global tester_login_id
            users = load_users()
            while True:
                tester_login_id = input("Login as: ")
                if tester_login_id not in users:
                    print("No such user is Present!")
                    continue
                if users[tester_login_id]["role"] != 'Tester':
                    print("No such Id is for Tester!")
                    ask = input("Role Switch? ")
                    if ask in "Yy":
                        return Role_Specification()
                    else:
                        continue
                else:
                    Tester()
                    break

        case 'Developer':
            global developer_login_id
            users = load_users()
            while True:
                developer_login_id = input("Login as: ")
                if developer_login_id not in users:
                    print("No such user is Present!")
                    continue
                if users[developer_login_id]["role"] != 'Developer':
                    print("No such Id is for Developer!")
                    ask = input("Role Switch? ")
                    if ask in "Yy":
                        return Role_Specification()
                    else:
                        continue
                else:
                    Developer()
                    break

        case 'Manager':
            global manager_login_id
            users = load_users()
            while True:
                manager_login_id = input("Login as: ")
                if manager_login_id not in users:
                    print("No such user is Present!")
                    continue
                if users[manager_login_id]["role"] != 'Manager':
                    print("No such Id is for Manager!")
                    ask = input("Role Switch? ")
                    if ask in "Yy":
                        return Role_Specification()
                    else:
                        continue
                else:
                    Manager()
                    break

        case _:
            print("No Such Role Exist")
            print("Exiting SBTS")

print("=== Software Bug Tracking System ===")
Role_Specification()