from errno import errorcode
import encodings
import pandas as pd
from tkinter import DISABLED, END, Canvas, filedialog as fd
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import speech_recognition as sr
from tktimepicker import AnalogPicker, AnalogThemes
from configparser import Error
import tkinter as tk
import mysql.connector
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from email.mime.text import MIMEText
import time
import smtplib , ssl
import random
import socket
from twilio.rest import *
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import pickle
import sklearn
import string
from validate_email import validate_email


try:
    bulk_DB = mysql.connector.connect(host="localhost", user="root", passwd="shanu873", database='bulk_email')
    mycursor = bulk_DB.cursor()
except:
    messagebox.showerror(title="error", message="something is worng with database")

msg = MIMEMultipart()

name_list = []
name_list1 = []

def mysql_selection(sql):
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for i in myresult:
        return i

def isconnect():
    try:
        sock = socket.create_connection(("www.google.com", 80))
        if sock is not None:
            sock.close
    except:
        return False
    else:
        return True

def first_login():

    mycursor.execute(f"select * from email_pass where email_2 = '{obj.enter_email_entry.get()}';")
    check = mycursor.fetchall()
    if check==[]:
        def commit_detail():

            try:

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(email_add_1.get(), email_pass.get())
            except:
                messagebox.showerror(title="ERROR", message="INFORMATION IS NOT CORRECT")

            else:
                try:
                    mycursor.execute(f"insert into email_pass(email_address, email_password, email_2) values('{email_add_1.get()}', '{email_pass.get()}','{obj.enter_email_entry.get()}');")
                    bulk_DB.commit()
                    mycursor.execute(f"insert into login_logout(email_ad) values ('{obj.enter_email_entry.get()}');")
                    bulk_DB.commit()
                    
                except:
                    messagebox.showerror(title="ERROR", message="Something is went wrong")
                else:
                    root2.destroy()
                    obj.login_frame.destroy()
                    obj.home_page()

        root2 = Tk()
        root2.geometry("400x200")
        root2.title("WELCOME TO BULK CLIENT")

        email_add = Label(root2, text="Enter email : ", fg="black", bg="white", font=("Helvetica", 10))
        email_add.place(x=20, y=20)

        email_add_1 = tk.Entry(root2 , bd = 2 , fg = "black" , highlightthickness= 1 , highlightbackground= "#884dff")
        email_add_1.place(width = 240 , x=20 , y=50)

        email_pas = Label(root2, text="Enter 2 step verification password : ", fg="black", bg="white", font=("Helvetica", 10))
        email_pas.place(x=20, y=85)

        email_pass=tk.Entry(root2 , bd = 2 , fg = "black" , highlightthickness= 1 , highlightbackground= "#884dff")
        email_pass.place(width = 240, x=20, y=115)

        submit_2 = tk.Button(root2 , text = "SUBMIT" , bd = 1 , highlightthickness= 1 , highlightbackground= "#110033" , background = "#aa80ff", command=commit_detail)
        submit_2.place(width = 100 , x=20 , y=150)

        root2.resizable(False, False)
        root2.mainloop()
    else:
        mycursor.execute(f"insert into login_logout(email_ad) values ('{obj.enter_email_entry.get()}');")
        bulk_DB.commit()
        obj.login_frame.destroy()
        obj.home_page()

def login():
        
    if isconnect()==True:

        email = obj.enter_email_entry.get().lower()
        password = obj.enter_password_entry.get()
        is_valid = validate_email(email,check_mx=True)
        if is_valid==True:

            mycursor.execute(f"select * from bulk_signup where sender_email='{email}';")
            result = mycursor.fetchall()

            if result==[]:
                messagebox.showerror(title="LOGIN ERROR", message="This email does not exist in our database \nplease check your email")
            elif result[0][2]==email and result[0][-1]==password:
                first_login()
            elif result[0][2]==email and result[0][-1]!=password:
                messagebox.showinfo(title="LOGIN INFO", message="You are entering wrong password \nplease enter correct password")
            else:
                messagebox.showerror(title="LOGIN ERROR", message="something goes wrong with login")
            
        elif email=="" and password=="":
            messagebox.showerror(title="Email Error", message="PLEASE ENTER EMAIL AND PASSWORD")
        
        elif email=="" or password=="":
            messagebox.showerror(title="Information Error", message="PLEASE ENTER COMPLETE INFORMATION")

        else:
            messagebox.showerror(title="Email Error", message="PLEASE ENTER VAILID EMAIL")

    else:
        messagebox.showinfo(title="INTERNET CHECK", message="PLEASE CHECK INTERNET CONNECTION")

# Function for forget password
def forget_password():

    def login_back():
        root.destroy()

    change_otp = random.randint(100000, 999999)
    def send_otp():
        if isconnect()==True:
            forget_pass = for_email.get()

            mycursor.execute(f"select * from bulk_signup where sender_email='{for_email.get()}';")
            result_1 = mycursor.fetchall()

            if result_1==[]:
                messagebox.showerror(title="INFORMATION ERROR", message=f"email : {for_email.get()} not registered in Bulk Client \nPlease check your email again.")
                root.destroy()
            elif result_1[0][2]==forget_pass:
                try:
                    sender_em = "bulkclient@gmail.com"
                    receiver_em = for_email.get()
                    password_em = "cvlhlnzmpadakehk"

                    msg = MIMEText(f"Dear member,\nThis is your reset OTP : {change_otp}.\nGreetings from BULK_CLIENT")
                    msg['Subject']="FORGET PASSWORD"
                    msg['From']="bulkclient@gmail.com"
                    msg['To']=for_email.get()

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(sender_em, password_em)
                    server.sendmail(sender_em, receiver_em, msg.as_string())
                except:
                    messagebox.showerror(title="ERROR", message="EMAIL HAS NOT SENT.")
                else:
                    def otp_forget():
                        get_otp = otp_1.get()
                        if get_otp==str(change_otp):
                            root1.destroy()
                            def pass_change():
                                new = new_password.get()
                                cur = conf_password.get()

                                if new==cur:
                                    try:
                                        mycursor.execute(f"update bulk_signup set sender_password = '{new}' where sender_email = '{for_email.get()}';")
                                        bulk_DB.commit()
                                    except:
                                        messagebox.showerror(title="ERROR", message="Something wrong with database connection")
                                    else:
                                        root2.destroy()
                                        messagebox.showinfo(title="SUCCESS", message="Password change successfully \nNow you can login with your new password")
                                else:
                                    messagebox.showerror(title="UNMATCHED0", message="Please check password once again \nPasswords are unmatched")

                                

                            root2 = Tk()
                            root2.geometry("400x200")
                            root2.title("CHANGE PASSWORD")

                            new_pas = Label(root2, text="New password : ", fg="black", bg="white", font=("Helvetica", 10))
                            new_pas.place(x=20, y=20)

                            new_password = tk.Entry(root2 , bd = 2 , fg = "black" , highlightthickness= 1 , highlightbackground= "#884dff")
                            new_password.place(width = 240 , x=20 , y=50)

                            conf_pas = Label(root2, text="Confirm password : ", fg="black", bg="white", font=("Helvetica", 10))
                            conf_pas.place(x=20, y=85)

                            conf_password=tk.Entry(root2 , bd = 2 , fg = "black" , highlightthickness= 1 , highlightbackground= "#884dff")
                            conf_password.place(width = 240, x=20, y=115)

                            submit_2 = tk.Button(root2 , text = "SUBMIT" , bd = 1 , highlightthickness= 1 , highlightbackground= "#110033" , background = "#aa80ff", command=pass_change)
                            submit_2.place(width = 100 , x=20 , y=150)

                            root2.resizable(False, False)
                            root2.mainloop()

                        else:
                            messagebox.showerror(title="OTP ERROR", message="PLEASE ENTER VAILID OTP.")
            
                    root.destroy()
                    root1 = Tk()
                    root1.geometry("400x200")
                    root1.title("OTP Verification")

                    lable2 = Label(root1, text="Enter OTP here : ", fg="black", bg="white", font=("Helvetica", 10))
                    lable2.place(x=20, y=40)

                    otp_1 = tk.Entry(root1 , bd = 2 , fg = "black" , highlightthickness= 1 , highlightbackground= "#884dff")
                    otp_1.place(width = 240 , x=20 , y=70)

                    submit = tk.Button(root1 , text = "SUBMIT" , bd = 1 , highlightthickness= 1 , highlightbackground= "#110033" , background = "#aa80ff", command=otp_forget)
                    submit.place(width = 100 , x=20 , y=100)

                    root1.resizable(False, False)
                    root1.mainloop()
            else:
                messagebox.showinfo(title="NOT IDENTIFY", message="Something went wrong")

        else:
            messagebox.showeinfo(title="INTERNET CHECK", message="PLEASE CHECK INTERNET CONNECTION")


    root = Tk()
    root.geometry("400x200")
    root.title("FORGET PASSWORD")

    lable1 = Label(root, text="Enter your register email here : ", fg="black", bg="white", font=("Helvetica", 10))
    lable1.place(x=20, y=40)

    for_email = tk.Entry(root , bd = 2 , fg = "black" , highlightthickness= 1 , highlightbackground= "#884dff")
    for_email.place(width = 240 , x=20 , y=70)

    sendotp = tk.Button(root , text = "SEND OTP" , bd = 1 , highlightthickness= 1 , highlightbackground= "#110033" , background = "#aa80ff", command=send_otp)
    sendotp.place(width = 100 , x=20 , y=100)

    back = tk.Button(root , text = "BACK" , bd = 1 , highlightthickness= 1 , highlightbackground= "#110033" , background = "#aa80ff", command=login_back)
    back.place(width = 100 , x=140, y=100)
    root.resizable(False, False)
    root.mainloop()

