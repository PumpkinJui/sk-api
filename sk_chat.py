"""The main functional system.

1. Read `conf`.
2. If balance check is requested
   and the desired service supports it, run it.
   If not, print an warning message.
3. Run `chat()`.

Can handle any of the following exceptions:

- `SystemExit`
  Normally requested by `exitc()` as a halfway exit.
- `KeyboardInterrupt`
  Ctrl+C exit requested by the user.
- `requests.exceptions.Timeout`
  `ConnectTimeout` or `ReadTimeout`, as a network issue.
- `requests.exceptions.ConnectionError`
  Also a network issue.

Other exceptions will be printed for debugging.

The main code is at the bottom.


The documentation system structure:

- SUMMARY
* {blank}
- Running Steps
* {blank}
- Expected Exceptions
* {blank}
- Returns
"""

from datetime import datetime,UTC # provide date to LLMs
import json # decode and encode
from traceback import print_exc # unexpected exceptions handling
import requests # GET and POST to servers
from jwt import encode # pass API KEY safely to supported services
from sk_conf import confGet # read `conf`

def exitc(reason:str='') -> None:
    """Halfway exit.

    Give a reason and raise `SystemExit`.

    No return provided.
    """
    if reason:
        print(reason)
    raise SystemExit

def conf_read() -> dict:
    conf_r = confGet('sk.json')
    if not conf_r:
        with open('sk.json','a',encoding='utf-8'):
            pass
        exitc('TIP: Please check your conf file.')
    print()
    service_list = tuple(conf_r.get('service').keys())
    service_name = service_model('service',service_list,False)
    service_info = service_infoget(service_name)
    service_conf = conf_r['service'].get(service_name)
    del conf_r['service']
    conf_r.update(service_conf)
    print()
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
    conf_r['model'] = model_info[0]
    conf_r['max_tokens'] = model_info[1]
    conf_r['tools'] = model_info[2]
    conf_r['msg'] = []
    conf_r['rnd'] = 0
    conf_r.update(service_info)
    del conf_r['models']
    # print(conf_r)
    return conf_r

def service_model(keyword:str,lst:tuple,lower:bool=True,sts:str='prompt') -> str:
    lt = tuple(i[0] for i in lst) if isinstance(lst[0],tuple) else lst
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
        info_print(lt)
        while True:
            chn = input('REQ: ')
            chn = chn.lower() if lower else chn.upper()
            if not chn:
                pass
            elif chn in lt:
                print(f'INF: Selection accepted: {chn}.')
                return lst[lt.index(chn)]
            else:
                for m,n in enumerate(lt):
                    if keyword == 'service' and sel_guess(chn.strip(),n) or \
                       keyword ==  'model'  and sel_guess(chn.strip(),n):
                        return lst[m]
            print('ERR: Selection invalid.')
    print(f'INF: {keyword.capitalize()} {lt[0]} in use.')
    return lst[0]

def info_print(lt:list) -> None:
    k = 0
    max_len = max(len(i) for i in lt)
    while k < len(lt):
        # pylint: disable-next=expression-not-assigned
        print('INF:',lt[k].ljust(max_len),end='\t') if k % 2 == 0 else print(lt[k])
        k += 1
    if k % 2 == 1:
        print()

def sel_guess(chn:str,sel:str) -> bool:
    mdlist = ('deepseek','glm','moonshot')
    sell = sel.split('-',1)
    if sell[0] in mdlist:
        selp = sell[1]
    else:
        selp = sel
    # print(selp)
    if chn == selp:
        print(f'INF: Selection accepted: {sel}.')
        return True
    if chn in selp:
        print(f'INF: Selection guessed: {sel}. Accepted.')
        return True
    return False

