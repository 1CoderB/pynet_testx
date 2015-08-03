#!/usr/bin/env python
import yaml
import json


def printlist(nm,lst):
    '''
    This function prints a list after a banner with the list name using pprint
    the list and name are passes as parameters
    '''
    from pprint import pprint as pp
    banner = "*"*10
    nl="\n"
    print banner*5,nl
    print banner,"Printing %s list "%(nm),nl
    print banner*5,nl
    pp(lst)
    print nl*2
    

def main():
    '''
    this function requests a file and a file type yaml or json from the user
    it then prints the file using pretty print
    '''
    yamf = ""
    jf = ""

    while ".yml" not in yamf:
        yamf = raw_input("\nEnter name of yaml file: ")
        print "\nYou entered:",yamf

    while ".json" not in jf:
        jf = raw_input("\nEnter name of json file: ")
        print "\nYou entered: ",jf
    alist = []
    l=[yamf,jf]
    for x in l: 
        with open(x,"r") as fh:
            if ".yml" in x:
                alist = yaml.load(fh)
                printlist(x,alist)
            elif ".json" in x:
                alist = json.load(fh)
                printlist(x,alist)       
            else:
                print "\nFile type error."

if __name__ == "__main__":
    main()
