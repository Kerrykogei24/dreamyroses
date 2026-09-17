// Mobile navigation
(function () {
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("sitenav");
  if (!toggle || !nav) return;
  toggle.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(open));
    toggle.textContent = open ? "Close" : "Menu";
  });
})();

// Drag-to-colour hero: the line-art layer is clipped to the slider position.
(function () {
  var slider = document.getElementById("revealSlider");
  var top = document.getElementById("revealTop");
  var handle = document.getElementById("revealHandle");
  if (!slider || !top || !handle) return;

  function paint() {
    var pct = slider.value + "%";
    top.style.width = pct;
    handle.style.left = pct;
  }

  slider.addEventListener("input", paint);
  paint();
})();