# .function for register client
def register_client():
        
    if isconnect()==True:
        name=obj.enter_admin_name.get()
        email=obj.enter_email.get()
        password=obj.enter_password.get()
        contact=obj.enter_contact_number.get()


        if email.endswith("@gmail.com")==True or email.endswith(".ac.in")==True or email.endswith(".org")==True:
            otp = random.randint(100000, 999999)
            try:
                sender_em = "bulkclient@gmail.com"
                receiver_em = email
                password_em = "cvlhlnzmpadakehk"

                msg = MIMEText(f"{otp}")
                msg['Subject']="OTP Verification"
                msg['From']="bulkclient@gmail.com"
                msg['To']=email

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_em, password_em)

                server.sendmail(sender_em, receiver_em, msg.as_string())

                otp_sms = random.randint(100000, 999999)

                acc_sid = "AC2119ad1dc427092d02448d898284cc4f"

                auth_token = "c8c1dc1aaccfb83705a4b2fc58047199"

                client = Client(acc_sid , auth_token)
                to_send = ["8821818297" , "8359003360" , "7000207480" , "9300268003" , "9406908707" , "7470704895"]
                for numbers in to_send:
                    if numbers==obj.enter_contact_number.get():
                        numbers="+91"+obj.enter_contact_number.get()
                        message = client.messages.create(
                            body = f"Message Sent to Authenticate OTP: {otp_sms}",
                            from_= "+13854833430" ,
                            to = numbers
                                )
                message_1 = message.sid
                messagebox.showinfo(title='SMS OTP', message=f"YOUR SMS HAS BEEN SENT SUCCESSFULLY \n THIS IS YOUR MESSAGE ID : {message_1}")
            except:
                messagebox.showerror(title="Error", message="OTP has not sent!!!")
            else:
                def otp_gui():
                    otp_verify = otp_1.get()
                    if otp_verify==str(otp) and otp_2.get()==str(otp_sms):
                        mycursor.execute("select * from bulk_signup order by sender_id DESC LIMIT 1;")
                        res = mycursor.fetchall()
                        if res==[]:
                            sender_id = "1"
                        else:
                            a = int(res[0][0])+1
                            sender_id = str(a)
                        try:
                            mycursor.execute(f"insert into bulk_signup(sender_id, sender_name, sender_email, sender_number, sender_password) values('{sender_id}','{name}', '{email}', '{contact}', '{password}');")
                            bulk_DB.commit()
                        except:
                            root.destroy()
                            messagebox.showerror(title="Error", message="Something went wrong with database!!!")
                        else:
                            root.destroy()
                            messagebox.showinfo(title="Submission", message="Registered successfullly please Sign In")
                            obj.signup_frame.destroy()
                            obj.login_page()
                    else:
                        messagebox.showinfo(title="WRONG OTP", message="YOU ARE ENTERING WRONG OTP")

                root = Tk()
                root.geometry("400x200")
                root.title("OTP Verification")

                lable1 = Label(root, text="Enter Email OTP here : ", fg="black", bg="white", font=("Helvetica", 10))
                lable1.place(x=20, y=20)

                lable2 = Label(root, text="Enter SMS OTP here : ", fg="black", bg="white", font=("Helvetica", 10))
                lable2.place(x=20, y=80)

                    
                otp_1 = tk.Entry(root , bd = 2 , fg = "black" , highlightthickness= 1 , highlightbackground= "#884dff")
                otp_1.place(width = 240 , x=20 , y=50)

                otp_2 = tk.Entry(root , bd = 2 , fg = "black" , highlightthickness= 1 , highlightbackground= "#884dff")
                otp_2.place(width = 240 , x=20 , y=110)

                login = tk.Button(root , text = "SUBMIT" , bd = 1 , highlightthickness= 1 , highlightbackground= "#110033" , background = "#aa80ff", command=otp_gui)
                login.place(width = 100 , x=20 , y=140)

                root.resizable(False, False)
                root.mainloop()

        elif email=='':
            messagebox.showinfo(title="INFORMATION", message="PLEASE ENTER INFORMATION")
        else:
            messagebox.showerror(title="EMAIL ERROR", message="PLEASE ENTER VAILID EMAIL")

    else:
        messagebox.showeinfo(title="INTERNET CHECK", message="PLEASE CHECK INTERNET CONNECTION")

def log_out():
    exist = messagebox.askyesno(title="LOGOUT?", message="Do you want to log out?")
    if exist==True:
        mycursor.execute("truncate login_logout;")
        bulk_DB.commit()
        mycursor.execute("truncate bulkemail_entermanually;")
        bulk_DB.commit()
        mycursor.execute("truncate bulkemail_attachment;")
        bulk_DB.commit()
        mycursor.execute("truncate bulkemail_csvupload;")
        bulk_DB.commit()
        obj.home_frame.destroy()
        obj.login_page()
    else:
        pass

def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

# function for attech file
len_wrong_mail=[]
len_actual_mail=[]
def attach_file():
    global len_wrong_mail
    global len_actual_mail
    global wrong_mail_id
    global email_list
    email_list = []
    wrong_mail_id=[]
    i = 0
    a = i
    try:
        f = fd.askopenfile(title="Select File To Upload", filetypes=(
            ('Excel File', ('*.xlsx', '*.xls')), ('Csv File', '*.csv'),('Json File','*.json'),('HTML File','.html'),('XML File','*.xml')))
        if f is not None:
            # Convert File path To String
            path = f.name
            if(path.endswith(".csv")):
                dframe = pd.read_csv(path)
                # Creating a list of Email Addresses taken from csv file given By User
                email_list = dframe['Emails'].tolist()
            elif(path.endswith(".xlsx") or path.endswith(".xls")):
                dframe1 = pd.read_excel(path)
                # Creating a list of Email Addresses taken from Excel file given by User
                email_list = dframe1['Emails'].tolist()
            elif(path.endswith(".json")):
                dframe1 = pd.read_json(path)
                # Creating a list of Email Addresses taken from Excel file given by User
                email_list = dframe1['Emails'].tolist()
            elif(path.endswith(".html")):
                dframe1 = pd.read_html(path)
                # Creating a list of Email Addresses taken from Excel file given by User
                email_list = dframe1['Emails'].tolist()
            elif(path.endswith(".xml")):
                dframe1 = pd.read_xml(path)
                # Creating a list of Email Addresses taken from Excel file given by User
                email_list = dframe1['Emails'].tolist()
            else:
                status_lbl1.config("Please Select Valid File!")
            
            for mails in email_list:
                is_valid = validate_email(mails,check_mx=True)
                if is_valid==False:
                    wrong_mail_id.append(mails)
                    email_list.remove(mails)
            len_actual_mail=len(email_list)
            len_wrong_mail=len(wrong_mail_id)
            df = pd.DataFrame(wrong_mail_id)
            if (len(wrong_mail_id) > 0):
                df.to_csv("wrong_id.csv", index = True  , encoding = 'utf-8' )
            b = a+1
            # Convert Email File To Binary Data To Store In Database
            email_file = convertToBinaryData(path)
            val = (b, email_file)
            sql = "INSERT INTO bulkemail_csvupload(id , email_file) VALUES (%s , %s)"


            # Insert Query For Database with Function mysql_connection
            # Passing Query to mysql_connection to Insert Email file in Database
            try:
                mycursor.execute(sql, val)
                bulk_DB.commit()
                messagebox.showinfo(title="STATUS", message="File Uploaded Successfully!")
                obj.attach_file['state']='disabled'
            # Passing index and Email Addresses list to mysql_connection function
            #    # Calling Function]
            except:
                messagebox.showerror(title="DATABASE ERROR", message="database attech file error")
        else:
            status_lbl1.config(text="Please Select A File!")
    except ValueError:
        status_lbl1.config(text="Please Select A Valid File Type!")
    except FileNotFoundError:
        status_lbl1.config(text="File Not Found!")

def visual(x,y):
    import tkinter as tk
    import matplotlib

    matplotlib.use('TkAgg')

    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import (
        FigureCanvasTkAgg,
        NavigationToolbar2Tk
    )


    class App(tk.Tk):
        
        def __init__(self):
            super().__init__()

            self.title('Tkinter Matplotlib Demo')


            # prepare data
            data = {
                'successufully_sent': x,
                'Failed_to_sent': y,
                }
            languages = data.keys()
            popularity = data.values()

            # create a figure
            figure = Figure(figsize=(3, 5), dpi=100)
            
            # create FigureCanvasTkAgg object
            figure_canvas = FigureCanvasTkAgg(figure, self)

            # create the toolbar
            NavigationToolbar2Tk(figure_canvas, self)

            # create axes
            axes = figure.add_subplot()

            # create the barchart
            axes.bar(languages, popularity)
            axes.set_title('Logs Visualisation')
            axes.set_ylabel('No.of Messages')

            figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
           
    app=App()
    app.mainloop()
#def ask():
 #   a = messagebox.askyesno(title="Confirmation",message="THIS IS GRAPH OF SUCCESS RATE, CONTINUE?",)
  #  if a==True:
   #     visual(len_actual_mail,len_wrong_mail)
    #
    #else:
     #   pass


global file
def attach_attachment():
    file = fd.askopenfilenames()
    ind = 0
    if file is not None:
        global file_path
        file_path = list(file)
        a = []
        for i in range(len(file_path)):
            a.append(os.path.getsize(file_path[i]))
            if ((a[i]) > 1.6e+7):
                messagebox.showwarning(
                    title="Warning!", message="File Selected Is Too Large !\nPLease Attach File Under 16MB")
            else:
                # attach_file = convertToBinaryData(file_path[i])
                attach_files= open(file_path[i] , 'rb')
                attach_file = attach_files.read()
                id1 = i+1
                sql = "INSERT INTO bulkemail_attachment(id , attachment) VALUES (%s , %s)"
                val = (id1, attach_file)

                try:
                    mycursor.execute(sql, val)
                    bulk_DB.commit()
                    messagebox.showinfo(title="STATUS", message="File Uploaded Successfully!")

                except:
                    messagebox.showerror(title="DATABASE ERROR", message="ATTECHMENT DATABSE1 something goes wronmg")

                sql = "SELECT attachment FROM bulkemail_attachment"
                mycursor.execute(sql)
                attechment_data = mycursor.fetchall()
                binary_file = attechment_data

                for f in file_path:
                    attachment_file_name = f
                    attachment_file_name1 = attachment_file_name.split('/')    # spliting the attached file and extracting only file name
                    try:
                        attach_file = binary_file[1][0]
                        ind = 1
                    except IndexError as err:
                        a = 1
                        #messagebox.showerror(title = "Something Went Wrong" , message = "error")
                        pass
                    if (ind == 1):
                        payload = MIMEBase("application" , "octate-stream" , Name = attachment_file_name1[len(attachment_file_name1)-1])
                        payload.set_payload(attach_file)
                        encoders.encode_base64(payload)
                        payload.add_header("Content-Decomposition" , "attachment")
                        msg.attach(payload)
                        ind = 0

