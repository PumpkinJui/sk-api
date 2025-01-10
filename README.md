# sk-api

通过调用 [DeepSeek API](https://api-docs.deepseek.com/zh-cn/)，在 Python 或 CLI 中进行 AI 对话补全。

## 兼容性

兼容 Windows 7 32-bit 及以上。

## 使用方法

1. 如果没有配置文件，输入 API KEY。请在 [DeepSeek Platform](https://platform.deepseek.com/) 申请。首次注册时，有有效期一个月的免费 10 元额度可用。
2. 输入 Temperature。这是介于 0 和 2 之间的一位小数，包含两端。更多信息见 [DeepSeek 官方说明](https://api-docs.deepseek.com/zh-cn/quick_start/parameter_settings)。可留空，默认为 1.0。
3. 输入 System Prompt。建议将 AI 的身份设定输入在此处。可留空，有默认设定。
4. 输入 User Prompt。支持多行，输入空行视为终止符。留空则终止对话。(这意味着，在输入该轮对话所有内容后需要**敲两次回车**才能触发回复！)

### 打包

在安装 Python 后：

```shell
pip install --upgrade requests pyinstaller
pyinstaller --clean --version-info file-version-info.txt -n sk-api -F sk_chat.py
```

## 结构组成

### sk.json

配置文件，使用 JSON 语言。支持的配置项如下：

- `KEY`：`str`。DeepSeek API KEY。  
  必填项。
- `stream`：`bool`。设定为 `true` 时，进行流式输出，`false` 反之。  
  选填项，默认为 `false`。
- `balance_chk`：`bool`。设定为 `true` 时，查询账户余额，输出后自动退出；`false` 进行对话。  
  选填项，默认为 `false`。

### sk_conf.py

通用配置读取模块。

#### `checklt`

配置对照表。格式如下：

```python
key: [value,vtype,required]
```

- `key`：键名称；`str`。
- `value`：该键对应值；any。
- `vtype`：对应值所属类型；`type`。
- `required`：是否必填；`bool`。  
  在此处设置为 `True` 时，推荐将 `value` 设置为 `None`；即使不设置，也大概率不会影响执行结果。

#### `confDefault()`

根据 `checklt` 生成并返回默认配置。

#### `confCheck(confG)`

根据默认配置，检查 `confG` 中的自定义配置。检查项包括：

- 键名称是否包含在可用配置列表内。
- 键对应值是否符合指定类型。

对于非法的自定义配置项，输出一条警告，并跳过该配置项。

检查后，返回合法的自定义配置。

#### `confMerge(confD,confC)`

将 `confC` 中的配置项合并到 `confD` 中。`confD` 中原有的配置项将被覆盖。

随后，检查必填项是否已经填写；如果有任一必填项未填写，输出一条错误信息，并返回 `False`。

如果必填项全部填写，返回合并后的配置。

#### `confGet(confFile)`

读取自定义配置文件 `confFile`。该文件应为 JSON 格式。

如果该文件不存在，或不合 JSON 语法，输出一条错误信息，并返回默认配置。

如果该文件存在并合 JSON 语法，检查所有配置项，将合法配置合并进默认配置，并返回合并后的配置。

### sk_chat.py

对话主脚本。

#### `exitc(reason=str)`

输出 `reason` 并抛出 `SystemExit`。这将导致剩余所有部分不再执行，等待用户确认退出。没有返回值。

#### `confGen()`

在 `KEY` 不存在时，提示用户输入 `KEY` 并将其写入配置文件。会检查输入是否为空，为空时重复提示输入。

返回新自定义配置中的合法部分，与默认配置合并后的配置。相当于 `confGet('sk.json')` 除打开配置文件以外的其他操作。

#### `balance_chk(KEY=str)`

使用 `requests` 库，向远程服务器发送请求，查询指定 KEY 对应账户的余额。

如果查询成功 (HTTP-200)，以 `total_balance currency` (类似于 `1.23 CNY`) 的形式返回余额。

如果查询失败，因 `status_code message` 调用 `exitc(reason)`。

*这里的逻辑其实可以再改一改，查询成功时也直接调用 `exitc(reason)`，而不是返回到 `main` 以后再退出……？*

#### `usr_get(rnd=int)`

输出 `User #rnd`，并获取用户的多行输入。

用户可以输入多行连续的内容。当输入空行 (连续敲两次回车) 时：

- 如果已经有了输入内容，将所有内容使用 `\n` 拼接在一起，以 `messages` 格式返回。
- 如果没有输入内容，因 `Null input; chat ended.` 调用 `exitc(reason)`。

#### `data_gen(msg=list,temp=float,stream=bool)`

根据各参数值，生成 JSON 格式的请求信息并返回。

#### `ast_nostream(url=str,headers=dict,msg=list,temp=float)`

在 `stream` 为 `False` 时执行的部分。

根据各参数值，使用 `requests` 库进行非流式传输请求。

如果请求成功 (HTTP-200)，提取返回内容中的生成文本，输出并以 `messages` 格式添加到 `msg` 中。

如果请求失败，因 `status_code message` 调用 `exitc(reason)`。

没有返回值。

#### `ast_stream(url=str,headers=dict,msg=list,temp=float)`

在 `stream` 为 `True` 时执行的内容。

根据各参数值，使用 `requests` 库进行流式传输请求。

如果请求成功 (HTTP-200)，不断提取返回内容中的新生成文本并输出；全部传输完毕后，将整段生成文本以 `messages` 格式添加到 `msg` 中。

如果请求失败，因 `status_code message` 调用 `exitc(reason)`。

没有返回值。

#### `chat(KEY=str,stream=bool)`

首先，获取 `Temperature`，并在其不合法时，反复提示正确格式并重新获取输入；此处为空将使用默认的 `1.0`。

然后，获取 `System Prompt`，并将其以 `messages` 格式添加到 `msg` 中；此处为空将使用默认的 `You are a helpful assistant.`

之后，使用之前的多个函数，进行多轮对话。

没有返回值。

#### main

整体上是一个大型的 `try-except-finally` 结构，用于在停止执行后等待用户确认退出。

首先，获取配置或生成配置。

然后，在 `balance_chk` 为 `True` 时进行余额查询，并因一条生成的余额信息调用 `exitc(reason)`。

之后，进行对话。

如果触发了 `SystemExit`，直接转至 `finally` 块，等待用户确认退出。

如果触发了 `KeyboardInterrupt`，因 `Aborted.` 调用 `exitc(reason)`。

*此处逻辑也可更改；即使只是 `print()` 也可以转至 `finally` 块，完全不需要 `exitc(reason)`。*

如果触发了其他异常，输出 `Traceback` 错误信息。

在任何情况下，最后都会提示用户按回车退出，以等待用户查看信息并确认退出。

## 参考文档

- [DeepSeek API Docs](https://api-docs.deepseek.com/zh-cn/)
