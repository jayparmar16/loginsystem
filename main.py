###
import sqlite3
import getpass_ak
conn = sqlite3.connect('accounts.db')
c = conn.cursor()
###


class User:
    
    def __init__(self,usr_name,password,v_password,uq_id):
        self.usr_name = usr_name
        self.password = password
        self.v_password = v_password
        self.uq_id = uq_id

    @staticmethod
    def validation(p,p1):  ### checking if password and re-entered pass is same
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


def pass_validation(password):
    l = len(password)

    if l < 8:
        print("Password is too short. Must contain 8 characters including atleast 1 uppercase, 1 lowercase, 1 digit and 1 special character.")
        return False
    else:
        for i in range(l):
            if password[i].isupper():

                for i in range(l):
                    if password[i].islower():
                        
                        for i in range(l):
                            if password[i].isdigit():

                                for i in range(l):
                                    if not password[i].isalnum():   
                                       return True     
                            
                                print("Password does not have a special character. Must contain 8 characters including atleast 1 uppercase, 1 lowercase, 1 digit and 1 special character.")
                                return False

                        print("Password does not have a digit. Must contain 8 characters including atleast 1 uppercase, 1 lowercase, 1 digit and 1 special character.")
                        return False

                print("Password does not have a lower case character. Must contain 8 characters including atleast 1 uppercase, 1 lowercase, 1 digit and 1 special character.")
                return False
                
        print("Password does not have an upper case character. Must contain 8 characters including atleast 1 uppercase, 1 lowercase, 1 digit and 1 special character.")
        return False    
    

print("Hello!")
print("1.Login \n")
print("2.Create an account \n")
choice = int(input("Enter your choice : "))

### LOGINING IN
if choice == 1:
    usr = input("Enter your username : ")
    passwrd = (getpass_ak.getpass('Enter password : '))
    cursor = conn.execute("SELECT Username,Password FROM accounts")
    for row in cursor:
        if row[0] == usr and row[1] == passwrd:
            print("Logged in succesfully !")
            if User.checkAdmin(usr) == 1:
                print("1.View the Database")
                print("2.Delete an Account")
                print("3.Make an Admin")
                choic = int(input("Enter your input : "))
                if choic == 1:
                    for ro in c.execute('SELECT * FROM accounts'):
                        print(row)
                elif choic == 2:
                    inp = input("Enter the Username or Unique ID you want to delete : ")
                    pass
                elif choic == 3:
                    pass
                else:
                    print("Wrong Input")
            else:
                pass
            break
        else:
            print("Incorrect Credentials")
    
### CREATING ACCOUNT
elif choice == 2:
    name = input("Enter your full name : ")
    usr = input("Enter your username : ")
    
    exit=False
    while exit==False:
        passwrd = (getpass_ak.getpass('Enter password : '))
        exit=pass_validation(passwrd)
        if exit==True:
            print("Password \'%s\' is valid."%passwrd)

    passwrd1 = (getpass_ak.getpass('Re enter password : '))
    cursor = conn.execute("SELECT MAX(uid) FROM accounts")
    for row in cursor:
        x = int(row[0])
    uq_id = User.unique_id(x)
    u1 = User(usr,passwrd,passwrd1,uq_id)
    #u1.show()

    if User.validation(passwrd,passwrd1) == True:
        print("Succesfully Created")
        c.execute("INSERT INTO accounts VALUES('%s','%s',%d,'%s',0)"%(usr,passwrd,uq_id,name))
        conn.commit()
    else:
        print("Passwords don't match")
else:
    print("Wrong input")
