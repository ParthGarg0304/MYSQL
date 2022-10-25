#importing my sql
import mysql.connector as connect
from datetime import date

fine_per_day=1.0 #global variable

def clear():
    for i in range(10):
        print()


def add_book():
    obj=connect.connect(host="localhost",user="root",passwd="Parth.garg*123#",database="Project")
    if not obj.is_connected():
        print("not connected sucessful")
    dbcursor=obj.cursor()
    title=input("enter book title ..")
    author=input("enter book author ..")
    pages=int(input("enter book page .."))
    price=int(input("enter book price .. "))
    publisher=input("enter publisher")
    edition=input("enter book edition .. ")
    type=input("enter book type")
    sql='insert into book(title,author,type,price,pages,publisher,edition,status) values ("'+title +'","'+author+'","'+type+'","'+str(price)+'","'+str(pages)+'","'+publisher+'","'+edition+'","available")'
    dbcursor.execute(sql)

    obj.close
    print("New Book Added Successfully")
    print("")
    print("")
    print("")
    wait=input("press any key to continue ...")

def add_member():
    obj=connect.connect(host="localhost",user="root",passwd="Parth.garg*123#",database="Project")
    if not obj.is_connected():
        print("not connected sucessful")
    dbcursor=obj.cursor()

    name=input("enter member name ..")
    clas=input("enter member class ..")
    address=input("enter member address ..")
    phone=input("enter member number ..")
    email=input("enter member email ..")
    sql='insert into member(name,class,address,phone,email) values("'+name+'","'+clas+'","'+address+'","'+phone+'","'+email+'")'
    dbcursor.execute(sql)

    obj.close
    print("New Member Added Successfully")
    print("")
    print("")
    print("")
    wait=input("press any key to continue ...")

def modify_book():
    obj=connect.connect(host="localhost",user="root",passwd="Parth.garg*123#",database="Project")
    if not obj.is_connected():
        print("not connected sucessful")
    dbcursor=obj.cursor()

    print("modify book detail screen")
    print("-"*100)
    print("1.   Book title")
    print("2.   Book author")
    print("3.   Book publisher")
    print("4.   Book pages")
    print("5.   Book price")
    print("6.   Book edition")
    print("")
    print("")
    print("")
    ch=int(input("enter the choice of action"))
    field=''
    if ch==1:
        field='title'
    elif ch==2:
        field='author'
    elif ch==3:
        field='publisher'
    elif ch==4:
        field='pages'
    elif ch==5:
        field='price'
    elif ch==6:
        field='edition'
    book_id=input("enter book id ..")
    value=input("enter new value ..")
    if field=='pages' or field=='price':
        sql='update book set' +field+ '=' +value+' where id= '+book_id+';'
    else:
        sql='update book set' +field+ '='" +value+"' where id= '+book_id+';'

    dbcursor.execute(sql)

    obj.close
    print("book details modified Successfully")
    print("")
    print("")
    print("")
    wait=input("press any key to continue ...")
        
def modify_member():
    obj=connect.connect(host="localhost",user="root",passwd="Parth.garg*123#",database="Project")
    if not obj.is_connected():
        print("not connected sucessful")
    dbcursor=obj.cursor()

    print("modify member detail screen")
    print("-"*100)
    print("1.   name")
    print("2.   class")
    print("3.   address")
    print("4.   phone")
    print("5.   email")
    print("")
    print("")
    print("")
    ch=int(input("enter the choice of action"))
    field=''
    if ch==1:
        field='name'
    elif ch==2:
        field='class'
    elif ch==3:
        field='address'
    elif ch==4:
        field='phone'
    elif ch==5:
        field='email'

    member_id=input("enter member id ..")
    value=input("enter new value ..")
    sql='update member set' +field+ '="' +value+'" where id= '+member_id+';'
    dbcursor.execute(sql)

    obj.close
    print("member details modified Successfully")
    print("")
    print("")
    print("")
    wait=input("press any key to continue ...")

def member_issue_status(member_id):
    obj=connect.connect(host="localhost",user="root",passwd="Parth.garg*123#",database="Project")
    if not obj.is_connected():
        print("not connected sucessful")
    dbcursor=obj.cursor()
    sql='select * from transaction where m_id='+member_id+''
    dbcursor.execute(sql)
    result=dbcursor.fetchone()
    return result

    

