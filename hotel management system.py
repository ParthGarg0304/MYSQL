from datetime import datetime
import mysql.connector
from sys import exit
HOST = "localhost"
USER = "root"
PASSWORD = ""
DATABASE = "hotel"

def get_database():
    try:
        database = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        cursor = database.cursor(dictionary=True)
        return database, cursor
    except mysql.connector.Error:
        return None, None
ROOMS_TABLE_NAME = "rooms"

class Room:
    def __init__(self):
        self.room_id = 0
        self.room_no = 0
        self.floor = ""
        self.beds = ""
        self.available = ""
    def create(self, room_id, room_no, floor, beds, available):
        self.room_id = room_id
        self.room_no = room_no
        self.floor = floor
        self.beds = beds
        self.available = available
        return self
    def create_from_record(self, record):
        self.room_id = record['id']
        self.room_no = record['room_no']
        self.floor = record['floor']
        self.beds = record['beds']
        self.available = record['available']
        return self
    def print_all(self):
        print(str(self.room_id).ljust(3),
              str(self.room_no).ljust(15),
              self.floor.ljust(15),
              str(self.beds).ljust(15),
              str(self.available).ljust(15))
    def print_full(self):
        print_bar()
        print("Record #", self.room_id)
        print("Room No: ", self.room_no)
        print("Floor: ", self.floor)
        print("Beds: ", self.beds)
        print("available: ", self.available)
        print_bar()
        
def create_room():
    room_id = None
    room_no = int(input("Enter the room no: "))
    floor = input("Enter the floor (Ex. ground, first etc.): ")
    beds = int(input("Enter number of beds: "))
    available = True
    return Room().create(room_id, room_no, floor, beds, available)

def print_room_header():
    print("="*100)
    print("id".ljust(3),
          "room no".ljust(15),
          "floor".ljust(15),
          "beds".ljust(15),
          "available".ljust(15)
          )
    print("="*100)
    
def create_rooms_table(database):
    cursor = database.cursor()
    cursor.execute("DROP table if exists {0}".format(ROOMS_TABLE_NAME))
    cursor.execute("create table {0} ("
                   "id int primary key auto_increment,"
                   "room_no int,"
                   "floor varchar(50),"
                   "beds int,"
                   "available bool)".format(ROOMS_TABLE_NAME))
    
def add_room(database, cursor):
    room = create_room()
    query = "insert into {0}(room_no,floor,beds,available) values({1},'{2}',{3},{4})".\
            format(ROOMS_TABLE_NAME, room.room_no, room.floor, room.beds, room.available)
    try:
        cursor.execute(query)
        database.commit()
    except mysql.connector.Error as err:
        create_rooms_table(database)
        cursor.execute(query)
        database.commit()
    print("Operation Successful")
    
def show_room_record(cursor, query):
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        if cursor.rowcount == 0:
            print("No Matching Records")
            return
        record = records[0]
        room = Room().create_from_record(record)
        room.print_full()
        return room
    except mysql.connector.Error as err:
        print(err)
        
def show_room_records(cursor, query):
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        if cursor.rowcount == 0:
            print("No Matching Records")
            return
        print_room_header()
        for record in records:
            room = Room().create_from_record(record)
            room.print_all()
        return records
    except mysql.connector.Error as err:
        print(err)
        
def get_and_print_room_by_no(cursor):
    room_no = int(input("Enter the room no: "))
    query = "select * from {0} where room_no={1}".format(ROOMS_TABLE_NAME, room_no)
    room = show_room_record(cursor, query)
    return room

def edit_room_by_room_no(database, cursor):
    room = get_and_print_room_by_no(cursor)
    if room is not None:
        query = "update {0} set".format(ROOMS_TABLE_NAME)
        print("Input new values (leave blank to keep previous value)")
        room_no = input("Enter new room no: ")
        if len(room_no) > 0:
            query += " room_no={0},".format(room_no)
        floor = input("Enter new floor: ")
        if len(floor) > 0:
            query += " floor='{0}',".format(floor)
        beds = input("Enter number of beds: ")
        if len(beds) > 0:
            query += " beds={0},".format(beds)
        query = query[0:-1] + " where id={0}".format(room.room_id)
        confirm = input("Confirm Update (Y/N): ").lower()
        if confirm == 'y':
            cursor.execute(query)
            database.commit()
            print("Operation Successful")
        else:
            print("Operation Cancelled")
            
