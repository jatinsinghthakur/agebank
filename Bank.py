import mysql.connector as sql
from datetime import date

class customException(Exception):
    def NoDataBaseError(self):
        print(self)


def get_connection():
    hostname = "1yysx5.h.filess.io"
    database = "bank1_walkantsam"
    port = "61032"
    username = "bank1_walkantsam"
    password = "699cede321c9fac60e9c7046247b91e7d4196ed5"
    
    return sql.connect(
        host=hostname,
        user=username,
        password=password,
        database=database,
        port=port
        )
    

def validate_passcode(x,y):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT passcode from customers where account_number=%s",(x,))
    f=cursor.fetchone()

    cursor.close()
    conn.close()
    try:
        if(f[0]!=y ):
            return False
        return True
    except :
        return False

def validate_name(name):

    for i in name:
        if(i.isnumeric()==True):
            return "The name is illogical"
            
    return name

def validate_amount(amount:str):
    amount=amount.rstrip(" ")

    if(amount==""):
        amount=0
    if(float(amount)<0):
            
            return "The amount is illogical"
    
    return float(amount)


def validate_dob(dob):
        dob=dob.rstrip(" ")
        current_year=str(date.today())[:4]
        if((int(current_year)-int(dob[:4]))<18):
            raise customException("You are below 18 hence not eligable to open account")
        return dob





class Bank:
    def open_account(self,name,initial_amount,dob,passcode):
        try:
            conn=get_connection()
            cursor=conn.cursor()

            name=validate_name(name)
            initial_amount=validate_amount(initial_amount)
            dob=validate_dob(dob)
            
            cursor.execute("INSERT INTO customers (passcode,name,dob,amount) values (%s,%s,%s,%s)",(passcode,name,dob,initial_amount))
            conn.commit()
            f=cursor.lastrowid
            
            cursor.close()
            conn.close()
            
            return f
        
        
        except Exception as e:
            print(e)
            return "error occured"



    def debit(self,account_number,passcode,amount):
        #details here to debit amount
        account_number=int(account_number)
        v=validate_passcode(account_number,passcode)
        if(v):
            a=float(amount)
            if(a>0):
                conn=get_connection()
                cursor=conn.cursor()
                cursor.execute("select amount from customers where account_number=%s",(account_number,))
                f=cursor.fetchone()[0] #type:ignore
                new_amount=float(f)-a #type:ignore
                if(new_amount<0):
                    res={
                        "status":"Transaction Barred",
                        "result":"The amount isn't enough in your account"
                    }
                    return res
                cursor.execute("UPDATE customers set amount=%s where account_number=%s",(new_amount,account_number))
                conn.commit()
                cursor.close()
                conn.close()
                
                return {
                    "status":"debit successful ✅",
                    "amount":amount,
                    "new_amount":new_amount
                }

        else:
            raise customException("Invalid Credentials")

    def verify_credit(self,account_number):
        #take input for details
        account_number=int(account_number)
        conn=get_connection()
        cursor=conn.cursor()
        try:
            cursor.execute("Select name from customers where account_number=%s",(account_number,))
        except:
            return customException("Invalid Account Number")
        f=cursor.fetchone()[0] #type:ignore
        cursor.close()
        conn.close()
        return f
        

    def confirm_credit(self,account_number,amount):
            conn=get_connection()
            cursor=conn.cursor()
            account_number=int(account_number)
            amount=float(amount)
            cursor.execute("select amount from customers where account_number=%s",(account_number,))
            t=cursor.fetchone()[0]#type:ignore
            new_ammount=float(t)+amount #type:ignore
            if(new_ammount<=0):
                result={"amount":"The Invalid Input Amount","new_amount":t}
                return result
            cursor.execute("UPDATE customers set amount=%s where account_number=%s",(new_ammount,account_number))
            conn.commit()
          
            cursor.close()  
            conn.close()
         
            return {
                "amount":amount,
                "new_amount":new_ammount
            }


    def info(self,account_number,passcode):
        conn=get_connection()
        cursor=conn.cursor()

        v=validate_passcode(int(account_number),passcode)
        if(v==False):
           res={
               "Account Number":"Nil",
               "Passcode":"Nil",
                "Name":"Invalid Credentials",
                "Current Amount":0,
                "DOB":"Nil"
           }
           return res
        
        cursor.execute("Select account_number,name,amount,dob from customers where account_number=%s",(account_number,))
        t=cursor.fetchone()
        cursor.close()
        conn.close()
        data={
            "Account Number":t[0],
            "Passcode":passcode,
            "Name":t[1],
            "Current Amount":float(t[2]),
            "DOB":str(t[3])
        }
        
        return data