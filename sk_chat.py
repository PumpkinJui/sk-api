import json
from traceback import print_exc
import requests
from sk_conf import confGet

def exitc(reason:str=''):
    if reason:
        print(reason)
    raise SystemExit

def conf_read():
    confR = confGet('sk.json')
    if not confR:
        with open('sk.json','a'):
            pass
        exitc('TIP: Please check your conf file.')
    service_list = tuple(confR.get('service').keys())
    service_name = service_model('service',service_list,False)
    service_info = service_infoget(service_name)
    service_conf = confR['service'].get(service_name)
    del confR['service']
    confR.update(service_conf)
    confR['name'] = service_name
    if not confR.get('balance_chk'):
        model_name = service_model('model',service_info.get('models'),True,service_conf.get('model'))
        confR['model'] = model_name
    for p,q in service_info.items():
        if p == 'models':
            continue
        if q:
            confR[p] = q
    return confR

def service_model(keyword:str,lt:tuple,lower:bool=True,sts:str='prompt'):
    if sts != 'prompt' and sts not in lt:
        print(f'WRN: {sts} is not a valid {keyword}.')
    if sts != 'prompt' and sts in lt:
        print(f'INF: {keyword.capitalize()} {sts} selected.')
        return sts
    if len(lt) > 1:
        print(f'INF: Multiple {keyword}s available.')
        print('INF: Select one from below by name.')
        print('TIP: Case insensitive; fragments accepted.')
        k = 0
        max_len = 0
        for i in lt:
            max_len = max(max_len,len(i))
        while k < len(lt):
            if k % 2 == 0:
                print('INF:',lt[k].ljust(max_len),end='\t')
                k += 1
            else:
                print(lt[k])
                k += 1
        if k % 2 == 1:
            print()
        while True:
            if lower:
                chn = input('REQ: ').lower()
            else:
                chn = input('REQ: ').upper()
            if not chn:
                pass
            elif chn in lt:
                print('INF: Selection accepted:',chn)
                return chn
            else:
                for i in lt:
                    if chn in i:
                        print(f'INF: Selection guessed: {i}.')
                        return i
            print('ERR: Selection invalid.')
    print(f'INF: {keyword.capitalize()} {lt[0]} in use.')
    return lt[0]

def service_infoget(service:str):
    info = {
        'DSK': {
            'cht_url': 'https://api.deepseek.com/chat/completions',
            'chk_url': 'https://api.deepseek.com/user/balance',
            'models': ('deepseek-chat'),
            'temp_range': (True,2,1.00),
            'max_tokens': 8192
        },
        'GLM': {
            'cht_url': 'https://open.bigmodel.cn/api/paas/v4/chat/completions',
            'chk_url': None,
            'models': (
                'glm-zero-preview',
                'glm-4-plus',
                'glm-4-air-0111',
                'glm-4-long',
                'glm-4-airx',
                'glm-4-flashx',
                'glm-4-flash',
                'glm-4-alltools',
                'charglm-4',
                'emohaa',
                'codegeex-4'),
            'temp_range': (True,1,0.95),
            'max_tokens': None
        }
    }
    return info.get(service)

def headers_make(KEY:str,contype:bool=True):
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {KEY}'
    }
    if contype:
        headers['Content-Type']: 'application/json'
    return headers

def balance_chk(url:str):
    payload={}
    rsp = requests.request("GET", url, headers=headers_make(conf.get('KEY'),False), data=payload)
    if rsp.status_code == requests.codes.ok:
        exitc('INF: {} {} left in the DeepSeek balance.'.format(json.loads(rsp.text)['balance_infos'][0]['total_balance'],json.loads(rsp.text)['balance_infos'][0]['currency']))
    else:
        exitc('ERR: {} {}'.format(rsp.status_code,json.loads(rsp.text)['error']['message']))

def usr_get(rnd:int):
    print(f'User #{rnd}')
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    if not lines:
        exitc('Null input, chat ended.')
    usr = '\n'.join(lines)
    return {'role': 'user', 'content': usr}

def data_gen(msg:list,model:str,max_tokens:int,temp:float,stream:bool):
    payload = json.dumps({
        "messages": msg,
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temp,
        "stream": stream
    })
    return payload

def ast_nostream(url:str,headers:dict,msg:list,temp:float):
    # print(data_gen(msg,temp,False))
    rsp = requests.request("POST",url,headers=headers_make(conf.get('KEY')),data=data_gen(msg,temp,False))
    if rsp.status_code == requests.codes.ok:
        ast = json.loads(rsp.text)['choices'][0]['message']['content']
        print(ast)
        msg.append({'role': 'assistant', 'content': ast})
        print()
    else:
        exitc('ERR: {} {}'.format(rsp.status_code,json.loads(rsp.text)['error']['message']))

def ast_stream(url:str,headers:dict,msg:list,temp:float):
    # print(data_gen(msg,temp,True))
    ast = ''
    rsp = requests.request("POST",url,headers=headers_make(conf.get('KEY')),data=data_gen(msg,temp,True),stream=True)
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
        exitc('ERR: {} {}'.format(rsp.status_code,json.loads(rsp.text)['error']['message']))

def chat(stream:bool):
    url = "https://api.deepseek.com/chat/completions"
    msg = []
    rnd = 0

    while True:
        try:
            temp = input('Temperature: ')
            if temp == '':
                temp = 1.0
                break
            temp = round(float(temp),2)
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
        print(f'Assistant #{rnd}')
        if not stream:
            ast_nostream(url,headers,msg,temp)
        else:
            ast_stream(url,headers,msg,temp)

try:
    conf = conf_read()
    print(conf)
    print()

    if conf.get('balance_chk'):
        if conf.get('chk_url'):
            balance_chk(conf.get('chk_url'))
        exitc(f'ERR: Balance check is not supported for {conf.get('name')}.')

    chat(conf['KEY'],conf['stream'])
except SystemExit:
    pass
except KeyboardInterrupt:
    print()
    print('INF: Aborted.')
except:
    print()
    print_exc()
    print()
    print('ERR: Unexcepted error(s) occurred.')
    print('TIP: See above for more info.')
finally:
    pause = input('INF: Press Enter to exit...')