def change_room_status(database, cursor, room_id, available):
    query = "update {0} set available={1} where id={2}".format(ROOMS_TABLE_NAME, available, room_id)
    cursor.execute(query)
    database.commit()
    
def delete_room_by_room_no(database, cursor):
    room = get_and_print_room_by_no(cursor)
    if room is not None:
        confirm = input("Confirm Deletion (Y/N): ").lower()
        if confirm == 'y':
            query = "delete from {0} where id={1}".format(ROOMS_TABLE_NAME, room.room_id)
            cursor.execute(query)
            database.commit()
            print("Operation Successful")
        else:
            print("Operation Cancelled")
            
def room_menu(database, cursor):
    while True:
        print()
        print("============================")
        print("==========Room Menu=========")
        print("============================")
        print()
        print("1. Add new room")
        print("2. Get room details by room no")
        print("3. Find available rooms by number of beds")
        print("4. Edit Room details")
        print("5. Delete room")
        print("6. View all rooms")
        print("0. Go Back")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            add_room(database, cursor)
        elif choice == 2:
            room_no = int(input("Enter the room no: "))
            query = "select * from {0} where room_no={1}".format(ROOMS_TABLE_NAME, room_no)
            show_room_records(cursor, query)
        elif choice == 3:
            beds = int(input("Enter number of beds required: "))
            query = "select * from {0} where beds={1}".format(ROOMS_TABLE_NAME, beds)
            show_room_records(cursor, query)
        elif choice == 4:
            edit_room_by_room_no(database, cursor)
        elif choice == 5:
            delete_room_by_room_no(database, cursor)
        elif choice == 6:
            query = "select * from {0}".format(ROOMS_TABLE_NAME)
            show_room_records(cursor, query)
        elif choice == 0:
            break
        else:
            print("Invalid choice (Press 0 to go back)")
            
CUSTOMER_TABLE_NAME = "customers"

class Customer:
    def __init__(self):
        self.customer_id = 0
        self.name = ""
        self.address = ""
        self.phone = ""
        self.room_no = "0"
        self.entry_date = ""
        self.checkout_date = ""
    def create(self, customer_id, name, address, phone, room_no, entry_date, checkout_date):
        self.customer_id = customer_id
        self.name = name
        self.address = address
        self.phone = phone
        self.room_no = room_no
        self.entry_date = entry_date
        self.checkout_date = checkout_date
        return self
    def create_from_record(self, record):
        self.customer_id = record['id']
        self.name = record['name']
        self.address = record['address']
        self.phone = record['phone']
        self.room_no = record['room_no']
        self.entry_date = record['entry']
        self.checkout_date = record['checkout']
        return self
    def print_all(self):
        print(str(self.customer_id).ljust(3),
              self.name[0:15].ljust(15),
              self.address[0:15].ljust(15),
              self.phone.ljust(15),
              str(self.room_no).ljust(10),
              self.entry_date.strftime("%d-%b-%y").ljust(15),
              (self.checkout_date.strftime("%d %b %y") if self.checkout_date is not None else "None").ljust(15))
    def print_full(self):
        print_bar()
        print("Customer #", self.customer_id)
        print("Name: ", self.name)
        print("Address: ", self.address)
        print("Phone: ", self.phone)
        print("Checked in to room #", self.room_no, " on ", self.entry_date.strftime("%d %b %y"))
        print("Checkout: ", self.checkout_date.strftime("%d %b %y") if self.checkout_date is not None else None)
        print_bar()
