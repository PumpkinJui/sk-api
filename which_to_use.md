# 我该用哪款服务？

当我们支持的平台越来越多时，我们意识到，选择用哪个平台的大模型及注册 API 密钥，对用户（尤其是对此行业不甚了解的用户）来说难度很高。本文旨在解决此问题。

> 说明
>
> 此处使用的缩写和程序内部使用一致。简表如下：
>
> - DS：DeepSeek，深度求索
> - GLM：ChatGLM / BigModel，智谱
> - KIMI：Moonshot Kimi，月之暗面
> - QWEN：Qwen / Model Studio，阿里百炼
> - SIF：SiliconFlow，硅基流动
>
> 体验金数据主要为个人注册时获取到的，可能有所变动。

## TL;DR

个人优先 QWEN 和 SIF 吧。

DeepSeek 官方容易繁忙（但是输出速度真快），智谱模型不抗打，Kimi 小贵不如用 APP（那个 k1.5 没有 API 接口）。

## DS

### API KEY

- [API KEY 管理页面](https://platform.deepseek.com/api_keys)

### 优势

不谈了，但凡过了 2025 这个年都已经知道它有多好多火了。

体验金是 10 元，一个月有效期。

### 劣势

服务器繁忙，请稍后再试。

在 API 端也有类似的情况，一次只能问一轮，我还没做历史记录。

如果等了 30 s 还没动静（显示为重复提示「请等待」），基本就是废了。能回复两次提示内应该会回复的。

另外目前联不了网，没这个接口。目前我做过的所有平台，DeepSeek 都不能上网。

## GLM

### API KEY

- [API KEY 管理页面](https://bigmodel.cn/usercenter/apikeys)

### 优势

能联网，另外有一些比较特别的模型，比如角色扮演和心理辅导。

`glm-zero-preview` 和 `DeepSeek-R1` 有点像，但是效果差远了。`glm-4-flash` 免费。

体验金爆炸，1600w air 专用 + 200w plus 专用 + 200w 所有按 token 计费的模型通用 + 400 次图片生成（这个程序用不上）。实名再送 500w 通用。「资源包」量大又便宜。

### 劣势

质量不过硬，我是相对 `DeepSeek-V3` 和通义千问系列说的。时不时该联网不联网，搜到的数据也是稍旧的。

`glm-zero-preview` 完全和 `DeepSeek-R1` 没有可比性。glm0 时不时就不思考了，思考也是在输出内容内部思考的（没有专门的 `reasoning_content` 字段）。

体验金有效期都是一个月，不能吃一辈子。

## KIMI

### API KEY

- [API KEY 管理页面](https://platform.moonshot.cn/console/api-keys)

### 优势

联网搜索很强，输出速度很快，擅长长文输入和总结。

体验金 15 元，有效期未知，据说一年。

### 劣势

也只有联网能打了，不联网就是傻子。

联网小贵，每次光调用费就要 0.03 元，还不算额外的 token 支出（每次在 7k tokens 左右）。

限流严重，不掏钱每分钟只能请求三次，也就是联网一次半。。

## QWEN

### API KEY

- [API KEY 管理页面](https://bailian.console.aliyun.com/?apiKey=1#/api-key)
- [API KEY 获取教程](https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key)

### 优势

通义千问是老牌开源模型，在 HuggingFace 上广受欢迎；Qwen2.5 是国内第一个和 DeepSeek-V3 达到一个水平的，我猜 QwQ 和 DeepSeek-R1 可能也是。

阿里云是算力大厂，全球前五，几乎没有服务器繁忙的可能。

有自己部署的第三方 DeepSeek。通义千问系列部分模型可以联网。

体验金爆炸，每个模型送 100w，大大小小一共 269 个模型……虽然我没做这么多支持。有效期 180 天。

### 劣势

小概率输出一半突然掉线（timeout）。通义系列比 DeepSeek 更快，盲猜是服务器给到位了。

## SIF

### API KEY

- [API KEY 管理页面](https://cloud.siliconflow.cn/account/ak)

### 优势

输出特别快！

模型也比较全面，见过的没见过的都有一些；上面的 DeepSeek-V3/R1、GLM-4、Qwen2.5、QwQ 等都有部署，但部分模型可能落后于官方。

体验金 14 元，没有有效期！

### 劣势

有时会出现服务连不上、回复短时间内掉速等情况。夜里比白天服务质量好。

模型全部不能联网。

## 生成效果对比

使用相同的提示词：如何界定依赖 AI 与合理运用 AI？

### deepseek-chat vs glm-4-flash vs kimi-latest vs qwen-max-latest

v1

当然这个对智谱有些不公平，没有用最好的旗舰打……但没办法，我没钱了，有钱再录一个。

视频没处理完，改天再放。

### deepseek-reasoner vs deepseek-r1 vs deepseek-ai/DeepSeek-R1

v2~v5

这个就是速度比拼了。

TL;DR：官方落后二十余秒，但和硅基流动几乎同时结束；之前阿里百炼快要慢死了，用时感觉像是另外两个的两倍多，现在也挺快。

视频没处理完，改天再放。

### deepseek-reasoner vs qwq-plus-latest

敬请期待
