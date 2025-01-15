from json import load
from json.decoder import JSONDecodeError

checklt = {
    "KEY": ["",str,True],
    "stream": [True,bool,False],
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
            print('WRN: "{}" is an invalid key.'.format(m))
        elif checklt.get(m)[1] != type(n):
            print('WRN：Key "{}" has an invalid value.'.format(m))
        else:
            confC[m] = n
    return confC

def confMerge(confD,confC):
    confD.update(confC)
    for m,n in confD.items():
        if checklt.get(m)[2] and n == checklt.get(m)[0]:
            print('ERR: Key "{}" is required.'.format(m))
            confD = False
    return confD

def confGet(confFile):
    try:
        with open(confFile,'r') as confR:
            confG = load(confR)
        print('INF: Configurations read!')
    except FileNotFoundError:
        print('ERR: Configurations not exist.')
        print('INF: Applying default configurations...')
        return confMerge(confDefault(),{})
    except JSONDecodeError:
        print('ERR: Invalid JSON format.')
        print('INF: Applying default configurations...')
        return confMerge(confDefault(),{})
    return confMerge(confDefault(),confCheck(confG))
