import yaml
import json

def main():
    '''
    This program takes a list including a dictionary with 2 keys
    and writes it out to a file using the users choice of either 
    yaml expanded or json forms
    '''

    nl ="\n"
    arange = range(5)

    adict = {'key1':'val1','key2':'val2','key3':arange}

    alist =['string1','string2',adict,arange]


    fn = raw_input("name output file: ")

    ft =""
    while (ft != "yaml" or ft != "json"):
        ft = raw_input("enter yaml or json:").strip('\n\r')
        ft = ft.strip('\n\r')
        pr= "you entered:'"+ft+"'"
        print nl,pr
        if ft == "yaml" :
            with open(fn+".yml", "w") as fh:
                fh.write("---\n\n")    
                fh.write(yaml.dump(alist, default_flow_style =False))
            break
        elif ft == "json" :
            with open(fn+".json","w") as fh:
                json.dump(alist,fh)
            break
        else:
            print nl,"type exactly yaml or json",nl
            continue

if __name__=="__main__":
    main()
