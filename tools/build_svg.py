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


if __name__ == "__main__":
    (OUT / "hero.svg").write_text(hero(), encoding="utf-8")
    (OUT / "models.svg").write_text(models(), encoding="utf-8")
    print("wrote hero.svg, models.svg")
