# -*- coding: utf-8 -*-
"""English resume (resume-en.html). Same template and the same public rules as build_resume.py:
no phone number, no education, no former company names. Numbers match the Korean resume.
"""
import copy

import build_resume as R

RESUME_EN = {
    "labels": {
        "lang": "en", "doc": "Resume", "more": "Details", "code": "Code", "got": "Results", "edu": "Education",
        "back": "← Portfolio", "pdf": "Download PDF", "pdf_href": "assets/cho-kyusong-resume-en.pdf",
        "other": "한국어", "other_href": "resume.html",
        "decisions": "Decisions I made and verified", "skills": "Core skills", "career": "Experience",
        "career_total": "6 yrs 2 mos in total · overlapping periods were held concurrently",
        "extra": "Other work", "kw": "Keywords", "tools": "Tools I use myself", "language": "Languages", "tech": "Built with",
        "built": "Built into the products", "built_note": "Chosen from AI coding tool suggestions; I tested, shipped and run them.",
        "foot": "Source code and core logic of private repositories are not disclosed. "
                "Screens and videos for each project are at chokyusong.github.io (pages in Korean).",
    },
    # 영문은 글이 길어 인쇄 글자를 조금 줄여 한글판과 같은 3쪽에 맞춘다
    "css": "@media print { body { font-size:8.5pt; line-height:1.45; } .proj { margin-bottom:2.6mm; } .skills p { font-size:8.2pt; } h2 { margin-top:4mm; } .foot { margin-top:3mm; } body { line-height:1.4; } li { margin-bottom:.3mm; } .summary { font-size:9.4pt; } .job { margin-bottom:3.5mm; } }",
    "name": "Cho Kyusong",
    "name_en": "조규송",
    "title": "AI Builder · AI Service Planning · Workflow Automation",
    "availability": "Open to full-time, contract or freelance work · on-site or remote · ONICSOFT continues as a side business",
    "contacts": [("Email", R.RESUME["contacts"][0][1], R.RESUME["contacts"][0][2]),
                 ("Portfolio", "chokyusong.github.io", "https://chokyusong.github.io/"),
                 ("Company", "onicsoft.co.kr", "https://onicsoft.co.kr/")],
    "summary": [
        "An AI service planning and workflow automation specialist who uses AI coding agents to turn ideas into "
        "working services, then sells and operates them.",
        "As Content Planning Team Lead at an MCN for over four years, I led a team of 5 and managed 20 creators, "
        "and automated company work such as settlements and invoice checks myself with GPT and Python. "
        "In September 2025 I founded ONICSOFT, where I sell and operate the broadcast automation product AutoLed "
        "for about 15 paying customers.",
    ],
    "numbers": [("6 yrs 2 mos", "Experience"), ("~15", "Paying AutoLed customers"), ("5 h → 3 min", "MCN settlement automation"),
                ("22 s → 0.25 s", "Dashboard first load"), ("47 / 48 wks", "Payroll program verified")],
    "way": "I write code together with AI coding agents. What to build, what is wrong, and when to ship are my "
           "decisions, and I verify them myself.",
    "decisions": [
        ("Reproduced a freeze, then fixed it", "Rebuilt the exact conditions under which the screen froze during live "
         "broadcasts to find the cause. Before the fix it froze 3 times out of 3; after the fix it ran normally 5 times out of 5."),
        ("Found the bottleneck by load testing", "Load-tested with 13.5 million synthetic records to locate the bottlenecks. "
         "Dashboard first load went from about 22 s to 0.25 s, and period rankings from 27–118 s to 1–7 s."),
        ("Checked results against past records", "Compared the payroll program's output with 48 weeks of the existing "
         "settlement spreadsheet and confirmed 47 weeks matched. Calculation errors and unconfirmed items are held back "
         "before any payment is finalized."),
        ("I decide when to ship", "AutoLed ships only after passing 2,051 automated tests and a second check in a real "
         "OBS setup. Update files are verified with signatures and checksums."),
    ],
    "keywords": "AX (AI transformation) · AI workflow automation · Service planning · PM/PO · Generative AI · AI coding agents · Python",
    "skills": [
        ("AI-assisted development management", "Requirements definition, feature design, directing AI agents, verifying output and fixing defects"),
        ("Service planning · productization", "User problem analysis, feature prioritization, UI/UX planning, product launch and paid service operation"),
        ("System architecture design", "Business process flows, external service integration, user authentication and permissions, data processing design"),
        ("Quality · operations", "Reviewing automated tests, real-environment verification, version control, release approval and maintenance"),
    ],
    "jobs": [
        {
            "company": "ONICSOFT",
            "role": "Founder · Product Owner",
            "period": "2025.09 – Present",
            "desc": "Plans, builds, sells and operates AI-based software and workflow automation solutions.",
            "projects": [
                {"title": "AutoLed: broadcast automation software, built and commercialized", "period": "2025.10 –", "link": "work/autoled.html",
                 "did": ["Analyzed requirements from live broadcasting to plan features, set priorities and judge compatibility with existing features",
                         "Set the scope and acceptance criteria for AI coding agents, checked test results and real broadcast-equipment integration, and made release decisions",
                         "Led customer feedback, incident response and product improvement"],
                 "got": ["Commercialized as an automation tool for live streamers (including Korean “Excel broadcast” shows) with about 15 paying customers; version 2.1.0 on sale",
                         "Unified donation alerts from PandaTV, SOOP, Toonation, Weflab and Funnation into one processing flow, automating everything from OBS and Resolume effects to returning to the original scene",
                         "Fixed an on-air screen freeze by reproducing its conditions: froze 3 of 3 times before the fix, ran normally 5 of 5 times after",
                         "Runs 2,051 automated tests, version control, release approval and update integrity checks (signatures and checksums)"],
                 "tech": "Python, Tkinter, OBS WebSocket, Resolume OSC, Nuitka, Inno Setup"},
                {"title": "Unified authentication · licensing · customer management server", "period": "2026.08 –", "link": "work/login-server.html",
                 "did": ["Designed one server to manage user authentication, permissions and subscription periods for multiple software products",
                         "Built the login → token verification → feature permission check → periodic check-in flow, with device limits",
                         "Plans, subscription renewals, and automatic renewal by matching bank deposit notifications with payment records",
                         "Separate admin roles, OTP authentication and audit logs; deployed with Nginx, HTTPS and systemd"],
                 "got": ["Runs several products, including AutoLed, on one server; new services can register and use the same authentication",
                         "Operations with automatic backups, server monitoring, failure alerts and a standby-server recovery procedure"],
                 "tech": "Python, FastAPI, SQLite, Linux, Nginx"},
                {"title": "Donation data aggregation server · performance tuning", "period": "2026.10", "link": "work/bighand.html",
                 "did": ["Planned a server that gathers donation records from many broadcasts, removes duplicates and shows statistics by period",
                         "Set up data retention rules, encrypted backups, automatic restore checks and server failure monitoring"],
                 "got": ["Processed 78,844 donation records in one day in production (October 6, 2026)",
                         "Load-tested with 13.5 million synthetic records (about 2 GB); dashboard first load from about 22 s to 0.25 s"],
                 "tech": "Python, SQLite, Linux, systemd, GitHub Actions"},
                {"title": "Revenue · payroll · tax settlement automation for an entertainment company", "period": "2026.10 –", "link": "work/enter-payroll.html",
                 "did": ["Planned and built a Windows program that calculates broadcast revenue, per-performer payouts, company profit and equity distribution",
                         "Handles withholding tax, VAT, advances and payment history; collects and reconciles Excel/CSV data and generates settlement sheets",
                         "Result review, exception holds, settlement confirmation and payment lists; personal-data encryption and automatic backups"],
                 "got": ["Matched 47 of 48 weeks when compared with the existing settlement spreadsheet",
                         "Separates calculation errors from unconfirmed items so a wrong payment cannot be finalized; verified on the office PC"],
                 "tech": "Python, PySide6, SQLite, Excel integration, Nuitka"},
                {"title": "Live broadcast monitoring program (CCTV)", "period": "2026.10", "link": "work/cctv.html",
                 "did": ["Detects when up to 60 streamers start or end a broadcast and brings video, chat and donation info onto one screen",
                         "Per-broadcast lists, sorting, search, Telegram alerts and settings stored in SQLite; separate desktop and Linux server features"],
                 "got": ["Replaced managers checking each channel one by one with automatic detection; server features finished with automated tests"],
                 "tech": "Python, WebSocket, SQLite, Linux, Telegram"},
                {"title": "Transaction ledger program for a supplier", "period": "2026.09", "link": "work/ledger.html",
                 "did": ["Replaced the duplicate Excel ledgers of a printed-advertising supplier with a program where each entry is typed once"],
                 "got": ["Found and listed the rows where the original ledgers disagreed during migration; verified Excel export round trips"],
                 "tech": "Python, SQLite, Excel integration"},
            ],
        },
        {
            "company": "MCN company",
            "role": "Content Planning Team Lead",
            "period": "2021.07 – 2025.11 (4 yrs 5 mos)",
            "desc": "Held concurrently with the broadcast technology company (2021.07–10) and ONICSOFT (2025.09–11).",
            "bullets": ["Led a team of 5 and managed 20 affiliated creators and streamers, including care and revenue-share consultations",
                        "Built in-house automation tools in Python with GPT: settlement 5 hours → 3 minutes (no more calculation mistakes), invoice checks 1 hour → 30 seconds, creator ranking and trend checks 1 hour → 30 seconds",
                        "Built automatic OBS · Resolume scene switching for “Excel broadcast” shows",
                        "Installed and set up broadcast equipment (PCs, lighting, cameras, audio) and trained creators to use it",
                        "Created broadcast design assets (signature emotes, LIVE standby screens, banner GIFs) in Photoshop and After Effects"],
        },
        {
            "company": "Broadcast technology company",
            "role": "Equipment setup · broadcast design",
            "period": "2020.10 – 2021.10 (1 yr 1 mo)",
            "desc": "Held concurrently with the MCN company from 2021.07.",
            "bullets": ["Installed PCs and set up lighting, cameras and audio",
                        "Created broadcast design assets (signature emotes, LIVE standby screens, banner GIFs) in Photoshop"],
        },
    ],
    "extra_projects": [("PDF2Obsidian", "Open-source tool that turns PDFs and lecture transcripts into Obsidian notes (2026.06, MIT). "
                        "Code and automated tests are public.", "work/pdf2obsidian.html"),
                       ("AI content planning", "A one-source multi-use system that adapts one piece of content to blog, YouTube, Naver and social formats; SEO; thumbnails and ad creatives with AI image tools (2026.09 –)", None),
                       ("Websites", "Planned, built and run the ONICSOFT website; 22 industry samples; an 8-page animated draft for the ASTRA entertainment company (2026.08 –)", "work/onicsoft-homepage.html"),
                       ("Motion graphics", "271 effects made with code and Blender through AI coding tools; AutoLed promo videos and broadcast alerts (2026.09 –)", "work/motion.html")],
    "education": None,
    "tools": ["ChatGPT · Claude Code · Codex", "Python (basic)", "Photoshop", "After Effects", "Excel"],
    "built": ["Python apps (Tkinter · PySide6)", "FastAPI", "SQLite", "Linux · Nginx", "HTML · CSS · JavaScript", "OBS WebSocket · Resolume OSC",
              "three.js · Blender · FFmpeg", "GitHub Actions"],
    "language": "Korean (native) · English (conversational)",
}


def private_copy(overrides):
    r = copy.deepcopy(RESUME_EN)
    overrides(r)
    return r