def service_infoget(service:str) -> dict:
    glm_tools = glm_tools_gen()
    kimi_tools = kimi_tools_gen()
    info = {
        'DSK': {
            'name': 'DSK',
            'full_name': 'DeepSeek',
            'cht_url': 'https://api.deepseek.com/chat/completions',
            'chk_url': 'https://api.deepseek.com/user/balance',
            'temp_range': (2,1.00),
            'models': (
                ('deepseek-chat',8192,None),
                ('deepseek-reasoner',8192,None)
            )
        },
        'GLM': {
            'name': 'GLM',
            'full_name': 'ChatGLM',
            'cht_url': 'https://open.bigmodel.cn/api/paas/v4/chat/completions',
            'chk_url': None,
            'temp_range': (1,0.95),
            'models': (
                ('glm-zero-preview',15360,None),
                ('glm-4-plus',4095,glm_tools),
                ('glm-4-air-0111',4095,glm_tools),
                ('glm-4-airx',4095,glm_tools),
                ('glm-4-flash',4095,glm_tools),
                ('glm-4-flashx',4095,glm_tools),
                ('glm-4-long',4095,glm_tools),
                ('codegeex-4',32768,None),
                ('charglm-4',4095,None),
                ('emohaa',8192,None)
            )
        },
        'KIMI': {
            'name': 'KIMI',
            'full_name': 'Kimi',
            'cht_url': 'https://api.moonshot.cn/v1/chat/completions',
            'chk_url': 'https://api.moonshot.cn/v1/users/me/balance',
            'temp_range': (1,0.30),
            'models': (
                ('moonshot-v1-auto',None,kimi_tools),
                ('moonshot-v1-8k',None,kimi_tools),
                ('moonshot-v1-32k',None,kimi_tools),
                ('moonshot-v1-128k',None,kimi_tools),
            )
        }
    }
    return info.get(service)

def glm_tools_gen() -> list:
    """GLM-dedicated tools generator.

    1. Generate `search-prompt`.
    2. Generate `tools`.

    Return `tools` as dict. Dead return.
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

def kimi_tools_gen() -> list:
    return None
    tools = [{
        "type": "builtin_function",
        "function": {
            "name": "$web_search",
        }
    }]
    return tools

def emohaa_meta_gen() -> dict:
    """Emohaa-dedicated meta generator.

    1. Get `user_name` in single line mode.
    2. Get `user_info` in multiple line mode.
    3. Generate `bot_info`.
    4. Generate `meta`.

    Return `meta` as dict. Input requested.
    """
    user_name = input('USER NAME\n')
    if not user_name:
        user_name = '用户'
    print()
    print('USER INFO')
    user_info = lines_get() or '用户对心理学不太了解。'
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
    """Generate jwt tokens for jwt-supported services.

    1. If the desired service is not jwt-supported,
       return `KEY` directly as str.
    2. If it is, split it by `.` and assess its length.
    3. If length is 3, the user puts a jwt token in `conf`, so return it directly.
    4. If length is not 2, `KEY` is not valid and call `exitc()`.
    5. Then length should be 2, since there is at least one `.` or `KEYcheck()` will fail.
       Generate a token that expires in 30 sec, and return it.

    Jwt-support ability is judged by `conf.jwt`. Currently the only one supporting jwt is GLM.

    Return `KEY` or `token` as str.
    """
    if not conf.get('jwt'):
        return conf.get('KEY')
    ksp = conf.get('KEY').split(".")
    if len(ksp) == 3:
        return conf.get('KEY')
    if len(ksp) != 2:
        exitc('ERR: Invalid KEY.')
    payload = {
        "api_key": ksp[0],
        "exp": int(round(datetime.now(UTC).timestamp() * 1000)) + 30 * 1000,
        "timestamp": int(round(datetime.now(UTC).timestamp() * 1000)),
    }
    return encode(
        payload,
        ksp[1],
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

    1. Get it in single line mode.
    2. If `None`, return the default value from `conf.temp_range`.
    3. Convert it into `x.xx` float.
    4. Check whether `temp` is within range according to `conf.temp_range`.
    5. If not, raise `ValueError`. If so, return it.

    If `ValueError` occurs, give an error message and some tips, and try again.
    Conditions: Not a number, out of range, etc.

    Return `temp x.xx` as float.
    """
    while True:
        try:
            temp = input('TEMPERATURE: ')
            if temp == '':
                print()
                return conf.get('temp_range')[1]
            temp = round(float(temp),2)
            if not 0 <= temp <= conf.get('temp_range')[0]:
                raise ValueError
            print()
            return temp
        except ValueError:
            print('ERR: Temperature invalid.')
            print(f'TIP: 0 <= temp <= {conf.get("temp_range")[0]}.')
            print(f'TIP: Leave blank to use default ({conf.get("temp_range")[1]}).')

def lines_get() -> str:
    r"""Multiple line mode general engine.

    Get multiple lines of input from user.
    A blank line is regarded as EOF mark.
    If `conf.long_prompt` is true, that would be two blank lines.
    Use `\n` to join lines after EOF, and then cut whitespace from boundaries.

    Return merged `lines` as str.
    A common use of this function is:
    `{parameter} = lines_get() or {default}`
    """
    lines = []
    nul_count = 0
    while True:
        line = input()
        if conf.get('long_prompt'):
            if line == '':
                if nul_count:
                    break
                nul_count += 1
            elif nul_count:
                nul_count = 0
        else:
            if line == '':
                break
        lines.append(line)
    # print('\n'.join(lines).strip().replace('\n','\\n'))
    return '\n'.join(lines).strip()

