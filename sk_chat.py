"""The main functional system.

1. Read the conf.
2. If balance check is requested
   and the desired service supports it,
   run it and exit.
   If not, print an error message.
3. Run chat().

Can handle any of the following exceptions:

- SystemExit
  Normally requested by exitc() as a halfway exit.
- KeyboardInterrupt
  Ctrl+C exit requested by the user.
- requests.exceptions.Timeout
  ConnectTimeout or ReadTimeout, as a network issue.

Other exceptions will be printed for debugging.

No return provided.
The main code is at the bottom.
"""
# The documentation system structure:
# SUMMARY
# (blank)
# Running steps
# (blank)
# Exceptions
# (blank)
# Returns

from datetime import datetime,UTC # provide date to LLMs
import json # decode and encode
from traceback import print_exc # unexpected exceptions handling
import requests # GET and POST to servers
from jwt import encode # pass API KEY safely to supported services
from sk_conf import confGet # read conf

def exitc(reason:str='') -> None:
    """Halfway exit.

    Give a reason and raise SystemExit.

    No return provided.
    """
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
    if service_conf.get('model'):
        model_info = service_model(
            'model',
            service_info.get('models'),
            True,
            service_conf.get('model')
        )
    else:
        model_info = service_model(
            'model',
            service_info.get('models'),
            True
        )
    confR['model'] = model_info[0]
    confR['max_tokens'] = model_info[1]
    confR['tools'] = model_info[2]
    confR['msg'] = []
    confR['rnd'] = 0
    confR.update(service_info)
    del confR['models']
    # print(confR)
    return confR

def service_model(keyword:str,lst:tuple,lower:bool=True,sts:str='prompt') -> str:
    if isinstance(lst[0],tuple):
        lt = []
        for i in lst:
            lt.append(i[0])
        lt = tuple(lt)
    else:
        lt = lst
    if sts != 'prompt' and sts not in lt:
        print(f'WRN: {sts} is not a valid {keyword}.')
    if sts != 'prompt' and sts in lt:
        print(f'INF: {keyword.capitalize()} {sts} selected.')
        return lst[lt.index(sts)]
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
                return lst[lt.index(chn)]
            else:
                for m,n in enumerate(lt):
                    if chn in n:
                        print(f'INF: Selection guessed: {n}. Accepted.')
                        return lst[m]
            print('ERR: Selection invalid.')
    print(f'INF: {keyword.capitalize()} {lt[0]} in use.')
    return lst[0]

def service_infoget(service:str) -> dict:
    glm_tools = glm_tools_gen()
    info = {
        'DSK': {
            'name': 'DSK',
            'full_name': 'DeepSeek',
            'cht_url': 'https://api.deepseek.com/chat/completions',
            'chk_url': 'https://api.deepseek.com/user/balance',
            'models': (
                ('deepseek-chat',8192,None),
                ('deepseek-reasoner',8192,None)
            ),
            'temp_range': (2,1.00)
        },
        'GLM': {
            'name': 'GLM',
            'full_name': 'ChatGLM',
            'cht_url': 'https://open.bigmodel.cn/api/paas/v4/chat/completions',
            'chk_url': None,
            'models': (
                ('glm-zero-preview',None,None),
                ('glm-4-plus',None,glm_tools),
                ('glm-4-air-0111',None,glm_tools),
                ('glm-4-airx',None,glm_tools),
                ('glm-4-flash',None,glm_tools),
                ('glm-4-flashx',None,glm_tools),
                ('glm-4-long',None,glm_tools),
                ('codegeex-4',8192,None),
                ('charglm-4',4095,None),
                ('emohaa',None,None)
            ),
            'temp_range': (1,0.95)
        }
    }
    return info.get(service)

def glm_tools_gen() -> list:
    """GLM-dedicated tools generator.

    Return the tools as dict.
    """
    search_prompt = '\n'.join([
        '','',
        '## 来自互联网的信息','',
        '{search_result}','',
        '## 要求','',
        '根据最新发布的信息回答用户问题。','',
        '必须在回答末尾提示：「此回答使用网络搜索辅助生成。」','',
        ''
    ])
    tools = [{
        "type": "web_search",
        "web_search": {
            "enable": True,
            "search_prompt": search_prompt
        }
    }]
    return tools

def emohaa_meta_gen() -> dict:
    """Emohaa-dedicated meta generator.

    Return the meta as dict.
    """
    user_name = input('USER NAME\n')
    if not user_name:
        user_name = '用户'
    print()
    print('USER INFO')
    lines = lines_get()
    if not lines:
        user_info = '用户对心理学不太了解。'
    else:
        user_info = '\n'.join(lines)
    bot_info = '，'.join([
        'Emohaa 学习了经典的 Hill 助人理论',
        '拥有人类心理咨询师的专业话术能力',
        '具有较强的倾听、情感映射、共情等情绪支持能力',
        '帮助用户了解自身想法和感受，学习应对情绪问题',
        '帮助用户实现乐观、积极的心理和情感状态。'
    ])
    meta= {
        "user_name": user_name,
        "user_info": user_info,
        "bot_name": "Emohaa",
        "bot_info": bot_info
    }
    return meta

