import streamlit as st
import time
import mysql.connector
con=mysql.connector.connect(host='localhost',user='root',password='D94885j@',database='online_shopping')
cur=con.cursor()
import pandas as pd

from reportlab.pdfgen import canvas

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from datetime import datetime
from datetime import date

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked=False
def callback():
    st.session_state.button_clicked=True

# pdf
def area(user_id):
    qry='select area from customer where user_id=%s'
    val=(user_id,)
    cur.execute(qry,val)
    data=cur.fetchall()
    return data[0][0]
def post(user_id):
    qry='select post from customer where user_id=%s'
    val=(user_id,)
    cur.execute(qry,val)
    data=cur.fetchall()
    return data[0][0]
def pincode(user_id):
    qry='select pincode from customer where user_id=%s'
    val=(user_id,)
    cur.execute(qry,val)
    data=cur.fetchall()
    return data[0][0]
def city(user_id):
    qry='select city from customer where user_id=%s'
    val=(user_id,)
    cur.execute(qry,val)
    data=cur.fetchall()
    return data[0][0]
def state(user_id):
    qry='select state from customer where user_id=%s'
    val=(user_id,)
    cur.execute(qry,val)
    data=cur.fetchall()
    return data[0][0]
def email_id(user_id):
    qry='select email_id from customer where user_id=%s'
    val=(user_id,)
    cur.execute(qry,val)
    data=cur.fetchall()
    return data[0][0]




# order

def view():
    qry='select * from product '
    cur.execute(qry)
    data=cur.fetchall()
    data=pd.DataFrame(data,columns=['product_name', 'product_id', 'price', 'quantity'])
    return st.dataframe(data,height = 200,width = 400)
def product_deatils(product_id):
    qry='select * from product where product_id=%s'
    val=(product_id,)
    cur.execute(qry,val)
    data=cur.fetchall()
    data=pd.DataFrame(data,columns=['product_name', 'product_id', 'price', 'quantity'])
    return st.dataframe(data,height = 50,width = 400)
def product_name(product_id):
    qry='select product_name from product where product_id=%s'
    val=(product_id,)
    cur.execute(qry,val)
    data=cur.fetchall()
    return data[0][0]
def quantity(product_id):
    qry='select quantity from product where product_id=%s'
    val=(product_id,)
    cur.execute(qry,val)
    data=cur.fetchall()
    return data[0][0]
def updated_quantity(update_quantity,product_id):
    qry='update product set quantity=%s where product_id=%s'
    val=(update_quantity,product_id)
    cur.execute(qry,val)
    con.commit()
def price(product_id):
    qry='select price from product where product_id=%s'
    val=(product_id,)
    cur.execute(qry,val)
    data=cur.fetchall()
    return data[0][0]
def user_name(user_id):
    qry='select user_name from customer where user_id=%s'
    val=(user_id,)
    cur.execute(qry,val)
    data=cur.fetchall()
    return data[0][0]
def product_name(product_id):
    qry='select product_name from product where product_id=%s'
    val=(product_id,)
    cur.execute(qry,val)
    data=cur.fetchall()
    return data[0][0]
def order(user_id,product_id,req_quantity):
    uname=user_name(user_id)
    pname=product_name(product_id)
    price_=price(product_id)
    tpr=price_*req_quantity
    o_date=date.today()
    o_date=o_date.strftime('%Y/%m/%d')
    print(o_date)
    dt=datetime.now()
    o_time=str(dt.strftime('%H:%M:%S'))
    print(o_time)
    qry='''insert into customer_purchases (user_id, product_id, product_name, price, quantity, total_price,order_date,order_time)
    values (%s,%s,%s,%s,%s,%s,%s,%s)'''
    val=(user_id,product_id,pname,price_,req_quantity,tpr,o_date,o_time)
    cur.execute(qry,val)
    con.commit()
    
    qry='select * from customer_purchases where user_id=%s and order_id=(select max(order_id) from customer_purchases where user_id=%s)'
    val=(user_id,user_id)
    cur.execute(qry,val)
    data=cur.fetchall()
    df=pd.DataFrame(data,columns=['order_id','user_id','product_id',' product_name', 'price', 'quantity', 'total_price','order_date','order_time'])
    return st.dataframe(df,height = 50,width = 800)
