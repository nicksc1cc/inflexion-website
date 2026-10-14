import json, base64, os, statistics, sys
sys.path.insert(0, os.path.dirname(__file__))
import diagrams as dg
from diagrams import esc

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(f"{HERE}/s1/_compiled.json"))
F = json.load(open(f"{HERE}/fit.json"))
LOGO = os.environ.get("INFLEXION_LOGO", f"{HERE}/assets/inflexion-media-logo-white.png")

SK = {s["id"]: s["name"] for s in D["skills"]}
SRC = {r["id"]: r for r in D["sources"]}
TGT = {t["id"]: t for t in D["targets"]}

# ---- data for charts and explorer ------------------------------------------
ai_targets = [t for t in D["targets"] if t["category"] == "ai_era"]
feeder_rows = []
for t in ai_targets:
    best = max(((dict((x[1], x[0]) for x in F["res"][r])[t["id"]], r) for r in SRC), key=lambda z: z[0])
    feeder_rows.append((t["titles"]["mid"], best[0], SRC[best[1]]["titles"]["mid"]))
feeder_rows.sort(key=lambda r: -r[1])

DISC = [("brand", "Brand"), ("marketing", "Marketing"), ("advertising", "Advertising"), ("creative", "Creative")]
strip_groups = []
best_ai_by_src = {}
for key, lab in DISC:
    pts = []
    for r in D["sources"]:
        if r["discipline"] != key:
            continue
        ai = [x for x in F["res"][r["id"]] if TGT[x[1]]["category"] == "ai_era"]
        b = max(ai, key=lambda x: x[0])
        best_ai_by_src[r["id"]] = b
        pts.append((b[0], r["titles"]["mid"]))
    strip_groups.append((lab, pts))
all_best = [v[0] for v in best_ai_by_src.values()]
two_step_wins = sum(1 for v in F["tw"].values() if v[1])
two_step_total = len(F["tw"])

EX = {"s": [], "t": {}, "k": SK}
for t in D["targets"]:
    EX["t"][t["id"]] = [t["titles"]["mid"], t["category"], t["demand_outlook"], t["description"],
                        t["titles"]["junior"], t["titles"]["senior"]]
for key, lab in DISC:
    for r in D["sources"]:
        if r["discipline"] != key:
            continue
        top = [[f, tid, g] for f, tid, g in F["res"][r["id"]][:10]]
        b = best_ai_by_src[r["id"]]
        tw = F["tw"][f'{r["id"]}|{b[1]}']
        EX["s"].append([r["id"], r["titles"]["mid"], lab, r["ai_displacement_risk"], r["summary"], top,
                        [b[0], b[1], b[2], tw[1]]])

# ---- content -------------------------------------------------------------------
SEVEN = [
    ("Account, client services, planning", "Growth Partner",
     "Leads the relationship with the business or client, owns the commercial result and decides what the team works on.",
     "AI Marketing Strategist, Growth Manager",
     "A piece of work sold and measured on growth"),
    ("SEO, PR, content", "AI Visibility Lead",
     "Makes sure AI assistants describe and recommend the brand accurately, using content, data and earned media.",
     "Answer Engine Optimisation Specialist",
     "A measured improvement in how AI assistants describe the brand"),
    ("Paid media, social, marketing operations", "Agentic Systems Designer",
     "Designs, runs and checks the AI agents that now carry out media, social and reporting work.",
     "Agent Workflow Designer, Agent Operations Manager",
     "A live agent workflow with quality measures"),
    ("Developers, technical analysts", "Forward Deployed Builder",
     "An engineer who works inside a marketing team and builds the tools and agents it needs.",
     "AI Solutions Consultant, Creative Technologist",
     "A system in production that is still running"),
    ("Analysts, insight, data science", "Decision Scientist",
     "Sets targets, designs tests and measures what worked, so spend follows evidence.",
     "Marketing Scientist, Synthetic Research Analyst",
     "A decision changed by evidence, with the result tracked"),
    ("Creative, design, copy, video", "Creative Systems Director",
     "Builds the brand rules and tools that let AI produce creative at volume, and protects its quality.",
     "AI Content Operations Manager, Generative Content Producer",
     "A brand system that outperforms the old process"),
    ("Marketplaces, retail media, ecommerce", "Agentic Commerce Lead",
     "Prepares product data and retail media so AI shopping assistants find and choose the brand's products.",
     "Ecommerce Manager, Social Commerce Manager",
     "Sales growth through AI shopping assistants"),
]

