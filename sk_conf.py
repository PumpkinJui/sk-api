from json import load
from json.decoder import JSONDecodeError

checklt = {
    "KEY": [None,str,True],
    "stream": [False,bool,False],
    "balance_chk": [False,bool,False]
}

def confDefault():
    confD = {}
    for m,n in checklt.items():
        confD[m] = n[0]
    return confD

def confCheck(confG):
    confC = {}
    for m,n in confG.items():
        if checklt.get(m) == None:
            print('WRN: Invalid key name {}.'.format(m))
        elif checklt.get(m)[1] != type(n):
            print('WRN：Invalid key value {}.'.format(m))
        else:
            confC[m] = n
    return confC

def confMerge(confD,confC):
    confD.update(confC)
    for m,n in confD.items():
        if checklt.get(m)[2] and n == None:
            print('ERR: Required key name {} undefined or invalid.'.format(m))
            confD = False
    return confD

def confGet(confFile):
    try:
        with open(confFile,'r') as confR:
            confG = load(confR)
        print('Configurations read!')
    except FileNotFoundError:
        print('Configurations not exist.')
        print('Applying default configurations...')
        return confDefault()
    except JSONDecodeError:
        print('Invalid JSON format.')
        print('Applying default configurations...')
        return confDefault()
    return confMerge(confDefault(),confCheck(confG))
