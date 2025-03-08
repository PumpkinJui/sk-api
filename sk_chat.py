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
    - free_models()
    - info_print()
    - sel_guess()
  - model_remap()
    - qwen_remap()
    - sif_remap()
- Generator
  - headers_gen()
  - payload_gen()
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
from sk_conf import conf_get, service_infoget # read conf and provide services' info

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
    service_conf = service_model('service',conf_r.get('service'))
    service_info = service_infoget(service_conf.get('service'))
    conf_r.update(service_conf)
    conf_r.update(service_info)
    del conf_r['service']
    print()
    try:
        model_hidden_set = set(conf_r.get('prompt_control').get('hidden_models'))
    except TypeError:
        exitc('ERR: Invalid prompt_control.hidden_models.')
    model_display = {
        m: n for m, n in service_info.get('models').items()
        if m not in model_hidden_set
    }
    model_info = service_model(
        'model',
        model_display,
        conf_r.get('model','prompt'),
        conf_r.get('prompt_control').get('free_only')
    )
    conf_r.update(model_info)
    conf_r.update(conf_r.get('temp_range'))
    del conf_r['models'], conf_r['temp_range']
    conf_r = model_remap(conf_r)
    nested = [m for m, n in conf_r.items() if isinstance(n, dict)]
    for i in nested:
        conf_r.update(conf_r.pop(i))
    conf_r['msg'] = []
    conf_r['rnd'] = 0
    # print(conf_r)
    return conf_r

def service_model(keyword:str,lst:dict,sts:str='prompt',free:bool=False) -> str:
    if free:
        lt = free_models(lst)
    else:
        lt = tuple(lst.keys())
    if sts != 'prompt' and sts not in lt:
        print(f'WRN: "{sts}" is not a valid {keyword}.')
    if sts != 'prompt' and sts in lt:
        print(f'INF: {keyword.capitalize()} {sts} selected.')
        lst[sts][keyword] = sts
        return lst[sts]
    if len(lt) > 1:
        print(f'INF: Multiple {keyword}s available.')
        print('INF: Select one from below by name.')
        print('TIP: Case insensitive.')
        print('TIP: Fragments accepted; guessed by order.')
        info_print(lt)
        while True:
            chn = input('REQ: ')
            chn = chn.strip().lower()
            if chn:
                for i in lt:
                    if sel_guess(chn,i):
                        lst[i][keyword] = i
                        return lst[i]
            print('ERR: Selection invalid.')
    print(f'INF: {keyword.capitalize()} {lt[0]} in use.')
    lst[lt[0]][keyword] = lt[0]
    return lst[lt[0]]

def free_models(lst:dict) -> tuple:
    """Filter free models out.

    Generate a tuple of free models.
    If none of the models is free,
    print a warning message and proceed with the full model list.

    Args:
        - lst: dict
          Keys are model names.
          Values are nested dicts: we only care the key `free` in it.
    Returns:
        tuple: a list of models.
    """
    if not (free := tuple(m for m, n in lst.items() if n.get('free'))):
        print('WRN: No free models available.')
        print('WRN: Proceeding with the full model list.')
        free = tuple(lst.keys())
    return free

def info_print(lt:list) -> None:
    """Print info neatly.

    If everything is within 18 characters,
    use space filling and tabs to align everything,
    and print them 2 per line (for the sake of narrow screens).
    If not, just print them 1 per line.

    Args:
        - lt: list
          The info list.
    Returns: None.
    """
    lt = [i.split('/')[1] if '/' in i else i for i in lt]
    max_len = max(len(i) for i in lt)
    if max_len <= 18:
        k = 0
        while k < len(lt):
            # pylint: disable-next=expression-not-assigned
            print('INF:',lt[k].ljust(max_len),end='\t') if k % 2 == 0 else print(lt[k])
            k += 1
        if k % 2 == 1:
            print()
    else:
        __ = [print('INF:',i) for i in lt]

def sel_guess(chn:str,sel:str) -> bool:
    mdlist = ('deepseek','glm','qwen')
    seld = sel.split('/',1)[1].lower() if '/' in sel else sel.lower()
    sell = seld.split('-',1)
    selp = sell[1] if '-' in seld and sell[0] in mdlist else seld
    # print(selp)
    if chn in {sel.lower(),selp}:
        print(f'INF: Selection accepted: {sel}.')
        return True
    if chn in selp:
        print(f'INF: Selection guessed: {sel}. Accepted.')
        return True
    return False