LADDER = [
    ("Growth Partner", ["Growth Associate", "Growth Partner", "Partner, Client Growth"]),
    ("AI Visibility Lead", ["AI Visibility Specialist", "AI Visibility Lead", "Head of AI Visibility"]),
    ("Agentic Systems Designer", ["Agent Workflow Specialist", "Agentic Systems Designer", "Head of Agentic Systems"]),
    ("Forward Deployed Builder", ["Associate Builder", "Forward Deployed Builder", "Head of Build"]),
    ("Decision Scientist", ["Decision Analyst", "Decision Scientist", "Head of Decision Science"]),
    ("Creative Systems Director", ["Creative Systems Producer", "Creative Systems Lead", "Creative Systems Director"]),
    ("Agentic Commerce Lead", ["Agentic Commerce Specialist", "Agentic Commerce Lead", "Head of Agentic Commerce"]),
]
RUNGS = [("Senior", "Owns results across several teams and develops the discipline"),
         ("Mid", "Owns a workflow or a business area from start to finish"),
         ("Junior", "Runs agents and checks their output on one account")]

FOUNDATION = ["Google AI Essentials, about 8 hours, free", "Anthropic Academy: Claude 101 and AI Fluency, free",
              "AI for Everyone (Andrew Ng), about 6 hours", "CXL Intro to CRO and Experimentation, about 1 hour",
              "Internal workshops on data literacy, commercial thinking and the EU AI Act, about 8 hours",
              "Automate one part of their own job and show it to colleagues"]
DETAIL = [
    ("Growth Partner", "from account, client services, planning", 70, 270,
     ["CXL Growth Marketing Minidegree, 40+ hours of video over about 3 months",
      "BCG agent native marketing operating model, read and discussed as a team",
      "Internal workshops on outcome pricing, scoping AI builds and leading a pod, about 12 hours"],
     "Lead one pod and agree one piece of work paid on results"),
    ("AI Visibility Lead", "from SEO, PR, content", 60, 280,
     ["HubSpot AEO Fundamentals, free certification", "CXL Optimize Pages for AI Search",
      "Reforge Mastering Search and AI Optimization", "iPullRank AI Search Manual as reference",
      "Optional: Advanced GEO and AI Optimisation, one day in London"],
     "Improve how often AI assistants recommend the brand and report it monthly"),
    ("Agentic Systems Designer", "from paid media, social, marketing operations", 70, 270,
     ["AI Python for Beginners, about 2 weeks at 10 hours a week", "Anthropic Academy: Introduction to MCP and Agent Skills",
      "Agentic AI (Andrew Ng), about 10 hours across 5 modules", "Hugging Face Agents Course, free"],
     "Replace one manual media or social workflow with a monitored agent"),
    ("Forward Deployed Builder", "from developers, technical analysts", 80, 260,
     ["Anthropic Academy: Building with the Claude API, 8+ hours", "Generative AI for Developers, about 30 hours over 6 to 10 weeks",
      "Agentic AI (Andrew Ng), about 10 hours", "AWS Certified AI Practitioner, 7 hour preparation path and exam"],
     "Work with an engineering partner to put one system into production"),
    ("Decision Scientist", "from analysts, insight, data science", 90, 250,
     ["AI Python for Beginners, about 20 hours", "CXL Conversion Optimization Minidegree, 20 courses",
      "Google Meridian, Google's open source marketing mix model, through its documentation",
      "Internal workshop on building and validating synthetic audiences, about 10 hours"],
     "Run one marketing mix model and one incrementality test"),
    ("Creative Systems Director", "from creative, design, copy, video", 40, 300,
     ["Create and Enhance Visuals with AI (Adobe Firefly), 6 courses of 3 to 4 hours",
      "Generative AI for Content Production, about 2 hours", "AI Fluency, shared with the foundation"],
     "Build a brand system that produces variants at scale and test them with synthetic audiences"),
    ("Agentic Commerce Lead", "from marketplaces, retail media, ecommerce", 70, 270,
     ["Amazon Ads certifications, free and renewed every 13 months", "CXL Ecommerce Marketing Minidegree, 36 hours of video",
      "Anthropic Academy: Introduction to MCP"],
     "Prepare one product range for AI shopping assistants and track the sales that follow"),
]

