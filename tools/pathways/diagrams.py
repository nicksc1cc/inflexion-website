"""SVG diagrams for the Inflexion pathways page. All colours come from CSS tokens."""
from html import escape as _e


def esc(s):
    return _e(str(s), quote=True)


def tw(text, size=8, k=0.62):
    return int(len(text) * size * k) + 12


def defs(p):
    m = ""
    for name, cls in [("a", "mk-a"), ("acc", "mk-acc"), ("dat", "mk-dat"), ("soft", "mk-soft")]:
        m += (f'<marker id="{p}-{name}" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">'
              f'<polygon points="0 0, 8 3, 0 6" class="{cls}"/></marker>')
    return f"<defs>{m}</defs>"


def svg_open(slug, w, h, title, desc, minw=None):
    mw = minw or min(w, 720)
    return (f'<svg class="dg" viewBox="0 0 {w} {h}" style="min-width:{mw}px" role="img" '
            f'aria-labelledby="{slug}-t {slug}-d"><title id="{slug}-t">{esc(title)}</title>'
            f'<desc id="{slug}-d">{esc(desc)}</desc>{defs(slug)}'
            f'<rect class="g-bg" width="{w}" height="{h}"/>')


def label(cx, y, text, side="above", xv=None):
    w = tw(text)
    if side == "above":
        x, yy = cx - w / 2, y - 18
        tx = cx
    else:
        x, yy = xv + 8, y - 6
        tx = x + w / 2
    return (f'<rect class="g-mask" x="{x}" y="{yy}" width="{w}" height="12" rx="2"/>'
            f'<text class="g-lab" x="{tx}" y="{yy + 9}">{esc(text)}</text>')


def node(x, y, w, h, name, sub=None, kind="std", tag=None):
    cx, cy = x + w / 2, y + h / 2
    o = f'<rect class="n n-{kind}" x="{x}" y="{y}" width="{w}" height="{h}" rx="3"/>'
    if tag:
        t = tw(tag, 7, 0.7) - 2
        o += (f'<rect class="n-tag" x="{x + 8}" y="{y + 7}" width="{t}" height="12" rx="2"/>'
              f'<text class="n-tagt{" on-dark" if kind == "dark" else ""}" x="{x + 8 + t / 2}" y="{y + 16}">{esc(tag)}</text>')
        cy += 6
    if sub:
        cy -= 6
    o += f'<text class="n-name n-name-{kind}" x="{cx}" y="{cy + 4}">{esc(name)}</text>'
    if sub:
        o += f'<text class="n-sub n-sub-{kind}" x="{cx}" y="{cy + 20}">{esc(sub)}</text>'
    return o


def zone(x, y, w, h, text):
    lw = tw(text, 7, 0.68)
    return (f'<rect class="z" x="{x}" y="{y}" width="{w}" height="{h}" rx="4"/>'
            f'<rect class="g-mask" x="{x + 12}" y="{y - 6}" width="{lw}" height="12" rx="2"/>'
            f'<text class="z-lab" x="{x + 12 + lw / 2}" y="{y + 3}">{esc(text)}</text>')


def legend(y, items, w):
    o = f'<line class="g-rule" x1="24" y1="{y - 10}" x2="{w - 24}" y2="{y - 10}"/>'
    o += f'<text class="lg-h" x="24" y="{y + 11}">KEY</text>'
    x = 72
    for kind, text in items:
        if kind in ("std", "focal", "agent", "ext", "dark"):
            o += f'<rect class="n n-{kind}" x="{x}" y="{y}" width="20" height="14" rx="2"/>'
        elif kind == "flow":
            o += f'<line class="f" x1="{x}" y1="{y + 7}" x2="{x + 20}" y2="{y + 7}"/>'
        elif kind == "dash":
            o += f'<line class="f-dash" x1="{x}" y1="{y + 7}" x2="{x + 20}" y2="{y + 7}"/>'
        elif kind in ("bar-a", "bar-b", "bar-f"):
            o += f'<rect class="{kind}" x="{x}" y="{y}" width="20" height="14" rx="2"/>'
        o += f'<text class="lg-t" x="{x + 28}" y="{y + 11}">{esc(text)}</text>'
        x += 28 + int(len(text) * 9 * 0.58) + 28
    return o


