import json, collections, sys
EV={"T":"test","W":"work_sample","I":"ai_interview","C":"cv_analysis","S":"self_rating"}
skills=[];sid=set()
for ln in open("skills.txt"):
    if ln.startswith("#") or not ln.strip(): continue
    p=ln.rstrip("\n").split("|"); assert len(p)==8,p[0]
    d=p[6].split(";"); assert len(d)==4,p[0]
    skills.append({"id":p[0],"name":p[1],"category":p[2],"ai_exposure":p[3],
      "best_evidence":[EV[x] for x in p[4].split(",")],"description":p[5],
      "level_descriptors":{"1":d[0],"2":d[1],"3":d[2],"4":d[3]},
      "related_skills":p[7].split(",") if p[7] else []})
    sid.add(p[0])
errs=[];warns=[]
for s in skills:
    for r in s["related_skills"]:
        if r not in sid: errs.append(f"related {s['id']}->{r}")
SEN=["junior","mid","senior"]
def parse_blocks(files,kind):
    out=[];cur=None
    for f in files:
        for ln in open(f):
            ln=ln.rstrip("\n")
            if not ln.strip() or ln.startswith("#"): continue
            if ln.startswith("@"):
                p=ln[1:].split("|"); cur={"_h":p,"_s":[]}; out.append(cur)
            else:
                core=ln.startswith("*"); ln=ln.lstrip("*")
                parts=ln.split(" ",2)
                lv=[int(x) for x in parts[1].split("/")]
                cur["_s"].append((parts[0],lv,core,parts[2] if len(parts)>2 else None))
    return out
sources=[]
for b in parse_blocks(["sources_brand_marketing.txt","sources_adv_creative.txt"],"s"):
    rid,disc,risk,titles,summary=b["_h"]; t=titles.split("/"); assert len(t)==3,rid
    seen=set(); sk=[]
    for k,lv,core,rat in b["_s"]:
        if k not in sid: errs.append(f"{rid}: unknown skill {k}")
        if k in seen: errs.append(f"{rid}: duplicate {k}")
        seen.add(k)
        if lv!=sorted(lv): warns.append(f"{rid}: {k} decreases with seniority {lv}")
        if not rat: errs.append(f"{rid}: {k} missing rationale")
        sk.append({"skill_id":k,"levels":dict(zip(SEN,lv)),"signature":core,"rationale":rat})
    if len(sk)<10: warns.append(f"{rid}: only {len(sk)} skills")
    if sum(s["signature"] for s in sk)<3: errs.append(f"{rid}: fewer than 3 signature skills")
    sources.append({"id":rid,"discipline":disc,"ai_displacement_risk":risk,
      "titles":dict(zip(SEN,t)),"summary":summary,"skills":sk})
targets=[]
for b in parse_blocks(["targets.txt"],"t"):
    rid,cat,dem,res,titles,desc,leads=b["_h"]; t=titles.split("/"); assert len(t)==3,rid
    seen=set(); rq=[]
    for k,lv,core,_ in b["_s"]:
        if k not in sid: errs.append(f"{rid}: unknown skill {k}")
        if k in seen: errs.append(f"{rid}: duplicate {k}")
        seen.add(k)
        if lv!=sorted(lv): warns.append(f"{rid}: {k} decreases {lv}")
        rq.append({"skill_id":k,"required_levels":dict(zip(SEN,lv)),"importance":"core" if core else "supporting"})
    if not any(r["importance"]=="core" for r in rq): errs.append(f"{rid}: no core")
    targets.append({"id":rid,"category":cat,"demand_outlook":dem,"ai_resilience":res,
      "titles":dict(zip(SEN,t)),"description":desc,"required_skills":rq,"leads_to":leads.split(";")})
ids=[r["id"] for r in sources]+[r["id"] for r in targets]
dups=[i for i,c in collections.Counter(ids).items() if c>1]
if dups: errs.append(f"duplicate role ids {dups}")
used=collections.Counter()
for r in sources:
    for s in r["skills"]: used[s["skill_id"]]+=1
tused=collections.Counter()
for r in targets:
    for s in r["required_skills"]: tused[s["skill_id"]]+=1
for s in sid:
    if used[s]==0: warns.append(f"skill never held by a source role: {s}")
    if tused[s]==0: warns.append(f"skill never required by a target role: {s}")
print("ERRORS",len(errs)); [print(" ",e) for e in errs]
print("WARNINGS",len(warns)); [print(" ",w) for w in warns]
print("skills",len(skills),collections.Counter(s["category"] for s in skills))
print("sources",len(sources),collections.Counter(s["discipline"] for s in sources))
print("targets",len(targets),collections.Counter(t["category"] for t in targets))
print("skill rows sources",sum(len(r["skills"]) for r in sources),"targets",sum(len(r["required_skills"]) for r in targets))
json.dump({"skills":skills,"sources":sources,"targets":targets},open("_compiled.json","w"))
