import sqlite3

conn = sqlite3.connect('test.db')

# create Db
#
# conn.execute('''
# CREATE TABLE Users(
# ID INTEGER PRIMARY KEY AUTOINCREMENT,
# NAME TEXT NOT NULL,
# SALUTATION TEXT NOT NULL,
# AGE INT NOT NULL,
# RATING FLOAT NOT NULL,
# USERNAME VARCHAR(20) UNIQUE,
# PASSWORD VARCHAR(100) NOT NULL,
# CURRENT_STATUS_MESSAGE VARCHAR(250)
# )''')
# # #Loading data in Database
# #
# with open("user_details.csv", "rb") as user_details:
#     import csv
#     read_obj = csv.reader(user_details)
#     for row in read_obj:
#         name = row[0]
#         salutation = row[1]
#         username = row[2]
#         age = int(row[3])
#         rating = float(row[4])
#         password = row[5]
#         conn.execute("INSERT INTO USERS(NAME,SALUTATION,USERNAME,PASSWORD,AGE,RATING)\
#                       VALUES (?,?,?,?,?,?)", (name, salutation, username, password, age, rating));
# conn.commit()


# class Users:
#
#     @classmethod
#     def show_user_details(cls):
#         cursor = conn.execute("SELECT id, name,username, age, password,rating from USERS")
#         print 'GOT data'
#         for row in cursor:
#             print "ID = ", row[0]
#             print "NAME = ", row[1]
#             print "USERNAME = ", row[2]
#             print "AGE = ", row[3]
#             print "PASSWORD = ", row[4]
#             print "RATING = ", row[5]

conn.execute('''DROP TABLE Friend''')
conn.execute('''
CREATE TABLE Friend(
ID INTEGER PRIMARY KEY AUTOINCREMENT,
Userid INT NOT NULL ,
FriendId INT NOT NULL ,
FOREIGN KEY(Userid) REFERENCES Users(ID),
FOREIGN KEY(FriendId) REFERENCES Users(ID)
)''')
conn.commit()

