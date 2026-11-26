"""Generate the Markdown-homepage images: hero.svg and models.svg.

Run:  python tools/build_svg.py
SVGs shown through <img> cannot run scripts, so all motion uses SMIL/CSS.
"""
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent
SANS = "'PingFang SC','Microsoft YaHei','Noto Sans SC','Hiragino Sans GB',sans-serif"
MONO = "Consolas,'JetBrains Mono',Menlo,'Courier New',monospace"
MOON, MOON2, VIOLET, CYAN, MUTED, TEXT, OK = "#f6dc9e", "#ffb86b", "#8b7cff", "#5fd4ff", "#8e97c4", "#e8ecff", "#5ee6a8"
N, DUR = 5, 15  # five models, 3s each


def text_w(s, cjk, ascii_):
    return sum(cjk if ord(c) > 0x2E80 else ascii_ for c in s)


def slot(i, on, off, attr):
    """Discrete animation: value `on` during slot i of N, else `off`."""
    a, b = i / N, (i + 1) / N
    if i == 0:
        kt, vals = f"0;{b}", f"{on};{off}"
    elif i == N - 1:
        kt, vals = f"0;{a}", f"{off};{on}"
    else:
        kt, vals = f"0;{a};{b}", f"{off};{on};{off}"
    return (f'<animate attributeName="{attr}" dur="{DUR}s" repeatCount="indefinite" '
            f'calcMode="discrete" keyTimes="{kt}" values="{vals}"/>')


def stars(w, h, n, seed):
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        r = rnd.choice([0.6, 0.8, 1, 1.2, 1.5])
        d = rnd.uniform(2.5, 6)
        lo = rnd.uniform(0.1, 0.35)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#e6ebff" opacity="{lo:.2f}">'
                   f'<animate attributeName="opacity" values="{lo:.2f};0.9;{lo:.2f}" dur="{d:.1f}s" '
                   f'begin="{rnd.uniform(0, 5):.1f}s" repeatCount="indefinite"/></circle>')
    return "\n".join(out)


DEFS = f"""<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05081a"/><stop offset=".5" stop-color="#090f2e"/><stop offset="1" stop-color="#05081a"/></linearGradient>
  <radialGradient id="glowV" cx=".12" cy=".3" r=".45"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".22"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
  <radialGradient id="glowM" cx=".85" cy=".1" r=".45"><stop offset="0" stop-color="{MOON}" stop-opacity=".2"/><stop offset="1" stop-color="{MOON}" stop-opacity="0"/></radialGradient>
  <radialGradient id="glowC" cx=".5" cy="1.05" r=".5"><stop offset="0" stop-color="{CYAN}" stop-opacity=".12"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
  <radialGradient id="moon" cx=".35" cy=".35" r=".75"><stop offset="0" stop-color="#fff6dc"/><stop offset=".4" stop-color="{MOON}"/><stop offset=".8" stop-color="#d9a85c"/><stop offset="1" stop-color="#a87635"/></radialGradient>
  <radialGradient id="halo"><stop offset=".45" stop-color="{MOON}" stop-opacity=".35"/><stop offset="1" stop-color="{MOON}" stop-opacity="0"/></radialGradient>
  <linearGradient id="title" x1="0" x2="1"><stop offset="0" stop-color="{MOON}"/><stop offset=".5" stop-color="{MOON2}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
  <linearGradient id="term" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#12183c" stop-opacity=".96"/><stop offset="1" stop-color="#090d24" stop-opacity=".98"/></linearGradient>
  <linearGradient id="meteor" x1="0" x2="1"><stop offset="0" stop-color="{MOON}" stop-opacity=".95"/><stop offset="1" stop-color="{MOON}" stop-opacity="0"/></linearGradient>
</defs>"""


def background(w, h, n_stars, seed):
    return f"""<clipPath id="clip"><rect width="{w}" height="{h}" rx="24"/></clipPath>
<g clip-path="url(#clip)">
<rect width="{w}" height="{h}" fill="url(#bg)"/>
<rect width="{w}" height="{h}" fill="url(#glowV)"/><rect width="{w}" height="{h}" fill="url(#glowM)"/><rect width="{w}" height="{h}" fill="url(#glowC)"/>
{stars(w, h, n_stars, seed)}"""


