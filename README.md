# sk-api

![Create At: 2025-01-09.](https://img.shields.io/github/created-at/PumpkinJui/sk-api?style=for-the-badge&logo=github&logoColor=white&color=477DB2)
[![License: CC BY 4.0.](https://img.shields.io/github/license/PumpkinJui/sk-api?style=for-the-badge&logo=creativecommons&logoColor=white&color=477DB2)](LICENSE)
![Repo Size: Various.](https://img.shields.io/github/repo-size/PumpkinJui/sk-api?style=for-the-badge&logo=gitbook&logoColor=white&color=477DB2)

[![Commit Activity: How many commits are there in total.](https://img.shields.io/github/commit-activity/t/PumpkinJui/sk-api?style=for-the-badge&color=yellow)](https://github.com/PumpkinJui/sk-api/commits/main/)
![Last Commit: When was the last commit made.](https://img.shields.io/github/last-commit/PumpkinJui/sk-api?display_timestamp=author&style=for-the-badge&color=yellow)

通过调用大模型 API，在 Python 或 CLI 中进行 AI 对话补全。

嫌 CLI 界面太丑，MarkDown 不渲染？试试 [NextChat](https://app.nextchat.dev/)！  
个人推荐，非广告；NextChat 与本人无利益关联。

## 功能特性

- 多轮对话
- 流式传输 (默认禁用)
- 多行输入输出
- 温度 (temperature)、系统提示词 (system prompt) 设定
- 极致轻简 (打包后仅占 6 MB 空间)

## 兼容性

兼容 Windows 7 32-bit 及以上。

## 使用方法

### 下载

- Windows 可执行文件：在 [Releases 页面](https://github.com/PumpkinJui/sk-api/releases/) 下载最新版的 EXE 可执行文件。下载后双击运行。
- 源码运行：
  - 安装 Python。在安装时，请勾选 「Add to PATH」 一项。
  - 打开命令行窗口 (在 Windows 上，按 `Win+R`，输入 `cmd` 后回车)，输入 `pip install --upgrade requests`，等待执行完毕。
  - 下载本仓库中的 `sk_chat.py` 和 `sk_conf.py`，放在同一目录下。
  - 在命令行使用 `cd /path/to/dir/` 定位到该目录，使用 `python sk_chat.py` 运行。(在 Windows 上，有时需要用 `cd /d /path/to/dir/` 来定位。)

### 开始使用

1. 如果没有配置文件，输入 API KEY。请在 [DeepSeek Platform](https://platform.deepseek.com/api_keys) 申请，沉浸式翻译的文档里有一份[申请教程](https://immersivetranslate.com/zh-Hans/docs/services/deepseek/)。使用中国大陆手机号注册开放平台账户，即可获得 10 元的 API 体验金，有效期一个月。
2. 输入 Temperature。这是介于 0 和 2 之间的一位小数，包含两端。更多信息见 [DeepSeek 官方说明](https://api-docs.deepseek.com/zh-cn/quick_start/parameter_settings)。可留空，默认为 1.0。
3. 输入 System Prompt。建议将 AI 的身份设定输入在此处。可留空，有默认设定。
4. 输入 User Prompt。支持多行，输入空行视为终止符。留空则终止对话。(这意味着，在输入该轮对话所有内容后需要**敲两次回车**才能触发回复！)

### 自行打包

下载本仓库，并在命令行定位到本仓库对应的目录。在安装 Python 后：

```shell
pip install -r requirements.txt
pyinstaller --clean --version-info file-version-info.txt -n sk-api -F sk_chat.py
```

## FAQ

大多数人的表现就是这样子的：「听上去好厉害哦，但具体来说……」

### 和网页版的区别

<details>

**各有优劣。**

网页版不能设温度，也不能设系统提示词；但是网页版有更多其他功能，能直接输入连续的空行，而且是免费的。API 虽然几乎相当于没收钱，毕竟还是收了的 (glm-4-flash 除外)。

API 更为灵活，因此可以在网页对话之外的众多场景中使用。

</details>

### 意义

<details>

……其实有的时候我挺讨厌这个问题的，干就完了管什么意义不意义的。问那么多意义不虚无主义吗。

好吧我还是回答一下。

最早做这个是意外注册了 DeepSeek 的开放平台账号，发现居然有 10 块钱，还一个月就到期。于是弄了一个 API KEY，把它挂上了[沉浸式翻译](https://immersivetranslate.com/)。

然后在翻译的时候发现这玩意质量特别高：我原来用的是免费的智谱翻译，在它没出时还用过微软翻译，有时还用腾讯交互翻译。  
后面这些服务在翻译 [Harry Potter Wiki](https://harrypotter.fandom.com/wiki/) 时全部处于蒙圈状态：人名翻译准不准确要看心情和运气，比如智谱，即使我专门配置了对 HPW 的提示词，还是对各位姓或名由 S 开头的分不清楚，斯拉格霍恩 (Slughorn) 和斯内普 (Snape) 全都变成了斯莱特林 (Slytherin)；咒语更是基本没有翻译对的，只有阿瓦达索命、呼神护卫等知名咒语翻译是准的。  
而 DeepSeek 没有译错的人名，咒语也能译对很多……

于是后来就想把手机里面的通义扔了换成 DeepSeek (吐槽通义不好好做对话弄一堆舞王和活动什么的)，但是发现它没做 APP；而我浏览器从来不记录历史记录和登录状态，它还每次要我验证码，就很难办了。  
最后我把通义换了 Kimi，但是还是想用 DeepSeek，那就跟着 API 文档鼓捣呗。

我手机上用的是 Termux。一开始看见文档有 CURL，就想用 Linux Bash 实现。后来靠着 AI (主要指 Kimi) 做出来非流式传输的多轮对话；还有 bug，不知道为什么一滚屏就不能多轮对话了，说我有控制字符；而且也不能多行输入，可能也是我当时没考虑到做这个。  
后来做流式传输时被多行输出卡住了，不管怎么改，都要么吞换行，要么显示成 n。于是索性掀桌不做了。

然后转战 Python。Python 是我的编程第一语言了，但是一上来就因为我 Termux 用的 Python 版本太新，装不上 OpenAI 的第三方库；于是改用 requests，靠改示例代码，写出来了这个程序。除了在手机上的编辑 (拿不上电脑导致的) 以外，有相当一部分工作 (包括 0.9 的打包) 都是在南 219 机房做的，因为那的电脑是 Windows 7 32-bit，我理想中的最低兼容目标。  
1.0 是人脑执行程序发现 bug 以后急急忙忙改的，最后借科夫的 Windows 7 64-bit 电脑，现场装了个 32 位的 Python 3.8.10 打包。至此 1.0 版本完工，当然也有需要优化的代码和新增的功能，但可用性已经很强了。再后来，就把这玩意上了 GitHub。

所以说了这么多，到底有什么意义呢？

折腾的意义，让我不用验证码同时用上 DeepSeek 的意义，学习 Bash 和 requests 的意义，甚至耍帅的意义。

或者在拿不上手机的场景、一人付费大家共享的场景，放在班里面大家公用一类的……

真要往大点说，毕竟这一套东西是和 OpenAI 接口兼容的，我改个网址就可以换成其他 AI……变相实现了 OpenAI 库的一些功能？

这么看来，意义么，我想做就好了。「想」比任何意义都管用。

<details>
<summary>
延伸阅读：價值評估 (节选)
</summary>

> 價值評估
>
> 價值的起點是一個真實的問題。當我們看到一個值得解決的問題，並清晰地認識到其背後的價值時，就會產生繼續推進的動力。而脫離了「實際問題」這個根基，整個計劃的目標就變成了一個「空想」，因此其未來自然是不明朗的。
>
> 明確價值，實際上就是在回答這樣的一個問題：「完成這個計劃的過程和結果能給我們帶來什麼樣的好處？」這裡得到的理由越充分，把計劃執行完的可能性就越高。
>
> ……
>
> 除了對自身價值的評估之外，計劃本身的價值也需要被納入考量。對價值的評估始於明確的「問題」。尤其是針對「開發軟體」、「製作遊戲」或者「寫本小說」這種企劃，在給它們的價值做定性的時候，最先需要回答的問題便是「這個計劃究竟解決了什麼問題？」
>
> 一個軟體在解決的問題可能是「工作效率」，而一款遊戲在解決的問題可能是「表達一個觀念、保存一段文化、記錄一個故事」。明確了這個問題之後我們便可以藉由問題的價值來推估整個計劃價值的天花板。具體的做法有很多：比如，從「有多少人關注這個問題？」這樣的角度來進行推算。再比如，假設你希望藉由這個計劃獲取資金上的利益的話，不妨再來進一步評估一下：「人們願意為了這個問題付出多少錢？」藉著這些資訊我們可以通過一個粗糙的乘法得到大致的盈利空間。
>
> 與如夢似幻的想像不同，以上討論到的「具象化概念」可以幫助我們找到計劃的「不可替代性」，進而為計劃長期執行提供持續性動力，而非單純地依靠「開坑嗎啡」做「短程衝刺」。
>
> ……
>
> 无论这个计划最终呈现出来的效果是怎样的，它对于我们的价值都独一无二，值得我们去呵护和坚守。
>
> ⸺《當代學生生存手冊》

</details>
</details>

### 它能干什么

<details>

用专业一点的说法，就是上面那句：「通过调用大模型 API，在 Python 或 CLI 中进行 AI 对话补全。」

用更容易理解的说法，就是这样的：(以下内容由本程序辅助生成)

> 简单来说，这个程序就像是一个桥梁，让你可以轻松地与一个聪明的 AI 助手对话，而不需要了解复杂的技术细节。
>
> API (应用程序编程接口) 就像是一个「服务员」或「中间人」，它帮助不同的软件或应用程序之间进行沟通和协作。想象一下，你去一家会员制餐厅吃饭。你不需要知道厨房里是如何做菜的，你只需要出示会员卡，告诉服务员你想要什么，服务员会把你的需求传达给厨房，然后把做好的菜端给你。
>
> API 就像这个服务员，它让不同的软件系统之间能够互相「点菜」和「上菜」，而不需要知道对方内部的具体实现细节。
>
> 而 API 密钥则像是那张会员卡，可以用来证明你的身份，如果没有它你就点不了菜，用不了更优惠的价格。
>
> 为了进行对话，你可以在命令行界面 (CLI) 运行已经打包好的程序，或者通过 Python 直接运行本程序的源码。

</details>

### 它是否收费

<details>

**本程序采用 [MIT](LICENSE) 授权，完全免费。**

**对于网页对话来说 *是免费的*；对于 API 请求*则不是*。**

具体定价见官方文档。[DeepSeek](https://api-docs.deepseek.com/zh-cn/quick_start/pricing)、[GLM](https://open.bigmodel.cn/pricing)。

</details>

### 那么既然可以免费用，为什么我要付费？

<details>

如果真的不喜欢付费，**你也可以直接使用免费的网页对话**。我喜欢用 API 的理由是它灵活开放，而且不用验证码。

API 提供的是一个更广阔的世界。例如，你还可以把它挂到[沉浸式翻译](https://immersivetranslate.com/)上面，获得更高质量的网页翻译。

还有许多像这样能接入 AI 的软件，[Awesome DeepSeek Integration](https://github.com/deepseek-ai/awesome-deepseek-integration) 中提供了一部分示例。这就是说，通过使用 API，你还可以使用不仅限于本程序的其他许多程序。

通过 API，也不必限于在浏览器和 APP 里用 AI 了，本程序实现的就是这个。

另外，也不是必须只用 API 不用网页版，这两者并不排斥。

</details>

### 它能否离线运行

<details>

**不能**。因为本程序是用 API 进行远程服务器请求，而不是本地大模型进行生成，所以必须联网。

如果有离线需求，请考虑本地大模型。教程请在[少数派 sspai](https://sspai.com/)等网站进行搜索。

</details>

### 其他系统打包可执行文件计划

<details>

~~**暂时没有计划**。Pyinstaller 决定了我只能有什么系统打包什么系统，而我只用 Windows 和 Termux；而 Termux 的 Python 版本 (或者兼容机制) 把我背刺了，装不上 Pyinstaller，就干脆打包不了了。我自己用的都是源码执行。~~

后续考虑 GitHub Actions。

</details>

## 结构组成

<details>

### sk.json

<details>

配置文件，使用 JSON 语言。支持的配置项如下：

- `stream`：`bool`。设定为 `true` 时，进行流式输出，`false` 反之。  
  选填项，默认为 `true`。
- `balance_chk`：`bool`。设定为 `true` 时，查询账户余额，输出后自动退出；`false` 进行对话。  
  选填项，默认为 `false`。
- `long_prompt`：`bool`。设定为 `true` 时，需要两个空行 (三次回车) 才能触发回复；`false` 仅需一个空行 (两次回车)。  
  适用于粘贴大段中间有空行的内容。系统提示词始终为单行输入，不受此影响。  
  选填项，默认为 `false`。
- `tool_use`：`bool`。设定为 `true` 时，使用 tools 进行调用，这可以启用网络搜索等功能；`false` 禁用。  
  选填项，默认为 `true`。
- `service`：`dict`。具体配置各大模型的信息。必填项。
  - `DSK`：`dict`。配置 DeepSeek 的信息。选填项。
    - `KEY`：`str`。API KEY。必填项。
    - `model`：`str`。选择使用的模型。  
      选填项，默认为 `prompt`。可选项包括：
      - prompt
      - deepseek-chat
      - deepseek-reasoner
  - `GLM`：`dict`。配置 ChatGLM 的信息。选填项。
    - `KEY`：`str`。API KEY。必填项。
    - `model`：`str`。选择使用的模型。  
      选填项，默认为 `prompt`。可选项包括：
      - prompt
      - glm-zero-preview
      - glm-4-plus
      - glm-4-air-0111
      - glm-4-airx
      - glm-4-flash
      - glm-4-flashx
      - glm-4-long
      - codegeex-4
      - charglm-4
      - emohaa
    - `jwt`：`bool`。指定在传输时是否使用 jwt 对 KEY 进行加密 (即使用鉴权 token 进行鉴权)。  
      选填项，默认为 `True`。这不影响直接传入鉴权 token。

</details>

### sk_conf.py

<details>

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
  在此处设置为 `True` 时，推荐将 `value` 设置为 `None`、`""` (如果类型为 `str`) 等空值。  
  这可以使它看上去更整洁。即使不这么设置，也不会影响执行结果。

#### `confDefault(ref:dict=checklt) -> dict`

根据 `ref` 递归式生成并返回默认配置。

#### `confCheck(confG:dict,ref:dict=checklt) -> dict`

根据 `ref` 中的配置，检查 `confG` 中的自定义配置。检查项包括：

- 键名称是否包含在可用配置列表内。
- 键对应值是否符合指定类型。
- 如果键对应值是字典，检查其是否为空，并在非空时进行递归。

对于非法的自定义配置项，输出一条警告，并跳过该配置项。

检查后，返回合法的自定义配置。

#### `confMerge(confE:dict,confI:dict=confDefault(),ref:dict=checklt) -> dict`

首先，检查必填项是否已经填写。未填写必填项将返回 `False`。

然后，将 `confE` 中的配置项合并到 `confI` 中。`confI` 中原有的配置项将被覆盖。

最后，检查 KEY 的填写格式。如果格式正确，返回合并后的配置；否则返回 `False`。

#### `confRcheck(confR:dict,ref:dict=checklt) -> dict`

根据 `ref` 中的配置，检查必填项是否已经填写。

如果有任一必填项未填写，输出一条错误信息，并返回 `False`；否则返回原配置。

#### `KEYcheck(confK:dict) -> dict`

本程序专用的 KEY 格式检查函数。原理为：

- GLM 的 KEY 和鉴权 token 均由 `.` 作为分隔符；
- 其他 (DeepSeek、Qwen、Kimi) 均由 `sk-` 开头。后两者可能在未来添加。

因默认配置中 GLM 无 KEY，但在前序环节无法筛查，先检查 GLM 是否存在 KEY。如不存在，删除此键。

然后，进行 KEY 格式检查。检查通过返回配置，不通过返回 `False`。

#### `confGet(confFile:str) -> dict`

读取自定义配置文件 `confFile`。该文件应为 JSON 格式。

如果该文件不存在，或不合 JSON 语法，输出一条错误信息，并返回默认配置。

如果该文件存在并合 JSON 语法，检查所有配置项，将合法配置合并进默认配置，并返回合并后的配置。

</details>

### sk_chat.py

<details>

对话主脚本。

#### `exitc(reason:str='') -> None`

输出 `reason` 并抛出 `SystemExit`。这将导致剩余所有部分不再执行，等待用户确认退出。没有返回值。

#### `conf_read() -> dict`

#### `service_model(keyword:str,lt:tuple,lower:bool=True,sts:str='prompt') -> str`

#### `service_infoget(service:str) -> dict`

#### `token_gen() -> str`

#### `headers_gen(contype:bool=True) -> dict`

根据使用场景 (`contype` 在 `balance_chk` 场景为 `False`)，生成请求 headers 并返回。

#### `data_gen(msg:list,temp:float,stream:bool) -> str`

根据各参数值，生成 JSON 格式的请求信息并返回。

#### `temp_get() -> float`

#### `usr_get(rnd:int) -> dict`

输出 `User #rnd`，并获取用户的多行输入。

用户可以输入多行连续的内容。当输入空行 (连续敲两次回车) 时：

- 如果已经有了输入内容，将所有内容使用 `\n` 拼接在一起，以 `messages` 格式返回。
- 如果没有输入内容，因 `Null input; chat ended.` 调用 `exitc(reason)`。

#### `ast_nostream(msg:list,temp:float) -> None`

在 `stream` 为 `False` 时执行的部分。

根据各参数值，使用 `requests` 库进行非流式传输请求。

如果请求成功 (HTTP-200)，提取返回内容中的生成文本，输出并以 `messages` 格式添加到 `msg` 中。

如果请求失败，因 `status_code message` 调用 `exitc(reason)`。

没有返回值。

#### `ast_stream(msg:list,temp:float) -> None`

在 `stream` 为 `True` 时执行的内容。

根据各参数值，使用 `requests` 库进行流式传输请求。

如果请求成功 (HTTP-200)，不断提取返回内容中的新生成文本并输出；全部传输完毕后，将整段生成文本以 `messages` 格式添加到 `msg` 中。

如果请求失败，因 `status_code message` 调用 `exitc(reason)`。

没有返回值。

#### `emohaa_meta() -> dict`

#### `site_models() -> None`

#### `balance_chk() -> None`

使用 `requests` 库，向远程服务器 `url` 发送请求，查询指定 KEY 对应账户的余额。

如果查询成功 (HTTP-200)，因 `INF: total_balance currency left in the DeepSeek balance.` (类似于 `1.23 CNY`) 调用 `exitc(reason)`。

如果查询失败，因 `status_code message` 调用 `exitc(reason)`。

#### ` chat() -> None`

首先，获取 `Temperature`，并在其不合法时，反复提示正确格式并重新获取输入；此处为空将使用默认的 `1.0`。

然后，获取 `System Prompt`，并将其以 `messages` 格式添加到 `msg` 中；此处为空将使用默认的 `You are a helpful assistant.`

之后，使用之前的多个函数，进行多轮对话。

没有返回值。

#### main

整体上是一个大型的 `try-except-finally` 结构，用于在停止执行后等待用户确认退出。

首先，获取配置或生成配置。

然后，在 `balance_chk` 为 `True` 时进行余额查询：如果指定服务不支持余额查询，则退出。

之后，进行对话。

如果触发了 `SystemExit`，直接转至 `finally` 块，等待用户确认退出。

如果触发了 `KeyboardInterrupt`，输出 `Aborted.`。

如果触发了其他异常，输出 `Traceback` 错误信息。

在任何情况下，最后都会提示用户按回车退出，以等待用户查看信息并确认退出。

</details>
</details>

## TODO

- [ ] 适配更多服务
      - [ ] QWEN
      - [ ] KIMI
- [ ] `sk_conf`：
      - [ ] `[1]` 疑似没有必要存在下去
      - [ ] 查询配置功能
      - [ ] 更改配置功能
- [ ] KEY：
      - [ ] 加密存储
      - [ ] 多个 KEY，分压
- [ ] 减少输出内容。(可能需要增加配置项)
- [ ] 添加配置：部分选项直接设为默认或配置值
- [ ] 增加异常处理：网络异常
- [ ] 将 README 中的一些操作说明作为 `TIP` 加入主程序中 (可能需要增加配置项)
- [ ] 将 README 中的函数介绍内嵌
- [ ] 截断自动继续
- [ ] Command-Line Switch
- [ ] GitHub Actions 自动打包
- [ ] 【高难】适配 `glm-4-alltools`
- [ ] 【高难】多模型对比

### Not-Planned

- MarkDown/LaTeX 渲染
- 历史记录
- 中途更改 Temperature 和 System Prompt
- 更改 `search_prompt`

## 参考文档

- [DeepSeek API Docs](https://api-docs.deepseek.com/zh-cn/)
- [BigModel API Docs](https://bigmodel.cn/dev/welcome)
- [Qwen API Docs](https://help.aliyun.com/zh/model-studio/)
- [Kimi API Docs](https://platform.moonshot.cn/docs/intro)