def new_order(user_id):
    req_quantity=st.number_input('How many do you wanna buy ',step=1,min_value=1)
    but=st.button('Place Order')
    if but==True:
        qry='select product_id from product '
        cur.execute(qry)
        data=cur.fetchall()
        pid=[]
        for i in data:
            x=str(i[0])
            pid.append(x)
        if product_id in pid:
            cur_quantity=quantity(product_id)
            if cur_quantity==0:
                st.error('Selected Product is out of stock')
            elif req_quantity>cur_quantity:
                st.error('We have only',cur_quantity,'peices')
            else:
                update_quantity=cur_quantity-req_quantity
                updated_quantity(update_quantity,product_id)
                user_id=user_id_l
                st.info('Your order has been placed')
                order(user_id,product_id,req_quantity)

                qry='select max(order_id) from customer_purchases where user_id=%s'
                val=(user_id,)
                cur.execute(qry,val)
                data=cur.fetchall()
                oid=data[0][0]
                total_price=price(product_id)*req_quantity
                or_id='ORDER ID = '+str(oid) 
                pro_name='PRODUCT NAME = '+product_name(product_id) 
                quan='QUANTITY = '+str(req_quantity)
                tp='TOTAL PRICE = '+str(total_price)
                pr='PER QUANTITY PRICE = '+str(price(product_id))
                ct=str(city(user_id)+'-'+str(pincode(user_id)))

                qry='select order_date from customer_purchases where order_id=%s'
                val=(oid,)
                cur.execute(qry,val)
                data=cur.fetchall()
                print(data)
                odate='ORDER DATE = '+data[0][0]
                
                def generate_pdf():
                    pdf_filename = "Invoice.pdf"
                    c = canvas.Canvas(pdf_filename)
                    
                    c.drawString(250, 800, '-_-ORDER INVOICE-_-') 

                    c.drawString(50, 760, 'FROM')
                    c.drawString(100, 740, 'STREAMLIT PRIVATE LIMITED')
                    c.drawString(100, 720, '8/1,MODEL HUTMENT ROAD')
                    c.drawString(100, 700, 'C.I.T NAGAR')
                    c.drawString(100, 680, 'CHENNAI-600035')
                    c.drawString(100, 660, 'TAMILNADU')

                    c.drawString(50, 620, 'TO')
                    c.drawString(100, 600, user_name(user_id).upper())
                    c.drawString(100, 580, area(user_id).upper())
                    c.drawString(100, 560, post(user_id).upper())
                    c.drawString(100, 540, ct.upper())
                    c.drawString(100, 520, state(user_id).upper())

                    c.drawString(50, 480, 'ORDER DETAILS :')
                    c.drawString(100, 460, odate)
                    c.drawString(100, 440, or_id)
                    c.drawString(100, 420, pro_name)
                    c.drawString(100, 400, quan)
                    c.drawString(100, 380, pr)
                    c.drawString(100, 360, tp)

                    c.drawString(50, 320, '-_'*20)
                    c.drawString(270, 320, 'THANK YOU')
                    c.drawString(350, 320, '_-'*20)
                    c.save()
                    return pdf_filename
                def send_email(pdf_filename):
                    email_sender ='appukuttykr@gmail.com'
                    email_receiver =email_id(user_id)
                    subject = 'ORDER DETAILS'
                    password = 'bcbk dcxt aewp nwwe'
                    body='Dear '+user_name(user_id).upper()+' , We are happy to say that your order has been placed \n\n'
                    smtp_server = "smtp.gmail.com"
                    smtp_port = 587

                    msg = MIMEMultipart()
                    msg['Subject'] = subject
                    msg['From'] = email_sender
                    msg['To'] = email_receiver
                    msg.attach(MIMEText(body, "plain"))

                    # Attach the PDF file
                    with open(pdf_filename, 'rb') as file:
                        attach = MIMEApplication(file.read(),_subtype="pdf")
                        attach.add_header('Content-Disposition','attachment',filename=str(pdf_filename))
                        msg.attach(attach)

                    # Connect to the SMTP server and send the email
                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                        server.starttls()
                        server.login(email_sender, password)
                        server.sendmail(email_sender, email_receiver, msg.as_string())

                    st.info(f"A copy of order has been sent to your {email_receiver} with the PDF attachment.")

                pdf_filename = generate_pdf()
                send_email(pdf_filename)
        else:
            st.error('Enter correct product id')
        
            
