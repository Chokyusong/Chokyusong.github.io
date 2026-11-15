# -*- coding: utf-8 -*-
"""포트폴리오 페이지 만들기.

    py -3 tools/build.py

index.html(첫 화면), work/<slug>.html(작업마다 상세), print.html(PDF용 인쇄 판), resume.html(이력서)을
아래 PROJECTS 자료 하나에서 만든다. 글을 고칠 때는 이 파일을 고치고 다시 돌린다.
그림 크기는 assets/img 안의 실제 파일에서 읽는다.
"""
import html
import os
import re

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
CLIPS = "https://chokyusong.github.io/motion-parts/clips/"
KAKAO = "https://pf.kakao.com/_exgErX/chat"
EMAIL = "joung2156@gmail.com"
GITHUB = "https://github.com/Chokyusong"
YOUTUBE = "https://www.youtube.com/@onicsoft-ai"
PDF = "assets/cho-kyusong-portfolio.pdf"
ASOF = "2026년 11월 15일"
from build_resume import RESUME  # 직무 이름은 이력서와 한 곳에서 같이 쓴다
ROLE = RESUME["title"]

e = html.escape


def ver(path):
    """파일 내용으로 만든 짧은 꼬리표. 고치면 바뀌어서 브라우저가 옛 파일을 쓰지 않는다."""
    import hashlib
    with open(os.path.join(ROOT, path), "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:8]


def size(slug, name):
    with Image.open(os.path.join(IMG, slug, name + ".webp")) as im:
        return im.size


def img(slug, name, alt, rel, cls="", lazy=True, extra=""):
    w, h = size(slug, name)
    c = f' class="{cls}"' if cls else ""
    lz = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    return f'<img{c} src="{rel}assets/img/{slug}/{name}.webp" width="{w}" height="{h}" alt="{e(alt)}"{lz}{extra}>'


# ---------------------------------------------------------------- 자료
# 블록 종류: yt, states, gallery, compare, flow, perf, kpis, cards, points, live, scroller, clips, hub, video
PROJECTS = [
    {
        "slug": "autoled",
        "title": "AutoLed",
        "lines": ["AutoLed"],
        "kind": "대표 제품 · 판매 · 운영 중",
        "tags": "Windows 앱 · 판매 중",
        "year": "2025.10 —",
        "short": "후원이 들어오면 방송 연출을 자동으로 실행하는 Windows 앱",
        "summary": "후원 알림이 뜨는 순간 방송 연출을 자동으로 실행하고, 끝나면 원래 장면으로 돌려놓는 Windows 앱입니다. 혼자 기획하고 만들어 정식 판매하며, 업데이트와 운영까지 맡고 있습니다.",
        "preview": ("autoled", "ui-overview"),
        "meta": [("맡은 일", "기획 · 개발 · 배포 · 운영 (1인)"), ("시작", "2025년 10월"), ("현재", "2.1.0 판매 중 (2026.11)"),
                 ("기술", "Python, Tkinter, OBS WebSocket, Resolume OSC, Companion, Nuitka, Inno Setup"),
                 ("기록", "커밋 861 · 자동 테스트 2,051"), ("공개", "소스 비공개 · 설치 파일 공개")],
        "cover": ("autoled", "ui-timeline", "Timeline 편집기. 음원 파형 아래 OBS 장면, 와이와이캠, Companion, 레졸룸, 소리 트랙과 자동으로 놓인 장면 블록. 예시 음원"),
        "story": [
            ("문제", "후원이 들어올 때마다 방송 중인 사람이 알림을 보고 장면을 바꾸고, 조명과 연출을 손으로 틀어야 했습니다. 방송을 하면서 동시에 하기에는 놓치는 순간이 많았습니다."),
            ("만든 것", "팬더TV, SOOP, 투네이션, 위플랩, 펀네이션 후원 알림을 감지해 <strong>후원 개수에 맞춘 OBS 장면 전환, Resolume LED 칼럼, 조명과 카메라, 배경음악 음소거</strong>를 실행합니다. 연출은 음원에 맞춰 놓는 시간축 편집기(Timeline)로 직접 짭니다."),
            ("결과", "버튼을 누르지 않아도 후원이 들어오는 순간 연출이 실행되고 스스로 원래 장면으로 돌아옵니다. 처음 설치한 사람도 준비 단계 화면만 따라 하면 방송을 시작할 수 있습니다. 지금 유료 고객 약 15명이 실제 방송에 쓰고 있습니다."),
        ],
        "blocks": [
            ("states", {"title": "상태를 눌러 보세요", "text": "기본창은 지금 무슨 일이 일어나는지 한눈에 보이게 다섯 가지 상태로 나눴습니다. 아래 버튼을 누르면 실제 화면이 바뀝니다.", "items": [
                ("state-0", "연결 필요", "OBS나 장비가 아직 연결되지 않은 상태. 무엇을 연결하면 되는지 알려 줍니다."),
                ("state-1", "대기", "연결은 끝났고, 감시를 시작하기 전입니다."),
                ("state-2", "감시 중", "플랫폼 후원 알림을 지켜보는 중입니다."),
                ("state-3", "실행 중", "후원이 들어와 연출을 실행하고 있습니다. 끝나면 원래 장면으로 돌아갑니다."),
                ("state-4", "잠금", "정해 둔 규칙에 따라 새 연출을 막아 둔 상태입니다.")]}),
            ("gallery", {"title": "처음 켠 사람을 위한 준비 단계", "text": "설명서를 읽지 않아도 되도록, 처음 켜면 할 일을 순서대로 보여 주고 끝난 단계는 지워 나갑니다.", "group": "onboarding", "fit": True, "w": "w3", "ar": "360 / 660", "items": [
                ("onboarding-1", "처음 켠 화면. 준비할 일을 순서대로 보여 줍니다."),
                ("onboarding-2", "연결이 끝나면 다음 단계(매핑 불러오기)로 넘어갑니다."),
                ("onboarding-3", "기본 장면 만들기 단계."),
                ("onboarding-4", "카메라 프로그램까지 연결하는 단계."),
            ]}),
            ("gallery", {"title": "Timeline 연출 편집기", "text": "음원 파형 위에 장면, 조명, 카메라, 소리 블록을 놓아 연출을 짭니다. 자동 연출 만들기로 초안을 한 번에 깔고 손으로 다듬습니다.", "group": "timeline", "items": [
                ("ui-timeline", "Timeline 편집기 전체 화면. 예시 음원.", "w8"),
                ("timeline-auto-dialog", "자동 연출 만들기 설정. 언제 바꿀지, 어떤 장면을 쓸지, 어디에 깔지 고르면 초안이 깔립니다.", "w4", True),
                ("timeline-auto-result", "자동 연출 만들기를 누른 직후. 음악 박자에 맞춰 장면 블록이 깔렸습니다.", "w6"),
                ("timeline-blocks", "장면, 조명, 카메라, 연출 영상 블록을 트랙마다 놓은 모습.", "w6"),
            ]}),
            ("gallery", {"title": "관리센터", "text": "방송에 필요한 설정을 한곳에 모았습니다. 화면은 모두 예시 데이터로 띄워 찍었습니다.", "group": "manage", "items": [
                ("ui-overview", "개요. 왼쪽 기본창은 준비 단계와 연결 상태, 오른쪽은 할 일과 장비별 연결 상태.", "w6"),
                ("mgmt-mapping", "후원 연출 표. 후원 개수마다 어떤 칼럼, 장면, 연출 영상을 실행할지 정합니다. 예시 매핑 156개.", "w6"),
                ("ui-watcher", "플랫폼 감시. 플랫폼마다 감시 상태를 보고, 연출 시점을 음악에 맞춥니다.", "w6"),
                ("ui-settings", "설정. 연출 끝 여유, 연출 최소 코인, 잠금(LOCK) 같은 방송 규칙.", "w6"),
                ("mgmt-mute", "음소거. 후원 연출 때 정해 둔 프로그램의 소리를 끄고, 끝나면 다시 켭니다.", "w6"),
                ("mgmt-profiles", "프로필. 매핑, OBS, 레졸룸, 음소거 설정을 한 묶음으로 바꿔 씁니다.", "w6"),
                ("mgmt-connect", "연결. OBS, 레졸룸, 와이와이캠, Companion 연결을 켜고 끕니다.", "w6"),
                ("mgmt-help", "도움말. 자주 묻는 질문과 가이드 영상을 앱 안에서 봅니다.", "w6"),
                ("alert-import", "알림 설정에서 매핑 불러오기. 후원 알림에 이미 만들어 둔 개수 구간을 그대로 가져옵니다.", "w4", True),
                ("status-trouble", "문제가 생기면 무엇이 안 되는지 상태 화면에 바로 띄웁니다.", "w4", True),
                ("state-3", "기본창. 연출을 실행하는 중.", "w4", True),
            ]}),
            ("points", {"title": "판매하고 운영하려고 한 일", "items": [
                ("ph-arrows-clockwise", "앱 안에서 새 버전을 알리고 바로 업데이트합니다. 업데이트 정보에는 서명과 SHA-256 체크섬을 붙입니다."),
                ("ph-user-circle", "계정과 이용 기간은 직접 만든 로그인 서버가 확인합니다."),
                ("ph-cpu", "소스를 기계어로 컴파일(Nuitka)하고 설치 파일(Inno Setup)로 배포합니다."),
                ("ph-test-tube", "자동 테스트 2,051개를 통과시키고, 실제 OBS에서 한 번 더 확인한 뒤 내보냅니다."),
                ("ph-bug-beetle", "방송 중 화면이 멈추는 문제는 멈추는 조건부터 다시 만들어 찾았습니다. 고치기 전 3번 모두 멈추던 상황이, 고친 뒤 5번 모두 정상으로 돌아왔습니다."),
            ]}),
            ("yt", {"title": "영상으로 보기", "text": "AutoLed 홍보영상과, 제품을 만든 과정을 담은 유튜브 영상입니다.", "items": [
                ("yISU4NWuGQY", "AutoLed 홍보영상 | 후원이 들어오면, 방송이 알아서"),
                ("OynwWtQM3Lg", "BJ 방송 자동화 프로그램, 1년 손님 한 곳에서 BJ 10명까지")]}),
        ],
        "notice": "소스 코드와 후원 감지 방식은 공개하지 않습니다. 공개 저장소에는 설치 파일만 둡니다. 화면은 예시 데이터로 띄워 찍었습니다.",
        "links": [("제품 페이지", "https://onicsoft.co.kr/autoled.html"), ("설치 파일 저장소", "https://github.com/Chokyusong/AutoLed-Releases")],
    },
    {
        "slug": "astra",
        "title": "ASTRA 엔터테인먼트 홈페이지",
        "lines": ["ASTRA", "엔터테인먼트 홈페이지"],
        "kind": "손님 홈페이지 · 제작 중",
        "tags": "웹 · 디자인 · 모션",
        "year": "2026.11",
        "short": "엔터 회사 홈페이지 8쪽, 직접 눌러 보는 움직이는 시안",
        "summary": "크리에이터 매니지먼트, 개인방송, 브랜드·미디어 제작을 하는 엔터테인먼트 회사의 홈페이지 8쪽을 움직이는 시안으로 만들었습니다. 아래 창은 그림이 아니라 실제 시안이라 직접 스크롤하고 눌러 볼 수 있습니다.",
        "preview": ("astra", "home-pc"),
        "meta": [("맡은 일", "기획 · 디자인 · 프런트엔드 · 모션 (1인)"), ("시작", "2026년 11월"), ("상태", "움직이는 시안 확인 단계"),
                 ("기술", "HTML, CSS, JavaScript · 실제 사이트는 Next.js와 PHP 백엔드"), ("기록", "커밋 280"), ("손님", "엔터테인먼트 회사")],
        "cover": None,
        "first": ("live", {}),
        "story": [
            ("의뢰", "크리에이터 매니지먼트, 개인방송, 브랜드·미디어 제작을 하는 엔터테인먼트 회사의 홈페이지입니다. 손님이 보낸 PPT 초안 8장에서 출발했습니다."),
            ("만든 것", "홈, 회사소개, MCN, 브랜드, 엔터테인먼트, 미디어, 협력사, CONTACT 8쪽입니다. 홈은 ASTRA 글자와 WE MAKE NEXT를 코드로 움직이는 그림 배경 위에 띄우고, MCN 첫 화면은 사무실 사진 한 장에 깊이를 넣어 <strong>카메라가 둘러보듯</strong> 움직입니다. 쪽마다 스크롤에 맞춰 장면이 바뀌고, 휴대폰 화면도 따로 맞췄습니다."),
            ("진행", "와이어프레임, 디자인 시안, 움직이는 시안 순서로 확인받으며 만들고 있습니다. 실제 사이트는 Next.js로 만든 화면과 전용 PHP 백엔드(관리자, 블로그, 지원 양식, 메일, 통계)를 웹호스팅에 올리는 방식이고, 이 과정을 다음 손님에게도 쓸 수 있게 공통 부품과 검사 도구로 함께 정리하고 있습니다."),
        ],
        "blocks": [
            ("flow", {"title": "만드는 순서", "items": [("PPT 초안", "손님이 보낸 8장"), ("와이어프레임", "쪽마다 내용과 순서"), ("디자인 시안", "색, 글꼴, 사진"), ("움직이는 시안", "지금 단계", True), ("실제 사이트", "Next.js + PHP 백엔드")]}),
            ("gallery", {"title": "쪽마다 첫 화면", "text": "움직이는 시안의 첫 화면을 찍은 것입니다. 실제 움직임은 위 창에서 볼 수 있습니다.", "group": "astra", "items": [
                ("home-pc", "홈. 흑백 그림 배경 위에 ASTRA 글자가 떠오릅니다.", "w8"),
                ("home-mobile", "홈 휴대폰 화면.", "w4", True),
                ("mcn-pc", "MCN. 사무실 사진 한 장에 깊이를 넣어 카메라가 둘러보듯 움직입니다.", "w6"),
                ("brand-pc", "브랜드. 큰 글자와 모델 사진, 흐르는 분야 이름.", "w6"),
                ("entertainment-pc", "엔터테인먼트.", "w6"),
                ("media-pc", "미디어.", "w6"),
                ("partners-pc", "협력사.", "w6"),
                ("contact-pc", "크리에이터 지원 양식. 시안이라 실제로 접수되지는 않습니다.", "w6"),
            ]}),
        ],
        "notice": "2026년 11월 11일 시안 판입니다. 지원·문의 양식은 화면만 있고 실제로 접수되지 않습니다. 배경 그림 일부는 AI로 만들었습니다.",
        "links": [("시안 새 창으로 열기", "../works/astra/motion/home.html")],
    },
    {
        "slug": "cctv",
        "title": "CCTV · BJ 방송 통합 관제",
        "lines": ["CCTV", "BJ 방송 통합 관제"],
        "kind": "방송 관제 프로그램 · 비공개 저장소",
        "tags": "Windows 앱 · 서버형",
        "year": "2026.10",
        "short": "BJ 최대 60명의 방송을 한 화면에서 지켜보는 관제 프로그램",
        "summary": "소속 BJ 최대 60명의 방송을 한 화면에서 지켜보고, 챙겨야 할 일은 텔레그램으로 알려 주는 관제 프로그램입니다.",
        "preview": ("cctv", "cover"),
        "meta": [("맡은 일", "기획 · 개발 · 배포 (1인)"), ("시작", "2026년 10월"), ("형태", "PC 설치형 · 서버형"), ("기술", "Python, Windows, Telegram, SQLite")],
        "cover": ("cctv", "cover", "CCTV 관제 화면. 방송 중인 BJ 영상 타일과 오른쪽 이벤트 기록. 예시 데이터"),
        "story": [
            ("문제", "매니저가 BJ 방을 하나씩 돌며 방송을 확인했습니다. 언제 켜고 몇 시간 했는지는 BJ 말에 기대야 했고, 큰 후원이나 채팅 끊김은 다음 날에야 알았습니다."),
            ("만든 것", "등록한 BJ의 방송 시작과 종료를 약 1분마다 확인해, 방송 중인 방을 <strong>타일로 동시에</strong> 보여 주고 채팅을 함께 띄웁니다. 방송마다 하트, 채팅 참여, 매일 10시 순위를 기록하고 정해 둔 상황은 텔레그램으로 알립니다."),
            ("결과", "매니저 한 명이 여러 BJ를 한 화면과 휴대폰 알림으로 챙깁니다. 방송 기록이 쌓여 면담 때 바로 꺼내 봅니다."),
        ],
        "blocks": [
            ("cards", {"title": "무엇을 하나", "cols": 3, "items": [
                ("등록만 하면 이어서", "운영자는 BJ 아이디나 방송 주소만 등록합니다. 방송이 켜지면 그 BJ가 LIVE로 바뀌어 위로 올라오고 영상과 채팅이 이어집니다."),
                ("한 화면에서 60명", "방송 중인 방을 타일로 동시에 보여 주고, 타일을 누르면 크게 보기와 소리, 그 방 채팅이 열립니다. 채팅은 등급, 매니저, 후원, 입장을 색으로 구분합니다."),
                ("방송마다 쌓이는 기록", "최근 방송의 시작·종료 시각, 하트 합계, 채팅 참여자 수가 방송마다 저절로 쌓입니다. 매일 오전 10시 순위를 기록해 전날과 비교합니다."),
                ("중요한 순간은 텔레그램으로", "방송 켜짐·꺼짐, 큰 하트, 채팅이 오래 멈춤, 매일 10시 보고 같은 알림을 종류별로 켜고 끕니다. 단체방에 연결하면 관리자 여러 명이 함께 받습니다."),
                ("PC를 꺼도 24시간", "서버에 켜 두면 휴대폰에서는 앱 모양 화면으로 바뀌고, 텔레그램 버튼만 눌러 방송 중인 BJ와 하트 순위를 받아 봅니다. 프로그램이 멈추면 저절로 다시 켭니다."),
                ("무리 없이, 안전하게", "플랫폼에 무리가 가지 않게 확인 간격과 동시 요청 수를 제한합니다. 보관하는 로그인 정보는 그 PC에서만 풀리게 암호화합니다."),
            ]}),
            ("gallery", {"title": "화면", "text": "모두 예시 데이터로 띄워 찍은 화면입니다.", "group": "cctv", "items": [
                ("chat", "타일을 누르면 그 방 채팅이 열립니다. 등급, 매니저, 하트, 입장을 색으로 구분합니다.", "w6"),
                ("bj-list", "BJ 목록. 매일 10시 순위를 전날과 비교하고, 방송마다 하트와 채팅 참여가 쌓입니다.", "w6"),
                ("mobile", "서버형을 휴대폰으로 열면 앱 모양 화면. 아래 탭으로 모니터링, BJ 목록, 설정을 넘깁니다.", "w6"),
                ("telegram", "텔레그램 알림과 버튼 메뉴. 한 BJ의 이번 방송 하트, 채팅, 순위를 버튼으로 받아 봅니다.", "w6"),
            ]}),
        ],
        "notice": "플랫폼 연결 방식과 소스 코드는 공개하지 않습니다. 화면은 예시 데이터입니다.",
        "links": [],
    },
    {
        "slug": "enter-payroll",
        "title": "BJ 엔터 주간 정산",
        "lines": ["BJ 엔터", "주간 정산"],
        "kind": "업무 자동화 · 비공개 저장소",
        "tags": "Windows 앱 · 정산",
        "year": "2026.10",
        "short": "엑셀 여러 장으로 하던 주간 정산을 프로그램으로",
        "summary": "엑셀 시트 여러 장으로 하던 주간 정산을, 자료 수집부터 계산까지 프로그램이 맡고 담당자는 예외만 확인해 확정하도록 바꿨습니다. 기존 정산 엑셀 48주 치와 맞춰 보니 47주의 계산 결과가 같았습니다.",
        "preview": ("enter-payroll", "cover"),
        "meta": [("맡은 일", "기획 · 개발 · 배포 (1인)"), ("시작", "2026년 10월"), ("기술", "Python, PySide6, SQLite, Nuitka"), ("기록", "커밋 28 · 자동 테스트 141")],
        "cover": ("enter-payroll", "cover", "이번 주 받을 돈, 줄 돈, 회사 몫 카드와 확인이 필요한 항목 목록. 예시 데이터"),
        "story": [
            ("문제", "매주 BJ 정산을 엑셀 시트 여러 장과 수식으로 했습니다. 개인방송과 경쟁방마다 나누는 방식이 달랐고, 수식이 틀리거나 자료가 빠져도 확정 전에 알아채기 어려웠습니다."),
            ("만든 것", "사무실 PC에 설치하는 Windows 프로그램입니다. 정해진 요일에 관리자 화면의 자료를 가져와 BJ와 맞추고, 개인방송, 경쟁방, 회사 수익, 지분 분배까지 계산합니다."),
            ("원칙", "<strong>모르는 조건은 0원으로 채우지 않고</strong> 그 줄만 보류합니다. 원본 합계와 계산 금액이 원 단위까지 맞아야 확정 버튼이 열립니다. 확정한 주는 다시 계산되지 않습니다."),
        ],
        "blocks": [
            ("flow", {"title": "매주 흐름", "text": "앞의 세 단계는 정해 둔 요일과 시각에 프로그램이 알아서 하고, 담당자는 남은 예외만 보고 확정합니다.", "items": [
                ("자료 수집", "관리자 화면에서 가져옴"), ("원본 합계 대조", "원 단위까지"), ("자동 정산", "방식별 계산"), ("예외 확인", "담당자가 보는 곳", True), ("정산 확정", "다시 계산 안 함"), ("지급목록", "계좌·금액 정리")]}),
            ("cards", {"title": "틀리지 않게 만든 장치", "cols": 2, "items": [
                ("모르면 0원으로 채우지 않는다", "등록되지 않은 BJ, 계약이 없는 BJ, 조건이 정해지지 않은 계산은 그 줄만 보류합니다. 무엇을 하면 되는지 버튼과 함께 띄우고, 조건이 정해지면 보류한 줄만 다시 계산합니다."),
                ("숫자를 두 번 맞춘다", "원본에 나온 합계와 프로그램이 계산한 금액이 다르면 확정 버튼이 막히고 어느 줄이 다른지 보여 줍니다. 같은 자료를 다시 넣어도 두 번 계산되지 않습니다."),
                ("계약은 날짜별로", "계약이 바뀌면 적용 시작일을 붙여 새로 등록하고, 지난 주 정산은 그때 계약으로 남습니다. 확정을 풀려면 사유를 적어야 하고, 이미 지급한 주는 풀 수 없습니다."),
                ("세금과 지급까지", "원천세와 부가세는 회사 수익과 따로 '보관해야 할 세금'으로 모아 납부 기한과 함께 보여 줍니다. 송금은 은행에서 직접 하고, 거래내역과 연결해 지급 완료를 확인합니다."),
            ]}),
            ("gallery", {"title": "화면", "text": "업체 이름과 화면 속 사람, 금액, 계좌는 모두 가상입니다. 예시 데이터로 실제 프로그램을 돌려 찍었습니다.", "group": "payroll", "items": [
                ("calc", "받는 사람별 자동 계산 내역. 조건이 정해지지 않은 줄은 0원이 아니라 '보류'로 남습니다.", "w6"),
                ("rooms", "경쟁방은 회차, 출연자, 하트를 경쟁방 장부에서 정해 둔 방식대로 나눕니다.", "w6"),
                ("bank", "은행 거래내역을 불러와 지급과 맞춥니다. 반복 거래는 규칙으로 자동 분류합니다.", "w6"),
                ("tax", "원천세와 부가세는 회사 몫이 아니라 낼 세금으로 따로 모아 보여 줍니다.", "w6"),
            ]}),
            ("points", {"title": "자료를 지키는 방법", "items": [
                ("ph-desktop-tower", "웹 서버나 외부 접속 없이 사무실 PC에만 저장합니다."),
                ("ph-lock-key", "관리자 비밀번호는 그 PC의 Windows 계정으로만 풀리게 암호화합니다."),
                ("ph-hard-drives", "정해 둔 폴더(USB, NAS 등)로 자동 백업합니다."),
                ("ph-test-tube", "자동 테스트 141개가 계산과 화면 버튼까지 확인합니다."),
            ]}),
        ],
        "notice": "정산 계산 규칙과 고객 정보는 공개하지 않습니다. 업체 이름과 화면 속 사람, 금액은 모두 가상입니다.",
        "links": [],
    },
    {
        "slug": "ledger",
        "title": "납품 거래장부",
        "lines": ["납품 거래장부", "엑셀에서 프로그램으로"],
        "kind": "고객 맞춤 제작 · 업무 자동화",
        "tags": "엑셀 자동화 · Windows 앱",
        "year": "2026.09",
        "short": "두 번씩 적던 엑셀 장부를, 한 번 적으면 끝나는 프로그램으로",
        "summary": "엑셀 장부에 두 번씩 적던 납품과 입금을, 한 번 적으면 받을 돈까지 계산되는 Windows 프로그램으로 바꿨습니다. 엑셀을 먼저 고치고, 그래도 남는 문제 때문에 프로그램으로 옮겼습니다.",
        "preview": ("ledger", "cover"),
        "meta": [("맡은 일", "분석 · 엑셀 자동화 · 프로그램 개발 (1인)"), ("시작", "2026년 9월"), ("기술", "Python, SQLite, Excel 연동, Windows"), ("확인", "자동 테스트 14 · 화면 테스트 15 · 엑셀 왕복 4")],
        "cover": ("ledger", "cover", "엑셀 장부와 거래장부 프로그램을 나란히 놓은 비교 화면. 예시 데이터"),
        "story": [
            ("자동화 전", "마트 전단, POP, 현수막을 납품하는 업체가 같은 거래를 엑셀 총원장과 거래처 시트에 두 번씩 적고, 월말에는 두 합계의 차액을 손으로 맞췄습니다. 입금내역을 붙여넣을 때마다 수식이 깨지곤 했습니다."),
            ("1단계 · 엑셀", "먼저 엑셀을 고쳤습니다. 총원장 한 곳에만 적으면 거래처 시트와 현황판이 수식으로 채워지게 했고, 차액이 0이면 정상이라고 알려 주는 검증 칸도 넣었습니다."),
            ("남은 문제", "행을 붙여넣거나 칸에 직접 쓰면 수식이 지워졌습니다. 그래서 수식이 아예 없는 프로그램으로 옮겼습니다."),
            ("2단계 · 프로그램", "메뉴는 '납품 적기', '입금 적기'처럼 할 일 이름입니다. 통장 내역을 붙여넣으면 <strong>입금자 이름으로 거래처를 찾아 주고</strong> 이미 적은 입금은 뺍니다. 엑셀로 저장하면 예전 장부 모양 그대로 나옵니다."),
            ("드러난 불일치", "옮기면서 원본 장부끼리 맞지 않는 줄이 드러났습니다. 임의로 고치지 않고 목록으로 정리해 고객에게 확인받았습니다."),
        ],
        "blocks": [
            ("compare", {"title": "끌어서 비교해 보세요", "text": "왼쪽은 손으로 적던 총원장, 오른쪽은 엑셀 자동화 뒤 총원장입니다. 회색 칸(합계, 잔액, 지점)은 자동 계산입니다.", "before": "01-before-ledger", "after": "04-excel-ledger", "lb": "자동화 전", "la": "엑셀 자동화 뒤"}),
            ("gallery", {"title": "자동화 전", "group": "ledger", "label": True, "items": [
                ("01-before-ledger", "자동화 전 총원장. 입금과 납품을 손으로 적고 잔액 수식도 줄마다 따로였습니다. 예시 데이터로 재현.", "w4"),
                ("02-before-client-sheet", "같은 거래를 거래처 시트에 한 번 더 적던 모습. 예시 데이터로 재현.", "w4"),
                ("03-before-summary", "시트 합계와 총원장 합계를 손으로 대조하던 표. 예시 데이터로 재현.", "w4"),
            ]}),
            ("gallery", {"title": "1단계 · 엑셀 자동화", "group": "ledger", "label": True, "items": [
                ("04-excel-ledger", "엑셀 자동화 뒤 총원장. 회색 칸은 자동 계산. 예시 데이터.", "w4"),
                ("05-excel-client-sheet", "거래처 시트는 총원장에서 그 거래처 줄만 날짜순으로 저절로 채워집니다. 예시 데이터.", "w4"),
                ("06-excel-dashboard", "거래처별 받을 돈과 검증 블록(차액 0이면 정상). 예시 데이터.", "w4"),
            ]}),
            ("gallery", {"title": "2단계 · 프로그램 '거래장부'", "group": "ledger", "label": True, "items": [
                ("07-app-overview", "거래장부 첫 화면. 아직 받을 돈 합계와 거래처별 미수금. 예시 데이터.", "w6"),
                ("08-app-delivery", "납품 적기. 거래처를 고르면 지금 받을 돈과 지난 납품이 보입니다. 예시 데이터.", "w6"),
                ("09-app-bank-import", "통장 입금내역을 붙여넣으면 입금자 이름으로 거래처를 찾고, 이미 적은 입금은 뺍니다. 예시 데이터.", "w6"),
                ("10-app-client-ledger", "거래처별 장부. 전년이월부터 잔액이 줄마다 계산됩니다. 예시 데이터.", "w6"),
                ("11-app-excel-export", "프로그램에서 저장한 엑셀. 예전 장부와 같은 모양으로 나옵니다. 예시 데이터.", "w8"),
            ]}),
        ],
        "notice": "고객 이름과 실제 장부 숫자는 공개하지 않습니다. 화면 속 업체와 금액은 모두 예시입니다.",
        "links": [("구축 사례 전체 보기", "https://onicsoft.co.kr/work.html?slug=mart-flyer-ledger")],
    },
    {
        "slug": "login-server",
        "title": "로그인 · 라이선스 서버",
        "lines": ["로그인 ·", "라이선스 서버"],
        "kind": "서버 · 운영 · 비공개 저장소",
        "tags": "서버 · 관리자 화면",
        "year": "2026.08 —",
        "short": "프로그램 계정과 이용 기간을 확인하는 서버와 관리자 화면",
        "summary": "AutoLed와 다른 프로그램이 함께 쓰는 계정과 이용 기간을 확인하는 서버와 관리자 화면입니다. 입금 확인과 기간 연장, 홈페이지 블로그까지 이 서버가 맡습니다.",
        "preview": ("login-server", "dashboard"),
        "meta": [("맡은 일", "기획 · 개발 · 운영 (1인)"), ("시작", "2026년 8월"), ("기술", "Python, FastAPI, SQLite, Nginx, systemd"), ("기록", "커밋 286")],
        "cover": ("login-server", "dashboard", "관리자 첫 화면. 회원, 입금, 방문, 서버 상태를 한 화면에서 봄. 예시 자료"),
        "story": [
            ("목적", "AutoLed를 판매하려면 계정과 이용 기간을 관리하고, 앱이 켜질 때마다 확인할 서버가 필요했습니다."),
            ("만든 것", "앱 로그인과 이용권 검증을 하는 서버와 관리자 화면입니다. <strong>은행 입금 알림을 읽어 이용 기간을 자동으로 늘리고</strong>, 새 프로그램은 서버 코드를 고치지 않고 관리자 화면에서 등록해 같은 로그인을 씁니다."),
            ("함께 맡는 일", "홈페이지 블로그와 구축 사례를 올리는 작은 CMS, 방문 통계도 이 서버가 맡습니다."),
        ],
        "blocks": [
            ("hub", {"title": "무엇과 이어져 있나", "core": ("로그인 서버", "계정 · 이용권 · 관리자"), "items": [
                ("데스크톱 앱", "AutoLed 등 프로그램이 켜질 때 로그인과 이용권을 확인"),
                ("입금 알림", "입금이 확인되면 이용 기간을 자동으로 연장"),
                ("관리자 화면", "회원, 입금, 글, 서버 상태를 한곳에서 관리"),
                ("홈페이지", "블로그 글과 구축 사례 페이지, 방문 통계")]}),
            ("points", {"title": "운영하며 챙기는 것", "items": [
                ("ph-users-three", "관리자 여러 명과 역할, OTP, 모든 쓰기에 감사 기록을 남깁니다."),
                ("ph-signature", "앱이 받는 토큰은 서버 키로 서명합니다."),
                ("ph-git-branch", "커밋마다 별도 폴더로 배포하고 버전 태그를 달아, 문제가 생기면 이전 버전으로 바로 돌아갑니다."),
                ("ph-shield-check", "지나치게 잦은 접속은 자동으로 막고, 서버가 멈추면 다시 켜지게 둡니다."),
            ]}),
            ("gallery", {"title": "관리자 화면", "text": "실제 운영 자료가 아니라 예시 자료로 띄워 찍었습니다. 계정, 이름, 금액, 방문 수는 모두 예시입니다.", "group": "admin", "items": [
                ("posts", "블로그 글 목록. 블로그 글과 구축 사례를 여기서 올리고 고칩니다.", "w6"),
                ("case-edit", "구축 사례 편집. 문제, 만든 것, 결과 칸을 채우면 사이트에 그대로 나옵니다.", "w6"),
                ("dashboard", "관리자 첫 화면. 회원, 입금, 방문, 서버 상태 요약.", "w6"),
            ]}),
        ],
        "notice": "서버 주소, 키, 검증 절차의 세부는 공개하지 않습니다. 화면은 예시 자료로 띄워 찍었습니다.",
        "links": [],
    },
    {
        "slug": "bighand",
        "title": "후원 데이터 집계 서버",
        "lines": ["후원 데이터", "집계 서버"],
        "kind": "데이터 수집 서버 · 비공개 저장소",
        "tags": "서버 · 성능 개선",
        "year": "2026.10",
        "short": "후원 데이터를 실시간으로 모아 집계하는 24시간 서버",
        "summary": "라이브 방송 수백 곳의 후원 데이터를 실시간으로 모아 집계하는 24시간 서버입니다. 1,350만 건으로 부하 시험을 해 병목을 고쳐 대시보드 응답을 수십 배 줄였습니다.",
        "preview": None,
        "pv_stat": ("22초 → 0.25초", "1,350만 건 부하 시험에서 대시보드 첫 화면"),
        "meta": [("맡은 일", "기획 · 개발 · 운영 (1인)"), ("시작", "2026년 10월"), ("기술", "Python, Linux, systemd, GitHub Actions"), ("기록", "커밋 67 · 자동 테스트 84")],
        "cover": None,
        "first": ("perf", {}),
        "story": [
            ("목적", "AutoLed와 조회 화면에 쓸 방송 후원 통계를 직접 모으는 서버가 필요했습니다."),
            ("만든 것", "공개 라이브 방송 수백 곳의 후원 기록을 모아 저장하고 집계합니다. 방송 목록은 1분마다 새로 확인합니다. 관리자만 보는 대시보드에서 기간별 방송 순위와 집계를 봅니다."),
            ("성능", "시험용으로 만든 3달 치 기록 1,350만 건으로 부하 시험을 해 병목을 고쳤습니다. 실제 운영에서는 <strong>하루 78,844건(2026년 10월 6일 기록)을 1vCPU, 1GB 서버 한 대</strong>로 받았습니다."),
        ],
        "blocks": [
            ("kpis", {"title": "운영 숫자", "items": [("78,844건", "하루에 받은 후원 기록 (2026.10.6)"), ("1vCPU · 1GB", "서버 한 대로 운영"), ("약 20초", "재부팅 시험에서 모두 복구"), ("84개", "코드가 바뀌면 도는 자동 테스트")]}),
            ("points", {"title": "멈추지 않게, 잃지 않게", "items": [
                ("ph-power", "서비스는 부팅하면 저절로 켜지고, 5분마다 멈춤을 감시합니다."),
                ("ph-lock-key", "매일 암호화 백업을 받고, 매달 백업을 실제로 풀어 건수를 맞춰 보는 복원 연습을 자동으로 돌립니다."),
                ("ph-pulse", "바깥 감시는 GitHub Actions가 30분마다 합니다."),
                ("ph-user-minus", "요청한 사람의 기록은 지우고 더 모으지 않는 수집 거부 목록을 둡니다."),
            ]}),
        ],
        "notice": "플랫폼 연결 방식, 모은 데이터, 대시보드 화면은 공개하지 않습니다. 실제 사람 이름이 보이는 화면이라 캡처도 싣지 않았습니다.",
        "links": [],
    },
    {
        "slug": "onicsoft-homepage",
        "title": "ONICSOFT 홈페이지",
        "lines": ["ONICSOFT", "홈페이지"],
        "kind": "운영 중인 사이트",
        "tags": "웹 · 서버 운영",
        "year": "2026.08 —",
        "short": "제품 데모와 블로그까지 직접 만들고 운영하는 회사 사이트",
        "summary": "회사 소개, 제품, 모션그래픽, 구축 사례, 블로그를 담은 회사 홈페이지를 빌드 도구 없이 만들고, 올라가는 서버까지 직접 운영합니다.",
        "preview": ("onicsoft-homepage", "cover-pc"),
        "meta": [("맡은 일", "기획 · 디자인 · 개발 · 운영 (1인)"), ("시작", "2026년 8월"), ("기술", "HTML, CSS, JavaScript · 서버는 Python"), ("기록", "커밋 235")],
        "cover": None,
        "first": ("scroller", {}),
        "story": [
            ("만든 것", "빌드 도구 없는 정적 사이트입니다. 회사 소개, 서비스, 제품, 모션그래픽, 구축 사례, 블로그, 문의 페이지가 있고 PC와 휴대폰 화면에 맞춥니다."),
            ("눌러 보는 화면", "AutoLed 데모와 자동화 체험, 절감 계산을 페이지에서 바로 실행합니다. <strong>업종별 홈페이지 견본 20여 개</strong>를 만들어 직접 넘겨 볼 수 있게 했습니다."),
            ("검색", "사이트맵과 검색용 정보를 갖추고, 블로그 글은 서버가 글마다 페이지를 만들어 보여 줍니다."),
        ],
        "blocks": [
            ("points", {"title": "사이트 밖에서 하는 일", "items": [
                ("ph-cloud", "국내 클라우드 서버를 직접 세팅하고 운영합니다. 도메인과 HTTPS 연결까지."),
                ("ph-note-pencil", "관리자 화면에서 블로그 글과 구축 사례를 직접 올리고 고칩니다."),
                ("ph-tree-structure", "글이 늘면 검색용 사이트맵을 서버가 알아서 다시 만듭니다."),
                ("ph-shield-check", "보안 설정과, 지나치게 잦은 접속 자동 차단."),
            ]}),
        ],
        "notice": "화면은 공개된 사이트를 찍은 것입니다. 서버 주소와 설정은 공개하지 않습니다.",
        "links": [("onicsoft.co.kr", "https://onicsoft.co.kr/"), ("홈페이지 견본", "https://onicsoft.co.kr/portfolio.html")],
    },
    {
        "slug": "motion",
        "title": "코드로 만드는 모션그래픽",
        "lines": ["코드로 만드는", "모션그래픽"],
        "kind": "영상 작업실 · 공개 미리보기",
        "tags": "three.js · Blender · 영상",
        "year": "2026.09 —",
        "short": "편집 프로그램 없이 코드로 만드는 영상과 효과 271종",
        "summary": "영상 편집 프로그램 없이 HTML, three.js, Blender로 화면을 그리고 프레임마다 찍어 영상을 만듭니다. 효과 271종을 도감으로 쌓아 두고 홍보영상과 방송 효과에 씁니다.",
        "preview": None,
        "pv_video": "chromeText",
        "meta": [("맡은 일", "기획 · 개발 · 영상 (1인)"), ("시작", "2026년 9월"), ("기술", "JavaScript, three.js, Blender, ffmpeg"), ("기록", "커밋 257 · 효과 271종 (공개 95)")],
        "cover": None,
        "first": ("video", {"clip": "fireBurst", "alt": "Blender로 만든 불꽃 폭발 효과"}),
        "story": [
            ("만든 것", "영상 편집 프로그램 없이 화면을 HTML, three.js, Blender로 그리고 프레임마다 찍어 MP4로 만듭니다. 배경음악도 코드로 합성해 사용 권리가 분명합니다."),
            ("쌓아 둔 것", "글자, 장면 전환, 3D, 방송 화면 등 <strong>12갈래로 나눈 모션 효과 도감 271종</strong>(그중 95가지는 공개)과, 미리보기와 타임라인으로 문구와 효과를 고치는 편집기가 있습니다."),
            ("쓰는 곳", "AutoLed 홍보영상, 유튜브 영상, 방송 후원 알림 효과를 여기서 만듭니다."),
        ],
        "blocks": [
            ("yt", {"title": "이렇게 만든 영상", "text": "모두 이 작업실에서 코드로 만든 영상입니다. 누르면 이 자리에서 재생됩니다.", "items": [
                ("I0QTxxemSAg", "오닉소프트 | 반복되는 모든 것을, 자동으로."),
                ("PQnVB7ns78A", "OVRA ONE 컨셉 광고 | 코드와 Blender로 만든 스마트워치 광고 (가상 제품)"),
                ("yISU4NWuGQY", "AutoLed 홍보영상 | 후원이 들어오면, 방송이 알아서"),
                ("AWeB3c9rIQM", "AI로 회사 홍보영상(모션그래픽) 만들기 — 만드는 과정")]}),
            ("clips", {"title": "효과 도감에서", "text": "271종 가운데 일부입니다. 화면에 보이면 저절로 재생됩니다.", "items": [
                ("chromeText", "크롬 글자", "3D"), ("fireBurst", "불꽃 폭발", "3D"), ("hologram", "홀로그램", "3D"), ("logo3D", "3D 로고", "3D"),
                ("glassBottle", "유리병 제품", "3D"), ("dotGlobe", "점 지구", "3D"), ("textCube", "글자 큐브", "3D"), ("blobSphere", "액체 구", "3D"),
                ("confetti3D", "3D 색종이", "3D"), ("glitchText", "글리치", "타이포"), ("extrudeText", "입체 글자", "타이포"), ("neonText", "네온사인", "타이포"),
                ("shatterText", "부서지는 글자", "타이포"), ("kineticStack", "포스터 글자", "타이포"), ("odometer", "숫자 롤링", "타이포"), ("charCascade", "한 글자씩", "글자"),
                ("alertPop", "후원 알림", "방송"), ("liveBadge", "LIVE 배지", "방송"), ("scoreboard", "스코어보드", "방송"), ("audioCircle", "원형 이퀄라이저", "음악 연동"),
                ("synthGrid", "신스웨이브", "배경"), ("meshGradient", "색 섞임 배경", "배경"), ("inkWipe", "잉크 번짐", "전환"), ("particleShape", "입자 로고", "3D")]}),
        ],
        "notice": "작업실 저장소는 재배포할 수 없는 글꼴이 들어 있어 비공개입니다. OVRA ONE은 가상 제품입니다.",
        "links": [("효과 95가지 미리보기", "https://chokyusong.github.io/motion-parts/"), ("모션그래픽 페이지", "https://onicsoft.co.kr/motion/"), ("유튜브 채널", YOUTUBE)],
    },
    {
        "slug": "pdf2obsidian",
        "title": "PDF2Obsidian",
        "lines": ["PDF2Obsidian"],
        "kind": "오픈소스 · MIT",
        "tags": "데스크톱 도구 · 공개",
        "year": "2026.06",
        "short": "PDF와 강의 자막을 옵시디언 노트로 바꾸는 도구",
        "summary": "PDF, 이미지, 강의 자막 파일을 옵시디언에서 바로 쓰는 마크다운 노트로 바꾸는 데스크톱 도구입니다. 파일을 내 PC 밖으로 보내지 않습니다.",
        "preview": ("pdf2obsidian", "gui"),
        "meta": [("맡은 일", "기획 · 개발 · 배포 (1인)"), ("시작", "2026년 6월"), ("기술", "Python, PySide6, Ollama(로컬), PyInstaller"), ("기록", "커밋 43 · 공개 저장소")],
        "cover": ("pdf2obsidian", "gui", "PDF2Obsidian 프로그램 화면. 예시 PDF와 강의 자막 파일을 불러온 모습"),
        "story": [
            ("만든 것", "PDF, 이미지, 강의 자막 파일을 옵시디언에서 바로 쓰는 마크다운 노트와 가벼운 그림 파일로 바꿉니다. 끌어다 놓으면 됩니다."),
            ("원칙", "<strong>파일을 서버로 보내지 않고 외부 AI API도 쓰지 않습니다.</strong> 요약이 필요하면 내 PC에 설치한 모델(Ollama)을 씁니다."),
            ("배포", "Windows용 실행 파일을 GitHub Releases로 내보내고, 코드가 바뀔 때마다 CI가 테스트합니다."),
        ],
        "blocks": [
            ("gallery", {"title": "변환 전과 뒤", "group": "pdf", "items": [
                ("before-after", "왼쪽 PDF가 오른쪽 옵시디언 노트로 바뀐 모습. 예시 자료.", "w8"),
                ("gui-course", "강의 자료를 불러온 화면.", "w4", True),
                ("obsidian-lecture", "강의 자막으로 만든 노트를 옵시디언에서 연 모습. 예시 자료.", "w8"),
                ("gui-lecture", "강의 자막 파일을 불러온 화면.", "w4", True),
            ]}),
        ],
        "notice": "누구나 쓰고 고칠 수 있는 MIT 라이선스로 공개했습니다. 화면 속 PDF와 자막은 예시 자료입니다.",
        "links": [("저장소 보기", "https://github.com/Chokyusong/pdf2obsidian")],
    },
]

# 작업 분류. 첫 화면 03 카드, 04 작업 목록 탭, 인쇄판 목차가 모두 이 분류를 쓴다.
# (키, 이름, 아이콘, 설명, 대표 그림(폴더, 이름) 또는 None, 속한 작업 순서)
CATS = [
    ("program", "프로그램", "ph-app-window", "설치해서 쓰는 Windows 프로그램과 도구입니다. 방송 자동화 제품 AutoLed는 직접 판매하고 업데이트까지 운영합니다.", ("autoled", "ui-timeline"), ["autoled", "cctv", "pdf2obsidian"]),
    ("automation", "업무 자동화", "ph-briefcase", "회사에서 사람이 손으로 반복하던 일을 그 회사에 맞춘 프로그램으로 바꿉니다. 지금까지 주간 정산과 거래장부를 만들었습니다.", ("ledger", "cover"), ["enter-payroll", "ledger"]),
    ("server", "서버", "ph-hard-drives", "로그인과 이용 기간을 확인하는 서버, 24시간 수집 서버를 세우고 감시와 백업까지 맡습니다.", ("login-server", "dashboard"), ["login-server", "bighand"]),
    ("web", "홈페이지", "ph-browser", "회사 사이트와 손님 홈페이지를 기획, 디자인, 개발하고 블로그와 구축 사례까지 운영합니다.", ("astra", "home-pc"), ["onicsoft-homepage", "astra"]),
    ("motion", "모션그래픽", "ph-film-strip", "편집 프로그램 없이 코드로 홍보영상과 효과를 만듭니다. 효과 271종을 만들었습니다.", None, ["motion"]),
]
CAT_OF = {sl: c[0] for c in CATS for sl in c[5]}
CAT_NAME = {c[0]: c[1] for c in CATS}
_order = [sl for c in CATS for sl in c[5]]
assert sorted(_order) == sorted(p["slug"] for p in PROJECTS), "분류에 빠지거나 겹친 작업이 있다"
PROJECTS.sort(key=lambda p: _order.index(p["slug"]))
N = len(PROJECTS)
FIELDS = [(ic, name, txt, sls, pic) for _, name, ic, txt, pic, sls in CATS]

# ---------------------------------------------------------------- 공통 틀

HEAD_SCRIPT = ("<script>(function(d){var r=d.documentElement;if(!window.matchMedia||!matchMedia('(prefers-reduced-motion: reduce)').matches){r.classList.add('anim');"
               "try{if(sessionStorage.getItem('pt')){r.classList.add('page-enter');sessionStorage.removeItem('pt')}}catch(e){}"
               "setTimeout(function(){if(!r.classList.contains('anim-ready'))r.classList.remove('anim','page-enter')},4000)}})(document)</script>")


def shell(title, desc, body, rel, og="assets/img/autoled/ui-overview.webp", home=False, robots=""):
    to = "" if home else f"{rel}index.html"
    nav = f"""<header class="nav"><div class="wrap nav-in">
  <a class="brand" href="{rel}index.html" aria-label="조규송 포트폴리오 처음으로"><span class="brand-mark" aria-hidden="true">{'<i></i>' * 9}</span>조규송 <small>CHO KYUSONG</small></a>
  <div class="nav-meta" aria-hidden="true"><span class="live-dot"></span>KST <span data-clock></span></div>
  <nav class="nav-links" aria-label="주요 메뉴"><a href="{to}#works">작업</a><a href="{to}#about">소개</a><a class="nav-keep" href="{rel}resume.html">이력서</a><a class="nav-keep" href="{rel}{PDF}">PDF</a><a class="nav-cta" href="{to}#contact">연락</a></nav>
</div></header>"""
    foot = f"""<footer class="foot wrap"><p>© 2026 조규송 (Cho Kyusong)</p><p>비공개 저장소의 소스 코드와 핵심 로직은 공개하지 않습니다. 화면 속 이름, 금액, 계정은 예시입니다.</p></footer>"""
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}<meta name="theme-color" content="#07090b">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 32 32%27%3E%3Crect width=%2732%27 height=%2732%27 rx=%277%27 fill=%27%2307090b%27/%3E%3Cg fill=%27%2345c6d6%27%3E%3Crect x=%277%27 y=%277%27 width=%275%27 height=%275%27/%3E%3Crect x=%2720%27 y=%277%27 width=%275%27 height=%275%27/%3E%3Crect x=%2713.5%27 y=%2713.5%27 width=%275%27 height=%275%27/%3E%3Crect x=%277%27 y=%2720%27 width=%275%27 height=%275%27/%3E%3Crect x=%2720%27 y=%2720%27 width=%275%27 height=%275%27/%3E%3C/g%3E%3C/svg%3E">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="https://chokyusong.github.io/{og}">
{HEAD_SCRIPT}
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/regular/style.css">
<link rel="stylesheet" href="{rel}assets/css/site.css?v={ver("assets/css/site.css")}">
</head>
<body>
<a class="skip" href="#main">본문으로 건너뛰기</a>
<div class="grain" aria-hidden="true"></div>
<div class="curtain" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i></div>
{nav}
<main id="main">
{body}
</main>
{foot}
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>
<script src="https://unpkg.com/lenis@1.1.14/dist/lenis.min.js" defer></script>
<script src="{rel}assets/js/site.js?v={ver("assets/js/site.js")}" defer></script>
</body>
</html>
"""


def lines_html(lines, tag="h1", cls="", extra=""):
    inner = "".join(f'<span class="line-mask"><span>{e(l)}</span></span>' for l in lines)
    return f'<{tag} class="{cls}" data-lines{extra}>{inner}</{tag}>'


def links_html(links, rel):
    out = []
    for label, href in links:
        ext = href.startswith("http")
        h = href if ext or not href.startswith("../") else href
        tgt = ' target="_blank" rel="noopener"' if ext or "works/astra" in href else ""
        out.append(f'<a class="text-link" href="{e(h)}"{tgt}>{e(label)}<i class="ph ph-arrow-up-right" aria-hidden="true"></i></a>')
    return "".join(out)


# ---------------------------------------------------------------- 블록

def block_head(d, idx=None):
    t = d.get("title")
    if not t:
        return ""
    p = f'<p>{e(d["text"])}</p>' if d.get("text") else ""
    return f'<div class="block-head" data-reveal><h2 class="h-2">{e(t)}</h2>{p}</div>'


def b_yt(p, d, rel):
    two = " two" if len(d["items"]) > 1 else ""
    items = "".join(
        f'<figure data-reveal><button class="yt" data-yt="{vid}" data-title="{e(title)}" data-cursor="재생" aria-label="{e(title)} 재생">'
        f'<img src="https://i.ytimg.com/vi/{vid}/maxresdefault.jpg" alt="" loading="lazy" width="1280" height="720">'
        f'<span class="yt-play"><span><i class="ph ph-play" aria-hidden="true"></i></span></span></button>'
        f'<figcaption class="yt-cap">{e(title)}</figcaption></figure>'
        for vid, title in d["items"])
    return f'<section class="block">{block_head(d)}<div class="yt-grid{two}">{items}</div></section>'


def b_states(p, d, rel):
    btns = "".join(f'<button type="button" aria-pressed="false"><i></i><b>{e(lab)}</b><span>{e(txt)}</span></button>' for _, lab, txt in d["items"])
    imgs = "".join(img(p["slug"], name, f"AutoLed 기본창 — {lab} 상태. 예시 데이터", rel) for name, lab, _ in d["items"])
    return f'<section class="block">{block_head(d)}<div class="states" data-states><div class="state-list" data-reveal>{btns}</div><div class="state-view" data-reveal>{imgs}</div></div></section>'


def gal_item(slug, name, cap, w, fit, group, rel, ar=None):
    W, H = size(slug, name)
    cls = "g-btn fit" if fit else "g-btn"
    style = f' style="--ar:{ar}"' if (fit and ar) else ""
    return (f'<figure class="g-item {w}" data-reveal><button class="{cls}"{style} type="button" data-lb="{group}" data-full="{rel}assets/img/{slug}/{name}.webp" data-cap="{e(cap)}" data-cursor="크게">'
            f'{img(slug, name, cap, rel)}</button><figcaption>{e(cap)}</figcaption></figure>')


def b_gallery(p, d, rel):
    slug = p["slug"]
    items = []
    for it in d["items"]:
        name, cap = it[0], it[1]
        w = it[2] if len(it) > 2 else d.get("w", "w6")
        fit = it[3] if len(it) > 3 else d.get("fit", False)
        ar = d.get("ar") if fit else None
        if fit and not ar:
            W, H = size(slug, name)
            ar = "16 / 12" if W < H else "16 / 10"
        items.append(gal_item(slug, name, cap, w, fit, d["group"], rel, ar))
    if d.get("label"):
        head = f'<p class="group-label" data-reveal>{e(d["title"])}</p>'
        return f'<div>{head}<div class="gallery">{"".join(items)}</div></div>'
    return f'<section class="block">{block_head(d)}<div class="gallery">{"".join(items)}</div></section>'


def b_compare(p, d, rel):
    s = p["slug"]
    return (f'<section class="block">{block_head(d)}<div class="compare" data-compare data-reveal data-cursor="끌기">'
            f'{img(s, d["before"], d["lb"] + " 화면. 예시 데이터", rel)}'
            f'<div class="after">{img(s, d["after"], d["la"] + " 화면. 예시 데이터", rel)}</div>'
            f'<span class="compare-label l">{e(d["lb"])}</span><span class="compare-label r">{e(d["la"])}</span>'
            f'<div class="compare-handle"><span><i class="ph ph-arrows-left-right" aria-hidden="true"></i></span></div>'
            f'<input type="range" min="0" max="100" value="50" aria-label="{e(d["lb"])}와 {e(d["la"])} 비교 위치"></div></section>')


def b_flow(p, d, rel):
    lis = "".join(f'<li class="{"hl" if len(it) > 2 and it[2] else ""}" data-reveal><b>{e(it[0])}</b><span>{e(it[1])}</span></li>' for it in d["items"])
    return f'<section class="block">{block_head(d)}<ol class="flow" style="--n:{len(d["items"])}">{lis}</ol><div class="flow-bar"><b></b></div></section>'


def b_perf(p, d, rel):
    rows = [
        ("대시보드 첫 화면", [("전", "100%", "22초"), ("후", "1.6%", "0.25초")]),
        ("30일 · 3달 방송 순위", [("전", "100%", "27~118초"), ("후", "6%", "1~7초")]),
    ]
    out = []
    for h, bars in rows:
        bs = "".join(f'<div class="perf-bar{" after" if k == "후" else ""}"><span>{k}</span><i><b style="--w:{w}"></b></i><em>{v}</em></div>' for k, w, v in bars)
        out.append(f'<div class="perf-row" data-reveal><h4>{h}</h4><div class="perf-bars">{bs}</div></div>')
    return (f'<section class="block"><div class="block-head" data-reveal><h2 class="h-2">1,350만 건 부하 시험 전과 뒤</h2>'
            f'<p>시험용으로 만든 3달 치 기록으로 병목을 찾아 고쳤습니다. 막대 길이는 걸린 시간입니다.</p></div><div class="perf">{"".join(out)}</div></section>')


def b_kpis(p, d, rel):
    cells = "".join(f'<div data-reveal><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in d["items"])
    return f'<section class="block">{block_head(d)}<div class="kpis">{cells}</div></section>'


def b_cards(p, d, rel):
    cs = "".join(f'<article class="card" data-reveal><span class="idx">{i + 1:02d}</span><h3>{e(t)}</h3><p>{e(x)}</p></article>' for i, (t, x) in enumerate(d["items"]))
    return f'<section class="block">{block_head(d)}<div class="cards" style="--c:{d.get("cols", 3)}">{cs}</div></section>'


def b_points(p, d, rel):
    lis = "".join(f'<li data-reveal><i class="ph {ic}" aria-hidden="true"></i><span>{e(t)}</span></li>' for ic, t in d["items"])
    return f'<section class="block">{block_head(d)}<ul class="points">{lis}</ul></section>'


def b_hub(p, d, rel):
    core = f'<div class="hub-core" data-reveal><b>{e(d["core"][0])}</b><span>{e(d["core"][1])}</span></div>'
    nodes = "".join(f'<div class="hub-node" data-reveal><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in d["items"])
    return f'<section class="block">{block_head(d)}<div class="hub">{core}{nodes}</div></section>'


def b_clips(p, d, rel):
    cs = "".join(
        f'<figure class="clip" data-reveal><video data-autoplay data-src="{CLIPS}{cid}.mp4" poster="{CLIPS}{cid}.jpg" muted loop playsinline preload="none" aria-label="{e(name)} 효과"></video>'
        f'<figcaption>{e(name)}<span>{e(cat)}</span></figcaption></figure>' for cid, name, cat in d["items"])
    return f'<section class="block">{block_head(d)}<div class="clips">{cs}</div></section>'


ASTRA_PAGES = [("홈", "motion/home.html"), ("회사소개", "motion/about.html"), ("MCN", "motion/mcn.html"), ("브랜드", "brand/brand-v3.html"),
               ("엔터테인먼트", "motion/entertainment.html"), ("미디어", "motion/media.html"), ("협력사", "motion/partners.html"), ("CONTACT", "motion/contact.html")]


def live_browser(rel, shield=True):
    base = f"{rel}works/astra/"
    tabs = "".join(f'<button type="button" data-page="{base}{path}" aria-pressed="{"true" if i == 0 else "false"}">{e(name)}</button>' for i, (name, path) in enumerate(ASTRA_PAGES))
    sh = '<button class="live-shield" type="button" data-cursor="조작" aria-label="시안 안에서 직접 조작하기"><span>눌러서 직접 조작</span></button>' if shield else ""
    return (f'<div class="browser" data-live="{base}motion/home.html" data-host="astra-ent · " data-reveal>'
            f'<div class="browser-bar"><span class="browser-dots" aria-hidden="true"><i></i><i></i><i></i></span><span class="browser-url">astra-ent · home.html</span>'
            f'<span class="seg browser-tools" role="group" aria-label="화면 크기"><button type="button" data-device="pc" aria-pressed="true">PC</button><button type="button" data-device="mobile" aria-pressed="false">휴대폰</button></span></div>'
            f'<div class="live-frame">{sh}<iframe title="ASTRA 움직이는 시안" loading="lazy"></iframe>'
            f'<div class="live-cover" style="background-image:url({rel}assets/img/astra/home-pc.webp)"><span>시안 불러오는 중</span></div></div>'
            f'<div class="page-tabs" role="group" aria-label="시안 쪽 고르기">{tabs}</div></div>')


HOME_PAGES = [("home", "홈", "/"), ("about", "회사 소개", "/about.html"), ("services", "서비스", "/services.html"), ("autoled", "제품 AutoLed", "/autoled.html"),
              ("motion", "모션그래픽", "/motion/"), ("works", "구축 사례", "/works.html"), ("blog", "블로그", "/blog"), ("contact", "문의", "/contact.html")]


def b_scroller(p, d, rel):
    base = f"{rel}assets/img/onicsoft-homepage/"
    tabs = "".join(f'<button type="button" data-shot="{k}" data-url="onicsoft.co.kr{u}" data-alt="ONICSOFT 홈페이지 {e(n)}" aria-pressed="{"true" if i == 0 else "false"}">{e(n)}</button>' for i, (k, n, u) in enumerate(HOME_PAGES))
    wpc, hpc = size("onicsoft-homepage", "home-pc")
    wm, hm = size("onicsoft-homepage", "home-mobile")
    return (f'<section class="block" style="margin-top:clamp(40px,5vw,72px)"><div class="scroller-wrap" data-scroller>'
            f'<div class="browser" data-reveal><div class="browser-bar"><span class="browser-dots" aria-hidden="true"><i></i><i></i><i></i></span><span class="browser-url">onicsoft.co.kr/</span></div>'
            f'<div class="scroller pc" data-base="{base}" data-kind="pc" data-cursor="훑기"><img src="{base}home-pc.webp" width="{wpc}" height="{hpc}" alt="ONICSOFT 홈페이지 홈 PC 화면" loading="lazy"></div>'
            f'<div class="page-tabs" role="group" aria-label="쪽 고르기">{tabs}</div></div>'
            f'<div class="phone" data-reveal><div class="scroller mobile" data-base="{base}" data-kind="mobile" data-cursor="훑기"><img src="{base}home-mobile.webp" width="{wm}" height="{hm}" alt="ONICSOFT 홈페이지 홈 휴대폰 화면" loading="lazy"></div></div>'
            f'</div><p class="live-note">화면 위에 마우스를 올리거나 누르면 페이지 끝까지 훑어 내려갑니다. 2026년 10월에 찍은 화면입니다. <a class="text-link" href="https://onicsoft.co.kr/" target="_blank" rel="noopener">실제 사이트 열기<i class="ph ph-arrow-up-right" aria-hidden="true"></i></a></p></section>')


def b_live(p, d, rel):
    return (f'<section class="block" style="margin-top:clamp(40px,5vw,72px)">{live_browser(rel, shield=False)}'
            f'<p class="live-note">그림이 아니라 실제 시안입니다. 창 안에서 스크롤하고, 위 메뉴나 아래 쪽 이름을 눌러 옮겨 다닐 수 있습니다. 휴대폰 버튼을 누르면 휴대폰 화면으로 바뀝니다.</p></section>')


def b_video(p, d, rel):
    c = d["clip"]
    return (f'<figure class="big-video" data-clip style="margin-top:clamp(40px,5vw,72px)"><video data-autoplay data-src="{CLIPS}{c}.mp4" poster="{CLIPS}{c}.jpg" muted loop playsinline preload="none" aria-label="{e(d["alt"])}"></video></figure>')


BLOCKS = {"yt": b_yt, "states": b_states, "gallery": b_gallery, "compare": b_compare, "flow": b_flow, "perf": b_perf, "kpis": b_kpis,
          "cards": b_cards, "points": b_points, "hub": b_hub, "clips": b_clips, "scroller": b_scroller, "live": b_live, "video": b_video}


# ---------------------------------------------------------------- 상세 페이지

def case_page(i, p):
    rel = "../"
    nxt = PROJECTS[(i + 1) % N]
    meta = "".join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in p["meta"])
    cols = 3 if len(p["meta"]) in (3, 6) else 4
    cover = ""
    if p.get("cover"):
        s, n, alt = p["cover"]
        cover = f'<figure class="case-cover" data-clip>{img(s, n, alt, rel, lazy=False)}</figure>'
    first = ""
    if p.get("first"):
        k, d = p["first"]
        first = BLOCKS[k](p, d, rel)
    story = "".join(
        f'<div class="story-item" data-reveal><dt><span class="idx">{j + 1:02d}</span><b>{e(h)}</b></dt><dd>{t}</dd></div>'
        for j, (h, t) in enumerate(p["story"]))
    blocks = []
    pend = []
    for k, d in p["blocks"]:
        if k == "gallery" and d.get("label"):
            pend.append(BLOCKS[k](p, d, rel))
            continue
        if pend:
            blocks.append(f'<section class="block"><div class="block-head" data-reveal><h2 class="h-2">단계마다 화면</h2><p>모든 사진은 눌러서 크게 볼 수 있습니다.</p></div>{"".join(pend)}</section>')
            pend = []
        blocks.append(BLOCKS[k](p, d, rel))
    if pend:
        blocks.append(f'<section class="block"><div class="block-head" data-reveal><h2 class="h-2">단계마다 화면</h2><p>모든 사진은 눌러서 크게 볼 수 있습니다.</p></div>{"".join(pend)}</section>')
    links = ""
    if p["links"]:
        links = f'<div class="case-links" data-reveal>{links_html(p["links"], rel)}</div>'
    notice = f'<p class="notice" data-reveal><i class="ph ph-eye-slash" aria-hidden="true"></i><span><b>공개 범위</b> · {e(p["notice"])}</span></p>'
    body = f"""<section class="case-hero wrap">
  <a class="back" href="../index.html#works"><i class="ph ph-arrow-left" aria-hidden="true"></i>모든 작업</a>
  <div class="case-top" data-reveal="fade"><span class="eyebrow">{e(p["kind"])}</span><span class="idx">{i + 1:02d} / {N:02d}</span></div>
  {lines_html(p["lines"], "h1", "case-title")}
  <p class="case-sum" data-reveal>{e(p["summary"])}</p>
  <dl class="meta" style="--cols:{cols}" data-reveal>{meta}</dl>
  {cover}{first}
