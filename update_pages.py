
import os

base = "/tmp/inflexion-website"

pages = [
    ("aeo.html", ".shift-row", ".old", ".new", [
        ("lim-row", ".lim-row"),
        ("why-row", ".why-row"),
        ("proc-step", ".proc-step"),
        ("stat-card", ".stat-card"),
        ("research-item", ".research-item"),
        ("quote-block", ".quote-block"),
        ("cta-inner", ".cta-inner"),
    ]),
    ("retail-media.html", ".shift-row", ".old", ".new", [
        ("feat-card", ".feat-card"),
        ("why-row", ".why-row"),
        ("proc-step", ".proc-step"),
        ("stat-card", ".stat-card"),
        ("cta-inner", ".cta-inner"),
    ]),
    ("consultancy.html", ".shift-row", ".old", ".new", [
        ("feat-card", ".feat-card"),
        ("client-strip span", ".client-strip"),
        ("proc-step", ".proc-step"),
        ("stat-card", ".stat-card"),
        ("cta-inner", ".cta-inner"),
    ]),
    ("ai-discovery.html", ".shift-row", ".old", ".new", [
        ("proc-step", ".proc-step"),
        ("stat-card", ".stat-card"),
        ("cta-inner", ".cta-inner"),
    ]),
    ("ai-visibility-analytics.html", ".shift-row", ".old", ".new", [
        ("feat-card", ".feat-card"),
        ("three-card", ".three-card"),
        ("proc-step", ".proc-step"),
        ("stat-card", ".stat-card"),
        ("cta-inner", ".cta-inner"),
    ]),
    ("technical-geo.html", ".shift-row", ".old", ".new", [
        ("feat-card", ".feat-card"),
        ("dark-stat", ".dark-stat"),
        ("proc-step", ".proc-step"),
        ("stat-card", ".stat-card"),
        ("cta-inner", ".cta-inner"),
    ]),
    ("digital-pr.html", ".shift-row", ".old", ".new", [
        ("feat-card", ".feat-card"),
        ("three-card", ".three-card"),
        ("proc-step", ".proc-step"),
        ("stat-card", ".stat-card"),
        ("cta-inner", ".cta-inner"),
    ]),
    ("measurement.html", ".shift-row", ".old", ".new", [
        ("why-row", ".why-row"),
        ("lim-row", ".lim-row"),
        ("proc-step", ".proc-step"),
        ("stat-card", ".stat-card"),
        ("cta-inner", ".cta-inner"),
    ]),
    ("contact.html", None, None, None, [
        ("cta-inner", ".cta-inner"),
    ]),
]

base = "/tmp/inflexion-website"

