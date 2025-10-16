import csv
import os.path
import pickle
import random
from datetime import date

def load_users(filename='users.pkl'):
    if os.path.exists(filename) and os.path.getsize(filename) != 0:
        with open(filename,'rb') as f:
            users = pickle.load(f)
        return users
    else:
        users = {'tester1': {'role': 'Tester', 'name': 'Bob Tester', 'assigned_bugs': set()},
                 'dev1': {'role': 'Developer', 'name': 'Alice Dev', 'assigned_bugs': set()},
                 "mgr1": {"role": "Manager", "name": "Ashutosh Manager", "assigned_bugs": set()},
                 'tester2': {'role': 'Tester', 'name': 'Jhon Tester', 'assigned_bugs': set()},
                 'dev2': {'role': 'Developer', 'name': 'Ali Dev', 'assigned_bugs': set()},
                 "mgr2": {"role": "Manager", "name": "Akash Manager", "assigned_bugs": set()}}
        save_users(users)
        return users

def save_users(users):
    with open('users.pkl','wb') as f:
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
    print("\n--- Report Bug ---")
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
    users = load_users()
    found = False
    print("\n+", '-' * 5, '+', '-' * 22, '+', '-' * 10, '+', '-' * 13, '+', '-' * 13, '+', '-' * 11,'+',sep='')
    print(f"| {'Id':^3} | {'Title':^20} | {'Priority':^8} | {'Status':^11} | {'Reported_by':^11} | {'Assignees':^9} |")
    print("+",'-'*5,'+','-'*22,'+','-'*10,'+','-'*13,'+','-'*13,'+','-'*11,'+',sep='')
    for bug_id,bug_data in bugs_data.items():
        if bug_data['Reported_by'] == tester_login_id:
            found = True
            assign = set()
            assigning = False
            for user_id,user_data in users.items():
                if user_data['role'] == 'Developer' and bug_id in  user_data['assigned_bugs']:
                    assign.add(user_id)
                    assigning = True
            if not assigning:
                assign = ','.join(bug_data['Assignees']) if bug_data['Assignees'] else '-'
            else:
                assign = str(assign)
            print(f"| {bug_id:^3} | {bug_data['Title']:^20} | {bug_data['Priority']:^8} | {bug_data['Status']:^11} | {bug_data['Reported_by']:^11} | {assign[1:-1]:^9} |")
            print("+",'-'*5,'+','-'*22,'+','-'*10,'+','-'*13,'+','-'*13,'+','-'*11,'+',sep='')
    if not found:
        print("No bugs Reported yet!")
    Tester()

def Add_Comment():
    global bugs_data
    bugs_data = load_bugs()
    id = input("\nEnter your bug id : ")
    if id.isdigit():
        id = int(id)
        if id in bugs_data and bugs_data[id]['Reported_by'] == tester_login_id:
            Comments = input("Enter Your comment: ")
            bugs_data[id]['Comments'].append((tester_login_id,Comments))
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
        id = input("\nBug ID: ")
        try:
            id = int(id)
            break
        except ValueError:
            print("Please Enter Valid id!")
    return id

def data_re_write(bugs_data):
    with open('bugs.csv','w',newline='') as files:
        writer = csv.DictWriter(files, fieldnames=field)
        writer.writeheader()
        for bug_id,bug_data in bugs_data.items():
            writer.writerow({"id": bug_id, "Title": bug_data['Title'], "Description": bug_data['Description'], "Priority": bug_data['Priority'], "Status": bug_data['Status'],"Reported_by": bug_data['Reported_by']})

def Claim_Bug():
    global bugs_data,users
    users = load_users()
    bugs_data = load_bugs()
    id = check_id()
    found = False
    for bug_id,bug_data in bugs_data.items():
        if bug_id == int(id):
            found = True
            bug_data['Status'] = 'Assigned'
            users[developer_login_id]['assigned_bugs'].add(bug_id)
            bug_data['Assignees'] = {developer_login_id}
            data_re_write(bugs_data)
            save_users(users)
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
            data_re_write(bugs_data)
            print("Updated! Comment added.")
            break
    if not found:
        print("No such bugs Exist!")
    Developer()

