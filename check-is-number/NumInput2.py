#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""NumInput2.py: Simple demo of how to check if a user input is a number."""

__author__      = "Breno RdV"
__copyright__   = "Breno RdV @ raccoon.ninja"
__contact__     = "http://raccoon.ninja"
__license__     = "MIT"
__version__     = "01.000"
__maintainer__  = "Breno RdV"
__status__      = "Demonstration"


def is_number(num):
    
    """Tests to see if arg is number. """
    
    try:
        #Try to convert the input. 
        float(num)
        
        #If successful, returns true.
        return True
        
    except:
        #Silently ignores any exception.
        pass
    
    #If this point was reached, the input is not a number and the function
    #will return False.
    return False


def should_exit(user_input, exit_flag = "exit"):
    
    """Checks if the user input is the exit flag."""
    
    return user_input.lower().strip() == exit_flag


#Only runs this part if you execute this script directly.
if __name__ == "__main__":
    #Declaring the initial state of user_input variable. 
    #Just to make things easier...
    user_input = ""
    
    print("(To exit, type exit and press enter.)")
    
    #While the user do input the word exit, keep going...
    while(not should_exit(user_input)):
        
        #Asks the user for an input...
        user_input = input("Hello! Please, input a number: ")
        
        #Added this check just to make things a bit prettier.
        if not should_exit(user_input):
            #Tells the user if the input is a number or not.
            if is_number(user_input):
                print("Great! A valid number! :D You chose: %s" % user_input)
            else:
                print("Sorry. I'm pretty sure that '%s' is not a number." % user_input)
    
    #Says goodbye to the user.        
    print("\r\nOk. See you later.\r\nThanks for all the fish!")