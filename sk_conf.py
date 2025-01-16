from json import load
from json.decoder import JSONDecodeError

checklt = {
    "stream": [True,bool,False],
    "balance_chk": [False,bool,False],
    "series": [{
        "DSK": [{
            "KEY": ["",str,True]
        },dict,False],
        "GLM": [{
            "KEY": ["",str,True],
            "model": ["glm-4-flash",str,False],
            "jwt": [True,bool,False]
        },dict,False]
    },dict,True]
}

def confDefault():
    confD = {}
    for m,n in checklt.items():
        confD[m] = n[0]
    return confD

def confCheck(confG:dict,ref:dict):
    confC = {}
    for m,n in confG.items():
        if ref.get(m) == None:
            print('WRN: "{}" is an invalid key.'.format(m))
        elif ref.get(m)[1] != type(n):
            print('WRN：Key "{}" has an invalid value.'.format(m))
        elif ref.get(m)[1] == dict:
            confC[m] = confCheck(n,ref.get(m)[0])
        else:
            confC[m] = n
    return confC

def confMerge(confD:dict,confC:dict):
    confD.update(confC)
    return confRcheck(confD,checklt)

def confRcheck(confR:dict,ref:dict):
    for m,n in confR.items():
        if ref.get(m)[2]:
            if n == ref.get(m)[0]:
                print('ERR: Key "{}" is required.'.format(m))
                return False
        if n != ref.get(m)[0] and ref.get(m)[1] == dict:
            if not confRcheck(n,ref.get(m)[0]):
                return False
    return confR

def confGet(confFile:str):
    try:
        with open(confFile,'r') as confF:
            confG = load(confF)
        print('INF: Configurations read!')
    except FileNotFoundError:
        print('ERR: Configurations not exist.')
        print('INF: Applying default configurations...')
        return confRcheck(confDefault(),checklt)
    except JSONDecodeError:
        print('ERR: Invalid JSON format.')
        print('INF: Applying default configurations...')
        return confRcheck(confDefault(),checklt)
    return confMerge(confDefault(),confCheck(confG,checklt))
