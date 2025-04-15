import streamlit as st
import mysql.connector
import pandas as pd
from tabulate import tabulate
from streamlit_option_menu import option_menu
from PIL import Image
import time

con = mysql.connector.connect(host="localhost",username="root",password="ayyappan2004",database="banking_app_sql")
bank = con.cursor()

acc_option = ""

def registration_form():

    user_name = st.text_input("Name",placeholder="Enter Your Name").upper()
    dob = st.text_input("Date of Birth",placeholder="Enter the Date of Birth (dd/mm/yyyy)")
    ph_no = st.text_input("Phone Number",placeholder="Enter the Phone Number")
    np = st.text_input("Native Place",placeholder="Enter the Native Place").upper()
    state = st.text_input("State",placeholder="Enter the State").upper()
    pin = st.text_input("PIN",placeholder="Set New Pin",type="password")
    pin_d = st.text_input("Re-Enter the PIN",placeholder="Set New Pin",type="password")
    upi_pin = st.text_input("UPI PIN",placeholder="Set New UPI Pin 6 Digits",type="password")
    upi_pin_d = st.text_input("Re-Enter the UPI PIN",placeholder="Set New UPI Pin",type="password")

    def acc_no():
        global account_no  
        account_no = 12340
        qry="select account_number from acc_register order by account_number desc limit 1"
        bank.execute(qry)
        acc_no = bank.fetchone()
        if acc_no == None:
            account_no = account_no + 1
            st.write("Your Account number Is",account_no)
            return account_no
        else:
            account_no = acc_no[0] + 1
            st.write("Your Account Number Is",account_no)
            return account_no
        
    if st.button("Submit"):
        if pin == pin_d:
            if upi_pin == upi_pin_d:
                account_no = acc_no()
                qry="insert into acc_register(account_number,user_name,date_of_birth,phone_number,native_place,state,pin,upi_pin)values(%s,%s,%s,%s,%s,%s,%s,%s)"
                val1=(account_no,user_name,dob,ph_no,np,state,pin,upi_pin)
                bank.execute(qry,val1)
                con.commit()
                st.success("Registeration Done")
            else:
                st.error("Check the UPI PIN")
        else:
            st.error("Check the PIN NUmber")

def account_no_lst():
    ac_no_lst = []
    qry = "select account_number from acc_register"
    bank.execute(qry)
    data1 = bank.fetchall()
    for i in data1:
        ac_no_lst.append(i[0])
    return ac_no_lst  

def get_pin_lst(account_number):
    qry = "select pin from acc_register where account_number = %s"
    val = (int(account_number),)
    bank.execute(qry,val)
    data2 = bank.fetchall()
    return data2[0][0]

def get_upi(account_number):
    qry = "SELECT upi_pin FROM acc_register WHERE account_number = %s"
    val = (int(account_number),)
    bank.execute(qry, val)
    data3 = bank.fetchall()
    if data3:
        return data3[0][0]
    else:
        return None

def get_pin(account_number):
    qry = "select pin from acc_register where account_number = %s"
    bank.execute(qry, (account_number,))
    data1 = bank.fetchall()
    return data1[0][0]

def saving_price(amount_no):
    qry = "select saving_amount from acc_register where account_number = %s"
    bank.execute(qry,(amount_no,))
    data2 = bank.fetchall()
    return data2[0][0]

def reciver_update_amount(account_number,reciver_update_amount):
    qry = "update acc_register set saving_amount = %s where account_number = %s"
    val2 = (reciver_update_amount,account_number)
    bank.execute(qry,val2)
    con.commit()

def self_deposite_amount(account_number,sender_update_amount):
    qry = "update acc_register set saving_amount = %s where account_number = %s"
    val2 = (sender_update_amount,account_number)
    bank.execute(qry,val2)
    con.commit()


def with_draw_amount(account_number,withdraw_amount):
    qry = "update acc_register set saving_amount = %s where account_number = %s"
    val2 = (withdraw_amount,account_number)
    bank.execute(qry,val2)
    con.commit()

def transfer_account_lst():
    t_a_lst = []
    qry = "select account_number from acc_register"
    bank.execute(qry)
    data4 = bank.fetchall()
    for i in data4:
        t_a_lst.append(i[0])
    return t_a_lst

def update_upi_pin(account_number,new_upi):
    qry = "update acc_register set upi_pin = %s where account_number = %s"
    val = (new_upi,account_number)
    bank.execute(qry,val)
    con.commit()

def get_dob_list(account_number):
    qry = "select date_of_birth from acc_register where account_number = %s"
    val5 = (int(account_number),)
    bank.execute(qry,val5)
    data3 = bank.fetchall()
    return data3[0][0]

