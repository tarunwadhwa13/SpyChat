import sqlite3
from datetime import datetime
from passlib.hash import pbkdf2_sha256
STATUS_MESSAGES = ['My name is Bond, James Bond', 'Shaken, not stirred.','Hey there']
user_list = []
friends = []
conn = sqlite3.connect('test.db')
import Validators as validator

class Users:
    def __init__(self,id, name, salutation,username, age, rating,password,current_status_message = None):
        # Spy.__init__(self,name,salutation,username,age,rating)
        self.id = id
        self.name = name
        self.salutation = salutation
        self.username = username
        self.age = age
        self.rating = rating
        self.is_online = True
        self.chats = []
        self.password = password
        self.current_status_message = current_status_message
        self.friends = []

    def change_rating(self):
        self.rating = float(raw_input("Enter new rating"))

    def change_status(self):
        updated_status_message = self.current_status_message
        if self.current_status_message is not None:
            print "Your current status message is " + self.current_status_message + "\n"
        else:
            print 'You don\'t have any status message currently \n'

        default = raw_input("Do you want to select from the older status (y/n)?")

        if default.upper() == "N":
            new_status_message = raw_input("What status message do you want to set?")

            if len(new_status_message) > 0:
                updated_status_message = new_status_message
                STATUS_MESSAGES.append(updated_status_message)

        elif default.upper() == 'Y':
            item_position = 1
            for message in STATUS_MESSAGES:
                print str(item_position) + ". " + message
                item_position = item_position + 1
            message_selection = validator.get_int("\nChoose from the above messages ",1,len(STATUS_MESSAGES)+1)
            updated_status_message = STATUS_MESSAGES[message_selection - 1]

        if updated_status_message != self.current_status_message:
            self.current_status_message = updated_status_message
            try:
                conn.execute("UPDATE USERS set CURRENT_STATUS_MESSAGE = ? where USERS.username is ?", (self.current_status_message,self.username))
                conn.commit
            except:
                print 'Couldn\'t save changes in the database'

        print 'Status Update successful'
        print 'Updated to ' + updated_status_message

        return updated_status_message

    def show_profile(self):
        print 'Name :' + self.salutation + self.name
        print 'Age %d:'%(self.age)
        print 'Name %f:'%(self.rating)
        print 'Your Status :' + self.current_status_message

    def change_password(self):
        self.password = pbkdf2_sha256.hash(raw_input("Enter new password :"))

    def load_friends(self):
        cursor = conn.execute("select * from Users where id in (Select FriendID from Friend where Friend.Userid = ?)",(self.id,))
        for row in cursor:
            temp_user = Users(id=row[0], name=row[1], salutation=row[2], age=row[3], rating=row[4], username=row[5],
                              password=row[6],current_status_message=row[7])
            friends.append(temp_user)
        return friends

    def load_chats(self):
        cursor = conn.execute("Select * from Chats where senderid=? or receiverid=?",(self.id,self.id))
        for row in cursor:
            temp_chat = ChatMessage(id = row[0],spy_id=row[1],friend_id=row[2],message=row[3],time=row[4],message_read=row[5])
            for friend in friends:
                if friend.id==row[2]:
                    friends[friends.index(friend)].chats.append(temp_chat)
                    break



    @classmethod
    def load(cls):
        cursor = conn.execute("SELECT * from USERS")
        for row in cursor:
            temp_user = Users(id = row[0],name=row[1],salutation=row[2],age=row[3],rating=row[4],username=row[5],password=row[6],\
                              current_status_message=row[7])
            user_list.append(temp_user)

        return user_list

    def save(self):
        print 'Writing to Database!!'
        try:
            conn.execute("INSERT INTO USERS(NAME,SALUTATION,USERNAME,PASSWORD,AGE,RATING)\
                                            VALUES (?,?,?,?,?,?)", (self.name, self.salutation, self.username, self.password, self.age, self.rating))
            conn.commit()
            self.id = conn.execute("select max(id) from Users")

        except:
            print 'Couldn\'t write to the database'


    @classmethod
    def show_user_details(cls):
        cursor = conn.execute("SELECT id, name,username, age, password,rating from USERS")
        for row in cursor:
            print "ID = ", row[0]
            print "NAME = ", row[1]
            print "USERNAME = ", row[2]
            print "AGE = ", row[3]
            print "PASSWORD = ", row[4]
            print "RATING = ", row[5]


class ChatMessage:

  def __init__(self,spy_id,friend_id, message,time,id=0,message_read=0):
    self.id = 0
    self.sender_id =  spy_id
    self.receiver_id = friend_id
    self.message = message
    self.time = time
    self.message_read = message_read

  def save(self):
      conn.execute("INSERT INTO CHATS(SENDERID,RECEIVERID,MESSAGE,DATETIME) VALUES(?,?,?,?)",(self.sender_id,self.receiver_id,self.message,self.time))
      conn.commit()
      cur = conn.execute('SELECT max(id) from Chats')
      self.id = cur.fetchone()[0]




class Friend():

    def __init__(self,user_id):
        self.userid = user_id


    def save(self,spy):
        conn.execute("INSERT INTO FRIEND(Userid,FriendID) VALUES(?,?)",(spy.id,self.userid))
        conn.commit()