#  cancel
def bookshow(user_id):
    qry='select * from customer_purchases where user_id=%s'
    val=(user_id,)
    cur.execute(qry,val)
    data=cur.fetchall()
    data=pd.DataFrame(data,columns=['order_id','user_id','product_id',' product_name', 'price', 'quantity', 'total_price','order_date','order_time'])
    return st.dataframe(data,height =200,width = 800)
def op_id(order_id):
    qry='select product_id from customer_purchases where order_id=%s '
    val=(order_id,)
    cur.execute(qry,val)
    data=cur.fetchall()
    return data[0][0]
def bookedquantity(order_id,user_id):
    qry='select quantity from customer_purchases where order_id=%s and user_id=%s '
    val=(order_id,user_id)
    cur.execute(qry,val)
    data=cur.fetchall()
    return data[0][0]
def delete(order_id):
    qry='delete from customer_purchases where order_id=%s'
    val=(order_id,)
    cur.execute(qry,val)
    con.commit()
def cancel(user_id):
    order_id=st.text_input('Which of order id to be cancelled ')
    but=st.button('CANCEL')
    if but==True:
        qry='select order_id from customer_purchases where user_id=%s'
        val=(user_id,)
        cur.execute(qry,val)
        data=cur.fetchall()
        oid=[]
        for i in data:
            x=str(i[0])
            oid.append(x)
        if order_id in  oid :
            product_id=op_id(order_id)
            pre_quantity=quantity(product_id)
            cur_quantity=bookedquantity(order_id,user_id)
            total_quantity=pre_quantity+cur_quantity
            update_quantity=total_quantity
            updated_quantity(update_quantity,product_id)
            delete(order_id)
            st.info('Order has been cancelled and the remaining orders are')
            return bookshow(user_id)
        else:
            st.error('Enter correct order id')
                
# update customer
def update(user_id):
    x=st.radio('CUSTOMER_UPDATE',['USER_NAME','PASSWORD','ADDRESS'])
    qry='select * from customer where user_id=%s'
    val=(user_id,)
    cur.execute(qry,val)
    data=cur.fetchall()
    data=pd.DataFrame(data,columns=['user_name', 'user_id', 'password', 'ph_number', 'area','post', 'city', 'pincode', 'state', 'email_id'])
    st.dataframe(data,height=50,width=800)
    if x=='USER_NAME':
        f,l=st.columns(2)
        first_name=f.text_input('First Name')
        last_name=l.text_input('Last Name ')
        user_name=first_name +' '+ last_name
    elif x=='PASSWORD':
        password=st.text_input('enter new password ')
    elif x=='ADDRESS':
        area=st.text_area('AREA ')
        post=st.text_input('POST ')
        city=st.text_input('CITY ')
        pincode=st.text_input('PINCODE')
        state=st.text_input('STATE')
    but_u=st.button('Update')
    if but_u==True:
        if x =='USER_NAME':
            if not user_name:
                st.error('Enter user name')
            else:
                qry='update customer set user_name=%s where user_id=%s'
                val=(user_name,user_id)
                cur.execute(qry,val)
                con.commit()
        elif x=='PASSWORD':
            if not password:
                st.error('Enter password')
            else:
                qry='update customer set password=%s where user_id=%s'
                val=(password,user_id)
                cur.execute(qry,val)
                con.commit()
        elif x=='ADDRESS':
            if not area or not post or not city or not pincode or not state:
                st.error('Enter address')
            else:
                qry='update customer set area=%s,post=%s,city=%s,pincode=%s,state=%s where user_id=%s'
                val=(area,post,city,pincode,state,user_id)
                cur.execute(qry,val)
                con.commit()
        qry='select * from customer where user_id=%s'
        val=(user_id,)
        cur.execute(qry,val)
        data=cur.fetchall()
        data=pd.DataFrame(data,columns=['user_name', 'user_id', 'password', 'ph_number', 'area','post', 'city', 'pincode', 'state', 'email_id'])
        st.dataframe(data,height=50,width=800)