def model_remap(remap_conf:dict) -> dict:
    """The remap center.

    Remap means that we map the selected models into different versions according to conf.
    Currently, we need to remap QWEN (3 ver) and SIF (2 ver).
    We use the service's full name as the identifier.

    Args:
        - remap_conf: dict
          The conf in which the model needs to be remapped.
    Returns:
        dict: The model-remapped conf.
    """
    if remap_conf.get('full_name') == 'ModelStudio':
        remap_conf['model'] = qwen_remap(remap_conf.get('model'),remap_conf.get('version'))
        del remap_conf['version']
        return remap_conf
    if remap_conf.get('full_name') == 'SiliconFlow' and \
       not remap_conf.get('prompt_control').get('free_only'):
        model = sif_remap(remap_conf.get('model'),remap_conf.get('pro'))
        remap_conf['model'] = model
        if model in {'Pro/deepseek-ai/DeepSeek-R1'}:
            remap_conf['max_tokens'] = 16384
        del remap_conf['pro']
        return remap_conf
    return remap_conf

def qwen_remap(model:str,ver:str) -> str:
    """QWEN-dedicated model remapper.

    Qwen has three types of models, roughly speaking.

    1. Commercial version, stable
    2. Commercial version, latest
    3. Open-Source version

    In order to simplify the selecting process, they are not fully displayed,
    but are decided through conf service.QWEN.version.

    1. Check whether the selected model has a remap choice, or if ver is `stable`.
       If not, return directly.
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
    if model not in {
        'qwen-max','qwen-plus','qwen-turbo',
        'qwen-math-plus','qwen-math-turbo',
        'qwen-coder-plus','qwen-coder-turbo',
        'qwq-plus'
    } or ver == 'stable':
        return model
    if ver not in {'stable','latest','oss'}:
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
        'qwen-coder-turbo': 'qwen2.5-coder-7b-instruct',
        'qwq-plus': 'qwq-32b'
    }
    model = oss_map.get(model)
    print(f'INF: Remap to {model}.')
    return model

def sif_remap(model:str,pro:bool) -> str:
    """SIF-dedicated model remapper.

    SIF has some 'Pro' models.
    Although I don't understand the differences between non-Pro and Pro,
    I write this function to add their support.

    Check whether the selected model has a remap choice,
    and if pro versions are wished to be used. If not, return directly.
    Otherwise add a 'Pro/' prefix, print a remap message and return it.

    Args:
        - model: str
          The model to be remapped.
        - pro: bool
          Whether or not Pro versions are wished to be used.
    Returns:
        str: the remapped model.
    """
    if model not in {
        'deepseek-ai/DeepSeek-R1',
        'deepseek-ai/DeepSeek-V3',
        'deepseek-ai/DeepSeek-R1-Distill-Qwen-7B',
        'Qwen/Qwen2.5-7B-Instruct',
        'Qwen/Qwen2.5-Coder-7B-Instruct',
        'THUDM/glm-4-9b-chat'
    } or not pro:
        return model
    model = 'Pro/' + model
    print(f'INF: Remap to {model}.')
    return model

def headers_gen() -> dict:
    """Generate request headers.

    Args: None.
    Returns:
        dict: the headers.
    """
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {conf.get("KEY")}'
    }
    # print(headers)
    return headers

def payload_gen() -> str:
    """Generate the request payload.

    1. Generate the basic payload.
    2. Add tools/meta to it, if conditions are met.
    3. Dump it into json format.

    Args: None.
    Returns:
        str: The json-format payload.
    """
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
    elif conf.get('tool_use') and conf.get('model') in {
        'qwen-max','qwen-max-latest',
        'qwen-plus','qwen-plus-latest',
        'qwen-turbo','qwen-turbo-latest'
    }:
        payload['enable_search'] = True
    payload_json = json.dumps(payload)
    # print(conf.get('msg'),payload_json,sep='\n')
    return payload_json

def temp_get() -> float:
    """Get TEMPERATURE from the user.

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
                return conf.get('default_temp')
            temp = round(float(temp),2)
            if not conf.get('no_max') and not 0 <= temp <= conf.get('max_temp') or \
                   conf.get('no_max') and not 0 <= temp < conf.get('max_temp'):
                raise ValueError
            print()
            return temp
        except ValueError:
            print('ERR: Temperature invalid.')
            print(
                f'TIP: 0 <= temp <= {conf.get("max_temp")}.'
                if not conf.get('no_max') else
                f'TIP: 0 <= temp < {conf.get("max_temp")}.'
            )
            print(f'TIP: Leave blank to use default ({conf.get("default_temp")}).')

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
    """Get SYSTEM PROMPT from the user.

    1. Get it in multiline mode.
       The multiline mode is used because Kimi's official default system prompt is multiline.
       Although I didn't use it, I realized its potential demand.
       Original:
         https://platform.moonshot.cn/docs/guide/faq#为什么-api-返回的结果和-kimi-智能助手返回的结果不一致
         https://github.com/MoonshotAI/MoonshotAI-Cookbook/
           blob/master/examples/awesome_kimi_prompt/kimi_assistant.json
    2. If `None`, use the default.
    3. Add time to it if `conf.autotime` is True.

    Args: None.
    Returns:
        dict: The system prompt in the message format.
    Input requested.
    """
    print('SYSTEM')
    sys = lines_get() or 'You are a helpful assistant.'
    if conf.get('autotime'):
        sys += f'\nNow it is {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")} in UTC.'
    return {'role': 'system', 'content': sys}

