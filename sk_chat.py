"""The main functional system.

1. Read `conf`.
2. If balance check is requested
   and the desired service supports it, run it.
   If not, print a warning message.
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

---

The function system structure: (arguments omitted)

- Exit
  exitc()
- Configuration reader
  conf_read()
  - service_model()
    - info_print()
    - sel_guess()
  - service_infoget()
    - glm_tools_gen()
    - kimi_tools_gen()
  - model_remap()
- Generator
  - token_gen()
  - headers_gen()
  - data_gen()
- Input reader
  lines_get()
  - temp_get()
  - system_get()
  - usr_get()
  - emohaa_meta_get()
- Balance checker
  balance_chk()
- Chat executive
  chat()
  - ast_nostream()
  - ast_stream()
    - delta_process()
    - tool_append()

The actual writing and running order may vary.

---

The documentation system structure:

- SUMMARY
* {blank}
- Instructions
  (Running Steps, Expected Exceptions)
* {blank}
- Arguments
- Returns
"""

from datetime import datetime,timezone # provide date to LLMs
import json # decode and encode
from traceback import print_exc # unexpected exceptions handling
import requests # GET and POST to servers
from jwt import encode # pass API KEY safely to supported services
from sk_conf import conf_get # read `conf`

def exitc(reason:str='') -> None:
    """Halfway exit.

    Print a reason message and raise `SystemExit`.
    The message must be ERR or INF type.

    Args:
        - reason: str, optional
          A reason to exit.
          default: ''
    Returns: None.
    """
    if reason:
        print(reason)
    raise SystemExit

def conf_read() -> dict:
    conf_r = conf_get('sk.json')
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
    model_info = service_model(
        'model',
        service_info.get('models'),
        True,
        service_conf.get('model','prompt')
    )
    conf_r['model'] = model_remap(model_info[0],service_conf.get('version'))
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
        print(f'WRN: "{sts}" is not a valid {keyword}.')
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
                    if sel_guess(chn.strip(),n):
                        return lst[m]
            print('ERR: Selection invalid.')
    print(f'INF: {keyword.capitalize()} {lt[0]} in use.')
    return lst[0]

def info_print(lt:list) -> None:
    """Print info neatly.

    Use space filling and tabs to align everything,
    and print them 2 per line (for the sake of narrow screens).

    Args:
        - lt: list
          The info list.
    Returns: None.
    """
    k = 0
    max_len = max(len(i) for i in lt)
    while k < len(lt):
        # pylint: disable-next=expression-not-assigned
        print('INF:',lt[k].ljust(max_len),end='\t') if k % 2 == 0 else print(lt[k])
        k += 1
    if k % 2 == 1:
        print()

