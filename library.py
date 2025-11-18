
import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",password="")
#CREATING DATABASE AND TABLE
mycursor=mydb.cursor()

db=input("Enter name of your database : ")   # input store

sql="create database if not exists %s"%(db,)  #mycursor.execute("create database if not exists store")
mycursor.execute(sql)
print("Databaes create Successfully.....")
mycursor.execute("use "+db)                         #database store

mycursor.execute("create table if not exists Available_Books(BookName varchar(30) primary key,Genre varchar(20),Quantity int(3),Author varchar(20),Publication varchar(30),Price int(4))")
mycursor.execute("create table if not exists Sell_rec(CustomerName varchar(20),PhoneNumber char(10) unique key, BookName varchar(30),Quantity int(100),Price int(4),foreign key (BookName) references Available_Books(BookName))")
mydb.commit()

print("""===============================================================
++++++++++++++++++++++++++ MY BOOK STORE +++++++++++++++++++++
===============================================================""")

while(True):
    print("""                    1:Add Books
                     2:Delete (Sold) Books
                     3:Search Books
                     4:Sell Record
                     5:Available Books
                     6:Total Income after the Latest Reset
                     7:Exit""")
    a=int(input("Enter your choice:"))
#ADD BOOKS
    if a==1:
        print("All information prompted are mandatory to be filled")
        book=str(input("Enter Book Name:"))
        genre=str(input("Genre:"))
        quantity=int(input("Enter quantity:"))
        author=str(input("Enter author name:"))
        publication=str(input("Enter publication house:"))
        price=int(input("Enter the unit price:"))
        mycursor.execute("select * from Available_Books where bookname='"+book+"'")
        row=mycursor.fetchone()
        print(row)
        if row is not None:
            mycursor.execute("update Available_Books set quantity=quantity+'"+str(quantity)+"' where bookname='"+book+"'")
            mydb.commit()
            print("""++++++++++++++++++++++++SUCCESSFULLY ADDED+++++++++++++++++++++++++""")
        else:
            mycursor.execute("insert into Available_Books(bookname,genre,quantity,author,publication,price) values('"+book+"','"+genre+"','"+str(quantity)+"','"+author+"','"+publication+"','"+str(price)+"')")
            mydb.commit()
            print("""++++++++++++++++++++++++SUCCESSFULLY ADDED++++++++++++++++++++++++""")

#DELETE BOOKS sell book
    elif a==2:
        print("AVAILABLE BOOKS...")
        mycursor.execute("select * from Available_Books ")
        for x in mycursor:
            print(x)
        cusname=str(input("Enter customer name:"))
        phno=int(input("Enter phone number:"))
        book=str(input("Enter Book Name:"))
        price=int(input("Enter the price:"))
        n=int(input("Enter quantity:"))
        mycursor.execute("select quantity from available_books where bookname='"+book+"'")
        lk=mycursor.fetchone()
        print(lk)
        if max(lk)<n:
            print(n,"Books are not available!!!!")
        else:
            mycursor.execute("select bookname from available_books where bookname='"+book+"'")
            log=mycursor.fetchone()
            print(log)
            if log is not None:
                mycursor.execute("insert into Sell_rec values('"+cusname+"','"+str(phno)+"','"+book+"','"+str(n)+"','"+str(price)+"')")
                mycursor.execute("update Available_Books set quantity=quantity-'"+str(n)+"' where BookName='"+book+"'")
                mydb.commit()
                print("""++++++++++++++++++++++++BOOK HAS BEEN SOLD++++++++++++++++++++++++""")
            

#SEARCH BOOKS ON THE BASIS OF GIVEN OPTIONS
    elif a==3:
        print("""1:Search by name
        2:Search by genre
        3:Search by author""")
        l=int(input("Search by?:"))
    #BY BOOKNAME
        if l==1:
            b=input("Enter Book to search:")
            mycursor.execute("select bookname from available_books where bookname='"+b+"'")
            tree=mycursor.fetchone()
            if tree!=None:
                print("""++++++++++++++++++++++BOOK IS IN STOCK++++++++++++++++++++++""")
                mycursor.execute("select * from available_books where bookname='"+b+"'")
                for x in mycursor:
                    print(x)
            else:
                print("BOOK IS NOT IN STOCK!!!!!!!")
    #BY GENRE
        elif l==2:
            g=input("Enter genre to search:")
            mycursor.execute("select genre from available_books where genre='"+g+"'")
            poll=mycursor.fetchall()
            if poll is not None:
                print("""++++++++++++++++++++++BOOK IS IN STOCK++++++++++++++++++++++""")
                mycursor.execute("select * from available_books where genre='"+g+"'")
                for y in mycursor:
                    print(y)
            else:
                print("BOOKS OF SUCH GENRE ARE NOT AVAILABLE!!!!!!!!!")
    #BY AUTHOR NAME
        elif l==3:
            au=input("Enter author to search:")
            mycursor.execute("select author from available_books where author='"+au+"'")
            home=mycursor.fetchall()
            if home is not None:
                print("""++++++++++++++++++++++BOOK IS IN STOCK++++++++++++++++++++++""")
                mycursor.execute("select * from available_books where author='"+au+"'")
                for z in mycursor:
                    print(z)
            else:
                print("BOOKS OF THIS AUTHOR ARE NOT AVAILABLE!!!!!!!")
            mydb.commit()

#SELL HISTORY
    elif a==4:
        print("1:Sell history details")
        print("2:Reset Sell history")
        ty=int(input("Enter your choice:"))
        if ty==1:
            mycursor.execute("select * from sell_rec")
            run=mycursor.fetchall()
            for u in run:
                print(u)
        if ty==2:
            bb=input("Are you sure(Y/N):")
            if bb=="Y":
                mycursor.execute("delete from sell_rec")
                mydb.commit()
            elif bb=="N":
                pass
#AVAILABLE BOOKS
    elif a==5:
        mycursor.execute("select * from available_books order by bookname")
        run=mycursor.fetchall()
        for v in run:
            print(v)
#TOTAL INCOME AFTER LATEST UPDATE
    elif a==6:
        mycursor.execute("select sum(price) from sell_rec")
        for x in mycursor:
            print(x)
#EXIT
    elif a==7:
        break

    else:
        print("Wrong choice ::")


