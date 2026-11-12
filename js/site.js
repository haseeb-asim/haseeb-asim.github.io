(function () {
  var root = document.documentElement;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  var nav = document.querySelector("[data-nav]");
  if (nav) {
    var path = location.pathname;
    document.querySelectorAll("[data-nav-link]").forEach(function (link) {
      var href = link.getAttribute("href");
      if (href && href !== "/" && (path === href || path.indexOf(href) === 0)) {
        link.setAttribute("aria-current", "page");
      }
    });
    var onScroll = function () { nav.classList.toggle("is-scrolled", window.scrollY > 8); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  var themeBtn = document.querySelector("[data-theme-toggle]");
  function applyTheme(next) {
    if (next) root.setAttribute("data-theme", next);
    else root.removeAttribute("data-theme");
    try { localStorage.setItem("theme", next || "system"); } catch (err) {}
    if (themeBtn) {
      var dark = root.getAttribute("data-theme") === "dark" || (!root.getAttribute("data-theme") && matchMedia("(prefers-color-scheme: dark)").matches);
      var label = themeBtn.querySelector(".theme-label");
      if (label) label.textContent = dark ? "Light" : "Dark";
      themeBtn.setAttribute("aria-pressed", dark ? "true" : "false");
    }
  }
  if (themeBtn) {
    applyTheme(root.getAttribute("data-theme"));
    themeBtn.addEventListener("click", function () {
      var dark = themeBtn.getAttribute("aria-pressed") === "true";
      applyTheme(dark ? "light" : "dark");
    });
  }

  function paintClock() {
    var text = new Intl.DateTimeFormat("en-US", {
      timeZone: "America/Chicago",
      hour: "numeric",
      minute: "2-digit"
    }).format(new Date());
    document.querySelectorAll("[data-clock]").forEach(function (node) { node.textContent = text; });
  }
  if (document.querySelector("[data-clock]")) {
    paintClock();
    setInterval(paintClock, 30000);
  }

  var progress = document.querySelector(".progress");
  if (progress) {
    var paintProgress = function () {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.transform = "scaleX(" + (max > 0 ? window.scrollY / max : 0) + ")";
    };
    paintProgress();
    window.addEventListener("scroll", paintProgress, { passive: true });
  }

  initCommand();

  var pending = null;
  document.addEventListener("click", function (event) {
    var anchor = event.target.closest && event.target.closest("a[data-vt]");
    pending = anchor || null;
  }, true);

  function slugFrom(pathname) {
    var work = pathname.match(/^\/work\/([^/]+)\/?$/);
    if (work && work[1]) return work[1];
    var concept = pathname.match(/^\/concepts\/([^/]+)\/?$/);
    if (concept) return concept[1];
    return "";
  }
  function namePair(node) {
    if (!node) return;
    var img = node.querySelector("img");
    var title = node.querySelector(".vt-title");
    if (img) img.style.viewTransitionName = "piece-media";
    if (title) title.style.viewTransitionName = "piece-title";
  }
  function arm(vt) {
    if (!vt) return;
    var skip = function () { try { vt.skipTransition(); } catch (err) {} };
    window.addEventListener("pointerdown", skip, { once: true });
    window.addEventListener("keydown", skip, { once: true });
  }
  window.addEventListener("pageswap", function (event) {
    if (!event.viewTransition) return;
    arm(event.viewTransition);
    if (reduced || !pending) { event.viewTransition.skipTransition(); return; }
    if (event.activation) {
      var slug = slugFrom(new URL(event.activation.entry.url).pathname);
      if (pending.getAttribute("data-vt") !== slug) return;
    }
    namePair(pending);
  });
  window.addEventListener("pagereveal", function (event) {
    if (!event.viewTransition) return;
    arm(event.viewTransition);
    if (reduced) { event.viewTransition.skipTransition(); return; }
    var hero = document.querySelector("[data-vt-hero]");
    var img = hero && (hero.tagName === "IMG" ? hero : hero.querySelector("img"));
    if (img) img.style.viewTransitionName = "piece-media";
    var title = document.querySelector("h1.vt-title");
    if (title) title.style.viewTransitionName = "piece-title";
  });

  if (reduced) {
    document.querySelectorAll(".story-steps li, .loop-line, .loop-answer, .loop-steps li").forEach(function (node) {
      node.classList.add("is-on");
    });
    return;
  }

  if (fine) {
    initCursor();
    initPreview();
    initMagnetic();
  }
  initAgent();
  initPipes();
  initStory();
  initGallery();
  initMobileReel();

  window.addEventListener("load", function () {
    if (root.classList.contains("rich")) {
      loadScript("/js/vendor/gsap.min.js")
        .then(function () { return loadScript("/js/vendor/ScrollTrigger.min.js"); })
        .then(function () { return loadScript("/js/vendor/lenis.min.js"); })
        .then(initRich)
        .catch(function () {});
      if (document.querySelector("[data-field]")) loadScript("/js/field.js").catch(function () {});
    }
  });

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var script = document.createElement("script");
      script.src = src;
      script.onload = resolve;
      script.onerror = reject;
      document.body.appendChild(script);
    });
  }

  function initRich() {
    if (!window.gsap || !window.ScrollTrigger) return;
    gsap.registerPlugin(ScrollTrigger);
    var lenis = null;
    if (window.Lenis) {
      lenis = new Lenis({ duration: 1.05, smoothWheel: true, wheelMultiplier: 0.9 });
      lenis.on("scroll", ScrollTrigger.update);
      gsap.ticker.add(function (time) { lenis.raf(time * 1000); });
      gsap.ticker.lagSmoothing(0);
      document.addEventListener("click", function (event) {
        var anchor = event.target.closest && event.target.closest('a[href^="#"]');
        if (!anchor) return;
        var id = anchor.getAttribute("href").slice(1);
        var target = id && document.getElementById(id);
        if (!target) return;
        event.preventDefault();
        lenis.scrollTo(target, { offset: -72 });
      });
    }
    initReel();
    document.querySelectorAll("[data-story]").forEach(function (story) {
      var img = story.querySelector(".stage img");
      if (!img) return;
      gsap.fromTo(img, { scale: 0.94, rotateX: 2.2 }, {
        scale: 1.045,
        rotateX: 0,
        ease: "none",
        scrollTrigger: { trigger: story, start: "top bottom", end: "bottom top", scrub: true }
      });
    });
    ScrollTrigger.refresh();
  }

  function preloadReel(items) {
    items.forEach(function (item) {
      var img = item.querySelector("img");
      if (!img) return;
      img.loading = "eager";
      var pre = new Image();
      var srcset = img.getAttribute("srcset");
      if (srcset) pre.srcset = srcset;
      pre.src = img.getAttribute("src");
    });
  }

  function initReel() {
    var reel = document.querySelector("[data-reel]");
    var pin = reel && reel.querySelector(".reel-sticky");
    if (!reel || !pin || !window.ScrollTrigger) return;
    var items = Array.prototype.slice.call(reel.querySelectorAll(".reel-item"));
    if (!items.length) return;
    preloadReel(items);
    var bar = reel.querySelector(".reel-bar span");
    var count = reel.querySelector(".reel-count");
    var n = items.length;
    function weight(dist) {
      if (dist <= 0.34) return 1;
      if (dist >= 0.7) return 0;
      return 1 - (dist - 0.34) / 0.36;
    }
    function textWeight(dist) {
      if (dist <= 0.45) return 1;
      if (dist >= 0.62) return 0;
      return 1 - (dist - 0.45) / 0.17;
    }
    ScrollTrigger.create({
      trigger: pin,
      start: "top top",
      end: function () { return "+=" + window.innerHeight * n; },
      pin: true,
      anticipatePin: 1,
      scrub: 0.35,
      snap: {
        snapTo: function (progress) {
          var i = Math.round(progress * (n - 1));
          return i / (n - 1);
        },
        duration: { min: 0.2, max: 0.5 },
        delay: 0.06,
        ease: "power2.inOut"
      },
      onUpdate: function (self) {
        var pos = self.progress * (n - 1);
        var nearest = 0;
        var best = 99;
        items.forEach(function (item, i) {
          var dist = Math.abs(pos - i);
          var figOpacity = weight(dist);
          var copyOpacity = textWeight(dist);
          var fig = item.querySelector(".reel-fig");
          var copy = item.querySelector(".reel-copy");
          if (fig) fig.style.opacity = String(figOpacity);
          if (copy) copy.style.opacity = String(copyOpacity);
          item.style.visibility = figOpacity > 0.02 ? "visible" : "hidden";
          item.style.pointerEvents = dist < 0.45 ? "auto" : "none";
          item.classList.toggle("is-on", dist < 0.45);
          if (dist < best) { best = dist; nearest = i; }
          var img = item.querySelector("img");
          if (img && figOpacity > 0.02) {
            var shift = (pos - i) * 14;
            img.style.transform = "translate3d(" + shift.toFixed(1) + "px,0,0) scale(" + (1.02 - Math.min(dist, 1) * 0.03).toFixed(3) + ")";
          }
        });
        if (bar) bar.style.transform = "scaleX(" + ((nearest + 1) / n).toFixed(4) + ")";
        if (count) count.textContent = String(nearest + 1).padStart(2, "0") + " / " + String(n).padStart(2, "0");
        var live = reel.querySelector("[role='progressbar']");
        if (live) live.setAttribute("aria-valuenow", String(nearest + 1));
      }
    });
  }

  function initMobileReel() {
    if (root.classList.contains("rich")) return;
    var reel = document.querySelector("[data-reel]");
    if (!reel) return;
    var track = reel.querySelector(".reel-track");
    var items = track ? track.querySelectorAll(".reel-item") : [];
    var bar = reel.querySelector(".reel-bar span");
    var count = reel.querySelector(".reel-count");
    if (!track || items.length < 2) return;
    var paint = function () {
      var box = items[0].getBoundingClientRect().width + 12;
      var idx = Math.max(0, Math.min(items.length - 1, Math.round(track.scrollLeft / box)));
      items.forEach(function (item, i) { item.classList.toggle("is-on", i === idx); });
      if (bar) bar.style.transform = "scaleX(" + ((idx + 1) / items.length) + ")";
      if (count) count.textContent = String(idx + 1).padStart(2, "0") + " / " + String(items.length).padStart(2, "0");
    };
    track.addEventListener("scroll", paint, { passive: true });
    paint();
  }

  function initStory() {
    var story = document.querySelector("[data-story]");
    var items = document.querySelectorAll(".story-steps li");
    if (!items.length) return;
    var img = story && story.querySelector(".stage img");
    function focus(index) {
      items.forEach(function (item, i) { item.classList.toggle("is-on", i === index); });
      if (!img) return;
      var scale = 1 + index * 0.035;
      var shift = (index - 1) * 10;
      img.style.transform = "scale(" + scale.toFixed(3) + ") translate3d(0," + shift + "px,0)";
    }
    if (!("IntersectionObserver" in window)) { focus(0); return; }
    var active = 0;
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var index = Array.prototype.indexOf.call(items, entry.target);
        if (index > -1 && index !== active) { active = index; focus(index); }
      });
    }, { rootMargin: "-35% 0px -35% 0px", threshold: 0.2 });
    items.forEach(function (item) { observer.observe(item); });
    focus(0);
  }

  function initPipes() {
    document.querySelectorAll("[data-pipe]").forEach(function (pipe) {
      if (!("IntersectionObserver" in window)) { pipe.classList.add("is-in"); return; }
      var observer = new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting) {
          pipe.classList.add("is-in");
          observer.disconnect();
        }
      }, { threshold: 0.35 });
      observer.observe(pipe);
    });
  }

  function initAgent() {
    var loop = document.querySelector("[data-loop]");
    if (!loop) return;
    var lines = Array.prototype.slice.call(loop.querySelectorAll("[data-out]"));
    var steps = Array.prototype.slice.call(loop.querySelectorAll("[data-step]"));
    var timer = null;
    var fill = loop.querySelector(".loop-fill");
    var typed = loop.querySelector("[data-typed]");
    var typeTimer = null;
    function typeAnswer() {
      if (!typed) return;
      window.clearInterval(typeTimer);
      var full = typed.getAttribute("data-typed") || "";
      var i = 0;
      typed.textContent = "";
      typeTimer = window.setInterval(function () {
        i += 1;
        typed.textContent = full.slice(0, i);
        if (i >= full.length) window.clearInterval(typeTimer);
      }, 16);
    }
    function play() {
      window.clearTimeout(timer);
      window.clearInterval(typeTimer);
      loop.classList.add("is-armed");
      lines.forEach(function (line) { line.classList.remove("is-on"); });
      steps.forEach(function (step) { step.classList.remove("is-on"); });
      if (fill) fill.style.height = "0px";
      if (typed) typed.textContent = "";
      var index = 0;
      var tick = function () {
        if (index >= lines.length) return;
        lines[index].classList.add("is-on");
        var id = lines[index].getAttribute("data-out");
        steps.forEach(function (step) {
          step.classList.toggle("is-on", step.getAttribute("data-step") === id);
        });
        if (fill && steps.length) {
          var current = steps.filter(function (step) { return step.getAttribute("data-step") === id; })[0];
          if (current) fill.style.height = Math.max(0, current.offsetTop + 8) + "px";
        }
        if (id === "5") typeAnswer();
        index += 1;
        timer = window.setTimeout(tick, 720);
      };
      tick();
    }
    var replay = loop.querySelector("[data-replay]");
    if (replay) replay.addEventListener("click", play);
    if (!("IntersectionObserver" in window)) { play(); return; }
    var once = new IntersectionObserver(function (entries) {
      if (!entries[0].isIntersecting) return;
      play();
      once.disconnect();
    }, { threshold: 0.4 });
    once.observe(loop);
  }

  function initGallery() {
    var gallery = document.querySelector("[data-gallery]");
    if (!gallery || reduced) return;
    var track = gallery.querySelector(".gallery-track");
    if (!track) return;
    var x = 0;
    var vx = 0;
    var dragging = false;
    var moved = 0;
    var suppress = false;
    var lastX = 0;
    var lastT = 0;
    var frame = 0;

    function limits() {
      return Math.min(0, gallery.clientWidth - track.scrollWidth);
    }
    function paint() {
      var skew = Math.max(-5, Math.min(5, -vx * 0.09));
      var scale = 1 + Math.min(0.04, Math.abs(vx) / 640);
      track.style.transform = "translate3d(" + x.toFixed(2) + "px,0,0)";
      gallery.style.setProperty("--drag-skew", skew.toFixed(2) + "deg");
      gallery.style.setProperty("--drag-scale", scale.toFixed(3));
    }
    function settle() {
      if (dragging) return;
      var min = limits();
      if (x > 0 || x < min) {
        var dest = x > 0 ? 0 : min;
        x += (dest - x) * 0.14;
        vx *= 0.8;
        if (Math.abs(dest - x) < 0.4) { x = dest; vx = 0; }
      } else {
        x += vx;
        vx *= 0.965;
        if (Math.abs(vx) < 0.12) vx = 0;
      }
      paint();
      if (vx !== 0 || x > 0 || x < min) frame = requestAnimationFrame(settle);
    }
    gallery.addEventListener("pointerdown", function (event) {
      if (event.button !== undefined && event.button !== 0) return;
      dragging = true;
      moved = 0;
      vx = 0;
      lastX = event.clientX;
      lastT = performance.now();
      gallery.classList.add("is-drag");
      gallery.setPointerCapture(event.pointerId);
      cancelAnimationFrame(frame);
    });
    gallery.addEventListener("pointermove", function (event) {
      if (!dragging) return;
      var dx = event.clientX - lastX;
      moved += Math.abs(dx);
      var now = performance.now();
      var dt = Math.max(16, now - lastT);
      vx = dx / dt * 16;
      lastX = event.clientX;
      lastT = now;
      x += dx;
      var min = limits();
      if (x > 0) x *= 0.72;
      if (x < min) x = min + (x - min) * 0.72;
      paint();
    });
    function endDrag() {
      if (!dragging) return;
      dragging = false;
      gallery.classList.remove("is-drag");
      suppress = moved > 8;
      frame = requestAnimationFrame(settle);
    }
    gallery.addEventListener("pointerup", endDrag);
    gallery.addEventListener("pointercancel", endDrag);
    gallery.addEventListener("click", function (event) {
      if (suppress) {
        event.preventDefault();
        event.stopPropagation();
        suppress = false;
      }
    }, true);
    gallery.addEventListener("keydown", function (event) {
      var min = limits();
      if (event.key === "ArrowRight") { x = Math.max(min, x - 180); paint(); }
      if (event.key === "ArrowLeft") { x = Math.min(0, x + 180); paint(); }
    });
    window.addEventListener("resize", function () {
      var min = limits();
      if (x < min) x = min;
      paint();
    });
  }

  function initCursor() {
    var cursor = document.createElement("div");
    cursor.className = "cursor";
    cursor.setAttribute("aria-hidden", "true");
    document.body.appendChild(cursor);
    var x = 0;
    var y = 0;
    var tx = 0;
    var ty = 0;
    var shown = false;
    window.addEventListener("pointermove", function (event) {
      tx = event.clientX;
      ty = event.clientY;
      shown = true;
      var hit = event.target.closest && event.target.closest("[data-cursor]");
      cursor.classList.toggle("is-view", !!hit);
    });
    window.addEventListener("pointerleave", function () { shown = false; cursor.style.opacity = "0"; });
    window.addEventListener("pointerenter", function () { cursor.style.opacity = "1"; });
    function loop() {
      x += (tx - x) * 0.32;
      y += (ty - y) * 0.32;
      if (shown) cursor.style.transform = "translate3d(" + x.toFixed(1) + "px," + y.toFixed(1) + "px,0)";
      requestAnimationFrame(loop);
    }
    requestAnimationFrame(loop);
  }

  function initPreview() {
    var float = document.createElement("div");
    float.className = "float";
    float.innerHTML = '<img alt="" width="960" height="720">';
    document.body.appendChild(float);
    var img = float.querySelector("img");
    var x = 0;
    var y = 0;
    var tx = 0;
    var ty = 0;
    var on = false;
    document.addEventListener("pointermove", function (event) {
      var link = event.target.closest && event.target.closest("[data-preview]");
      tx = event.clientX + 28;
      ty = event.clientY - 40;
      if (!link) { on = false; float.classList.remove("is-on"); return; }
      var src = link.getAttribute("data-preview");
      if (img.getAttribute("src") !== src) img.src = src;
      on = true;
      float.classList.add("is-on");
    });
    function loop() {
      x += (tx - x) * 0.22;
      y += (ty - y) * 0.22;
      if (on) float.style.transform = "translate3d(" + x.toFixed(1) + "px," + y.toFixed(1) + "px,0)";
      requestAnimationFrame(loop);
    }
    requestAnimationFrame(loop);
  }

  function initMagnetic() {
    document.querySelectorAll("[data-magnetic]").forEach(function (el) {
      el.addEventListener("mousemove", function (event) {
        var rect = el.getBoundingClientRect();
        var dx = (event.clientX - (rect.left + rect.width / 2)) / rect.width;
        var dy = (event.clientY - (rect.top + rect.height / 2)) / rect.height;
        el.style.transform = "translate(" + (dx * 5).toFixed(2) + "px," + (dy * 3).toFixed(2) + "px)";
      });
      el.addEventListener("mouseleave", function () { el.style.transform = ""; });
    });
  }

  function initCommand() {
    var dialog = document.querySelector("[data-cmd]");
    var input = document.querySelector("[data-cmd-input]");
    var list = document.querySelector("[data-cmd-list]");
    var source = document.getElementById("cmd-index");
    var openBtn = document.querySelector("[data-command]");
    if (!dialog || !input || !list || !source) return;
    var items = [];
    try { items = JSON.parse(source.textContent); } catch (err) { items = []; }
    var selected = 0;
    var lastFocus = null;

    function render(query) {
      var q = (query || "").trim().toLowerCase();
      var matches = items.filter(function (item) {
        return !q || (item.label + " " + (item.hint || "")).toLowerCase().indexOf(q) !== -1;
      }).slice(0, 8);
      if (selected >= matches.length) selected = 0;
      list.innerHTML = "";
      matches.forEach(function (item, index) {
        var link = document.createElement("a");
        link.href = item.href;
        if (item.href.indexOf("mailto:") === 0) link.rel = "noopener";
        link.setAttribute("aria-selected", index === selected ? "true" : "false");
        var name = document.createElement("span");
        name.textContent = item.label;
        var hint = document.createElement("span");
        hint.className = "hint";
        hint.textContent = item.hint || "";
        link.appendChild(name);
        link.appendChild(hint);
        list.appendChild(link);
      });
      return matches;
    }

    function open() {
      lastFocus = document.activeElement;
      dialog.hidden = false;
      input.value = "";
      selected = 0;
      render("");
      input.focus();
    }
    function close() {
      dialog.hidden = true;
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }
    if (openBtn) openBtn.addEventListener("click", open);
    dialog.addEventListener("click", function (event) { if (event.target === dialog) close(); });
    input.addEventListener("input", function () { selected = 0; render(input.value); });
    document.addEventListener("keydown", function (event) {
      var key = event.key.toLowerCase();
      if ((event.metaKey || event.ctrlKey) && key === "k") {
        event.preventDefault();
        if (dialog.hidden) open(); else close();
        return;
      }
      if (dialog.hidden) return;
      if (event.key === "Escape") { event.preventDefault(); close(); return; }
      var links = list.querySelectorAll("a");
      if (event.key === "ArrowDown") {
        event.preventDefault();
        selected = Math.min(links.length - 1, selected + 1);
        render(input.value);
      } else if (event.key === "ArrowUp") {
        event.preventDefault();
        selected = Math.max(0, selected - 1);
        render(input.value);
      } else if (event.key === "Enter") {
        var current = links[selected];
        if (current) { event.preventDefault(); current.click(); }
      }
    });
  }
})();