# update product
def p_update():
    product_id=st.number_input('Enter product id ',step=0)
    ch=st.selectbox('product_update',['product_price','product_quantity'])
    if ch=='product_price':
        price_=st.number_input('enter new price ',step=1,min_value=1)
    elif ch=='product_quantity':
        new_quantity_=st.number_input('enter new quantity ',step=1,min_value=1)
    but=st.button('Update')
    if but==True:
        qry='select product_id from product'
        cur.execute(qry)
        data=cur.fetchall()
        if (product_id,) in data:
            qry='select * from products where product_id=%s'
            val=(product_id,)
            cur.execute(qry,val)
            data=cur.fetchall()
            data=pd.DataFrame(data,columns=['product_name','product_id','price','quantity'])
            st.dataframe(data,height=50,width=400)
            if ch=='product_price':
                qry='update product set price=%s where product_id=%s'
                val=(price,product_id) 
                cur.execute(qry,val)
                con.commit()
            elif ch=='product_quantity':
                old_quantity=quantity(product_id)
                update_quantity=new_quantity+old_quantity
                updated_quantity(update_quantity,product_id)
            qry='select * from products where product_id=%s'
            val=(product_id,)
            cur.execute(qry,val)
            data=cur.fetchall()
            data=pd.DataFrame(data,columns=['product_name','product_id','price','quantity'])
            st.dataframe(data,height=50,width=400)
        else:
            st.error('enter correct product id')   
# product add
def p_insert():
    product_name=st.text_input('Enter product name ')
    price=st.number_input('Enter price ',step=1,min_value=1)
    quantity=st.number_input('Enter quantity ',step=0,min_value=1)
    but=st.button('submit')
    if but==True:
        qry='select product_name from product'
        cur.execute(qry)
        data=cur.fetchall()
        if product_name=='':
            st.error('Enter all details')
        if (product_name,) in data:
            st.error('product_name already exists')
        else:
            qry='insert into product (product_name,price,quantity) values (%s,%s,%s)'
            val=(product_name, price,quantity)
            cur.execute(qry,val)
            con.commit()
            st.info('Product added')
            qry='select * from product'
            cur.execute(qry)
            return cur.fetchall()

# update employee
def eupdate(e_id):
    x=st.radio('E_UPDATE',['e_name','e_city','e_password','e_state'])
    if x=='e_name':
        f,l=st.columns(2)
        first_name=f.text_input('First Name')
        last_name=l.text_input('Last Name ')
        e_name=first_name +' '+ last_name
    elif x=='e_city':
        e_city=st.text_input('enter new city name ')
    elif x=='e_password':
        e_password=st.text_input('enter new password ')
    elif x=='e_state':
        e_state=st.text_input('enter new name ')
    but_u=st.button('E_UPDATE')
    if but_u==True:
        st.info('Updated')
        qry='select * from employees where e_id=%s'
        val=(e_id,)
        cur.execute(qry,val)
        data=cur.fetchall()
        data=pd.DataFrame(data,columns=['e_name','e_id','e_password', 'e_ph_number','e_city','e_state','email_id'])
        st.dataframe(data,height=50,width=700)
        if x=='e_name':
            qry='update employees set e_name=%s where e_id=%s'
            val=(e_name,e_id)
            cur.execute(qry,val)
            con.commit()
        elif x=='e_city':
            qry='update employees set e_city=%s where e_id=%s'
            val=(e_city,e_id)
            cur.execute(qry,val)
            con.commit()
        elif x=='e_password':
            qry='update employees set e_password=%s where e_id=%s'
            val=(e_password,e_id)
            cur.execute(qry,val)
            con.commit()
        elif x=='e_state':
            qry='update employees set e_state=%s where e_id=%s'
            val=(e_state,e_id)
            cur.execute(qry,val)
            con.commit()
        qry='select * from employees where e_id=%s'
        val=(e_id,)
        cur.execute(qry,val)
        data=cur.fetchall()
        data=pd.DataFrame(data,columns=['e_name','e_id','e_password', 'e_ph_number','e_city','e_state'])
        st.dataframe(data,height=50,width=600)

index=st.sidebar.selectbox('USER',['customer','employee'])

