import requests
import json
from sk_conf import *
from traceback import print_exc

def exitc(reason:str):
    if reason:
        print(reason)
    raise SystemExit

def confGen():
    try:
        with open('sk.json','r') as sk:
            SKjson = json.load(sk)
    except:
        SKjson = {}
    while True:
        try:
            print('INF: Enter your DeepSeek API KEY.')
            KEY = input('REQ: ')
            if KEY == '':
                raise
            break
        except:
            print('ERR: Null KEY.')
    SKjson['KEY'] = KEY
    with open('sk.json','w') as sk:
        json.dump(SKjson,sk)
    print('INF: Configurations saved!')
    print('INF: Applying new configurations...')
    return confMerge(confDefault(),confCheck(SKjson))

def balance_chk(KEY:str):
    url = "https://api.deepseek.com/user/balance"
    payload={}
    headers = {
      'Accept': 'application/json',
      'Authorization': 'Bearer {}'.format(KEY)
    }
    rsp = requests.request("GET", url, headers=headers, data=payload)
    if rsp.status_code == requests.codes.ok:
        exitc('INF: {} {} left in the DeepSeek balance.'.format(json.loads(rsp.text)['balance_infos'][0]['total_balance'],json.loads(rsp.text)['balance_infos'][0]['currency']))
    else:
        exitc('ERR: {} {}'.format(rsp.status_code,json.loads(rsp.text)['error']['message']))

def usr_get(rnd:int):
    print('User #{}'.format(rnd))
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    if lines == []:
        exitc('Null input, chat ended.')
    usr = '\n'.join(lines)
    return {'role': 'user', 'content': usr}

def data_gen(msg:list,temp:float,stream:bool):
    payload = json.dumps({
      "messages": msg,
      "model": "deepseek-chat",
      "max_tokens": 8192,
      "temperature": temp,
      "stream": stream
    })
    return payload

def ast_nostream(url:str,headers:dict,msg:list,temp:float):
    # print(data_gen(msg,temp,False))
    rsp = requests.request("POST", url, headers=headers, data=data_gen(msg,temp,False))
    if rsp.status_code == requests.codes.ok:
        ast = json.loads(rsp.text)['choices'][0]['message']['content']
        print(ast)
        msg.append({'role': 'assistant', 'content': ast})
        print()
    else:
        exitc('{} {}'.format(rsp.status_code,json.loads(rsp.text)['error']['message']))

def ast_stream(url:str,headers:dict,msg:list,temp:float):
    # print(data_gen(msg,temp,True))
    ast = ''
    rsp = requests.request("POST",url, headers=headers, data=data_gen(msg,temp,True),stream=True)
    if rsp.status_code == requests.codes.ok:
        for line in rsp.iter_lines():
            if line:
                data = line.decode('utf-8')[len('data:'):].strip()
                if data == '[DONE]':
                    break
                json_data = json.loads(data)
                delta = json_data['choices'][0]['delta'].get('content')
                ast += delta
                print(delta,end='',flush=True)
        msg.append({'role': 'assistant', 'content': ast})
        print()
        print()
    else:
        exitc('{} {}'.format(rsp.status_code,json.loads(rsp.text)['error']['message']))

def chat(KEY:str,stream:bool):
    url = "https://api.deepseek.com/chat/completions"
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': 'Bearer {}'.format(KEY)
    }
    msg = []
    rnd = 0

    while True:
        try:
            temp = input('Temperature: ')
            if temp == '':
                temp = 1.0
                break
            temp = round(float(temp),1)
            if not 0 <= temp <= 2:
                raise
            break
        except:
            print('Invalid temperature. Should be a float between 0.0 and 2.0, inclusive of the boundaries.')

    sys = input('     System: ')
    if sys == '':
        sys = 'You are a helpful assistant.'
    msg.append({'role': 'system', 'content': sys})

    print()

    while True:
        rnd += 1
        msg.append(usr_get(rnd))
        print('Assistant #{}'.format(rnd))
        if not stream:
            ast_nostream(url,headers,msg,temp)
        else:
            ast_stream(url,headers,msg,temp)

try:
    conf = confGet('sk.json')
    if not conf:
        conf = confGen()
    print()

    if conf['balance_chk']:
        balance_chk(conf['KEY'])

    chat(conf['KEY'],conf['stream'])
except SystemExit:
    pass
except KeyboardInterrupt:
    print()
    print('Aborted.')
except:
    print()
    print_exc()
    print()
    print('Unexcepted error(s) occurred.')
    print('See above for more info.')
finally:
    pause = input('Press Enter to exit...')
