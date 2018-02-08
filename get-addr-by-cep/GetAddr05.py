#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GetAddr05.py: How to get a address using a webservice and a CEP number.
This only works in Brazil and may not work for every CEP. The official database,
if i'm not mistaken, is owned by the Post Office (Correios) and it's not free.

Same as GetAddr04, but now we'll handle more exceptions.
"""

__author__      = "Breno RdV"
__copyright__   = "Breno RdV @ raccoon.ninja"
__contact__     = "http://raccoon.ninja"
__license__     = "MIT"
__version__     = "01.001"
__maintainer__  = "Breno RdV"
__status__      = "Demonstration"


import requests
from requests.exceptions import *

base_url = "http://api.postmon.com.br/v1/cep/%s" 
google_cep_num = "30170010" #Google's office in Belo Horizonte, MG. Brazil.


cep_num = ""
print("Input your CEP number or press Enter to use our default test value.")
print("To exit, type -1 and press Enter.")
while cep_num != "-1":
    cep_num = input("Please, enter your CEP (just numbers): ")
    should_exit = cep_num == "-1"
    if cep_num.strip() == "":
        print("Using default test value...")
        cep_num = google_cep_num
    elif not cep_num.isdigit() and not should_exit:
        print("Please, enter CEP number... just the numbers.")
        continue

    if not should_exit:
        response = requests.get(base_url % cep_num)
        if response.status_code == 200:
            try:
                data = response.json()
                print(data)
            except ConnectionError as coe:
                print("[ERROR!]")
                print("\tConnection error. Are you connected to the internet?")
                print("\tTechnical details:\r\n\t%s" % coe)

            except Timeout as toe:
                print("[ERROR!]")
                print("\tError! Request timedout.")
                print("\tTechnical details:\r\n\t%s" % toe)

            except HTTPError as hpe:
                print("[ERROR!]")
                print("\tSomething went wrong.\r\n\tStatus code: %s" % response.status_code)
                print("\tFind more info about this error at: https://www.google.com.br/search?q=http+status+code+%s" % response.status_code)
                print("\tTechnical details:\r\n\t%s" % hpe)

            except TooManyRedirects as tre:
                print("[ERROR!]")
                print("\tError! Too Many Redirects...")
                print("\tTechnical details:\r\n\t%s" % tre)
                
            except RequestException as ree:
                print("[ERROR!]")
                print("\tSomething went wrong with the request...")
                print("\tHere's the technical details:\r\n\t%s" % ree)          

            except Exception as why:
                print("[ERROR!]")
                print("\tWell... i was not expecting that. Sorry...")
                print("\tTechnical details:\r\n\t%s" % why)                
                

        else:
            print("Something went wrong.\r\nStatus code: %s" % response.status_code)
            print("Find more info about this error at: https://www.google.com.br/search?q=http+status+code+%s" % response.status_code)
    
    else:
        print("Cancelling operation.")