def View_Assigned_Bugs():
    global bugs_data,developer_login_id
    bugs_data = load_bugs()
    users = load_users()
    found = False
    print("\n+", '-' * 5, '+', '-' * 22, '+', '-' * 10, '+', '-' * 13, '+', sep='')
    print(f"| {'Id':^3} | {'Title':^20} | {'Priority':^8} | {'Status':^11} |")
    print("+", '-' * 5, '+', '-' * 22, '+', '-' * 10, '+', '-' * 13, '+', sep='')
    for bug_id, bug_data in bugs_data.items():
        if bug_id in users[developer_login_id]['assigned_bugs']:
            found = True
            print(f"| {bug_id:^3} | {bug_data['Title']:^20} | {bug_data['Priority']:^8} | {bug_data['Status']:^11} |")
            print("+", '-' * 5, '+', '-' * 22, '+', '-' * 10, '+', '-' * 13, '+', sep='')
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
            time = int(input("Days to Resolve: "))
            bug_data['Resolution_time'] = time
            bug_data['Status'] = 'Resolved'
            print(f"Resolution time set: {time} days.")
            break
    data_re_write(bugs_data)
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
    print("\n--- Dashboard ---")
    global bugs_data
    bugs_data = load_bugs()
    open_count = re_count = re_time = 0
    priority = {}
    for bug_id,bug_data in bugs_data.items():
        if bug_data['Status'] == 'Resolved':
            re_count += 1
            if type(bug_data['Resolution_time']) == int:
                re_time += bug_data['Resolution_time']
        else:
            open_count += 1
        priority[bug_id] = int(bug_data['Priority'])
    try:
        avg_re_time = re_time/re_count
    except:
        avg_re_time = 0
    users = load_users()
    bugs_per_dev = {}
    for user_id,user_data in users.items():
        if user_data['role'] == 'Developer':
            count = len(user_data['assigned_bugs'])
            bugs_per_dev[user_id] = count
    print(f"Total Bugs: {len(bugs_data)}")
    print(f"Open Bugs: {open_count}")
    print(f"Resolved: {re_count} Avg Resolution Time: {avg_re_time} days")
    print(f"Priority Distribution: {str(priority)[1:-1]}")
    print(f"Bugs per Developer: {str(bugs_per_dev)[1:-1]}")
    Manager()

def Assign_Bug():
    global bugs_data,users
    bugs_data = load_bugs()
    users = load_users()
    id = check_id()
    found = False
    for bug_id, bug_data in bugs_data.items():
        if bug_id == int(id):
            found = True
            while True:
                assign = input("Assign Bug to: ")
                if assign in users and users[assign]['role']=='Developer':
                    bug_data['Assignees'].add(assign)
                    bug_data['Status'] = 'Assigned'
                    users[assign]['assigned_bugs'].add(bug_id)
                    data_re_write(bugs_data)
                    save_users(users)
                    print(f"Bug {bug_id} Assigned Successfully!")
                    break
                else:
                    print("No Such user Exist to assign Bugs! \nEnter Correct User id")
            break
    if not found:
        print("No such bugs Exist!")
    Manager()

def Preparing_Report():
    bugs_data = load_bugs()
    users = load_users()
    field = ['Bug_id','Title','Description','Priority','Status','Reported_by','Reporter_name','Assignees','Assignees_name','Comments','Resolution_time']
    filename = 'report_' + str(date.today()) + '.csv'
    with open(filename,'w',newline='') as file:
        writer = csv.DictWriter(file,fieldnames=field)
        writer.writeheader()
    for bug_id, bug_data in bugs_data.items():
        report = {'Bug_id': bug_id, 'Title': bug_data['Title'], 'Description': bug_data['Description'],'Priority': bug_data['Priority'], 'Status': bug_data['Status'],
                          'Reported_by': bug_data['Reported_by'],'Reporter_name': None, 'Assignees': list(), 'Assignees_name': list(), 'Comments': bug_data['Comments'],
                          'Resolution_time': bug_data['Resolution_time']}
        for user_id, user_data in users.items():
            if user_id == bug_data['Reported_by']:
                report['Reporter_name'] = user_data['name']
            if user_data['role'] == 'Developer':
                report['Assignees'].append(user_id)
                report['Assignees_name'].append(user_data['name'])
        if not report['Assignees']:
            report['Assignees'] = "-"
        with open(filename,'a',newline='') as file:
            writer = csv.DictWriter(file,fieldnames=field)
            writer.writerow(report)
    return filename

