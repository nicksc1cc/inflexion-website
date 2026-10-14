import json,collections
D=json.load(open("s1/_compiled.json"))
SK={s["id"]:s for s in D["skills"]}
def prof_src(r,sen="mid"): return {s["skill_id"]:s["levels"][sen] for s in r["skills"]}
def prof_tgt(t,sen="mid"): return {s["skill_id"]:s["required_levels"][sen] for s in t["required_skills"]}
def fit(have,t,sen="mid"):
    num=den=0;gaps=[]
    for s in t["required_skills"]:
        n=s["required_levels"][sen]; w=2 if s["importance"]=="core" else 1
        h=have.get(s["skill_id"],0)
        if h==0:
            rel=[have.get(x,0)*0.5 for x in SK[s["skill_id"]]["related_skills"]]
            h=max(rel) if rel else 0
        c=min(h/n,1) if n else 1
        num+=w*c;den+=w
        if h<n: gaps.append((s["importance"]=="core",n-h,s["skill_id"]))
    gaps.sort(key=lambda g:(-g[0],-g[1]))
    return num/den,[g[2] for g in gaps]
T=D["targets"];S=D["sources"]
res={}
for r in S:
    hv=prof_src(r);rows=[]
    for t in T:
        f,g=fit(hv,t);rows.append((f,t["id"],g))
    rows.sort(reverse=True);res[r["id"]]=rows
# two-step via any target as middle
mid={t["id"]:prof_tgt(t) for t in T}
tw={}
for r in S:
    hv=prof_src(r)
    for t in T:
        if t["category"]!="ai_era":continue
        d,_=fit(hv,t)
        best=None
        for m in T:
            if m["id"]==t["id"]:continue
            a,_=fit(hv,m);b,_=fit(mid[m["id"]],t);sc=min(a,b)
            if sc>d+0.05 and (best is None or sc>best[0]):best=(sc,m["id"])
        tw[(r["id"],t["id"])]=(d,best)
# stats
best_ai={t["id"]:max((res[r["id"]][[x[1] for x in res[r["id"]]].index(t["id"])][0],r["id"]) for r in S) for t in T}
for t in T:
    if t["category"]=="ai_era": print(t["titles"]["mid"],round(best_ai[t["id"]][0]*100),best_ai[t["id"]][1])
disc=collections.defaultdict(list)
for r in S:
    b=max(x[0] for x in res[r["id"]] if [t for t in T if t["id"]==x[1]][0]["category"]=="ai_era")
    disc[r["discipline"]].append(round(b*100))
print({k:sorted(v) for k,v in disc.items()})
print(sum(1 for k,v in tw.items() if v[1]),len(tw))
json.dump({"res":{k:[(round(f*100),t,g[:4]) for f,t,g in v] for k,v in res.items()},"tw":{f"{a}|{b}":[round(v[0]*100),(round(v[1][0]*100),v[1][1]) if v[1] else None] for (a,b),v in tw.items()}},open("fit.json","w"))