# 1. Operating model -------------------------------------------------------
def operating_model():
    s, W, H = "om", 960, 600
    A, AC, DT, SF = (f"url(#{s}-a)", f"url(#{s}-acc)", f"url(#{s}-dat)", f"url(#{s}-soft)")
    o = svg_open(s, W, H, "How the seven roles work together",
                 "A client pod led by a Growth Partner sets targets with a Decision Scientist, briefs a shared build studio, "
                 "and runs what is built through an Agentic Systems Designer whose agents are guided by specialists. Practices supply standards and training.")
    o += zone(196, 72, 476, 360, "CLIENT POD · 3 TO 5 PEOPLE WITH AGENTS")
    o += zone(704, 72, 232, 236, "BUILD STUDIO · SHARED")
    # flows
    o += f'<line class="f f-acc" x1="164" y1="128" x2="219" y2="128" marker-end="{AC}"/>' + label(192, 128, "OUTCOME")
    o += f'<line class="f" x1="400" y1="128" x2="459" y2="128" marker-end="{A}"/>' + label(430, 128, "TARGETS")
    o += f'<line class="f" x1="640" y1="128" x2="723" y2="128" marker-end="{A}"/>' + label(682, 128, "BRIEF")
    o += f'<line class="f f-dat" x1="820" y1="158" x2="820" y2="215" marker-end="{DT}"/>' + label(0, 188, "BUILDS WITH", "right", 820)
    o += f'<line class="f" x1="724" y1="248" x2="641" y2="248" marker-end="{A}"/>' + label(682, 248, "SHIPS")
    o += f'<line class="f" x1="550" y1="278" x2="550" y2="341" marker-end="{A}"/>' + label(0, 312, "RUNS", "right", 550)
    o += f'<path class="f" d="M310 278 V362 Q310 370 318 370 H459" marker-end="{A}"/>' + label(385, 370, "GUIDES")
    o += f'<path class="f" d="M550 98 V44 Q550 36 542 36 H102 Q94 36 94 44 V97" marker-end="{A}"/>' + label(322, 36, "RESULTS")
    o += f'<line class="f-dash" x1="310" y1="468" x2="310" y2="279" marker-end="{SF}"/>' + label(0, 446, "STANDARDS", "right", 310)
    o += f'<line class="f-dash" x1="820" y1="468" x2="820" y2="279" marker-end="{SF}"/>' + label(0, 446, "TRAINING", "right", 820)
    # nodes
    o += node(24, 98, 140, 60, "Client", "brand and growth goal", "ext", "CLIENT")
    o += node(220, 98, 180, 60, "Growth Partner", "owns the outcome", "focal", "LEAD")
    o += node(460, 98, 180, 60, "Decision Scientist", "targets and measurement", "std", "DATA")
    o += node(220, 218, 180, 60, "Specialists", "visibility · commerce · creative", "std", "CRAFT")
    o += node(460, 218, 180, 60, "Systems Designer", "runs agent workflows", "std", "OPS")
    o += node(460, 342, 180, 56, "Agents", "do the execution", "agent", "AI")
    o += node(724, 98, 192, 60, "Builders", "forward deployed", "std", "BUILD")
    o += node(724, 218, 192, 60, "Engineering partner", "platform and security", "ext", "PARTNER")
    o += node(196, 468, 740, 56, "Practices", "Growth · Visibility · Commerce · Creative · Data · Build   /   standards, training, reusable IP", "dark")
    o += legend(560, [("focal", "Accountable lead"), ("std", "Person"), ("agent", "AI agents"), ("ext", "Client or partner"),
                      ("flow", "Work"), ("dash", "Standards and training")], W)
    return o + "</svg>"


