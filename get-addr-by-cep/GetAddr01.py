#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GetAddr01.py: How to get a address using a webservice and a CEP number.
This only works in Brazil and may not work for every CEP. The official database,
if i'm not mistaken, is owned by the Post Office (Correios) and it's not free.

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
cep_num = "30170010" #Google's office in Belo Horizonte, MG. Brazil.

response = requests.get(base_url % cep_num)
data = response.json()

print(data)