QUESTIONS = [
    "Which parts of the marketing work are now done by platform automation, or soon could be, and what are the people who did that work doing instead?",
    "What will the marketing team look like in 2028, and who is accountable for getting it there?",
    "How many current staff could move into the new roles, and what happens for those who cannot?",
    "How much agency spend still pays for execution the agency is now automating, and do the contracts reflect that?",
    "Who in the team can direct AI agents today, and who checks the quality of what those agents produce?",
    "Which activities should stay in house, and who owns the agents and tools an agency builds on the brand's data?",
    "Which commercial results will the redesigned team be measured on?",
]

SOURCES = [
    ("WEF, Future of Jobs Report 2025", "https://www.weforum.org/publications/the-future-of-jobs-report-2025/digest/"),
    ("BCG, the agent native marketing operating model, 2026", "https://www.bcg.com/publications/2026/agent-native-marketing-operating-model"),
    ("IPA Agency Census 2025, via Prolific North", "https://www.prolificnorth.co.uk/?p=137330"),
    ("HR Katha, WPP to cut 1,000 more jobs, September 2026", "https://www.hrkatha.com/news/wpp-to-cut-1000-more-jobs-as-ai-reshapes-global-advertising/"),
    ("PPC Land, Google AI Max upgrade from 1 September 2026", "https://ppc.land/google-ads-ai-max-auto-upgrade-lands-september-1-will-ads-all-look-alike/"),
    ("Relevant Audience, Amazon Ads Agent and Full-Funnel Campaigns", "https://www.relevantaudience.com/ecommerce-marketing/amazon-ads-agent-unboxed-2026-full-funnel-dva-plus/"),
    ("Google AI Essentials", "https://career.skills.google/course_templates/1224"),
    ("Agentic AI course details", "https://www.beri.net/learning/dlai-agentic-ai"),
    ("AI Python for Beginners", "https://www.coursera.org/learn/ai-python-for-beginners"),
    ("AWS AI Practitioner path", "https://www.codecademy.com/ext-paths/aif-c01-aws-certified-ai-practitioner"),
    ("Google Meridian", "https://www.research-live.com/article/news/google-opens-marketing-mix-model-to-all-users/id/5135693"),
    ("Adobe Firefly specialisation", "https://www.coursera.org/specializations/create-and-enhance-visuals-with-ai"),
    ("Amazon Ads certifications", "https://titannetwork.com/amazon-ads-certification-guide/"),
    ("CXL Ecommerce Minidegree", "https://www.reliablesoft.net/tools/cxl-ecommerce-marketing"),
    ("AEO training courses", "https://www.rankability.com/blog/best-aeo-training-courses/"),
]

CSS = open(f"{HERE}/page.css").read()
JS = open(f"{HERE}/page.js").read()
MED = round(statistics.median(all_best))
TITLE = "The marketing team is being redesigned around AI agents"


def section(num, sid, eyebrow, h2, p, body, alt=False):
    return (f'<section class="sec{" alt" if alt else ""}" id="{sid}"><div class="w">'
            f'<div class="sec-head rv"><div class="eyebrow"><b>{num}</b> / {eyebrow}</div><h2>{h2}</h2>'
            f'{f"<p>{p}</p>" if p else ""}</div>{body}</div></section>')


def essay(*paras):
    return '<div class="essay rv">' + "".join(f"<p>{p}</p>" for p in paras) + "</div>"


def figure(svg, cap=None):
    return (f'<figure class="fig rv"><div class="scroll">{svg}</div>'
            f'{f"<figcaption>{cap}</figcaption>" if cap else ""}</figure>')