def sel_guess(chn:str,sel:str) -> bool:
    mdlist = ('deepseek','glm','moonshot','qwen')
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
    """Provide services' info.

    Generate tools from other functions first to reduce time-consuming function calling
    (they might be use more than once).
    Then all supported services, models and other info are listed.
    For every service, the following keys are provided:

    - name: str.
      Just repeat the key name so might be removed in the future.
    - full_name: str.
      To simplify the selecting process, the name is usually an abbr.
      So this value is used to call the service rather formally.
    - cht_url: str. CHaT URL.
    - chk_url: str. balance CHecK URL. None for unsupported ones.
    - temp_range: tuple (int,int). The first value is max_temp and the second is default_temp.
    - models: tuple (tuple+ (str,int,dict)).
      - name: The model name.
      - max_tokens: The max_tokens to be passed.
        If docs don't mention it at all, or mark the max as default, then a None can be set.
      - tools: The usable tools. Usually the web search one.
        If there is none, set to None.

    Changes should be made since mixing dict and tuple is not a good idea.

    Args:
        - service: str
          The service of which you want info.
    Returns:
        dict: the info of the specified service.
    """
    glm_tools = glm_tools_gen()
    kimi_tools = kimi_tools_gen()
    info = {
        'DS': {
            'name': 'DS',
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
                ('glm-4-plus',4095,glm_tools),
                ('glm-4-air-0111',4095,glm_tools),
                ('glm-4-airx',4095,glm_tools),
                ('glm-4-flash',4095,glm_tools),
                ('glm-4-flashx',4095,glm_tools),
                ('glm-4-long',4095,glm_tools),
                ('glm-zero-preview',15360,None),
                ('codegeex-4',32768,None),
                ('charglm-4',4095,None),
                ('emohaa',8192,None)
            )
        },
        'KIMI': {
            'name': 'KIMI',
            'full_name': 'Moonshot',
            'cht_url': 'https://api.moonshot.cn/v1/chat/completions',
            'chk_url': 'https://api.moonshot.cn/v1/users/me/balance',
            'temp_range': (1,0.30),
            'models': (
                ('moonshot-v1-auto',None,kimi_tools),
                ('moonshot-v1-8k',None,kimi_tools),
                ('moonshot-v1-32k',None,kimi_tools),
                ('moonshot-v1-128k',None,kimi_tools),
            )
        },
        'QWEN': {
            'name': 'QWEN',
            'full_name': 'ModelStudio',
            'cht_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
            'chk_url': None,
            'temp_range': (2,0.70),
            'models': (
                ('qwen-max',None,None),
                ('qwen-plus',None,None),
                ('qwen-turbo',None,None),
                ('qwen-long',None,None),
                ('qwen-math-plus',None,None),
                ('qwen-math-turbo',None,None),
                ('qwen-coder-plus',None,None),
                ('qwen-coder-turbo',None,None),
                ('deepseek-v3',8192,None),
                ('deepseek-r1',32768,None),
                ('qwq-32b-preview',None,None)
            )
        }
    }
    return info.get(service)

def glm_tools_gen() -> list:
    """GLM-dedicated tools generator.

    Generate a search prompt first to control searching performance and
    display the using of tools (although not always useful). Then generate tools.

    Args: None.
    Returns:
        list: the GLM tools.
        Dead return.
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
    """Kimi-dedicated tools generator.

    Args: None.
    Returns:
        list: the Kimi tools.
        Dead return.
    """
    tools = [{
        "type": "builtin_function",
        "function": {
            "name": "$web_search",
        }
    }]
    return tools

def model_remap(model:str,ver:str) -> str:
    """Remap models for QWEN.

    Qwen has three types of models, roughly speaking.

    1. Commercial version, stable
    2. Commercial version, latest
    3. Open-Source version

    In order to simplify the selecting process, they are not fully displayed,
    but are decided through conf service.QWEN.version.

    1. Check whether the selected model has a remap choice, or if ver is `stable`.
       If not, return directly.
       It is convenient so we just apply this function globally
       (and that's why it is not a 'dedicated' one).
    2. Check whether ver is a supported value.
       If not, print a warning message and assume it is `latest`.
    3. Check whether ver is `latest`.
       If so, add `-latest` to the model, print a remap message and return it.
    4. Now ver must be `oss`. We will use a dict to remap it, print a message and return it.

    Args:
        - model: str
          The model to be remapped.
        - ver: str
          Valid: one of 'stable', 'latest' and 'oss' (Open-Source Software).
          Short for 'VERsion'.
    Returns:
        str: the remapped model.
    """
    if model not in (
        'qwen-max','qwen-plus','qwen-turbo',
        'qwen-math-plus','qwen-math-turbo',
        'qwen-coder-plus','qwen-coder-turbo'
    ) or ver == 'stable':
        return model
    if ver not in ('stable','latest','oss'):
        print(f'WRN: "{ver}" is not a valid version.')
        print('WRN: Fallback to "latest".')
        ver = 'latest'
    if ver == 'latest':
        model += '-latest'
        print(f'INF: Remap to {model}.')
        return model
    oss_map = {
        'qwen-max': 'qwen2.5-72b-instruct',
        'qwen-plus': 'qwen2.5-32b-instruct',
        'qwen-turbo': 'qwen2.5-14b-instruct-1m',
        'qwen-math-plus': 'qwen2.5-math-72b-instruct',
        'qwen-math-turbo': 'qwen2.5-math-7b-instruct',
        'qwen-coder-plus': 'qwen2.5-coder-32b-instruct',
        'qwen-coder-turbo': 'qwen2.5-coder-7b-instruct'
    }
    model = oss_map.get(model)
    print(f'INF: Remap to {model}.')
    return model

def token_gen() -> str:
    """Generate jwt tokens for jwt-supported services.

    1. If the desired service is not jwt-supported,
       return `KEY` directly.
    2. If it is, split it by `.` and assess its length.
    3. If length is 3, the user puts a jwt token in `conf`, so return it directly.
    4. If length is not 2, `KEY` is not valid and call `exitc()`.
    5. Then length should be 2, since there is at least one `.` or `KEYcheck()` will fail.
       Generate a token that expires in 30 sec, and return it.

    Jwt-support ability is judged by `conf.jwt`. Currently the only one supporting jwt is GLM.

    Args: None.
    Returns:
        str: KEY or token.
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
        "exp": int(round(datetime.now(timezone.utc).timestamp() * 1000)) + 30 * 1000,
        "timestamp": int(round(datetime.now(timezone.utc).timestamp() * 1000)),
    }
    return encode(
        payload,
        ksp[1],
        algorithm="HS256",
        headers={"alg": "HS256", "sign_type": "SIGN"},
    )

