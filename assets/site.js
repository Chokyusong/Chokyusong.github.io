// 칸을 누르면 자세히 보기 창, 화면에 들어오면 부드럽게 나타나기, 짧은 반복 영상 재생.
(function () {
  var root = document.documentElement;
  root.classList.add("js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // 자세히 보기
  var lastButton = null;
  document.querySelectorAll("[data-open]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var dlg = document.getElementById(btn.getAttribute("data-open"));
      if (!dlg || typeof dlg.showModal !== "function") return;
      lastButton = btn;
      dlg.showModal();
      document.body.classList.add("dlg-open");
      dlg.querySelectorAll("video.loop").forEach(play);
      dlg.querySelectorAll(".live-frame").forEach(loadLive);
    });
  });

  // 움직이는 시안: 창을 열 때만 불러오고, PC 화면(1440×900)을 창 폭에 맞춰 줄여 보여 준다.
  // 휴대폰처럼 창이 좁으면 휴대폰 화면(390×844)으로 띄운다.
  function fitLive(box) {
    var f = box.querySelector("iframe");
    if (!f) return;
    var phone = box.parentElement.clientWidth < 640;
    var w = phone ? 390 : 1440, h = phone ? 844 : 900;
    box.style.aspectRatio = w + " / " + h;
    if (phone) { box.style.width = "min(100%, 300px)"; box.style.marginInline = "auto"; }
    else { box.style.width = ""; box.style.marginInline = ""; }
    f.style.width = w + "px";
    f.style.height = h + "px";
    f.style.transform = "scale(" + (box.clientWidth / w) + ")";
  }
  function loadLive(box) {
    var f = box.querySelector("iframe");
    if (!f) return;
    fitLive(box);
    if (!f.getAttribute("src")) f.setAttribute("src", box.getAttribute("data-live"));
  }
  window.addEventListener("resize", function () {
    document.querySelectorAll("dialog[open] .live-frame").forEach(fitLive);
  });
  document.querySelectorAll("dialog").forEach(function (dlg) {
    dlg.addEventListener("click", function (e) {
      if (e.target === dlg || e.target.closest("[data-close]")) dlg.close();
    });
    dlg.addEventListener("close", function () {
      document.body.classList.remove("dlg-open");
      dlg.querySelectorAll("video").forEach(function (v) { v.pause(); });
      dlg.querySelectorAll(".live-frame iframe").forEach(function (f) { f.removeAttribute("src"); });
      if (lastButton) lastButton.focus();
    });
  });

  function play(v) {
    if (reduce) return;
    if (v.preload === "none") { v.preload = "auto"; v.load(); }
    var p = v.play();
    if (p && p.catch) p.catch(function () {});
  }

  if (!("IntersectionObserver" in window)) {
    document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("in"); });
    return;
  }

  // 나타나기: 같은 줄에 있는 것끼리 조금씩 늦게
  var io = new IntersectionObserver(function (entries) {
    var i = 0;
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      en.target.style.setProperty("--d", (i++ * 70) + "ms");
      en.target.classList.add("in");
      io.unobserve(en.target);
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
  document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });

  // 목록 칸의 반복 영상은 화면에 보일 때만 튼다
  var vo = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) play(en.target); else en.target.pause();
    });
  }, { threshold: 0.3 });
  document.querySelectorAll(".bento video.loop").forEach(function (v) { vo.observe(v); });
})();