def create_customer(room_no):
    customer_id = None
    name = input("Enter the name: ")
    address = input("Enter the address: ")
    phone = input("Enter the phone: ")
    entry_date = datetime.now()
    return Customer().create(customer_id, name, address, phone, room_no, entry_date, None)
def print_customer_header():
    print("="*100)
    print("id".ljust(3),
          "name".ljust(15),
          "address".ljust(15),
          "phone".ljust(15),
          "room no".ljust(10),
          "entry".ljust(15),
          "check out".ljust(15))
    print("="*100)


def create_customer_table(database):
    cursor = database.cursor()
    cursor.execute("DROP table if exists {0}".format(CUSTOMER_TABLE_NAME))
    cursor.execute("create table {0} ("
                   "id int primary key auto_increment,"
                   "name varchar(20),"
                   "address varchar(50),"
                   "phone varchar(10),"
                   "room_no int,"
                   "entry datetime,"
                   "checkout datetime)".format(CUSTOMER_TABLE_NAME))
NUMBER_OF_RECORDS_PER_PAGE = 10
def add_customer(database, cursor):
    room = get_and_print_room_by_no(cursor)
    if room is not None:
        customer = create_customer(room.room_no)
        confirm = input("Complete the operation? (Y/N) ").lower()
        if confirm == 'y':
            query = "insert into {0}(name, address, phone, room_no, entry) values('{1}','{2}','{3}',{4},'{5}')". \
                format(CUSTOMER_TABLE_NAME, customer.name, customer.address, customer.phone,
                       customer.room_no, customer.entry_date.strftime("%Y-%m-%d %H:%M:%S"))
            try:
                cursor.execute(query)
                database.commit()
            except mysql.connector.Error:
                create_customer_table(database)
                cursor.execute(query)
                database.commit()
            change_room_status(database, cursor, room.room_id, False)
            print("Operation Successful")
        else:
            print("Operation Canceled")
def show_customer_records(cursor, query):
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        if cursor.rowcount == 0:
            print("No Matching Records")
            return
        print_customer_header()
        for record in records:
            customer = Customer().create_from_record(record)
            customer.print_all()
        return records
    except mysql.connector.Error as err:
        print(err)
def show_customer_record(cursor, query):
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        if cursor.rowcount == 0:
            print("No Matching Records")
            return
        record = records[0]
        customer = Customer().create_from_record(record)
        customer.print_full()
        return customer
    except mysql.connector.Error as err:
        print(err)
def get_and_print_customer_by_room_no(cursor):
    room = get_and_print_room_by_no(cursor)
    if room is not None:
        query = "select * from {0} where room_no={1} order by id desc limit 1".format(CUSTOMER_TABLE_NAME, room.room_no)
        customer = show_customer_record(cursor, query)
        return room, customer
    return None, None
def check_out(database, cursor):
    room, customer = get_and_print_customer_by_room_no(cursor)
    if room is not None and customer is not None:
        confirm = input("Confirm checkout? (Y/N): ")
        if confirm == 'y':
            checkout = datetime.now()
            query = "update {0} set checkout='{1}' where id={2}".\
                format(CUSTOMER_TABLE_NAME, checkout.strftime("%Y-%m-%d %H:%M:%S"), customer.customer_id)
            cursor.execute(query)
            database.commit()
            change_room_status(database, cursor,room.room_id, True)
            print("Operation Successful")
        else:
            print("Operation Cancelled")
def edit_customer_by_room_no(database, cursor):
    room, customer = get_and_print_customer_by_room_no(cursor)
    if room is not None and customer is not None:
        query = "update {0} set".format(CUSTOMER_TABLE_NAME)
        print("Input new values (leave blank to keep previous value)")
        name = input("Enter new name: ")
        if len(name) > 0:
            query += " name='{0}',".format(name)
        address = input("Enter new address: ")
        if len(address) > 0:
            query += " address='{0}',".format(address)
        phone = input("Enter number of phone: ")
        if len(phone) > 0:
            query += " phone='{0}',".format(phone)
        query = query[0:-1] + " where id={0}".format(customer.customer_id)
        confirm = input("Confirm Update (Y/N): ").lower()
        if confirm == 'y':
            cursor.execute(query)
            database.commit()
            print("Operation Successful")
        else:
            print("Operation Cancelled")
