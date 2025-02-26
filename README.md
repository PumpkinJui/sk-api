# sk-api

![Create At: 2025-01-09.](https://img.shields.io/github/created-at/PumpkinJui/sk-api?style=for-the-badge&logo=github&logoColor=white&color=477DB2)
[![License: CC BY 4.0.](https://img.shields.io/github/license/PumpkinJui/sk-api?style=for-the-badge&color=477DB2)](LICENSE)
![Repo Size: Various.](https://img.shields.io/github/repo-size/PumpkinJui/sk-api?style=for-the-badge&logo=python&logoColor=white&color=477DB2)

![GitHub Release: The latest release name.](https://img.shields.io/github/v/release/PumpkinJui/sk-api?display_name=tag&style=for-the-badge&color=limegreen)
![GitHub Actions Workflow Status: Building status.](https://img.shields.io/github/actions/workflow/status/PumpkinJui/sk-api/build.yml?style=for-the-badge)

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

1. 申请 API KEY。一般会提供有效期不定的体验金。更多指导见：[我该用哪款服务？](which_to_use.md)
2. 自版本 1.1.1 开始，我们在 Releases 页面提供示例配置文件。将 API KEY 填入示例 `sk.json` 文件中对应服务的 `ENTER_YOUR_KEY` 所在位置，并把用不上的删除；如果不删会有多余的报错，但不影响使用。
3. 启动程序。如果你填入了多个服务的 KEY，将需要选择使用哪个服务。然后，选择使用的模型。  
   为了避免重名，简化选择机制，服务名称使用简称。下文亦可能使用这些作为简称。它们是：
   - DS：DeepSeek，深度求索
   - GLM：ChatGLM / BigModel，智谱
   - KIMI：Moonshot Kimi，月之暗面
   - QWEN：Qwen / Model Studio，阿里百炼
   - SIF：SiliconFlow，硅基流动
4. 输入 Temperature。以下简要信息限于「不会报错」。  
   - 因为设了也没有作用，deepseek-reasoner 不展示此条。
   - 温度数值越低，对于相同的输入，输出越稳定；越高则相反，但设置过高可能出现乱码等情况。
   - 如不提供，将会自动使用默认值；默认值见输入错误时的说明。
   - 对于 DS，这是范围 [0,2] 的两位小数。更多信息见 [官方说明](https://api-docs.deepseek.com/zh-cn/quick_start/parameter_settings)。
   - 对于 GLM，这是范围 [0,1] 的两位小数。更多信息见 [官方说明](https://bigmodel.cn/dev/api/parameter-description)。
   - 对于 Kimi，这是范围 [0,2] 的两位小数。更多信息见 [官方说明](https://platform.moonshot.cn/docs/api/chat#%E5%AD%97%E6%AE%B5%E8%AF%B4%E6%98%8E)。
   - 对于 Qwen 中的大部分，这是范围 [0,2) 的两位小数。更多信息见[官方说明](https://help.aliyun.com/zh/model-studio/developer-reference/use-qwen-by-calling-api)。
5. 输入 System Prompt。建议将 AI 的身份设定输入在此处。可留空，有默认设定。末尾会自动追加当前 UTC 时间，精确到秒。因为[官方不建议设](https://github.com/deepseek-ai/DeepSeek-R1)，deepseek-reasoner 不展示此条。
6. 输入 User Prompt。支持多行，输入空行视为终止符。留空则终止对话。(这意味着，在输入该轮对话所有内容后需要**敲两次回车**才能触发回复！)
7. 等待回复。回复完成后，可以继续重复第 6 步，也可以直接敲回车终止对话。
8. 如有需要，在退出程序前通过截图、复制文本等方式保存对话内容。程序不保留历史记录。

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

本程序采用 [MIT](LICENSE) 授权，完全免费。

各家 AI 对于网页对话来说*是免费的*；对于 API 请求*则不是*。

具体定价见官方文档。

- [DeepSeek](https://api-docs.deepseek.com/zh-cn/quick_start/pricing)
- [GLM](https://open.bigmodel.cn/pricing)
- [Kimi](https://platform.moonshot.cn/docs/pricing/chat)
- [Qwen](https://help.aliyun.com/zh/model-studio/getting-started/models)

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

已使用 GitHub Actions 实现。如果您需要在其他系统上运行此程序，请提交 issues。

但出于未知原因，Termux 仍暂不支持（显示为 `error: required file not found`）；请使用源码执行。

</details>

## 结构组成

<details>

### sk.json

<details>

配置文件，使用 JSON 语言。支持的配置项如下：

- `stream`：`bool`。设定为 `true` 时，进行流式输出，`false` 反之。  
  选填项，默认为 `true`。
- `tool_use`：`bool`。设定为 `true` 时，使用 tools 进行调用，这可以启用网络搜索等功能；`false` 禁用。  
  选填项，默认为 `true`。
- `autotime`：`bool`。设定为 `true` 时，自动在系统提示词中追加当前 UTC 时间，格式为 `%Y-%m-%d %H:%M:%S`；`false` 禁用。  
  开启后，可能触发意想不到的回复 (特别是 `deepseek-reasoner` 模型)。  
  选填项，默认为 `true`。
- `prompt_control`：`dict`。配置输出控制。选填项。
  - `balance_chk`：`bool`。设定为 `true` 时，查询账户余额后再进行对话；`false` 直接进行对话，不查询余额。  
  选填项，默认为 `true`。
  - `long_prompt`：`bool`。设定为 `true` 时，需要两个空行 (三次回车) 才能触发下一步；`false` 仅需一个空行 (两次回车)。  
    适用于粘贴大段中间有空行的内容。影响系统提示词和用户提示词。  
    选填项，默认为 `false`。
  - `show_temp`：`bool`。设定为 `true` 时提示设置温度，`false` 不提示。此项不影响 `reasoner`。  
    选填项，默认为 `true`。
  - `show_system`：`bool`。设定为 `true` 时提示设置系统提示词，`false` 不提示。  
    选填项，默认为 `true`。
  - `hidden_models`：`list`。将模型全称区分大小写地填入其中，填写的模型将不会在询问时展示；该列表对全部服务适用。模型名称请以选择成功时的提示结果为准，不要以选择列表或重映射信息为准。  
    选填项，默认为 `[]`。
- `service`：`dict`。具体配置各大模型的信息。必填项。
  - `DS`：`dict`。配置 DeepSeek 的信息。选填项。
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
      - glm-4-plus
      - glm-4-air-0111
      - glm-4-airx
      - glm-4-flash
      - glm-4-flashx
      - glm-4-long
      - glm-zero-preview
      - codegeex-4
      - charglm-4
      - emohaa
    - `jwt`：`bool`。指定在传输时是否使用 jwt 对 KEY 进行加密 (即使用鉴权 token 进行鉴权)。  
      选填项，默认为 `True`。这不影响直接传入鉴权 token。
  - `KIMI`：`dict`。配置 Kimi 的信息。选填项。
    - `KEY`：`str`。API KEY。必填项。
    - `model`：`str`。选择使用的模型。  
      选填项，默认为 `prompt`。可选项包括：
      - prompt
      - moonshot-v1-auto
      - kimi-latest
  - `QWEN`：`dict`。配置 ModelStudio 的信息。选填项。
    - `KEY`：`str`。API KEY。必填项。
    - `model`：`str`。选择使用的模型。  
      选填项，默认为 `prompt`。可选项包括：
      - prompt
      - qwen-max
      - qwen-plus
      - qwen-turbo
      - qwen-long
      - qwen-math-plus
      - qwen-math-turbo
      - qwen-coder-plus
      - qwen-coder-turbo
      - deepseek-v3
      - deepseek-r1
      - qwq-32b-preview
    - `version`：`str`。选择使用的模型版本。  
      选填项，默认为 `latest`。可选项包括：
      - latest
      - stable
      - oss
  - `SIF`：`dict`。配置 SiliconFlow 的信息。选填项。
    - `KEY`：`str`。API KEY。必填项。
    - `model`：`str`。选择使用的模型。  
      选填项，默认为 `prompt`。可选项包括：
      - prompt
      - deepseek-ai/DeepSeek-R1
      - deepseek-ai/DeepSeek-V3
      - deepseek-ai/DeepSeek-R1-Distill-Llama-8B
      - deepseek-ai/DeepSeek-R1-Distill-Qwen-7B
      - meta-llama/Llama-3.3-70B-Instruct
      - meta-llama/Meta-Llama-3.1-8B-Instruct
      - Qwen/Qwen2.5-72B-Instruct-128K
      - Qwen/Qwen2.5-7B-Instruct
      - Qwen/Qwen2.5-Coder-32B-Instruct
      - Qwen/Qwen2.5-Coder-7B-Instruct
      - Qwen/QwQ-32B-Preview
      - THUDM/glm-4-9b-chat
      - internlm/internlm2_5-20b-chat
      - internlm/internlm2_5-7b-chat
      - AIDC-AI/Marco-o1
      - SeedLLM/Seed-Rice-7B
      - TeleAI/TeleChat2
    - `pro`：`bool`。设为 `true` 时如能使用 Pro 版模型则自动使用，反之不使用。Pro 版与普通版有扣费渠道、最大输出、限流等一系列差异。  
      选填项，默认为 `false`。

</details>
</details>

## TODO

- [ ] 适配更多服务
- [ ] `sk_conf`：
      - [ ] 查询配置功能
      - [ ] 更改配置功能
- [ ] KEY：
      - [ ] 加密存储
      - [ ] 多个 KEY，分压
- [x] 添加配置：部分选项直接设为默认或配置值
- [ ] 将 README 中的一些操作说明作为 `TIP` 加入主程序中 (可能需要增加配置项)
- [ ] 将 README 中的函数介绍内嵌
- [ ] 截断/触发限流自动继续 (需考虑如何处理 DeepSeek 目前的繁忙状态)
- [ ] Command-Line Switch
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
- [Kimi API Docs](https://platform.moonshot.cn/docs/intro)
- [ModelStudio API Docs](https://help.aliyun.com/zh/model-studio/)
- [SiliconFlow API Docs](https://docs.siliconflow.cn/cn/userguide/introduction)
