#!/usr/bin/env python3
"""
Universal 1080p PDF exporter for Espressif Web Decks.
Uses headless Google Chrome via Playwright and compiles into a 16:9 1080p PDF using ReportLab.

Usage:
    uv run --with playwright --with reportlab --with pillow python export_pdf.py [input_html] [output_pdf]
"""
import sys
import os
import re
import tempfile
from playwright.sync_api import sync_playwright
from reportlab.pdfgen import canvas

PAGE_WIDTH = 1920
PAGE_HEIGHT = 1080

def export_deck_to_pdf(html_path, output_pdf=None):
    if not os.path.exists(html_path):
        print(f"Error: File not found: {html_path}")
        sys.exit(1)
        
    html_abs = os.path.abspath(html_path)
    base_dir = os.path.dirname(html_abs)
    
    # Read HTML title for PDF metadata
    with open(html_abs, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    title_match = re.search(r"<title>(.*?)</title>", html_content, re.IGNORECASE)
    doc_title = title_match.group(1).strip() if title_match else "Espressif Systems Presentation"
    
    if not output_pdf:
        stem = os.path.splitext(os.path.basename(html_abs))[0]
        output_pdf = os.path.join(base_dir, f"{stem}_1080p.pdf")
    else:
        output_pdf = os.path.abspath(output_pdf)
        
    html_url = f"file://{html_abs}"
    print(f"Loading deck: {html_url}")
    print(f"Output PDF target: {output_pdf}")

    with tempfile.TemporaryDirectory() as tmpdir:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                args=["--disable-web-security", "--allow-file-access-from-files"]
            )
            # Render at 2x Retina resolution for crisp vector/raster output
            page = browser.new_page(
                viewport={"width": PAGE_WIDTH, "height": PAGE_HEIGHT},
                device_scale_factor=2
            )
            
            page.goto(html_url, wait_until="networkidle")
            page.wait_for_timeout(1000)
            
            # Hide interactive UI chrome (nav dots, hint bars, ESC overview)
            page.evaluate("""() => {
                const style = document.createElement('style');
                style.innerHTML = `
                    #hint, #nav, #overview { display: none !important; }
                    #deck { transition: none !important; }
                    * { transition: none !important; }
                `;
                document.head.appendChild(style);
            }""")
            
            total_slides = page.evaluate("() => document.querySelectorAll('.slide').length")
            print(f"Detected {total_slides} slides in deck.")
            
            shot_paths = []
            for i in range(total_slides):
                print(f"  Rendering slide {i + 1} / {total_slides}...")
                page.evaluate(f"""() => {{
                    const deck = document.getElementById('deck');
                    const slides = document.querySelectorAll('.slide');
                    deck.style.transition = 'none';
                    deck.style.transform = 'translateX(-{i * 100}vw)';
                    
                    const el = slides[{i}];
                    const isDark = el.classList.contains('dark') || el.classList.contains('accent');
                    document.body.classList.toggle('dark-bg', isDark);
                    window.__currentSlideIndex = {i};
                    if (window.__playSlide) window.__playSlide({i});
                }}""")
                
                # Allow Canvas ASCII field and animations to stabilize
                page.wait_for_timeout(600)
                
                # Ensure all elements have opacity: 1 and no hidden state
                page.evaluate(f"""() => {{
                    const s = document.querySelectorAll('.slide')[{i}];
                    s.querySelectorAll('*').forEach(el => {{
                        const op = window.getComputedStyle(el).opacity;
                        if (op === '0' || parseFloat(op) < 0.9) {{
                            el.style.opacity = '1';
                        }}
                    }});
                }}""")
                
                shot_path = os.path.join(tmpdir, f"slide_{i+1:02d}.png")
                page.screenshot(path=shot_path, full_page=False)
                shot_paths.append(shot_path)
                
            browser.close()

        print(f"Compiling {len(shot_paths)} slides into 1080p PDF...")
        c = canvas.Canvas(output_pdf, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
        c.setTitle(doc_title)
        c.setAuthor("Espressif Systems")
        c.setSubject(doc_title)

        for f in shot_paths:
            c.drawImage(f, 0, 0, width=PAGE_WIDTH, height=PAGE_HEIGHT)
            c.showPage()
        c.save()

    size_mb = os.path.getsize(output_pdf) / (1024 * 1024)
    print(f"✓ PDF export complete: {output_pdf} ({size_mb:.2f} MB, {total_slides} pages)")

if __name__ == "__main__":
    in_html = sys.argv[1] if len(sys.argv) > 1 else "latest_progress.html"
    if not os.path.exists(in_html) and os.path.exists("index.html"):
        in_html = "index.html"
    out_pdf = sys.argv[2] if len(sys.argv) > 2 else None
    export_deck_to_pdf(in_html, out_pdf)