if index=='customer':
    sig=st.sidebar.selectbox('customer',['Registration','login'])
    if sig=='Registration':
        st.title('Customer Registration')
        f,l=st.columns(2)
        first_name=f.text_input('First Name')
        last_name=l.text_input('Last Name ')
        username_r=first_name +' '+ last_name
        user_id_r=st.text_input('User ID')
        password_r=st.text_input('Password',type='password')
        repassword_r=st.text_input('Re enter Password',type='password')
        phnumber_r=st.text_input('Phone Number')
        email_id=st.text_input('Email ID')
        a,p=st.columns([2,1])
        area=a.text_area('Area')
        post=p.text_input('Post')
        c,p,s=st.columns([1,1,1])
        city_r=c.text_input('City')
        pincode=p.text_input('Pincode')
        state_r=s.text_input('State')
        st.checkbox('I agree') 
        but_r=st.button('SUBMIT')
        if but_r==True: 
            p=st.progress(0)
            for i in range(100):
                time.sleep(0.001)
                p.progress(i+1)
            qry='select user_id from customer'
            cur.execute(qry)
            data=cur.fetchall()
            
            qry='select email_id from customer'
            cur.execute(qry)
            data_e=cur.fetchall()

            if pincode=='' or area=='' or post=='' or  first_name =='' or password_r =='' or phnumber_r == '' or city_r == '' or state_r == '' or user_id_r == '' or email_id=='':
                st.error('Enter all details')
            elif (user_id_r,) in data :
                st.error('User id already exists')
            elif password_r!=repassword_r:
                st.error('Pasword should be same')
            elif len(email_id)<11:
                st.error('enter correct email id')
            elif email_id.endswith('@gmail.com')==False:
                st.warning('Enter correct email id')
            elif (email_id,) in data_e:
                st.error('email id exists')
            elif len(pincode)!=6:
                st.warning('Enter correct pincode')
            else:
                qry='select ph_number from customer '  
                cur.execute(qry)
                data_ph=cur.fetchall()

                if (phnumber_r,) in data_ph:
                    st.error('Phone number exists')
                elif phnumber_r.startswith('9'or'6'or'8')==False:
                    st.error('Enter correct phone number')
                elif len(phnumber_r)!=10:
                    st.error('Enter correct phone number')
                else:
                    for i in phnumber_r:
                        if i not in '0123456789':
                            st.warning('Enter correct phone number')
                            break
                    else:
                        for i in pincode:
                            if i not in '0123456789':
                                st.warning('Enter correct pincode')
                                break

                        else:
                            qry='insert into customer values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                            val=(username_r,user_id_r,password_r,phnumber_r,area,post,city_r,pincode,state_r,email_id)
                            cur.execute(qry,val)
                            con.commit()

                            user_id=user_id_r
                            email_sender ='appukuttykr@gmail.com'
                            email_receiver =email_id
                            subject = 'LOGIN DETAILS'
                            password = 'bcbk dcxt aewp nwwe'
                            body='Dear '+user_name(user_id).upper()+' , Thank you for becoming a member \n\n'
                            body1='LOGIN ID : '+user_id+'\n'+'PASSWORD : '+password
                            
                            msg =MIMEMultipart()
                            msg['From'] = email_sender
                            msg['To'] = email_receiver
                            msg['Subject'] = subject
                            msg.attach(MIMEText(body, "plain"))
                            msg.attach(MIMEText(body1, "plain"))

                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls()
                            server.login(email_sender, password)
                            server.sendmail(email_sender, email_receiver, msg.as_string())
                            server.quit()

                            st.info('Thank you for becoming a member and a copy of your ID and Password has been sent to your email')
                            st.balloons()

                                
    elif sig=='login':
        st.title('Customer Login')
        user_id_l=st.text_input('User ID')
        password_l=st.text_input('Password',type='password')
        if st.button("C_LOGIN",on_click=callback) or st.session_state.button_clicked:
            p=st.progress(0)
            for i in range(100):
                time.sleep(0.0001)
                p.progress(i+1)
            qry='select user_id from customer '
            cur.execute(qry)
            data=cur.fetchall()
            if (user_id_l,) not in data:
                st.error('incorrect user id')
            else:
                qry='select password from customer where user_id=%s '
                val=(user_id_l,)
                cur.execute(qry,val)
                data=cur.fetchall()
                if (password_l,) not in data:
                    st.error('incorrect password')
                else:
                    sel=st.selectbox('CHOICE',['VIEW','ORDER','CANCEL','UPDATE'])
                    if sel=='VIEW':
                        st.title('VIEW')
                        view()
                    elif sel=='ORDER':
                        st.title('NEW ORDER')
                        user_id=user_id_l
                        view()
                        product_id=st.text_input('Enter required product id ')
                        new_order(user_id)
                    elif sel=='CANCEL':
                        st.title('CANCEL')
                        user_id=user_id_l
                        bookshow(user_id)
                        cancel(user_id)
                    elif sel=='UPDATE':
                        st.title('UPDATE')
                        user_id=user_id_l
                        update(user_id)
            