def Generate_Report():
    filename = Preparing_Report()
    with open(filename,'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(f"\n---- Report of Bug id-{row['Bug_id']} ----")
            print(f"Title: {row['Title']}")
            print(f"Description: {row['Description']}")
            print(f"Priority: {row['Priority']}     Status: {row['Status']}")
            print(f"Reported By: {row['Reported_by']}          Reporter Name: {row['Reporter_name']}")
            print(f"Assignees: {row['Assignees']}         Assignees Names: {row['Assignees_name']}")
            print(f"Comments: {row['Comments']}          Resolution Time: {row['Resolution_time']}")
    Manager()

def Searching_by_Status(stat):
    if stat == 'Open':
        stat = 'New'
    print("+", '-' * 5, '+', '-' * 22, '+', '-' * 10, '+', '-' * 13, '+', '-' * 13, '+', sep='')
    print(f"| {'Id':^3} | {'Title':^20} | {'Priority':^8} | {'Status':^11} | {'Reported_by':^11} |")
    print("+", '-' * 5, '+', '-' * 22, '+', '-' * 10, '+', '-' * 13, '+', '-' * 13, '+', sep='')
    found = False
    for bug_id, bug_data in bugs_data.items():
        if bug_data['Status'] == stat:
            found = True
            print(f"| {bug_id:^3} | {bug_data['Title']:^20} | {bug_data['Priority']:^8} | {bug_data['Status']:^11} | {bug_data['Reported_by']:^11} |")
            print("+", '-' * 5, '+', '-' * 22, '+', '-' * 10, '+', '-' * 13, '+', '-' * 13, '+', sep='')
    if not found:
        print(f"No bugs {stat}!")

def Search_Bugs():
    global bugs_data,users
    bugs_data = load_bugs()
    users = load_users()
    print("\nSearch by: 1) Status 2) Priority 3) Assignee")
    choice = input("Choice: ")
    match choice:
        case '1':
            while True:
                stat = input("Status: ").title()
                if stat in ['Open','Assigned','In Progress','Resolved']:
                    Searching_by_Status(stat)
                    break
                else:
                    print("Invalid Status! Enter Apropriate Status...\n")

        case '2':
            while True:
                pri = input("Priority: ")
                if pri in '12345':
                    found = False
                    print("+", '-' * 5, '+', '-' * 22, '+', '-' * 10, '+', '-' * 13, '+', '-' * 13, '+', sep='')
                    print(f"| {'Id':^3} | {'Title':^20} | {'Priority':^8} | {'Status':^11} | {'Reported_by':^11} |")
                    print("+", '-' * 5, '+', '-' * 22, '+', '-' * 10, '+', '-' * 13, '+', '-' * 13, '+', sep='')
                    for bug_id,bug_data in bugs_data.items():
                        if bug_data['Priority'] == pri:
                            found = True
                            print(f"| {bug_id:^3} | {bug_data['Title']:^20} | {bug_data['Priority']:^8} | {bug_data['Status']:^11} | {bug_data['Reported_by']:^11} |")
                            print("+", '-' * 5, '+', '-' * 22, '+', '-' * 10, '+', '-' * 13, '+', '-' * 13, '+', sep='')
                    if not found:
                        print(f"No bugs Present having Priority {pri}")
                    break
                else:
                    print("Invalid Priority! Please enter correct Priority...\n")

        case '3':
            while True:
                assign = input("Assignee: ")
                if assign in users and users[assign]['role']=='Developer':
                    found = False
                    print("+", '-' * 5, '+', '-' * 22, '+', '-' * 10, '+', '-' * 13, '+', '-' * 13, '+', sep='')
                    print(f"| {'Id':^3} | {'Title':^20} | {'Priority':^8} | {'Status':^11} | {'Reported_by':^11} |")
                    print("+", '-' * 5, '+', '-' * 22, '+', '-' * 10, '+', '-' * 13, '+', '-' * 13, '+', sep='')
                    for bug_id, bug_data in bugs_data.items():
                        if bug_id in users[assign]['assigned_bugs']:
                            found = True
                            print(f"| {bug_id:^3} | {bug_data['Title']:^20} | {bug_data['Priority']:^8} | {bug_data['Status']:^11} | {bug_data['Reported_by']:^11} |")
                            print("+", '-' * 5, '+', '-' * 22, '+', '-' * 10, '+', '-' * 13, '+', '-' * 13, '+', sep='')
                    if not found:
                        print(f"No bugs are Assigned to {assign}.")
                    break
                else:
                    print("Invalid Assignee! Enter Correct Assignee\n")

        case _:
            print("Invalid Choice! Moving back to Menu...")
    Manager()

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