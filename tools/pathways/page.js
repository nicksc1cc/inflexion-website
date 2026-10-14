const reduce=matchMedia("(prefers-reduced-motion: reduce)").matches;

/* pathway explorer. Data shape is documented in the Hermes brief:
   s: [id, title, discipline, ai_risk, summary, top10[[fit, targetId, gapSkillIds]], best_ai[fit, targetId, gaps, twoStep[fit, viaId]|null]]
   t: {id: [title, category, demand, description, juniorTitle, seniorTitle]}
   k: {skillId: skillName} */
(function(){
  const X=JSON.parse(document.getElementById("exData").textContent);
  const sel=document.getElementById("exSel"),sum=document.getElementById("exSum"),best=document.getElementById("exBest"),list=document.getElementById("exList");
  const CAT={ai_era:"AI era",adjacent:"Adjacent",cross_sector:"Cross sector"};
  const RISK={high:"high",medium:"medium",low:"low"};
  const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
  const gaps=g=>g.length?g.slice(0,3).map(id=>X.k[id]).join(", "):"No core gaps at mid level";
  let grp="";
  X.s.forEach((r,i)=>{if(r[2]!==grp){grp=r[2];const og=document.createElement("optgroup");og.label=grp;sel.appendChild(og)}
    const o=document.createElement("option");o.value=i;o.textContent=r[1];sel.lastChild.appendChild(o)});
  function render(i){
    const r=X.s[i],b=r[6],t=X.t[b[1]];
    sum.innerHTML=`<b>${esc(r[1])}</b> · ${esc(r[4])}. Exposure to AI automation: ${RISK[r[3]]}.`;
    let route=`<div class="step"><div class="pct">${b[0]}%</div><div><b>Direct move</b><span>Skill match today. Skills to build first: ${esc(gaps(b[2]))}.</span></div></div>`;
    if(b[3]){const v=X.t[b[3][1]];route+=`<div class="step"><div class="pct">${b[3][0]}%</div><div><b>Via ${esc(v[0])}</b><span>Move into this role first. Both steps score at least ${b[3][0]}%, which makes this route easier than the direct move.</span></div></div>`}
    best.innerHTML=`<div class="cap">Best AI era move</div><h3>${esc(t[0])}</h3><p class="ex-sum">${esc(t[3])}. Ladder: ${esc(t[4])} to ${esc(t[5])}.</p><div class="route">${route}</div>`;
    list.innerHTML=`<div class="cap" style="padding-block:12px 4px">Top ten destinations</div>`+r[5].map(([f,id,g])=>{const d=X.t[id];
      return `<div class="erow"><div class="nm">${esc(d[0])}<span class="chip${d[1]==="ai_era"?" ai":""}">${CAT[d[1]]}</span></div><div class="meter"><i><em style="width:${f}%"></em></i>${f}%</div><div class="gp">Gaps: ${esc(gaps(g))}</div></div>`}).join("");
  }
  let start=X.s.findIndex(r=>r[0]==="seo");if(start<0)start=0;
  try{const k=localStorage.getItem("pw-role");if(k!==null&&X.s[+k])start=+k}catch(e){}
  sel.value=start;render(start);
  sel.addEventListener("change",()=>{render(+sel.value);try{localStorage.setItem("pw-role",sel.value)}catch(e){}});
})();

/* subtle reveal from a visible resting state */
(function(){
  if(reduce||!("IntersectionObserver" in window))return;
  const vh=innerHeight;
  const els=[...document.querySelectorAll(".rv")].filter(e=>e.getBoundingClientRect().top>vh*0.92);
  els.forEach(e=>e.classList.add("pre"));
  const io=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){en.target.classList.remove("pre");io.unobserve(en.target)}}),{rootMargin:"0px 0px -8% 0px"});
  els.forEach(e=>io.observe(e));
  setTimeout(()=>els.forEach(e=>e.classList.remove("pre")),6000);
})();

/* hero line field, matching the Inflexion site */
(function(){
  const canvas=document.getElementById("field");
  if(typeof THREE==="undefined")return;
  let renderer;try{renderer=new THREE.WebGLRenderer({canvas,alpha:true,antialias:true})}catch(e){return}
  renderer.setClearColor(0x000000,0);renderer.setPixelRatio(Math.min(devicePixelRatio||1,2));
  const scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(55,1,0.1,100);camera.position.set(0,-2,9);
  const group=new THREE.Group();scene.add(group);
  const lines=60,ppl=100;
  for(let i=0;i<lines;i++){const pts=[],x=(i-lines/2)*0.2;
    for(let j=0;j<ppl;j++)pts.push(new THREE.Vector3(x,(j-ppl/2)*0.2,0));
    const c=new THREE.Color().setHSL(0.08-(i/lines)*0.12,0.8,0.6+(i/lines)*0.3);
    group.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts),new THREE.LineBasicMaterial({color:c,transparent:true,opacity:0.16+Math.random()*0.18,blending:THREE.AdditiveBlending})));}
  group.rotation.z=-0.35;group.position.x=3;
  function resize(){const r=canvas.parentElement.getBoundingClientRect();camera.aspect=Math.max(1,r.width)/Math.max(1,r.height);camera.updateProjectionMatrix();renderer.setSize(r.width,r.height,false)}
  resize();addEventListener("resize",resize,{passive:true});
  let visible=true,running=false;
  function start(){if(!running&&!reduce){running=true;requestAnimationFrame(frame)}}
  new IntersectionObserver(es=>{visible=es[0].isIntersecting;if(visible)start()}).observe(canvas);
  function frame(){if(!visible&&!reduce){running=false;return}
    const t=reduce?0:performance.now()*0.0004;
    group.children.forEach(line=>{const d=line.geometry.attributes.position.array;
      for(let k=0;k<ppl;k++){const px=d[k*3],py=d[k*3+1];d[k*3+2]=Math.sin(py*1.2+t+px*0.8)*0.8+Math.cos(px*1.5-t*0.8+py*0.5)*0.6}
      line.geometry.attributes.position.needsUpdate=true});
    renderer.render(scene,camera);if(!reduce)requestAnimationFrame(frame)}
  if(reduce)frame();else start();
})();
