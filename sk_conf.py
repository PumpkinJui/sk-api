from json import load
from json.decoder import JSONDecodeError

checklt = {
    "stream": [True,bool,False],
    "balance_chk": [True,bool,False],
    "long_prompt": [False,bool,False],
    "tool_use": [True,bool,False],
    "service": [{
        "DSK": [{
            "KEY": ["",str,True],
            "model": ["prompt",str,False]
        },dict,False],
        "GLM": [{
            "KEY": ["",str,True],
            "model": ["prompt",str,False],
            "jwt": [True,bool,False]
        },dict,False]
    },dict,True]
}

def confDefault(ref:dict=checklt) -> dict:
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

def confCheck(confG:dict,ref:dict=checklt) -> dict:
    confC = {}
    for m,n in confG.items():
        if not ref.get(m):
            print(f'WRN: "{m}" is an invalid key.')
        elif ref.get(m)[1] != type(n):
            print(f'WRN：Key "{m}" has an invalid value.')
        elif ref.get(m)[1] == dict:
            if not n:
                print(f'WRN: Key "{m}" has an empty dict.')
            else:
                confC[m] = confCheck(n,ref.get(m)[0])
        else:
            confC[m] = n
    return confC

def confMerge(confE:dict,confI:dict=confDefault(),ref:dict=checklt) -> dict:
    if confRcheck(confE,ref):
        for m,n in confE.items():
            if m not in confI:
                confI[m] = n
            elif isinstance(n,dict):
                if not confMerge(n,confI.get(m),ref.get(m)[0]):
                    return {}
            else:
                confI[m] = n
        return KEYcheck(confI)
        # return confI
    return {}

def confRcheck(confR:dict,ref:dict=checklt) -> dict:
    for m,n in ref.items():
        if n[2] and not confR.get(m):
            print(f'ERR: Key "{m}" is required.')
            return {}
    return confR

def KEYcheck(confK:dict) -> dict: # specific
    if confK.get('service'):
        if confK.get('service').get('GLM') and not confK.get('service').get('GLM').get('KEY'):
            del confK['service']['GLM']
        for m,n in confK.get('service').items():
            if m == 'GLM':
                if '.' not in n.get('KEY'):
                    print('The KEY for GLM should be splitted with "." but there is none.')
                    return {}
            else:
                if n.get('KEY')[:3] != 'sk-':
                    print(f'The KEY for {m} should begin with "sk-".')
                    return {}
    return confK

def confGet(confFile:str) -> dict:
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

# print(confGet('sk.json'))