# 2. Delivery loop ----------------------------------------------------------
def loop():
    s, W, H = "lp", 1040, 660
    A, SF = f"url(#{s}-a)", f"url(#{s}-soft)"
    o = svg_open(s, W, H, "The delivery loop",
                 "Six steps run clockwise: Frame, Define, Build, Run, Shape and Prove. Every pass leaves reusable agents and playbooks in practice IP at the centre.")
    for d in ["M600 103.726 A240 240 0 0 1 704.969 177.073", "M743.285 242 A240 240 0 0 1 743.722 416.882",
              "M705.731 482 A240 240 0 0 1 601.130 555.871", "M440 556.274 A240 240 0 0 1 335.031 482.927",
              "M296.715 418 A240 240 0 0 1 296.278 243.118", "M334.269 178 A240 240 0 0 1 438.870 104.129"]:
        o += f'<path class="f" d="{d}" marker-end="{A}"/>'
    for d in ["M520 122 V270", "M672 242 L616 274", "M672 418 L616 386", "M520 538 V390", "M368 418 L424 386", "M368 242 L424 274"]:
        o += f'<path class="f-dash" d="{d}" marker-end="{SF}"/>'
    o += label(560, 206, "BRIEFS") + label(476, 470, "RUNBOOKS")
    st = [(440, 58, "1  Frame", "growth partner", "std"), (648, 178, "2  Define", "decision scientist", "std"),
          (648, 418, "3  Build", "builder with engineering", "focal"), (440, 538, "4  Run", "systems designer and agents", "std"),
          (232, 418, "5  Shape", "specialists", "std"), (232, 178, "6  Measure", "decision scientist", "std")]
    for x, y, n, sub, k in st:
        o += node(x, y, 160, 64, n, sub, k)
    o += node(420, 278, 200, 104, "Practice IP", "agents · playbooks · data", "dark")
    return o + "</svg>"


# 3. Skills matrix ----------------------------------------------------------
ROLES7 = ["Growth Partner", "AI Visibility Lead", "Agentic Systems Designer", "Forward Deployed Builder",
          "Decision Scientist", "Creative Systems Director", "Agentic Commerce Lead"]
MATRIX = [
    ("Shared foundation", [
        ("AI fluency", [3] * 7), ("Data literacy", [3] * 7), ("Commercial thinking", [3] * 7), ("Governance and AI risk", [3] * 7)]),
    ("Role specific", [
        ("Client leadership and outcome selling", [2, 1, 0, 0, 1, 0, 1]),
        ("AI search and citation", [0, 2, 0, 0, 0, 1, 1]),
        ("Workflow and agent design", [0, 0, 2, 1, 0, 1, 1]),
        ("Code, APIs and evals", [0, 0, 1, 2, 1, 0, 0]),
        ("Evaluating agent output", [0, 1, 2, 2, 0, 1, 0]),
        ("Experimentation and measurement", [1, 1, 1, 0, 2, 0, 1]),
        ("Synthetic audience testing", [1, 0, 0, 0, 2, 1, 0]),
        ("Generative creative craft", [0, 1, 0, 0, 0, 2, 0]),
        ("Product data and retail media", [0, 1, 0, 0, 0, 0, 2]),
    ]),
]


def skills_matrix():
    s, W = "sk", 960
    LX, CW, RH, TOP = 250, 96, 32, 92
    rows = sum(len(g[1]) for g in MATRIX)
    H = TOP + rows * RH + len(MATRIX) * 30 + 70
    o = svg_open(s, W, H, "Skills map for the seven roles",
                 "Four skills are shared by every role. Nine role specific skills show where each pathway goes deep and where roles overlap.")
    for i, r in enumerate(ROLES7):
        cx = LX + i * CW + CW / 2
        a, b = r.rsplit(" ", 1) if r.count(" ") else (r, "")
        if r == "Agentic Systems Designer":
            a, b = "Agentic Systems", "Designer"
        if r == "Forward Deployed Builder":
            a, b = "Forward Deployed", "Builder"
        if r == "Creative Systems Director":
            a, b = "Creative Systems", "Director"
        if r == "Agentic Commerce Lead":
            a, b = "Agentic Commerce", "Lead"
        o += f'<text class="mx-h" x="{cx}" y="{TOP - 40}">{esc(a)}</text><text class="mx-h" x="{cx}" y="{TOP - 26}">{esc(b)}</text>'
    y = TOP
    for gname, items in MATRIX:
        o += f'<text class="mx-g" x="24" y="{y + 4}">{esc(gname.upper())}</text>'
        o += f'<line class="g-rule-strong" x1="24" y1="{y + 12}" x2="{W - 24}" y2="{y + 12}"/>'
        y += 30
        for name, vals in items:
            cy = y + RH / 2
            o += f'<text class="mx-r" x="24" y="{cy + 4}">{esc(name)}</text>'
            o += f'<line class="g-rule" x1="24" y1="{y + RH}" x2="{W - 24}" y2="{y + RH}"/>'
            for i, v in enumerate(vals):
                cx = LX + i * CW + CW / 2
                if v == 3:
                    o += f'<rect class="mx-found" x="{cx - 7}" y="{cy - 7}" width="14" height="14" rx="2"/>'
                elif v == 2:
                    o += f'<circle class="mx-core" cx="{cx}" cy="{cy}" r="7"/>'
                elif v == 1:
                    o += f'<circle class="mx-sup" cx="{cx}" cy="{cy}" r="6"/>'
                else:
                    o += f'<circle class="mx-none" cx="{cx}" cy="{cy}" r="1.6"/>'
            y += RH
        y += 6
    ly = y + 26
    o += f'<text class="lg-h" x="24" y="{ly + 11}">KEY</text>'
    o += f'<rect class="mx-found" x="72" y="{ly}" width="14" height="14" rx="2"/><text class="lg-t" x="94" y="{ly + 11}">Everyone, months 0 to 4</text>'
    o += f'<circle class="mx-core" cx="279" cy="{ly + 7}" r="7"/><text class="lg-t" x="294" y="{ly + 11}">Core to the role</text>'
    o += f'<circle class="mx-sup" cx="429" cy="{ly + 7}" r="6"/><text class="lg-t" x="444" y="{ly + 11}">Supporting</text>'
    return o + "</svg>"