</section>
<section class="wrap" style="margin-top:clamp(80px,10vw,150px)">
  <div class="block-head" data-reveal><span class="idx">이야기</span></div>
  <dl class="story">{story}</dl>
  {"".join(blocks)}
  {links}
  {notice}
</section>
<a class="next wrap" href="{nxt["slug"]}.html" data-cursor="다음">
  <span class="mono">다음 작업 · {(i + 2 if i + 1 < N else 1):02d}</span>
  <span class="next-title">{e(nxt["title"])}<i class="ph ph-arrow-right" aria-hidden="true"></i></span>
</a>"""
    og = f'assets/img/{p["cover"][0]}/{p["cover"][1]}.webp' if p.get("cover") else (f'assets/img/{p["preview"][0]}/{p["preview"][1]}.webp' if p.get("preview") else "assets/img/autoled/ui-overview.webp")
    return shell(f'{p["title"]} — 조규송 포트폴리오', p["summary"], body, rel, og=og)


# ---------------------------------------------------------------- 첫 화면

def home():
    rel = ""
    rows, pvs = [], []
    for i, p in enumerate(PROJECTS):
        thumb = ""
        if p.get("preview"):
            s, n = p["preview"]
            thumb = f'<span class="work-thumb">{img(s, n, "", rel)}</span>'
            pvs.append(img(s, n, "", rel, extra=f' data-pv-item="{p["slug"]}"'))
        elif p.get("pv_video"):
            c = p["pv_video"]
            pvs.append(f'<video data-pv-item="{p["slug"]}" data-autoplay data-src="{CLIPS}{c}.mp4" poster="{CLIPS}{c}.jpg" muted loop playsinline preload="none"></video>')
            thumb = f'<span class="work-thumb"><img src="{CLIPS}{c}.jpg" alt="" loading="lazy" width="1280" height="720"></span>'
        elif p.get("pv_stat"):
            a, b = p["pv_stat"]
            pvs.append(f'<div class="pv-stat" data-pv-item="{p["slug"]}"><b>{e(a)}</b><span>{e(b)}</span></div>')
        cat = CAT_OF[p["slug"]]
        if i == 0 or CAT_OF[PROJECTS[i - 1]["slug"]] != cat:
            cnt = sum(1 for q in PROJECTS if CAT_OF[q["slug"]] == cat)
            rows.append(f'<div class="work-group" data-cat="{cat}" data-reveal><b>{e(CAT_NAME[cat])}</b><span>{cnt}</span></div>')
        rows.append(
            f'<a class="work-row" href="work/{p["slug"]}.html" data-pv="{p["slug"]}" data-cat="{cat}" data-reveal data-cursor="보기">'
            f'<span class="work-n">{i + 1:02d}</span><span class="work-title">{e(p["title"])}</span>'
            f'<span class="work-sub">{e(p["short"])}</span><span class="work-tags">{e(CAT_NAME[cat])} · {e(p["tags"])}<br>{e(p["year"])}</span>'
            f'<span class="work-arrow" aria-hidden="true"><i class="ph ph-arrow-up-right"></i></span>{thumb}</a>')

    show_steps = [
        ("onboarding-1", "준비", "01 · 준비", "처음 켜면 할 일을 순서대로", "설명서를 읽지 않아도 됩니다. 연결할 장비와 다음 할 일을 순서대로 보여 주고, 끝난 단계는 지워 나갑니다."),
        ("state-2", "감시 중", "02 · 감시", "방송을 시작하면 알림을 지켜봅니다", "팬더TV, SOOP, 투네이션, 위플랩, 펀네이션 후원 알림을 지켜봅니다. 지금 상태는 가운데 원 하나로 보입니다."),
        ("state-3", "실행 중", "03 · 실행", "후원이 들어오는 순간 연출이 실행됩니다", "후원 개수에 맞춘 OBS 장면 전환, LED 칼럼, 조명과 카메라, 배경음악 음소거를 실행하고, 끝나면 원래 장면으로 돌려놓습니다."),
        ("ui-timeline", "Timeline", "04 · 연출 편집", "음악에 맞춰 연출을 짭니다", "음원 파형 위에 장면, 조명, 카메라 블록을 놓는 Timeline 편집기. 자동 연출 만들기로 초안을 한 번에 깝니다."),
        ("ui-overview", "관리센터", "05 · 운영", "판매하고, 업데이트하고, 운영합니다", "관리센터에서 연결, 매핑, 감시, 설정을 한곳에서 봅니다. 새 버전은 앱 안에서 알리고 업데이트하며, 계정은 직접 만든 서버가 확인합니다."),
    ]
    steps_html = "".join(
        f'<div class="show-step" data-label="AutoLed · {e(lab)}"><span class="idx">{e(idx)}</span><h3 class="h-2">{e(h)}</h3><p>{e(t)}</p>'
        f'<figure class="device"><div class="device-screen">{img("autoled", n, "AutoLed " + lab + " 화면. 예시 데이터", rel)}</div></figure></div>'
        for n, lab, idx, h, t in show_steps)
    stage_imgs = "".join(img("autoled", n, "AutoLed " + lab + " 화면. 예시 데이터", rel) for n, lab, *_ in show_steps)
    bars = "<i><b></b></i>" * len(show_steps)

    reel_ids = [("chromeText", "크롬 글자", "3D"), ("fireBurst", "불꽃 폭발", "3D · Blender"), ("alertPop", "후원 알림", "방송 화면"),
                ("glitchText", "글리치", "타이포"), ("audioCircle", "원형 이퀄라이저", "음악 연동")]
    reel = "".join(
        f'<figure class="reel-item"><video data-autoplay data-src="{CLIPS}{c}.mp4" poster="{CLIPS}{c}.jpg" muted loop playsinline preload="none" aria-label="{e(n)} 효과"></video>'
        f'<figcaption>{e(n)}<span>{e(k)}</span></figcaption></figure>' for c, n, k in reel_ids)

    marquee_words = ["Python", "Windows 앱", "업무 자동화", "FastAPI", "홈페이지", "방송 자동화", "라이선스 서버", "PySide6", "SQLite", "서버 운영", "모션그래픽", "three.js", "자동 테스트", "OBS WebSocket"]
    mq = "".join(f"<span>{e(w)}</span>" for w in marquee_words) * 2

    history = [("2020.10", "방송 기술 회사 입사. 방송 장비 세팅과 방송 화면 디자인"),
               ("2021.07", "MCN 회사 콘텐츠기획팀 팀장. 크리에이터 관리와 함께 정산, 계산서 확인, OBS·레졸룸 자동 전환 프로그램을 GPT와 Python으로 회사 안에서 만듦. 2021.10까지 방송 기술 회사와 겸직"),
               ("2025.09", "오닉소프트 시작. 2025.11까지 MCN 회사와 겸직"), ("2025.10", "AutoLed 개발 시작"), ("2026.06", "PDF2Obsidian 공개"), ("2026.08", "로그인 서버 운영, AutoLed 정식 배포, 회사 홈페이지"),
               ("2026.09", "모션그래픽 작업실, 유튜브 채널 시작, 납품 업체 엑셀 장부 자동화"), ("2026.10", "후원 데이터 집계 서버, 엔터 정산, CCTV 관제, 거래장부 프로그램"),
               ("2026.11", "AutoLed 2.1.0, 엔터 회사 홈페이지 ASTRA 제작")]
    by = {p["slug"]: p for p in PROJECTS}
    short = {"autoled": "AutoLed", "cctv": "CCTV 관제", "bighand": "후원 집계 서버", "enter-payroll": "엔터 주간 정산", "ledger": "납품 거래장부",
             "pdf2obsidian": "PDF2Obsidian", "onicsoft-homepage": "회사 홈페이지", "astra": "ASTRA 손님 홈페이지", "login-server": "로그인 서버",
             "motion": "모션그래픽"}
    cards = []
    for k, (key, name, ic, txt, pic, sls) in enumerate(CATS):
        if pic:
            media = img(pic[0], pic[1], "", rel)
        else:
            media = f'<img src="{CLIPS}chromeText.jpg" alt="" width="1280" height="720" loading="lazy" decoding="async">'
        chips = "".join(f'<a href="work/{sl}.html">{e(short[sl])}</a>' for sl in sls)
        cards.append(f'<article class="field" data-reveal><a class="field-media" href="#works" data-filter-go="{key}" data-cursor="보기" aria-label="{e(name)} 작업 모아 보기">{media}</a>'
                     f'<div class="field-body"><span class="idx">{k + 1:02d}</span><h3 class="h-3"><i class="ph {ic}" aria-hidden="true"></i>{e(name)}<small>{len(sls)}</small></h3><p>{e(txt)}</p>'
                     f'<div class="field-links">{chips}</div></div></article>')
    fields_html = "".join(cards)
    work_tabs = f'<button type="button" data-filter="all" aria-pressed="true">전체<span>{N}</span></button>' + "".join(
        f'<button type="button" data-filter="{c[0]}" aria-pressed="false">{e(c[1])}<span>{len(c[5])}</span></button>' for c in CATS)
    tl = "".join(f'<li data-reveal><time datetime="{d.replace(".", "-")}">{d}</time><p>{e(t)}</p></li>' for d, t in history)

    body = f"""<section class="hero">
  <canvas class="hero-canvas" data-word="BUILD" aria-hidden="true"></canvas>
  <div class="wrap hero-in">
    <p class="eyebrow" data-hero-fade>AI BUILDER · 조규송</p>
    <h1 class="h-display hero-title" data-lines data-hero><span class="line-mask"><span>AI로 필요한 것을</span></span><span class="line-mask"><span>만들고, 팔고,</span></span><span class="line-mask"><span><em>직접 운영</em>합니다.</span></span></h1>
    <div class="hero-foot">
      <p class="lead" data-hero-fade>기획, 디자인, 개발, 배포, 운영까지 AI와 함께 혼자 끝내는 AI&nbsp;Builder입니다. 방송 자동화 제품 AutoLed를 만들어 유료 고객 약 15명에게 팔고, 회사 업무를 줄이는 자동화 프로그램과 서버를 직접 만들고 운영합니다. 이 페이지에서 만든 것을 전부 직접 보고 눌러 볼 수 있습니다.</p>
      <div class="btn-row" data-hero-fade><a class="btn btn-primary" href="#works" data-magnet>작업 보기<i class="ph ph-arrow-down" aria-hidden="true"></i></a><a class="btn btn-ghost" href="resume.html" data-magnet><i class="ph ph-identification-card" aria-hidden="true"></i>이력서</a></div>
    </div>
    <div class="hero-meta" data-hero-fade><div>ROLE<b>{e(ROLE)}</b></div><div>NOW<b>AutoLed 2.1.0 · 유료 고객 약 15명</b></div><div>FOCUS<b>AI 서비스 기획 · 업무 자동화 · 서버</b></div></div>
  </div>
  <div class="scroll-hint" aria-hidden="true">SCROLL</div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee-track">{mq}</div></div>

