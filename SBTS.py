import csv
import os.path

with open("bugs.csv",'a',newline='') as file:
    field = ['id','Title','Description','Priority','Status','Reported_by']
    if os.path.getsize('bugs.csv') == 0:
        writer = csv.DictWriter(file, fieldnames=field)
        writer.writeheader()

with open('add_info.csv','a',newline='') as file:
    field1 = ['id','Comments','Assignees','Resolution_time']
    if os.path.getsize('add_info.csv') == 0:
        writer = csv.DictWriter(file, fieldnames=field1)
        writer.writeheader()

bug = {}
def Report_Bug():
    print("--- Report Bug ---")
    bug_id = 1      # will change this later and made autogenerate id using random module.
    title = input("Title: ")
    description = input("Description: ")
    priority = int(input("Priority (1-5):"))
    status = "New"
    print(f"Status: {status}\n")
    global bug
    bug = {"id": bug_id, "Title": title, "Description": description, "Priority": priority, "Status": status,"Reported_by": tester_login_id}
    Tester()

def View_my_Bugs():
    with open('bugs.csv','r',newline='') as file:
        reader = csv.DictReader(file)
        print("+", '-' * 5, '+', '-' * 20, '+', '-' * 9, '+', '-' * 8, '+', '-' * 13, '+', '-' * 12,'+',sep='')
        print(f"| {'Id':^4} | {'Title':^20} | {'Priority':^8} | {'Status':^8} | {'Reported_by':^12} | {'Assignees':^10} |")
        print("+",'-'*5,'+','-'*20,'+','-'*9,'+','-'*8,'+','-'*13,'+','-'*12,'+',sep='')
        temp = "None"
        for row in reader:
            print(f"|{row["id"]:<5}|{row["Title"]:<20}|{row["Priority"]:<9}|{row["Status"]:<8}|{row["Reported_by"]:<13}|{temp:<12}|")
            print("+",'-'*5,'+','-'*20,'+','-'*9,'+','-'*8,'+','-'*13,'+','-'*12,'+',sep='')
        print()
    Tester()

def Add_Comment():
    with open('bugs.csv','r') as file:
        reader = csv.DictReader(file)
        id = int(input("Enter your bug id : "))
        found = False
        for row in reader:
            print(row)
            if id == int(row["id"]):
                found = True
                comment = input("Enter Your comment: ")
                add_info = {"id": id, "Comments": comment, "Assignees": None, 'Resolution_time': None}
                with open('add_info.csv','a', newline='') as file:
                    writer = csv.DictWriter(file,fieldnames=field1)
                    writer.writerow(add_info)
                    print("\nComment Added successfully\n")
                    Tester()
        if not found:
            print("Bug id not found !\n")
    Tester()

def Save_Exit():
    if bug != {}:
        with open("bugs.csv",'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=field)
            writer.writerow(bug)
    print("Saved\n")
    ask = input("Role Switch? ")
    if ask == "y":
        Role_Specification()

def Tester():
    choice = input("Choice: ")
    match choice:
        case '1':
            Report_Bug()
        case '2':
            View_my_Bugs()
        case '3':
            Add_Comment()
        case '4':
            Save_Exit()

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
            tester_login_id = input("Login as: ")
            print("--- Tester Menu ---")
            print("1. Report Bug")
            print("2. View My Bugs")
            print("3. Add Comment")
            print("4. Save & Exit")
            Tester()
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

print(" === Software Bug Tracking System (SBTS) ===")
Role_Specification()