elif index=='employee':
    sig=st.sidebar.selectbox('employee', ['registration','login'])
    if sig=='registration':
        st.title('Employee Registration')
        f,l=st.columns(2)
        first_name=f.text_input('First Name')
        last_name=l.text_input('Last Name ')
        e_name=first_name+' '+last_name
        e_password=st.text_input('Password',type='password')
        re_e_password=st.text_input('Re enter Password',type='password')
        e_ph_number=st.text_input('Phone Number')
        email_id=st.text_input('Email ID')
        e_city=st.text_input('City')
        e_state=st.text_input('State')
        check=st.checkbox('I agree')
        but_r=st.button('Submit')
        if but_r==True:
            p=st.progress(0)
            for i in range(100):
                time.sleep(0.001)
                p.progress(i+1)
            qry='select e_ph_number from employees'
            cur.execute(qry)
            data_ph=cur.fetchall()
            qry='select email_id from employees'
            cur.execute(qry)
            data_e=cur.fetchall()
            
            if e_password =='' or e_ph_number == '' or e_city == '' or e_state == '' or first_name=='' or email_id=='':
                st.error('Enter all details')
            elif e_password!=re_e_password:
                st.error('pasword should be same')
            elif len(email_id)<11:
                st.error('enter correct email id')
            elif email_id.endswith('@gmail.com')==False:
                st.warning('Enter correct email id')
            elif (email_id,) in data_e:
                st.error('email id exists')
            
            else:
                qry='select e_ph_number from employees '
                cur.execute(qry)
                data_ph=cur.fetchall()
                if (e_ph_number,) in data_ph:
                    st.error('Phone number exists')
                elif phnumber_r.startswith('9')==False:
                    st.error('Enter correct phone number')
                elif len(e_ph_number)!=10:
                    st.error('Enter correct phone number')
                else:
                    for i in e_ph_number:
                        if i not in '1234567890':
                            st.warning('Enter correct phone number')
                            break
                    else:
                        qry='insert into employees (e_name,e_password,e_ph_number,e_city,e_state,email_id) values(%s,%s,%s,%s,%s,%s)'
                        val=(e_name,e_password,e_ph_number,e_city,e_state,email_id)
                        cur.execute(qry,val)
                        con.commit()
                        
                        qry='select e_id from employees where email_id=%s'
                        val=(email_id,)
                        cur.execute(qry,val)
                        data=cur.fetchall()
                        eid=data[0][0]

                        email_sender ='appukuttykr@gmail.com'
                        email_receiver =email_id
                        subject = 'LOGIN DETAILS'
                        password = 'bcbk dcxt aewp nwwe'
                        body='Dear '+e_name.upper()+' , Thank you for becoming our employee \n\n'
                        body1='LOGIN ID : '+eid+'\n'+'PASSWORD : '+e_password
                        
                        msg =MIMEMultipart()
                        msg['From'] = email_sender
                        msg['To'] = email_receiver
                        msg['Subject'] = subject
                        msg.attach(MIMEText(body, "plain"))
                        msg.attach(MIMEText(body1, "plain"))

                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        server.login(email_sender, password)
                        server.sendmail(email_sender, email_receiver, msg.as_string())
                        server.quit()

                        st.info('Thank you for becoming our employee ')
                        st.balloons() 
    
    
    elif sig=='login':
        st.title('Employee Login')
        e_id=st.text_input('employee ID')
        e_password=st.text_input('Password',type='password')
        if st.button("E_LOGIN",on_click=callback) or st.session_state.button_clicked:
            p=st.progress(0)
            for i in range(100):
                time.sleep(0.0001)
                p.progress(i+1)
            qry='select e_id from employees '
            cur.execute(qry)
            data=cur.fetchall()
            if (e_id,) not in data:
                st.error('employee id does not exits')
            else:
                qry='select e_password from employees where e_id=%s'
                val=(e_id,)
                cur.execute(qry,val)
                data=cur.fetchall()
                if (e_password,) not in data:
                    st.error('incorrect password')
                else:
                    sel=st.radio('CHOICE ',['PRODUCT_VIEW','PRODUCT_UPDATE','PRODUCT_ADD','YOUR_UPDATE'])
                    if sel=='PRODUCT_VIEW':
                        st.title('PRODUCT_VIEW')
                        view()
                    elif sel=='PRODUCT_UPDATE':
                        view()
                        st.title('PRODUCT_UPDATE')
                        p_update()
                    elif sel=='PRODUCT_ADD':
                        st.title('PRODUCT_ADD')
                        view()
                        p_insert()
                    elif sel=='YOUR_UPDATE':
                        st.title('YOUR_UPDATE')
                        eupdate(e_id)