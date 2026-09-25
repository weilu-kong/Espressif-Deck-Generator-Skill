#!/usr/bin/env python3
"""Validate rendered Web Deck geometry and browser errors with Playwright."""
from __future__ import annotations
import argparse, json, os, sys
from _browser_utils import launch_chromium
from inline_assets import inline_html
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html", type=Path)
    ap.add_argument("--report", type=Path, default=Path("validation-report.json"))
    ap.add_argument("--min-font", type=float, default=16.0)
    args = ap.parse_args()
    if not args.html.exists(): raise SystemExit(f"File not found: {args.html}")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit("Playwright is required. Run: uv run --with playwright python scripts/validate_deck.py ...")

    errors, warnings = [], []
    console_errors, page_errors = [], []
    browser_html, inline_stats = inline_html(args.html)
    with sync_playwright() as p:
        browser = launch_chromium(p)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: page_errors.append(str(exc)))
        page.set_content(browser_html, wait_until="load")
        page.wait_for_timeout(500)
        result = page.evaluate("""(minFont) => {
          const slides=[...document.querySelectorAll('.slide')];
          const out={slides:slides.length, brokenImages:[], overflows:[], smallText:[], zeroSize:[], missingAlt:[], ids:[], pageNums:[]};
          slides.forEach((s, si)=>{
            const sid=s.id||`slide-${si+1}`; out.ids.push(s.id||'');
            const sr=s.getBoundingClientRect();
            const safe=s.querySelector('.safe'); const safeR=safe?safe.getBoundingClientRect():sr;
            const pn=s.querySelector('.page-num'); out.pageNums.push(pn?pn.textContent.trim():'');
            s.querySelectorAll('img').forEach(img=>{ if(!img.complete || img.naturalWidth===0) out.brokenImages.push({slide:sid,src:img.getAttribute('src')}); if(!img.getAttribute('alt')) out.missingAlt.push({slide:sid,src:img.getAttribute('src')}); });
            s.querySelectorAll('h1,h2,h3,p,li,td,th,.card-positioning,.arch-detail,.caption').forEach(el=>{
              const r=el.getBoundingClientRect(); const cs=getComputedStyle(el); const fs=parseFloat(cs.fontSize);
              if(r.width===0 || r.height===0) out.zeroSize.push({slide:sid,tag:el.tagName,text:(el.textContent||'').slice(0,80)});
              if(fs < minFont && (el.textContent||'').trim()) out.smallText.push({slide:sid,fontSize:fs,text:(el.textContent||'').trim().slice(0,80)});
            });
            s.querySelectorAll('.content > *, .card, .detail-layout, .table-wrap, .arch-flow, .image-layout, .grid-2, .grid-3').forEach(el=>{
              const r=el.getBoundingClientRect();
              const tol=2;
              if(r.left < safeR.left-tol || r.right > safeR.right+tol || r.top < safeR.top-tol || r.bottom > safeR.bottom+tol){
                out.overflows.push({slide:sid,cls:el.className,left:Math.round(r.left-safeR.left),right:Math.round(r.right-safeR.right),top:Math.round(r.top-safeR.top),bottom:Math.round(r.bottom-safeR.bottom)});
              }
            });
          });
          return out;
        }""", args.min_font)
        browser.close()

    for x in inline_stats.get("missing", []): errors.append({"type":"missing-local-asset","path":x})
    for x in inline_stats.get("unresolved", []): warnings.append({"type":"unresolved-local-reference","ref":x})
    for x in result["brokenImages"]: errors.append({"type":"broken-image", **x})
    for x in result["overflows"]: errors.append({"type":"safe-area-overflow", **x})
    for x in result["zeroSize"]: warnings.append({"type":"zero-size", **x})
    for x in result["smallText"]: warnings.append({"type":"small-text", **x})
    for x in result["missingAlt"]: warnings.append({"type":"missing-alt", **x})
    if console_errors: errors.extend({"type":"console-error","message":x} for x in console_errors)
    if page_errors: errors.extend({"type":"page-error","message":x} for x in page_errors)
    ids = result["ids"]
    if any(not x for x in ids) or len(ids) != len(set(ids)):
        errors.append({"type":"invalid-slide-ids","ids":ids})
    if any(not x for x in result["pageNums"]): warnings.append({"type":"missing-page-number"})

    report={"passed": not errors, "slides": result["slides"], "errors": errors, "warnings": warnings,
            "summary":{"broken_images":len(result["brokenImages"]),"overflows":len(result["overflows"]),"console_errors":len(console_errors),"page_errors":len(page_errors),"small_text":len(result["smallText"]),"missing_alt":len(result["missingAlt"])}}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False))
    print(("✓ PASS" if report["passed"] else "✗ FAIL") + f": {args.report.resolve()}")
    sys.exit(0 if report["passed"] else 2)

if __name__ == "__main__": main()