def index():
    mycursor.execute("select id from recent_details order by id DESC LIMIT 1;")
    val3 = mycursor.fetchall()

    if val3 == []:
        messagebox.showerror(title = "WARNING" , message = "No Record Found In Database")
    elif val3 != []:
        index = val3[0][0]+1
    else:
        messagebox.showerror(title = "WARNING" , message = "SOMETHING WENT WRONG!")

    sql1 = "INSERT INTO recent_details(id , sent_to) VALUES (%s , %s)"
    val2 = (index , "")
    mycursor.execute(sql1, val2)
    bulk_DB.commit()

def recent_details():
    current_time = datetime.now()
    time = current_time.strftime("%H:%M:%S")
    mycursor.execute("select * from login_logout;")
    mail_address = mycursor.fetchall()
    mycursor.execute(f"select * from email_pass where email_2='{mail_address[0][0]}';")
    email_address=mycursor.fetchall()
    if email_address is None:
        messagebox.showerror(title = "SOMETHING WENT WRONG" , message = "Couldn't Found Admin Details")
    elif email_address is not None:
        sql3 = "SELECT id FROM recent_details"
        mycursor.execute(sql3)
        val3 = mycursor.fetchall()
        for i in range(len(email_list)):     
            if val3 == []:
                val1 = ("1" , email_address[0][2] ,email_address[0][0], current_time  , time , email_list[i])
            elif val3 is not None:
                length = len(val3)
                if length == 0:
                    val1 = ("1" , sender_email , current_time  , time , email_list[i])
                else:
                    index = val3[length - 1][0]
                    val1 = (index ,email_address[0][2] ,email_address[0][0], current_time  , time , email_list[i])
            else:
                messagebox.showerror(title = "WARNING" , message = "SOMETHING WENT WRONG!")
            sql1 = "INSERT INTO recent_details(id, account_1, admin_email , date , time , sent_to) VALUES (%s , %s, %s , %s , %s , %s)"
            mycursor.execute(sql1 , val1)
            bulk_DB.commit()
    else:
        messagebox.showerror(title = "WARNING" , message = "SOMETHING WENT WRONG!")
        
def next():
    count_1 = 0
    em = ''
    name = obj.e.get()
    if " " in name:
        list_1 = name.split(" ")
    elif "," in name:
        list_1 = name.split(",")
    elif "/" in name:
        list_1 = name.split("/")
    else:
        list_1= name.split()
    for i in range(len(list_1)):
        if list_1[i].endswith("@gmail.com") or list_1[i].endswith("@GMAIL.COM"):
            name_list.append(list_1[i])
            name_list1.append(list_1[i])
        else:
            count_1+=1
            em+=str(i+1)+","
    if count_1==0:
        messagebox.showinfo(title="STATUS", message=f"Click Finish To Move Ahead!")
        obj.e.delete(0, "end")
    else:
        messagebox.showinfo(title="STATUS", message=f"{count_1} emails are invailid {em}")


def finish():
    mycursor.execute("SELECT * FROM login_logout;")
    fetch = mycursor.fetchall()
    mycursor.execute(f"select * from email_pass where email_2 = '{fetch[0][0]}';")
    fetch = mycursor.fetchall()
    try:
        for i in range(len(name_list)):   
            sql = "INSERT INTO bulkemail_entermanually(id , email_list , date , time) VALUES (%s , %s , %s , %s)"
            id1 = i+1
            current_time = datetime.now()
            time = current_time.strftime("%H:%M:%S")
            val = (id1 , name_list[i] , current_time , time)
            mycursor.execute(sql , val)
            bulk_DB.commit()
            sql3 = "SELECT id FROM recent_details order by id DESC LIMIT 1;"
            mycursor.execute(sql3)
            val3 = mycursor.fetchall()     
            if val3 == []:
                val1 = (1 , fetch[0][2], fetch[0][0], current_time  , time , name_list[i])
            elif val3 != []:
                index = val3[0][0]+1
                val1 = (index , fetch[0][2], fetch[0][0], current_time  , time , name_list[i])
            else:
                messagebox.showerror(title = "WARNING" , message = "SOMETHING WENT WRONG!")
            sql1 = "INSERT INTO recent_details(id, account_1, admin_email , date , time , sent_to) VALUES (%s , %s, %s, %s , %s , %s)"
            mycursor.execute(sql1 , val1)
            bulk_DB.commit()
    except:
        messagebox.showerror(title="FINISH ERROR", message='SOMETHING WRONG IN FINISH')
    else:
        messagebox.showinfo(title="DONE", message="ALL SET TO GO!!!")
        obj.btn['state']='disabled'
        obj.finish_func['state']='disabled'
        obj.e['state']='disabled'
    name_list[:] = []

# manually send email
def send():
    def send_manually():
        mycursor.execute("select * from login_logout;")
        a=mycursor.fetchall()
        mycursor.execute(f"select * from email_pass where email_2='{a[0][0]}';")
        mail=mycursor.fetchall()
        server = "smtp.gmail.com"
        port = 465
        message = obj.msg_text.get("1.0" , 'end')
                
        msg['From'] = mail[0][0]
        msg['To'] = ','.join(name_list1)
        msg['Subject'] = (obj.subject_entry.get())
        if (len(obj.subject_entry.get()) > 50):
            messagebox.showerror(title = "Something Went Wrong!" , message = "Subject Length is Exceeded!\nPlease Try to Edit Subject within 40 Characters!")
            return
        else:
            pass
        
        msg.attach(MIMEText(message , 'plain'))
                
        text = msg.as_string()
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(server , port , context=context) as Server:
            Server.login(mail[0][0], mail[0][1])
            answer = messagebox.askyesno(title = "Status" , message = "Are You Sure? ")
            if (answer == True):
                pass
            else:
                return
            Server.sendmail(mail[0][0] , name_list1 , text)
            obj.send['state'] = 'disabled'
            messagebox.showinfo(title = "STATUS" , message = "Email Sent Successfully!")
            index()
    if isconnect()==True:
        check = if_spam_manually()
        if (check == True):
            ayn = messagebox.askyesno(title = "Spam Checker" , message = "This message is going to Spam!\nDo You Want to Continue?")
            if (ayn == True):
                send_manually()
            else:
               message = obj.msg_text.get("1.0" , 'end') 
        else:
            send_manually()            
    else:
        messagebox.showeinfo(title="INTERNET CHECK", message="PLEASE CHECK INTERNET CONNECTION")
        

def check_spam(text):
    ps=PorterStemmer()
    vector=pickle.load(open("C:\\Users\\acer\\Desktop\\ML-Projects\\spam classifier\\vectorizer.pkl","rb"))
    model=pickle.load(open("C:\\Users\\acer\\Desktop\\ML-Projects\\spam classifier\\model.pkl","rb"))

    inp_msg=text

    def clean_masg(masg):
        masg=masg.lower()
        text=nltk.word_tokenize(masg)
        clean_masg=[]
        for word in text:
            if word.isalnum():
              clean_masg.append(word)
        masg=clean_masg[:]
        clean_masg.clear()
        for word in masg:
            if word not in stopwords.words('english') and word not in string.punctuation:
                clean_masg.append(word)
        masg=clean_masg[:]
        clean_masg.clear()
        for word in masg:
            clean_masg.append(ps.stem(word))
            
                
        return " ".join(clean_masg)

    cleaned_msg=clean_masg(inp_msg)
    vectorise=vector.transform([cleaned_msg])

    result=model.predict(vectorise)[0]
    return result


global email_address
email_address = []

# csvupload send mail
def send_msg():
    global message
    if isconnect()==True:
        mycursor.execute("select * from login_logout;")
        a=mycursor.fetchall()
        mycursor.execute(f"select * from email_pass where email_2='{a[0][0]}';")
        mail=mycursor.fetchall()
        
        message = obj.enter_msg_text.get('1.0', 'end')
        sentSuccess = False

        if mail == []:
            messagebox.showerror(title = "SOMETHING WENT WRONG" , message = "Couldn't Found Admin Details")
        elif mail != []:
            server = "smtp.gmail.com"
            port = 465

            msg['From'] = mail[0][0]
            msg['To'] = ','.join(email_list)
            msg['Subject'] = (obj.enter_subject_entry.get())
            if (len(obj.enter_subject_entry.get()) > 50):
                messagebox.showerror(title = "Something Went Wrong!" , message = "Subject Length is Exceeded!\nPlease Try to Edit Subject within 40 Characters!")
                return
            else:
                pass
            msg.attach(MIMEText(message , 'plain'))
            check = if_spam()
            
            if (check == True):
                ayn = messagebox.askyesno(title = "Spam Checker" , message = "This message is going to Spam!\nDo You Want to Continue?")
                if (ayn == True):
                    pass
                else:
                    message = obj.enter_msg_text.get('1.0', 'end')
                    return
            else:
                pass

            text = msg.as_string()
            refused = {}
            # Create a SSL context
            context = ssl.create_default_context()
            # Login and Send Email
            with smtplib.SMTP_SSL(server, port, context=context) as Server:

    # old unchanged
                Server.login(mail[0][0], mail[0][1])
                answer = messagebox.askyesno(title = "Status" , message = "Are You Sure? ")
                if (answer == True):
                    pass
                else:
                    return
                               
                
                Server.sendmail(mail[0][0], email_list, text)
                obj.send_btn['state'] = 'disabled'
                #obj.enter_subject_entry.delete('1.0' , 'end')
                #obj.enter_msg_text.delete('1.0' , 'end')
                
                ask_msgbox = messagebox.askyesno(title = "STATUS" , message = "Email Sent Successfully!\nWould You Like To View The Visualisation of Success Rate!")
                if (ask_msgbox == True):
                    visual(len_actual_mail,len_wrong_mail)
                else:
                    pass
            index()
            recent_details()
        else:
            messagebox.showerror(title = "WARNING" , message = "SOMETHING WENT WRONG!")
    else:
        messagebox.showinfo(title="INTERNET CHECK", message="PLEASE CHECK INTERNET CONNECTION")


def if_spam():
    global message
    message = obj.enter_msg_text.get('1.0', 'end')
    result=check_spam(message)
    if result==1:
        #tk.messagebox.showerror("Spam Checker",  "This is a Spam message")
        return True
    else:
        #tk.messagebox.showinfo("Spam Checker",  "This is a Non-Spam message")
        return False

def if_spam_manually():
    global message
    message = obj.msg_text.get('1.0', 'end')
    result=check_spam(message)
    if result==1:
        #tk.messagebox.showerror("Spam Checker",  "This is a Spam message")
        return True
    else:
        #tk.messagebox.showinfo("Spam Checker",  "This is a Non-Spam message")
        return False

