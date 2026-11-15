# -*- coding: utf-8 -*-
"""print.html(포트폴리오)과 resume.html·resume-en.html(이력서)을 A4 PDF로 찍는다. 창 없이(headless) 돌린다.

    py -3 tools/make_pdf.py
"""
import os
import pathlib
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
JOBS = [("print.html", ROOT / "assets" / "cho-kyusong-portfolio.pdf", "조규송 · AI Builder · chokyusong.github.io"),
        ("resume.html", ROOT / "assets" / "cho-kyusong-resume.pdf", "조규송 이력서 · chokyusong.github.io"),
        ("resume-en.html", ROOT / "assets" / "cho-kyusong-resume-en.pdf", "Cho Kyusong · Resume · chokyusong.github.io")]


def foot(label):
    return ('<div style="width:100%;font-size:7pt;color:#8a929b;padding:0 14mm;display:flex;justify-content:space-between;'
            f'font-family:sans-serif"><span>{label}</span>'
            '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')


def render(src, out, label):
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, channel="chrome")
        page = b.new_page()
        page.goto(pathlib.Path(src).resolve().as_uri(), wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(800)
        page.emulate_media(media="print")
        page.pdf(path=str(out), format="A4", print_background=True, prefer_css_page_size=True,
                 display_header_footer=True, header_template="<span></span>", footer_template=foot(label))
        b.close()
    print(pathlib.Path(out).name, round(os.path.getsize(out) / 1024 / 1024, 2), "MB")


if __name__ == "__main__":
    if len(sys.argv) == 4:  # 다른 파일을 찍을 때: 원본 html, 내보낼 pdf, 바닥글
        render(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        for name, out, label in JOBS:
            render(ROOT / name, out, label)