def hero():
    W, H = 1200, 560
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="MidnightMind API：夜深了，模型还醒着。">',
         DEFS, background(W, H, 110, 7)]
    # meteor
    p.append(f'''<g opacity="0"><rect x="0" y="0" width="170" height="1.6" fill="url(#meteor)" transform="rotate(152)"/>
<animateTransform attributeName="transform" type="translate" values="900,40;520,240" keyTimes="0;1" dur="1.1s" begin="2s;meteorEnd.end+6s" id="meteorRun" fill="freeze"/>
<animate attributeName="opacity" values="0;1;0" dur="1.1s" begin="meteorRun.begin" id="meteorEnd"/></g>''')
    # moon
    p.append(f'''<circle cx="1060" cy="95" r="170" fill="url(#halo)"/>
<circle cx="1060" cy="95" r="98" fill="url(#moon)"/>
<circle cx="1030" cy="70" r="17" fill="#96642a" opacity=".22"/><circle cx="1085" cy="128" r="11" fill="#96642a" opacity=".22"/><circle cx="1045" cy="140" r="8" fill="#96642a" opacity=".2"/>''')
    # badge
    badge = "OpenAI 协议兼容 · 改一行 base_url 即可切换"
    bw = text_w(badge, 13, 7.2) + 92
    p.append(f'''<rect x="70" y="86" width="{bw:.0f}" height="34" rx="17" fill="{MOON}" fill-opacity=".08" stroke="{MOON}" stroke-opacity=".3"/>
<rect x="76" y="92" width="46" height="22" rx="11" fill="{MOON}"/>
<text x="99" y="108" text-anchor="middle" font-family="{SANS}" font-size="12" font-weight="700" fill="#1a1206">NEW</text>
<text x="134" y="108" font-family="{SANS}" font-size="13" fill="{MOON}">{badge}</text>''')
    # headline + lead
    p.append(f'''<text x="68" y="205" font-family="{SANS}" font-size="66" font-weight="900" fill="{TEXT}" letter-spacing="-1">夜深了，</text>
<text x="68" y="290" font-family="{SANS}" font-size="66" font-weight="900" fill="url(#title)" letter-spacing="-1">模型还醒着。</text>
<text font-family="{SANS}" font-size="18" fill="{MUTED}">
  <tspan x="70" y="345">MidnightMind API 用<tspan fill="{TEXT}" font-weight="700">一个 Key</tspan> 聚合 DeepSeek、Kimi、</tspan>
  <tspan x="70" y="375">GLM、Qwen 等主流开源大模型。统一接口、智能路由、</tspan>
  <tspan x="70" y="405">按量计费，让你的应用在任何时刻都有最聪明的大脑在线。</tspan>
</text>''')
    x = 70
    for label in ["7×24 小时在线", "多上游自动容灾", "无月费 · 用多少付多少"]:
        p.append(f'<circle cx="{x + 4}" cy="461" r="4" fill="{OK}"><animate attributeName="opacity" values="1;.4;1" dur="2.4s" repeatCount="indefinite"/></circle>'
                 f'<text x="{x + 16}" y="466" font-family="{SANS}" font-size="14" fill="{MUTED}">{label}</text>')
        x += text_w(label, 14, 7.5) + 46
    # terminal
    tx, ty, tw, th = 650, 150, 490, 330
    p.append(f'''<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="18" fill="url(#term)" stroke="#aab9ff" stroke-opacity=".14"/>
<circle cx="{tx + 24}" cy="{ty + 24}" r="5.5" fill="#ff6b6b"/><circle cx="{tx + 42}" cy="{ty + 24}" r="5.5" fill="#ffcf5c"/><circle cx="{tx + 60}" cy="{ty + 24}" r="5.5" fill="#5ee6a8"/>
<text x="{tx + tw - 20}" y="{ty + 28}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{MUTED}">POST /v1/chat/completions</text>
<line x1="{tx}" y1="{ty + 48}" x2="{tx + tw}" y2="{ty + 48}" stroke="#aab9ff" stroke-opacity=".12"/>''')
    lx, ly, lh = tx + 22, ty + 82, 25
    code = [
        f'<tspan fill="{VIOLET}">curl</tspan> https://midnightmind.net/v1/chat/completions \\',
        f'  -H <tspan fill="{MOON}">"Authorization: Bearer $MM_API_KEY"</tspan> \\',
        f'  -d <tspan fill="{MOON}">\'{{</tspan>',
        None,
        f'<tspan fill="{MOON}">    "messages": [{{"role":"user","content":"午夜好"}}]</tspan>',
        f'<tspan fill="{MOON}">  }}\'</tspan>',
    ]
    models = ["deepseek-chat", "kimi-k2", "glm-4", "qwen3", "minimax-m1"]
    for k, line in enumerate(code):
        y = ly + k * lh
        if line is None:
            for i, m in enumerate(models):
                p.append(f'<text x="{lx}" y="{y}" xml:space="preserve" font-family="{MONO}" font-size="13.5" fill="{MOON}" opacity="0">'
                         f'    "model": "<tspan font-weight="700">{m}</tspan>",{slot(i, 1, 0, "opacity")}</text>')
        else:
            p.append(f'<text x="{lx}" y="{y}" xml:space="preserve" font-family="{MONO}" font-size="13.5" fill="#c9d0f5">{line}</text>')
    # reply box
    by = ty + 228
    p.append(f'<rect x="{tx + 20}" y="{by}" width="{tw - 40}" height="56" rx="10" fill="{CYAN}" fill-opacity=".05" stroke="{CYAN}" stroke-opacity=".28" stroke-dasharray="4 4"/>')
    replies = ["“午夜好！DeepSeek 正在为你值守。”", "“晚上好，Kimi 在线，想聊点什么？”", "“GLM 已就绪，随时帮你写代码。”",
               "“通义千问在此，今晚想探索什么？”", "“MiniMax 报到，长文档交给我。”"]
    for i, r in enumerate(replies):
        p.append(f'<text x="{tx + 36}" y="{by + 24}" font-family="{SANS}" font-size="14" fill="#a9e9ff" opacity="0">{r}{slot(i, 1, 0, "opacity")}</text>')
    p.append(f'<text x="{tx + 36}" y="{by + 44}" font-family="{MONO}" font-size="11.5" fill="{MUTED}">200 OK · stream · 智能路由已选择最优上游</text>')
    # chips
    cx, cy = tx + 20, ty + th - 22
    for i, name in enumerate(["DeepSeek", "Kimi", "GLM", "Qwen", "MiniMax"]):
        cw = len(name) * 7.4 + 24
        p.append(f'<rect x="{cx}" y="{cy - 17}" width="{cw:.0f}" height="26" rx="13" fill="{MOON}" fill-opacity="0" stroke="#aab9ff" stroke-opacity=".2">{slot(i, 1, 0, "fill-opacity")}</rect>'
                 f'<text x="{cx + cw / 2:.0f}" y="{cy}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTED}">{name}{slot(i, "#1a1206", MUTED, "fill")}</text>')
        cx += cw + 8
    p.append("</g></svg>")
    return "\n".join(p)


