from spy_details import friends,Spy
from steganography.steganography import Steganography
from datetime import datetime
import ctypes
from passlib.hash import pbkdf2_sha256
import csv

STATUS_MESSAGES = ['My name is Bond, James Bond', 'Shaken, not stirred.','Hey there']

users = []


def load_users():
    try:
        with open("user_details.csv","rb") as user_details:
            read_obj = csv.reader(user_details)
            for row in read_obj:
                new_user = Spy(name=row[0],salutation=row[1],age=int(row[2]),rating=float(row[3]),password=row[4])
                users.append(new_user)
        user_details.close()
        return users[0]
    except:
        print 'There was some error in loading friends. App may not work as expected'
    return None


def getpassword(username):
    for user in users:
        if user.name == username:
            return True,user
    return False,None


def login(username):
    count =0
    a, user_pass = getpassword(username)
    if not a:
        print 'User not found '
        print 'Please try signing up on our App'
        return False
    while count<3:
        passw = raw_input("Please enter your password to continue :")
        if pbkdf2_sha256.verify(passw, user_pass.password):
            return user_pass
        else:
            ctypes.windll.user32.MessageBoxA(0, "Wrong Password entered", "Password error", 1)
            count+=1
    print 'Too many Login attempts..\nExiting Program..'
    return None


def signup():
    spy_name = get_name()
    for user in users:
      if spy_name == user.name:
          print 'User with this username already exists. Please try another name'
          return signup()

    spy_salutation = get_salutation()
    spy_age = get_age()
    spy_rating = get_rating()
    spy = Spy('', '', 0, 0.0,'')
    spy.is_online = True
    spy.name = spy_name
    spy.salutation = spy_salutation
    spy.age = spy_age
    spy.rating = spy_rating
    user_pass = 'password'
    pass_verify = 'to verify password'
    while user_pass != pass_verify:
        user_pass = raw_input('Enter user Password :')
        pass_verify = raw_input('Verify Password :')
        if user_pass == pass_verify:
            continue
        print 'Passwords matching failed. Please try again'

    spy.password= pbkdf2_sha256.hash(user_pass)
    users.append(spy)
    try:
        with open("user_details.csv","ab") as user_data:
            write_obj = csv.writer(user_data)
            write_obj.writerow([spy_name,spy_salutation,spy_age,spy_rating,spy.password])
    except:
        print 'Write into file failed'
    print "Authentication complete. Welcome " + spy_name + " age: " + str(spy_age) + " and rating of: " + \
          str(spy_rating) + " Proud to have you Onboard"
    return spy


def start_chat(spy):
    show_menu = True
    current_status_message = None

    while show_menu :
        menu_choices = "What do you want to do? \n1. Add a status update\n2. Add a friend\n3. Select a friend" \
                       "\n4. Send a Message\n5. Read a Message\n6. Read chats\n7. Logout\n8. Check Your Profile\n9. Close application\n"
        menu_choice = int(raw_input(menu_choices))

        if menu_choice == 1:
            current_status_message = add_status(current_status_message)
        elif menu_choice == 2:
            len_friends = add_friend()
        elif menu_choice == 3:
            select_friend()
        elif menu_choice == 4:
            send_message()
        elif menu_choice == 5:
            read_message()
        elif menu_choice == 6:
            read_chats()
        elif menu_choice == 7:
            show_menu = False
        elif menu_choice == 8:
            show_profile(spy)
        else:
            exit(0)

    print 'Thank you for using spychat'


def add_status(current_status_message):
    updated_status_message = current_status_message
    if current_status_message != None:
      print "Your current status message is " + current_status_message + "\n"
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

    return updated_status_message


def add_friend():

    new_friend = Spy('','',0,0.0,None)
    new_friend.name = get_name()
    new_friend.salutation = get_salutation()
    new_friend.age = get_age()
    new_friend.rating = get_rating()
    try:
        friends.append(new_friend)
    except:
        print 'We couldn\'t add friend. Please try again or check log.'

    return len(friends)