# 4. Pod variants -----------------------------------------------------------
def pod(slug, title, members, agents, lead="Growth Partner"):
    W, H = 340, 300
    A = f"url(#{slug}-a)"
    o = svg_open(slug, W, H, title, f"{lead} leads {', '.join(members)}. Agents handle {agents}.", minw=280)
    o += node(100, 12, 140, 44, lead, None, "focal")
    o += f'<line class="f" x1="170" y1="56" x2="170" y2="79" marker-end="{A}"/>'
    o += zone(8, 86, 324, 116, "POD")
    pos = [(16, 98), (172, 98), (16, 148), (172, 148)]
    for (x, y), m in zip(pos, members):
        o += node(x, y, 152, 42, m, None, "ext" if m == "Engineering partner" else "std")
    o += f'<line class="f" x1="170" y1="202" x2="170" y2="221" marker-end="{A}"/>'
    o += f'<rect class="n n-agent" x="8" y="222" width="324" height="58" rx="3"/>'
    o += f'<text class="n-tagt" x="36" y="240">AGENTS</text>'
    words, line, lines = agents.split(), "", []
    for w in words:
        if len(line + " " + w) > 50:
            lines.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    lines.append(line)
    for i, l in enumerate(lines[:2]):
        o += f'<text class="n-sub n-sub-std" x="170" y="{258 + i * 14}">{esc(l)}</text>'
    return o + "</svg>"


PODS = [
    ("pa", "Retail and marketplace brand", ["Agentic Commerce Lead", "AI Visibility Lead", "Decision Scientist", "Systems Designer"],
     "feeds, listings, retail media bids and weekly reporting"),
    ("pb", "Content led consumer brand", ["Creative Systems Director", "AI Visibility Lead", "Decision Scientist", "Systems Designer"],
     "on brand variants, social publishing and synthetic audience tests"),
    ("pc", "Build led transformation", ["Forward Deployed Builder", "Systems Designer", "Decision Scientist", "Engineering partner"],
     "the client's own workflows as they move into production"),
]


def pods():
    return [(t, pod(sl, t, m, a)) for sl, t, m, a in PODS]


# 5. Gantt ------------------------------------------------------------------
PATHS = [
    ("Growth Partner", "from account, client services, planning", "CXL Growth Marketing", "Lead a pod, agree work paid on results", False, 70),
    ("AI Visibility Lead", "from SEO, PR, content", "HubSpot AEO · CXL AI Search", "Raise how often AI recommends the brand", False, 60),
    ("Agentic Systems Designer", "from paid media, social, operations", "Python · Agentic AI · MCP", "Replace a workflow with agents", False, 70),
    ("Forward Deployed Builder", "from developers, technical analysts", "Claude API · GenAI for Devs · AWS", "Put a system into production", True, 80),
    ("Decision Scientist", "from analysts, insight, data", "Python · CXL CRO · Meridian", "Run a mix model and an incrementality test", False, 90),
    ("Creative Systems Director", "from creative, design, copy, video", "Adobe Firefly specialisation", "Brand system producing at scale", False, 40),
    ("Agentic Commerce Lead", "from marketplaces, retail, ecommerce", "Amazon Ads certs · CXL Ecommerce", "Grow sales through AI assistants", False, 70),
]


