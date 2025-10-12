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
    bug_id = bug_id_creation()     # will change this later and made autogenerate id using random module.
    title = input("Title: ")
    description = input("Description: ")
    priority = int(input("Priority (1-5):"))
    status = "New"
    print(f"Status: {status}\n")
    bugs_data[bug_id] = {"Title": title, "Description": description, "Priority": priority, "Status": status,"Reported_by": tester_login_id, "Comments": [tuple()], "Assignees": set(), 'Resolution_time': None}
    with open("bugs.csv", 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field)
        writer.writerow({"id": bug_id, "Title": title, "Description": description, "Priority": priority, "Status": status,"Reported_by": tester_login_id})
    print("Bug Reported Successfully!")
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

def Claim_Bug():
    pass

def Update_Status():
    pass

def View_Assigned_Bugs():
    pass

def Resolve_Bug():
    pass

def Developer():
    choice = input("Choice: ")
    match choice:
        case '1':
            Claim_Bug()
        case '2':
            Update_Status()
        case '3':
            View_Assigned_Bugs()
        case '4':
            Resolve_Bug()
        case '5':
            pass

def View_Dashboard():
    pass

def Assign_Bug():
    pass

def Generate_Report():
    pass

def Search_Bugs():
    pass

def Manager():
    choice = input("Choice: ")
    match choice:
        case '1':
            View_Dashboard()
        case '2':
            Assign_Bug()
        case '3':
            Generate_Report()
        case '4':
            Search_Bugs()
        case '5':
            pass

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
            developer_login_id = input("Login as: ")
            print("--- Developer Menu ---")
            print("1. Claim Bug")
            print("2. Update Status")
            print("3. View Assigned Bugs")
            print("4. Resolve Bug")
            print("5. Save & Exit")
            Developer()
        case 'Manager':
            global manager_login_id
            manager_login_id = input("Login as: ")
            print("--- Manager Menu ---")
            print("1. View Dashboard")
            print("2. Assign Bug")
            print("3. Generate Report")
            print("4. Search Bugs")
            print("5. Save & Exit")
            Manager()
        case _:
            print("No Such Role Exist")

print("=== Software Bug Tracking System ===")
Role_Specification()