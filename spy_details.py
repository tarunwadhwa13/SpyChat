from datetime import datetime
from passlib.hash import pbkdf2_sha256

class Spy:
    def __init__(self, name, salutation, age, rating):
        self.name = name
        self.salutation = salutation
        self.age = age
        self.rating = rating
        self.current_status_message = None
        self.is_online = True


class Admin(Spy):
    def __init__(self, name, salutation, age, rating,password):
        Spy.__init__(self,name,salutation,age,rating)
        self.is_online = True
        self.chats = []
        self.password = password

    def show_profile(self):
        print 'Name :' + self.salutation + self.name
        print 'Age :' + self.age
        print 'Name :' + self.rating
        print 'Your Status :' + self.current_status_message

    def change_rating(self):
        self.rating = float(raw_input("Enter new rating"))

    def change_password(self):
        self.password = pbkdf2_sha256.hash(raw_input("Enter new password :"))


class ChatMessage:

  def __init__(self, message, sent_by_me):
    self.message = message
    self.time = datetime.now()
    self.sent_by_me = sent_by_me


friends = []