# -*- coding: utf-8 -*-
"""인쇄용 한 권(print.html)과 그 그림(assets/print/*.jpg) 만들기.

build.py가 끝에 부른다. PDF는 tools/make_pdf.py로 print.html을 찍어 만든다.
"""
import html
import os
import re

from PIL import Image

import build as B

e = html.escape
OUT_IMG = os.path.join(B.ROOT, "assets", "print")
SITE = "https://chokyusong.github.io/"
NO_IMG = {"bighand", "aios"}  # 화면을 공개하지 않는 작업


def strip(s):
    return re.sub(r"<[^>]+>", "", s)


def thumb(slug, name, tall=False):
    """1000px 너비 JPG. 긴 화면은 위쪽 16:10만 자른다."""
    os.makedirs(OUT_IMG, exist_ok=True)
    out = f"{slug}-{name}.jpg"
    path = os.path.join(OUT_IMG, out)
    src = os.path.join(B.IMG, slug, name + ".webp")
    if not os.path.exists(path) or os.path.getmtime(path) < os.path.getmtime(src):
        with Image.open(src) as im:
            im = im.convert("RGB")
            w, h = im.size
            if h / w > 0.9 and not tall:
                im = im.crop((0, 0, w, int(w * 0.625)))
            im.thumbnail((1000, 1000 if not tall else 1600))
            im.save(path, "JPEG", quality=80, optimize=True, progressive=True)
    return f"assets/print/{out}"


def images(p):
    """대표 그림 최대 4장: (주소, 설명, 휴대폰처럼 세로인지)."""
    slug = p["slug"]
    if slug in NO_IMG:
        return []
    picks = []
    if p.get("cover"):
        picks.append((p["cover"][1], p["cover"][2]))
    for kind, d in p["blocks"]:
        if kind == "gallery":
            picks += [(it[0], it[1]) for it in d["items"]]
        elif kind == "states":
            picks += [(n, f"기본창 — {lab} 상태") for n, lab, _ in d["items"]]
        elif kind == "compare":
            picks += [(d["before"], d["lb"] + " 화면"), (d["after"], d["la"] + " 화면")]
        elif kind == "clips":
            return [(f'{B.CLIPS}{cid}.jpg', f"{name} · {cat}", False) for cid, name, cat in d["items"][:4]]
    if slug == "autoled":
        picks = [("ui-timeline", p["cover"][2]), ("ui-overview", "관리센터 개요. 준비 단계와 장비별 연결 상태"), ("mgmt-mapping", "후원 연출 표. 후원 개수마다 실행할 칼럼과 장면. 예시 매핑"), ("ui-settings", "설정. 연출 끝 여유, 최소 코인, 잠금 같은 방송 규칙")]
    if slug == "onicsoft-homepage":
        picks = [("cover-pc", "홈페이지 첫 화면"), ("services-pc", "서비스 쪽"), ("autoled-pc", "제품 AutoLed 쪽"), ("blog-pc", "블로그")]
    seen, out = set(), []
    for n, cap in picks:
        if n in seen or not os.path.exists(os.path.join(B.IMG, slug, n + ".webp")):
            continue
        seen.add(n)
        w, h = B.size(slug, n)
        tall = h > w and w < 900
        out.append((thumb(slug, n, tall=tall), cap, tall))
        if len(out) == 4:
            break
    return out


def facts(p):
    """그림 대신 읽을 거리: 핵심 점, 숫자, 카드, 흐름."""
    out, nums = [], []
    for kind, d in p["blocks"]:
        if kind == "points":
            out += [t for _, t in d["items"]]
        elif kind == "cards":
            out += [f"{t}: {x}" for t, x in d["items"]]
        elif kind == "kpis":
            nums += d["items"]
        elif kind == "hub":
            out += [f"{a}: {b}" for a, b in d["items"]]
        elif kind == "flow":
            out.append(" → ".join(it[0] for it in d["items"]))
        elif kind == "perf":
            nums += [("22초 → 0.25초", "대시보드 첫 화면 (1,350만 건 부하 시험)"), ("27~118초 → 1~7초", "30일 · 3달 방송 순위")]
    return out[:3], nums[:4]