def book_status(book_id):
    obj=connect.connect(host="localhost",user="root",passwd="Parth.garg*123#",database="Project")
    if not obj.is_connected():
        print("not connected sucessful")
    dbcursor=obj.cursor()
    sql='select * from book where id='+book_id+';'
    dbcursor.execute(sql)
    result=dbcursor.fetchone()
    return result[5]

def book_issue_status(book_id,member_id):
    obj=connect.connect(host="localhost",user="root",passwd="Parth.garg*123#",database="Project")
    if not obj.is_connected():
        print("not connected sucessful")
    dbcursor=obj.cursor()
    sql='select * from transaction where b_id='+book_id+' and m_id='+member_id+''
    dbcursor.execute(sql)
    result=dbcursor.fetchone()
    return result
    


def issue_book():
    obj=connect.connect(host="localhost",user="root",passwd="Parth.garg*123#",database="Project")
    if not obj.is_connected():
        print("not connected sucessful")
    dbcursor=obj.cursor()
    clear()

    print("Book issue Screen")
    print("-"*100)
    book_id=input("enter book id ..")
    member_id=input("enter member id ..")

    result=book_status(book_id)
    result1=member_issue_status(member_id)
    today=date.today()
    if len(result1)==0:
        if result=="available":
            sql='insert into transaction(b_id,m_id,doi) values('+book_id+','+member_id+',"'+str(today)+'");'
            sql_book='update book set status="issue" where id='+book_id+';'
            dbcursor.execute(sql)
            dbcursor.execute(sql_book)
            print("Book issued successfully")
        else:
            print("")
            print("")
            print("")
            print("book is not available for issue....current status:",result1)
    else:
        if len(result1)<1:
            sql='insert into transaction(b_id,m_id,doi) values('+book_id+','+member_id+',"'+str(today)+'");'
            sql_book='update book set status="issue" where id='+book_id+';'
            dbcursor.execute(sql)
            dbcursor.execute(sql_book)
            print("Book issued successfully")
        else:
            print("member already has book from the library")

    obj.close
    print("")
    print("")
    print("")
    wait=input("press any key to continue ...")


def return_book():
    obj=connect.connect(host="localhost",user="root",passwd="Parth.garg*123#",database="Project")
    if not obj.is_connected():
        print("not connected sucessful")
    dbcursor=obj.cursor()
    global fine_per_day
    clear()
    print("Book Return Screen")
    print("-"*100)
    book_id=input("enter book id ..")
    member_id=input("enter member id ..")
    today=date.today()
    result=book_issue_status(book_id,member_id)
    if result==None:
        print("Book was not issued...Check book id and member id")
    else:
        sql='update book set status="available" where id='+book_id+';'
        din=(today-result[3]).days
        fine=din*fine_per_day   ##fine per day
        sql1='update tranation set dor="'+str(today)+'" , fine='+str(fine)+' where b_id='+book_id+' and m_id='+member_id+';'

        dbcursor.execute(sql)
        dbcursor.execute(sql1)
        print("Book returned successfully")
        obj.close
        print("")
        print("")
        print("")
        wait=input("press any key to continue ...")


def search_book(field):
    obj=connect.connect(host="localhost",user="root",passwd="Parth.garg*123#",database="Project")
    if not obj.is_connected():
        print("not connected sucessful")
    dbcursor=obj.cursor()
    clear()

    print("BOOK SEARCH SCREEN")
    print("-"*100)
    msg='enter'+field+' value ..'
    title=input(msg)
    sql='select * from book where '+ field +' like %'+ title+'%'
    dbcursor.execute(sql)
    data=dbcursor.fetchall()
    print("")
    print("")
    print("")
    print("search result for:",field,":",title,)
    print("-"*100)
    for i in data:
        print(i)
          
    obj.close
    print("search completed Successfully")
    print("")
    print("")
    print("")
    wait=input("press any key to continue ...")
    

def search_menu():
    while True:
        print("SEARCH MENU")
        print("-"*100)
        print("1.   Book Title")
        print("2.   Book Author")
        print("3.   Publisher")
        print("4.   Exit to main menu")
        print("")
        print("")
        print("")
        ch=int(input("enter the choice of action"))
        field=''
        if ch==1:
            field='title'
        elif ch==2:
            field='author'
        elif ch==3:
            field='publisher'
        elif ch==4:
            break
        search_book(field)

    
