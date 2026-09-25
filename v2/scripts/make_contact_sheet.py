#!/usr/bin/env python3
"""Create a contact sheet PNG from a rendered deck."""
from __future__ import annotations
import argparse, math, os, tempfile
from _browser_utils import launch_chromium
from inline_assets import inline_html
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('html',type=Path); ap.add_argument('-o','--output',type=Path); ap.add_argument('--columns',type=int,default=4); args=ap.parse_args()
    try:
        from playwright.sync_api import sync_playwright
        from PIL import Image,ImageOps,ImageDraw
    except ImportError:
        raise SystemExit('Requires playwright and pillow. Example: uv run --with playwright --with pillow python scripts/make_contact_sheet.py ...')
    src=args.html.resolve(); out=(args.output or src.with_name(src.stem+'_contact_sheet.png')).resolve(); out.parent.mkdir(parents=True,exist_ok=True)
    html_text, stats = inline_html(src)
    if stats.get("missing"): raise SystemExit(f"Missing local assets: {stats['missing']}")
    with tempfile.TemporaryDirectory() as td, sync_playwright() as p:
        browser=launch_chromium(p); page=browser.new_page(viewport={'width':1920,'height':1080}); page.set_content(html_text,wait_until='load'); page.wait_for_timeout(350); page.evaluate("document.body.classList.add('motion-off')")
        total=page.locator('.slide').count(); fps=[]
        for i in range(total):
            page.evaluate("i => window.__deck && window.__deck.go(i,false)",i); page.wait_for_timeout(70); fp=Path(td)/f'{i:03d}.png'; page.screenshot(path=str(fp)); fps.append(fp)
        browser.close()
        thumb_w=480; thumb_h=270; label_h=34; gap=18; cols=max(1,args.columns); rows=math.ceil(total/cols)
        sheet=Image.new('RGB',(cols*thumb_w+(cols+1)*gap, rows*(thumb_h+label_h)+(rows+1)*gap),(25,27,32)); draw=ImageDraw.Draw(sheet)
        for i,fp in enumerate(fps):
            img=Image.open(fp).convert('RGB').resize((thumb_w,thumb_h)); x=gap+(i%cols)*(thumb_w+gap); y=gap+(i//cols)*(thumb_h+label_h+gap); sheet.paste(img,(x,y)); draw.text((x,y+thumb_h+8),f'{i+1:02d}',fill=(220,222,228))
        sheet.save(out)
    print(f'✓ Contact sheet: {out} ({total} slides)')
if __name__=='__main__': main()
