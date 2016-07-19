import sys
from CLogin import *
import json

# Implementation of the Alpha interface in the IDL
def main():
#    j = json.loads('{"one" : "1", "two" : "22222222222", "three" : "3"}')
#    print j['two']

    lo = CLogin()
    lo.pcCodUsu = '9999'
    lo.pcClave  = '999991'
    llOk = lo.omLogin()
    if not llOk:
       print lo.pcError
    else:
       print lo.pcData

main()