def videos(p):
    for kind, d in p["blocks"]:
        if kind == "yt":
            return d["items"]
    return []


def project(i, p):
    meta = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in p["meta"])
    story = "".join(f"<div><h4>{e(h)}</h4><p>{t}</p></div>" for h, t in p["story"])
    pts, nums = facts(p)
    if p.get("pv_stat") and not nums:
        nums = [p["pv_stat"]]
    nums_html = "".join(f"<div><b>{e(a)}</b><span>{e(b)}</span></div>" for a, b in nums)
    nums_html = f'<div class="nums">{nums_html}</div>' if nums else ""
    pts_html = "".join(f"<li>{e(t)}</li>" for t in pts)
    pts_html = f'<ul class="pts">{pts_html}</ul>' if pts else ""
    ims = images(p)
    figs = "".join(f'<figure class="{"tall" if tall else ""}"><img src="{src}" alt="{e(cap)}"><figcaption>{e(strip(cap))}</figcaption></figure>' for src, cap, tall in ims)
    figs = f'<div class="figs n{len(ims)}">{figs}</div>' if ims else ""
    vids = "".join(f'<li>{e(t)} — youtu.be/{v}</li>' for v, t in videos(p))
    vids = f'<div class="vids"><h4>영상</h4><ul>{vids}</ul></div>' if vids else ""
    links = "".join(f'<li>{e(t)} — {e(u.replace("https://", ""))}</li>' for t, u in p.get("links", []))
    links = f'<li>상세 페이지 — {SITE.replace("https://", "")}work/{p["slug"]}.html</li>' + links
    notice = f'<p class="notice">{e(p["notice"])}</p>' if p.get("notice") else ""
    return f"""<section class="proj">
  <header><span class="n">{i + 1:02d} / {B.N:02d} · {e(B.CAT_NAME[B.CAT_OF[p["slug"]]])}</span><span class="kind">{e(p["kind"])}</span></header>
  <h2>{e(p["title"])}</h2>
  <p class="sum">{e(p["summary"])}</p>
  <dl class="meta">{meta}</dl>
  <div class="story">{story}</div>
  {nums_html}{figs}{pts_html}{vids}
  <ul class="links">{links}</ul>{notice}
</section>"""


def main(projects):
    idx = ""
    for i, p in enumerate(projects):
        c = B.CAT_OF[p["slug"]]
        if i == 0 or B.CAT_OF[projects[i - 1]["slug"]] != c:
            idx += f'<li class="cat">{e(B.CAT_NAME[c])}</li>'
        idx += f'<li><span>{i + 1:02d}</span><b>{e(p["title"])}</b><em>{e(p["short"])}</em></li>'
    body = "".join(project(i, p) for i, p in enumerate(projects))
    by = {p["slug"]: p for p in projects}
    fields = "".join(f'<div><b>{e(n)}</b><p>{e(t)}</p><span>{e(", ".join(by[x]["title"] for x in sl))}</span></div>' for _, n, t, sl, _pic in B.FIELDS)
    page = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>조규송 · AI Builder 포트폴리오 (인쇄판)</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<style>
