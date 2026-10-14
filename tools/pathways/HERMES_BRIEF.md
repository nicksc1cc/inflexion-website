HERMES BRIEF: INFLEXION PATHWAYS PAGE
Repo: nicksc1cc/inflexion-website
Live URL once shipped: https://nicksc1cc.github.io/inflexion-website/pathways/
Owner: Nick. Ask Nick before anything marked ASK.


1. WHAT THIS IS

A thought leadership page in the Inflexion brand, written for senior leaders without ever addressing them directly. Its argument: platform automation and agency cuts mean the marketing team is being redesigned around AI agents, cutting headcount first loses knowledge that is expensive to replace, and a planned two year retraining route is the alternative. It moves from what is changing, to the cost of cutting first, to the seven roles and how they work, to how the client and agency relationship changes, to how far today's roles are from them, to what could prove wrong, and ends with seven open questions. Detail on skills, training and assessment sits in an appendix.

It draws on two pieces of work:

a) The agency model: seven future roles (Growth Partner, AI Visibility Lead, Agentic Systems Designer, Forward Deployed Builder, Decision Scientist, Creative Systems Director, Agentic Commerce Lead), how they work together in pods, a delivery loop, career ladders and a 24 month training plan with real courses and hours.

b) The pathway engine: a skills map of 86 skills, 62 current UK marketing roles (9 brand, 23 marketing, 14 advertising, 16 creative) and 61 destination roles (24 AI era, 18 adjacent, 19 cross sector), each profiled at junior, mid and senior. Every current role is scored against every destination. A route finder lets a reader pick their role and see where it can go.

The page is finished and builds from source. Your jobs are: integrate it into the site (section 3), then the extensions in section 6 when Nick asks for them. Do not rewrite the argument or reorder sections without asking Nick.


2. WHAT IS IN THIS KIT

site/pathways/index.html        The finished page (title: The marketing team is being redesigned around AI agents). Full HTML document, relative paths, ready to drop in.
site/pathways/pathways-data.json Readable copy of the route finder data (the page has it inline; this file is for reference).
pathways.html                   Artifact version (logo inlined, no head). Ignore for the site.
build.py                        Builds both files. Single source of truth for page copy and content.
diagrams.py                     All SVG diagrams as Python functions. Colours come only from CSS classes.
page.css                        All styles, tokens at the top, light and dark themes.
page.js                         Route finder, scroll reveal, hero line field (same as the opportunity map).
fit.py                          Scores every current role against every destination and two step routes. Writes fit.json.
s1/                             Stage 1 skills map source: skills.txt, sources_*.txt, targets.txt, compile.py, stage1_schema.json.
assets/inflexion-media-logo-white.png  Used only by the artifact build.
copy_check.py                   Copy checker. Must report 0 issues before any commit.

To rebuild after any change, from the kit folder:
cd s1 && python3 compile.py && cd ..
python3 fit.py
python3 build.py
Needs Python 3 only. No packages.

Never hand edit site/pathways/index.html. Change build.py, diagrams.py, page.css or page.js, then rebuild. Otherwise the next rebuild wipes your edit.


3. INTEGRATION STEPS

Deploy note: the site deploys from the main branch via .github/workflows/pages-deploy.yml. Commit to main. Check the workflow file before you push in case it has changed.

3.1 Copy site/pathways/index.html to pathways/index.html in the repo root. It sits next to opportunity-map/ and follows the same standalone pattern: its own styles, white logo from ../assets/images/inflexion-media-logo-white.png, contact link to ../contact/.

3.2 Store the build kit in the repo at tools/pathways/ (everything except site/ and pathways.html), so the page can be rebuilt later. Add a one line README there with the rebuild commands above.

3.3 Check page_configs.py and update_pages.py. If either rewrites headers, footers or nav across pages, make sure it skips pathways/ the same way it skips opportunity-map/. Run them in dry mode if they have one and confirm pathways/index.html is unchanged.

3.4 Open Graph image. The page points at assets/og-pathways.png. Create assets/og-pathways.svg by copying assets/og-opportunity-map.svg and changing the text to: "The marketing team is being redesigned around AI agents." Export it to assets/og-pathways.png at the same size as og-opportunity-map.png, using whatever method was used for the existing OG images.