def headers_gen(contype:bool=True) -> dict:
    """Generate headers to make requests.

    1. Define the basic header (used by balance_chk)
    2. If `contype` (CONtent-TYPE) is True (used by chat), add `Content-Type`.

    Args:
        - contype: bool, optional
          Whether to add Content-Type to headers,
          which is required for chat but not for balance_chk.
          Short for 'CONtent-TYPE'.
          default: True
    Returns:
        dict: the headers.
    """
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
    elif conf.get('tool_use') and conf.get('model') in (
        'qwen-max','qwen-max-latest',
        'qwen-plus','qwen-plus-latest',
        'qwen-turbo','qwen-turbo-latest'
    ):
        payload['enable_search'] = True
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

    If `ValueError` occurs, print an error message and some tips, and try again.
    Conditions: Not a number, out of range, etc.

    Args: None.
    Returns:
        float: The temperature (x.xx).
    Input requested.
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
    r"""A general engine for multiline mode.

    Get multiple lines of input from the user.
    A blank line is regarded as an EOF mark.
    If `conf.long_prompt` is true, that would be two blank lines.
    Use `\n` to join lines after EOF, and then cut whitespace from boundaries.

    Args: None.
    Returns:
        str: the merged lines of input.
    Input requested.
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
    if conf.get('autotime'):
        sys += f'\nNow it is {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")} in UTC.'
    return {'role': 'system', 'content': sys}

def usr_get() -> dict:
    print(f'USER #{conf.get("rnd")}')
    usr = lines_get() or exitc('INF: Null input, chat ended.')
    return {'role': 'user', 'content': usr}

def emohaa_meta_get() -> dict:
    """Get META from user. Emohaa-dedicated.

    1. Get `user_name` in single line mode.
    2. Get `user_info` in multiline mode.
    3. Generate `bot_info`.
    4. Generate `meta`.

    Args: None.
    Returns:
        dict: the emohaa meta.
    Input requested.
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