def time_pick():
    # import tkinter as tk
    from tktimepicker import AnalogPicker, AnalogThemes
    # note: you can also make use of mouse wheel or keyboard to scroll or enter the spin timepicker
    root = tk.Tk()
    root.geometry('310x350')

    def schedule(time):
        ask_schedule = messagebox.askyesno(title = "Confirmation" , message = f"Schedule Mail at {time}")
        if (ask_schedule == True):
            hour = time[0]
            min = time[1]
            sec = time[2]

            print(hour)
            print(min)
            print(sec)
            root.destroy()
        else:
            root.focus_force()


    time_picker = AnalogPicker(root)
    time_picker.pack(fill="x")
    time_picker.place(height = 300 , width = 310 , x = 0 , y = 0)
    # print(time_picker.time())
    # schedule(time_picker.time())

    select_time = tk.Button(root , text = "Schedule" , command = lambda : schedule(time_picker.time()))
    select_time.place(width = 100 , x = 100 , y = 310)
    theme = AnalogThemes(time_picker)
    theme.setDracula()
    
    root.mainloop()


# def voice_recognition():
#     pass
    
def show_email():
    obj.text_box.configure(state = "normal")
    sql = "SELECT email_list FROM bulkemail_entermanually"
    mycursor.execute(sql)
    list_2 = mycursor.fetchall()
    # print(list_2) 
    if (list_2 != []):
        for i in range(len(list_2)):
            for j in range(len(list_2[i])):
                # print(i ,j)
                if i<10:
                    obj.text_box.insert(END , i+1 )
                    obj.text_box.insert(END , "  |\t\t")
                    obj.text_box.insert(END , list_2[i][j])
                    obj.text_box.insert(END , "\n")


                else:
                    obj.text_box.insert(END , i+1)
                    obj.text_box.insert(END , " |\t\t")
                    obj.text_box.insert(END , list_2[i])
                    obj.text_box.insert(END , "\n")
                obj.text_box.insert(END , "   |\t\t\n")
    else:
        messagebox.showwarning(title = "SOMETHING WENT WRONG!" , message = "No Mail Address Added!")
    obj.text_box.clipboard_clear()
    obj.text_box.configure(state="disabled")

def change_Email():
    e = obj.enter_key.get()
    e1 = obj.change_email.get()
    if "@gmail.com" not in e1 or len(e) == 0:
        if len(e) == 0 and len(e1) == 0:
            messagebox.showerror(title = "SOMETHING WENT WRONG" , message = "Please Enter Index of Email Address And New Email Address To Change Email Address!")
            # print("working")
        elif len(e) == 0:
            messagebox.showerror(title = "SOMETHING WENT WRONG" , message = "Please Enter New Email Address To Change!")
            # print("working1")
        elif len(e1) == 0:
            messagebox.showerror(title = "SOMETHING WENT WRONG" , message = "Please Enter Index of Email Address And New Email Address To Change Email Address!")
            # print("working1")
        else:
            messagebox.showerror(title = "SOMETHING WENT WRONG" , message = "Please Enter Valid Email Address")
    else:
        # a=int(enter_key.get())
        # b=change_email.get()
        # list_2[e]=e1
        key = int(e)
        # print("show")
        sql = "UPDATE bulkemail_entermanually SET email_list = %s WHERE id = %s"
        val = (e1 , key)
        try:
            mycursor.execute(sql , val)
            bulk_DB.commit()
        except:
            messagebox.showerror(title="ERROR",message="COULD NOT ABLE TO CHANGE!!!")
        else:
            messagebox.showinfo(title="SUCCESS",message="DONE")
            
        obj.show_frame.focus_force()

def refresh():
    obj.text_box.configure(state = "normal")
    obj.text_box.delete('1.0' , 'end')
    show_email()

def sms_csv_upload():
    pass

def schedule_sms():
    pass

def open_frame():
    pass

def contact_us():
    pass

def documentation1():
    pass

def tutorial_watchout():
    pass

def voice_recognition():
    
    # lang = voice_helper(id_voice())
    lang = ""
    obj.lang_choosen.place(height = 30 , width = 80 , x = 775 , y = 430)
    # lang_choosen.current(0)
    

    # lan = input("Enter language to Recognize:").lower()
    # lan1 = messagebox.QUESTION("hindi or english")
    # class custom_messagebox():
    #     root_frame = tk.Tk()
    #     root_frame.geometry('300x150')
    #     root_frame.title("SELECT AN OPTION")

    #     label = tk.Label(root_frame , text = "Please Select a Language!" , background="white")
    #     label.place(x=80 , y=20)
    #     eng = tk.Button(root_frame , text = "ENGLISH" , background="#b90ee3" )
    #     eng.place(width = 80 , x=60 , y = 100)
    #     hin = tk.Button(root_frame , text = "HINDI" , background="#b90ee3" )
    #     hin.place(width = 80 , x=160 , y = 100)

    #     root_frame.mainloop()

    lang_input = (obj.lang_choosen.get()).lower()
    if (lang_input == "english"):
        # print("English")
        lan = "english"
    elif (lang_input == "hindi"):
        # print("Hindi")
        lan = "hindi"
    else:
        lan = "language"
        # voice_recognition()


    languages = ['en-Us' , 'hi-IN']
    if (lan == "english"):
        lang = languages[0]
    elif (lan == "hindi"):
        lang = languages[1]
    # elif (lan == "language"):
    #     lang = "language"
    #     messagebox.showerror(title = "SOMETHING WENT WRONG!" , message = "Select A language First!")
    # else:
        # messagebox.showerror(title = "SOMETHING WENT WRONG!" , message = "Language not Supported!")
    if (lang == "en-Us" or lang == "hi-IN"):
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                obj.voice_rec_btn.config(background="green")
                # print('Clearing background noise..')
                recognizer.adjust_for_ambient_noise(source,duration=1)
                # print("waiting for your message...")
                # recordedaudio = ""
                # while(recordedaudio == "stop"):
                recordedaudio=recognizer.listen(source)
                print('Done recording..!')
                # print(recordedaudio)
            try:
                print('Printing the message..')
                text=recognizer.recognize_google(recordedaudio,language = lang)
                # print('Your message:{}'.format(text))
                obj.enter_msg_text.insert(END , f" {text}")
                # voice_rec_btn.config(background = "purple")
                # messagebox.showinfo(title = "Message" , message = text)
                    # return text
                # lang_choosen.place_forget()
                
            except Exception as ex:
                messagebox.showerror(title = "Something Went Wrong!" , message = f"Error occurred: {ex} ")
            finally:
                obj.voice_rec_btn.config(background = "purple")

                obj.lang_choosen.place_forget()

    elif (lang == "language"):
        messagebox.showwarning(title = "Something Went Wrong!" , message = "Please Select a Language!")
    
    obj.lang_choosen.pack_forget()

def voice_recognition_manually():
    
    lang = ""
    obj.lang1_choosen.place(height = 30 , width = 80 , x = 775 , y = 430)
    lang_input = (obj.lang1_choosen.get()).lower()
    if (lang_input == "english"):
        # print("English")
        lan = "english"
    elif (lang_input == "hindi"):
        # print("Hindi")
        lan = "hindi"
    else:
        lan = "language"
        # voice_recognition()


    languages = ['en-Us' , 'hi-IN']
    if (lan == "english"):
        lang = languages[0]
    elif (lan == "hindi"):
        lang = languages[1]
    if (lang == "en-Us" or lang == "hi-IN"):
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                obj.voice_rec_btn.config(background="green")
                recognizer.adjust_for_ambient_noise(source,duration=1)
                recordedaudio=recognizer.listen(source)
                print('Done recording..!')
                # print(recordedaudio)
            try:
                print('Printing the message..')
                text=recognizer.recognize_google(recordedaudio,language = lang)
                # print('Your message:{}'.format(text))
                obj.msg_text.insert(END , f" {text}")
            except Exception as ex:
                messagebox.showerror(title = "Something Went Wrong!" , message = f"Error occurred: {ex} ")
            finally:
                obj.voice_rec_btn.config(background = "purple")

                obj.lang1_choosen.place_forget()

    elif (lang == "language"):
        messagebox.showwarning(title = "Something Went Wrong!" , message = "Please Select a Language!")
    
    obj.lang1_choosen.pack_forget()

def admin_access():
    mycursor.execute("select * from recent_details;")
    history=mycursor.fetchall()
    if (history == []):
        messagebox.showinfo(title = "STATUS" , message = "No Record Found In Database!")
    else:
        for i in range (len(history)):
            obj.tree.insert('' , 'end' , values = (history[i][0] , history[i][1] , history[i][2] , history[i][3] , history[i][4] , history[i][5]))
            obj.tree.insert('' , 'end' , values = ())

def clear_history():
    ask = messagebox.askyesno(title = "STATUS" , message = "Are You Sure You Want To Clear All Records ?")
    if ask == 1:
        mycursor.execute("truncate recent_details;")
        bulk_DB.commit()
    elif ask == 0:
        pass
    else:
        messagebox.showerror(title = "WARNING" , message = "Something Went Wrong!")

def user_history():
    mycursor.execute("select * from login_logout;")
    m = mycursor.fetchall()
    mycursor.execute(f"select * from recent_details where account_1='{m[0][0]}'")
    user = mycursor.fetchall()

def close_login():
    exit = messagebox.askyesno(title="EXIT?", message="Do you want to EXIT?")
    if exit==True:
        mycursor.execute("truncate login_logout;")
        bulk_DB.commit()
        obj.login_frame.destroy()
    else:
        pass

def close_signup():
    exit = messagebox.askyesno(title="EXIT?", message="Do you want to EXIT?")
    if exit==True:
        mycursor.execute("truncate login_logout;")
        bulk_DB.commit()
        obj.signup_frame.destroy()
    else:
        pass

def close_home():
    exit = messagebox.askyesno(title="EXIT?", message="Do you want to EXIT?")
    if exit==True:
        mycursor.execute("truncate login_logout;")
        bulk_DB.commit()
        obj.home_frame.destroy()
    else:
        pass

def close_csv():
    exit = messagebox.askyesno(title="EXIT?", message="Do you want to EXIT?")
    if exit==True:
        mycursor.execute("truncate bulkemail_csvupload;")
        bulk_DB.commit()
        mycursor.execute("truncate bulkemail_attachment;")
        bulk_DB.commit()
        mycursor.execute("truncate login_logout;")
        bulk_DB.commit()
        obj.csvupload_frame.destroy()
    else:
        pass