def get_name():
    try:
        name = raw_input("Please enter your name to continue :")
        if len(name)>3 and name.isalpha():
            return name
        else:
            ctypes.windll.user32.MessageBoxA(0, "That doesnt look like a valid name. Please use alphabets [a-z] only",
                                             "Error", 1)
    except:
        print 'There was some error whiile processing your request. Please Try Again'
    return get_name()


def get_age():
    try:
        age = raw_input("Please enter your age to continue :")
        if age.isdigit():
            age = int(age)
            if age>12 and age<50:
                return age
            else:
                ctypes.windll.user32.MessageBoxA(0, "That doesnt look like a valid age. \
                        Please use digits [0-9] only.\nNote- Spy with age 12-50 are considered valid", "Error", 1)
    except:
        print 'There was some error whiile processing your request. Please Try Again'
    return get_age()


def get_salutation():
    try:
        salutation = raw_input("Please enter salutation :")
        if len(salutation)>=2 and salutation.isalpha():
            return salutation.title()
        else:
            ctypes.windll.user32.MessageBoxA(0,"That doesnt look like a valid salutation. Please use alphabets [a-z] only",
                                             "Error", 1)
    except:
        print 'There was some error whiile processing your request. Please Try Again'
    return get_salutation()


def get_rating():
    try:
        rating = raw_input("Please enter your rating to continue :")
        if rating.isdigit():
            rating = float(rating)
            if rating >0:
                return float(rating)
            else:
                print 'rating must be a positive float'
        else:
            ctypes.windll.user32.MessageBoxA(0, "Rating not valid", "Error", 1)
    except:
        print 'There was some error whiile processing your request. Please Try Again'
    return get_rating()


def select_friend():
    item_position = 1
    for i in friends:
        print str(item_position) + ' ' + i.name
        item_position = item_position+1;
    choice = input('Enter your choice')
    if len(friends)>=choice:
        return choice-1
    else:
        print 'Invalid option'
    return select_friend()


def send_message():
  friend_choice = select_friend()

  original_image = raw_input("What is the name of the image?")
  output_path = 'output.jpg'
  text = raw_input("What do you want to say?")
  Steganography.encode(original_image, output_path, text)

  new_chat = {
      "message": text,
      "time": datetime.now(),
      "sent_by_me": True
  }

  friends[friend_choice]['chats'].append(new_chat)
  print friends[friend_choice]['chats']
  print "Your secret message is ready!"


def read_message():
    friend_choice = select_friend()
    output_path = raw_input('ENter image path')
    secret_text = Steganography.decode(output_path)
    new_chat = {
        "message": secret_text,
        "time": datetime.now(),
        "sent_by_me": False
    }
    print new_chat['message']
    friends[friend_choice]['chats'].append(new_chat)
    print "Your secret message is ready!"


def read_chats():
    friend_choice = select_friend()
    for chat in friends[friend_choice].chats:
        if chat.sent_by_me:
            print '[%s] %s: %s' % (
                chat.time.strftime("%b %d %Y %H:%M:%S") +  'You said ' + chat.message)
        else:
            print '[%s] %s read: %s' % (
            chat.time.strftime("%b %d %Y %H:%M:%S") + friends[friend_choice].name +
            chat.message)


def show_profile(spy):
    index = users.index(spy)
    show_options = True
    while show_options:
        print 'Name :%s\n' \
              'Age :%d\n' \
              'Rating :%.1f\n'%(spy.name,spy.age,float(spy.rating))
        print 'You can\n' \
              '1. Change your rating\n' \
              '2. Change your password\n' \
              '3. Get back to the main menu\n'
        choice = raw_input("Enter your choice to continue :")
        if choice.isdigit():
            choice = int(choice)
            if choice == 1:
                spy.rating = float(raw_input("Enter new rating :"))
            elif choice == 2:
                spy.password = pbkdf2_sha256.hash(raw_input("Enter new password :"))
            elif choice == 3:
                show_options = False
            else:
                print 'Invalid option selected'
        else:
            print 'Option must be an integer'