<section class="section wrap" id="about">
  <div class="section-head">
    <div><p class="idx" data-reveal>01 — 요약</p>{lines_html(["혼자 만들고,", "끝까지 책임집니다."], "h2", "h-1")}</div>
    <p class="lead" data-reveal>방송 자동화 제품, 업무 자동화 프로그램, 서버를 기획부터 운영까지 한 사람이 맡습니다. 홈페이지와 영상도 직접 만듭니다. 코드는 AI 코딩 도구와 함께 쓰고, 무엇을 만들고 언제 내보낼지는 제가 정합니다.</p>
  </div>
  <div class="stats">
    <div class="stat" data-reveal><span class="stat-num"><span data-count="15">15</span><small>명</small></span><span class="stat-label">AutoLed 유료 고객(약) · 2.1.0 판매 중</span></div>
    <div class="stat" data-reveal><span class="stat-num"><span data-count="6">6</span><small>년</small></span><span class="stat-label">방송·MCN 현장부터 제품 개발까지 경력</span></div>
    <div class="stat" data-reveal><span class="stat-num"><span data-count="2200">2,200</span><small>+</small></span><span class="stat-label">소개한 작업의 자동 테스트</span></div>
    <div class="stat" data-reveal><span class="stat-num"><span data-count="{N}">{N}</span></span><span class="stat-label">상세 페이지로 소개한 작업</span></div>
  </div>
  <p class="stats-note">{ASOF} 기준. 테스트 수는 각 저장소 기록, 경력은 이력서 기준입니다.</p>
