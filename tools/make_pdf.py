# -*- coding: utf-8 -*-
"""print.html을 A4 PDF로 찍는다. 창 없이(headless) 돌린다.

    py -3 tools/make_pdf.py
"""
import os
import pathlib

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "cho-kyusong-portfolio.pdf"
FOOT = ('<div style="width:100%;font-size:7pt;color:#8a929b;padding:0 14mm;display:flex;justify-content:space-between;'
        'font-family:sans-serif"><span>조규송 포트폴리오 · chokyusong.github.io</span>'
        '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, channel="chrome")
    page = b.new_page()
    page.goto((ROOT / "print.html").as_uri(), wait_until="networkidle")
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(800)
    page.pdf(path=str(OUT), format="A4", print_background=True, prefer_css_page_size=True,
             display_header_footer=True, header_template="<span></span>", footer_template=FOOT)
    b.close()
print(OUT.name, round(os.path.getsize(OUT) / 1024 / 1024, 2), "MB")