3.5 sitemap.xml: add a url block after the opportunity map one:
loc https://nicksc1cc.github.io/inflexion-website/pathways/
changefreq monthly
priority 0.8

3.6 llms.txt: add after the Opportunity map block:
## The marketing team is being redesigned around AI agents
Seven roles the AI era marketing team will be built around, how close 62 of today's marketing roles are to them and a two year plan to retrain people.
https://nicksc1cc.github.io/inflexion-website/pathways/

3.7 Main navigation. ASK Nick before adding "Pathways" to the nav in index.html and other pages. If yes, add it straight after the Opportunity map link in the same format.

3.8 Commit message: "Add perspective: the marketing team is being redesigned around AI agents".


4. DESIGN AND COPY RULES

Brand: matches the opportunity map. Montserrat light for headings and body, IBM Plex Mono for labels. Warm white sections alternating with #f4f4f0, dark hero and footer with the orange to blue line field. Orange #ff5a1f for emphasis only. Blue #2438da for data. Dark theme tokens are defined in page.css; keep both themes working.

Diagrams: every colour is a CSS class (.n, .n-focal, .f, .f-dash, .bar-a and so on). Never put a hex colour inside an SVG. Wide diagrams sit inside .scroll so phones scroll them sideways; the page body must never scroll sideways.