@page {{ size: A4; margin: 14mm 14mm 16mm; }}
:root {{ --ink:#111418; --sub:#4a525c; --mute:#7b848f; --line:#dfe3e8; --acc:#0f8a99; --soft:#f3f6f8; }}
* {{ box-sizing:border-box; }}
html {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
body {{ margin:0; font-family:"Pretendard Variable",Pretendard,system-ui,sans-serif; color:var(--ink); font-size:9pt; line-height:1.55; word-break:keep-all; background:#fff; }}
.wrap {{ max-width:182mm; margin:0 auto; }}
h1,h2,h3,h4 {{ margin:0; letter-spacing:-0.02em; }}
.cover {{ min-height:262mm; display:flex; flex-direction:column; }}
.cover .eyebrow {{ color:var(--acc); font-weight:600; font-size:9pt; letter-spacing:.08em; }}
.cover h1 {{ font-size:34pt; line-height:1.12; margin:6mm 0 5mm; font-weight:800; }}
.cover h1 em {{ font-style:normal; color:var(--acc); }}
.cover .lead {{ font-size:11pt; color:var(--sub); max-width:150mm; }}
.stats {{ display:grid; grid-template-columns:repeat(4,1fr); border-top:1.5pt solid var(--ink); margin-top:10mm; }}
.stats div {{ padding:4mm 3mm 3mm 0; border-right:.5pt solid var(--line); }}
.stats div:last-child {{ border:0; }}
.stats b {{ display:block; font-size:20pt; font-weight:800; }}
.stats span {{ color:var(--sub); font-size:8.5pt; }}
.asof {{ color:var(--mute); font-size:8pt; margin-top:2mm; }}
.cols {{ display:grid; grid-template-columns:1fr 1fr; gap:8mm; margin-top:10mm; }}
h3 {{ font-size:10.5pt; margin-bottom:2.5mm; padding-bottom:1.5mm; border-bottom:.75pt solid var(--ink); }}
.hist {{ list-style:none; padding:0; margin:0; }}
.hist li {{ display:grid; grid-template-columns:16mm 1fr; padding:1.2mm 0; border-bottom:.5pt solid var(--line); }}
.hist time {{ color:var(--acc); font-weight:600; }}
.stack div {{ display:grid; grid-template-columns:22mm 1fr; margin-bottom:1.6mm; }}
.how {{ display:grid; grid-template-columns:1fr 1fr; gap:3mm 6mm; margin-top:8mm; }}
.how div b {{ display:block; margin-bottom:.5mm; }} .how p {{ margin:0; color:var(--sub); }}
.contact {{ margin-top:auto; padding-top:8mm; display:grid; grid-template-columns:repeat(4,auto); gap:2mm 8mm; justify-content:start; font-size:9pt; }}
.contact span {{ color:var(--mute); display:block; font-size:7.5pt; }}
.toc {{ break-before:page; }}
.toc h2 {{ font-size:18pt; margin-bottom:3.5mm; }}
.toc .fields {{ display:grid; grid-template-columns:1fr 1fr; gap:3mm 8mm; margin-bottom:7mm; }}
.toc .fields div {{ border-top:1.5pt solid var(--ink); padding-top:2mm; }}
.toc .fields b {{ font-size:10.5pt; }} .toc .fields p {{ margin:.6mm 0; color:var(--sub); font-size:8.5pt; line-height:1.45; }} .toc .fields span {{ font-size:8pt; color:var(--acc); }}
.toc ol {{ list-style:none; padding:0; margin:0; border-top:1.5pt solid var(--ink); }}
.toc li {{ display:grid; grid-template-columns:12mm 62mm 1fr; padding:1.2mm 0; border-bottom:.5pt solid var(--line); align-items:baseline; }}
.toc li.cat {{ display:block; padding:2.6mm 0 .8mm; color:var(--acc); font-weight:700; font-size:8.5pt; letter-spacing:.06em; border-bottom:.75pt solid var(--ink); }}
.toc li span {{ color:var(--acc); font-weight:700; }} .toc li b {{ font-size:11pt; }} .toc li em {{ font-style:normal; color:var(--sub); }}
.toc .note {{ color:var(--mute); font-size:8pt; margin-top:3mm; }}
.proj {{ break-before:page; }}
.proj header {{ display:flex; justify-content:space-between; color:var(--mute); font-size:8pt; border-bottom:.5pt solid var(--line); padding-bottom:2mm; }}
.proj header .n {{ color:var(--acc); font-weight:700; }}
.proj h2 {{ font-size:20pt; font-weight:800; margin:4mm 0 2mm; line-height:1.2; }}
.sum {{ font-size:10pt; color:var(--sub); margin:0 0 3.5mm; }}
.meta {{ display:grid; grid-template-columns:repeat(2,1fr); gap:0 8mm; margin:0 0 5mm; border-top:.75pt solid var(--ink); }}
.meta div {{ display:grid; grid-template-columns:18mm 1fr; padding:1.4mm 0; border-bottom:.5pt solid var(--line); }}
.meta dt {{ color:var(--mute); }} .meta dd {{ margin:0; }}
.story {{ display:grid; grid-template-columns:repeat(3,1fr); gap:5mm; margin-bottom:4mm; }}
.story h4 {{ font-size:9pt; color:var(--acc); margin-bottom:1mm; }}
.story p {{ margin:0; font-size:8.5pt; line-height:1.5; }} .story strong {{ font-weight:700; }}
.nums {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(38mm,1fr)); gap:3mm; margin-bottom:5mm; }}
.nums div {{ background:var(--soft); padding:3mm; border-radius:2mm; }}
.nums b {{ display:block; font-size:13pt; font-weight:800; }} .nums span {{ font-size:8pt; color:var(--sub); }}
.figs {{ display:grid; grid-template-columns:1fr 1fr; gap:3mm 4mm; margin-bottom:3mm; }}
.figs.n1 {{ grid-template-columns:1fr; }}
.figs figure {{ margin:0; break-inside:avoid; }}
.figs img {{ width:100%; aspect-ratio:16/7.8; object-fit:cover; object-position:top; border:.5pt solid var(--line); border-radius:1.5mm; display:block; background:var(--soft); }}
.figs figure.tall img {{ object-fit:contain; }}
.figs.n1 img {{ aspect-ratio:16/7.5; }}
.figs figcaption {{ font-size:7.5pt; color:var(--mute); margin-top:1mm; line-height:1.45; }}
.pts {{ margin:0 0 4mm; padding-left:4.5mm; }} .pts li {{ margin-bottom:.6mm; }}
.vids h4 {{ font-size:9pt; margin-bottom:1mm; }} .vids ul {{ margin:0 0 3mm; padding-left:4.5mm; }}
.links li {{ display:inline; }} .links li + li::before {{ content:"  ·  "; }}
.links {{ list-style:none; padding:2mm 0 0; margin:0; border-top:.5pt solid var(--line); color:var(--sub); font-size:8.5pt; }}
.notice {{ color:var(--mute); font-size:8pt; margin:2mm 0 0; }}
@media screen {{ body {{ background:#e9edf0; }} .cover,.toc,.proj {{ background:#fff; width:210mm; margin:8mm auto; padding:14mm; min-height:297mm; }} }}
</style></head>
<body>
<section class="cover"><div class="wrap">
  <p class="eyebrow">조규송 (CHO KYUSONG) · {html.escape(B.ROLE)}</p>
  <h1>AI로 필요한 것을<br>만들고, 팔고,<br><em>직접 운영</em>합니다.</h1>
  <p class="lead">기획, 디자인, 개발, 배포, 운영까지 AI와 함께 혼자 끝내는 AI&nbsp;Builder입니다. 방송 자동화 제품 AutoLed를 만들어 유료 고객 약 15명에게 팔고, 회사 업무를 줄이는 자동화 프로그램과 서버를 직접 만들고 운영합니다. 코드는 AI 코딩 도구와 함께 쓰고, 무엇을 만들고 언제 내보낼지는 제가 정합니다.</p>
  <div class="stats">
    <div><b>약 15명</b><span>AutoLed 유료 고객 · 2.1.0 판매 중</span></div>
    <div><b>6년</b><span>방송·MCN 현장부터 제품 개발까지</span></div>
    <div><b>2,200+</b><span>소개한 작업의 자동 테스트</span></div>
    <div><b>{B.N}</b><span>소개한 작업</span></div>
  </div>
  <p class="asof">{B.ASOF} 기준. 테스트 수는 각 저장소 기록, 경력은 이력서 기준입니다.</p>
  <div class="cols">
    <div><h3>연혁</h3><ol class="hist">
      <li><time>2020.10</time>방송 기술 회사 입사. 장비 세팅과 방송 디자인</li>
      <li><time>2021.07</time>MCN 팀장, 팀원 5명(방송 기술 회사와 겸직). 재직 중 사내 자동화</li>
      <li><time>2025.09</time>오닉소프트 시작(MCN과 겸직), AutoLed</li>
      <li><time>2026.06</time>PDF2Obsidian 공개</li>
      <li><time>2026.08</time>로그인 서버 운영, AutoLed 정식 배포, 회사 홈페이지</li>
      <li><time>2026.09</time>모션그래픽 작업실, 유튜브 채널, 납품 업체 엑셀 장부 자동화</li>
      <li><time>2026.10</time>후원 데이터 집계 서버, 엔터 정산, CCTV 관제, 거래장부</li>
      <li><time>2026.11</time>AutoLed 2.1.0, 엔터 회사 홈페이지 ASTRA 제작</li>
    </ol></div>
    <div class="stack"><h3>주로 쓰는 기술</h3>
      <div><b>언어</b>Python, JavaScript, HTML/CSS, PHP</div>
      <div><b>데스크톱 앱</b>Tkinter, PySide6, Nuitka, PyInstaller, Inno Setup</div>
      <div><b>서버</b>FastAPI, Nginx, Caddy, systemd, SQLite, Ubuntu</div>
      <div><b>방송 · 영상</b>OBS WebSocket, Resolume OSC, Companion, three.js, Blender, ffmpeg</div>
      <div><b>운영</b>GitHub Actions, Telegram 봇 알림, fail2ban, 암호화 백업</div>
    </div>
  </div>
  <div class="how">
    <div><b>AI와 나눠서 만듭니다</b><p>코드는 Claude Code, Codex 같은 AI 코딩 도구와 함께 씁니다. 무엇을 만들지, 공개할지, 언제 내보낼지는 제가 정합니다.</p></div>
    <div><b>테스트로 확인하고 내보냅니다</b><p>자동 테스트를 먼저 통과시키고, 실제 OBS나 실제 서버에서 한 번 더 확인한 뒤 배포합니다.</p></div>
    <div><b>만든 뒤에도 운영합니다</b><p>서버가 멈추면 다시 켜지고 알림이 오게 둡니다. 백업은 암호화해 매일 받고 매달 복원 연습을 자동으로 돌립니다.</p></div>
    <div><b>공개 범위를 나눕니다</b><p>제품 소스와 핵심 로직은 비공개로 둡니다. 화면은 모두 예시 데이터로 찍었습니다.</p></div>
  </div>
  <div class="contact">
    <div><span>웹 포트폴리오 · 이력서</span>chokyusong.github.io</div>
    <div><span>이메일</span>{e(B.EMAIL)}</div>
    <div><span>GitHub</span>github.com/Chokyusong</div>
    <div><span>근무 형태 · 모두 가능 · 오닉소프트는 부업</span>정규직·계약직·프리랜서 / 출근·원격</div>
  </div>
</div></section>
<section class="toc"><div class="wrap"><h2>하는 일</h2><div class="fields">{fields}</div><h2>작업 {B.N}가지</h2><ol>{idx}</ol>
<p class="note">웹 포트폴리오(chokyusong.github.io)에서는 같은 작업을 영상, 움직이는 시안, 전체 화면으로 직접 볼 수 있습니다. 비공개 저장소는 핵심 로직 없이 무엇을 만들고 어떤 결과가 났는지만 소개합니다.</p></div></section>
<div class="wrap">{body}</div>
</body></html>
"""
    with open(os.path.join(B.ROOT, "print.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(page)
