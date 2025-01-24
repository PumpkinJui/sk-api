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
  - 克隆本仓库。你可以使用 Git，或直接下载源码并解压。
  - 打开命令行窗口。在 Windows 上，按 `Win+R`，输入 `cmd` 后回车。
  - 定位到源码所在的目录。使用 `cd /path/to/dir` 即可，如果没有作用可以使用 `cd /d /path/to/dir`。
  - 输入 `pip install -r requirements.txt`，等待执行完毕。
  - 使用 `python sk_chat.py` 运行。

### 开始使用

1. 申请 API KEY。一般会提供有效期不定的体验金。
   - [DeepSeek Platform](https://platform.deepseek.com/api_keys)
   - [BigModel Platform](https://bigmodel.cn/usercenter/apikeys)
2. 将 API KEY 按 JSON 格式填入 `sk.json` 文件，位于 `service` 下 `DSK` 或 `GLM` 中的 `KEY` 键。例如：
   ```json
   {
       "service": {
           "DSK": {
               "KEY": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
           }
       }
   }
   ```
3. 启动程序。如果你填入了两个服务的 KEY，将需要选择使用哪个服务。然后，选择使用的模型。
4. 输入 Temperature。对 deepseek-reasoner 不起作用。以下简要信息限于「不会报错」。  
   - 对于 DSK，这是介于 0 和 2 之间的两位小数，包含两端。更多信息见 [DeepSeek 官方说明](https://api-docs.deepseek.com/zh-cn/quick_start/parameter_settings)。可留空，默认为 1.00。
   - 对于 GLM，这是介于 0 和 1 之间的两位小数，包含两端。更多信息见 [BigModel 官方说明](https://bigmodel.cn/dev/api/parameter-description)。可留空，默认为 0.95。
5. 输入 System Prompt。建议将 AI 的身份设定输入在此处。可留空，有默认设定。末尾会自动追加当前 UTC 时间，精确到秒。
6. 输入 User Prompt。支持多行，输入空行视为终止符。留空则终止对话。(这意味着，在输入该轮对话所有内容后需要**敲两次回车**才能触发回复！)
7. 等待回复。回复完成后，可以继续重复第 4 步，也可以直接敲回车终止对话。
8. 如有需要，在退出程序前保存对话内容。程序不保留历史记录。

### 自行打包

下载本仓库，并在命令行定位到本仓库对应的目录。在安装 Python 后：

```shell
pip install -r requirements.txt
pyinstaller --clean --version-info file-version-info.txt -n sk-api -F sk_chat.py
```

## FAQ

### 做这个程序有什么意义？

如[此文](rationale.md)。

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

### 和网页版的区别

<details>

**各有优劣。**

网页版不能设温度，也不能设系统提示词；但是网页版有更多其他功能，能直接输入连续的空行，而且是免费的。API 虽然几乎相当于没收钱，毕竟还是收了的 (glm-4-flash 除外)。

API 更为灵活，因此可以在网页对话之外的众多场景中使用。

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
- `balance_chk`：`bool`。设定为 `true` 时，查询账户余额后再进行对话；`false` 直接进行对话，不查询余额。  
  选填项，默认为 `true`。
- `long_prompt`：`bool`。设定为 `true` 时，需要两个空行 (三次回车) 才能触发下一步；`false` 仅需一个空行 (两次回车)。  
  适用于粘贴大段中间有空行的内容。影响系统提示词和用户提示词。  
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