</section>

<section class="section wrap" id="fields">
  <div class="section-head">
    <div><p class="idx" data-reveal>02 — 하는 일</p>{lines_html(["한 분야만", "하지 않습니다."], "h2", "h-1")}</div>
    <p class="lead" data-reveal>방송 자동화 제품을 팔면서, 회사 업무를 줄이는 프로그램과 서버를 직접 만들고 운영합니다. 홈페이지와 영상도 직접 만듭니다. 그림을 누르면 아래 작업 목록이 그 분류로 정리되고, 이름표를 누르면 상세 페이지가 열립니다.</p>
  </div>
  <div class="fields">{fields_html}</div>
</section>

<section class="section wrap" id="works">
  <div class="section-head">
    <div><p class="idx" data-reveal>03 — 모든 작업</p>{lines_html(["만든 것", f"{N}가지"], "h2", "h-1")}</div>
    <p class="lead" data-reveal>프로그램, 업무 자동화, 홈페이지, 서버, 모션그래픽으로 나눠 정리했습니다. 줄을 누르면 화면, 영상, 직접 눌러 보는 데모를 모은 상세 페이지가 열립니다. 비공개 저장소는 핵심 로직 없이 무엇을 만들고 어떤 결과가 났는지만 소개합니다. 공개 코드는 <a class="text-link" href="https://github.com/Chokyusong/pdf2obsidian">PDF2Obsidian 저장소</a>에서 볼 수 있습니다.</p>
  </div>
  <div class="work-tabs" role="group" aria-label="분류 고르기" data-reveal>{work_tabs}</div>
  <div class="works" data-works>{"".join(rows)}</div>
