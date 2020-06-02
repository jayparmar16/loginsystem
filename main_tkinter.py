import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os, sys
import sqlite3

conn = sqlite3.connect('accounts.db',timeout=10)
c = conn.cursor()

cursor = conn.execute("SELECT max(uid) FROM accounts")
for uid in cursor:
    x=int(uid[0])


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







class  LoginSystem(tk.Tk):                                                                     # initializing the app
    def __init__(self, *args, **kwargs):                                                                                            #I DON'T KNOW WHAT TO COMMENT ON THIS CLASS. 

        tk.Tk.__init__(self, *args,**kwargs)

        #tk.Tk.iconbitmap(self, default="arcadeicon.ico")                                           # This is the app icon. since the fifa 14 icon was already there on the macbook, I used it. So the line is commented because you don't have the icon.
        tk.Tk.wm_title(self, "RJ Login System")
        
        container = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        container.pack(side="top", fill="both", expand = True)          #placement of the frame
        container.grid_rowconfigure(0, weight=1)                    #uhhh
        container.grid_columnconfigure(0, weight=1)                 #uhhh



        self.frames = {}

        for F in (StartPage, LoginPage, CreateAccountPage,AdminPage,DeleteAccountPage,MakeAdminPage,UserPage): 

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        self.pack(fill="both",expand=True)

        self["bg"] = "light green"

        label=tk.Label(self,text="Welcome to Login System",bg="dark blue",fg="silver")
        label.pack(pady=10,padx=10)

        login_button=tk.Button(self,text="Login",bg="dark blue",fg="silver",command=lambda: controller.show_frame(LoginPage))
        login_button.pack()

        create_account_button=tk.Button(self,text="Create Account",bg="dark blue",fg="silver",command=lambda: controller.show_frame(CreateAccountPage))
        create_account_button.pack()

        close_button=tk.Button(self,text="Close App",bg="dark blue",fg="silver",command = self.close_window)
        close_button.pack()


    def close_window(self):
        app.destroy()


class LoginPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        self["bg"] = "light green"

        global lusername_entry
        global lpassword_entry

        ###             Title Frame (Frame No. 1)

        title_frame = tk.Frame(self,bg="light green")
        title_frame.pack(pady=3)

        title_label = tk.Label(title_frame,text="LOGIN",bg="dark blue",fg="silver")
        title_label.pack()

        ###             Username Frame (Frame No. 2)

        username_frame = tk.Frame(self,bg="light green")
        username_frame.pack(pady=2)

        username_label = tk.Label(username_frame, text="Enter Username",width=15)
        username_label.pack(side=tk.LEFT, padx=5, pady=5)

        lusername_entry = tk.Entry(username_frame)
        lusername_entry.pack(padx=5,expand=True)


        ###            Password Frame (Frame No. 3)

        password_frame = tk.Frame(self,bg="light green")
        password_frame.pack(pady=2)

        password_label = tk.Label(password_frame, text="Enter Password",width=15)
        password_label.pack(side=tk.LEFT, padx=5, pady=5)

        lpassword_entry = tk.Entry(password_frame,show="*")
        lpassword_entry.pack(padx=5,expand=True)    

        ###             Button Frame (Frame No. 4)

        button_frame = tk.Frame(self,bg="light green")
        button_frame.pack(fill="both",expand=True)

        create_button = tk.Button(button_frame,text="Login",bg="dark blue",fg="silver",command=self.check_login )
        create_button.pack(side=tk.RIGHT,padx=2)

        back_button = tk.Button(button_frame,text="Go Back",bg="dark blue",fg="silver",command=lambda: controller.show_frame(StartPage))
        back_button.pack(side=tk.RIGHT,padx=2)


    def check_login(self):
        #global lusername_entry
        #global lpassword_entry
        flag=False
        cursor = conn.execute("SELECT Username,Password,Admin FROM accounts")
        for row in cursor:
            username = lusername_entry.get()
            password = lpassword_entry.get()
            #print(username,row[0])
            #print(password,row[1])
            if row[0] == username and row[1] == password:
                flag=True
                break

        if flag==True:    
            if row[2]==1:
                lusername_entry.delete(0, tk.END)
                lpassword_entry.delete(0, tk.END)
                app.show_frame(AdminPage)
            else:
                lusername_entry.delete(0, tk.END)
                lpassword_entry.delete(0, tk.END)
                messagebox.showinfo(title="Logged in",message="Successfully Logged In")
                app.show_frame(UserPage)
                
        else:
            messagebox.showwarning(title="Error", message="Invalid Credentials.")   


class AdminPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        self["bg"] = "light green"

        ###             Title Frame (Frame No. 1)

        title_frame = tk.Frame(self,bg="light green")
        title_frame.pack(pady=3)

        title_label = tk.Label(title_frame,text="Welcome Admin",bg="dark blue",fg="silver")
        title_label.pack()

        view_button = tk.Button(self,text="View Database",bg="dark blue",fg="silver",command=self.view_Database)
        view_button.pack()

        delete_button = tk.Button(self,text="Delete Account",bg="dark blue",fg="silver",command=lambda : controller.show_frame(DeleteAccountPage))
        delete_button.pack()

        makeAdmin_button = tk.Button(self,text="MakeAdmin",bg="dark blue",fg="silver",command=lambda : controller.show_frame(MakeAdminPage))
        makeAdmin_button.pack()

        button_frame = tk.Frame(self,bg="light green")
        button_frame.pack(fill="both",expand=True)

        logout_button = tk.Button(button_frame,text="Logout",bg="dark blue",fg="silver",command=lambda: controller.show_frame(StartPage))
        logout_button.pack(side=tk.RIGHT,padx=2)


    def view_Database(self):
        # Creating tkinter window 
        window = tk.Tk() 
        window.resizable(width = 1, height = 1) 

        window.title("View Database")
        self["bg"]='light green'
        
        # Using treeview widget 
        treev = ttk.Treeview(window, selectmode ='browse') 
        
        # Calling pack method w.r.to treeview 
        treev.pack(side ='right') 
        
        # Constructing vertical scrollbar 
        # with treeview 
        verscrlbar = ttk.Scrollbar(window,  
                                orient ="vertical",  
                                command = treev.yview) 
        
        # Calling pack method w.r.to verical  
        # scrollbar 
        verscrlbar.pack(side ='right', fill ='x') 
        
        # Configuring treeview 
        treev.configure(xscrollcommand = verscrlbar.set) 
        
        # Defining number of columns 
        treev["columns"] = ("1", "2", "3","4","5") 
        
        # Defining heading 
        treev['show'] = 'headings'
        
        # Assigning the width and anchor to  the 
        # respective columns 
        treev.column("1", width = 90, anchor ='c') 
        treev.column("2", width = 90, anchor ='se') 
        treev.column("3", width = 90, anchor ='se') 
        treev.column("4", width = 90, anchor ='se') 
        treev.column("5", width = 90, anchor ='se') 
        
        # Assigning the heading names to the  
        # respective columns 
        treev.heading("1", text ="Name") 
        treev.heading("2", text ="U_id") 
        treev.heading("3", text ="Username")
        treev.heading("4", text ="Password")
        treev.heading("5", text ="Admin")
         
        
        # Inserting the items and their features to the  
        # columns built 


#        treev.insert("", 'end', text ="L1", values =("Nidhi", "F", "25")) 

        for row in c.execute('SELECT * FROM accounts'):
            treev.insert("", 'end', text ="L1", values = (row[3],row[2],row[0],row[1],row[4])) 
        
        
        # Calling mainloop 
        window.mainloop() 

class DeleteAccountPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        self["bg"] = "light green"

        global dusername_entry

        ###             Title Frame (Frame No. 1)

        title_frame = tk.Frame(self,bg="light green")
        title_frame.pack(pady=3)

        title_label = tk.Label(title_frame,text="DeleteAccount",bg="dark blue",fg="silver")
        title_label.pack()

        ###             Username Frame (Frame No. 2)

        username_frame = tk.Frame(self,bg="light green")
        username_frame.pack(pady=2)

        username_label = tk.Label(username_frame, text="Enter Username you wish to delete:",width=30)
        username_label.pack(side=tk.LEFT, padx=5, pady=5)

        dusername_entry = tk.Entry(username_frame)
        dusername_entry.pack(padx=5,expand=True)

        button_frame = tk.Frame(self,bg="light green")
        button_frame.pack(fill="both",expand=True)

        create_button = tk.Button(button_frame,text="Delete",bg="dark blue",fg="silver",command=self.check_username )
        create_button.pack(side=tk.RIGHT,padx=2)

        back_button = tk.Button(button_frame,text="Go Back",bg="dark blue",fg="silver",command=lambda: controller.show_frame(AdminPage))
        back_button.pack(side=tk.RIGHT,padx=2)


    def check_username(self):
        flag=True
        username = dusername_entry.get()
        cursor = conn.execute("SELECT Username FROM accounts")
        for row in cursor:
            #print(row[0],username)
            if username==row[0]:
                flag=False
    
        if flag==True:
            messagebox.showwarning(title="Error", message="Username does not exist")
        else:
            MsgBox = tk.messagebox.askquestion ('Are You Sure?','Are you sure you want to delete this user?',icon = 'warning')
            if MsgBox == 'yes':
                c.execute("DELETE FROM accounts WHERE Username='%s'"%username)
                conn.commit()
                messagebox.showinfo(title="Success", message="User has been deleted.")
                dusername_entry.delete(0, tk.END)
                app.show_frame(AdminPage)
            else:
                app.show_frame(DeleteAccountPage)

class MakeAdminPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        self["bg"] = "light green"

        global ausername_entry

        ###             Title Frame (Frame No. 1)

        title_frame = tk.Frame(self,bg="light green")
        title_frame.pack(pady=3)

        title_label = tk.Label(title_frame,text="Make Admin",bg="dark blue",fg="silver")
        title_label.pack()

        ###             Username Frame (Frame No. 2)

        username_frame = tk.Frame(self,bg="light green")
        username_frame.pack(pady=2)

        username_label = tk.Label(username_frame, text="Enter Username you wish to make admin:",width=30)
        username_label.pack(side=tk.LEFT, padx=5, pady=5)

        ausername_entry = tk.Entry(username_frame)
        ausername_entry.pack(padx=5,expand=True)

        button_frame = tk.Frame(self,bg="light green")
        button_frame.pack(fill="both",expand=True)

        create_button = tk.Button(button_frame,text="Make Admin",bg="dark blue",fg="silver",command=self.check_username )
        create_button.pack(side=tk.RIGHT,padx=2)

        back_button = tk.Button(button_frame,text="Go Back",bg="dark blue",fg="silver",command=lambda: controller.show_frame(AdminPage))
        back_button.pack(side=tk.RIGHT,padx=2)


    def check_username(self):
        flag=True
        username = ausername_entry.get()
        cursor = conn.execute("SELECT Username FROM accounts")
        for row in cursor:
            #print(row[0],username)
            if username==row[0]:
                flag=False
    
        if flag==True:
            messagebox.showwarning(title="Error", message="Username does not exist")
        else:
            MsgBox = tk.messagebox.askquestion ('Are You Sure?','Are you sure you want to make this user an admin?',icon = 'warning')
            if MsgBox == 'yes':
                c.execute("UPDATE accounts SET Admin=1 WHERE Username='%s'"%username)
                conn.commit()
                messagebox.showinfo(title="Success", message="User has been made an Admin")
                ausername_entry.delete(0, tk.END)
                app.show_frame(AdminPage)
            else:
                app.show_frame(MakeAdminPage)


class UserPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        self["bg"] = "light green"

        ###             Title Frame (Frame No. 1)

        title_frame = tk.Frame(self,bg="light green")
        title_frame.pack(pady=3)

        title_label = tk.Label(title_frame,text="Welcome User",bg="dark blue",fg="silver")
        title_label.pack()

        button_frame = tk.Frame(self,bg="light green")
        button_frame.pack(fill="both",expand=True)

        logout_button = tk.Button(button_frame,text="Logout",bg="dark blue",fg="silver",command=lambda: controller.show_frame(StartPage))
        logout_button.pack(side=tk.RIGHT,padx=2)


class CreateAccountPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        self["bg"] = "light green"

        #title_label=tk.Label(self,text="ACCOUNT CREATION",bg="dark blue",fg="silver")
        #title_label.config(anchor=tk.CENTER)
        #title_label.grid()

        #FullName_label = tk.Label(self,text="Enter Fullname",bg="Silver",fg="black").grid(column=0,row=1)
        #FullName_entry = tk.Entry(self).grid(column=2,row=1)
        




        #back_button=tk.Button(self,text="Go Back",bg="dark blue",fg="silver",command=lambda: controller.show_frame(StartPage))
        #back_button.grid()


        #closeButton = tk.Button(self, text="Close")
        #closeButton.pack(side=tk.RIGHT, padx=5, pady=5)
        #okButton = tk.Button(self, text="OK")
        #okButton.pack(side=tk.RIGHT)

#        frame2 = tk.Frame(self)
#       frame2.pack(fill=tk.X)

