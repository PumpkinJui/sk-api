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
> - LEC：LeChat
> - FQWQ：Free QWQ
> - ARK：VolcanoArk，火山方舟
>
> 体验金数据主要为个人注册时获取到的，可能有所变动。

## TL;DR

个人优先 ARK、SIF、QWEN、GLM 吧。

DeepSeek 官方容易繁忙（不过最近逐渐也不这样了），Kimi 小贵不如用 APP（而且那个 k1.5 没有 API 接口），LeChat 是国外的可能不稳定，FQWQ 平台有点小而且只支持推理模型。

DS、SIF、QWEN、FQWQ、ARK、GLM 有推理模型（即深度思考）。换句话说，只有 KIMI 和 LEC 没有。

## DS

### API KEY

- [API KEY 控制台](https://platform.deepseek.com/api_keys)

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

- [API KEY 控制台](https://bigmodel.cn/usercenter/apikeys)

### 优势

能联网，另外有一些比较特别的模型，比如角色扮演和心理辅导。

`glm-4-flash` 和 `glm-z1-flash` 免费。

体验金爆炸，1600w air 专用 + 200w plus 专用 + 200w 所有按 token 计费的模型通用 + 400 次图片生成（这个程序用不上）。实名再送 500w 通用。「资源包」量大又便宜。

### 劣势

质量不过硬，我是相对 `DeepSeek-V3` 和通义千问系列说的。时不时该联网不联网，搜到的数据也是稍旧的。

体验金有效期都是一个月，不能吃一辈子。

## KIMI

### API KEY

- [API KEY 控制台](https://platform.moonshot.cn/console/api-keys)

### 优势

联网搜索很强，输出速度很快，擅长长文输入和总结。

体验金 15 元，有效期未知，据说一年。

### 劣势

也只有联网能打了，不联网就是傻子。

联网小贵，每次光调用费就要 0.03 元，还不算额外的 token 支出（每次在 7k tokens 左右）。

限流严重，不掏钱每分钟只能请求三次，也就是联网回复一次半。。

## QWEN

### API KEY

- [API KEY 控制台](https://bailian.console.aliyun.com/?apiKey=1#/api-key)
- [API KEY 获取教程](https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key)

### 优势

通义千问是老牌开源模型，在 HuggingFace 上广受欢迎；Qwen2.5 是国内第一个和 DeepSeek-V3 达到一个水平的，我猜 QwQ 和 DeepSeek-R1 可能也是。

阿里云是算力大厂，全球前五，几乎没有服务器繁忙的可能。

有自己部署的第三方 DeepSeek。通义千问系列部分模型可以联网。

体验金爆炸，每个模型送 100w，大大小小一共 269 个模型……虽然我没做这么多支持。有效期 180 天。

### 劣势

小概率输出时突然卡住一段时间。通义系列比 DeepSeek 更快，盲猜是服务器给到位了。

## SIF

### API KEY

- [注册邀请码](https://cloud.siliconflow.cn/i/gwe5E9hK)
- [API KEY 控制台](https://cloud.siliconflow.cn/account/ak)

### 优势

输出特别快！

模型也比较全面，见过的没见过的都有一些；上面的 DeepSeek-V3/R1、GLM-4、Qwen2.5、QwQ 等都有部署，但部分模型可能落后于官方。

体验金 14 元，没有有效期！

### 劣势

有时会出现回复短时间内掉速。模型全部不能联网。

## LEC

### API KEY

- [API KEY 控制台](https://console.mistral.ai/api-keys)

### 优势

国外的服务商（可能也只有它一家还给国内提供服务了罢），而且输出极快。

所有模型都可以无限期免费体验（有较为严格的限速，不过只要不是多线程一般碰不到）。

### 劣势

毕竟是国外的，连接速度略慢；不能联网。

## FQWQ

- [灵感来源](https://www.ruanyifeng.com/blog/2025/03/weekly-issue-341.html)
- [自荐文章](https://sspai.com/post/97081)

### API KEY

- [注册邀请码](https://api.suanli.cn/register?aff=Iphv)
- [API KEY 控制台](https://api.suanli.cn/token)

### 优势

免费模型居多，输出速度也比较快。

体验金 $2，暂未看到有效期。

### 劣势

模型太少了，只有推理模型（R1 和 QwQ）……

另外平台小，有点怕它倒了。

## ARK

### API KEY

- [API KEY 控制台](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey?apikey=%7B%7D)

### 优势

输出又稳又快，毕竟字节也是算力大厂了。

体验金接近爆炸：虽然每个模型只送 50w，但有三年的有效期，只要模型不开通就不算有效期。除此以外，还有一个[协作奖励计划](https://www.volcengine.com/docs/82379/1391869)，几乎是用多少送多少……

### 劣势

平台特别复杂：账号的 Access Key、方舟的 API Key、IAM 账户、模型开通、接入点……尤其是很多能在一页上展示的东西非要分成 10 条 / 页，使人做着都烦。

平台对手机端尤其不友好：有一个巨大的侧边栏，需要开桌面模式才能正常用；几乎所有页面都是新窗口打开，而且优化还挺烂，多开几个页面就非常卡。

实名认证后才能获取 API Key，未满 18 周岁不允许实名验证。*幸好我刚好满 18 了。*

联网的组件和不联网的，用的不是一个 API 接口，所以没法做联网。另外模型相对于百炼和硅基的来看，算是偏少的。

## 生成效果对比

下次一定。

可以参考文章：[喧嚣之后，2 月份谁是 R1/V3 供应商的王者](https://mp.weixin.qq.com/s/59TW4SfZ5VMH1aVJVYnM9A)，但信息可能过时。