def gantt():
    s, W, H = "gt", 1120, 600
    X0, P = 228, 32
    xm = lambda m: X0 + m * P
    o = svg_open(s, W, H, "The 24 month training plan",
                 "Everyone completes a four month foundation. Each pathway then spends months four to twelve on courses and pairing, passes a readiness test, and spends months twelve to twenty four doing the role on live work.")
    for m in [0, 4, 8, 12, 16, 20, 24]:
        o += f'<text class="ax" x="{xm(m)}" y="58">M{m}</text>'
    o += f'<line class="g-rule-strong" x1="24" y1="66" x2="{W - 24}" y2="66"/>'
    o += f'<text class="ax" x="1060" y="58">COURSE HRS</text>'
    o += zone(16, 84, W - 32, 60, "FOUNDATION · EVERYONE")
    o += zone(16, 162, W - 32, 360, "PATHWAYS · MONTHS 4 TO 24")
    o += f'<line class="gate" x1="{xm(12)}" y1="72" x2="{xm(12)}" y2="526"/>'
    o += label(xm(12) + 56, 44, "READINESS TEST")
    y = 92
    o += f'<text class="rw-n" x="32" y="{y + 22}">Foundation</text><text class="rw-s" x="32" y="{y + 36}">all roles</text>'
    o += f'<rect class="bar-a" x="{xm(0)}" y="{y + 12}" width="{4 * P - 4}" height="24" rx="2"/>'
    o += f'<text class="br-t" x="{xm(0) + 8}" y="{y + 28}">AI fluency and data</text><text class="hrs" x="1060" y="{y + 28}">≈30</text>'
    y = 176
    for name, sub, a, b, focal, hrs in PATHS:
        o += f'<text class="rw-n{" is-acc" if focal else ""}" x="32" y="{y + 22}">{esc(name)}</text>'
        o += f'<text class="rw-s" x="32" y="{y + 36}">{esc(sub)}</text>'
        o += f'<rect class="{"bar-f" if focal else "bar-a"}" x="{xm(4)}" y="{y + 12}" width="{8 * P - 4}" height="24" rx="2"/>'
        o += f'<text class="br-t" x="{xm(4) + 8}" y="{y + 28}">{esc(a)}</text>'
        o += f'<rect class="{"bar-fb" if focal else "bar-b"}" x="{xm(12) + 4}" y="{y + 12}" width="{12 * P - 4}" height="24" rx="2"/>'
        o += f'<text class="br-t" x="{xm(12) + 12}" y="{y + 28}">{esc(b)}</text>'
        o += f'<text class="hrs" x="1060" y="{y + 28}">≈{hrs}</text>'
        y += 48
    o += legend(556, [("bar-a", "Courses and pairing"), ("bar-b", "Live client work"), ("bar-f", "Builder, the hardest role to hire")], W)
    return o + "</svg>"


# 6. Feeder bars ------------------------------------------------------------
def feeders(rows):
    """rows: list of (target title, best fit %, best source title) sorted desc."""
    s, W = "fd", 960
    L, R0, R1 = 268, 280, 640
    RH, TOP = 26, 54
    H = TOP + len(rows) * RH + 40
    xs = lambda v: R0 + (R1 - R0) * v / 100
    o = svg_open(s, W, H, "Best current feeder for each AI era role",
                 "For each of the 24 AI era roles, the strongest direct match from the 62 current roles. Most sit between 45 and 80 percent; only one clears 90.")
    o += f'<text class="ax-l" x="{L}" y="30" text-anchor="end">AI ERA ROLE</text>'
    o += f'<text class="ax-l" x="{R1 + 24}" y="30">STRONGEST CURRENT ROLE</text>'
    for v in [0, 25, 50, 75, 100]:
        o += f'<line class="{"g-50" if v == 50 else "g-grid"}" x1="{xs(v)}" y1="{TOP - 8}" x2="{xs(v)}" y2="{H - 30}"/>'
        o += f'<text class="ax" x="{xs(v)}" y="{H - 14}">{v}%</text>'
    y = TOP
    for t, f, src in rows:
        cy = y + RH / 2
        o += f'<text class="fd-n" x="{L}" y="{cy + 4}">{esc(t)}</text>'
        o += f'<rect class="{"fd-bar" if f >= 50 else "fd-bar lo"}" x="{R0}" y="{cy - 6}" width="{xs(f) - R0}" height="12" rx="1"/>'
        o += f'<text class="fd-v" x="{xs(f) + 6}" y="{cy + 4}">{f}</text>'
        o += f'<text class="fd-s" x="{R1 + 24}" y="{cy + 4}">{esc(src)}</text>'
        y += RH
    return o + "</svg>"


