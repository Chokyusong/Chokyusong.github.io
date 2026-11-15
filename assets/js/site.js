/* 조규송 포트폴리오 — 움직임 모음.
   GSAP·ScrollTrigger·Lenis가 없거나 '동작 줄이기'를 켠 사람에게는 움직임 없이 내용이 그대로 보인다. */
(function () {
  "use strict";
  var root = document.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var G = window.gsap, ST = window.ScrollTrigger;
  var anim = !!(G && ST) && !reduce;
  if (!anim) root.classList.remove("anim", "page-enter");
  else G.registerPlugin(ST);
  root.classList.add("anim-ready");

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var onView = function (el, fn, opt) {
    if (!("IntersectionObserver" in window)) { fn(el, true); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { fn(e.target, e.isIntersecting, io); });
    }, opt || { rootMargin: "0px 0px -10% 0px", threshold: 0.15 });
    io.observe(el);
    return io;
  };

  /* ---------- 부드러운 스크롤 ---------- */
  var lenis = null;
  if (anim && window.Lenis) {
    lenis = new window.Lenis({ lerp: 0.1, smoothWheel: true, wheelMultiplier: 1, prevent: function (n) { return n.closest && n.closest(".lb, .reel-track"); } });
    lenis.on("scroll", ST.update);
    G.ticker.add(function (t) { lenis.raf(t * 1000); });
    G.ticker.lagSmoothing(0);
  }
  window.__lenis = lenis;
  $$('a[href^="#"]').forEach(function (a) {
    a.addEventListener("click", function (e) {
      var id = a.getAttribute("href");
      if (id.length < 2 || a.hasAttribute("data-filter-go")) return;
      var t = document.querySelector(id);
      if (!t) return;
      e.preventDefault();
      if (lenis) lenis.scrollTo(t, { offset: -20, duration: 1.4 });
      else t.scrollIntoView({ behavior: reduce ? "auto" : "smooth" });
      history.replaceState(null, "", id);
    });
  });

  /* ---------- 머리 메뉴: 내려가면 숨고 올라오면 보임 ---------- */
  var nav = $(".nav");
  if (nav) {
    var lastY = 0;
    var navTick = function () {
      var y = window.scrollY;
      nav.classList.toggle("is-solid", y > 40);
      nav.classList.toggle("is-hidden", y > 400 && y > lastY + 2 && !document.body.classList.contains("lb-open"));
      if (y < lastY - 2) nav.classList.remove("is-hidden");
      lastY = y;
    };
    window.addEventListener("scroll", navTick, { passive: true });
    navTick();
  }
  var clock = $("[data-clock]");
  if (clock) {
    var tick = function () {
      try {
        clock.textContent = new Intl.DateTimeFormat("ko-KR", { timeZone: "Asia/Seoul", hour: "2-digit", minute: "2-digit", hour12: false }).format(new Date());
      } catch (e) { clock.textContent = ""; }
    };
    tick(); setInterval(tick, 20000);
  }

  /* ---------- 커서 ---------- */
  if (fine && !reduce) {
    var cur = document.createElement("div");
    cur.className = "cursor";
    cur.setAttribute("aria-hidden", "true");
    cur.innerHTML = '<div class="cursor-ring"><span></span></div><div class="cursor-dot"></div>';
    document.body.appendChild(cur);
    root.classList.add("has-cursor");
    var ring = cur.firstChild, dot = cur.lastChild, label = ring.firstChild;
    var mx = -100, my = -100, rx = -100, ry = -100;
    window.addEventListener("pointermove", function (e) {
      mx = e.clientX; my = e.clientY;
      cur.classList.remove("is-hidden");
      var t = e.target.closest ? e.target.closest("[data-cursor], a, button, input[type=range], label") : null;
      var lab = t && t.getAttribute("data-cursor");
      cur.classList.toggle("is-label", !!lab);
      cur.classList.toggle("is-link", !!t && !lab);
      if (lab) label.textContent = lab;
    }, { passive: true });
    document.addEventListener("pointerleave", function () { cur.classList.add("is-hidden"); });
    window.addEventListener("blur", function () { cur.classList.add("is-hidden"); });
    $$("iframe").forEach(function (f) {
      f.addEventListener("pointerenter", function () { cur.classList.add("is-hidden"); });
    });
    (function loop() {
      rx += (mx - rx) * 0.18; ry += (my - ry) * 0.18;
      dot.style.transform = "translate3d(" + mx + "px," + my + "px,0)";
      ring.style.transform = "translate3d(" + rx + "px," + ry + "px,0)";
      requestAnimationFrame(loop);
    })();
  }

  /* ---------- 첫 화면: 커서에 반응하는 LED 점 화면 ---------- */
  var canvas = $(".hero-canvas");
  if (canvas && canvas.getContext) heroField(canvas);

  function heroField(cv) {
    var ctx = cv.getContext("2d");
    var w, h, gap, cols, rows, mask, dpr;
    var mouse = { x: -9999, y: -9999, tx: -9999, ty: -9999 };
    var rings = [];
    var running = false, visible = true, t0 = performance.now();
    var word = cv.getAttribute("data-word") || "ON AIR";

    function build() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = cv.clientWidth; h = cv.clientHeight;
      if (!w || !h) return;
      cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      gap = w < 700 ? 11 : 14;
      cols = Math.ceil(w / gap) + 1; rows = Math.ceil(h / gap) + 1;
      var off = document.createElement("canvas");
      off.width = cols; off.height = rows;
      var o = off.getContext("2d");
      var narrow = w < 960;
      var fs = Math.floor(rows * (narrow ? 0.16 : 0.26));
      o.font = "800 " + fs + "px 'Pretendard Variable', Pretendard, sans-serif";
      var tw = o.measureText(word).width;
      var maxw = narrow ? cols * 0.86 : cols * 0.4;
      if (tw > maxw) { fs = Math.floor(fs * maxw / tw); o.font = "800 " + fs + "px 'Pretendard Variable', Pretendard, sans-serif"; tw = o.measureText(word).width; }
      o.fillStyle = "#fff"; o.textBaseline = "middle";
      var x = narrow ? (cols - tw) / 2 : cols - tw - cols * 0.05;
      var y = narrow ? rows * 0.2 : rows * 0.25;
      o.fillText(word, x, y);
      var d = o.getImageData(0, 0, cols, rows).data;
      mask = new Float32Array(cols * rows);
      for (var i = 0; i < mask.length; i++) mask[i] = d[i * 4 + 3] / 255;
      if (!running) draw(performance.now());
    }

    function draw(now) {
      var t = (now - t0) / 1000;
      mouse.x += (mouse.tx - mouse.x) * 0.14;
      mouse.y += (mouse.ty - mouse.y) * 0.14;
      ctx.clearRect(0, 0, w, h);
      var R = w < 700 ? 120 : 190, R2 = R * R;
      for (var k = rings.length - 1; k >= 0; k--) if (t - rings[k].t > 2.4) rings.splice(k, 1);
      for (var r = 0; r < rows; r++) {
        var y = r * gap + gap / 2;
        for (var c = 0; c < cols; c++) {
          var x = c * gap + gap / 2;
          var m = mask[r * cols + c];
          var n = Math.sin(c * 0.16 + t * 0.8) * Math.cos(r * 0.2 - t * 0.6) + Math.sin((c + r) * 0.05 - t * 0.4);
          var a = 0.045 + (n + 2) * 0.022;
          var hot = 0;
          if (m > 0.35) { hot = 0.5 + 0.35 * (0.5 + 0.5 * Math.sin(t * 1.6 + c * 0.22 - r * 0.15)); }
          var dx = x - mouse.x, dy = y - mouse.y, d2 = dx * dx + dy * dy;
          if (d2 < R2) { var kk = 1 - Math.sqrt(d2) / R; hot = Math.max(hot, kk * kk * 0.95); }
          for (var q = 0; q < rings.length; q++) {
            var rg = rings[q], age = t - rg.t, rr = age * 520;
            var ex = x - rg.x, ey = y - rg.y, dist = Math.sqrt(ex * ex + ey * ey), band = Math.abs(dist - rr);
            if (band < 30) hot = Math.max(hot, (1 - band / 30) * 0.85 * (1 - age / 2.4));
          }
          if (hot > 0.02) {
            ctx.globalAlpha = Math.min(1, hot + a);
            ctx.fillStyle = "#45c6d6";
            var s = 1.6 + hot * 1.9;
            ctx.fillRect(x - s / 2, y - s / 2, s, s);
          } else {
            ctx.globalAlpha = a;
            ctx.fillStyle = "#cfe3e8";
            ctx.fillRect(x - 0.8, y - 0.8, 1.6, 1.6);
          }
        }
      }
      ctx.globalAlpha = 1;
    }

    function loop(now) {
      if (!running) return;
      draw(now);
      requestAnimationFrame(loop);
    }
    function start() { if (running || reduce) return; running = true; requestAnimationFrame(loop); }
    function stop() { running = false; }

    function spawn(x, y) { rings.push({ x: x, y: y, t: (performance.now() - t0) / 1000 }); }
    var auto = setInterval(function () {
      if (!running || !mask) return;
      for (var tries = 0; tries < 40; tries++) {
        var i = Math.floor(Math.random() * mask.length);
        if (mask[i] > 0.5) { spawn((i % cols) * gap, Math.floor(i / cols) * gap); return; }
      }
    }, 2600);

    window.addEventListener("pointermove", function (e) {
      var b = cv.getBoundingClientRect();
      mouse.tx = e.clientX - b.left; mouse.ty = e.clientY - b.top;
      if (mouse.x < -999) { mouse.x = mouse.tx; mouse.y = mouse.ty; }
    }, { passive: true });
    cv.parentElement.addEventListener("pointerdown", function (e) {
      if (e.target.closest("a, button")) return;
      var b = cv.getBoundingClientRect();
      spawn(e.clientX - b.left, e.clientY - b.top);
    });
    var rt;
    window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(build, 150); });
    onView(cv, function (_, inView) { visible = inView; if (inView && !document.hidden) start(); else stop(); }, { threshold: 0 });
    document.addEventListener("visibilitychange", function () { if (document.hidden) stop(); else if (visible) start(); });
    build();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(build);
    if (reduce) draw(performance.now());
    else start();
    void auto;
  }

  /* ---------- 글자 바꿔 끼우기 (기계 글자처럼 흩어졌다 맞춰짐) ---------- */
  var glyphs = "ABCDEFGHJKLMNPQRSTUVWXYZ0123456789#%&*+=<>/";
  function scramble(el) {
    var final = el.getAttribute("data-scramble") || el.textContent;
    el.setAttribute("data-scramble", final);
    if (reduce) { el.textContent = final; return; }
    var frame = 0, total = 22;
    (function step() {
      var out = "";
      for (var i = 0; i < final.length; i++) {
        var ch = final[i];
        if (ch === " " || ch === "." || ch === ",") { out += ch; continue; }
        out += frame / total > i / final.length ? ch : glyphs[(Math.random() * glyphs.length) | 0];
      }
      el.textContent = out;
      if (++frame <= total) requestAnimationFrame(step);
      else el.textContent = final;
    })();
  }
  $$("[data-scramble]").forEach(function (el) {
    onView(el, function (t, inView, io) { if (inView) { scramble(t); io.unobserve(t); } });
  });

  /* ---------- 숫자 세기 ---------- */
  $$("[data-count]").forEach(function (el) {
    var target = parseFloat(el.getAttribute("data-count"));
    var fmt = function (v) { return Math.round(v).toLocaleString("ko-KR"); };
    if (!anim) { el.textContent = fmt(target); return; }
    el.textContent = "0";
    onView(el, function (t, inView, io) {
      if (!inView) return;
      io.unobserve(t);
      var o = { v: 0 };
      G.to(o, { v: target, duration: 2, ease: "power3.out", onUpdate: function () { t.textContent = fmt(o.v); } });
    });
  });

  /* ---------- 나타나기 ---------- */
  if (anim) {
    var revealIO = new IntersectionObserver(function (es) {
      var els = [];
      es.forEach(function (en) { if (en.isIntersecting) { els.push(en.target); revealIO.unobserve(en.target); } });
      if (els.length) G.to(els, { opacity: 1, y: 0, duration: 1.1, ease: "expo.out", stagger: 0.08, overwrite: true });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0 });
    $$("[data-reveal]").forEach(function (el) { revealIO.observe(el); });
    $$("[data-lines]").forEach(function (el) {
      if (el.hasAttribute("data-hero")) return;
      G.to($$(".line-mask > span", el), {
        y: 0, yPercent: 0, duration: 1.2, ease: "expo.out", stagger: 0.09,
        scrollTrigger: { trigger: el, start: "top 86%", once: true }
      });
    });
    $$("[data-clip]").forEach(function (el) {
      var img = el.querySelector("img, video");
      var tl = G.timeline({ scrollTrigger: { trigger: el, start: "top 85%", once: true } });
      tl.to(el, { clipPath: "inset(0% 0% 0% 0% round 14px)", duration: 1.4, ease: "expo.out" });
      if (img) tl.from(img, { scale: 1.18, duration: 1.8, ease: "expo.out" }, 0);
    });
    $$("[data-parallax]").forEach(function (el) {
      var amt = parseFloat(el.getAttribute("data-parallax")) || 10;
      G.fromTo(el, { yPercent: -amt / 2 }, { yPercent: amt / 2, ease: "none", scrollTrigger: { trigger: el.parentElement, start: "top bottom", end: "bottom top", scrub: true } });
    });

    // 첫 화면 들어오기
    var hero = $("[data-hero]");
    if (hero) {
      var tl = G.timeline({ delay: root.classList.contains("page-enter") ? 0.55 : 0.15 });
      tl.to($$(".line-mask > span", hero), { y: 0, yPercent: 0, duration: 1.5, ease: "expo.out", stagger: 0.11 });
      tl.to($$("[data-hero-fade]"), { opacity: 1, y: 0, duration: 1.1, ease: "expo.out", stagger: 0.08 }, "-=1.0");
    }
  }

  /* ---------- 흐르는 띠 (스크롤 속도에 따라 빨라짐) ---------- */
  $$(".marquee-track").forEach(function (track) {
    if (reduce) return;
    var x = 0, base = parseFloat(track.getAttribute("data-speed")) || 0.6, dir = track.hasAttribute("data-reverse") ? 1 : -1;
    var half = 0;
    var measure = function () { half = track.scrollWidth / 2; };
    measure(); window.addEventListener("resize", measure);
    (function loop() {
      var v = lenis ? Math.min(Math.abs(lenis.velocity || 0), 40) : 0;
      x += dir * (base + v * 0.25);
      if (half) { if (x <= -half) x += half; if (x > 0) x -= half; }
      track.style.transform = "translate3d(" + x + "px,0,0)";
      requestAnimationFrame(loop);
    })();
  });

  /* ---------- AutoLed: 스크롤에 맞춰 화면이 바뀜 ---------- */
  $$("[data-show]").forEach(function (sec) {
    var steps = $$(".show-step", sec), imgs = $$(".show-stage img", sec), bars = $$(".show-progress b", sec);
    var n = steps.length, cur = -1;
    var set = function (i) {
      if (i === cur) return; cur = i;
      steps.forEach(function (s, k) { s.classList.toggle("on", k === i); });
      imgs.forEach(function (s, k) { s.classList.toggle("on", k === i); });
      var lab = $("[data-show-label]", sec);
      if (lab && steps[i]) lab.textContent = steps[i].getAttribute("data-label") || "";
    };
    set(0);
    if (!ST) return;
    var mm = window.matchMedia("(min-width: 1024px)");
    ST.create({
      trigger: sec, start: "top top", end: "bottom bottom",
      onUpdate: function (self) {
        if (!mm.matches) return;
        var p = self.progress * n;
        set(Math.min(n - 1, Math.floor(p)));
        bars.forEach(function (b, k) { b.style.transform = "scaleX(" + Math.max(0, Math.min(1, p - k)) + ")"; });
      }
    });
  });

  /* ---------- 움직이는 시안 창 ---------- */
  $$("[data-live]").forEach(function (box) {
    var frame = $(".live-frame", box), ifr = $("iframe", box), url = $(".browser-url", box);
    var size = { w: 1440, h: 900 };
    var current = box.getAttribute("data-live");
    var fit = function () {
      var phone = size.w < 600;
      frame.style.width = phone ? "min(100%, 360px)" : "100%";
      var bw = frame.clientWidth, s = bw / size.w;
      ifr.style.width = size.w + "px"; ifr.style.height = size.h + "px";
      ifr.style.transform = "scale(" + s + ")";
      frame.style.height = Math.round(size.h * s) + "px";
    };
    var load = function () {
      if (ifr.getAttribute("src") !== current) ifr.setAttribute("src", current);
      frame.classList.add("is-loaded");
      if (url) url.textContent = box.getAttribute("data-host") + current.split("/").pop();
    };
    fit();
    window.addEventListener("resize", fit);
    if (window.matchMedia("(max-width: 599px)").matches) { size = { w: 390, h: 844 }; fit(); $$("[data-device]", box).forEach(function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-device") === "mobile")); }); }
    onView(box, function (t, inView, io) { if (inView) { load(); io.unobserve(t); } }, { rootMargin: "300px 0px", threshold: 0 });
    $$("[data-page]", box).forEach(function (b) {
      b.addEventListener("click", function () {
        current = b.getAttribute("data-page");
        $$("[data-page]", box).forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
        load();
      });
    });
    $$("[data-device]", box).forEach(function (b) {
      b.addEventListener("click", function () {
        size = b.getAttribute("data-device") === "mobile" ? { w: 390, h: 844 } : { w: 1440, h: 900 };
        $$("[data-device]", box).forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
        fit();
        if (ifr.getAttribute("src")) { ifr.setAttribute("src", "about:blank"); setTimeout(load, 30); }
      });
    });
    var cover = $(".live-cover", box);
    if (cover) cover.addEventListener("click", load);
    var shield = $(".live-shield", box);
    if (shield) {
      shield.addEventListener("click", function () { load(); frame.classList.add("is-active"); });
      frame.addEventListener("pointerleave", function (e) { if (e.pointerType === "mouse") frame.classList.remove("is-active"); });
    }
  });

  /* ---------- 작업 목록: 마우스를 따라다니는 미리보기 ---------- */
  var pv = $(".hover-preview");
  if (pv && fine) {
    var px = 0, py = 0, tx = 0, ty = 0, on = false;
    $$(".work-row").forEach(function (row) {
      var key = row.getAttribute("data-pv");
      row.addEventListener("pointerenter", function () {
        on = true; pv.classList.add("on");
        $$("[data-pv-item]", pv).forEach(function (it) { it.classList.toggle("on", it.getAttribute("data-pv-item") === key); });
      });
      row.addEventListener("pointerleave", function () { on = false; pv.classList.remove("on"); });
    });
    window.addEventListener("pointermove", function (e) { tx = e.clientX; ty = e.clientY; }, { passive: true });
    (function loop() {
      px += (tx - px) * 0.12; py += (ty - py) * 0.12;
      var rot = Math.max(-8, Math.min(8, (tx - px) * 0.05));
      pv.style.transform = "translate3d(" + (px + 28) + "px," + (py - 140) + "px,0) rotate(" + rot + "deg)" + (on ? "" : " scale(.85)");
      requestAnimationFrame(loop);
    })();
  }

  /* ---------- 작업 목록: 분류 탭 ---------- */
  var works = $("[data-works]");
  function filterWorks(cat) {
    if (!works) return;
    $$(".work-tabs button").forEach(function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-filter") === cat)); });
    works.classList.toggle("is-filtering", cat !== "all");
    $$(".work-row, .work-group", works).forEach(function (r) {
      r.hidden = cat !== "all" && r.getAttribute("data-cat") !== cat;
      if (!r.hidden) { r.style.opacity = ""; r.style.transform = ""; r.style.visibility = ""; }
    });
    if (ST) requestAnimationFrame(function () { ST.refresh(); });
  }
  $$(".work-tabs button").forEach(function (b) {
    b.addEventListener("click", function () { filterWorks(b.getAttribute("data-filter")); });
  });
  $$("[data-filter-go]").forEach(function (a) {
    a.addEventListener("click", function (e) {
      e.preventDefault();
      filterWorks(a.getAttribute("data-filter-go"));
      var t = document.getElementById("works");
      // 거른 뒤 자리 계산(ScrollTrigger)이 끝난 다음에 내려간다
      requestAnimationFrame(function () { requestAnimationFrame(function () {
        if (lenis) { lenis.resize(); lenis.scrollTo(t, { offset: -20, duration: 1.2 }); }
        else t.scrollIntoView({ behavior: reduce ? "auto" : "smooth" });
      }); });
    });
  });

  /* ---------- 모션 영상 띠: 가로로 흐름 ---------- */
  var reel = $("[data-reel]");
  if (reel && anim) {
    var track = $(".reel-track", reel);
    var mmr = window.matchMedia("(min-width: 1024px)");
    if (mmr.matches) {
      var dist = function () { return Math.max(0, track.scrollWidth - window.innerWidth); };
      G.to(track, {
        x: function () { return -dist(); }, ease: "none",
        scrollTrigger: { trigger: reel, start: "top top", end: function () { return "+=" + dist(); }, pin: true, scrub: 0.8, invalidateOnRefresh: true, anticipatePin: 1 }
      });
    }
  }
  // 보이는 영상만 재생
  $$("video[data-autoplay]").forEach(function (v) {
    if (reduce) return;
    onView(v, function (t, inView) {
      if (inView) {
        if (!t.getAttribute("src") && t.getAttribute("data-src")) t.setAttribute("src", t.getAttribute("data-src"));
        var p = t.play(); if (p && p.catch) p.catch(function () {});
      } else t.pause();
    }, { threshold: 0.2 });
  });

  /* ---------- 연혁 선 그리기 ---------- */
  $$(".tl").forEach(function (tl) {
    var b = $(".tl-line b", tl);
    if (!b || !anim) return;
    G.to(b, { scaleY: 1, ease: "none", scrollTrigger: { trigger: tl, start: "top 75%", end: "bottom 60%", scrub: true } });
  });
  $$(".flow").forEach(function (fl) {
    var b = $(".flow-bar b", fl.parentElement);
    if (!b || !anim) return;
    G.to(b, { scaleX: 1, ease: "none", scrollTrigger: { trigger: fl, start: "top 80%", end: "bottom 50%", scrub: true } });
  });
  $$(".perf").forEach(function (pf) {
    if (!anim) return;
    G.to($$(".perf-bar i b", pf), { scaleX: 1, duration: 1.6, ease: "expo.out", stagger: 0.12, scrollTrigger: { trigger: pf, start: "top 80%", once: true } });
  });

  /* ---------- 칸 위 빛 ---------- */
  $$(".how-item").forEach(function (el) {
    el.addEventListener("pointermove", function (e) {
      var b = el.getBoundingClientRect();
      el.style.setProperty("--mx", e.clientX - b.left + "px");
      el.style.setProperty("--my", e.clientY - b.top + "px");
    });
  });

  /* ---------- 자석 버튼 ---------- */
  if (fine && !reduce) {
    $$("[data-magnet]").forEach(function (el) {
      var strength = parseFloat(el.getAttribute("data-magnet")) || 0.35;
      el.addEventListener("pointermove", function (e) {
        var b = el.getBoundingClientRect();
        var x = (e.clientX - b.left - b.width / 2) * strength, y = (e.clientY - b.top - b.height / 2) * strength;
        el.style.transform = "translate(" + x + "px," + y + "px)";
      });
      el.addEventListener("pointerleave", function () {
        el.style.transition = "transform .6s cubic-bezier(.22,1,.36,1)";
        el.style.transform = "";
        setTimeout(function () { el.style.transition = ""; }, 600);
      });
    });
  }

  /* ---------- 사진 확대 보기 ---------- */
  var lb = null, lbItems = [], lbIdx = 0, lbLast = null;
  function buildLb() {
    lb = document.createElement("div");
    lb.className = "lb";
    lb.setAttribute("role", "dialog");
    lb.setAttribute("aria-modal", "true");
    lb.setAttribute("aria-label", "사진 크게 보기");
    lb.innerHTML = '<div class="lb-stage"><img alt=""><button class="lb-prev" aria-label="이전 사진"><i class="ph ph-arrow-left"></i></button><button class="lb-next" aria-label="다음 사진"><i class="ph ph-arrow-right"></i></button><button class="lb-x" aria-label="닫기"><i class="ph ph-x"></i></button></div><div class="lb-cap"><p></p><span></span></div>';
    document.body.appendChild(lb);
    $(".lb-x", lb).addEventListener("click", closeLb);
    $(".lb-prev", lb).addEventListener("click", function () { showLb(lbIdx - 1); });
    $(".lb-next", lb).addEventListener("click", function () { showLb(lbIdx + 1); });
    $(".lb-stage", lb).addEventListener("click", function (e) { if (e.target === e.currentTarget) closeLb(); });
    var sx = null;
    lb.addEventListener("touchstart", function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener("touchend", function (e) {
      if (sx === null) return;
      var dx = e.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 50) showLb(lbIdx + (dx < 0 ? 1 : -1));
      sx = null;
    });
    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("open")) return;
      if (e.key === "Escape") closeLb();
      if (e.key === "ArrowRight") showLb(lbIdx + 1);
      if (e.key === "ArrowLeft") showLb(lbIdx - 1);
    });
  }
  function showLb(i) {
    lbIdx = (i + lbItems.length) % lbItems.length;
    var it = lbItems[lbIdx];
    var img = $(".lb-stage img", lb);
    img.src = it.getAttribute("data-full");
    img.alt = it.querySelector("img") ? it.querySelector("img").alt : "";
    $(".lb-cap p", lb).textContent = it.getAttribute("data-cap") || "";
    $(".lb-cap span", lb).textContent = (lbIdx + 1) + " / " + lbItems.length;
    if (anim) G.fromTo(img, { opacity: 0, scale: 0.97 }, { opacity: 1, scale: 1, duration: 0.5, ease: "expo.out" });
  }
  function closeLb() {
    lb.classList.remove("open");
    document.body.classList.remove("lb-open");
    if (lenis) lenis.start();
    if (lbLast) lbLast.focus();
  }
  $$("[data-lb]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!lb) buildLb();
      var group = btn.getAttribute("data-lb");
      lbItems = $$('[data-lb="' + group + '"]');
      lbLast = btn;
      lb.classList.add("open");
      document.body.classList.add("lb-open");
      if (lenis) lenis.stop();
      showLb(lbItems.indexOf(btn));
      $(".lb-x", lb).focus();
    });
  });

  /* ---------- 유튜브: 누를 때만 불러오기 ---------- */
  $$("[data-yt]").forEach(function (box) {
    var id = box.getAttribute("data-yt");
    var img = $("img", box);
    if (img) img.addEventListener("error", function once() { img.removeEventListener("error", once); img.src = "https://i.ytimg.com/vi/" + id + "/hqdefault.jpg"; });
    box.addEventListener("click", function () {
      if ($("iframe", box)) return;
      var f = document.createElement("iframe");
      f.src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0";
      f.title = box.getAttribute("data-title") || "유튜브 영상";
      f.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
      f.allowFullscreen = true;
      box.appendChild(f);
    });
  });

  /* ---------- AutoLed 상태 바꿔 보기 ---------- */
  $$("[data-states]").forEach(function (wrap) {
    var btns = $$(".state-list button", wrap), imgs = $$(".state-view img", wrap);
    var i = 0, timer = null, touched = false;
    var set = function (k) {
      i = k;
      btns.forEach(function (b, n) { b.setAttribute("aria-pressed", String(n === k)); });
      imgs.forEach(function (im, n) { im.classList.toggle("on", n === k); });
    };
    btns.forEach(function (b, n) { b.addEventListener("click", function () { touched = true; clearInterval(timer); set(n); }); });
    set(0);
    if (!reduce) onView(wrap, function (_, inView) {
      clearInterval(timer);
      if (inView && !touched) timer = setInterval(function () { set((i + 1) % btns.length); }, 2400);
    });
  });

  /* ---------- 전후 비교 ---------- */
  $$("[data-compare]").forEach(function (box) {
    var input = $("input", box);
    var set = function (v) { box.style.setProperty("--pos", v + "%"); };
    input.addEventListener("input", function () { set(input.value); });
    set(input.value);
    if (anim) onView(box, function (t, inView, io) {
      if (!inView) return; io.unobserve(t);
      var o = { v: 82 };
      G.to(o, { v: 50, duration: 1.6, ease: "expo.inOut", delay: 0.2, onUpdate: function () { input.value = o.v; set(o.v); } });
    });
  });

  /* ---------- 긴 화면 훑어보기 ---------- */
  $$("[data-scroller]").forEach(function (wrap) {
    var boxes = $$(".scroller", wrap);
    var run = function (box, down) {
      var img = $("img", box);
      var d = Math.max(0, img.getBoundingClientRect().height - box.clientHeight);
      var dur = Math.min(14, Math.max(3, d / 500));
      img.style.transitionDuration = (down ? dur : 1.2) + "s";
      img.style.transform = down ? "translateY(" + -d + "px)" : "";
    };
    boxes.forEach(function (box) {
      box.addEventListener("pointerenter", function () { run(box, true); });
      box.addEventListener("pointerleave", function () { run(box, false); });
      box.addEventListener("click", function () { var img = $("img", box); run(box, !img.style.transform); });
    });
    $$("[data-shot]", wrap).forEach(function (b) {
      b.addEventListener("click", function () {
        $$("[data-shot]", wrap).forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
        var key = b.getAttribute("data-shot");
        boxes.forEach(function (box) {
          var img = $("img", box);
          img.style.transitionDuration = "0s"; img.style.transform = "";
          img.src = box.getAttribute("data-base") + key + "-" + box.getAttribute("data-kind") + ".webp";
          img.alt = b.getAttribute("data-alt") + (box.getAttribute("data-kind") === "pc" ? " PC 화면" : " 휴대폰 화면");
        });
        var u = $(".browser-url", wrap);
        if (u) u.textContent = b.getAttribute("data-url");
      });
    });
  });

  /* ---------- 페이지 넘김 ---------- */
  var curtain = $(".curtain");
  if (curtain && anim) {
    var bars = $$("i", curtain);
    if (root.classList.contains("page-enter")) {
      G.to(bars, { scaleY: 0, transformOrigin: "50% 0%", duration: 0.7, ease: "expo.inOut", stagger: 0.04, onComplete: function () { root.classList.remove("page-enter"); G.set(bars, { clearProps: "all" }); } });
    }
    document.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest("a[href]");
      if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
      if (a.target && a.target !== "_self") return;
      var href = a.getAttribute("href");
      if (!href || href.charAt(0) === "#" || /^(mailto|tel|javascript):/.test(href)) return;
      var u = new URL(a.href, location.href);
      if (u.origin !== location.origin || u.pathname.indexOf("/works/") === 0 || u.pathname.indexOf("/motion-parts/") === 0) return;
      if (u.pathname === location.pathname && u.hash) return;
      e.preventDefault();
      try { sessionStorage.setItem("pt", "1"); } catch (err) {}
      G.to(bars, { scaleY: 1, transformOrigin: "50% 100%", duration: 0.55, ease: "expo.inOut", stagger: 0.04, onComplete: function () { location.href = a.href; } });
    });
    window.addEventListener("pageshow", function (e) { if (e.persisted) { G.set(bars, { scaleY: 0 }); root.classList.remove("page-enter"); } });
  }

  if (ST) {
    requestAnimationFrame(function () { ST.refresh(); ST.update(); });
    setTimeout(function () { ST.update(); }, 400);
    window.addEventListener("load", function () { ST.refresh(); });
  }
})();