def close_manually():
    exit = messagebox.askyesno(title="EXIT?", message="Do you want to EXIT?")
    if exit==True:
        mycursor.execute("truncate bulkemail_entermanually;")
        bulk_DB.commit()
        mycursor.execute("truncate login_logout;")
        bulk_DB.commit()
        mycursor.execute("truncate bulkemail_attachment;")
        bulk_DB.commit()
        obj.entermanually_frame.destroy()
    else:
        pass

def close_schedule():
    exit = messagebox.askyesno(title="EXIT?", message="Do you want to EXIT?")
    if exit==True:
        mycursor.execute("truncate login_logout;")
        bulk_DB.commit()
        obj.scheduling_frame.destroy()
    else:
        pass

def close_show():
    exit = messagebox.askyesno(title="EXIT?", message="Do you want to EXIT?")
    if exit==True:
        mycursor.execute("truncate login_logout;")
        bulk_DB.commit()
        obj.show_frame.destroy()
    else:
        pass
    
def close_contact():
    exit = messagebox.askyesno(title="EXIT?", message="Do you want to EXIT?")
    if exit==True:
        obj.contact_frame.destroy()
    else:
        pass

def close_about():
    exit = messagebox.askyesno(title="EXIT?", message="Do you want to EXIT?")
    if exit==True:
        obj.about_frame.destroy()
    else:
        pass

def clear_history():
    ask = messagebox.askyesno(title = "STATUS" , message = "Are You Sure You Want To Clear All Records ?")
    if ask == 1:
        mycursor.execute("truncate recent_details;")
        bulk_DB.commit()
    elif ask == 0:
        pass
    else:
        messagebox.showerror(title = "WARNING" , message = "Something Went Wrong!")
        
def user_access():
    mycursor.execute("select * from login_logout;")
    a1=mycursor.fetchall()
    mycursor.execute(f"select * from recent_details where account_1='{a1[0][0]}';")
    history=mycursor.fetchall()
    if (history == []):
        messagebox.showinfo(title = "STATUS" , message = "No Record Found In Database!")
        
    else:
        for i in range (len(history)):
            obj.tree.insert('' , 'end' , values = (history[i][0] , history[i][1] , history[i][2] , history[i][3] , history[i][4] , history[i][5]))
            obj.tree.insert('' , 'end' , values = ())

def admin_access():
    mycursor.execute("select * from recent_details;")
    history=mycursor.fetchall()
    if (history == []):
        messagebox.showinfo(title = "STATUS" , message = "No Record Found In Database!")
    else:
        for i in range (len(history)):
            obj.tree.insert('' , 'end' , values = (history[i][0] , history[i][1] , history[i][2] , history[i][3] , history[i][4] , history[i][5]))
            obj.tree.insert('' , 'end' , values = ())
            
def admin_page():
    def admin():
        if for_admin.get()=='BULK100':
            root.destroy()
            obj.home_frame.destroy()
            obj.admin_page_1()
        else:
            root.destroy()
            messagebox.showinfo(title="ACCESS DENY", message='ADMIN ID IS WRONG')

    root = Tk()
    root.geometry("400x200")
    root.title("ADMIN ID")

    lable1 = Label(root, text="Enter Admin ID : ", fg="black", bg="white", font=("Helvetica", 10))
    lable1.place(x=20, y=40)

    for_admin = tk.Entry(root , bd = 2 , fg = "black" , highlightthickness= 1 , highlightbackground= "#884dff")
    for_admin.place(width = 240 , x=20 , y=70)

    submit = tk.Button(root , text = "SUBMIT" , bd = 1 , highlightthickness= 1 , highlightbackground= "#110033" , background = "#aa80ff", command=admin)
    submit.place(width = 100 , x=20 , y=100)

    root.resizable(False, False)
    root.mainloop()
    
def change_account():
    def change_detail():
        mycursor.execute("select * from login_logout;")
        me = mycursor.fetchall()
        
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_add_1.get(), email_pass.get())
        except:
            messagebox.showerror(title="ERROR", message="INFORMATION IS NOT CORRECT")

        else:
            try:
                mycursor.execute(f"UPDATE email_pass SET email_address = '{email_add_1.get()}', email_password = '{email_pass.get()}' WHERE email_2 = '{me[0][0]}';")
                bulk_DB.commit()
            except:
                messagebox.showinfo(title="INFORMATION", message="COULDN'T ABLE T0 CHANGE!!!")
            else:
                messagebox.showinfo(title="SUCCESS", message="ACCOUNT CHANGED SUCCESSFULLY")
                root4.destroy()

    root4 = Tk()
    root4.geometry("400x200")
    root4.title("WELCOME TO BULK CLIENT")

    email_add = Label(root4, text="Enter email : ", fg="black", bg="white", font=("Helvetica", 10))
    email_add.place(x=20, y=20)

    email_add_1 = tk.Entry(root4 , bd = 2 , fg = "black" , highlightthickness= 1 , highlightbackground= "#884dff")
    email_add_1.place(width = 240 , x=20 , y=50)

    email_pas = Label(root4, text="Enter 2 step verification password : ", fg="black", bg="white", font=("Helvetica", 10))
    email_pas.place(x=20, y=85)

    email_pass=tk.Entry(root4 , bd = 2 , fg = "black" , highlightthickness= 1 , highlightbackground= "#884dff")
    email_pass.place(width = 240, x=20, y=115)

    submit_2 = tk.Button(root4 , text = "SUBMIT" , bd = 1 , highlightthickness= 1 , highlightbackground= "#110033" , background = "#aa80ff", command=change_detail)
    submit_2.place(width = 100 , x=20 , y=150)

    root4.resizable(False, False)
    root4.mainloop()

