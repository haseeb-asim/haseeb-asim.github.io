(function () {
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var pointer = false;
  var root = document.documentElement;

  document.addEventListener("pointerdown", function () { pointer = true; }, true);
  document.addEventListener("keydown", function () { pointer = false; }, true);

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
    try { localStorage.setItem("theme", next || "system"); } catch (e) {}
    if (themeBtn) {
      var dark = root.getAttribute("data-theme") === "dark" || (!root.getAttribute("data-theme") && matchMedia("(prefers-color-scheme: dark)").matches);
      themeBtn.textContent = dark ? "Light" : "Dark";
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

  function slugFrom(pathname) {
    var work = pathname.match(/^\/work\/([^/]+)\/?$/);
    if (work && work[1] !== "") return work[1];
    var concept = pathname.match(/^\/concepts\/([^/]+)\/?$/);
    if (concept) return concept[1];
    return "";
  }

  var pending = null;
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest && ev.target.closest("a[data-vt]");
    pending = a || null;
  }, true);

  function namePair(rootNode) {
    if (!rootNode) return;
    var img = rootNode.querySelector("img");
    var title = rootNode.querySelector(".vt-title");
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
    if (reduced || !pointer || !pending) {
      event.viewTransition.skipTransition();
      return;
    }
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
})();
