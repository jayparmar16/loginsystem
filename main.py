import os, sys
import sqlite3
import getpass_ak

cwd=os.getcwd()
print(cwd)

## dirlist = os.listdir()

## from pprint import pprint
## pprint(dirlist)

conn = sqlite3.connect('accounts.db',timeout=10)
c = conn.cursor()

cursor = conn.execute("SELECT max(uid) FROM accounts")
for uid in cursor:
    x=int(uid[0])
    #print("x=",x)

class User:
    def __init__(self,usr_name,password,v_password,uq_id):
        self.usr_name = usr_name
        self.password = password
        self.v_password = v_password
        self.uq_id = uq_id

    @staticmethod
    def validation(p,p1):
        if p == p1:
            return True
        else:
            return False

    @staticmethod
    def unique_id(x):
       x+=1
       return x

    @staticmethod
    def checkAdmin(usr_name):
        cursor = conn.execute("SELECT Admin FROM accounts WHERE Username='%s'"%usr_name)
        for r in cursor:
            a = r[0]
        if (a == 1):
            return True
        else:
            return False   
       
    def show(self):
        print(f"Username: {self.usr_name}")
        print(f"Password: {self.password}")
        print(f"V_Password : {self.v_password}")
        print(f"Unique Id : {self.uq_id}")

### FUNCTION TO CHECK VALIDITY OF PASSWORD
def pass_validation(password):
    l=len(password)
    lcount,ucount,dcount,scount=0,0,0,0

    if l < 8:
        print("Password is too short. Must contain 8 characters including atleast 1 uppercase, 1 lowercase, 1 digit and 1 special character.")
        return False

    else:
        for i in range(l):

            if password[i].islower():
                lcount+=1

            elif password[i].isupper():
                ucount+=1

            elif password[i].isdigit():
                dcount+=1

            elif not password[i].isalnum():
                scount+=1            

        if (lcount > 0) and (ucount > 0) and (dcount > 0) and (scount > 0) and (lcount+ucount+dcount+scount==l):
            return True
        else:
            print("Password must contain 8 characters including atleast 1 uppercase, 1 lowercase, 1 digit and 1 special character.")
            return False

### ADMIN FUNCTION FOR DELETING ACCOUNT  
def delete_acc():
    inp = input("Enter the Username you want to delete : ")
    cursor = conn.execute("SELECT Username,Password,Name,uid FROM accounts WHERE Username='%s'"%inp)
    for row in cursor:
        print (f"Deleting Account : {row}")
    choice = input("Are you sure you want to delete this account (Y/N) : ")
    if choice == "Y" or choice == "y":
        c.execute("DELETE FROM accounts WHERE Username='%s'"%inp)
        conn.commit()                            

    else:
        choice2=input("Do you wish to delete an account (Y/N)? : ")
        if choice2 == "Y" or choice2 == "y":
            delete_acc()
        else:
            return

### ADMIN FUNCTION FOR VIEWING ALL ACCOUNTS
def show():
    for row in c.execute('SELECT * FROM accounts'):
        print(row)


### ADMIN FUNCTION TO GIVE AN ACCOUNT ADMIN PREVILIGES
def make_admin():
    inp = input("Enter the Username you want to make an admin : ")
    c.execute("UPDATE accounts SET Admin=1 WHERE Username='%s'"%inp)
    print(f"Successfully made {inp} an admin !")
    conn.commit()


### MAIN FUNCTION CALLED WITHIN A LOOP    
def main():
    print("\n\nHello!")
    print("1. Login \n")
    print("2. Create an account \n")
    print("3. Quit \n")
    choice = int(input("Enter your choice : "))

    ### LOGINING IN
    if choice == 1:
        usr = input("Enter your username : ")
        passwrd = (getpass_ak.getpass('Enter password : '))
        cursor = conn.execute("SELECT Username,Password FROM accounts")
        for row in cursor:
            if row[0] == usr and row[1] == passwrd:
                
                print("Logged in succesfully !")
                
                while True:
                    if User.checkAdmin(usr) == 1:
                        print("\n\nWelcome Admin!")
                        print("1. View the Database")
                        print("2. Delete an Account")
                        print("3. Make an Admin")
                        print("4. Logout")
                        choic = int(input("Enter your input : "))
                        if choic == 1:
                            show()

                        elif choic == 2:
                            delete_acc()

                        elif choic == 3:
                            make_admin()

                        elif choic == 4:
                            break

                        else:
                            print("Wrong Input")
                    else:
                        print ("Welcome User! ")
                        break
                break

        else:
            print("Incorrect Credentials \n \n")
        
        return True
        
    ### CREATING ACCOUNT
    elif choice == 2:
        name = input("Enter your full name : ")
        usr = input("Enter your username : ")
        
        while True:
            exit=False
            while exit==False:
                passwrd = (getpass_ak.getpass('Enter password : '))
                exit=pass_validation(passwrd)
                if exit==True:
                    print("Password \'%s\' is valid."%passwrd)

            passwrd1 = (getpass_ak.getpass('Re enter password : '))
            uq_id = User.unique_id(x)
            u1 = User(usr,passwrd,passwrd1,uq_id)
            #u1.show()

            if User.validation(passwrd,passwrd1) == True:
                print("Succesfully Created")
                c.execute("INSERT INTO accounts VALUES('%s','%s',%d,'%s',0)"%(usr,passwrd,uq_id,name))
                conn.commit()
                break

            else:
                print("Passwords don't match")

        return True
    
    elif choice == 3:
        return False
    
    else:
        print("Wrong input")

        


exit_status=True
while (exit_status):
    exit_status=main()