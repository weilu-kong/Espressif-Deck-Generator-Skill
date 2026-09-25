#!/usr/bin/env python3
"""Export Espressif Web Deck to fidelity or vector PDF.

Fidelity: 2x browser screenshots assembled into a 16:9 PDF.
Vector: Chromium print-to-PDF with print CSS, preserving selectable text where possible.
"""
from __future__ import annotations
import argparse, os, re, tempfile
from _browser_utils import launch_chromium
from inline_assets import inline_html
from pathlib import Path

PAGE_W_PT=960
PAGE_H_PT=540
VIEW_W=1920
VIEW_H=1080

def prepare(page,html_text):
    page.set_content(html_text,wait_until='load'); page.wait_for_timeout(500)
    page.evaluate("""() => { document.body.classList.add('motion-off'); const h=document.getElementById('nav-hint'); if(h) h.style.display='none'; }""")

def export_fidelity(html_path:Path,out:Path):
    try:
        from playwright.sync_api import sync_playwright
        from reportlab.pdfgen import canvas
    except ImportError:
        raise SystemExit('Fidelity export requires playwright and reportlab. Example: uv run --with playwright --with reportlab python scripts/export_pdf.py ...')
    html_text, stats = inline_html(html_path)
    if stats.get("missing"): raise SystemExit(f"Missing local assets: {stats['missing']}")
    with tempfile.TemporaryDirectory() as td, sync_playwright() as p:
        browser=launch_chromium(p); page=browser.new_page(viewport={'width':VIEW_W,'height':VIEW_H},device_scale_factor=2); prepare(page,html_text)
        total=page.locator('.slide').count(); shots=[]
        for i in range(total):
            page.evaluate("i => window.__deck && window.__deck.go(i,false)",i); page.wait_for_timeout(120)
            fp=Path(td)/f'slide-{i+1:03d}.png'; page.screenshot(path=str(fp),full_page=False); shots.append(fp)
        browser.close()
        c=canvas.Canvas(str(out),pagesize=(PAGE_W_PT,PAGE_H_PT))
        c.setTitle(html_path.stem)
        for fp in shots: c.drawImage(str(fp),0,0,width=PAGE_W_PT,height=PAGE_H_PT); c.showPage()
        c.save()
        return total

def export_vector(html_path:Path,out:Path):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit('Vector export requires playwright. Example: uv run --with playwright python scripts/export_pdf.py ...')
    html_text, stats = inline_html(html_path)
    if stats.get("missing"): raise SystemExit(f"Missing local assets: {stats['missing']}")
    with sync_playwright() as p:
        browser=launch_chromium(p); page=browser.new_page(viewport={'width':VIEW_W,'height':VIEW_H}); prepare(page,html_text)
        total=page.locator('.slide').count()
        page.emulate_media(media='print')
        page.pdf(path=str(out),width='13.333333in',height='7.5in',scale=0.6666667,print_background=True,margin={'top':'0','right':'0','bottom':'0','left':'0'},prefer_css_page_size=True)
        browser.close(); return total

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('html',type=Path); ap.add_argument('--mode',choices=['fidelity','vector'],default='fidelity'); ap.add_argument('-o','--output',type=Path); args=ap.parse_args()
    src=args.html.resolve()
    if not src.exists(): raise SystemExit(f'File not found: {src}')
    out=(args.output or src.with_name(src.stem+('_fidelity.pdf' if args.mode=='fidelity' else '_vector.pdf'))).resolve(); out.parent.mkdir(parents=True,exist_ok=True)
    total=export_fidelity(src,out) if args.mode=='fidelity' else export_vector(src,out)
    print(f'✓ {args.mode} PDF: {out} ({total} pages, {out.stat().st_size/1024/1024:.2f} MB)')
if __name__=='__main__': main()