for page, shift_sel, shift_old, shift_new, extra in pages:
    path = os.path.join(base, page)
    with open(path) as f:
        c = f.read()
    
    # Build shift animation code
    shift_code = ""
    if shift_sel:
        shift_code = f"""  // Shift rows ({shift_sel})
  gsap.utils.toArray('{shift_sel}').forEach((el) => {{
    gsap.from(el.querySelector('{shift_old}'), {{
      ...revealDefaults,
      x: -30,
      scrollTrigger: {{ trigger: el, start: 'top 85%', toggleActions: 'play none none none' }}
    }});
    gsap.from(el.querySelector('{shift_new}'), {{
      ...revealDefaults,
      x: 30, delay: 0.1,
      scrollTrigger: {{ trigger: el, start: 'top 85%', toggleActions: 'play none none none' }}
    }});
  }});"""

    # Build extra staggers
    extra_code = []
    for selector, trigger in extra:
        extra_code.append(f"""  // {selector}
  gsap.from('{selector}', {{
    ...revealDefaults,
    stagger: 0.1,
    scrollTrigger: {{ trigger: '{trigger}', start: 'top 80%', toggleActions: 'play none none none' }}
  }});""")
    
    # Build new script
    new_script = """<script>
  gsap.registerPlugin(ScrollTrigger);

  // --- Hero entrance ---
  gsap.timeline({delay:0.3})
    .from('.hero .sup', { y: 30, opacity: 0, duration: 0.6, ease: 'power3.out' })
    .from('.hero h1', { y: 40, opacity: 0, duration: 0.8, ease: 'power3.out' }, '-=0.3')
    .from('.hero .desc, .hero .cta-row > *', { y: 30, opacity: 0, duration: 0.6, stagger: 0.1, ease: 'power2.out' }, '-=0.4')
    .from('.hero .data-banner > *', { y: 20, opacity: 0, duration: 0.5, stagger: 0.08, ease: 'power2.out' }, '-=0.3');

  // --- Scroll-triggered reveals ---
  const revealDefaults = { opacity: 0, y: 40, duration: 0.9, ease: 'power2.out' };
""" + shift_code + """

""" + "\n".join([
        f"""  // {selector}
  gsap.from('{selector}', {{
    ...revealDefaults,
    stagger: 0.1,
    scrollTrigger: {{ trigger: '{trigger}', start: 'top 80%', toggleActions: 'play none none none' }}
  }});""" for selector, trigger in extra
    ]) + """

  // --- Reduced-motion ---
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    gsap.globalTimeline.clear();
    ScrollTrigger.getAll().forEach(t => t.kill());
  }

  // --- Fallback ---
  setTimeout(() => {
    if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {
      document.querySelectorAll('.econ-col, .econ-shift > *, .shift-row > *, .proc-step, .svc, .cta-inner > *').forEach(el => {
        el.style.opacity = '1';
        el.style.transform = 'none';
      });
    }
  }, 3000);

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(function(a){
    a.addEventListener('click',function(e){e.preventDefault();var t=document.querySelector(this.getAttribute('href'));if(t)t.scrollIntoView({behavior:'smooth',block:'start'})});
  });

  // Mobile menu toggle
  var h = document.querySelector('.hamburger');
  var n = document.querySelector('header nav');
  if(h){h.addEventListener('click',function(){n.classList.toggle('open');h.classList.toggle('open')})}
  n.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){n.classList.remove('open');h.classList.remove('open')})});

  // Three.js Data Field animation
  (function(){
    var canvas = document.getElementById('data-field-canvas');
    if (!canvas || typeof THREE === 'undefined') return;
    var scene = new THREE.Scene();
    scene.background = null;
    var camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 100);
    camera.position.set(0, -2, 9);
    var renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
    renderer.setClearColor(0x000000, 0);
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    var group = new THREE.Group();
    scene.add(group);
    var numLines = 60, pts = 100;
    for (var i = 0; i < numLines; i++) {
      var points = [];
      var xPos = (i - numLines / 2) * 0.22;
      for (var j = 0; j < pts; j++) {
        points.push(new THREE.Vector3(xPos, (j - pts / 2) * 0.2, 0));
      }
      var t = i / numLines;
      var color = new THREE.Color().setHSL(0.08 - t * 0.12, 0.8, 0.6 + t * 0.3);
      var mat = new THREE.LineBasicMaterial({ color: color, transparent: true, opacity: 0.2 + Math.random() * 0.3, blending: THREE.AdditiveBlending });
      var line = new THREE.Line(new THREE.BufferGeometry().setFromPoints(points), mat);
      group.add(line);
    }
    group.rotation.x = Math.PI / 3;
    group.rotation.z = -Math.PI / 8;
    function animate() {
      requestAnimationFrame(animate);
      var time = performance.now() * 0.0004;
      group.children.forEach(function(line){
        var pos = line.geometry.attributes.position.array;
        for (var j = 0; j < pts; j++) {
          var idx = j * 3;
          var x = pos[idx], y = pos[idx + 1];
          pos[idx + 2] = Math.sin(y * 1.2 + time + x * 0.8) * 0.8 + Math.cos(x * 1.5 - time * 0.8 + y * 0.5) * 0.6;
        }
        line.geometry.attributes.position.needsUpdate = true;
      });
      renderer.render(scene, camera);
    }
    animate();
    window.addEventListener('resize', function(){
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });
  })();

  // Mobile menu toggle
  var h = document.querySelector('.hamburger');
  var n = document.querySelector('header nav');
  if(h){h.addEventListener('click',function(){n.classList.toggle('open');h.classList.toggle('open')})}
  n.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){n.classList.remove('open');h.classList.remove('open')})});

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(function(a){
    a.addEventListener('click',function(e){e.preventDefault();var t=document.querySelector(this.getAttribute('href'));if(t)t.scrollIntoView({behavior:'smooth',block:'start'})});
  });
</script>"""

    # Find and replace the last script
    with open(os.path.join("/tmp/inflexion-website", page)) as f:
        c = f.read()
    
    idx = c.rfind('<script>')
    if idx == -1:
        print(f"  No script tag found for {page}")
        continue
    
    script_end = c.find('</script>', idx)
    if script_end == -1:
        print(f"  No closing script tag for {page}")
        continue
    script_end += 9
    
    old_script = c[idx:script_end]
    new_c = c[:idx] + new_script + c[script_end:]
    
    with open(os.path.join("/tmp/inflexion-website", page), "w") as f:
        f.write(new_c)
    print(f"Updated {page}")

print("Done!")
