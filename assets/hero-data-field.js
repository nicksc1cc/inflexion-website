/* Shared Inflexion hero data field */
(function () {
  var canvas = document.getElementById('data-field-canvas');
  if (!canvas || typeof THREE === 'undefined') return;
  var gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
  if (!gl) return;

  var scene = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera(55, 1, 0.1, 100);
  camera.position.set(0, -2, 9);
  var renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
  renderer.setClearColor(0x000000, 0);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

  var group = new THREE.Group();
  scene.add(group);
  var lines = 60;
  var pointsPerLine = 100;
  for (var i = 0; i < lines; i += 1) {
    var points = [];
    var x = (i - lines / 2) * 0.2;
    for (var j = 0; j < pointsPerLine; j += 1) {
      points.push(new THREE.Vector3(x, (j - pointsPerLine / 2) * 0.2, 0));
    }
    var colour = new THREE.Color().setHSL(0.08 - (i / lines) * 0.12, 0.8, 0.6 + (i / lines) * 0.3);
    var material = new THREE.LineBasicMaterial({
      color: colour,
      transparent: true,
      opacity: 0.18 + Math.random() * 0.2,
      blending: THREE.AdditiveBlending
    });
    group.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(points), material));
  }

  function resize() {
    var rect = canvas.parentElement.getBoundingClientRect();
    var width = Math.max(1, rect.width);
    var height = Math.max(1, rect.height);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height, false);
  }
  resize();
  window.addEventListener('resize', resize, { passive: true });

  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function render() {
    var t = reduceMotion ? 0 : performance.now() * 0.0004;
    group.children.forEach(function (line) {
      var data = line.geometry.attributes.position.array;
      for (var k = 0; k < pointsPerLine; k += 1) {
        var px = data[k * 3];
        var py = data[k * 3 + 1];
        data[k * 3 + 2] = Math.sin(py * 1.2 + t + px * 0.8) * 0.8 + Math.cos(px * 1.5 - t * 0.8 + py * 0.5) * 0.6;
      }
      line.geometry.attributes.position.needsUpdate = true;
    });
    renderer.render(scene, camera);
    if (!reduceMotion) requestAnimationFrame(render);
  }
  render();
})();