def get_phone_number(account_number):
    qry = "select phone_number from acc_register where account_number = %s"
    val = (int(account_number),)
    bank.execute(qry,val)
    data2 = bank.fetchall()
    if data2 and len(data2[0]) > 0:
        return data2[0][0]
    else:
        st.error(f"No phone number found for account number: {account_number}")
        return None


def update_password(account_number,new_password):
    qry = "update acc_register set pin = %s where account_number = %s"
    val = (new_password,account_number)
    bank.execute(qry,val)
    con.commit()

def personal_banking():

    st.markdown("### Personal Banking")
    
    # Login or Reset Password menu
    option = option_menu(
        menu_title="Login Options",
        options=["Login", "Reset Password"],
        icons=["cash","key"],
        menu_icon="menu",
        default_index=0 )

    if option == "Login":
        account_number = st.text_input("Enter Your Account  (If You Enter the Correct A/C No [IT WILL PROCESS NEXT STEP])",key="account_number")

        if account_number.strip():
        
      
            try:
                account_number = int(account_number)
        
                account_lst = account_no_lst()#checking account number is there or not
                if account_number in account_lst: #checking condition

                    pin = st.text_input("Enter the PIN   (If You Enter the Correct PIN *IT WILL PROCESS NEXT STEP*)",placeholder="4 DIGIT PIN",type="password")
                    pin_lst = get_pin_lst(int(account_number)) #checking PIN is there or not
                    if pin == pin_lst: #checking condition
                        st.success("Succefully Login")
                
                        login_option = st.selectbox("",["Deposite","Transfer Amount","Withdraw Amount","Balance Enquiry","Reset UPI","User Details"])

                        st.write(f"You Selected {login_option}")
                
                        if login_option == "Deposite":

                            deposite_amount = st.text_input("Enter Deposite Amount")

                            if st.button("Deposite"):

                                deposite_amount = float(deposite_amount)

                                current_saving_amount = saving_price(account_number)
                                if current_saving_amount is None:
                                    current_saving_amount = 0
                                deposited_amount = current_saving_amount + deposite_amount
                                self_deposite_amount(account_number,deposited_amount)

                                st.success(f"Amount has Been Debit Successfully :{deposite_amount}")
                        


                        elif login_option == "Transfer Amount":

                            transfer_account_number = st.text_input("Enter Transfer Account Number (If You Enter the Correct A/C No It will process)",value=0)
                            deposite_amount = st.text_input("Enter Transfer Amount",placeholder="Enter The Amount")
                    
                            deposite_amount = float(deposite_amount)

                            transfer_account_number = int(transfer_account_number)

                            t_a_lst = transfer_account_lst()
                            if transfer_account_number in t_a_lst:

                                upi_lst = get_upi(account_number)
                                upi_pin = st.text_input("Enter UPI PIN")

                                if upi_pin == upi_lst: #checking upi is in the account
                                    sender_current_amount=saving_price(account_number)
                                    reciver_current_amount=saving_price(transfer_account_number)

                                        # Check if sender has sufficient balance
                                    if deposite_amount>=sender_current_amount:
                                        st.error(f"insufficient Amount in your Account  {sender_current_amount}")
                                    else:
                                        # Perform transfer      
                                        new_sender_balance_amount = sender_current_amount - deposite_amount
                                
                                        if reciver_current_amount is None:
                                            # Handle the error appropriately, e.g., set a default value or raise an exception
                                            reciver_current_amount = 0  # or handle as per your application logic

                                            if deposite_amount is None:
                                                deposite_amount = 0  # or handle as needed

                                        new_receiver_balance_amount = reciver_current_amount + deposite_amount
                            

                                        # Update balances in database (assuming a function for this exists)
                                        self_deposite_amount(account_number , new_sender_balance_amount )
                                        reciver_update_amount(transfer_account_number , new_receiver_balance_amount)

                                        st.success(f"Successfully Amount has been Transferred {deposite_amount}")
                                else:
                                    st.error("Wrong PIN")
                
                        elif login_option == "Withdraw Amount":
                            withdraw_amount = st.text_input("Enter the Amount:",placeholder="After enter the UPI PIN **Enter**",value = 0)

                            withdraw_current_account = saving_price(account_number)

                            withdraw_amount = float(withdraw_amount)  #changing to float 

                            pin=st.text_input("Enter the PIN   (If You Enter the Correct PIN *Error Will Not Show*)",placeholder="4 DIGIT PIN",type="password",key="unique_key_for_pin_input")
                            pin_lst=get_pin_lst(int(account_number)) #checking PIN is there or not
                            if pin == pin_lst: #checking condition
                    
                                if withdraw_amount >= withdraw_current_account:
                                    st.error("Insufficient Amount in your Account")
                                else:              
                                    with_amount_p = withdraw_current_account - withdraw_amount
                                    with_draw_amount(account_number,with_amount_p)
                                    st.success(f"Collect Your Amount {withdraw_amount}")
                            else:
                                st.error("Invalid Pin")

                        elif login_option == "Balance Enquiry":
                            qry="select saving_amount from acc_register where account_number = %s"
                            bank.execute(qry,(account_number,))
                            data12=bank.fetchall()
                            s_a=pd.DataFrame(data12,columns=["saving_amount"])
                            st.write("Your Account Balance ",s_a)

                        elif login_option == "Reset UPI":

                            new_upi=st.text_input("Enter the new UPI Number")
                    
                            if st.button("Submit"):
                                if new_upi == new_upi:  #Checking new_upi is equal or not
                                    update_upi_pin(account_number,new_upi)
                                    st.success("UPI Number Has Update is Done")
                                else:
                                    st.write("Check The Enter Pin")

                        elif login_option=="User Details":
                            qry="select account_number,user_name,date_of_birth,phone_number,native_place,state from acc_register where account_number = %s"
                            bank.execute(qry,(account_number,))
                            data3 = bank.fetchall()
                            man = pd.DataFrame(data3,columns = ["account_number","user_name","date_of_birth","phone_number","native_place","state"])
                            st.table(man)
                    else:
                        st.error("Invalid Pin")
                else:
                    st.error("Account number not found")
            except:
                st.warning("Carefull to Enter the details")
        else:
            st.error("Account number cannot be empty")
      
    elif option == "Reset Password":
        account_number=st.number_input("Enter Account Number (If You Enter the Correct A/C No *Error Will Not Show*)",value=12340)
        account_lst=account_no_lst()
            
        enter_ph_no=st.text_input("Enter the Phone Number(If You Enter the Correct Phone No *Error Will Not Show*")
        ph_no=get_phone_number(account_number)

        if account_number in account_lst:
            if enter_ph_no == ph_no:
                new_password=st.text_input("New Password",type="password")
                
                if st.button("Submit"):
                    if new_password == new_password:
                        update_password(account_number,new_password)
                        st.success("Password Has Change")
        else:
            st.write("Check wheather your enter input details")






