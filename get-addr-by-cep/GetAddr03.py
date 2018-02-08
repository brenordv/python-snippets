#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GetAddr03.py: How to get a address using a webservice and a CEP number.
This only works in Brazil and may not work for every CEP. The official database,
if i'm not mistaken, is owned by the Post Office (Correios) and it's not free.

Same as GetAddr02, but now we'll ask the user for a CEP number and validate it 
before sending to the webservice.
"""

__author__      = "Breno RdV"
__copyright__   = "Breno RdV @ raccoon.ninja"
__contact__     = "http://raccoon.ninja"
__license__     = "MIT"
__version__     = "01.001"
__maintainer__  = "Breno RdV"
__status__      = "Demonstration"


import requests

base_url = "http://api.postmon.com.br/v1/cep/%s" 
google_cep_num = "30170010" #Google's office in Belo Horizonte, MG. Brazil.


cep_num = ""
print("Input your CEP number or press Enter to use our default test value.")
print("To exit, type -1 and press Enter.")
while not cep_num.isdigit() and cep_num != "-1":
    cep_num = input("Please, enter your CEP (just numbers): ")
    if cep_num.strip() == "":
        print("Using default test value...")
        cep_num = google_cep_num

if cep_num != "-1":
    response = requests.get(base_url % cep_num)
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print("Something went wrong.\r\nStatus code: %s" % response.status_code)
        print("Find more info about this error at: https://www.google.com.br/search?q=http+status+code+%s" % response.status_code)

else:
    print("Cancelling operation.")