#        lbl2 = tk.Label(frame2, text="Author", width=6)
#        lbl2.pack(side=tk.LEFT, padx=5, pady=5)

#       entry2 = tk.Entry(frame2)
#        entry2.pack(fill=tk.X, padx=5, expand=True)    

        global cname_entry
        global cusername_entry
        global cpassword_entry
        global crepassword_entry


###             Title Frame (Frame No. 1)

        title_frame = tk.Frame(self,bg="light green")
        title_frame.pack(pady=3)

        title_label = tk.Label(title_frame,text="ACCOUNT CREATION",bg="dark blue",fg="silver")
        title_label.pack()


###             Name Frame (Frame No. 2)
        name_frame = tk.Frame(self,bg="light green")
        name_frame.pack(pady=2)

        name_label = tk.Label(name_frame, text="Enter FullName",width=15)
        name_label.pack(side=tk.LEFT, padx=5, pady=5)

        cname_entry = tk.Entry(name_frame)
        cname_entry.pack(padx=5, expand=True)

###             Username Frame (Frame No. 3)

        username_frame = tk.Frame(self,bg="light green")
        username_frame.pack(pady=2)

        username_label = tk.Label(username_frame, text="Enter Username",width=15)
        username_label.pack(side=tk.LEFT, padx=5, pady=5)

        cusername_entry = tk.Entry(username_frame)
        cusername_entry.pack(padx=5,expand=True)


###             Password Frame (Frame No. 4)

        password_frame = tk.Frame(self,bg="light green")
        password_frame.pack(pady=2)

        password_label = tk.Label(password_frame, text="Enter Password",width=15)
        password_label.pack(side=tk.LEFT, padx=5, pady=5)

        cpassword_entry = tk.Entry(password_frame,show="*")
        cpassword_entry.pack(padx=5,expand=True)

###             Re-Password Frame (Frame No. 5)

        repassword_frame = tk.Frame(self,bg="light green")
        repassword_frame.pack(pady=2)

        repassword_label = tk.Label(repassword_frame, text="Re-Enter Password",width=15)
        repassword_label.pack(side=tk.LEFT, padx=5, pady=5)

        crepassword_entry = tk.Entry(repassword_frame,show="*")
        crepassword_entry.pack(padx=5,expand=True)

###             Button Frame (Frame No. 6)

        button_frame = tk.Frame(self,bg="light green")
        button_frame.pack(fill="both",expand=True)

        create_button = tk.Button(button_frame,text="Create",bg="dark blue",fg="silver", command=self.check_username_availability)
        create_button.pack(side=tk.RIGHT,padx=2)

        back_button = tk.Button(button_frame,text="Go Back",bg="dark blue",fg="silver",command=lambda: controller.show_frame(StartPage))
        back_button.pack(side=tk.RIGHT,padx=2)

    def check_username_availability(self):
        flag=True
        username = cusername_entry.get()
        cursor = conn.execute("SELECT Username FROM accounts")
        for row in cursor:
            #print(row[0],username)
            if username==row[0]:
                flag=False
    
        if flag==False:
            messagebox.showwarning(title="Error", message="Username is already taken")
        else:
            CreateAccountPage.password_validity(self)
        
    def password_validity(self):
        name=cname_entry.get()
        username=cusername_entry.get()
        password=cpassword_entry.get()
        repassword = crepassword_entry.get()
        u_id=User.unique_id(x)

        l=len(password)
        lcount,ucount,dcount,scount=0,0,0,0

        if l < 8:
            messagebox.showwarning(title="Error", message="Password is too short. Must be atleast 8 characters.")

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
                print("Password Check: ",password,repassword)
                if password != repassword:
                    messagebox.showwarning(title="Error", message="Entered passwords do not match.")
                else:        
                    c.execute("INSERT INTO accounts VALUES('%s','%s',%d,'%s',0)"%(username,password,u_id,name))
                    conn.commit()
                    messagebox.showwarning(title="Success", message="Account has been created.")
                    cname_entry.delete(0, tk.END)
                    cusername_entry.delete(0, tk.END)
                    cpassword_entry.delete(0, tk.END)
                    crepassword_entry.delete(0, tk.END)
                    app.show_frame(LoginPage)
            else:
                messagebox.showwarning(title="Error", message="Password must contain 8 characters including atleast 1 uppercase, 1 lowercase, 1 digit and 1 special character.")
                


        

app = LoginSystem()
app.geometry("500x500")
app.mainloop()
