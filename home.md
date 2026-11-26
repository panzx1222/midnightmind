![MidnightMind API：夜深了，模型还醒着。](https://panzx1222.github.io/midnightmind/hero.svg?v=1)

> 🌙 **一个 Key，唤醒所有开源大模型。** MidnightMind API 聚合 DeepSeek、Kimi、GLM、Qwen、MiniMax 等主流模型，100% 兼容 OpenAI 协议，按量计费，7×24 小时在线。

## ✦ 模型广场：一个入口，汇聚整片星空

![支持的模型：DeepSeek、Kimi、GLM、Qwen、MiniMax 等](https://panzx1222.github.io/midnightmind/models.svg?v=1)

## ✦ 为开发者的每一个深夜而生

| | 核心能力 | 说明 |
| :---: | --- | --- |
| 🛰️ | **智能路由与自动容灾** | 同一模型对接多个上游渠道，实时探测延迟与可用性，故障秒级切换，请求不掉线 |
| 🔌 | **100% OpenAI 协议兼容** | 支持流式输出、Function Calling、JSON Mode，LangChain、Dify、Cursor、Cherry Studio 等工具开箱即用 |
| 🌕 | **按量计费，透明账单** | 按 Token 精确计费，无月费、无最低消费，每一次调用都可追溯 |
| 🔒 | **安全与隐私** | 全链路 HTTPS 加密，不存储对话内容，支持多 Key 管理与额度限制 |
| 📊 | **用量可视化** | 控制台实时查看各模型调用量、花费与延迟，团队成本一目了然 |

## ✦ 三分钟，点亮你的第一盏灯

1. **注册并登录**，在「令牌」页面创建 API Key
2. **替换 base_url** 为 `https://midnightmind.net/v1`，原有代码无需改动
3. **修改 `model` 参数**，在 DeepSeek、Kimi、GLM 之间随心切换

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-xxxxxxxx",
    base_url="https://midnightmind.net/v1",
)

resp = client.chat.completions.create(
    model="kimi-k2",  # 或 deepseek-chat / glm-4
    messages=[{"role": "user", "content": "写一首关于午夜的诗"}],
    stream=True,
)
for chunk in resp:
    print(chunk.choices[0].delta.content or "", end="")
```

```bash
curl https://midnightmind.net/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-xxxxxxxx" \
  -d '{"model": "deepseek-chat", "messages": [{"role": "user", "content": "午夜好"}]}'
```

## ✦ 像月光一样，温柔地计费

| 方案 | 适合谁 | 包含内容 |
| --- | --- | --- |
| ⭐ **星光 · 体验** | 个人开发者与尝鲜用户 | 注册赠送体验额度 · 全部模型可调用 · 标准速率 |
| 🌙 **月光 · 按量付费** | 初创团队与生产应用 | 余额充值随用随扣 · 更高并发 · 智能路由与容灾 · 多 Key 管理 |
| 🌌 **银河 · 企业** | 大规模调用与定制需求 | 阶梯折扣 · 专属通道与 SLA · 对公转账与发票 |

各模型的实时单价请查看顶部导航中的价格页面。

## ✦ 常见问题

**Q：和直接调用官方接口有什么区别？**

A：你只需管理一个 Key、一份账单，就能调用多家厂商的模型；每个模型都配置了多个上游渠道，单一渠道异常时会自动切换，稳定性更高。

**Q：现有项目迁移需要改多少代码？**

A：完全兼容 OpenAI 协议，通常只需修改 `base_url` 与 `api_key` 两处配置，再把 `model` 换成想用的模型即可。

**Q：支持流式输出和函数调用吗？**

A：支持。SSE 流式输出、Function Calling / Tools、JSON Mode 等能力随上游模型同步开放。

**Q：会保存我的对话数据吗？**

A：不会。我们仅记录计费所需的 Token 用量与调用元信息，不存储请求与回复内容。

---

🌙 **当世界入睡，你的 AI 依然清醒。** · © 2026 MidnightMind API
