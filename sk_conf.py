from json import load
from json.decoder import JSONDecodeError
from types import MappingProxyType as mpt

checklt_ori = {
    "stream": (True, False),
    "tool_use": (True, False),
    "autotime": (True, False),
    "prompt_control": ({
        "balance_chk": (True, False),
        "long_prompt": (False, False),
        "show_temp": (True, False),
        "show_system": (True, False),
        "hidden_models": ([], False),
        "benchmark": ({
            "enable": (False, False),
            "long": (False, False)
        }, False)
    }, False),
    "service": ({
        "DS": ({
            "KEY": ("", True),
            "model": ("prompt", False)
        }, False),
        "GLM": ({
            "KEY": ("", True),
            "model": ("prompt", False),
            "free_only": (False, False)
        }, False),
        "KIMI": ({
            "KEY": ("", True),
            "model": ("prompt", False)
        }, False),
        "QWEN": ({
            "KEY": ("", True),
            "model": ("prompt", False),
            "version": ("latest", False),
            "free_only": (False, False)
        }, False),
        "SIF": ({
            "KEY": ("", True),
            "model": ("prompt", False),
            "pro": (False, False),
            "free_only": (False, False)
        }, False),
        "LEC": ({
            "KEY": ("", True),
            "model": ("prompt", False)
        }, False),
        "FQWQ": ({
            "KEY": ("", True),
            "model": ("prompt", False),
            "free_only": (False, False)
        }, False),
        "ARK": ({
            "KEY": ("", True),
            "model": ("prompt", False)
        }, False)
    }, True)
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
            if not n.get('KEY').isascii():
                print(f'The KEY for {m} should contain ASCII characters only.')
                return {}
            if m == 'LEC':
                return key_conf
            if m == 'GLM':
                if '.' not in n.get('KEY'):
                    print('The KEY for GLM should be splitted with "." but there is none.')
                    return {}
            elif m == 'ARK':
                if len(n.get('KEY').split('-')) != 5:
                    print('The KEY for ARK should be split into 5 parts by "-".')
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

def service_infoget(service:str) -> dict:
    """Provide services' info.

    Generate tools from other functions first to reduce time-consuming function calling
    (they might be use more than once).
    Then all supported services, models and other info are listed.
    For every service, the following keys are provided:

    - full_name: str
      To simplify the selecting process, the name is usually an abbr.
      So this value is used to call the service rather formally.
    - cht_url: str
      CHaT URL.
    - chk_url: str
      balance CHecK URL. Omit it for unsupported ones.
    - temp_range: dict
      - max_temp: int
        The min temp is always 0.
      - default_temp: float
        x.xx
      - no_max: bool
        If the max temp is not allowed, set to True. Otherwise omitted.
    - models: dict
      - max_tokens: int
        The max_tokens to be passed.
        If docs don't mention it at all, or mark the max as default, then omit it.
      - tools: list
        The usable tools. Usually the web search one.
        If there is none, omit it.
      - temp_range: dict
        The same as the above one; use it to override the service setting.
      - reasoner: bool
        Whether the model is DeepSeek-R1 like.
      - free: bool
        Whether the model is free of charge.

    Root keys here can override the ones in conf (to avoid invalid usage),
    and are overriden by the ones in models (to be more model-specific).

    Dependency tree:
        - service_infoget()
            - glm_tools_gen()
            - kimi_tools_gen()
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
            'full_name': 'DeepSeek',
            'cht_url': 'https://api.deepseek.com/chat/completions',
            'chk_url': 'https://api.deepseek.com/user/balance',
            'max_tokens': 8192,
            'temp_range': {
                'max_temp': 2,
                'default_temp': 1.00
            },
            'models': {
                'deepseek-chat': {},
                'deepseek-reasoner': {
                    'reasoner': True
                }
            }
        },
        'GLM': {
            'full_name': 'ChatGLM',
            'cht_url': 'https://open.bigmodel.cn/api/paas/v4/chat/completions',
            'max_tokens': 4095,
            'temp_range': {
                'max_temp': 1,
                'default_temp': 0.95
            },
            'models': {
                'glm-4-plus': {
                    'tools': glm_tools
                },
                'glm-4-air-250414': {
                    'tools': glm_tools
                },
                'glm-4-airx': {
                    'tools': glm_tools
                },
                'glm-4-flash-250414': {
                    'tools': glm_tools,
                    'free': True
                },
                'glm-4-flashx': {
                    'tools': glm_tools
                },
                'glm-4-long': {
                    'tools': glm_tools
                },
                'glm-z1-air': {
                    'max_tokens': 30000,
                    'reasoner': True
                },
                'glm-z1-airx': {
                    'max_tokens': 30000,
                    'reasoner': True
                },
                'glm-z1-flash': {
                    'max_tokens': 30000,
                    'reasoner': True,
                    'free': True
                },
                'codegeex-4': {
                    'max_tokens': 32768
                },
                'charglm-4': {},
                'emohaa': {
                    'max_tokens': 8192
                }
            }
        },
        'KIMI': {
            'full_name': 'Moonshot',
            'cht_url': 'https://api.moonshot.cn/v1/chat/completions',
            'chk_url': 'https://api.moonshot.cn/v1/users/me/balance',
            'temp_range': {
                'max_temp': 1,
                'default_temp': 0.30
            },
            'models': {
                'moonshot-v1-auto': {
                    'tools': kimi_tools
                },
                'kimi-latest': {
                    'tools': kimi_tools
                }
            }
        },
        'QWEN': {
            'full_name': 'ModelStudio',
            'cht_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
            'temp_range': {
                'max_temp': 2,
                'default_temp': 0.70,
                'no_max': True
            },
            'models': {
                'qwen-max': {},
                'qwen-plus': {},
                'qwen-turbo': {},
                'qwen-long': {
                    'temp_range': {
                        'max_temp': 2,
                        'default_temp': 1.00,
                        'no_max': True
                    }
                },
                'qwen2.5-1.5b-instruct': {
                    'free': True
                },
                'qwen-math-plus': {
                    'temp_range': {
                        'max_temp': 2,
                        'default_temp': 0.00,
                        'no_max': True
                    }
                },
                'qwen-math-turbo': {
                    'temp_range': {
                        'max_temp': 2,
                        'default_temp': 0.00,
                        'no_max': True
                    }
                },
                'qwen2.5-math-1.5b-instruct': {
                    'temp_range': {
                        'max_temp': 2,
                        'default_temp': 0.00,
                        'no_max': True
                    },
                    'free': True
                },
                'qwen-coder-plus': {},
                'qwen-coder-turbo': {},
                'qwen2.5-coder-3b-instruct': {
                    'free': True
                },
                'qwq-plus': {
                    'reasoner': True
                },
                'qwq-32b-preview': {},
                'deepseek-v3': {
                    'max_tokens': 8192,
                    'temp_range': {
                        'max_temp': 2,
                        'default_temp': 0.70
                    }
                },
                'deepseek-r1': {
                    'max_tokens': 8192,
                    'reasoner': True
                },
                'deepseek-r1-distill-llama-70b': {
                    'max_tokens': 16384,
                    'reasoner': True,
                    'free': True
                },
                'deepseek-r1-distill-qwen-1.5b': {
                    'max_tokens': 16384,
                    'reasoner': True,
                    'free': True
                }
            }
        },
        'SIF': {
            'full_name': 'SiliconFlow',
            'cht_url': 'https://api.siliconflow.cn/v1/chat/completions',
            'chk_url': 'https://api.siliconflow.cn/v1/user/info',
            'max_tokens': 4096,
            'temp_range': {
                'max_temp': 2,
                'default_temp': 0.70
            },
            'models': {
                'deepseek-ai/DeepSeek-R1': {
                    'max_tokens': 8192,
                    'reasoner': True
                },
                'deepseek-ai/DeepSeek-V3': {},
                'deepseek-ai/DeepSeek-R1-Distill-Qwen-7B': {
                    'max_tokens': 16384,
                    'reasoner': True,
                    'free': True
                },
                'Qwen/Qwen2.5-72B-Instruct-128K': {},
                'Qwen/Qwen2.5-7B-Instruct': {
                    'free': True
                },
                'Qwen/Qwen2.5-Coder-32B-Instruct': {},
                'Qwen/Qwen2.5-Coder-7B-Instruct': {
                    'free': True
                },
                'Qwen/QwQ-32B': {
                    'reasoner': True
                },
                'Qwen/QwQ-32B-Preview': {
                    'max_tokens': 8192
                },
                'THUDM/GLM-4-32B-0414': {
                    'max_tokens': 8192
                },
                'THUDM/GLM-4-9B-0414': {
                    'max_tokens': 8192,
                    'free': True
                },
                'THUDM/GLM-Z1-32B-0414': {
                    'reasoner': True
                },
                'THUDM/GLM-Z1-9B-0414': {
                    'reasoner': True,
                    'free': True
                },
                'THUDM/GLM-Z1-Rumination-32B-0414': {
                    'reasoner': True
                },
                'THUDM/glm-4-9b-chat': {
                    'free': True
                },
                'internlm/internlm2_5-20b-chat': {},
                'internlm/internlm2_5-7b-chat': {
                    'free': True
                },
                'TeleAI/TeleChat2': {}
            }
        },
        'LEC': {
            'full_name': 'LeChat',
            'cht_url': 'https://api.mistral.ai/v1/chat/completions',
            'temp_range': {
                'max_temp': 1.5,
                'default_temp': 0.30
            },
            'models': {
                'mistral-large-latest': {
                    'temp_range': {
                        'max_temp': 1.5,
                        'default_temp': 0.70
                    }
                },
                'mistral-small-latest': {},
                'open-mistral-nemo': {},
                'codestral-latest': {},
                'open-codestral-mamba': {
                    'temp_range': {
                        'max_temp': 1.5,
                        'default_temp': 0.70
                    }
                },
                'ministral-3b-latest': {},
                'ministral-8b-latest': {}
            }
        },
        'FQWQ': {
            'full_name': 'FreeQwQ',
            'cht_url': 'https://api.suanli.cn/v1/chat/completions',
            'reasoner': True,
            'models': {
                'deepseek-r1': {},
                'deepseek-r1:7b': {
                    'free': True
                },
                'deepseek-v3': {},
                'QwQ-32B': {
                    'free': True
                },
                'free:QwQ-32B': {
                    'free': True
                },
                'pro:QwQ-32B': {}
            }
        },
        'ARK': {
            'full_name': 'VolcanoArk',
            'cht_url': 'https://ark.cn-beijing.volces.com/api/v3/chat/completions',
            'temp_range': {
                'max_temp': 1,
                'default_temp': 0.80
            },
            'max_tokens': 12288,
            'models': {
                'doubao-1.5-pro-32k-250115': {},
                'doubao-1.5-pro-256k-250115': {},
                'doubao-1.5-lite-32k-250115': {},
                'deepseek-r1-250120': {
                    'reasoner': True,
                    'max_tokens': 16384
                },
                'deepseek-v3-250324': {
                    'max_tokens': 16384
                },
                'moonshot-v1-8k': {
                    'max_tokens': 4096
                },
                'moonshot-v1-32k': {
                    'max_tokens': 4096
                },
                'moonshot-v1-128k': {
                    'max_tokens': 4096
                },
                'mistral-7b-instruct-v0.2': {
                    'max_tokens': 4096
                }
            }
        }
    }
    sinfo = info.get(service)
    return sinfo

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

# print(conf_get('sk.json'))