def ast_nostream() -> None:
    rsp = requests.request(
        "POST",
        conf.get('cht_url'),
        headers = headers_gen(),
        data = data_gen(),
        timeout = (3.05,None)
    )
    if rsp.status_code == requests.codes.ok: # pylint: disable=no-member
        choices = json.loads(rsp.text)['choices'][0]
        # print(choices)
        if conf.get('model') in ('deepseek-reasoner','deepseek-r1'):
            print(choices['message']['reasoning_content'])
            print()
            print(f'ASSISTANT CONTENT #{conf.get("rnd")}')
        ast = choices.get('message')
        print(ast.get('content'),end='')
        conf['msg'].append(ast)
        if choices.get('finish_reason') == 'tool_calls':
            for tool_call in ast.get('tool_calls'):
                conf['msg'].append({
                    "role": "tool",
                    "tool_call_id": tool_call.get('id'),
                    "name": tool_call.get('function').get('name'),
                    "content": tool_call.get('function').get('arguments'),
                })
            print('INF: Web Search has been performed.')
            ast_nostream()
        else:
            print('\n')
    else:
        # pylint: disable-next=consider-using-f-string
        exitc('ERR: {} {}'.format(
            rsp.status_code,
            json.loads(rsp.text)['error']['message']
        ))

def ast_stream() -> None:
    conf['ast'] = ''
    conf['gocon'] = True
    conf['tool_lt'] = []
    conf['tool'] = {'role': 'tool'}
    conf['tool_index'] = 0
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
                if not (delta_lt := json.loads(data).get('choices')[0].get('delta')):
                    continue
                delta_process(delta_lt)
        if len(conf.get('tool')) != 1:
            conf['tool_lt'].append(conf.get('tool'))
            tool_append(conf.get('tool_lt'))
            print('INF: Web Search has been performed.')
            ast_stream()
        else:
            conf['msg'].append({'role': 'assistant', 'content': conf.get('ast')})
            print()
            print()
    else:
        # pylint: disable-next=consider-using-f-string
        exitc('ERR: {} {}'.format(
            rsp.status_code,
            json.loads(rsp.text)['error']['message']
        ))

def delta_process(delta_lt:str) -> None:
    if (delta := delta_lt.get('content')) or delta == '':
        conf['ast'] += delta
        if not conf.get('gocon'):
            print(f'\n\nASSISTANT CONTENT #{conf.get("rnd")}',flush=True)
            conf['gocon'] = True
    else:
        if delta := delta_lt.get('reasoning_content'):
            conf['gocon'] = False
        elif delta := delta_lt.get('tool_calls'):
            delta = delta[0]
            index = delta.get('index')
            if index != conf.get('tool_index'):
                conf['tool_index'] += 1
                conf['tool_lt'].append(conf.get('tool'))
            if delta.get('id'):
                conf['tool']['tool_call_id'] = delta.get('id')
                conf['tool']['name'] = delta.get('function').get('name')
            else:
                conf['tool']['content'] = delta.get('function').get('arguments')
            delta = ''
        else:
            delta = ''
    print(delta,end='',flush=True)

def tool_append(tool_lt:list) -> None:
    tool_ast_lt = []
    for m,n in enumerate(tool_lt):
        tool_ast = {
            'index': m,
            'id': n.get('tool_call_id'),
            'type': 'builtin_function', 
            'function': {
                'name': n.get('name'),
                'arguments': n.get('content')
            }
        }
        tool_ast_lt.append(tool_ast)
    conf['msg'].append({
        'role': 'assistant',
        'content': conf.get('ast'),
        'tool_calls': tool_ast_lt
    })
    for i in tool_lt:
        conf['msg'].append(i)

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
        if conf.get('name') == 'DS':
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
    if conf.get('model') not in ('deepseek-reasoner','deepseek-r1'):
        conf['temp'] = temp_get()
    conf['msg'].append(system_get())
    if conf.get('model') == 'emohaa':
        conf['meta'] = emohaa_meta_get()
    while True:
        conf['rnd'] += 1
        conf['msg'].append(usr_get())
        print(
            f'ASSISTANT #{conf.get("rnd")}'
            if conf.get('model') not in ('deepseek-reasoner','deepseek-r1')
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
