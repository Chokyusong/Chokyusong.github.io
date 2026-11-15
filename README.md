# 조규송 포트폴리오

GitHub Pages로 올린 개인 포트폴리오 사이트. 방문자에게는 빌드 없는 정적 HTML이고, 페이지는 `tools/build.py`가 만든다.

## 구조

- `index.html` 첫 화면, `work/<slug>.html` 작업 11개 상세, `print.html` 인쇄판(검색 제외)
- `assets/css/site.css`, `assets/js/site.js` 디자인과 움직임(GSAP, ScrollTrigger, Lenis)
- `assets/img/<slug>/` 작업별 실제 화면(webp), `assets/print/` 인쇄판용 작은 그림
- `assets/cho-kyusong-portfolio.pdf` 인쇄판을 찍은 PDF
- `works/astra/` ASTRA 움직이는 시안(상세 페이지 안에서 직접 조작)
- `tools/build.py` 글과 그림 목록(PROJECTS) → 페이지, `tools/build_print.py` 인쇄판, `tools/build_resume.py` 이력서(한글), `tools/resume_en.py` 영문 이력서 자료(같은 틀), `tools/make_pdf.py` PDF 세 개(포트폴리오·이력서·영문 이력서)

## 고치는 법

```bash
py -3 tools/build.py
```

```bash
py -3 tools/make_pdf.py
```

글은 `tools/build.py`의 PROJECTS를 고치고 다시 만든다. 만든 HTML을 직접 고치지 않는다. 작업 분류(프로그램·업무 자동화·홈페이지·서버·모션그래픽)와 순서는 같은 파일의 CATS 한 곳에서 정한다(첫 화면 카드, 작업 목록 탭, PDF 목차가 같이 바뀐다).

## 지금 상태

- 2026-11-04 공개, 2026-11-16 전면 개편(작업별 상세 페이지, 움직임, 인쇄용 PDF). 주소 https://chokyusong.github.io/ (저장소 `Chokyusong.github.io`, Pages는 `main` 브랜치 루트).
- 연락처는 회사 카카오톡 채널과 개인 이메일.

## 미리보기

```bash
py -3 -m http.server 8792 --directory .
```

## 쓰는 원칙

- 비공개 저장소는 "무엇을 만들었고 어떤 결과가 났는지"만 쓴다. 감지·연결 방식 같은 핵심 로직, 서버 주소·키, 고객 정보는 쓰지 않는다.
- 그림은 실제 화면이고 예시 데이터로 찍은 것만 쓴다(홈페이지 구축 사례에 공개된 그림과 같은 것). AI로 만든 그림은 캡션에 밝힌다.
- 숫자는 저장소 기록과 README에 있는 것만 쓴다(2026-11-15 기준).
- PANDAWA는 이름도 쓰지 않는다. 관리자 화면처럼 여러 서비스가 한 화면에 나오는 그림은 올리기 전에 그 이름이 없는지 본다(로그인 서버 그림은 그 메뉴와 카드를 지운 판).
- CCTV는 관제(지켜보기)만, bighand는 "후원 데이터 집계 서버"로만 소개한다. 수집 방식과 후원자 정보, 대시보드 화면은 쓰지 않는다.
- 이력서(`resume.html`·`resume-en.html`, `tools/build_resume.py`·`tools/resume_en.py`) 공개판에는 전화번호, 학력, 전 회사 이름을 넣지 않는다. 그 셋이 든 지원용 판은 저장소 밖에서만 만든다.
- 직무 이름은 `build_resume.py`의 `RESUME["title"]` 한 곳에서 정하고 첫 화면·인쇄판이 따라 쓴다. 한글판 숫자·사실을 바꾸면 `resume_en.py`도 같이 고친다.
- 그만둔 작업은 "개발 중"으로 두지 않고 뺀다.

© 2026 조규송. 그림과 글의 무단 재사용을 허용하지 않습니다.
