(function () {
  var canvas = document.createElement('canvas');
  var available = false;
  try {
    available = !!(canvas.getContext('webgl') || canvas.getContext('experimental-webgl'));
  } catch (error) {
    available = false;
  }
  window.__webglAvailable = available;
  if (!available) document.documentElement.classList.add('no-webgl');
  window.addEventListener('error', function (event) {
    var message = event && event.message ? event.message : '';
    if (message.indexOf('Error creating WebGL context') !== -1) {
      event.preventDefault();
      event.stopImmediatePropagation();
    }
  }, true);
}());