def system_get() -> dict:
    print('SYSTEM')
    sys = lines_get() or 'You are a helpful assistant.'
    sys += f'\nNow it is {datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")} in UTC.'
    return {'role': 'system', 'content': sys}

def usr_get() -> dict:
    print(f'USER #{conf.get("rnd")}')
    usr = lines_get() or exitc('INF: Null input, chat ended.')
    return {'role': 'user', 'content': usr}

def ast_nostream() -> None:
    rsp = requests.request(
        "POST",
        conf.get('cht_url'),
        headers = headers_gen(),
        data = data_gen(),
        timeout = (3.05,None)
    )
    if rsp.status_code == requests.codes.ok: # pylint: disable=no-member
        # print(rsp.text)
        if conf.get('model') == 'deepseek-reasoner':
            print(json.loads(rsp.text)['choices'][0]['message']['reasoning_content'])
            print()
            print(f'ASSISTANT CONTENT #{conf.get("rnd")}')
        ast = json.loads(rsp.text)['choices'][0]['message']['content']
        print(ast)
        conf['msg'].append({'role': 'assistant', 'content': ast})
        print()
    else:
        # pylint: disable-next=consider-using-f-string
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
        timeout = (3.05,30),
        stream = True
    )
    if rsp.status_code == requests.codes.ok: # pylint: disable=no-member
        for line in rsp.iter_lines():
            # print(line)
            if line:
                if line == b': keep-alive':
                    print('INF: Stay connected. Please wait.')
                    print('TIP: Typically due to server load.')
                    continue
                data = line.decode('utf-8')[len('data:'):].strip()
                if data == '[DONE]':
                    break
                if not (delta_list := json.loads(data).get('choices')[0].get('delta')):
                    continue
                delta = delta_list.get('content')
                if delta or delta == '':
                    ast += delta
                    if not gocon:
                        print('\n')
                        print(f'ASSISTANT CONTENT #{conf.get("rnd")}')
                        gocon = True
                else:
                    delta = delta_list.get('reasoning_content')
                    gocon = False
                print(delta,end='',flush=True)
        conf['msg'].append({'role': 'assistant', 'content': ast})
        print()
        print()
    else:
        # pylint: disable-next=consider-using-f-string
        exitc('ERR: {} {}'.format(
            rsp.status_code,
            json.loads(rsp.text)['error']['message']
        ))

# pylint: disable-next=inconsistent-return-statements
def balance_chk() -> str:
    rsp = requests.request(
        "GET",
        conf.get('chk_url'),
        headers = headers_gen(False),
        data = {},
        timeout = (3.05,10)
    )
    text = json.loads(rsp.text)
    if rsp.status_code == requests.codes.ok: # pylint: disable=no-member
        if conf.get('name') == 'DSK':
            # pylint: disable-next=consider-using-f-string
            return 'INF: {} {} left in the {} balance.'.format(
                text['balance_infos'][0]['total_balance'],
                text['balance_infos'][0]['currency'],
                conf.get('full_name')
            )
        if conf.get('name') == 'KIMI':
            # pylint: disable-next=consider-using-f-string
            return 'INF: {} CNY left in the {} balance.'.format(
                text['data']['available_balance'],
                conf.get('full_name')
            )
    # pylint: disable-next=consider-using-f-string
    exitc('ERR: {} {}'.format(
        rsp.status_code,
        text['error']['message']
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
        print(
            f'ASSISTANT #{conf.get("rnd")}' if conf.get('model') != 'deepseek-reasoner'
            else f'ASSISTANT REASONING #{conf.get("rnd")}'
        )
        # pylint: disable-next=expression-not-assigned
        ast_stream() if conf.get('stream') else ast_nostream()

try:
    conf = conf_read()
    print()
    if conf.get('balance_chk'):
        print(
            balance_chk() if conf.get('chk_url')
            else f'WRN: Balance check is unsupported for {conf.get("full_name")}.'
        )
    print()
    # print(data_gen([],0,False))
    # exitc('INF: Debug Exit.')
    chat()
except KeyboardInterrupt:
    print()
    print('INF: Aborted.')
except requests.exceptions.Timeout:
    print()
    print("ERR: The request timed out.")
except requests.exceptions.ConnectionError:
    print()
    print('ERR: A Connection error occurred.')
# pylint: disable-next=broad-exception-caught
except Exception:
    print()
    print_exc()
    print()
    print('ERR: Unexpected error(s) occurred.')
    print('TIP: See above for more info.')
finally:
    pause = input('INF: Press Enter to exit...')
