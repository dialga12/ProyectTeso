import sys
from Beta import *

# Implementation of the Alpha interface in the IDL
def main():
    print "1)", sys.argv[1]
    lo = Beta()
    llOk = lo.Dispatch(sys.argv[1])
    print llOk
    print lo.pcData
    print lo.pcError


main()