SHIFT = [
    ("Pricing", "Hours, FTEs and rate cards", "Fees linked to results, a running fee for agent systems and fixed prices for builds"),
    ("Agency team shape", "A pyramid of junior staff billed under a few seniors", "Small senior pods directing AI agents"),
    ("Execution", "Run by the agency on the brand's behalf", "Run inside platforms and by agents, overseen by whichever side owns them"),
    ("Contract", "Agency of record retainers lasting several years", "A smaller core retainer plus short paid projects"),
    ("Procurement", "Scopes headcount and benchmarks day rates", "Scopes outputs and results, often through a paid pilot"),
    ("Measurement", "Often reported by the agency running the work", "Increasingly separated from whoever runs the work"),
]
SIDES = [
    ("Brand side", [
        ("Marketing director", "Owns the commercial result and the design of the team. Less time goes on managing channels and agencies and more on deciding where money and people go."),
        ("Growth lead", "The in house counterpart of the Growth Partner, setting priorities across pods and holding agencies to agreed results."),
        ("Decision Scientist", "Owns targets and the measurement framework, so results can be judged independently of whoever runs the work."),
        ("Agentic Systems Designer", "Runs the agents behind always on channels where the brand wants direct control."),
        ("Creative Systems lead", "Owns the brand rules and protects quality when creative is produced at volume."),
    ]),
    ("Agency side", [
        ("Growth Partner", "Leads the agency's work for the brand and is accountable for the results it was hired to deliver."),
        ("Forward Deployed Builders", "Build agents and tools inside the brand's team, then hand them over or run them under a separate fee."),
        ("AI Visibility Lead", "Brings depth in how AI assistants select and describe brands, which few brands can justify hiring for."),
        ("Agentic Commerce Lead", "Brings retail media and product data expertise across marketplaces and AI shopping assistants."),
        ("Decision Scientist", "Provides independent measurement where the brand does not hold that capability itself."),
    ]),
]
MODELS = [
    ("Brand runs, agency builds",
     "The brand employs the growth, decision science and systems design roles and runs its own agents. Agencies supply Builders and specialists on defined projects.",
     "Brands with large and steady spend, several markets on one platform stack and the ability to hire scarce technical people.",
     "Hiring is slow and expensive, capability can leave with a few people, and the brand carries the full burden of quality control."),
    ("Agency runs a managed service",
     "The agency runs pods and agents for the brand under a fee linked to results or a subscription. The brand sets targets and keeps its customer knowledge and data.",
     "Brands with lean marketing teams, many channels or markets, or no wish to build technical capability of their own.",
     "Dependence on one agency, an agency measuring its own results, and tools that are hard to move if the relationship ends."),
    ("Hybrid",
     "The brand runs its always on channels in house. The agency builds the tools, runs specialist areas and peak periods, and may provide independent measurement.",
     "Brands moving from a traditional agency model that want control of core channels without hiring every specialism.",
     "Accountability can blur at the points where work passes between the two sides unless ownership of each activity and each tool is written down."),
]


def relationship_html():
    shift = "".join(f'<tr><td>{esc(a)}</td><td>{esc(b)}</td><td class="em-col">{esc(c)}</td></tr>' for a, b, c in SHIFT)
    sides = '<div class="sides rv">' + "".join(
        f'<div><h4>{esc(side)}</h4><dl>' + "".join(f'<div><dt>{esc(n)}</dt><dd>{esc(d)}</dd></div>' for n, d in rows) + "</dl></div>"
        for side, rows in SIDES) + "</div>"
    models = '<div class="models rv">' + "".join(
        f'<article><div class="cap">Model {i + 1}</div><h4>{esc(n)}</h4><p><b>How it works</b>{esc(h)}</p><p><b>Suits</b>{esc(s)}</p><p><b>Risks</b>{esc(r)}</p></article>'
        for i, (n, h, s, r) in enumerate(MODELS)) + "</div>"
    out = essay(
        "Most agency contracts still price work by time. A retainer funds a team of named people, a rate card sets what each grade costs, and procurement benchmarks those rates against other agencies. That works while the work scales with people. Once agents and platform automation carry much of the execution, the hours behind a campaign fall sharply while the value of the decisions around it stays the same, and a price based on time no longer describes what the client is buying.",
        "Three forms of pricing are likely to replace it, often in the same contract. Strategy and measurement are bought as a smaller retainer for senior judgement. Agents and tools are bought as builds, with a separate fee if the agency also runs them. Specialist work is bought as short projects with defined results, which also gives procurement something more useful to compare than day rates.")
    out += f'<div class="tbl rv" style="margin-top:32px"><div class="scroll"><table><thead><tr><th>Area</th><th>Traditional model</th><th>Emerging model</th></tr></thead><tbody>{shift}</tbody></table></div></div>'
    out += '<h3 class="sub-h rv">Who leads each activity</h3>'
    out += essay("How work divides depends on how much capability a brand wants to own. The matrix shows who typically leads twelve activities under three models. Goals, customer knowledge and customer data stay with the brand in every model, and media execution sits with the platforms in all three. The differences are in the middle, in who runs the agents, who checks their output and who measures the results.")
    out += '<div style="margin-top:24px"></div>' + figure(dg.relationship_matrix())
    out += '<h3 class="sub-h rv">Roles on each side</h3>'
    out += essay("Some of the seven roles tend to sit inside the brand and others with an agency. The split below reflects the hybrid model, where the division is least obvious. The marketing director's job changes most, moving from managing channels and suppliers towards deciding how the team is designed and where its money goes.")
    out += '<div style="margin-top:24px"></div>' + sides
    out += '<h3 class="sub-h rv">Three likely models</h3>'
    out += essay("None of the three suits every brand. Each fits different conditions and carries different risks, and many brands will use more than one across markets or channels.")
    out += '<div style="margin-top:24px"></div>' + models
    out += '<h3 class="sub-h rv">Where the tensions are</h3>'
    out += essay(
        "The agency pyramid is under the most pressure. Holding company margins have long depended on billing many junior staff under a few senior ones, and agents now do much of the junior work. WPP expects most of its £500 million savings to come from people costs. The same change removes the traditional training ground for future senior staff, so agencies will need other ways to develop people, such as the two year route set out in the appendix.",
        "Ownership of what gets built is the least settled question. An agent trained on a brand's data and refined over a year of its campaigns is valuable to both sides. Agencies want to reuse the method for other clients, and brands want to keep what their data and budget paid for. Few contracts separate the two today. Terms covering who owns the reusable method, who owns agents and outputs specific to the client, and what can be reused for competitors are likely to become standard.",
        "The platforms are now suppliers and competitors at once. Google and Amazon sell automated execution directly to brands and report on its performance themselves, and independent tests reported by PPC Land have already questioned how AI Max performs, particularly in campaigns with limited budgets. Judging spend across platforms and measuring results independently are areas where neither the platform nor the agency running the work is well placed to assess itself.")
    return out


