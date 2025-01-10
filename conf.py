from json import load
from json.decoder import JSONDecodeError

checklt = {
    "KEY": [None,str,True],
    "stream": [False,bool,False]
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
            print('警告：{} 键是一个无效键。'.format(m))
        elif checklt.get(m)[1] != type(n):
            print('警告：{} 键的对应值不合法。'.format(m))
        else:
            confC[m] = n
    return confC

def confMerge(confD,confC):
    confD.update(confC)
    for m,n in confD.items():
        if checklt.get(m)[2] and n == None:
            print('错误：{} 键未指定或指定的值不合法。'.format(m))
            confD = False
    return confD

def confGet(confFile):
    try:
        with open(confFile,'r') as confR:
            confG = load(confR)
        print('配置文件读取成功！')
    except FileNotFoundError:
        print('配置文件不存在，将使用默认配置...')
        return confDefault()
    except JSONDecodeError:
        print('配置文件不合 JSON 语法，将使用默认配置...')
        return confDefault()
    return confMerge(confDefault(),confCheck(confG))