CARDS = [
    ("DS", ("#4d6bfe", "#2a3fbf"), "DeepSeek", "深度求索", ["V3 通用对话与 R1 深度推理，", "数学、代码与复杂逻辑表现出众。"], ["推理", "代码", "Function Call"]),
    ("K", ("#2a2a2a", "#4a4a4a"), "Kimi", "月之暗面", ["K2 系列 MoE 大模型，超长上下文，", "Agent 与工具调用能力强大。"], ["长上下文", "Agent", "工具调用"]),
    ("GLM", ("#3b5bdb", "#7048e8"), "GLM", "智谱", ["GLM-4 系列，中文理解扎实，", "编程与智能体任务表现优秀。"], ["中文", "编程", "多模态"]),
    ("Q", ("#615ced", "#8b5cf6"), "Qwen", "通义千问", ["Qwen3 全尺寸家族，从轻量到旗舰，", "混合思考模式随需切换。"], ["全尺寸", "思考模式", "Coder"]),
    ("M", ("#e8375a", "#f76b1c"), "MiniMax", "稀宇科技", ["高效长文本与 Agent 模型，适合", "大规模文档处理与多步任务编排。"], ["长文本", "高吞吐", "Agent"]),
]


def models():
    W, H, pad, gap = 1200, 540, 30, 20
    cw, ch = (W - 2 * pad - 2 * gap) / 3, (H - 2 * pad - gap) / 2
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="支持的模型：DeepSeek、Kimi、GLM、Qwen、MiniMax 等">',
         DEFS.replace("</defs>", "".join(
             f'<linearGradient id="lg{i}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c[1][0]}"/><stop offset="1" stop-color="{c[1][1]}"/></linearGradient>'
             for i, c in enumerate(CARDS)) + "</defs>"),
         background(W, H, 70, 11)]
    for idx in range(6):
        x = pad + (idx % 3) * (cw + gap)
        y = pad + (idx // 3) * (ch + gap)
        if idx == 5:
            p.append(f'''<rect x="{x:.0f}" y="{y:.0f}" width="{cw:.0f}" height="{ch:.0f}" rx="18" fill="#ffffff" fill-opacity=".03" stroke="{MOON}" stroke-opacity=".35" stroke-dasharray="6 6"/>
<text x="{x + 26:.0f}" y="{y + 82:.0f}" font-family="{SANS}" font-size="22" font-weight="700" fill="{TEXT}"><tspan fill="{MOON}">+</tspan> 更多模型持续上线</text>
<text font-family="{SANS}" font-size="14.5" fill="{MUTED}"><tspan x="{x + 26:.0f}" y="{y + 120:.0f}">豆包、阶跃星辰、混元、Llama 等更多模型，</tspan><tspan x="{x + 26:.0f}" y="{y + 144:.0f}">以及 Embedding / Rerank 接口。</tspan></text>
<text x="{x + 26:.0f}" y="{y + 190:.0f}" font-family="{MONO}" font-size="12" fill="{MOON}">✦ 新模型上线，第一时间接入</text>''')
            continue
        abbr, _, name, vendor, desc, tags = CARDS[idx]
        p.append(f'''<rect x="{x:.0f}" y="{y:.0f}" width="{cw:.0f}" height="{ch:.0f}" rx="18" fill="#ffffff" fill-opacity=".035" stroke="#aab9ff" stroke-opacity=".14"/>
<rect x="{x + 26:.0f}" y="{y + 26:.0f}" width="48" height="48" rx="13" fill="url(#lg{idx})"/>
<text x="{x + 50:.0f}" y="{y + 56:.0f}" text-anchor="middle" font-family="{SANS}" font-size="{16 if len(abbr) > 2 else 18}" font-weight="700" fill="#fff">{abbr}</text>
<text x="{x + 88:.0f}" y="{y + 46:.0f}" font-family="{SANS}" font-size="19" font-weight="700" fill="{TEXT}">{name}</text>
<text x="{x + 88:.0f}" y="{y + 68:.0f}" font-family="{SANS}" font-size="13" fill="{MUTED}">{vendor}</text>
<text font-family="{SANS}" font-size="14.5" fill="{MUTED}"><tspan x="{x + 26:.0f}" y="{y + 114:.0f}">{desc[0]}</tspan><tspan x="{x + 26:.0f}" y="{y + 138:.0f}">{desc[1]}</tspan></text>''')
        tx = x + 26
        for j, t in enumerate(tags):
            w = text_w(t, 12, 7) + 18
            col, bg = (MOON, MOON) if j == 0 else ("#bdb4ff", VIOLET)
            p.append(f'<rect x="{tx:.0f}" y="{y + 168:.0f}" width="{w:.0f}" height="24" rx="7" fill="{bg}" fill-opacity=".13"/>'
                     f'<text x="{tx + w / 2:.0f}" y="{y + 184:.0f}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{col}">{t}</text>')
            tx += w + 6
    p.append("</g></svg>")
    return "\n".join(p)


def panel(W, H, seed, label):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">',
            DEFS, background(W, H, int(W * H / 9000), seed)]