</section>
<div class="hover-preview" aria-hidden="true">{"".join(pvs)}</div>

<section class="show" data-show id="autoled">
  <div class="show-sticky"><div class="wrap show-grid">
    <div>
      <div class="show-head"><p class="idx">04 — 대표 작업</p><h2 class="h-1">AutoLed</h2></div>
      <div class="show-steps">{steps_html}</div>
      <div class="show-progress" aria-hidden="true">{bars}</div>
      <div class="show-cta"><a class="btn btn-primary" href="work/autoled.html" data-magnet>AutoLed 자세히 보기<i class="ph ph-arrow-right" aria-hidden="true"></i></a><a class="btn btn-ghost" href="https://onicsoft.co.kr/autoled.html" data-magnet>제품 페이지</a></div>
    </div>
    <div class="show-stage" aria-hidden="true"><div class="device"><div class="device-bar"><i></i><i></i><i></i><span data-show-label>AutoLed</span></div><div class="device-screen">{stage_imgs}</div></div></div>
  </div></div>
</section>

<section class="section wrap" id="how">
  <div class="section-head">
    <div><p class="idx" data-reveal>05 — 일하는 방식</p>{lines_html(["만들고 끝내지 않고,", "운영까지 맡습니다."], "h2", "h-1")}</div>
  </div>
  <div class="how">
    <div class="how-item" data-reveal><i class="ph ph-robot" aria-hidden="true"></i><h3 class="h-3">AI와 나눠서 만듭니다</h3><p>코드는 Claude Code, Codex 같은 AI 코딩 도구와 함께 씁니다. 무엇을 만들지, 무엇을 공개할지, 언제 내보낼지는 제가 정합니다.</p></div>
    <div class="how-item" data-reveal><i class="ph ph-check-square-offset" aria-hidden="true"></i><h3 class="h-3">테스트로 확인하고 내보냅니다</h3><p>자동 테스트를 먼저 통과시키고, 실제 OBS나 실제 서버에서 한 번 더 확인한 뒤 배포합니다. 엔터 정산은 테스트 141개가 계산과 화면 버튼까지 봅니다.</p></div>
    <div class="how-item" data-reveal><i class="ph ph-hard-drives" aria-hidden="true"></i><h3 class="h-3">만든 뒤에도 운영합니다</h3><p>서버를 직접 세우고, 멈추면 다시 켜지고 알림이 오게 둡니다. 백업은 암호화해 매일 받고, 매달 실제로 풀어 보는 복원 연습까지 자동으로 돌립니다.</p></div>
    <div class="how-item" data-reveal><i class="ph ph-shield-check" aria-hidden="true"></i><h3 class="h-3">공개 범위를 나눕니다</h3><p>제품 소스와 핵심 로직은 비공개 저장소에 둡니다. 고객 정보와 서버 정보는 커밋 기록에도 남기지 않습니다. 이 페이지의 화면도 예시 데이터로 찍었습니다.</p></div>
  </div>