# 7. Discipline strip -------------------------------------------------------
def strip(groups):
    """groups: list of (discipline, [(fit, title), ...])"""
    s, W = "st", 960
    L, R0, R1 = 150, 170, 930
    RH, TOP = 64, 56
    H = TOP + len(groups) * RH + 40
    xs = lambda v: R0 + (R1 - R0) * (v - 30) / 70
    o = svg_open(s, W, H, "Readiness for an AI era role by discipline",
                 "Each dot is one current role, placed at its best direct match to any AI era role. Ticks mark the median for each discipline.")
    o += f'<text class="ax-l" x="{R0}" y="18">EACH DOT: ONE CURRENT ROLE AT ITS BEST AI ERA MATCH</text>'
    for v in [30, 40, 50, 60, 70, 80, 90, 100]:
        o += f'<line class="{"g-50" if v == 50 else "g-grid"}" x1="{xs(v)}" y1="{TOP - 6}" x2="{xs(v)}" y2="{H - 30}"/>'
        o += f'<text class="ax" x="{xs(v)}" y="{H - 14}">{v}%</text>'
    y = TOP
    for name, pts in groups:
        cy = y + RH / 2
        o += f'<text class="fd-n" x="{L}" y="{cy + 4}">{esc(name)}</text>'
        o += f'<text class="rw-s" x="{L}" y="{cy + 18}" text-anchor="end">{len(pts)} roles</text>'
        o += f'<line class="g-rule" x1="{R0}" y1="{y + RH}" x2="{R1}" y2="{y + RH}"/>'
        seen = {}
        for f, t in sorted(pts):
            k = round(f)
            n = seen.get(k, 0)
            seen[k] = n + 1
            off = [0, -9, 9, -18, 18][n % 5]
            o += f'<circle class="st-d" cx="{xs(f)}" cy="{cy + off}" r="5"><title>{esc(t)}: {f}%</title></circle>'
        vals = sorted(f for f, _ in pts)
        med = vals[len(vals) // 2] if len(vals) % 2 else (vals[len(vals) // 2 - 1] + vals[len(vals) // 2]) / 2
        o += f'<line class="st-m" x1="{xs(med)}" y1="{cy - 22}" x2="{xs(med)}" y2="{cy + 22}"/>'
        o += f'<text class="fd-v" x="{xs(med)}" y="{cy - 26}" text-anchor="middle">median {round(med)}</text>'
        y += RH
    return o + "</svg>"


# 8. Scoring flow -----------------------------------------------------------
def scoring():
    s, W, H = "sc", 960, 360
    A, AC, SF = f"url(#{s}-a)", f"url(#{s}-acc)", f"url(#{s}-soft)"
    o = svg_open(s, W, H, "How a person is scored",
                 "Five kinds of evidence feed a skill profile, weighted by how reliable each is. The profile is matched against 61 roles at three seniorities to produce ranked routes, and placement outcomes feed back into the weights.")
    ev = [("Tests", "HIGH"), ("Work samples", "HIGH"), ("AI interview", "MEDIUM"), ("CV analysis", "MEDIUM"), ("Self rating", "LOW")]
    ys = [40 + i * 60 for i in range(5)]
    for (n, wgt), y in zip(ev, ys):
        cy = y + 22
        o += f'<line class="f" x1="214" y1="{cy}" x2="262" y2="{cy}"/>'
    o += f'<line class="f" x1="262" y1="{ys[0] + 22}" x2="262" y2="{ys[-1] + 22}"/>'
    o += f'<line class="f" x1="262" y1="182" x2="309" y2="182" marker-end="{A}"/>'
    for (n, wgt), y in zip(ev, ys):
        o += node(24, y, 190, 44, n, None, "std", wgt)
    o += node(310, 146, 180, 72, "Skill profile", "86 skills · level and confidence", "std", "PROFILE")
    o += f'<line class="f" x1="490" y1="182" x2="539" y2="182" marker-end="{A}"/>' + label(514, 182, "MATCH")
    o += node(540, 146, 180, 72, "Every role", "61 roles × 3 seniorities", "std", "COMPARE")
    o += f'<line class="f f-acc" x1="720" y1="182" x2="769" y2="182" marker-end="{AC}"/>'
    o += node(770, 146, 166, 72, "Ranked routes", "gaps, modules, time", "focal", "OUTPUT")
    o += f'<path class="f-dash" d="M853 218 V318 Q853 326 845 326 H638 Q630 326 630 318 V219" marker-end="{SF}"/>'
    o += label(742, 326, "PLACEMENT OUTCOMES RECALIBRATE")
    o += f'<text class="n-sub n-sub-std" x="400" y="252">Where sources disagree,</text>'
    o += f'<text class="n-sub n-sub-std" x="400" y="266">confidence drops instead of averaging</text>'
    return o + "</svg>"


# 9. Who does what across three relationship models -------------------------
REL_MODELS = [("Brand runs,", "agency builds"), ("Agency runs a", "managed service"), ("Hybrid", "")]
REL_ROWS = [
    ("Commercial goals and targets", ["B", "B", "B"]),
    ("Strategy and prioritisation", ["B", "S", "S"]),
    ("Brand and customer knowledge", ["B", "B", "B"]),
    ("Customer data", ["B", "B", "B"]),
    ("Building agents and tools", ["A", "A", "A"]),
    ("Running agents day to day", ["B", "A", "S"]),
    ("Media execution", ["P", "P", "P"]),
    ("Checking the quality of agent output", ["B", "A", "S"]),
    ("Measuring results", ["B", "A", "A"]),
    ("Specialist depth such as AEO and commerce", ["A", "A", "A"]),
    ("Agents built on the brand's data", ["B", "N", "N"]),
    ("Reusable methods and tooling", ["A", "A", "A"]),
]
REL_KEY = {"B": ("Brand", "ch-b"), "A": ("Agency", "ch-a"), "P": ("Platform", "ch-p"), "S": ("Shared", "ch-s"), "N": ("Negotiated", "ch-n")}


def relationship_matrix():
    s, W = "rl", 960
    LX, CX0, CW, RH, TOP = 24, 360, 196, 36, 86
    H = TOP + len(REL_ROWS) * RH + 70
    o = svg_open(s, W, H, "Who leads each activity in three client and agency models",
                 "Twelve marketing activities and which party typically leads each one when the brand runs its own agents, when an agency runs a managed service, and in a hybrid of the two.")
    for i, (a, b) in enumerate(REL_MODELS):
        cx = CX0 + i * CW + CW / 2
        o += f'<text class="mx-h" x="{cx}" y="{TOP - 40}">{esc(a)}</text>'
        if b:
            o += f'<text class="mx-h" x="{cx}" y="{TOP - 25}">{esc(b)}</text>'
    o += f'<line class="g-rule-strong" x1="{LX}" y1="{TOP - 10}" x2="{W - 24}" y2="{TOP - 10}"/>'
    y = TOP
    for name, vals in REL_ROWS:
        cy = y + RH / 2
        o += f'<text class="mx-r" x="{LX}" y="{cy + 4}">{esc(name)}</text>'
        o += f'<line class="g-rule" x1="{LX}" y1="{y + RH}" x2="{W - 24}" y2="{y + RH}"/>'
        for i, v in enumerate(vals):
            cx = CX0 + i * CW + CW / 2
            lab, cls = REL_KEY[v]
            o += f'<rect class="ch {cls}" x="{cx - 52}" y="{cy - 10}" width="104" height="20" rx="10"/>'
            o += f'<text class="ch-t {cls}-t" x="{cx}" y="{cy + 4}">{esc(lab)}</text>'
        y += RH
    ly = y + 26
    o += f'<text class="lg-h" x="{LX}" y="{ly + 11}">KEY</text>'
    x = 72
    for k in ["B", "A", "P", "S", "N"]:
        lab, cls = REL_KEY[k]
        o += f'<rect class="ch {cls}" x="{x}" y="{ly}" width="28" height="14" rx="7"/>'
        txt = {"S": "Shared lead", "N": "Ownership set by contract"}.get(k, f"{lab} leads")
        o += f'<text class="lg-t" x="{x + 36}" y="{ly + 11}">{esc(txt)}</text>'
        x += 36 + int(len(txt) * 9 * 0.58) + 30
    return o + "</svg>"