def token_gen() -> str:
    """Generate a jwt token for jwt-supported services.

    Jwt-support ability is judged by the `jwt` value in conf.
    Currently the only one supporting jwt is GLM.

    If the desired service is not jwt-supported,
    return the KEY directly as str.

    If it is, generate a token that expires in 30 sec,
    and return it as str.
    """
    if not conf.get('jwt'):
        return conf.get('KEY')
    KEYs = conf.get('KEY').split(".")
    if len(KEYs) == 3:
        return conf.get('KEY')
    if len(KEYs) != 2:
        exitc('ERR: Invalid KEY.')
    payload = {
        "api_key": KEYs[0],
        "exp": int(round(datetime.now(UTC).timestamp() * 1000)) + 30 * 1000,
        "timestamp": int(round(datetime.now(UTC).timestamp() * 1000)),
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

def data_gen() -> str:
    payload = {
        "messages": conf.get('msg'),
        "model": conf.get('model'),
        "max_tokens": conf.get('max_tokens'),
        "temperature": conf.get('temp'),
        "stream": conf.get('stream')
    }
    if conf.get('tool_use') and conf.get('tools'):
        payload["tools"] = conf.get('tools')
    elif conf.get('model') == 'emohaa':
        payload['meta'] = conf.get('meta')
    payload_json = json.dumps(payload)
    # print(conf.get('msg'),payload_json,sep='\n')
    return payload_json

def temp_get() -> float:
    """Get TEMPERATURE from user.

    Also check whether temp is within range.
    If temp is out of range,
    give an error message and some tips, and try again.

    Return the temp x.xx as float.
    """
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

def lines_get() -> list:
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
    return lines

def system_get() -> dict:
    print('SYSTEM')
    lines = lines_get()
    if not lines:
        sys = 'You are a helpful assistant. Now it is {} in UTC.'.format(
            datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
        )
    else:
        sys = '\n'.join(lines)
    return {'role': 'system', 'content': sys}

def usr_get() -> dict:
    print(f'USER #{conf.get("rnd")}')
    lines = lines_get()
    if not lines:
        exitc('INF: Null input, chat ended.')
    usr = '\n'.join(lines)
    return {'role': 'user', 'content': usr}

def ast_nostream() -> None:
    rsp = requests.request(
        "POST",
        conf.get('cht_url'),
        headers = headers_gen(),
        data = data_gen(),
        timeout = (3.05,9.05)
    )
    if rsp.status_code == requests.codes.ok: # pylint: disable=no-member
        if conf.get('model') == 'deepseek-reasoner':
            print(json.loads(rsp.text)['choices'][0]['message']['reasoning_content'])
            print()
            print(f'ASSISTANT CONTENT #{conf.get("rnd")}')
        ast = json.loads(rsp.text)['choices'][0]['message']['content']
        print(ast)
        conf['msg'].append({'role': 'assistant', 'content': ast})
        print()
    else:
        exitc('ERR: {} {}'.format(
            rsp.status_code,
            json.loads(rsp.text)['error']['message']
        ))

def ast_stream() -> None:
    ast = ''
    gocon = True
    rsp = requests.request(
        "POST",
        conf.get('cht_url'),
        headers = headers_gen(),
        data = data_gen(),
        timeout = (3.05,9.05),
        stream = True
    )
    if rsp.status_code == requests.codes.ok: # pylint: disable=no-member
        for line in rsp.iter_lines():
            if line:
                data = line.decode('utf-8')[len('data:'):].strip()
                if data == '[DONE]':
                    break
                json_data = json.loads(data)
                delta = json_data.get('choices')[0].get('delta').get('content')
                if delta or delta == '':
                    ast += delta
                    if not gocon:
                        print('\n')
                        print(f'ASSISTANT CONTENT #{conf.get("rnd")}')
                        gocon = True
                else:
                    delta = json_data.get('choices')[0].get('delta').get('reasoning_content')
                    gocon = False
                print(delta,end='',flush=True)
        conf['msg'].append({'role': 'assistant', 'content': ast})
        print()
        print()
    else:
        exitc('ERR: {} {}'.format(
            rsp.status_code,
            json.loads(rsp.text)['error']['message']
        ))

def balance_chk() -> None:
    rsp = requests.request(
        "GET",
        conf.get('chk_url'),
        headers = headers_gen(False),
        data = {},
        timeout = (3.05,9.05)
    )
    if rsp.status_code == requests.codes.ok: # pylint: disable=no-member
        return 'INF: {} {} left in the {} balance.'.format(
            json.loads(rsp.text)['balance_infos'][0]['total_balance'],
            json.loads(rsp.text)['balance_infos'][0]['currency'],
            conf.get('full_name')
        )
    else:
        exitc('ERR: {} {}'.format(
            rsp.status_code,
            json.loads(rsp.text)['error']['message']
        ))

def chat() -> None:
    if conf.get('model') != 'deepseek-reasoner':
        conf['temp'] = temp_get()
    conf['msg'].append(system_get())
    if conf.get('model') == 'emohaa':
        conf['meta'] = emohaa_meta_gen()
    while True:
        conf['rnd'] += 1
        conf['msg'].append(usr_get())
        if conf.get('model') != 'deepseek-reasoner':
            print(f'ASSISTANT #{conf.get("rnd")}')
        else:
            print(f'ASSISTANT REASONING #{conf.get("rnd")}')
        if not conf.get('stream'):
            ast_nostream()
        else:
            ast_stream()

try:
    conf = conf_read()
    print()
    if conf.get('balance_chk'):
        if conf.get('chk_url'):
            print(balance_chk())
        else:
            print(f'WRN: Balance check is unsupported for {conf.get("full_name")}.')
    print()
    # print(data_gen([],0,False))
    # exitc('INF: Debug Exit.')
    chat()
except SystemExit:
    pass
except KeyboardInterrupt:
    print()
    print('INF: Aborted.')
except requests.exceptions.Timeout:
    print("ERR: The request timed out.")
except:
    print()
    print_exc()
    print()
    print('ERR: Unexcepted error(s) occurred.')
    print('TIP: See above for more info.')
finally:
    pause = input('INF: Press Enter to exit...')
