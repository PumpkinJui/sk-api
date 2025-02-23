from json import load
from json.decoder import JSONDecodeError
from types import MappingProxyType as mpt

checklt_ori = {
    "stream": (True,False),
    "balance_chk": (True,False),
    "long_prompt": (False,False),
    "tool_use": (True,False),
    "autotime": (True,False),
    "service": ({
        "DS": ({
            "KEY": ("",True),
            "model": ("prompt",False)
        },False),
        "GLM": ({
            "KEY": ("",True),
            "model": ("prompt",False),
            "jwt": (True,False)
        },False),
        "KIMI": ({
            "KEY": ("",True),
            "model": ("prompt",False)
        },False),
        "QWEN": ({
            "KEY": ("",True),
            "model": ("prompt",False),
            "version": ("latest",False)
        },False),
        "SIF": ({
            "KEY": ("",True),
            "model": ("prompt",False),
            "pro": (False,False)
        },False)
    },True)
}

checklt = mpt(checklt_ori)

def conf_default(ref:dict=checklt) -> dict:
    default_conf = {}
    for m,n in ref.items():
        if n[1] or isinstance(n[0],dict):
            continue
        default_conf[m] = n[0]
    return default_conf

def conf_check(user_conf:dict,ref:dict) -> dict:
    checked_conf = {}
    for m,n in user_conf.items():
        if not ref.get(m):
            print(f'WRN: "{m}" is an invalid key.')
        elif not isinstance(ref.get(m)[0],type(n)):
            print(f'WRN：Key "{m}" has an invalid value.')
        elif isinstance(ref.get(m)[0],dict):
            if not n:
                print(f'WRN: Key "{m}" has an empty dict.')
            else:
                checked_conf[m] = conf_check(n,ref.get(m)[0])
        else:
            checked_conf[m] = n
    return checked_conf

# pylint: disable-next=dangerous-default-value
def conf_merge(external_conf:dict,internal_conf:dict=conf_default(),ref:dict=checklt) -> dict:
    dele = []
    for m,n in external_conf.items():
        if isinstance(n,dict) and not conf_merge(n,conf_default(ref.get(m)[0]),ref.get(m)[0]):
            if not ref.get(m)[1]:
                dele.append(m)
                continue
            return {}
        internal_conf[m] = n
    __ = [(internal_conf.pop(i,None),external_conf.pop(i,None)) for i in dele]
    if conf_required_check(internal_conf,ref):
        return key_check(internal_conf)
        # return internal_conf
    return {}

def conf_required_check(required_conf:dict,ref:dict) -> dict:
    for m,n in ref.items():
        if n[1] and not required_conf.get(m):
            print(f'ERR: Key "{m}" is required.')
            return {}
    return required_conf

def key_check(key_conf:dict) -> dict: # specific
    if ser := key_conf.get('service'):
        for m,n in ser.items():
            # print(m,n)
            if m == 'GLM':
                if '.' not in n.get('KEY'):
                    print('The KEY for GLM should be splitted with "." but there is none.')
                    return {}
            else:
                if n.get('KEY')[:3] != 'sk-':
                    print(f'The KEY for {m} should begin with "sk-".')
                    return {}
    return key_conf

def conf_get(conf_file:str) -> dict:
    try:
        with open(conf_file,'r',encoding='utf-8') as f:
            user_conf = load(f)
        print('INF: Configurations read!')
    except FileNotFoundError:
        print('ERR: Configurations not exist.')
        print('INF: Applying default configurations...')
        return conf_merge(conf_default())
    except JSONDecodeError:
        print('ERR: Invalid JSON format.')
        print('INF: Applying default configurations...')
        return conf_merge(conf_default())
    return conf_merge(conf_check(user_conf,checklt))

# print(conf_get('sk.json'))