</section>

<section class="section wrap" id="history">
  <div class="section-head">
    <div><p class="idx" data-reveal>06 — 연혁</p>{lines_html(["방송 현장에서", "제품까지"], "h2", "h-1")}</div>
    <p class="lead" data-reveal>MCN과 방송 현장에서 6년 동안 일하며 필요한 프로그램을 직접 만들었고, 2025년 9월부터는 오닉소프트에서 제품으로 만들어 팝니다. 오닉소프트 뒤의 날짜는 각 저장소를 만든 달입니다.</p>
  </div>
  <div class="tl"><span class="tl-line" aria-hidden="true"><b></b></span><ol>{tl}</ol></div>
</section>

<section class="section wrap" id="stack" style="padding-top:0">
  <div class="section-head"><div><p class="idx" data-reveal>07 — 기술</p>{lines_html(["주로 쓰는 기술"], "h2", "h-2")}</div></div>
  <div class="stack-grid">
    <div data-reveal><h3>언어</h3><ul><li>Python</li><li>JavaScript</li><li>HTML / CSS</li><li>PHP</li></ul></div>
    <div data-reveal><h3>데스크톱 앱</h3><ul><li>Tkinter</li><li>PySide6</li><li>Nuitka</li><li>PyInstaller</li><li>Inno Setup</li></ul></div>
    <div data-reveal><h3>서버</h3><ul><li>FastAPI</li><li>Nginx · Caddy</li><li>systemd</li><li>SQLite</li><li>Ubuntu</li></ul></div>
    <div data-reveal><h3>방송 · 영상</h3><ul><li>OBS WebSocket</li><li>Resolume OSC</li><li>Companion</li><li>three.js · Blender</li><li>ffmpeg</li></ul></div>
    <div data-reveal><h3>운영</h3><ul><li>GitHub Actions</li><li>Telegram 봇 알림</li><li>fail2ban</li><li>암호화 백업</li></ul></div>
  </div>
