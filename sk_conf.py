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

def confDefault(ref:dict=checklt):
    confD = {}
    for m,n in ref.items():
        if n[1] == dict:
            q = confDefault(n[0])
            if q:
                confD[m] = q
            else:
                continue
        else:
            if n[2]:
                continue
            confD[m] = n[0]
    return confD

def confCheck(confG:dict,ref:dict=checklt):
    confC = {}
    for m,n in confG.items():
        if ref.get(m) == None:
            print('WRN: "{}" is an invalid key.'.format(m))
        elif ref.get(m)[1] != type(n):
            print('WRN：Key "{}" has an invalid value.'.format(m))
        elif ref.get(m)[1] == dict:
            if n == {}:
                print('WRN: Key "{}" has an empty dict.'.format(m))
            else:
                confC[m] = confCheck(n,ref.get(m)[0])
        else:
            confC[m] = n
    return confC

def confMerge(confE:dict,confI:dict=confDefault(),ref:dict=checklt):
    if confRcheck(confE,ref):
        for m,n in confE.items():
            if m not in confI:
                confI[m] = n
            elif type(n) == dict:
                if not confMerge(n,confI.get(m),ref.get(m)[0]):
                    return False
            else:
                confI[m] = n
        return KEYcheck(confI)
        # return confI
    else:
        return False

def confRcheck(confR:dict,ref:dict=checklt):
    for m,n in ref.items():
        if n[2] and not confR.get(m):
            print('ERR: Key "{}" is required.'.format(m))
            return False
    return confR

def KEYcheck(confK:dict): # specific
    if confK.get('series'):
        if not confK.get('series').get('GLM').get('KEY'):
            del confK['series']['GLM']
        for m,n in confK.get('series').items():
            if m == 'GLM':
                if '.' not in n.get('KEY'):
                    print('The KEY for GLM should be splitted with "." but there is none.')
                    return False
            else:
                if n.get('KEY')[:3] != 'sk-':
                    print('The KEY for {} should begin with "sk-".'.format(m))
                    return False
    return confK

def confGet(confFile:str):
    try:
        with open(confFile,'r') as confF:
            confG = load(confF)
        print('INF: Configurations read!')
    except FileNotFoundError:
        print('ERR: Configurations not exist.')
        print('INF: Applying default configurations...')
        return confMerge(confDefault())
    except JSONDecodeError:
        print('ERR: Invalid JSON format.')
        print('INF: Applying default configurations...')
        return confMerge(confDefault())
    return confMerge(confCheck(confG))

print(confGet('sk.json'))