class Bulk_Client:

    # method for show password for login page
    def show_password(self):
        if (self.enter_password_entry.cget('show') == '*'):
            self.enter_password_entry.config(show = '')
        else:
            self.enter_password_entry.config(show = "*")
    
    # method for login page interface
    def login_page(self):
        self.login_frame=tk.Tk()
        self.login_frame.geometry("1000x600")
        self.login_frame.title("LOGIN")
        self.login_frame.configure(bg="#9f3ae7")
        self.canvas = Canvas(
            self.login_frame,
            bg = "#9f3ae7",
            height = 600,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        self.canvas.place(x = 0, y = 0)
        self.background_img = PhotoImage(file = "background.png")
        self.background = self.canvas.create_image(
            500.0, 300.0,
            image=self.background_img)
        self.login_frame.focus_force()
        self.login_frame.pack_propagate(0)

        self.enter_email_entry = tk.Entry(self.login_frame , bd = 2 , fg = "black" , highlightthickness= 1 , highlightbackground= "#884dff")
        self.enter_email_entry.place(width = 200 , x=560 , y=272)

        self.enter_password_entry = tk.Entry(self.login_frame , bd = 2 , fg = "black" , highlightthickness= 1 , highlightbackground= "#884dff" , show = "*")
        self.enter_password_entry.place(width = 200 , x=560 , y=368)

        self.check_button = tk.Checkbutton(self.login_frame , text = "Show Password", command=obj.show_password)
        self.check_button.place(width = 100 , x = 560 , y = 392)

        self.forget = tk.Button(self.login_frame, text = "Forgot password?",font=("Helvetica", 10, "bold"), border=0, bg="white", fg="#57a1f8" , command = forget_password)
        self.forget.place( x=680, y=392)

        self.login = tk.Button(self.login_frame , text = "LOGIN" , bd = 1 , highlightthickness= 1 , highlightbackground= "#110033" , background = "#aa80ff", command=login)
        self.login.place(width = 60 , x=630 , y=440)


        self.lebal1 = tk.Label(self.login_frame, text="Create an accout ?",fg="black", bg="white", font=("Helvetica", 10))
        self.lebal1.place(x=585, y=470)

        self.signup = tk.Button(self.login_frame , text = "Sign up",font=("Helvetica", 10, "bold"), border=0, bg="white", fg="#57a1f8", command=obj.sign_switch)
        self.signup.place(x=700, y=468)

        self.login_frame.protocol('WM_DELETE_WINDOW' , close_login)
        self.login_frame.resizable(False, False)
        self.login_frame.mainloop(0)

    def admin_page(self):
        self.admin_frame = tk.Tk()
        self.admin_frame.geometry('1000x600')
        self.admin_frame.config(bg = "#9f3ae7")
        self.admin_frame.title("Recent Activity")
        self.admin_frame.focus_force()
        self.admin_frame.pack_propagate(1)

        self.canvas = Canvas(
            self.admin_frame,
            bg = "#9f3ae7",
            height = 600,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        self.canvas.place(x = 0, y = 0)

        self.background_img = tk.PhotoImage(file = f"background_recentdetails.png")
        self.background = self.canvas.create_image(
            500.0, 300.0,
            image=self.background_img)

        self.columns = ('id' , 'Sender_Email' , 'Admin_Email' , 'Date' , 'Time' , 'Sent_To')
        self.tree = ttk.Treeview(self.admin_frame , columns = self.columns , show = "headings")
        self.tree.place(height = 322 , width = 585 , x=332 , y=122)
        self.tree.column('id' , anchor = "center" , width = 70)
        self.tree.column('Sender_Email' , anchor = "center" , width = 120)
        self.tree.column('Admin_Email' , anchor = "center", width = 120)
        self.tree.column('Date' , anchor = "center", width = 60)
        self.tree.column('Time' , anchor = "center", width = 60)
        self.tree.column('Sent_To' , anchor = "center", width = 120)


        self.label = tk.Label(self.admin_frame , text = "Recent_Details" , background = "white" , font = ("Algerian" , "42") , anchor = "center")
        self.label.place(height = 50 , width = 460 , x=400 , y=55)
        self.clear_history = tk.Button(self.admin_frame , text = "Clear History" , command = clear_history , background = "#b90ee3" , bd = 2)
        self.clear_history.place(width = 100 , x=440 , y=480)
        self.back = tk.Button(self.admin_frame , text = "Back" , command = obj.admin_to_home, background = "#b90ee3" , bd = 2)
        self.back.place(width = 100 , x=570 , y=480)
        self.show_history = tk.Button(self.admin_frame , text = "Show History" , command = admin_access , background = "#b90ee3" , bd = 2)
        self.show_history.place(width = 100 , x=700 , y=480)
        self.tree.heading('id' , text = "Record_Id")
        self.tree.heading('Sender_Email' , text = "Sender_Email")
        self.tree.heading('Admin_Email' , text = "Admin_Email")
        self.tree.heading('Date' , text = "Date")
        self.tree.heading('Time' , text = "Time")
        self.tree.heading('Sent_To' , text = "Sent_To")

        # show_details = tk.Text(frame , background = "pink" , foreground = "red")
        # show_details.place(height=200 , width=800 , x=100 , y=150)

        self.admin_frame.resizable(False, False)
        self.admin_frame.mainloop()
    # method for show password register page
    def show_password_1(self):
        if (self.enter_password.cget('show') == '*'):
            self.enter_password.config(show = '')
        else:
            self.enter_password.config(show = "*")
        if (self.confirm_pass.cget('show') == '*'):
            self.confirm_pass.config(show = '')
        else:
            self.confirm_pass.config(show = "*")

    # Method for sign up page intrerface
    def signup_page(self):

        self.signup_frame = tk.Tk()

        self.signup_frame.geometry("1000x600")
        self.signup_frame.title("Admin Details")
        self.signup_frame.configure(bg = "#9f3ae7")

        self.canvas = Canvas(
            self.signup_frame,
            bg = "#9f3ae7",
            height = 600,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        self.canvas.place(x = 0, y = 0)

        self.background_img = PhotoImage(file = f"background_signup1.png")
        self.background = self.canvas.create_image(
            500.0, 300.0,
            image=self.background_img)

        self.signup_frame.focus_force()
        self.signup_frame.pack_propagate(0)


        self.enter_admin_name = tk.Entry(self.signup_frame , bd = 2 , fg = "black" , highlightthickness= 1 , highlightbackground= "#884dff")
        self.enter_admin_name.place(width = 240 , x=558 , y=260)

        self.enter_email = tk.Entry(self.signup_frame , bd = 2 , fg = "black" , highlightthickness= 1 , highlightbackground= "#884dff")
        self.enter_email.place(width = 240 , x=558 , y=315)

        self.enter_contact_number = tk.Entry(self.signup_frame , bd = 2 , fg = "black" , highlightthickness= 1 , highlightbackground= "#884dff")
        self.enter_contact_number.place(width = 240 , x=558 , y=372)

        self.enter_password = tk.Entry(self.signup_frame , bd = 2 , fg = "black" , highlightthickness= 1 , highlightbackground= "#884dff" , show = "*")
        self.enter_password.place(width = 240 , x=558 , y=430)

        self.check_button = tk.Checkbutton(self.signup_frame , text = "Show Password" , activeforeground="purple" , command = obj.show_password_1)
        self.check_button.place(width = 100 , x = 685 , y = 515)

        self.register = tk.Button(self.signup_frame , text = "REGISTER" , bd = 1 , highlightthickness= 1 , highlightbackground= "#110033" , background = "#aa80ff", command=register_client)
        self.register.place(width = 100 , x=575, y=515)

        self.lebal1 = tk.Label(self.signup_frame, text="Already have an account?",fg="black", bg="white", font=("Helvetica", 10))
        self.lebal1.place(x=170, y=500)

        self.signin = tk.Button(self.signup_frame , text = "Sign in",font=("Helvetica", 10, "bold"), border=0, bg="white", fg="#57a1f8", command = obj.login_switch)
        self.signin.place(x=310, y=500)
        
        self.confirm_pass = tk.Entry(self.signup_frame , bd = 2 , fg = "black" , background = "white" , highlightthickness = 1 , highlightbackground = "#884dff" , show = "*")
        self.confirm_pass.place(width=240,x=558, y=482)

        self.signup_frame.protocol('WM_DELETE_WINDOW' , close_signup)
        self.signup_frame.resizable(False, False)
        self.signup_frame.mainloop()

    # Method for home page
    def home_page(self):
        self.home_frame = tk.Tk()
        self.home_frame.geometry("1000x600")
        self.home_frame.title("Email Sender ")
        self.home_frame.config(bg = "#9f3ae7")
        self.home_frame.focus_force()
        self.home_frame.pack_propagate(0)

        self.canvas = Canvas(
            self.home_frame,
            bg = "#9f3ae7",
            height = 600,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        self.canvas.place(x = 0, y = 0)

        self.background_img = tk.PhotoImage(file = f"background_emailmainframe.png")
        self.background = self.canvas.create_image(
            500.0, 300.0,
            image=self.background_img)

        self.home_frame.option_add('*tearOff', False)
        self.menubar = tk.Menu(self.home_frame)

        self.home_frame['menu'] = self.menubar

        # Create the pull down menu's on menu bar
        self.email = tk.Menu(self.menubar)
        self.menubar.add_cascade(menu = self.email , label = "Email")

        self.sms = tk.Menu(self.menubar)
        self.menubar.add_cascade(menu = self.sms , label = "SMS")

        # Creating Menu Items for each menu bar
        self.email.add_command(label = "Upload File" , command = obj.csvupload_switch)
        self.email.add_command(label = "Manual Email Customisation" , command = obj.entermanually_switch)
        self.email.add_command(label = "Schedule Mail" , command = obj.schedulemail_switch)
        self.email.add_command(label = "Previous Records" , command = obj.previous_switch)

        # Creating menu items for sms bar
        self.sms.add_command(label = "Upload CSV File" , command = sms_csv_upload)
        self.sms.add_command(label = "Schedule SMS" , command = schedule_sms)


        self.about = tk.Button(self.home_frame , text = "ABOUT US" ,font = ("Times New Roman" , 10 , "bold") , bd = 0 , background = "white" , activebackground="#B946F2"  , command = obj.about_page_switch)
        self.about.place(width = 100 , x=490 , y=60)

        self.contact = tk.Button(self.home_frame , text = "ADMIN" ,font = ("Times New Roman" , 10 , "bold") , bd = 0 , background = "white" , activebackground="#B946F2"  , command = admin_page)
        self.contact.place(width = 100 , x=555 , y=60)
        
        self.contact = tk.Button(self.home_frame , text = "CHANGE" ,font = ("Times New Roman" , 10 , "bold") , bd = 0 , background = "white" , activebackground="#B946F2"  , command = change_account)
        self.contact.place(width = 100 , x=630 , y=60)

        self.logout = tk.Button(self.home_frame , text = "LOGOUT" ,font = ("Times New Roman" , 10 , "bold") , bd = 0 , background = "white" , activebackground="#B946F2" , command = log_out)
        self.logout.place(width = 100 , x = 720 , y = 60)

        self.documentation = tk.Button(self.home_frame , text = "DOCUMENTATION" ,font = ("Times New Roman" , 10 , "bold") , bd = 0 , background = "white" , activebackground="#B946F2" , command = documentation1)
        self.documentation.place(width = 120 , x = 810 , y = 60)

        self.label = tk.Label(self.home_frame , text = "A paragraph is a self-contained unit of discourse in writing\n dealing with a particular point or idea.\n A paragraph consists of three or more sentences. \nThough not required by the syntax of\n any language, paragraphs are usually an expected part\n  of formal writing, used to organize longer prose\n" , background="white" , font = ("Times New Roman" , 12))
        self.label.place(height = 240 , width = 320 , x = 100 , y = 180)

        self.tutorial = tk.Button(self.home_frame , text = "WATCHOUT OUR TUTORIAL" ,font = ("Times New Roman" , 8 , "bold") , bd = 0 , background = "#B946F2" , activebackground="#B946F2" , command = tutorial_watchout)
        self.tutorial.place(height = 40 , width = 240 , x = 160 , y = 420)

        self.home_frame.protocol('WM_DELETE_WINDOW' , close_home)
        self.home_frame.resizable(False , False)
        self.home_frame.mainloop()

    #Method for csv upload page 
    def csvupload_page(self):
        self.csvupload_frame = tk.Tk()
        self.csvupload_frame.geometry('1000x600')
        self.background_photo = tk.PhotoImage(file = f"background_csvupload.png")
        self.csvupload_frame.config(bg = "#9f3ae7")
        self.csvupload_frame.title("Bulk Email Client")

        self.canvas = Canvas(
            self.csvupload_frame,
            bg = "#9f3ae7",
            height = 600,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        self.canvas.place(x = 0, y = 0)

        self.background_img = tk.PhotoImage(file = f"background_csvupload.png")
        self.background = self.canvas.create_image(
            500.0, 300.0,
            image=self.background_img)

        messagebox.showinfo(title="Important Message!", message='''   Please Note that The File You Are Selecting To Attach,\nShould Have the Email Addresses Column With Column \t\t\t\t  Heading as\n\t\t     "Emails"\n\t----------------------------------------------\n\n\t\tIf Already Done!\n\t            You Are All Set To Go ''')

        self.csvupload_frame.focus_force()
        self.csvupload_frame.pack_propagate(0)

        self.msg = MIMEMultipart()

        self.l = tk.Label(
        self.csvupload_frame, text="Attach Excel File To\n Import Email Addresses",font = ("Times New Roman" , 8 ))
        self.l.place(width=140, x=320, y=230)
        self.attach_file = tk.Button(self.csvupload_frame, text="Choose Files", bd=2, fg="black", background="#b90ee3" , command=attach_file)
        self.attach_file.place(width=140, x=320, y=310)

        self.enter_subject_label = tk.Label(self.csvupload_frame , text = "Enter\nSubject:" )
        self.enter_subject_label.place(width=50 , x=510 , y=160)
        self.enter_subject_entry = tk.Entry(self.csvupload_frame , bd=2 , bg = "#C5B4E3")
        self.enter_subject_entry.insert(0 , "Subject")
        self.enter_subject_entry.place(height=40 , width=350 , x=580 , y=160)
        self.enter_msg_label = tk.Label(self.csvupload_frame, text="Enter\nMessage")
        self.enter_msg_label.place(width=50, x=510, y=230)
        self.enter_msg_text = tk.Text(self.csvupload_frame, bd=2 , bg = "#C5B4E3")
        self.enter_msg_text.insert(END , "Message")
        self.enter_msg_text.place(height=200, width=350, x=580, y=230)
        self.voice_rec_photo = tk.PhotoImage(file = f"voice_rec.png")
        self.voice_rec_btn = tk.Button(self.csvupload_frame , background = "purple" , command = voice_recognition , image = self.voice_rec_photo , bd = 2 )
        self.voice_rec_btn.place(height = 30 , width = 30 , x = 860 , y = 430)
        self.pause_btn_photo = tk.PhotoImage(file = f"stop_btn1.png")
        # pause_btn = tk.Button(frame , background = "red" , image = pause_btn_photo , bd = 2)
        # pause_btn.place(height = 30 , width = 30 , x = 920 , y = 420)
        self.photo = tk.PhotoImage(file=f"attachment11.png")
        self.attach_file_btn = tk.Button(self.csvupload_frame, background="purple", image=self.photo , command=attach_attachment)
        self.attach_file_btn.place(height=30, width=30, x=897, y=430)
        self.send_btn = tk.Button(self.csvupload_frame, text="SEND", bd=2, command=send_msg , bg = "#b90ee3")
        self.send_btn.place(width=100, x=600, y=480)
        self.back_btn = tk.Button(self.csvupload_frame, text="BACK", bd=2, command=obj.csv_home_switch , bg = "#b90ee3")
        self.back_btn.place(width=100, x=750, y=480)
        #self.log_btn = tk.Button(self.csvupload_frame, text="Log Visualization", bd=2, command=ask , bg = "#b90ee3")
        #self.log_btn.place(width=100, x=340, y=450)
        
        self.n=tk.StringVar()
        self.lang_choosen = ttk.Combobox(self.csvupload_frame , height = 10 , width = 10 , textvariable=self.n , background="#b90ee3" , state = "readonly")
        self.lang_choosen['values'] = ('LANGUAGE' , 'ENGLISH' , 'HINDI')
        self.lang_choosen.place(x = 775 , y = 430)
        self.lang_choosen.current(0)
        self.lang_choosen.place_forget()


        self.csvupload_frame.protocol('WM_DELETE_WINDOW' , close_csv)
        self.csvupload_frame.resizable(False, False)
        self.csvupload_frame.mainloop()

        
    def enter_manually_page(self):
        self.entermanually_frame = tk.Tk()
        self.entermanually_frame.geometry('1000x600')
        self.entermanually_frame.config(bg = "#9f3ae7")
        self.entermanually_frame.title("Bulk Email Client")

        self.canvas = Canvas(
            self.entermanually_frame,
            bg = "#9f3ae7",
            height = 600,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        self.canvas.place(x = 0, y = 0)

        self.background_img = tk.PhotoImage(file = f"background_entermanually.png")
        self.background = self.canvas.create_image(
            500.0, 300.0,
            image=self.background_img)

        messagebox.showinfo(title = "Important Message!" , message = "Please Click Next After Entering Every Email Address ,\nAnd After Finished Entering Email Addresses Click Finish!\n-------------------------------------------------------------------------\n\t     Now, You Are All Set To Go!")
        self.entermanually_frame.focus_force()
        self.entermanually_frame.pack_propagate(0)

        self.l = tk.Label(self.entermanually_frame , text = "Enter Email Addresses Manually and \n Click 'NEXT' \n to Enter Next Email Address :" , background="white" , bd=0)
        self.l.place(width = 190 , x = 285 , y = 185)
        self.e = tk.Entry(self.entermanually_frame , bd=2 , background = "#C5B4E3")
        self.e.place(height = 50 , width = 190 , x=285 , y=250)
        self.btn = tk.Button(self.entermanually_frame , text = "NEXT" , bg = "#b90ee3" , command = next)
        self.btn.place(width = 80 , x = 295 , y = 335)
        self.finish_func = tk.Button(self.entermanually_frame , text = "FINISH" , bg = "#b90ee3" , command = finish)
        self.finish_func.place(width = 80 , x=380 , y=335)
        self.subject_label = tk.Label(self.entermanually_frame , text = "Enter \n Subject:")
        self.subject_label.place(width=50 , x=510 , y=160)
        self.subject_entry = tk.Entry(self.entermanually_frame , bd=2 , background = "#C5B4E3")
        self.subject_entry.place(height=40 , width=350 , x=580 , y=160)
        self.message_label = tk.Label(self.entermanually_frame , text = "Enter \n Message:")
        self.message_label.place(width=50 , x=510, y=230)
        self.msg_text = tk.Text(self.entermanually_frame , bd = 2, background = "#C5B4E3")
        self.msg_text.place(height=200, width=350, x=580, y=230)
        self.show = tk.Button(self.entermanually_frame , text = "Show Email Addresses" , bg = "#b90ee3" , command = obj.show_switch)
        self.show.place(width = 140 , x=310 , y=410)
        self.send = tk.Button(self.entermanually_frame , text = "SEND" , bg = "#b90ee3" , command = send)
        self.send.place(width=100, x=620, y=480)
        self.back = tk.Button(self.entermanually_frame , text = "BACK" , command = obj.manually_home , bg = "#b90ee3")
        self.back.place(width=100, x=750, y=480)
        self.photo = tk.PhotoImage(file = r"attachment11.png")
        self.add_attachment = tk.Button(self.entermanually_frame , text = "Add Attachment" , background="purple" ,  image = self.photo , command = attach_attachment)
        self.add_attachment.place(height=30, width=30, x=897, y=430)
        self.voice_rec_photo = tk.PhotoImage(file = f"voice_rec.png")
        self.voice_rec_btn = tk.Button(self.entermanually_frame , background = "purple" , command = voice_recognition_manually , image = self.voice_rec_photo , bd = 2 )
        self.voice_rec_btn.place(height = 30 , width = 30 , x = 860 , y = 430)

        self.n=tk.StringVar()
        self.lang1_choosen = ttk.Combobox(self.entermanually_frame , height = 10 , width = 10 , textvariable=self.n , background="#b90ee3" , state = "readonly")
        self.lang1_choosen['values'] = ('LANGUAGE' , 'ENGLISH' , 'HINDI')
        self.lang1_choosen.place(x = 775 , y = 430)
        self.lang1_choosen.current(0)
        self.lang1_choosen.place_forget()

        self.entermanually_frame.protocol("WM_DELETE_WINDOW" , close_manually)
        self.entermanually_frame.resizable(False, False)
        self.entermanually_frame.mainloop()
    
    def schedul_email_page(self):
        self.scheduling_frame = tk.Tk()
        self.scheduling_frame.geometry('1000x600')
        # background_photo = tk.PhotoImage(file = f"background_schedule.png")
        self.scheduling_frame.config(bg = "#9f3ae7")
        self.scheduling_frame.title("Bulk Email Client")

        self.canvas = Canvas(
            self.scheduling_frame,
            bg = "#9f3ae7",
            height = 600,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        self.canvas.place(x = 0, y = 0)

        self.background_img = tk.PhotoImage(file = f"background_schedule.png")
        self.background = self.canvas.create_image(
            500.0, 300.0,
            image=self.background_img)

        messagebox.showinfo(title="Important Message!", message='''   Please Note that The File You Are Selecting To Attach,\nShould Have the Email Addresses Column With Column \t\t\t\t  Heading as\n\t\t     "Emails"\n\t----------------------------------------------\n\n\t\tIf Already Done!\n\t            You Are All Set To Go ''')

        self.scheduling_frame.focus_force()
        self.scheduling_frame.pack_propagate(0)
        
        self.l = tk.Label(self.scheduling_frame, text="Attach Excel File\n To Import\n Email Addresses:", background="white")
        self.l.place(width=120, x=352, y=300)
        self.attach_file = tk.Button(self.scheduling_frame, text="Choose Files",bd=2, background="#b90ee3" , command=attach_file)
        self.attach_file.place(width=120, x=351, y=398)

        self.l2 = tk.Label(self.scheduling_frame, text="Set Time For \nScheduling:", background="white")
        self.l2.place(width=120, x=352, y=138)

        # scheduling button 
        self.select_timer = tk.Button(self.scheduling_frame , text = "Schedule Time" , background = "#b90ee3" , command = time_pick)
        self.select_timer.place(width=120, x=351, y=234)
        self.enter_subject_label = tk.Label(self.scheduling_frame , text = "Enter \nSubject")
        self.enter_subject_label.place(width=50 , x=510 , y=160)
        self.enter_subject_entry = tk.Entry(self.scheduling_frame , bd=2 , bg = "#C5B4E3")
        self.enter_subject_entry.insert(0 , "Subject")
        self.enter_subject_entry.place(height=40 , width=350 , x=580 , y=160)
        self.enter_msg_label = tk.Label(self.scheduling_frame, text="Enter \nMessage")
        self.enter_msg_label.place(width=50, x=510, y=230)
        self.enter_msg_text = tk.Text(self.scheduling_frame, bd=2 , background="#C5B4E3")
        self.enter_msg_text.insert(END , "Message")
        self.enter_msg_text.place(height=200, width=350, x=580, y=230)
        self.voice_rec_photo = tk.PhotoImage(file = f"voice_rec.png")
        self.voice_rec_btn = tk.Button(self.scheduling_frame , background = "purple" , command = voice_recognition , image = self.voice_rec_photo , bd = 2 )
        self.voice_rec_btn.place(height = 32 , width = 32 , x = 860 , y = 430)
        # pause_btn_photo = tk.PhotoImage(file = f"stop_btn1.png")
        # pause_btn = tk.Button(frame , background = "purple" , image = pause_btn_photo , bd = 2)
        # pause_btn.place(height = 30 , width = 30 , x = 920 , y = 420)
        self.photo = tk.PhotoImage(file=f"attachment11.png")
        self.attach_file_btn = tk.Button(self.scheduling_frame, background="#b90ee3",
                                    image=self.photo , command=attach_attachment)
        self.attach_file_btn.place(height=30, width=30, x=897, y=430)
        self.send_btn = tk.Button(self.scheduling_frame, text="SEND", bd=2, background = "#b90ee3" , command=send_msg)
        self.send_btn.place(width=100, x=620, y=480)
        self.back_btn = tk.Button(self.scheduling_frame, text="BACK", bd=2, background = "#b90ee3" , command=obj.scheduling_home_switch)
        self.back_btn.place(width=100, x=750, y=480)

        self.scheduling_frame.protocol('WM_DELETE_WINDOW' , close_schedule)
        self.scheduling_frame.resizable(False, False)
        self.scheduling_frame.mainloop()

    def show_page(self):
        self.show_frame = tk.Tk()
        self.show_frame.geometry('1000x600')
        # background_photo = tk.PhotoImage(file = f"background_schedule.png")
        self.show_frame.config(bg = "#9f3ae7")
        self.show_frame.title("Bulk Email Client")

        self.canvas = Canvas(
            self.show_frame,
            bg = "#9f3ae7",
            height = 600,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        self.canvas.place(x = 0, y = 0)

        self.background_img = tk.PhotoImage(file = f"show_email.png")
        self.background = self.canvas.create_image(
            500.0, 300.0,
            image=self.background_img)

        self.text_box = tk.Text(self.show_frame , bd = 2 , background = "#C5B4E3")
        self.text_box.place(height = 300 , width = 400 , x=75 , y=100)
        self.change = tk.Button(self.show_frame , text = "Change Email", bd = 3 , bg = "#b90ee3" , command = change_Email)
        self.change.place(height = 25 , width = 85 , x=550 , y=387)
        self.enter_key = tk.Entry(self.show_frame , bd=2 , highlightbackground="red" , background="#C5B4E3")
        self.enter_key.place(height = 30 , width = 180 , x=550 , y=210)
        self.l = tk.Label(self.show_frame , text = "Enter Index of List To Change:" , bd=2 , background="white")
        self.l.place(height = 30 , width = 170 , x=550 , y=180)
        self.l1 = tk.Label(self.show_frame , text = "Enter New Email Address:" , background="white")
        self.l1.place(height = 30 , width = 150 , x=550 , y=260)
        self.change_email = tk.Entry(self.show_frame , bd=2 , highlightbackground="red" , background="#C5B4E3")
        self.change_email.place(height = 30 , width = 180 , x=550 , y=290)
        self.next = tk.Button(self.show_frame , text = "Back" , bg = "#b90ee3" , bd = 3 , command = obj.manually_back)
        self.next.place(height = 25 ,width = 80 , x=650 , y=387)
        # label = tk.Label(show , text = "To Modify\nEmail Addresses :" , background = "blue")
        # label.place(width = 150 , x=200 , y=550)
        self.show_email_button = tk.Button(self.show_frame , text = "SHOW EMAILS" , bd = 3 , command = show_email , bg = "#b90ee3")
        self.show_email_button.place(width = 120 , x=300 , y=460)
        self.refresh_btn = tk.Button(self.show_frame , text = "REFRESH" , bd = 3 , command = refresh , bg = "#b90ee3")
        self.refresh_btn.place(width = 120 , x=140 , y=460)
        self.text_box.configure(state = "disabled")

        self.show_frame.protocol('WM_DELETE_WINDOW' , close_show)
        self.show_frame.resizable(False, False)
        self.show_frame.mainloop()

    def about_page(self):
        self.about_frame = tk.Tk()

        self.about_frame.geometry('1000x600')
        self.about_frame.config(background = "#9f3ae7" )
        self.about_frame.title("STORED EMAIL ADDRESSES")
        self.about_frame.focus_force()
        self.about_frame.pack_propagate(0)  

        self.canvas = Canvas(
            self.about_frame,
            bg = "#9f3ae7",
                height = 600,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
                relief = "ridge")
        self.canvas.place(x = 0, y = 0)

        self.background_img = tk.PhotoImage(file = f"aboutus.png")
        self.background = self.canvas.create_image(
                500.0, 300.0, image=self.background_img)

        self.back_btn = tk.Button(self.about_frame , text = "BACK" , bd = 3 , command =obj.about_to_home  , bg = "#b90ee3")
        self.back_btn.place(width = 120 , x=770, y=520)

        self.about_frame.protocol('WM_DELETE_WINDOW' , close_about)
        self.about_frame.resizable(False, False)
        self.about_frame.mainloop()
        
    def admin_page_1(self):
        self.admin_frame = tk.Tk()
        self.admin_frame.geometry('1000x600')
        self.admin_frame.config(bg = "#9f3ae7")
        self.admin_frame.title("Recent Activity")
        self.admin_frame.focus_force()
        self.admin_frame.pack_propagate(1)

        self.canvas = Canvas(
            self.admin_frame,
            bg = "#9f3ae7",
            height = 600,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        self.canvas.place(x = 0, y = 0)

        self.background_img = tk.PhotoImage(file = f"background_recentdetails.png")
        self.background = self.canvas.create_image(
            500.0, 300.0,
            image=self.background_img)

        self.columns = ('id' , 'Sender_Email' , 'Admin_Email' , 'Date' , 'Time' , 'Sent_To')
        self.tree = ttk.Treeview(self.admin_frame , columns = self.columns , show = "headings")
        self.tree.place(height = 322 , width = 585 , x=332 , y=122)
        self.tree.column('id' , anchor = "center" , width = 70)
        self.tree.column('Sender_Email' , anchor = "center" , width = 120)
        self.tree.column('Admin_Email' , anchor = "center", width = 120)
        self.tree.column('Date' , anchor = "center", width = 60)
        self.tree.column('Time' , anchor = "center", width = 60)
        self.tree.column('Sent_To' , anchor = "center", width = 120)


        self.label = tk.Label(self.admin_frame , text = "Recent_Details" , background = "white" , font = ("Algerian" , "42") , anchor = "center")
        self.label.place(height = 50 , width = 460 , x=400 , y=55)
        self.clear_history = tk.Button(self.admin_frame , text = "Clear History" , command = clear_history , background = "#b90ee3" , bd = 2)
        self.clear_history.place(width = 100 , x=440 , y=480)
        self.back = tk.Button(self.admin_frame , text = "Back" , command = obj.admin_to_home, background = "#b90ee3" , bd = 2)
        self.back.place(width = 100 , x=570 , y=480)
        self.show_history = tk.Button(self.admin_frame , text = "Show History" , command = admin_access , background = "#b90ee3" , bd = 2)
        self.show_history.place(width = 100 , x=700 , y=480)
        self.tree.heading('id' , text = "Record_Id")
        self.tree.heading('Sender_Email' , text = "Sender_Email")
        self.tree.heading('Admin_Email' , text = "Admin_Email")
        self.tree.heading('Date' , text = "Date")
        self.tree.heading('Time' , text = "Time")
        self.tree.heading('Sent_To' , text = "Sent_To")

        # show_details = tk.Text(frame , background = "pink" , foreground = "red")
        # show_details.place(height=200 , width=800 , x=100 , y=150)

        self.admin_frame.resizable(False, False)
        self.admin_frame.mainloop()
        
    def previous_page(self):
        self.previous_frame = tk.Tk()
        self.previous_frame.geometry('1000x600')
        self.previous_frame.config(bg = "#9f3ae7")
        self.previous_frame.title("Recent Activity")
        self.previous_frame.focus_force()
        self.previous_frame.pack_propagate(1)

        self.canvas = Canvas(
            self.previous_frame,
            bg = "#9f3ae7",
            height = 600,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        self.canvas.place(x = 0, y = 0)

        self.background_img = tk.PhotoImage(file = f"background_recentdetails.png")
        self.background = self.canvas.create_image(
            500.0, 300.0,
            image=self.background_img)

        self.columns = ('id' , 'Sender_Email' , 'Admin_Email' , 'Date' , 'Time' , 'Sent_To')
        self.tree = ttk.Treeview(self.previous_frame , columns = self.columns , show = "headings")
        self.tree.place(height = 322 , width = 585 , x=332 , y=122)
        self.tree.column('id' , anchor = "center" , width = 70)
        self.tree.column('Sender_Email' , anchor = "center" , width = 120)
        self.tree.column('Admin_Email' , anchor = "center", width = 120)
        self.tree.column('Date' , anchor = "center", width = 60)
        self.tree.column('Time' , anchor = "center", width = 60)
        self.tree.column('Sent_To' , anchor = "center", width = 120)


        self.label = tk.Label(self.previous_frame , text = "Recent_Details" , background = "white" , font = ("Algerian" , "42") , anchor = "center")
        self.label.place(height = 50 , width = 460 , x=400 , y=55)
        # self.clear_history = tk.Button(self.previous_frame , text = "Clear History" , command = clear_history , background = "#b90ee3" , bd = 2)
        # self.clear_history.place(width = 100 , x=440 , y=480)
        self.back = tk.Button(self.previous_frame , text = "Back" , command = obj.previous_to_home, background = "#b90ee3" , bd = 2)
        self.back.place(width = 100 , x=500 , y=480)
        self.show_history = tk.Button(self.previous_frame , text = "Show History" , command = user_access , background = "#b90ee3" , bd = 2)
        self.show_history.place(width = 100 , x=700 , y=480)
        self.tree.heading('id' , text = "Record_Id")
        self.tree.heading('Sender_Email' , text = "Sender_Email")
        self.tree.heading('Admin_Email' , text = "Admin_Email")
        self.tree.heading('Date' , text = "Date")
        self.tree.heading('Time' , text = "Time")
        self.tree.heading('Sent_To' , text = "Sent_To")


        self.previous_frame.resizable(False, False)
        self.previous_frame.mainloop()

    def previous_switch(self):
        self.home_frame.destroy()
        obj.previous_page()
        
    def previous_to_home(self):
        self.previous_frame.destroy()
        obj.home_page()
        
    def admin_to_home(self):
        obj.admin_frame.destroy()
        obj.home_page()

    def about_page_switch(self):
        self.home_frame.destroy()
        obj.about_page()

    def about_to_home(self):
        self.about_frame.destroy()
        obj.home_page()    

    def admin_page_switch(self):
        self.home_frame.destroy()
        obj.admin_page()

    def admin_to_home(self):
        obj.admin_frame.destroy()
        obj.home_page()

    def sign_switch(self):
        self.login_frame.destroy()
        obj.signup_page()

    def login_switch(self):
        self.signup_frame.destroy()
        obj.login_page()

    def csvupload_switch(self):
        self.home_frame.destroy()
        obj.csvupload_page()

    def entermanually_switch(self):
        self.home_frame.destroy()
        obj.enter_manually_page()

    def schedulemail_switch(self):
        self.home_frame.destroy()
        obj.schedul_email_page()

    def csv_home_switch(self):
        global len_actual_mail
        len_actual_mail=0
        global len_wrong_mail
        len_wrong_mail=0
        mycursor.execute("truncate bulkemail_csvupload;")
        bulk_DB.commit()
        mycursor.execute("truncate bulkemail_attachment;")
        bulk_DB.commit()
        
        self.csvupload_frame.destroy()
        obj.home_page()

    def manually_home(self):
        mycursor.execute("truncate bulkemail_entermanually;")
        bulk_DB.commit()
        mycursor.execute("truncate bulkemail_attachment;")
        bulk_DB.commit()
        self.entermanually_frame.destroy()
        obj.home_page()

    def scheduling_home_switch(self):
        self.scheduling_frame.destroy()
        obj.home_page()

    def show_switch(self):
        self.entermanually_frame.destroy()
        obj.show_page()

    def manually_back(self):
        self.show_frame.destroy()
        obj.enter_manually_page()
        
obj = Bulk_Client()
obj.login_page()