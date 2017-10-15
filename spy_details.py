from datetime import datetime
from passlib.hash import pbkdf2_sha256
STATUS_MESSAGES = ['My name is Bond, James Bond', 'Shaken, not stirred.','Hey there']


class Spy:
    def __init__(self, name, salutation,username, age, rating):
        self.name = name
        self.salutation = salutation
        self.username = username
        self.age = age
        self.rating = rating
        self.current_status_message = None
        self.is_online = True

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
            message_selection = input("\nChoose from the above messages ")
            if len(STATUS_MESSAGES) >= message_selection:
                updated_status_message = STATUS_MESSAGES[message_selection - 1]

        if updated_status_message != self.current_status_message:
            try:
                import sqlite3
                conn = sqlite3.connect('test.db')
                conn.execute("UPDATE USERS set CURRENT_STATUS_MESSAGE = ? where ID = ?",(self.current_status_message))
                conn.commit
            except:
                print 'Couldn\'t save changes in the database'

        return updated_status_message


class Admin(Spy):
    def __init__(self, name, salutation,username, age, rating,password):
        Spy.__init__(self,name,salutation,username,age,rating)
        self.is_online = True
        self.chats = []
        self.password = password

    def show_profile(self):
        print 'Name :' + self.salutation + self.name
        print 'Age %d:'%(self.age)
        print 'Name %f:'%(self.rating)
        print 'Your Status :' + self.current_status_message


    def change_password(self):
        self.password = pbkdf2_sha256.hash(raw_input("Enter new password :"))


class ChatMessage:

  def __init__(self, message, sent_by_me):
    self.message = message
    self.time = datetime.now()
    self.sent_by_me = sent_by_me


friends = []