Copy rules (Nick's standard, apply to anything you add or change):
Write about the subject. Never address the reader or name the audience: no "you", "your", "the board should", "CEOs need to", "leaders must".
Write in full, connected paragraphs where each sentence follows from the last. No fragments, no slogan sentences, no tidy moral at the end of a paragraph.
Every claim is either sourced or framed as Inflexion's own estimate or finding. Prefer a specific finding from the data to a general statement.
No em dashes or en dashes. No hyphenated compounds (write "AI era", "two year", "content led").
No "not X, but Y", no "isn't X. It's Y", no colon reveals, no rhetorical questions in body copy, no signposting such as "this piece sets out".
Headings are single plain statements, with the orange accent on the closing words only.
UK English. Concise.

Before every commit, run: python3 copy_check.py site/pathways/index.html
It must report 0 issues. It checks dashes, hyphenated compounds, reader address, stock phrases and common AI sentence patterns. Passing it is the minimum; also read the changed copy aloud once.
No founder claims, no team names, no client names, no case studies, no invented results.
Never name the parent technology company.
Every statistic needs a source in section 12 of the page.


5. HOW THE PAGE IS BUILT

Section order (ids in brackets): hero, 01 Platforms and agencies (change), 02 The cost of cutting first (why), 03 Seven roles (roles), 04 Operating model (model), 05 Delivery (loop), 06 Client and agency (relationship), 07 Skills gap (people), 08 What is still uncertain (unknowns), 09 Open questions (questions), Appendix band (appendix), A1 Skills (skills), A2 Career levels (ladders), A3 Pod mix (pods), A4 Training route (plan), A5 Assessment (scoring), A6 Role finder (explore), Method and sources (notes), footer.

The piece is thought leadership. Keep Inflexion to the logo and the plain "Contact Inflexion" footer link. Do not add buttons, service pitches or Inflexion product names. The three client and agency models are presented neutrally; do not rank them.

Every statistic in sections 01 and 02 and the hero banner was checked against its source on 14 October 2026. If you add or change a figure, add its source to SOURCES.

Where to change content:
Seven roles table: SEVEN in build.py (today, role, what it does, related roles, ready when delivered).
Essay sections 01 and 02 and all section intros: inside page() in build.py.
Open questions: QUESTIONS in build.py.
Client and agency section: SHIFT, SIDES, MODELS and relationship_html() in build.py; the who leads matrix is REL_ROWS and relationship_matrix() in diagrams.py.
Uncertainties: UNKNOWNS in build.py.
Ladder titles and rung descriptions: LADDER and RUNGS in build.py.
Training cards, courses, hours, readiness tests: FOUNDATION and DETAIL in build.py.
Gantt bars: PATHS in diagrams.py. Keep hours in PATHS and DETAIL in step.
Skills map rows and dots: MATRIX in diagrams.py. 3 = shared foundation, 2 = core, 1 = supporting, 0 = none.
Pod variants: PODS in diagrams.py. Four members per pod.
Sources: SOURCES in build.py.

Diagram functions in diagrams.py: operating_model, loop, skills_matrix, pods, gantt, feeders, strip, scoring. Shared helpers: node(x, y, w, h, name, sub, kind, tag) where kind is std, focal, agent, ext or dark; zone(); label(); legend().

Skill match method (fit.py):
For each required skill of a destination at mid level, credit = held level divided by required level, capped at 1. If the person lacks the skill, they get half credit from their best related skill. Core skills count twice. Match = weighted credit divided by total weight.
Two step routes: for each current role and AI era destination, try every other destination as a middle step, using the middle role's required levels as its profile. Route score = the weaker of the two legs. A route is kept only if it beats the direct move by more than 5 points.
Gaps: required skills where the held level falls short, core first, largest shortfall first.

Route finder data (inline JSON in script#exData, same as pathways-data.json):
s: list of current roles, each [id, title, discipline, ai_risk, summary, top10, best_ai]
   top10 is [[match %, destination id, [gap skill ids]], ...] sorted best first
   best_ai is [match %, destination id, [gap skill ids], two_step or null], two_step is [route %, middle destination id]
t: {destination id: [title, category, demand, description, junior title, senior title]}
k: {skill id: skill name}

Stage 1 source format (s1/*.txt):
Skills: id|name|category|ai_exposure|evidence codes|description|four level descriptors separated by ;|related skill ids
Current roles: @id|discipline|ai_risk|junior/mid/senior titles|summary, then one line per skill: [*]skill_id j/m/s rationale (* marks a signature skill)
Destinations: @id|category|demand|ai_resilience|junior/mid/senior titles|description|leads_to;leads_to, then one line per skill: [*]skill_id j/m/s (* marks a core requirement)
compile.py validates and prints errors and warnings. Fix all errors before rebuilding. Current warnings are known and acceptable.


6. EXTENSIONS (only when Nick asks)

6.1 Role pages. One page per future role at pathways/<role-slug>/ with a week by week plan for months 0 to 24, course links, the proof gate, the ladder and which current roles feed it. Same template and build approach. ASK Nick which role first.

6.2 Full permutations (Stage 2). Extend fit.py to score every current role x destination x seniority (about 11,000 one step routes) and keep the best five middle roles per pair for two step routes. Write to data/pathways-full.json. Do not inline it into the page if it exceeds 2 MB; load it with fetch from the same folder instead.

6.3 Scoring engine (Stage 3). A JavaScript function that takes evidence per skill (source: test, work_sample, ai_interview, cv_analysis, self_rating; level 1 to 4) and returns a level and confidence per skill, then ranked destinations with gaps. Weight tests and work samples highest, AI interview and CV next, self rating lowest. Where sources disagree by 2 or more levels, lower the confidence instead of averaging. Mirror it in Python for testing. ASK Nick to confirm the weights before shipping.

6.4 Seniority switch in the route finder. Add junior, mid and senior tabs that recompute matches. Needs 6.2 data.


7. QA CHECKLIST BEFORE YOU PUSH

1. Page opens locally with no console errors except blocked fonts when offline.
2. At 400px wide the page does not scroll sideways. Diagrams scroll inside their boxes.
3. Toggle the OS to dark mode. All text is readable, nothing appears as white on white.
4. Route finder: pick SEO Manager, Illustrator and Media Buyer. Each shows a best AI era move and ten destinations with gaps.
5. All 15 source links in section 14 open.
6. The header logo and footer logo load from ../assets/images/.
7. sitemap.xml validates, llms.txt entry added, og-pathways.png exists.
8. python3 copy_check.py site/pathways/index.html reports 0 issues.
9. After pushing, wait for the Pages workflow to finish and open the live URL.

Report back to Nick with the live URL and anything you skipped.