def report_fine_collection():
    obj=connect.connect(host="localhost",user="root",passwd="Parth.garg*123#",database="Project")
    if not obj.is_connected():
        print("not connected sucessful")
    dbcursor=obj.cursor()

    dbcursor.execute("select sum(fine) from transaction")
    total=dbcursor.fetchone()
    print("total fine collected")
    print("-"*100)
    print("Rs",total[0])
    print("")
    print("")
    print("")
    wait=input("press any key to continue ...")
    

def report_menu():
    obj=connect.connect(host="localhost",user="root",passwd="Parth.garg*123#",database="Project")
    if not obj.is_connected():
        print("not connected sucessful")
    dbcursor=obj.cursor()
    
    while True:
        print('REPORT MENU')
        print("1.   Book list")
        print("2.   Member list ")
        print("3.   issued book")
        print("4.   available book")
        print("5.   weed out book")
        print("6.   stolen book")
        print("7.   lost book")
        print("8.   fine collection")
        print("9.   exit to main menu")
        print("")
        print("")


        ch=int(input("enter the choice of action"))
        if ch==1:
            print("Report book list")
            print("-"*100)
            dbcursor.execute("select * from book")
            data=dbcursor.fetchall()
            for i in data:
                print(i)
            wait=input("press any key to continue ...")
        elif ch==2:
            print("Report member list")
            print("-"*100)
            dbcursor.execute("select * from member")
            data=dbcursor.fetchall()
            for i in data:
                print(i)
            wait=input("press any key to continue ...")
        elif ch==3:
            print("Report issued book list")
            print("-"*100)
            dbcursor.execute("select * from book where status='issue'")
            data=dbcursor.fetchall()
            for i in data:
                print(i)
            wait=input("press any key to continue ...")
        elif ch==4:
            print("Report available book list")
            print("-"*100)
            dbcursor.execute("select * from book where status='available'")
            data=dbcursor.fetchall()
            for i in data:
                print(i)
            wait=input("press any key to continue ...")
        elif ch==5:
            print("Report weed out book list")
            print("-"*100)
            dbcursor.execute("select * from book where status='weed out'")
            data=dbcursor.fetchall()
            for i in data:
                print(i)
            wait=input("press any key to continue ...")
        elif ch==6:
            print("Report stolen book list")
            print("-"*100)
            dbcursor.execute("select * from book where status='stolen'")
            data=dbcursor.fetchall()
            for i in data:
                print(i)
            wait=input("press any key to continue ...")
        elif ch==7:
            print("Report lost book list")
            print("-"*100)
            dbcursor.execute("select * from book where status='lost'")
            data=dbcursor.fetchall()
            for i in data:
                print(i)
            wait=input("press any key to continue ...")
        elif ch==8:
            report_fine_collection()
        elif ch==9:
            break
        

def change_book_status(status,book_id):
    obj=connect.connect(host="localhost",user="root",passwd="Parth.garg*123#",database="Project")
    if not obj.is_connected():
        print("not connected sucessful")
    dbcursor=obj.cursor()
    sql='update book set status="'+status +'"where id='+book_id+ ' and status="available"'
    dbcursor.execute(sql)

    obj.close
    print("book status changed Successfully")
    print("")
    print("")
    print("")
    wait=input("press any key to continue ...")

        
def special_menu():
    while True:
        print('SPECIAL MENU')
        print("1.   Book Stolen")
        print("2.   Book Lost")
        print("3.   Book weed out")
        print("4.   return to menu")
        print("")
        print("")
        ch=int(input("enter the choice of action"))
        status=''
        if ch==1:
            status='stolen'
        elif ch==2:
            status='lost'
        elif ch==3:
            status='weed out'
        elif ch==4:
            break
        book_id=input("enter book id ..")
        change_book_status(status,book_id)
        
def main_menu():
    while True:
        clear()
        print('LIBRARY MENU')
        print("1.   Add Book")
        print("2.   Add Member")
        print("3.   Modify Book Information")
        print("4.   Modify Student information")
        print("5.   Issue Book")
        print("6.   Return Book")
        print("7.   Search Menu")
        print("8.   Report Menu")
        print("9.   Special Menu")
        print("0.   Close Application")
        print("")
        print("")


        ch=int(input("enter the choice of action"))
        if ch==1:
            add_book()
        elif ch==2:
            add_member()
        elif ch==3:
            modify_book()
        elif ch==4:
            modify_member()
        elif ch==5:
            issue_book()
        elif ch==6:
            return_book()
        elif ch==7:
            search_menu()
        elif ch==8:
            report_menu()
        elif ch==9:
            special_menu()
        elif ch==0:
            break


main_menu()
                    



