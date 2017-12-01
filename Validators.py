"""
    Functions to perform validation checks on user, username ,password etc.
"""
import sys
import ctypes


def get_int(input_message,min_length=0,max_length=sys.maxint):
    var = raw_input(input_message)

    if var and var.isdigit():
        var = int(var)
        if var>=min_length and var<max_length:
            return var
        print 'Input not within Limits:'+ str(min_length) + ' to ' + str(max_length-1)
    else:
        ctypes.windll.user32.MessageBoxA(0, "That doesnt look like a valid input. Please use digits[0-9] only",
                                         "Error", 1)
    return get_int(input_message,min_length,max_length)


def get_alpha(input_message,min_length=0,max_length=sys.maxint, *args):
    var = raw_input(input_message)
    if var and var.isalpha():
        if var.__len__() >= min_length and var.__len__() < max_length:
            if len(args):
                if var.upper() in args[0]:
                    return var.upper()
                else:
                    print 'Not a valid option.Please try again'
            else:
                return var.upper()
        else:
            print 'Input not within Limits:' +str(min_length) + ' to ' + str(max_length-1)
    else:
        ctypes.windll.user32.MessageBoxA(0, "That doesnt look like a valid input. Please use alphabets [a-z] only",
                                         "Error", 1)
    return get_alpha(input_message,min_length,max_length,*args)


def get_float(input_message,min_length=0,max_length=sys.float_info.max):
    var = raw_input(input_message)
    if var:
        try:
            var = float(var)
            if var >= min_length and var < max_length:
                return var
            print 'Input not within Limits:' + str(min_length) + ' to ' + str(max_length-1)
        except:
            print "Not a float"
            return get_int(input_message, min_length, max_length)
    else:
        ctypes.windll.user32.MessageBoxA(0, "That doesnt look like a valid input. Please Enter a float Value",
                                         "Error", 1)
    return get_float(input_message,min_length,max_length)

