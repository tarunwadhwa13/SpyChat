from spy_details import friends,Users,Friend
from steganography.steganography import Steganography
from datetime import datetime
import ctypes
from passlib.hash import pbkdf2_sha256
import csv
import Validators as validators

usernames = []
user_list = Users.load()


def load_users():

        for user in user_list:
         usernames.append(user.username)

        # with open("user_details.csv","rb") as user_details:
        #     read_obj = csv.reader(user_details)
        #     for row in read_obj:
        #         name = row[0]
        #         salutation = row[1]
        #         username = row[2]
        #         age = int(row[3])
        #         rating = float(row[4])
        #         password = row[5]
        #         new_user = Users(name,salutation,username,age,rating,password)
        #         usernames.append(username)
        #         users.append(new_user)
        #
        # user_details.close()
        # Users.show_user_details()

        return user_list[0]


def getpassword(username):
    for user in user_list:
        if user.name == username:
            return True,user
    return False,None


def login(username):
    count = 0
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
    spy_username = get_username()
    spy_name = get_name()
    spy_salutation = get_salutation()
    spy_age = get_age()
    spy_rating = get_rating()
    spy = Users('', '','', 0, 0.0,'')
    spy.is_online = True
    spy.name = spy_name
    spy.username = spy_username
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
    print 'Passwords matched\nRegistering User.Please Wait...'
    spy.password= pbkdf2_sha256.hash(user_pass)
    user_list.append(spy)
    Users.write(name=spy.name,salutation=spy.salutation,username=spy_username,age=spy.age,rating=spy.rating,password=spy.password)
#     conn.execute("INSERT INTO USERS(NAME,SALUTATION,USERNAME,PASSWORD,AGE,RATING)\
#                   VALUES (?,?,?,?,?,?)", (spy.name, spy.salutation, spy.name, spy.password, spy.age, spy.rating))
    with open("user_details.csv","ab") as user_data:
        write_obj = csv.writer(user_data)
        write_obj.writerow([spy_name,spy_salutation,spy_username,spy_age,spy_rating,spy.password])

    print "Authentication complete. Welcome " + spy_name + " age: " + str(spy_age) + " and rating of: " + \
          str(spy_rating) + " Proud to have you Onboard"
    return spy


def start_chat(spy):
    show_menu = True

    while show_menu :
        menu_choices = "What do you want to do? \n1. Add a status update\n2. Add a friend\n3. Select a friend" \
                       "\n4. Send a Message\n5. Read a Message\n6. Read chats\n7. Logout\n8. Check Your Profile\n9. Close application\n"
        menu_choice = (raw_input(menu_choices))
        if menu_choice.isdigit():
            menu_choice = int(menu_choice)
            if menu_choice == 1:
                spy.change_status()
            elif menu_choice == 2:
                len_friends = add_friend(spy)
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


def add_friend(spy):

    # new_friend = Spy('','',0,0.0)
    # new_friend.name = get_name()
    # new_friend.salutation = get_salutation()
    # new_friend.age = get_age()
    # new_friend.rating = get_rating()
    # try:
    #     friends.append(new_friend)
    # except:
    #     print 'We couldn\'t add friend. Please try again or check log.'
    Users.show_user_details()
    index = spy.id
    print 'Spy id ' + str(spy.id)
    while index == spy.id:
        index = validators.get_int("Select friend to add as friend",1,len(user_list)+1)
        if index == spy.id:
            print 'You cant add yourself as friend'
    friend = Friend(user_id = index)
    friend.save(spy)
    friends.append(user_list[index-1])
    print 'Friend Added successfully'
    return len(friends)


def get_username():
    username = raw_input("Enter Username :")
    if username in usernames:
        print 'User with this username already exists. Please try another name !!'
        return get_username()
    return username


def get_name():
    try:
        return validators.get_alpha("Please enter your name to continue",3)
    except:
        print 'There was some error while processing your request. Please Try Again'
    return get_name()


def get_age():
    try:
       return validators.get_int("Please Enter your age",12,50)
    except:
        print 'There was some error whiile processing your request. Please Try Again'
    return get_age()


def get_salutation():
    try:
        return validators.get_alpha("Please Enter your Salutation",2,5).title()
    except:
        print 'There was some error whiile processing your request. Please Try Again'
    return get_salutation()


def get_rating():
    try:
        return validators.get_float("Please Enter a vallid rating",1.0,10.0)
    except:
        print 'There was some error whiile processing your request. Please Try Again'
    return get_rating()


def select_friend():
    item_position = 1
    if len(friends):
        for i in friends:
            print '%d %s %s aged %d with rating %.1f'%(item_position,i.salutation,i.name,i.age,i.rating)
            item_position = item_position+1
        choice = validators.get_int("Enter your choice",1,len(friends)+1)
        return choice-1

    else:
        print 'You dont have any friends'
    return None


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
    output_path = raw_input('Enter image path')
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
    if friend_choice:
        if len(friends[friend_choice].chats):
            for chat in friends[friend_choice].chats:
                if chat.sent_by_me:
                    print '[%s] %s: %s' % (
                        chat.time.strftime("%b %d %Y %H:%M:%S") +  'You said ' + chat.message)
                else:
                    print '[%s] %s read: %s' % (
                    chat.time.strftime("%b %d %Y %H:%M:%S") + friends[friend_choice].name
                    + chat.message)
        else:
            print 'You dont have any conversations'
    else:
        print 'You dont have any friend'


def show_profile(spy):
    show_options = True
    while show_options:
        spy.show_profile()
        print 'You can\n' \
              '1. Change your rating\n' \
              '2. Change your password\n' \
              '3. Get back to the main menu\n'
        choice = raw_input("Enter your choice to continue :")
        if choice.isdigit():
            choice = int(choice)
            if choice == 1:
                spy.change_rating()
            elif choice == 2:
                spy.change_password()
            elif choice == 3:
                show_options = False
            else:
                print 'Invalid option selected'
        else:
            print 'Option must be an integer'

