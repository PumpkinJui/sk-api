import json
from time import time
from traceback import print_exc
import requests
from jwt import encode
from sk_conf import confGet

def exitc(reason:str='') -> None:
    if reason:
        print(reason)
    raise SystemExit

def conf_read() -> dict:
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
    if not confR.get('tool_use'):
        del conf['tools']
    if not confR.get('balance_chk'):
        if service_conf.get('model'):
            model_name = service_model(
                'model',
                service_info.get('models'),
                True,
                service_conf.get('model')
            )
        else:
            model_name = service_model(
                'model',
                service_info.get('models'),
                True
            )
        confR['model'] = model_name
    confR.update(service_info)
    del confR['models']
    return confR

def service_model(keyword:str,lt:tuple,lower:bool=True,sts:str='prompt') -> str:
    if sts != 'prompt' and sts not in lt:
        print(f'WRN: {sts} is not a valid {keyword}.')
    if sts != 'prompt' and sts in lt:
        print(f'INF: {keyword.capitalize()} {sts} selected.')
        return sts
    if len(lt) > 1:
        print(f'INF: Multiple {keyword}s available.')
        print('INF: Select one from below by name.')
        print('TIP: Case insensitive.')
        print('TIP: Fragments accepted; guessed by order.')
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
                print(f'INF: Selection accepted: {chn}.')
                return chn
            else:
                for i in lt:
                    if chn in i:
                        print(f'INF: Selection guessed: {i}. Accepted.')
                        return i
            print('ERR: Selection invalid.')
    print(f'INF: {keyword.capitalize()} {lt[0]} in use.')
    return lt[0]

def service_infoget(service:str) -> dict:
    info = {
        'DSK': {
            'name': 'DSK',
            'full_name': 'DeepSeek',
            'cht_url': 'https://api.deepseek.com/chat/completions',
            'chk_url': 'https://api.deepseek.com/user/balance',
            'models': ('deepseek-chat',),
            'temp_range': (2,1.00),
            'max_tokens': 8192,
            'tools': None
        },
        'GLM': {
            'name': 'GLM',
            'full_name': 'GLM',
            'cht_url': 'https://open.bigmodel.cn/api/paas/v4/chat/completions',
            'chk_url': None,
            'models': (
                'glm-zero-preview',
                'glm-4-plus',
                'glm-4-air-0111',
                'glm-4-airx',
                'glm-4-flash',
                'glm-4-flashx',
                'glm-4-long',
                'glm-4-alltools',
                'charglm-4',
                'emohaa',
                'codegeex-4'),
            'temp_range': (1,0.95),
            'max_tokens': None,
            'tools': [{
                "type": "web_search",
                "web_search": {"enable": True}
            }]
        }
    }
    return info.get(service)

def token_gen() -> str:
    if not conf.get('jwt'):
        return conf.get('KEY')
    KEYs = conf.get('KEY').split(".")
    if len(KEYs) == 3:
        return conf.get('KEY')
    if len(KEYs) != 2:
        exitc('ERR: Invalid KEY.')
    payload = {
        "api_key": KEYs[0],
        "exp": int(round(time() * 1000)) + 60 * 1000,
        "timestamp": int(round(time() * 1000)),
    }
    return encode(
        payload,
        KEYs[1],
        algorithm="HS256",
        headers={"alg": "HS256", "sign_type": "SIGN"},
    )

def headers_gen(contype:bool=True) -> dict:
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token_gen()}'
    }
    if contype:
        headers['Content-Type'] = 'application/json'
    # print(headers)
    return headers

def data_gen(msg:list,temp:float,stream:bool) -> str:
    payload = {
        "messages": msg,
        "model": conf.get('model'),
        "max_tokens": conf.get('max_tokens'),
        "temperature": temp,
        "stream": stream
    }
    if conf.get('tool_use'):
        payload["tools"] = conf.get('tools')
    payload_json = json.dumps(payload)
    # print(msg,payload_json,sep='\n')
    return payload_json

def temp_get() -> float:
    while True:
        try:
            temp = input('TEMPERATURE: ')
            if temp == '':
                print()
                return conf.get('temp_range')[1]
            temp = round(float(temp),2)
            if not 0 <= temp <= conf.get('temp_range')[0]:
                raise
            print()
            return temp
        except:
            print('ERR: Temperature invalid.')
            print(f'TIP: 0 <= temp <= {conf.get("temp_range")[0]}.')
            print(f'TIP: Leave blank to use default ({conf.get("temp_range")[1]}).')

def usr_get(rnd:int) -> dict:
    print(f'USER #{rnd}')
    lines = []
    nul_count = 0
    while True:
        line = input()
        if conf.get('long_prompt'):
            if line == '':
                if nul_count:
                    del lines[-1]
                    break
                nul_count += 1
            elif nul_count:
                nul_count = 0
        else:
            if line == '':
                break
        lines.append(line)
    if not lines:
        exitc('INF: Null input, chat ended.')
    usr = '\n'.join(lines)
    return {'role': 'user', 'content': usr}

def ast_nostream(msg:list,temp:float) -> None:
    rsp = requests.request(
        "POST",
        conf.get('cht_url'),
        headers=headers_gen(),
        data=data_gen(msg,temp,False)
    )
    if rsp.status_code == requests.codes.ok:
        ast = json.loads(rsp.text)['choices'][0]['message']['content']
        print(ast)
        msg.append({'role': 'assistant', 'content': ast})
        print()
    else:
        exitc('ERR: {} {}'.format(
            rsp.status_code,
            json.loads(rsp.text)['error']['message']
        ))

def ast_stream(msg:list,temp:float) -> None:
    ast = ''
    rsp = requests.request(
        "POST",
        conf.get('cht_url'),
        headers=headers_gen(),
        data=data_gen(msg,temp,True),
        stream=True
    )
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
        exitc('ERR: {} {}'.format(
            rsp.status_code,
            json.loads(rsp.text)['error']['message']
        ))

def balance_chk() -> None:
    payload={}
    rsp = requests.request(
        "GET",
        conf.get('chk_url'),
        headers=headers_gen(False),
        data=payload
    )
    if rsp.status_code == requests.codes.ok:
        exitc('INF: {} {} left in the {} balance.'.format(
            json.loads(rsp.text)['balance_infos'][0]['total_balance'],
            json.loads(rsp.text)['balance_infos'][0]['currency'],
            conf.get('full_name')
        ))
    else:
        exitc('ERR: {} {}'.format(
            rsp.status_code,
            json.loads(rsp.text)['error']['message']
        ))

def chat() -> None:
    msg = []
    rnd = 0
    temp = temp_get()
    sys = input('SYSTEM\n')
    if sys == '':
        sys = 'You are a helpful assistant.'
    msg.append({'role': 'system', 'content': sys})
    print()
    while True:
        rnd += 1
        msg.append(usr_get(rnd))
        print(f'ASSISTANT #{rnd}')
        if not conf.get('stream'):
            ast_nostream(msg,temp)
        else:
            ast_stream(msg,temp)

try:
    conf = conf_read()
    print()
    if conf.get('balance_chk'):
        if conf.get('chk_url'):
            balance_chk()
        exitc(f'ERR: Balance check is unsupported for {conf.get('full_name')}.')
    chat()
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