def usr_get() -> dict:
    """Get USER PROMPT from the user.

    1. Get it in multiline mode.
    2. If `None`, exit the program peacefully.

    Args: None.
    Returns:
        dict: The user prompt in the message format.
    Input requested.
    """
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
        data = payload_gen(),
        timeout = (3.05,None)
    )
    if rsp.status_code == requests.codes.ok: # pylint: disable=no-member
        choices = json.loads(rsp.text)['choices'][0]
        # print(choices)
        if choices.get('message').get('reasoning_content'):
            print(choices.get('message').get('reasoning_content').strip('\n'))
            print()
            print(f'ASSISTANT CONTENT #{conf.get("rnd")}')
        ast = choices.get('message')
        print(ast.get('content').strip('\n'),end='')
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
        data = payload_gen(),
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
                if error_detail := json.loads(data).get('error'):
                    print()
                    exitc(f'ERR: {error_detail.get("message")} ({error_detail.get("code")})')
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
    if (delta := delta_lt.get('content')) or \
       (delta == '' and not delta_lt.get('reasoning_content')):
        if not conf['ast'] and delta.lstrip('\n') != delta:
            delta = delta.lstrip('\n')
        conf['ast'] += delta
        if not conf.get('gocon') and \
           not delta_lt.get('reasoning_content') and delta_lt.get('content'):
            print(f'\n\nASSISTANT CONTENT #{conf.get("rnd")}',flush=True)
            conf['gocon'] = True
    else:
        if delta := delta_lt.get('reasoning_content'):
            if conf.get('gocon') and delta.lstrip('\n') != delta:
                delta = delta.lstrip('\n')
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
        headers = headers_gen(),
        data = {},
        timeout = (3.05,10)
    )
    text = json.loads(rsp.text)
    if rsp.status_code == requests.codes.ok: # pylint: disable=no-member
        if conf.get('full_name') == 'DeepSeek':
            # pylint: disable-next=consider-using-f-string
            return 'INF: {} {} left in the {} balance.'.format(
                text['balance_infos'][0]['total_balance'],
                text['balance_infos'][0]['currency'],
                conf.get('full_name')
            )
        if conf.get('full_name') == 'Moonshot':
            # pylint: disable-next=consider-using-f-string
            return 'INF: {} CNY left in the {} balance.'.format(
                text['data']['available_balance'],
                conf.get('full_name')
            )
        if conf.get('full_name') == 'SiliconFlow':
            # pylint: disable-next=consider-using-f-string
            return 'INF: {} CNY left in the {} balance.'.format(
                text['data']['totalBalance'],
                conf.get('full_name')
            )
    # pylint: disable-next=consider-using-f-string
    exitc('ERR: {} {}'.format(
        rsp.status_code,
        text['error']['message']
    ))

def chat() -> None:
    if conf.get('show_temp') and not conf.get('reasoner'):
        conf['temp'] = temp_get()
    if conf.get('show_system') and not conf.get('reasoner'):
        conf['msg'].append(system_get())
    if conf.get('model') == 'emohaa':
        conf['meta'] = emohaa_meta_get()
    while True:
        conf['rnd'] += 1
        conf['msg'].append(usr_get())
        print(
            f'ASSISTANT #{conf.get("rnd")}'
            if not conf.get('reasoner') else
            f'ASSISTANT REASONING #{conf.get("rnd")}'
        )
        # pylint: disable-next=expression-not-assigned
        ast_stream() if conf.get('stream') else ast_nostream()

try:
    conf = conf_read()
    print()
    if conf.get('balance_chk') and conf.get('chk_url'):
        print(balance_chk())
        print()
    # print(payload_gen([],0,False))
    # exitc('INF: Debug Exit.')
    chat()
except KeyboardInterrupt:
    print()
    print('INF: Aborted.')
except requests.exceptions.Timeout as e:
    print()
    print(f'ERR: {e}')
    print('ERR: The request timed out.')
except requests.exceptions.ConnectionError as e:
    print()
    print(f'ERR: {e}')
    print('ERR: A Connection error occurred.')
# pylint: disable-next=broad-exception-caught
except Exception:
    print()
    print_exc()
    print()
    print('ERR: Unexpected error(s) occurred.')
    print('TIP: See above for more info.')
finally:
    __ = input('INF: Press Enter to exit...')
