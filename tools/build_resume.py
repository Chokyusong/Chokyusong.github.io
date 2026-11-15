# -*- coding: utf-8 -*-
"""이력서 페이지(resume.html) 만들기. PDF는 tools/make_pdf.py가 찍는다.

공개판에는 전화번호, 학력, 전 회사 이름을 넣지 않는다(대표 2026-11-16).
그 셋이 들어간 지원용 판은 저장소 밖에서만 만든다. 이 파일에 적지 않는다.
숫자는 포트폴리오(build.py)와 같은 기록을 쓴다.
"""
import copy
import html
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
e = html.escape

RESUME = {
    "name": "조규송",
    "name_en": "Cho Kyusong",
    "title": "AI Builder · AI 서비스 기획 · 업무 자동화",
    "availability": "정규직 · 계약직 · 프리랜서 모두 가능 · 출근과 원격 모두 가능 · 입사하면 오닉소프트는 부업으로 운영",
    "contacts": [("이메일", "joung2156@gmail.com", "mailto:joung2156@gmail.com"),
                 ("포트폴리오", "chokyusong.github.io", "https://chokyusong.github.io/"),
                 ("GitHub", "github.com/Chokyusong", "https://github.com/Chokyusong"),
                 ("회사", "onicsoft.co.kr", "https://onicsoft.co.kr/")],
    "summary": [
        "AI 코딩 에이전트로 아이디어를 실제로 작동하는 서비스로 만들고, 판매하고, 운영하는 AI 서비스 기획·업무 자동화 전문가입니다.",
        "MCN 콘텐츠기획팀 팀장으로 4년 넘게 팀원 5명을 이끌며 크리에이터 20명 관리, 콘텐츠 기획, 방송 시스템 구축, 스튜디오 운영과 기술 지원을 맡았고, 그때부터 GPT와 Python으로 정산, 계산서 확인, 방송 화면 자동 전환 같은 회사 업무를 직접 자동화했습니다. 2025년 9월 오닉소프트를 세워 방송 자동화 제품 AutoLed를 유료 고객 약 15명에게 팔고 운영하고 있습니다.",
    ],
    "numbers": [("6년 2개월", "경력"), ("약 15명", "AutoLed 유료 고객"), ("78,844건", "하루 처리한 후원 기록"), ("22초 → 0.25초", "대시보드 첫 화면 개선"), ("47 / 48주", "정산 엑셀과 계산 일치")],
    "skills": [
        ("AI 활용 개발 관리", "요구사항 정의, 기능 설계, AI 에이전트 작업 지시, 구현 결과 검증과 오류 개선"),
        ("서비스 기획 · 제품화", "사용자 문제 분석, 기능 우선순위 결정, UI/UX 기획, 제품 출시와 유료 서비스 운영"),
        ("시스템 구조 설계", "업무 처리 흐름, 외부 서비스 연동, 사용자 인증·권한, 데이터 처리 구조 기획"),
        ("품질 · 운영 관리", "자동 테스트 검토, 실제 환경 검증, 버전 관리, 배포 승인과 유지보수"),
        ("프로젝트 · 협업", "팀장 경험을 바탕으로 한 업무 조율, 고객 요구사항 분석, 문제 해결과 개선 방향 수립"),
        ("콘텐츠 · 디자인", "방송 시스템 운영, 그래픽 디자인, 영상 편집, 모션그래픽, 웹사이트·콘텐츠 기획"),
    ],
    "way": "코드는 AI 코딩 에이전트와 함께 씁니다. 무엇을 만들지, 어디가 틀렸는지, 언제 내보낼지는 제가 정하고 직접 확인합니다.",
    "decisions": [
        ("멈춤 문제를 다시 만들어 고침", "방송 중 화면이 멈추는 문제를 멈추는 조건부터 다시 만들어 원인을 찾았습니다. 고치기 전 3번 모두 멈추던 상황이 고친 뒤 5번 모두 정상이었습니다."),
        ("느린 곳을 시험으로 찾아 고침", "가상 데이터 1,350만 건으로 부하 시험을 해 병목을 찾았습니다. 대시보드 첫 화면 약 22초 → 0.25초, 기간별 순위 27~118초 → 1~7초."),
        ("계산이 맞는지 옛 자료와 대조", "정산 프로그램 결과를 기존 정산 엑셀 48주 치와 맞춰 47주가 같음을 확인했고, 계산 오류와 미확정 항목은 지급 확정 전에 따로 걸러지게 나눴습니다."),
        ("내보낼지는 직접 결정", "AutoLed는 자동 테스트 2,051개를 통과시키고 실제 OBS에서 한 번 더 확인한 뒤 배포합니다. 업데이트 파일은 서명과 체크섬으로 검증합니다."),
    ],
    "jobs": [
        {
            "company": "오닉소프트 (ONICSOFT)",
            "role": "대표 · Founder / Product Owner",
            "period": "2025.09 – 재직 중",
            "desc": "AI 기반 소프트웨어·업무 자동화 솔루션을 기획하고 만들어 판매·운영합니다.",
            "projects": [
                {"title": "방송 자동화 솔루션 AutoLed 개발 · 상용화", "period": "2025.10 –", "link": "work/autoled.html",
                 "did": ["방송 현장 요구사항을 분석해 제품 기능을 기획하고, 기능 우선순위와 기존 기능 호환성을 판단",
                         "AI 코딩 에이전트의 작업 범위와 검증 조건을 정하고, 테스트 결과와 실제 방송 장비 연동을 확인해 배포 결정",
                         "고객 의견 수집, 장애 대응, 제품 개선 총괄"],
                 "got": ["개인방송·엑셀방송 자동화 솔루션으로 상용화해 유료 고객 약 15명 확보, 2.1.0 판매 중",
                         "팬더TV, SOOP, 투네이션, 위플랩, 펀네이션 후원 알림을 한 가지 처리 구조로 묶어 OBS·Resolume 연출부터 원래 장면 복귀까지 자동화",
                         "방송 중 화면 멈춤 문제를 재현 조건부터 찾아 해결: 고치기 전 3번 모두 멈춤 → 고친 뒤 5번 모두 정상",
                         "자동 테스트 2,051개, 버전 관리, 배포 승인, 업데이트 무결성(서명·체크섬) 검증 절차 운영"],
                 "tech": "Python, Tkinter, OBS WebSocket, Resolume OSC, Nuitka, Inno Setup, GitHub"},
                {"title": "통합 인증 · 라이선스 · 고객 관리 서버", "period": "2026.08 –", "link": "work/login-server.html",
                 "did": ["여러 소프트웨어 제품의 사용자 인증, 권한, 이용 기간을 한 서버에서 관리하도록 설계",
                         "로그인 → 토큰 검증 → 기능 권한 확인 → 주기적 접속 확인 흐름과 접속 기기 제한 구성",
                         "요금제, 이용권 연장, 은행 입금 문자와 결제 내역을 맞춰 자동으로 연장하는 기능",
                         "관리자 역할 분리, OTP 인증, 감사 기록, Nginx·HTTPS·systemd 배포"],
                 "got": ["AutoLed 등 여러 제품을 한 서버로 운영하고, 새 서비스를 등록해 같은 인증을 쓰는 구조 마련",
                         "자동 백업, 서버 감시, 장애 알림, 예비 서버 복구 절차까지 갖춘 운영 체계"],
                 "tech": "Python, FastAPI, SQLite, REST API, JWT, Linux, Nginx, GitHub"},
                {"title": "후원 데이터 집계 서버 · 성능 개선", "period": "2026.10", "link": "work/bighand.html",
                 "did": ["여러 방송의 후원 기록을 모아 중복을 걸러 저장하고 기간별 통계를 보는 서버 기획",
                         "데이터 보관 기준, 암호화 백업, 자동 복원 확인, 서버 장애 감시 체계 구축"],
                 "got": ["실제 운영 기록 기준 하루 후원 기록 78,844건 처리 (2026년 10월 6일)",
                         "가상 데이터 1,350만 건(약 2GB)으로 부하 시험, 대시보드 첫 화면 약 22초 → 0.25초"],
                 "tech": "Python, SQLite, Linux, systemd, GitHub Actions"},
                {"title": "엔터테인먼트 매출 · 급여 · 세금 자동 정산 프로그램", "period": "2026.10 –", "link": "work/enter-payroll.html",
                 "did": ["방송 수입, 출연자별 지급액, 회사 수익과 지분 분배를 자동으로 계산하는 Windows 프로그램 기획·개발",
                         "원천세, 부가세, 가불, 지급 내역 관리와 Excel·CSV 자료 수집·대조, 정산표 자동 생성",
                         "계산 결과 확인, 예외 보류, 정산 확정과 지급 목록, 개인정보 암호화와 자동 백업"],
                 "got": ["기존 정산 엑셀 48주 치와 비교해 47주의 계산 결과 일치",
                         "계산 오류와 미확정 항목을 나눠 잘못된 지급 확정을 막는 구조, 사무실 PC에서 실제 환경 검증"],
                 "tech": "Python, PySide6, SQLite, Pandas, OpenPyXL, Nuitka"},
                {"title": "실시간 방송 모니터링 프로그램 (CCTV)", "period": "2026.10", "link": "work/cctv.html",
                 "did": ["BJ 최대 60명의 방송 시작·종료를 감지하고 영상·채팅·후원 정보를 한 화면에 모은 관제 프로그램",
                         "방송별 목록, 정렬, 검색, 텔레그램 알림과 SQLite 설정 저장, PC용과 Linux 서버용 기능 분리"],
                 "got": ["매니저가 하나씩 들어가 확인하던 일을 자동 감지로 바꾸고, 서버 기능은 자동 테스트까지 완료"],
                 "tech": "Python, WebSocket, SQLite, Linux, Telegram"},
                {"title": "납품 업체 거래장부 프로그램", "period": "2026.09", "link": "work/ledger.html",
                 "did": ["인쇄 광고물 납품 업체가 두 번씩 적던 엑셀 장부를 한 번 입력으로 끝나게 바꾼 프로그램"],
                 "got": ["옮기는 과정에서 원본 장부끼리 맞지 않는 줄을 찾아 목록으로 정리, 엑셀 내보내기 왕복 확인"],
                 "tech": "Python, SQLite, Excel 연동"},
                {"title": "AI 활용 콘텐츠 기획 · 마케팅", "period": "2026.09 –", "link": None,
                 "did": ["원본 콘텐츠 하나를 블로그·유튜브·네이버·SNS 형식으로 나눠 쓰는 OSMU 체계 설계",
                         "검색 키워드 분석, SEO 제목·메타데이터·글 구조 최적화, 게시 전 사실 확인과 게시 기록 관리",
                         "AI 이미지 도구로 썸네일·광고 소재 제작, 크몽·숨고 판매 자료 구성"],
                 "got": [],
                 "tech": "생성형 AI, SEO, HTML, Photoshop, 영상 편집"},
            ],
        },
        {
            "company": "MCN 회사",
            "role": "콘텐츠기획팀 팀장 · 총괄",
            "period": "2021.07 – 2025.11 (4년 5개월)",
            "desc": "2021.07~10은 방송 기술 회사, 2025.09~11은 오닉소프트와 겸직했습니다.",
            "bullets": ["팀원 5명을 이끌며 소속 크리에이터·BJ 20명 관리, 케어와 정산 비율 상담",
                        "GPT를 활용해 Python으로 회사 업무 자동화 프로그램 직접 제작: 자동 정산, 계산서 발행 확인, 엑셀방송 OBS·레졸룸 자동 전환",
                        "방송 장비(PC·조명·카메라·오디오) 설치와 세팅, 크리에이터 장비 교육",
                        "방송 디자인 요소(시그니처 이모티콘, LIVE 대기 화면, 방송 배너 GIF) 제작: Photoshop, After Effects"],
        },
        {
            "company": "방송 기술 회사",
            "role": "장비 세팅 · 방송 디자인",
            "period": "2020.10 – 2021.10 (1년 1개월)",
            "desc": "2021.07부터 MCN 회사와 겸직했습니다.",
            "bullets": ["PC 장비 설치와 조명·카메라·오디오 세팅",
                        "방송 디자인 요소(시그니처 이모티콘, LIVE 대기 화면, 방송 배너 GIF) 제작: Photoshop"],
        },
    ],
    "extra_projects": [("PDF2Obsidian", "PDF와 강의 자막을 옵시디언 노트로 바꾸는 오픈소스 도구 (2026.06, MIT). 코드와 자동 테스트를 공개했습니다.",
                        "work/pdf2obsidian.html", "https://github.com/Chokyusong/pdf2obsidian"),
                       ("홈페이지", "오닉소프트 공식 홈페이지 기획·제작·운영, 업종별 견본 22종, 엔터 회사 ASTRA 움직이는 시안 8쪽 (2026.08 –)", "work/onicsoft-homepage.html"),
                       ("모션그래픽", "코드와 Blender로 만든 효과 271종, AutoLed 홍보영상과 방송 알림 (2026.09 –)", "work/motion.html")],
    "education": None,
    "tools": ["Python", "FastAPI", "PySide6 · Tkinter", "SQLite", "Linux · Nginx · systemd", "HTML · CSS · JavaScript", "three.js · Blender", "FFmpeg",
              "OBS WebSocket · Resolume OSC", "GitHub · GitHub Actions", "Excel · Pandas", "Photoshop · After Effects", "Claude Code · AI 코딩 에이전트"],
    "language": "영어 · 일상 회화",
}