UNKNOWNS = [
    "Platform automation may not perform as well as its adoption suggests. Independent testing of tools such as AI Max is still limited, and brands with small budgets or specialist products may find that manual control still pays. If that holds, more execution work stays with people than this analysis assumes.",
    "Brands may move more slowly than agencies. Much of their execution work already sits outside their payroll, budgets are set annually, and few have redesigned a marketing function around AI agents before. The two year route assumes a decision to start, which many organisations have not yet made.",
    "The seven roles are a reading of today's tools. Agent reliability, regulation such as the EU AI Act and attitudes to AI generated work could each move tasks back to people or remove roles kept here. The skill match scores compare role profiles rather than assessed individuals, so any real team will vary around them.",
]


def page(logo_src):
    seven = "".join(
        f'<tr><td>{esc(a)}</td><td class="to">{esc(b)}<small>Related: {esc(rel)}</small></td><td>{esc(what)}</td><td>{esc(ready)}</td></tr>'
        for a, b, what, rel, ready in SEVEN)
    ladder = '<div class="ladder rv"><div class="scroll"><div class="lgrid">'
    ladder += '<div class="lh"></div>' + "".join(f'<div class="lh">{esc(r)}</div>' for r, _ in LADDER)
    for i, (rung, scope) in enumerate(RUNGS):
        ladder += f'<div class="lr"><b>{rung}</b><span>{esc(scope)}</span></div>'
        for _, titles in LADDER:
            ladder += f'<div class="lc{" mid" if i == 1 else ""}">{esc(titles[2 - i])}</div>'
    ladder += '</div></div></div>'
    pods = '<div class="pods rv">' + "".join(
        f'<figure class="pod"><figcaption><span class="cap">Pod {i + 1}</span><b>{esc(t)}</b></figcaption><div class="scroll">{svg}</div></figure>'
        for i, (t, svg) in enumerate(dg.pods())) + "</div>"
    cards = '<div class="cards rv"><article class="card found"><div class="cap">Months 0 to 4 · everyone · about 30 hours</div><h3>Shared foundation</h3><ul>' + "".join(
        f"<li>{esc(x)}</li>" for x in FOUNDATION) + "</ul></article>"
    for name, frm, ch, lh, courses, ready in DETAIL:
        cards += (f'<article class="card"><div class="cap">{esc(frm)}</div><h3>{esc(name)}</h3>'
                  f'<div class="hrsrow"><span><b>≈{ch}</b> course hours</span><span><b>≈{lh}</b> hours on live work</span></div>'
                  f'<ul>{"".join(f"<li>{esc(c)}</li>" for c in courses)}</ul>'
                  f'<p class="proof"><span class="cap">Readiness test at month 12</span>{esc(ready)}</p></article>')
    cards += "</div>"
    qs = '<ol class="qs rv">' + "".join(f"<li>{esc(q)}</li>" for q in QUESTIONS) + "</ol>"
    srcs = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(n)}</a></li>' for n, u in SOURCES)
    roles_table = f'''<div class="tbl rv"><div class="scroll"><table><thead><tr><th>Draws from</th><th>Role</th><th>What the job involves</th><th>Delivered before taking the title</th></tr></thead><tbody>{seven}</tbody></table></div></div>'''
    explore_html = '''<div class="ex rv">
  <div class="ex-top"><label for="exSel" class="cap">Current role</label><select id="exSel"></select><p id="exSum" class="ex-sum"></p></div>
  <div class="ex-grid"><div id="exBest" class="ex-best"></div><div id="exList" class="ex-list"></div></div>
</div>'''

    body = f'''
<div class="hero">
  <canvas id="field" aria-hidden="true"></canvas>
  <div class="w">
    <div class="top">
      <a href="https://nicksc1cc.github.io/inflexion-website/" target="_blank" rel="noopener" aria-label="Inflexion Media"><img src="{logo_src}" alt="Inflexion Media"></a>
      <nav aria-label="Sections"><a href="#change">The change</a><a href="#roles">Seven roles</a><a href="#relationship">Client and agency</a><a href="#people">Skills gap</a><a href="#appendix">Appendix</a></nav>
    </div>
    <div class="hero-body hero-in">
      <div class="sup">Inflexion Intelligence &middot; Perspective &middot; October 2026</div>
      <h1>The marketing team is being redesigned <em>around AI agents.</em></h1>
      <p class="desc">Google and Amazon now automate much of the media work that marketing budgets used to pay people to do, and the largest agencies have cut thousands of roles in response. The same shift is changing the roles inside marketing teams and the relationship between brands and their agencies. Marketing teams are likely to be rebuilt around seven roles, with work divided differently between brands, agencies and platforms. Scored against those roles, most of today's 62 marketing roles are about halfway there.</p>
      <div class="banner">
        <div><b>39%</b><span>of workers' existing skills expected to be transformed or outdated by 2030</span><small>WEF, Future of Jobs 2025</small></div>
        <div><b>14.3%</b><span>fall in headcount at UK creative agencies in the year to September 2025</span><small>IPA Agency Census</small></div>
        <div><b>60%</b><span>fewer resources needed by small campaign teams working with AI agents</span><small>BCG, 2026</small></div>
        <div><b>{MED}%</b><span>of the skills its closest AI era role needs, held today by the median marketing role</span><small>Inflexion skills map</small></div>
      </div>
    </div>
  </div>
</div>
{section("01", "change", "Platforms and agencies", "Media buying and campaign setup are becoming <em>platform settings.</em>", None, essay(
"Since 1 September 2026, Google has been moving search campaigns that use broad match or automatically created assets onto AI Max. The system chooses which searches an ad appears against and writes much of the ad copy itself. Amazon's Full-Funnel Campaigns ask the advertiser for a budget, a product list and creative, then decide the channels and audiences without letting the advertiser select either.",
"For more than a decade, setting up, bidding on and optimising campaigns like these was skilled work for planners, buyers and campaign managers. As more of it moves inside the platforms, the agencies that employed those people have reduced headcount. WPP has removed around 11,000 roles since early 2025 and has said most of its £500 million savings target will come from people costs. Among UK creative agencies counted in the IPA census, headcount fell 14.3% in the year to September 2025, and 30% of those agencies expect to make further cuts because of AI within a year.",
"Marketing teams inside brands have changed less so far, partly because much of their execution work sits with agencies and platforms rather than on their own payroll. That protection is weakening. BCG estimates that three to five people working alongside AI agents can run campaigns with 60% fewer resources than a conventional campaign team, and figures like that reach finance teams quickly. A marketing department with a large execution workload will be asked how it plans to change."))}
{section("02", "why", "The cost of cutting first", "Reducing headcount first loses knowledge that is <em>expensive to replace.</em>", None, essay(
"The quickest response to automation is to reduce headcount and let the platforms carry the work, and the saving appears in the next set of accounts. What leaves with those people is harder to measure. They know the brand's customers, why particular campaigns worked, which products carry the margin and how decisions get made internally. Agents produce good work when someone gives them that context. Without it they produce plausible work that gradually drifts away from what the business needs.",
"Most large employers say they intend to retrain staff before replacing them. In the World Economic Forum's 2025 survey, 85% of employers planned to prioritise upskilling and half planned to move staff from declining roles into growing ones. The same report expects 39% of workers' existing skills to be transformed or become outdated by 2030.",
"Retraining a marketing team for the roles described below takes around two years, based on published course lengths and a year of supervised project work. A company that starts in 2026 can do most of it with the people it already employs. A company that starts later is more likely to be cutting and hiring at the same time, paying a premium for skills that are still scarce, after the people with the most context have already left."), alt=True)}
{section("03", "roles", "Seven roles", "Seven roles cover most of the work <em>a marketing team will still do.</em>", "The work that remains after automation groups into seven roles. Each builds on a role that exists today and adds the ability to direct AI agents and check what they produce. The table lists the current roles each one draws from, what the job involves and the piece of work that would show someone is ready for the title.", roles_table)}
{section("04", "model", "Operating model", "Small pods run the work and a shared studio <em>builds the tools.</em>", "Most marketing work is likely to be run by pods of three to five people, each working with AI agents, which matches the structure BCG describes. A Growth Partner leads each pod and is accountable for its commercial results. Builders, the engineers in this model, sit in a shared studio and move between pods, turning anything used more than once into a tool every pod can use. Each discipline also keeps a practice that sets standards and runs training, so a creative working in a commerce pod still develops alongside other creatives.", figure(dg.operating_model()), alt=True)}
{section("05", "loop", "Delivery", "Each project runs through six steps and <em>leaves a reusable tool behind.</em>", "A beauty brand losing sales because shoppers now ask AI assistants for recommendations is a typical case. The Growth Partner defines the commercial problem, and the Decision Scientist sets a target and decides how it will be measured. A Builder writes an agent that corrects and enriches the brand's product data. The Agentic Systems Designer runs that agent day to day while the visibility and commerce specialists decide what it should change. The Decision Scientist then measures the effect on sales, and where the contract allows, the method behind the agent is reused for the next brand with the same problem.", figure(dg.loop()))}
{section("06", "relationship", "Client and agency", "The client and agency relationship is being repriced <em>around results and ownership.</em>", None, relationship_html(), alt=True)}
{section("07", "people", "Skills gap", "Today's marketing roles hold about half of the skills <em>the new roles need.</em>", f"We profiled 62 current brand, marketing, advertising and creative roles and 61 destination roles across 86 skills, then scored every current role against every destination at mid level. The median current role holds {MED}% of what its closest AI era role requires. The easiest move is from CRM Manager to Personalisation Manager, at 93%. Media Buyer and Media Planner, the roles most exposed to platform automation, score 39% and 41% against their closest AI era roles, which puts them among the furthest from the new work.", figure(dg.feeders(feeder_rows), "Skill match is the share of a role's required skill levels a person already holds. Core skills count double and closely related skills earn partial credit.") + figure(dg.strip(strip_groups), f"Marketing has the widest spread because it includes roles close to AI era work, such as CRM, SEO and marketing operations, alongside account based and field marketing roles that sit further away. In {two_step_wins} of the {two_step_total} moves scored into AI era roles, going through an intermediate role scores higher than moving directly."))}
{section("08", "unknowns", "What is still uncertain", "Three parts of this analysis <em>could prove wrong.</em>", None, essay(*UNKNOWNS), alt=True)}
{section("09", "questions", "Open questions", "Seven questions that shape how <em>a marketing team changes.</em>", "A leadership team would need answers to these before agreeing a marketing budget for 2027.", qs)}
<div class="appx" id="appendix"><div class="w"><div class="eyebrow">Appendix</div><h2>Skills, training and assessment in detail</h2><p>The sections that follow give the detail behind the analysis. They cover the skills each role needs, career levels, how pod composition varies, a two year training route with courses and hours, how people can be assessed, and a role finder covering all 62 current roles.</p></div></div>
{section("A1", "skills", "Skills", "Four skills are common to <em>every role.</em>", "Every role needs a working command of AI tools, enough data literacy to judge evidence, an understanding of how the business makes money and a grasp of AI risk and regulation. Each role then needs depth in two or three further areas, shown below. Roles that share a core skill make natural sideways moves later in a career.", figure(dg.skills_matrix()))}
{section("A2", "ladders", "Career levels", "Each role has a junior, mid and <em>senior level.</em>", "Retraining is easier to commit to when it leads to a career, so each role has three titles. Promotion is based on delivered work rather than completed courses. The mid level title is the one used for each role elsewhere on this page.", ladder, alt=True)}
{section("A3", "pods", "Pod mix", "The specialists in a pod depend on <em>the problem it is solving.</em>", "Every pod has a Growth Partner and a Decision Scientist, and the rest changes with the work. A retailer selling through Amazon and AI shopping assistants needs commerce and visibility specialists. A consumer brand producing large volumes of content needs someone running creative systems. A company building its own AI tools needs Builders working alongside its engineers.", pods)}
{section("A4", "plan", "Training route", "The route takes two years at <em>half a day a week.</em>", "Everyone starts with the same four month foundation. People then spend eight months on courses and supervised work for their new role, and at month twelve they deliver one real piece of work in it before taking the title. The second year is spent in the role on live projects. That comes to about 340 hours per person, roughly 100 on courses and 240 on project work. Course hours come from published course lengths, and the totals are estimates.", figure(dg.gantt()) + cards, alt=True)}
{section("A5", "scoring", "Assessment", "Assessment should weight evidence <em>by how reliable it is.</em>", "Placing people on the right route depends on an accurate view of what they can already do. Tests and work samples are the most reliable evidence, an AI led interview and CV analysis less so, and a self rating least of all. Where sources disagree, lowering confidence in that skill is safer than averaging the scores, because it stops a self rating alone from placing someone on a route. Tracking how placed people perform over time shows whether the weighting is right.", figure(dg.scoring()))}
{section("A6", "explore", "Role finder", "Where each current role <em>can move next.</em>", "Choose a current role to see its closest destinations, ranked by skill match, and the core skills it would need to build first.", explore_html, alt=True)}
<section class="sec" id="notes"><div class="w"><div class="sec-head rv"><div class="eyebrow">Method and sources</div><h2>Method and sources</h2></div>
<div class="notes rv"><div><h3>Method</h3><p>The skills map profiles 62 UK roles across brand, marketing, advertising and creative at junior, mid and senior level, and 61 destination roles with the skill levels and core skills each requires. Skill match uses mid level profiles. Course hours come from published course lengths, and total hours per role are Inflexion estimates. The relationship models describe common patterns and are not a ranking. Courses and prices change quickly, so the list is reviewed every six months.</p></div>
<div><h3>Sources</h3><ul class="srcs">{srcs}</ul></div></div></div></section>
<footer><div class="w"><div class="row"><div><img src="{logo_src}" alt="Inflexion Media"><p class="tag">Inflexion Intelligence publishes research on how AI is changing <em>marketing work.</em></p></div>
<div class="cta-row"><a class="foot-link" href="https://nicksc1cc.github.io/inflexion-website/contact/" target="_blank" rel="noopener">Contact Inflexion</a></div></div>
<small>Inflexion Intelligence &middot; {TITLE} &middot; October 2026</small></div></footer>
<script id="exData" type="application/json">{json.dumps(EX, separators=(",", ":"))}</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>{JS}</script>'''
    return body


