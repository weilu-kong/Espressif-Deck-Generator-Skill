#!/usr/bin/env python3
"""
Universal standalone packager for Espressif Web Decks.
Converts all referenced local images/SVGs into embedded Base64 Data URIs,
producing a 100% self-contained HTML presentation that opens anywhere without missing images.

Usage:
    python3 inline_assets.py [input_html] [output_html]
"""
import sys
import os
import re
import base64
import mimetypes

def inline_deck(input_html, output_html=None):
    if not os.path.exists(input_html):
        print(f"Error: File not found: {input_html}")
        sys.exit(1)
        
    input_abs = os.path.abspath(input_html)
    base_dir = os.path.dirname(input_abs)
    
    if not output_html:
        stem = os.path.splitext(os.path.basename(input_abs))[0]
        output_html = os.path.join(base_dir, f"{stem}_standalone.html")
    else:
        output_html = os.path.abspath(output_html)
        
    with open(input_abs, "r", encoding="utf-8") as f:
        html = f.read()
        
    # Match all src="..." in img tags
    matches = list(set(re.findall(r"""<img[^>]+src=["']([^"']+)["']""", html)))
    print(f"Found {len(matches)} distinct img src tags.")
    
    inlined_count = 0
    for rel_path in matches:
        if rel_path.startswith("data:") or rel_path.startswith("http://") or rel_path.startswith("https://"):
            continue
            
        full_path = os.path.join(base_dir, rel_path)
        if os.path.exists(full_path):
            mime, _ = mimetypes.guess_type(full_path)
            if full_path.lower().endswith(".svg"):
                mime = "image/svg+xml"
            elif not mime:
                mime = "application/octet-stream"
                
            with open(full_path, "rb") as img_f:
                b64_str = base64.b64encode(img_f.read()).decode("utf-8")
                
            data_uri = f"data:{mime};base64,{b64_str}"
            html = html.replace(f'src="{rel_path}"', f'src="{data_uri}"')
            html = html.replace(f"src='{rel_path}'", f"src='{data_uri}'")
            inlined_count += 1
            print(f"  ✓ Inlined {rel_path} ({mime})")
        else:
            print(f"  ⚠️ Warning: Local image not found: {full_path}")
            
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html)
        
    size_mb = os.path.getsize(output_html) / (1024 * 1024)
    print(f"✓ Standalone HTML packaged: {output_html} ({size_mb:.2f} MB, {inlined_count} images inlined)")

if __name__ == "__main__":
    in_file = sys.argv[1] if len(sys.argv) > 1 else "latest_progress.html"
    if not os.path.exists(in_file) and os.path.exists("index.html"):
        in_file = "index.html"
    out_file = sys.argv[2] if len(sys.argv) > 2 else None
    inline_deck(in_file, out_file)
