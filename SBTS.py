import csv
import os.path

with open("bugs.csv",'a',newline='') as file:
    field = ['id','Title','Description','Priority','Status','Reported_by']
    if os.path.getsize('bugs.csv') == 0:
        writer = csv.DictWriter(file, fieldnames=field)
        writer.writeheader()

def Report_Bug(login_id):
    print("--- Report Bug ---")
    bug_id = 1
    title = input("Title: ")
    description = input("Description: ")
    priority = int(input("Priority (1-5):"))
    status = "New"
    Assignees = set()
    Comments = []
    Resolution_time = None
    print(f"Status: {status}\n")
    global bug
    bug = {"id": bug_id, "Title": title, "Description": description, "Priority": priority, "Status": status,"Reported_by": login_id}
    Tester(login_id)

def View_my_Bugs(login_id):
    pass

def Add_Comment(login_id):
    while True:
        try:
            id = int(input("Enter your tester id : "))
            if id in bug_ids:
                break
            else:
                print("Tester id not found !")
                pass
        except:
            print("Enter your id again : ")

def Save_Exit(login_id):
    with open("bugs.csv", 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field)
        writer.writerow(bug)
    print("Saved\n")
    ask = input("Role Switch? ")
    if ask == "y":
        Role_Specification()

def Tester(login_id):
    choice = input("Choice: ")
    match choice:
        case '1':
            Report_Bug(login_id)
        case '2':
            View_my_Bugs(login_id)
        case '3':
            Add_Comment(login_id)
        case '4':
            Save_Exit(login_id)

def Claim_Bug():
    pass

def Update_Status():
    pass

def View_Assigned_Bugs():
    pass

def Resolve_Bug():
    pass

def Developer():
    login_id = input("Login as: ")
    print("--- Developer Menu ---")
    print("1. Claim Bug")
    print("2. Update Status")
    print("3. View Assigned Bugs")
    print("4. Resolve Bug")
    print("5. Save & Exit")
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
    login_id = input("Login as: ")
    print("--- Manager Menu ---")
    print("1. View Dashboard")
    print("2. Assign Bug")
    print("3. Generate Report")
    print("4. Search Bugs")
    print("5. Save & Exit")
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
            login_id = input("Login as: ")
            print("--- Tester Menu ---")
            print("1. Report Bug")
            print("2. View My Bugs")
            print("3. Add Comment")
            print("4. Save & Exit")
            Tester(login_id)
        case 'Developer':
            Developer()
        case 'Manager':
            Manager()
        case _:
            print("No Such Role Exist")

print(" === Software Bug Tracking System (SBTS) ===")
Role_Specification()