LABELS = {
    "lang": "ko", "doc": "이력서", "more": "자세히", "code": "코드 보기", "got": "성과", "edu": "학력",
    "back": "← 포트폴리오", "pdf": "PDF로 받기", "pdf_href": "assets/cho-kyusong-resume.pdf",
    "other": "English", "other_href": "resume-en.html",
    "decisions": "직접 판단하고 확인한 것", "skills": "핵심 역량", "career": "경력", "career_total": "총 6년 2개월 · 겹치는 기간은 겸직",
    "extra": "그 밖의 작업", "tools": "쓰는 도구", "language": "언어",
    "foot": "비공개 저장소의 소스 코드와 핵심 로직은 공개하지 않습니다. 작업별 화면과 영상은 chokyusong.github.io에서 볼 수 있습니다.",
}


def li(items):
    return "".join(f"<li>{e(x)}</li>" for x in items)


def render(r, base="", private=False):
    L = r.get("labels", LABELS)
    contacts = "".join(f'<a href="{u}">{e(k)} <b>{e(v)}</b></a>' for k, v, u in r["contacts"])
    nums = "".join(f"<div><b>{e(a)}</b><span>{e(b)}</span></div>" for a, b in r["numbers"])
    skills = "".join(f"<div><b>{e(a)}</b><p>{e(b)}</p></div>" for a, b in r["skills"])
    jobs = []
    for j in r["jobs"]:
        body = ""
        if j.get("projects"):
            ps = []
            for p in j["projects"]:
                link = f' <a class="more" href="{base}{p["link"]}">{L["more"]}</a>' if p.get("link") else ""
                got = f'<p class="lab">{L["got"]}</p><ul class="got">{li(p["got"])}</ul>' if p["got"] else ""
                ps.append(f'<article class="proj"><header><h4>{e(p["title"])}{link}</h4><span>{e(p["period"])}</span></header>'
                          f'<ul>{li(p["did"])}</ul>{got}<p class="tech">{e(p["tech"])}</p></article>')
            body = "".join(ps)
        else:
            body = f'<ul>{li(j["bullets"])}</ul>'
        desc = f'<p class="jdesc">{e(j["desc"])}</p>' if j.get("desc") else ""
        jobs.append(f'<section class="job"><header><div><h3>{e(j["company"])}</h3><p>{e(j["role"])}</p></div><span>{e(j["period"])}</span></header>{desc}{body}</section>')
    extra = "".join(f'<li><b>{e(x[0])}</b> {e(x[1])} <a class="more" href="{base}{x[2]}">{L["more"]}</a>'
                    + (f' <a class="more" href="{x[3]}">{L["code"]}</a>' if len(x) > 3 else "") + '</li>' for x in r["extra_projects"])
    decisions = "".join(f"<div><b>{e(a)}</b><p>{e(b)}</p></div>" for a, b in r["decisions"])
    edu = ""
    if r.get("education"):
        edu = f'<h2>{L["edu"]}</h2><ul class="plain">{li(r["education"])}</ul>'
    tools = "".join(f"<span>{e(t)}</span>" for t in r["tools"])
    avail = f'<p class="avail">{e(r["availability"])}</p>' if r.get("availability") else ""
    robots = '<meta name="robots" content="noindex">'
    bar = "" if private else (f'<div class="bar"><a href="{base}index.html">{L["back"]}</a><span>'
                              f'<a class="alt" href="{base}{L["other_href"]}">{L["other"]}</a>'
                              f'<a class="dl" href="{base}{L["pdf_href"]}">{L["pdf"]}</a></span></div>')
    return f"""<!doctype html>
<html lang="{L["lang"]}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
{robots}
<title>{e(r["name"])} {L["doc"]} · AI Builder</title>
<meta name="description" content="{e(r["name"])} {L["doc"]}. {e(r["title"])}.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' rx='3' fill='%2307090b'/%3E%3Crect x='4' y='4' width='3' height='3' fill='%2345c6d6'/%3E%3Crect x='9' y='4' width='3' height='3' fill='%2345c6d6'/%3E%3Crect x='4' y='9' width='3' height='3' fill='%2345c6d6'/%3E%3C/svg%3E">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<style>
@page {{ size:A4; margin:13mm 14mm 15mm; }}
:root {{ --ink:#111418; --sub:#454d57; --mute:#7b848f; --line:#dfe3e8; --acc:#0f8a99; --soft:#f2f6f7; }}
* {{ box-sizing:border-box; }}
html {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
body {{ margin:0; font-family:"Pretendard Variable",Pretendard,system-ui,sans-serif; color:var(--ink); font-size:9pt; line-height:1.5; word-break:keep-all; background:#fff; }}
a {{ color:inherit; text-decoration:none; }}
.page {{ max-width:182mm; margin:0 auto; }}
h1,h2,h3,h4 {{ margin:0; letter-spacing:-0.02em; }}
.top {{ display:grid; grid-template-columns:1fr auto; gap:4mm; align-items:end; padding-bottom:5mm; border-bottom:1.5pt solid var(--ink); }}
.top h1 {{ font-size:26pt; font-weight:800; line-height:1.1; }}
.top h1 small {{ font-size:11pt; color:var(--mute); font-weight:500; margin-left:2.5mm; letter-spacing:0; }}
.top .role {{ color:var(--acc); font-weight:700; font-size:11pt; margin:2mm 0 0; }}
.avail {{ margin:1.2mm 0 0; font-size:8.6pt; color:var(--sub); }}
.contacts {{ display:grid; gap:.8mm; text-align:right; font-size:8.6pt; color:var(--mute); }}
.contacts b {{ color:var(--ink); font-weight:600; }}
.summary {{ margin:4mm 0 3.5mm; font-size:10pt; color:var(--sub); }}
.summary p {{ margin:0 0 1.6mm; }}
.nums {{ display:grid; grid-template-columns:repeat(5,1fr); gap:2.5mm; margin-bottom:4mm; }}
.nums div {{ background:var(--soft); border-radius:2mm; padding:3mm 3mm 2.5mm; }}
.nums b {{ display:block; font-size:12.5pt; font-weight:800; letter-spacing:-0.02em; }}
.nums span {{ font-size:7.8pt; color:var(--sub); }}
h2 {{ font-size:11pt; margin:5mm 0 2.5mm; padding-bottom:1.5mm; border-bottom:.75pt solid var(--ink); display:flex; justify-content:space-between; align-items:baseline; }}
h2 small {{ font-size:8.5pt; font-weight:500; color:var(--mute); }}
.skills {{ display:grid; grid-template-columns:1fr 1fr; gap:1.8mm 7mm; }}
.skills b {{ font-size:9.2pt; }} .skills p {{ margin:.3mm 0 0; color:var(--sub); font-size:8.6pt; }}
.way {{ margin:0 0 2.2mm; color:var(--sub); }}
.decisions b {{ color:var(--acc); }}
.job {{ margin-bottom:5mm; }}
.job > header {{ display:flex; justify-content:space-between; align-items:baseline; gap:4mm; margin-bottom:2mm; }}
.job h3 {{ font-size:12pt; font-weight:800; }}
.job > header p {{ margin:.5mm 0 0; color:var(--acc); font-weight:600; font-size:9pt; }}
.job > header span, .proj header span {{ color:var(--mute); font-size:8.5pt; white-space:nowrap; font-variant-numeric:tabular-nums; }}
.jdesc {{ margin:0 0 3mm; color:var(--sub); }}
.proj {{ border-left:1.5pt solid var(--line); padding:0 0 0 4mm; margin:0 0 3.2mm; break-inside:avoid; }}
.proj header {{ display:flex; justify-content:space-between; align-items:baseline; gap:4mm; }}
.proj h4 {{ font-size:10pt; font-weight:700; }}
.more {{ font-size:7.8pt; font-weight:500; color:var(--acc); margin-left:2mm; white-space:nowrap; }}
ul {{ margin:1.2mm 0 0; padding-left:4.2mm; }} li {{ margin-bottom:.5mm; }}
.lab {{ margin:1.6mm 0 0; font-size:8pt; font-weight:700; color:var(--acc); }}
.got {{ margin-top:.5mm; }} .got li {{ font-weight:600; }}
.tech {{ margin:1.2mm 0 0; font-size:8pt; color:var(--mute); }}
.job > ul {{ margin-top:0; }}
.plain {{ list-style:none; padding:0; }}
.tools {{ display:flex; flex-wrap:wrap; gap:1.6mm; }}
.tools span {{ border:.6pt solid var(--line); border-radius:10mm; padding:.8mm 2.8mm; font-size:8.4pt; }}
.two {{ display:grid; grid-template-columns:1fr 1fr; gap:7mm; }}
.foot {{ margin-top:6mm; color:var(--mute); font-size:7.8pt; }}
.bar {{ display:none; }}
@media screen {{
  body {{ background:#e8ecef; padding:0 0 40px; }}
  .bar {{ display:flex; justify-content:space-between; max-width:210mm; margin:0 auto; padding:18px 16px; font-size:14px; }}
  .bar .dl {{ background:#111418; color:#fff; padding:8px 16px; border-radius:999px; }}
  .bar > span {{ display:flex; align-items:center; gap:14px; }} .bar .alt {{ border-bottom:1px solid #9aa3ad; }}
  .page {{ background:#fff; max-width:210mm; padding:16mm 14mm; box-shadow:0 20px 60px -30px rgba(0,0,0,.35); }}
}}
@media screen and (max-width:700px) {{
  .page {{ padding:28px 18px; }} .top {{ grid-template-columns:1fr; }}
  .contacts {{ text-align:left; grid-template-columns:auto auto; justify-content:start; gap:4px 18px; font-size:12px; }}
  .contacts a {{ display:flex; flex-direction:column; }}
  .summary {{ font-size:13px; }}
  .nums {{ grid-template-columns:repeat(2,1fr); gap:6px; }}
  .nums div {{ padding:8px 10px; }} .nums b {{ font-size:16px; }}
  .nums div:last-child:nth-child(odd) {{ grid-column:span 2; }} .skills, .two {{ grid-template-columns:1fr; }}
  .job > header, .proj header {{ flex-direction:column; gap:1mm; }}
}}
{r.get("css", "")}</style></head>
<body>
{bar}
<main class="page">
  <header class="top">
    <div><h1>{e(r["name"])}<small>{e(r["name_en"])}</small></h1><p class="role">{e(r["title"])}</p>{avail}</div>
    <div class="contacts">{contacts}</div>
  </header>
  <div class="summary">{"".join(f"<p>{e(x)}</p>" for x in r["summary"])}</div>
  <div class="nums">{nums}</div>
  <h2>{L["decisions"]}</h2><p class="way">{e(r["way"])}</p><div class="skills decisions">{decisions}</div>
  <h2>{L["skills"]}</h2><div class="skills">{skills}</div>
  <h2>{L["career"]}<small>{L["career_total"]}</small></h2>
  {"".join(jobs)}
  <h2>{L["extra"]}</h2><ul class="plain">{extra}</ul>
  {edu}
  <h2>{L["tools"]}<small>{L["language"]}: {e(r["language"])}</small></h2><div class="tools">{tools}</div>
  <p class="foot">{L["foot"]}</p>
</main>
</body></html>
"""


def main():
    import resume_en  # 영문판 자료는 따로 둔다(같은 틀, 같은 공개 규칙)
    for name, r in (("resume.html", RESUME), ("resume-en.html", resume_en.RESUME_EN)):
        with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(render(r))


def private_copy(overrides, base=None):
    """지원용 판 자료. 전화번호·학력·회사 이름은 부르는 쪽(저장소 밖)에서 넘긴다."""
    r = copy.deepcopy(base or RESUME)
    overrides(r)
    return r


if __name__ == "__main__":
    main()
