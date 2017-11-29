from datetime import datetime
from passlib.hash import pbkdf2_sha256
STATUS_MESSAGES = ['My name is Bond, James Bond', 'Shaken, not stirred.','Hey there']
import sqlite3
user_list = []
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
        if self.current_status_message != None:
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

    # def show_friends(self):
    #     cursor = conn.execute("Select * from users where Friend.friendId = users.? and ",(self.id))


    @classmethod
    def load(cls):
        cursor = conn.execute("SELECT * from USERS")
        for row in cursor:
            temp_user = Users(id = row[0],name=row[1],salutation=row[2],age=row[3],rating=row[4],username=row[5],password=row[6],\
                              current_status_message=row[7])
            user_list.append(temp_user)
        return user_list

    @classmethod
    def write(cls, **kwargs):
        print 'Writing to Database!!'
        print kwargs
        name = kwargs['name']
        salutation = kwargs['salutation']
        username = kwargs['username']
        age = int(kwargs['age'])
        rating = float(kwargs['rating'])
        password = kwargs['password']
        try:
            conn.execute("INSERT INTO USERS(NAME,SALUTATION,USERNAME,PASSWORD,AGE,RATING)\
                                            VALUES (?,?,?,?,?,?)", (name, salutation, username, password, age, rating))
            conn.commit()
            Users.show_user_details()
        except:
            print 'Couldn\'t write to the database'


    @classmethod
    def show_user_details(cls):
        cursor = conn.execute("SELECT id, name,username, age, password,rating from USERS")
        print 'GOT data'
        for row in cursor:
            print "ID = ", row[0]
            print "NAME = ", row[1]
            print "USERNAME = ", row[2]
            print "AGE = ", row[3]
            print "PASSWORD = ", row[4]
            print "RATING = ", row[5]


class ChatMessage:

  def __init__(self, message, sent_by_me):
    self.message = message
    self.time = datetime.now()
    self.sent_by_me = sent_by_me


class Friend():

    def __init__(self,user_id):
        self.userid = user_id


    def save(self,spy):
        conn.execute("INSERT INTO FRIEND(Userid,FriendID) VALUES(?,?)",(spy.id,self.userid))
        conn.commit()

friends = []