</section>

<section class="section reel" data-reel id="motion">
  <div class="wrap section-head">
    <div><p class="idx" data-reveal>08 — 모션그래픽</p>{lines_html(["편집 프로그램 없이,", "코드로 만든 영상"], "h2", "h-1")}</div>
    <p class="lead" data-reveal>HTML, three.js, Blender로 그리고 프레임마다 찍어 만든 효과입니다. 271종 가운데 일부를 옮겼습니다.</p>
  </div>
  <div class="reel-track">{reel}</div>
  <div class="wrap reel-foot"><a class="text-link" href="work/motion.html">홍보영상과 효과 더 보기<i class="ph ph-arrow-right" aria-hidden="true"></i></a></div>
</section>

<section class="contact wrap" id="contact">
  <p class="idx" data-reveal>09 — 연락</p>
  <h2 class="contact-title" data-lines><span class="line-mask"><span>함께 일할 자리가</span></span><span class="line-mask"><span>있다면<span class="accent">.</span></span></span></h2>
  <div class="contact-grid">
    <p class="lead" data-reveal>Python 데스크톱 앱, 업무 자동화, 서버 개발과 운영, 웹과 영상 경험을 살릴 수 있는 일에 관심이 있습니다. 정규직, 계약직, 프리랜서 모두 가능하고 출근과 원격 모두 괜찮습니다. 입사하면 오닉소프트는 부업으로 운영합니다. 비공개 저장소의 자세한 내용은 면담에서 화면으로 보여 드릴 수 있습니다.</p>
    <div class="btn-row" data-reveal><a class="btn btn-primary" href="{KAKAO}" data-magnet><i class="ph ph-chat-circle-dots" aria-hidden="true"></i>카카오톡으로 연락</a><a class="btn btn-ghost" href="mailto:{EMAIL}" data-magnet><i class="ph ph-envelope-simple" aria-hidden="true"></i>{EMAIL}</a></div>
  </div>
  <div class="big-links" data-reveal style="margin-top:clamp(48px,6vw,80px)">
    <a href="{GITHUB}">GitHub<span>Chokyusong</span></a>
    <a href="https://onicsoft.co.kr/">회사 홈페이지<span>onicsoft.co.kr</span></a>
    <a href="{YOUTUBE}">유튜브 채널<span>AI로 회사키우기</span></a>
    <a href="resume.html">이력서<span>경력 · 역량 · PDF</span></a>
    <a href="resume-en.html" lang="en">Resume (English)<span>Experience · Skills · PDF</span></a>
    <a href="{PDF}">포트폴리오 PDF<span>인쇄용 한 권</span></a>
  </div>
</section>"""
    desc = f"기획부터 디자인, 개발, 운영까지 AI와 함께 혼자 끝내는 AI Builder 조규송. 방송 자동화 제품 AutoLed, 업무 자동화 프로그램, 홈페이지, 서버, 영상까지 작업 {N}가지. 화면, 영상, 움직이는 시안을 직접 볼 수 있습니다."
    return shell("조규송 · AI Builder 포트폴리오", desc, body, rel, home=True)


def main():
    os.makedirs(os.path.join(ROOT, "work"), exist_ok=True)
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(home())
    for i, p in enumerate(PROJECTS):
        with open(os.path.join(ROOT, "work", p["slug"] + ".html"), "w", encoding="utf-8", newline="\n") as f:
            f.write(case_page(i, p))
    try:
        import build_print
        build_print.main(PROJECTS)
    except ImportError:
        pass
    import build_resume
    build_resume.main()
    print("만든 페이지:", 1 + N)


if __name__ == "__main__":
    main()