def delete_customer_by_room_no(database, cursor):
    room, customer = get_and_print_customer_by_room_no(cursor)
    if room is not None and customer is not None:
        confirm = input("Confirm Deletion (Y/N): ").lower()
        if confirm == 'y':
            query = "delete from {0} where id={1}".format(CUSTOMER_TABLE_NAME, customer.customer_id)
            cursor.execute(query)
            database.commit()
            print("Operation Successful")
        else:
            print("Operation Cancelled")
def customer_menu(database, cursor):
    while True:
        print()
        print("==============================")
        print("==========Customer Menu=========")
        print("==============================")
        print()
        print("1. New Customer")
        print("2. Show Customer Details by name")
        print("3. Show customer details by customer_id")
        print("4. Show customer details by address")
        print("5. Show customer details by phone number")
        print("6. Show customer details by room no")
        print("7. Show customer details by check in date")
        print("8. Show current list of customers")
        print("9. Check out")
        print("10. Edit customer Details")
        print("11. Delete Customer record")
        print("12. View all customers")
        print("0. Go Back")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            add_customer(database, cursor)
        elif choice == 2:
            name = input("Enter the name: ").lower()
            query = "select * from {0} where name like '%{1}%'".format(CUSTOMER_TABLE_NAME, name)
            show_customer_records(cursor, query)
        elif choice == 3:
            customer_id = input("Enter the customer id: ")
            query = "select * from {0} where id = {1}".format(CUSTOMER_TABLE_NAME, customer_id)
            show_customer_record(cursor, query)
        elif choice == 4:
            address = input("Enter the address: ").lower()
            query = "select * from {0} where address like '%{1}%'".format(CUSTOMER_TABLE_NAME, address)
            show_customer_records(cursor, query)
        elif choice == 5:
            phone = input("Enter the phone number: ")
            query = "select * from {0} where phone like '%{1}%'".format(CUSTOMER_TABLE_NAME, phone)
            show_customer_records(cursor, query)
        elif choice == 6:
            room_no = input("Enter the room_no: ")
            query = "select * from {0} where room_no = {1}".format(CUSTOMER_TABLE_NAME, room_no)
            show_customer_record(cursor, query)
        elif choice == 7:
            print("Enter the check in date: ")
            day = int(input("day of month: "))
            month = int(input("month: "))
            year = int(input("year: "))
            query = "select * from {0} where date(entry) = '{1}-{2}-{3}'".format(CUSTOMER_TABLE_NAME, year, month, day)
            show_customer_records(cursor, query)
        elif choice == 8:
            query = "select * from {0} where checkout is null".format(CUSTOMER_TABLE_NAME)
            show_customer_records(cursor, query)
        elif choice == 9:
            check_out(database, cursor)
        elif choice == 10:
            edit_customer_by_room_no(database, cursor)
        elif choice == 11:
            delete_customer_by_room_no(database, cursor)
        elif choice == 12:
            query = "select * from {0}".format(CUSTOMER_TABLE_NAME)
            show_customer_records(cursor, query)
        elif choice == 0:
            break
        else:
            print("Invalid choice (Press 0 to go back)")
if __name__ == '__main__':
    database, cursor = get_database()
    if database is None:
        print("The Database does not exist or not accessible.")
        exit(1)
    while True:
        print()
        print_center("==============================")
        print_center("=====Galaxy Hotel=====")
        print_center("==============================")
        print_center("1. Manage Rooms")
        print_center("2. Manage Customers")
        print_center("0. Exit")
        print()
        choice = int(input_center("Enter your choice: "))
        if choice == 1:
            room_menu(database, cursor)
        elif choice == 2:
            customer_menu(database, cursor)
        elif choice == 0:
            break
        else:
            print("Invalid choice (Press 0 to exit)")
    print_center("GoodBye")