def head(x, y, eyebrow, title, sub=None, anchor="start"):
    out = [f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{MONO}" font-size="13" letter-spacing="2" fill="{MOON}">{eyebrow}</text>',
           f'<text x="{x}" y="{y + 48}" text-anchor="{anchor}" font-family="{SANS}" font-size="38" font-weight="900" fill="{TEXT}">{title}</text>']
    if sub:
        out.append(f'<text x="{x}" y="{y + 84}" text-anchor="{anchor}" font-family="{SANS}" font-size="16" fill="{MUTED}">{sub}</text>')
    return out


def card(x, y, w, h, hot=False):
    if hot:
        return (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="18" fill="{MOON}" fill-opacity=".07" stroke="{MOON}" stroke-opacity=".45"/>')
    return f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="18" fill="#ffffff" fill-opacity=".035" stroke="#aab9ff" stroke-opacity=".14"/>'


def lines(x, y, rows, size=14.5, fill=MUTED, step=24, family=SANS):
    t = "".join(f'<tspan x="{x:.0f}" y="{y + i * step:.0f}">{r}</tspan>' for i, r in enumerate(rows))
    return f'<text font-family="{family}" font-size="{size}" fill="{fill}">{t}</text>'


ICONS = {
    "route": '<path d="M4 12h4l3-8 2 16 3-8h4"/>',
    "code": '<path d="M8 9l-4 3 4 3M16 9l4 3-4 3M14 5l-4 14"/>',
    "coin": '<circle cx="12" cy="12" r="9"/><path d="M12 7v10M9 9.5c0-1 1.3-1.8 3-1.8s3 .8 3 1.8-1.3 1.7-3 2-3 1-3 2 1.3 1.8 3 1.8 3-.8 3-1.8"/>',
    "lock": '<rect x="4" y="10" width="16" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    "chart": '<path d="M3 20h18M6 16V9M11 16V5M16 16v-6M21 16v-3"/>',
}


def icon(x, y, name):
    return (f'<rect x="{x:.0f}" y="{y:.0f}" width="44" height="44" rx="12" fill="{VIOLET}" fill-opacity=".16" stroke="#aab9ff" stroke-opacity=".18"/>'
            f'<g transform="translate({x + 10:.0f},{y + 10:.0f})" fill="none" stroke="{MOON}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')


def features():
    W, H, pad, gap = 1200, 660, 30, 20
    p = panel(W, H, 21, "核心能力：智能路由与自动容灾、OpenAI 协议兼容、按量计费、安全与隐私、用量可视化")
    p += head(60, 72, "// WHY MIDNIGHTMIND", "为开发者的每一个深夜而生", "你只管写业务，模型切换、上游故障、账单对账这些琐事，交给我们在夜里默默处理。")
    ww = (W - 2 * pad - gap) / 2
    y1, h1 = 200, 240
    # wide card 1: routing
    x = pad
    p += [card(x, y1, ww, h1), icon(x + 28, y1 + 28, "route"),
          f'<text x="{x + 28}" y="{y1 + 102}" font-family="{SANS}" font-size="19" font-weight="700" fill="{TEXT}">智能路由与自动容灾</text>',
          lines(x + 28, y1 + 132, ["同一模型对接多个上游渠道，实时探测延迟与可用性，故障秒级切换。"])]
    for i, (name, pct, lat, d) in enumerate([("渠道 A", .92, "286ms", "3.2s"), ("渠道 B", .74, "341ms", "4.1s"), ("渠道 C", .38, "备用", "5s")]):
        by = y1 + 162 + i * 22
        bw = ww - 28 - 28 - 70 - 70
        p.append(f'<text x="{x + 28}" y="{by + 5}" font-family="{MONO}" font-size="12" fill="{MUTED}">{name}</text>'
                 f'<rect x="{x + 98}" y="{by - 3}" width="{bw:.0f}" height="7" rx="3.5" fill="#ffffff" fill-opacity=".07"/>'
                 f'<rect x="{x + 98}" y="{by - 3}" width="{bw * pct:.0f}" height="7" rx="3.5" fill="url(#title)">'
                 f'<animate attributeName="width" values="{bw * pct:.0f};{bw * pct * .86:.0f};{bw * pct:.0f}" dur="{d}" repeatCount="indefinite"/></rect>'
                 f'<text x="{x + ww - 28:.0f}" y="{by + 5}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{TEXT}">{lat}</text>')
    # wide card 2: compat
    x = pad + ww + gap
    p += [card(x, y1, ww, h1), icon(x + 28, y1 + 28, "code"),
          f'<text x="{x + 28:.0f}" y="{y1 + 102}" font-family="{SANS}" font-size="19" font-weight="700" fill="{TEXT}">100% OpenAI 协议兼容</text>',
          lines(x + 28, y1 + 132, ["支持 Chat Completions、流式输出、Function Calling、", "JSON Mode，主流工具开箱即用，只需替换 base_url。"])]
    tx = x + 28
    for t in ["LangChain", "Dify", "Cursor", "Cherry Studio", "OpenAI SDK"]:
        w = len(t) * 7.2 + 20
        p.append(f'<rect x="{tx:.0f}" y="{y1 + 178}" width="{w:.0f}" height="26" rx="8" fill="{VIOLET}" fill-opacity=".14"/>'
                 f'<text x="{tx + w / 2:.0f}" y="{y1 + 195}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#bdb4ff">{t}</text>')
        tx += w + 8
    # three small cards
    sw = (W - 2 * pad - 2 * gap) / 3
    y2, h2 = y1 + h1 + gap, 180
    for i, (ic, title, desc) in enumerate([
        ("coin", "按量计费，透明账单", ["按 Token 精确计费，无月费、", "无最低消费，每次调用可追溯。"]),
        ("lock", "安全与隐私", ["全链路 HTTPS 加密，不存储对话", "内容，支持多 Key 与额度限制。"]),
        ("chart", "用量可视化", ["控制台实时查看调用量、花费与", "延迟，团队成本一目了然。"]),
    ]):
        x = pad + i * (sw + gap)
        p += [card(x, y2, sw, h2), icon(x + 28, y2 + 26, ic),
              f'<text x="{x + 88:.0f}" y="{y2 + 55}" font-family="{SANS}" font-size="18" font-weight="700" fill="{TEXT}">{title}</text>',
              lines(x + 28, y2 + 110, desc)]
    p.append("</g></svg>")
    return "\n".join(p)


def quickstart():
    W, H = 1200, 560
    p = panel(W, H, 31, "三分钟接入：注册创建 API Key，把 base_url 改为 https://midnightmind.net/v1，修改 model 参数即可切换模型")
    p += head(60, 80, "// QUICK START", "三分钟，点亮你的第一盏灯")
    steps = [("注册并创建 API Key", "注册登录后，在「令牌」页面创建。"),
             ("替换 base_url", "指向 https://midnightmind.net/v1，原有代码无需改动。"),
             ("自由切换模型", "修改 model 参数，在 DeepSeek、Kimi、GLM 之间切换。")]
    for i, (t, d) in enumerate(steps):
        y = 200 + i * 100
        p.append(f'<circle cx="80" cy="{y + 12}" r="19" fill="none" stroke="{MOON}" stroke-opacity=".5"/>'
                 f'<text x="80" y="{y + 18}" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="700" fill="{MOON}">{i + 1}</text>'
                 f'<text x="116" y="{y + 10}" font-family="{SANS}" font-size="18" font-weight="700" fill="{TEXT}">{t}</text>'
                 f'<text x="116" y="{y + 38}" font-family="{SANS}" font-size="14.5" fill="{MUTED}">{d}</text>')
        if i < 2:
            p.append(f'<line x1="80" y1="{y + 36}" x2="80" y2="{y + 88}" stroke="{MOON}" stroke-opacity=".25" stroke-dasharray="3 4"/>')
    tx, ty, tw, th = 600, 60, 560, 440
    p.append(f'''<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="18" fill="url(#term)" stroke="#aab9ff" stroke-opacity=".14"/>
<circle cx="{tx + 24}" cy="{ty + 24}" r="5.5" fill="#ff6b6b"/><circle cx="{tx + 42}" cy="{ty + 24}" r="5.5" fill="#ffcf5c"/><circle cx="{tx + 60}" cy="{ty + 24}" r="5.5" fill="#5ee6a8"/>
<text x="{tx + 96}" y="{ty + 29}" font-family="{MONO}" font-size="13" fill="{MOON}">quickstart.py</text>
<line x1="{tx}" y1="{ty + 48}" x2="{tx + tw}" y2="{ty + 48}" stroke="#aab9ff" stroke-opacity=".12"/>''')
    k = lambda s: f'<tspan fill="{VIOLET}">{s}</tspan>'
    s = lambda s: f'<tspan fill="{MOON}">{s}</tspan>'
    c = lambda s: f'<tspan fill="#5d6696">{s}</tspan>'
    n = lambda s: f'<tspan fill="{CYAN}">{s}</tspan>'
    code = [
        f'{k("from")} openai {k("import")} OpenAI', "",
        "client = OpenAI(",
        f'    api_key={s(chr(34) + "sk-xxxxxxxx" + chr(34))},',
        f'    base_url={s(chr(34) + "https://midnightmind.net/v1" + chr(34))},',
        ")", "",
        "resp = client.chat.completions.create(",
        f'    model={s(chr(34) + "kimi-k2" + chr(34))},  {c("# 或 deepseek-chat / glm-4")}',
        f'    messages=[{{{s(chr(34) + "role" + chr(34))}: {s(chr(34) + "user" + chr(34))}, {s(chr(34) + "content" + chr(34))}: {s(chr(34) + "写一首关于午夜的诗" + chr(34))}}}],',
        f'    stream={n("True")},',
        ")",
        f'{k("for")} chunk {k("in")} resp:',
        f'    print(chunk.choices[{n("0")}].delta.content {k("or")} {s(chr(34) * 2)}, end={s(chr(34) * 2)})',
    ]
    for i, line in enumerate(code):
        if line:
            p.append(f'<text x="{tx + 24}" y="{ty + 86 + i * 24}" xml:space="preserve" font-family="{MONO}" font-size="13.5" fill="#c9d0f5">{line}</text>')
    # blinking cursor
    p.append(f'<rect x="{tx + 24}" y="{ty + 86 + 14 * 24 - 12}" width="8" height="15" fill="{MOON}"><animate attributeName="opacity" values="1;0;1" dur="1.1s" calcMode="discrete" repeatCount="indefinite"/></rect>')
    p.append("</g></svg>")
    return "\n".join(p)


def pricing():
    W, H, pad, gap = 1200, 560, 30, 20
    p = panel(W, H, 41, "计费方案：星光体验版、月光按量付费、银河企业版")
    p += head(W // 2, 72, "// PRICING", "像月光一样，温柔地计费", "所有方案均可调用全部模型，各模型实时单价以价格页面为准。", anchor="middle")
    cw = (W - 2 * pad - 2 * gap) / 3
    plans = [
        ("星光 · 体验版", "个人开发者与尝鲜用户", ("¥0", "起"), ["注册赠送体验额度", "全部模型可调用", "标准速率限制", "社区支持"]),
        ("月光 · 按量付费", "初创团队与生产应用", ("按 Token", "计费"), ["余额充值，随用随扣", "更高并发与速率", "智能路由 + 自动容灾", "用量明细与多 Key 管理"]),
        ("银河 · 企业版", "大规模调用与定制需求", ("定制", "报价"), ["阶梯折扣与专属价格", "专属通道与 SLA 保障", "对公转账与发票", "专属技术对接"]),
    ]
    y, h = 200, 320
    for i, (name, desc, (big, small), items) in enumerate(plans):
        x = pad + i * (cw + gap)
        hot = i == 1
        p.append(card(x, y, cw, h, hot))
        if hot:
            p.append(f'<rect x="{x + cw - 112:.0f}" y="{y - 13}" width="88" height="26" rx="13" fill="{MOON}"/>'
                     f'<text x="{x + cw - 68:.0f}" y="{y + 5}" text-anchor="middle" font-family="{SANS}" font-size="12.5" font-weight="700" fill="#1a1206">最受欢迎</text>')
        p.append(f'<text x="{x + 30:.0f}" y="{y + 48}" font-family="{SANS}" font-size="19" font-weight="700" fill="{MOON if hot else TEXT}">{name}</text>'
                 f'<text x="{x + 30:.0f}" y="{y + 74}" font-family="{SANS}" font-size="14" fill="{MUTED}">{desc}</text>'
                 f'<text x="{x + 30:.0f}" y="{y + 128}" font-family="{SANS}" font-size="36" font-weight="900" fill="{TEXT}">{big}<tspan font-size="14" font-weight="400" fill="{MUTED}" dx="8">{small}</tspan></text>'
                 f'<line x1="{x + 30:.0f}" y1="{y + 152}" x2="{x + cw - 30:.0f}" y2="{y + 152}" stroke="#aab9ff" stroke-opacity=".12"/>')
        for j, it in enumerate(items):
            iy = y + 186 + j * 30
            p.append(f'<text x="{x + 30:.0f}" y="{iy}" font-family="{SANS}" font-size="14.5" fill="#c9d0f5"><tspan fill="{OK}" font-weight="700">✓</tspan>  {it}</text>')
    p.append("</g></svg>")
    return "\n".join(p)


def faq():
    W, H, pad, gap = 1200, 720, 30, 20
    p = panel(W, H, 51, "常见问题与结语：当世界入睡，你的 AI 依然清醒")
    p += head(W // 2, 72, "// FAQ", "常见问题", anchor="middle")
    qa = [
        ("和直接调用官方接口有什么区别？", ["只需管理一个 Key、一份账单，就能调用多家厂商的模型；", "每个模型配置多个上游渠道，异常时自动切换，更稳定。"]),
        ("现有项目迁移需要改多少代码？", ["完全兼容 OpenAI 协议，通常只需修改 base_url 与", "api_key 两处配置，再把 model 换成想用的模型即可。"]),
        ("支持流式输出和函数调用吗？", ["支持。SSE 流式输出、Function Calling / Tools、", "JSON Mode 等能力随上游模型同步开放。"]),
        ("会保存我的对话数据吗？", ["不会。我们仅记录计费所需的 Token 用量与调用元信息，", "不存储请求与回复内容。"]),
    ]
    cw, ch = (W - 2 * pad - gap) / 2, 140
    for i, (q, a) in enumerate(qa):
        x = pad + (i % 2) * (cw + gap)
        y = 150 + (i // 2) * (ch + gap)
        p += [card(x, y, cw, ch),
              f'<text x="{x + 30:.0f}" y="{y + 44}" font-family="{SANS}" font-size="17" font-weight="700" fill="{TEXT}"><tspan fill="{MOON}" font-family="{MONO}">Q </tspan>{q}</text>',
              lines(x + 30, y + 82, a)]
    cy = 150 + 2 * (ch + gap) + 10
    p.append(f'''<radialGradient id="ctaGlow" cx=".5" cy="0" r=".7"><stop offset="0" stop-color="{MOON}" stop-opacity=".22"/><stop offset="1" stop-color="{MOON}" stop-opacity="0"/></radialGradient>
<rect x="{pad}" y="{cy}" width="{W - 2 * pad}" height="180" rx="24" fill="#141a46" fill-opacity=".8" stroke="{MOON}" stroke-opacity=".25"/>
<rect x="{pad}" y="{cy}" width="{W - 2 * pad}" height="180" rx="24" fill="url(#ctaGlow)"/>
<text x="{W // 2}" y="{cy + 40}" text-anchor="middle" font-family="{MONO}" font-size="13" letter-spacing="2" fill="{MOON}">// READY WHEN YOU ARE</text>
<text x="{W // 2}" y="{cy + 98}" text-anchor="middle" font-family="{SANS}" font-size="42" font-weight="900" fill="{TEXT}">当世界入睡，<tspan fill="url(#title)">你的 AI 依然清醒</tspan></text>
<text x="{W // 2}" y="{cy + 142}" text-anchor="middle" font-family="{SANS}" font-size="16" fill="{MUTED}">注册 MidnightMind API，用一个 Key 唤醒所有开源大模型。</text>
<text x="{W // 2}" y="{H - 22}" text-anchor="middle" font-family="{SANS}" font-size="13" fill="#5d6696">© 2026 MidnightMind API · Made for the night owls</text>''')
    p.append("</g></svg>")
    return "\n".join(p)


if __name__ == "__main__":
    for name, fn in [("hero", hero), ("models", models), ("features", features), ("quickstart", quickstart), ("pricing", pricing), ("faq", faq)]:
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
        print("wrote", f"{name}.svg")