logo_uri = "data:image/png;base64," + base64.b64encode(open(LOGO, "rb").read()).decode()
art = f'<title>Inflexion Pathways</title>\n<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@200;300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">\n<style>{CSS}</style>\n' + page(logo_uri)
open(f"{HERE}/pathways.html", "w").write(art)

URL = "https://nicksc1cc.github.io/inflexion-website/pathways/"
DESC = "Seven roles the AI era marketing team will be built around, how close 62 of today's marketing roles are to them and a two year plan to retrain people."
head = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{TITLE} | Inflexion</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="{URL}">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:type" content="article"><meta property="og:url" content="{URL}">
<meta property="og:image" content="https://nicksc1cc.github.io/inflexion-website/assets/og-pathways.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="https://nicksc1cc.github.io/inflexion-website/assets/og-pathways.png">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{TITLE}","description":"{DESC}","author":{{"@type":"Organization","name":"Inflexion"}},"publisher":{{"@type":"Organization","name":"Inflexion"}},"datePublished":"2026-10-14","url":"{URL}"}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@200;300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>[hidden]{{display:none!important}}img{{max-width:100%}}body{{margin:0}}{CSS}</style>
</head>
<body>'''
site = head + page("../assets/images/inflexion-media-logo-white.png").replace(
    'href="https://nicksc1cc.github.io/inflexion-website/contact/"', 'href="../contact/"').replace(
    'href="https://nicksc1cc.github.io/inflexion-website/"', 'href="../"') + "\n</body>\n</html>\n"
os.makedirs(f"{HERE}/site/pathways", exist_ok=True)
open(f"{HERE}/site/pathways/index.html", "w").write(site)
json.dump(EX, open(f"{HERE}/site/pathways/pathways-data.json", "w"), indent=1)
print(len(art), len(site), "median", statistics.median(all_best), two_step_wins, two_step_total)