st.sidebar.title("Menu Bar")

with st.sidebar:
    bank_option = option_menu("",["Home Page","Corporate Banking","Contact us"])

    if bank_option == "Corporate Banking":
        st.sidebar.title("Welcome To SBI")
        acc_option = st.selectbox("",["Select The Options To Process","Personal Banking","Registration Form"])

if bank_option == "Home Page":
    st.markdown('''<div style="text-align: center;">
                <h3>Welcome to Corporate Internet Banking</h3>
                </div>''',
                unsafe_allow_html = True
                )
    st.markdown("---")

    st.image("images.png",width = 700)

    st.markdown('''<div style="text-align: center;">
            <h6>"Your Dreams, Our Commitment. 
                Empowering You with Trusted Banking Solutions for Every Step of Life"</h6>
            </div>''',
            unsafe_allow_html = True
            )
    
    st.markdown("---")
    st.header("Customer Reviews")
    st.subheader("Our Customers are saying")
    st.write("⭐⭐⭐⭐⭐ - 'I love this App! Great working and fast transcation.'")
    st.write("⭐⭐⭐⭐ - 'Good quality application at affordable prices.'")
    st.write("⭐⭐⭐⭐⭐ - 'Excellent customer service and a wide selection of account.'")
    st.write("© 2025 My Online Store. All rights reserved.")
    st.markdown("---")

if acc_option == "Select The Options To Process":
    st.markdown('''<div style="text-align; center"><h5>About the source</h5>
    <h1>Select The Options To Process</h1></div>''',
    unsafe_allow_html = True
    )

elif acc_option == "Personal Banking":
    st.markdown('''<div style="text-align; center"><h5>About the source</h5>
        <h6>State Bank of India Financial services company
        State Bank of India is an Indian multinational public sector bank and 
        financial services statutory body headquartered in Mumbai, Maharashtra</h6></div>''',
        unsafe_allow_html = True
                )
    personal_banking()
    
elif acc_option == "Registration Form":
    st.markdown('''<div style="text-align: center;">
            <h5>Registration Form</h5>
            </div>''',
            unsafe_allow_html = True
            )
    registration_form()

if bank_option == "Contact us":
    st.markdown('''<div style="text-align: center;">
                 <h5>Call us toll free on 1800 1234 and 1800 2100 and get a wide range of services through SBI
                 Contact Centre.
                 SBI never asks for your Card/PIN/OTP/CVV details on phone, message or email. 
                 Please do not click on links received on your email or mobile asking your Bank/Card details.</h5>
                 ''',  
                 unsafe_allow_html = True
                 )
    st.image("SBI-Phone-Banking-Registration.webp",width = 700)


























