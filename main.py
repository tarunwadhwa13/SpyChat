'''
    SpyChat by Tarun Wadhwa(tarunwadhwa13@gmail.com)
'''

#Import Statements
from functions import start_chat,login,signup,load_users,users


spy = load_users()
if spy:
    print '\t\t-----Welcome to SpyChat------\n'
    print 'This app is configured for {0} {1}'.format(spy.salutation, spy.name)
    while True:
        spy = users[0]
        response = raw_input("Do you want to continue as " + spy.salutation + " " + spy.name + "?(Y/N)")

        if response.upper() == "Y":
            print 'Welcome ' + spy.salutation + " " + spy.name
            if login(spy.name):
                start_chat(spy)
            else:
                exit(0)

        elif response.upper() == "N":
            choice = raw_input("You can \n1 Login(if registered)\n2 Or sign up as a new User :)")
            try:
                if int(choice) == 1:
                    username = raw_input("Enter your registered username :")
                    spy = login(username)
                    if spy:
                        start_chat(spy)
                    else:
                        print 'Login failed :('
                elif int(choice) == 2:
                        spy = signup()
                        start_chat(spy)

                else:
                    print 'Not a valid option i guess'
            except:
                'Error occured. Please try again later'


        else:
            print 'Invalid option. Shutting app down!'

else:
    spy = signup()
    start_chat(spy)