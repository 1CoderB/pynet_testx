#!/usr/bin/env python
from ciscoconfparse import CiscoConfParse as cc
from ciscoconfparse import IOSCfgLine as cf
from pprint import pprint as pp
linespec = r"^crypto\smap\sCRYPTO"
parentspec = linespec
childtofind = r"pfs\sgroup2"
missingchildspec = r"AES" 
tempparentvar=""
tempparsedconf =list()
tempchildspec= r"transform-set"

def reply(rpl):
    '''prints a reply from user entry'''
    print "\nYou entered: ", rpl,"\n"

def requestinfile():
    '''requests input filename and returns this as a string'''
    afile = raw_input("provide filepath\\name of the config file\n that you would like to parse. \nEnter z to use the default file from class: ")
    if afile in ('z','Z'):
        afile = "/home/bhaire/pynet_testx/cisco_ipsec.txt"
    try:
        reply(afile)
    except:
        print "reply failed"
    return afile

def requestoutfile():
    '''requests output file name and returns this as a string'''
    outfile = raw_input("provide name of output text file: ")
    if ".txt" not in outfile: outfile += ".txt"
    reply(outfile)
    return outfile

def rqstparenttofind():
    '''requests a string compares it to a local var and returns it'''
    global parentspec
    parent = raw_input("Enter regex string to locate. \nFormat: r^'astring' Enter z if you would like to use the default of r'^crypto\smap\sCRYPTO' ")
    if parent in ('z','Z'):
        parent = parentspec 
    reply(parent)
    return parent

def rqstchildtofind():
    global childtofind
    '''requests a string compares it to a global var and returns it'''
    print "\nNow we will request a child string to locate.\n"
    child = raw_input("Enter regex string to locate. Format: r'^set\spfs\sgroup2' Enter z to use this default string. ")
    if child in ('z','Z'):
        child = childtofind
    reply(child)
    return child

def rqstmissingchild():
    global missingchildspec
    ''' requests a string from the user compares it to a global var and returns it'''
    print "\nNow we will request the string that you want to avoid.\n"
    child = raw_input("Enter regex string to avoid. Format: r'^set\stransform-set\sAES.+' Enter z to use this default string. ")
    if child in ('z','Z'):
        child = missingchildspec
    reply(child)
    return child

def locobjswparent(parent,parsedc):
    #print "inside loc obj w parent, parent=",parent,"parsedc=",parsedc
    cryptomap = parsedc.find_objects(linespec=parent,exactmatch=False, ignore_ws=False)
    #print "cryptomap=",cryptomap
    return cryptomap

def locparentwchild(parent,child,parsedc):
    foundparents = parsedc.find_objects_w_child(parentspec=parent,childspec=child,ignore_ws=False)
    #print "foundparents in loc parent with child=",foundparents
    return foundparents

def locparentwochild(parent,child,parsedc):
    foundparents = parsedc.find_objects_wo_child(parentspec=parent,childspec=child,ignore_ws=False)
    return foundparents

def printparentandallchildren(foundobjects):
    '''iterates through a list of tuples fed from ciscoconfparse and
        prints parents on a line then a succsessive group of children on lines below'''
    global pp
    #print "inside printfunction foundobjects=",foundobjects
    
    for p in foundobjects:
        print p.text.rstrip('\r\n') #{:-10}'.format(p.text,'left aligned')
        chillins = p.children
        for c in chillins: print c.text.rstrip()

def printparentandspecchild(foundobjects,childstr):
    '''iterates through a list of tuples parsed by ciscoconfparse and prints the parents
       then it prints the children that contain the childstr''' 
    for p in foundobjects:
        print p.text.rstrip('\r\n') #'{:-10}'.format(p.text,'left aligned')
        chillins = p.children
        for c in chillins:
            if childstr in c.text:
            #children.has_line_with(childstr):
                print c.text.rstrip('\r\n') #'{4:}'.format(p.children.text,'left aligned')

def forclass8():
    '''Write a Python program using ciscoconfparse that parses a config, 
    finds all of the parent objects that begin with 'crypto map CRYPTO' and 
    prints out the children.'''
    global tempparentvar
    global tempparsedconf
    #print "\nstoring parsed config for next function...\n"
    tempparsedconf = parseconf()
    #print "\ntemppased=",tempparsedconf 
    #print "\nstoring parents for next function...\n"
    tempparentvar = rqstparenttofind()
    #print "\ntempparvar=", tempparentvar
    print "\nprinting crypto map entries and children\n"
    printparentandallchildren(locobjswparent(tempparentvar,tempparsedconf))    

def forclass9():
    '''Find all of the crypto map entries that are using PFS group2'''
    global tempparentvar
    global tempparsedconf
    print "\nfinding entries with pfs group 2\n"
    printparentandallchildren(locparentwchild(tempparentvar,rqstchildtofind(),tempparsedconf))  

def forclass10():
    '''find the crypto maps that are not using AES (based-on the transform set name). 
    Print these entries and their corresponding transform set name.'''
    global temparentvar
    global temparsedconf
    global tempchildspec
    print "\nfinding/printing entries that do not have a transform-set name including AES\n"
    printparentandspecchild(locparentwochild(tempparentvar,rqstmissingchild(),tempparsedconf),tempchildspec)
  

def parseconf():
    '''uses ciscoconfparse to return a list of tuples'''
    global cc
    #print "\nparsing config...\n"
    bbool =  False
    while bbool is False:
        try:
            with open(requestinfile()) as fh:
                parsed = cc(fh)
            #print "parsed=",parsed,"\n"
            return parsed
        except IOError:
            print "Bad file name: try again: "
            bbool = False
            continue
        bbool = True

def main():
    forclass8()
    forclass9()
    forclass10()
    print "\nScript Complete\n\n"
    
    

if __name__=="__main__":
    main()
