#!/usr/bin/env python3
"""Render an Espressif Web Deck from YAML or JSON.

Usage:
  python3 scripts/render_deck.py deck.yaml -o output/deck.html
  uv run --with pyyaml python scripts/render_deck.py deck.yaml -o output/deck.html
"""
from __future__ import annotations
import argparse, html, json, re, sys, shutil, hashlib
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parents[1]
SPEC_DIR = Path.cwd()
OUTPUT_DIR = Path.cwd()


def load_spec(path: Path):
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    try:
        import yaml  # type: ignore
    except ImportError:
        raise SystemExit("PyYAML is required for YAML input. Run: uv run --with pyyaml python scripts/render_deck.py ...")
    return yaml.safe_load(text)


def esc(value) -> str:
    return html.escape(str(value or ""), quote=True)

def text_html(value) -> str:
    return esc(value).replace("\n", "<br>")


def safe_id(value: str, fallback: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_-]+", "-", value or "").strip("-").lower()
    return value or fallback


def list_items(items, css="bullets"):
    if not items:
        return ""
    return f'<ul class="{css}">' + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"


def heading(slide):
    eyebrow = f'<div class="eyebrow">{esc(slide.get("eyebrow"))}</div>' if slide.get("eyebrow") else ""
    subtitle = f'<div class="slide-subtitle">{esc(slide.get("subtitle"))}</div>' if slide.get("subtitle") else ""
    return f'{eyebrow}<h1 class="slide-title">{esc(slide.get("title"))}</h1>{subtitle}'


def source_html(slide):
    src = slide.get("source")
    if not src:
        return ""
    if isinstance(src, list):
        text = " · ".join(str(x) for x in src)
    elif isinstance(src, dict):
        text = " · ".join(f"{k}: {v}" for k, v in src.items())
    else:
        text = str(src)
    return f'<div class="footer-source">Source: {esc(text)}</div>'


def chrome(i, total, deck_meta):
    label = deck_meta.get("kicker") or deck_meta.get("title") or "ESPRESSIF SYSTEMS"
    return (
        '<div class="chrome">'
        '<div class="brand-mark"><span class="brand-dot"></span><span>ESPRESSIF</span>'
        f'<span style="opacity:.42;font-weight:500">{esc(label)}</span></div>'
        f'<div class="page-num">{i:02d} / {total:02d}</div>'
        '</div>'
    )


def image_tag(path, alt, cls=""):
    if not path:
        return '<div style="color:var(--muted-2);font-size:18px">No image provided</div>'
    src = str(path)
    if not (src.startswith(("data:", "http://", "https://", "//", "file:"))):
        candidate = (SPEC_DIR / src).resolve()
        if candidate.exists() and candidate.is_file():
            asset_dir = OUTPUT_DIR / "_deck_assets"
            asset_dir.mkdir(parents=True, exist_ok=True)
            digest = hashlib.sha1(str(candidate).encode("utf-8")).hexdigest()[:8]
            target = asset_dir / f"{candidate.stem}-{digest}{candidate.suffix}"
            if not target.exists() or target.stat().st_mtime < candidate.stat().st_mtime:
                shutil.copy2(candidate, target)
            src = f"_deck_assets/{target.name}"
    return f'<img class="{esc(cls)}" src="{esc(src)}" alt="{esc(alt)}">'


def specs_block(specs):
    if not specs:
        return ""
    rows = "".join(
        f'<div class="spec-mini-row"><span>{esc(k)}</span><b>{esc(v)}</b></div>' for k, v in specs.items()
    )
    return f'<div class="spec-mini">{rows}</div>'


def product_card(p):
    badge = f'<div class="badge">{esc(p.get("badge"))}</div>' if p.get("badge") else ""
    positioning = f'<div class="card-positioning">{esc(p.get("positioning"))}</div>' if p.get("positioning") else ""
    apps = p.get("applications") or []
    app_html = '<div class="app-list">' + "".join(f'<span class="app-chip">{esc(x)}</span>' for x in apps) + '</div>' if apps else ""
    image = image_tag(p.get("image"), p.get("name", "product"))
    spec = specs_block(p.get("specs") or {})
    hardware = f'<div class="hardware-box"><div>{image}</div>{spec}</div>'
    return f'<article class="card product-card">{badge}<h2 class="card-title">{esc(p.get("name"))}</h2>{positioning}{list_items(p.get("highlights") or [])}{app_html}{hardware}</article>'


def render_slide(slide, i, total, deck_meta):
    stype = slide.get("type")
    sid = safe_id(slide.get("id"), "") if slide.get("id") else f"slide-{i:02d}-{safe_id(slide.get("title", ""), "untitled")}"
    common = {"slide_id": sid, "chrome": chrome(i, total, deck_meta), "heading": heading(slide), "source": source_html(slide)}

    if stype == "cover":
        presenter_parts = []
        for key in ("company", "presenter", "date"):
            val = slide.get(key) or deck_meta.get(key if key != "presenter" else "author")
            if val: presenter_parts.append(f"<div>{esc(val)}</div>")
        presenter = '<div class="presenter">' + "".join(presenter_parts) + '</div>' if presenter_parts else ""
        data = {**common, "eyebrow": esc(slide.get("eyebrow") or deck_meta.get("kicker") or "TECHNOLOGY UPDATE"), "title": text_html(slide.get("title")), "subtitle": text_html(slide.get("subtitle") or ""), "presenter": presenter}
        template = "cover.html"
    elif stype == "section":
        data = {**common, "section_no": f"{i:02d}", "eyebrow": esc(slide.get("eyebrow") or "SECTION"), "title": text_html(slide.get("title")), "subtitle": text_html(slide.get("subtitle") or "")}
        template = "section.html"
    elif stype == "product_compare":
        products = slide.get("products") or []
        cls = "grid-2" if len(products) <= 2 else "grid-3"
        content = f'<div class="{cls}">' + "".join(product_card(p) for p in products[:3]) + "</div>"
        data = {**common, "content": content}; template = "product-compare.html"
    elif stype == "product_detail":
        p = slide.get("product") or (slide.get("products") or [{}])[0]
        badge = f'<div class="badge">{esc(p.get("badge"))}</div>' if p.get("badge") else ""
        metric = ""
        if p.get("hero_stat"):
            hs = p["hero_stat"]
            if isinstance(hs, dict):
                metric = f'<div class="metric"><div class="metric-value">{esc(hs.get("value"))}</div><div class="metric-label">{esc(hs.get("label"))}</div></div>'
        left = f'<div class="card card-strong">{badge}<h2 class="card-title">{esc(p.get("name"))}</h2><div class="card-positioning">{esc(p.get("positioning"))}</div>{metric}{list_items(p.get("highlights") or [])}<div class="app-list">' + "".join(f'<span class="app-chip">{esc(x)}</span>' for x in (p.get("applications") or [])) + f'</div>{specs_block(p.get("specs") or {})}</div>'
        right = f'<div class="detail-image">{image_tag(p.get("image"), p.get("name", "product"))}</div>'
        data = {**common, "content": f'<div class="detail-layout">{left}{right}</div>'}; template = "product-detail.html"
    elif stype == "spec_table":
        columns = slide.get("columns") or []
        rows = slide.get("rows") or []
        th = "".join(f"<th>{esc(c)}</th>" for c in columns)
        body = []
        for row in rows:
            cells = row if isinstance(row, list) else [row.get(c, "") for c in columns]
            body.append("<tr>" + "".join(f"<td>{esc(x)}</td>" for x in cells) + "</tr>")
        content = f'<div class="table-wrap"><table class="spec-table"><thead><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'
        data = {**common, "content": content}; template = "spec-table.html"
    elif stype == "architecture":
        nodes = slide.get("nodes") or []
        conns = slide.get("connections") or []
        pieces = []
        for idx, n in enumerate(nodes):
            tone = safe_id(n.get("tone", ""), "")
            pieces.append(f'<div class="arch-node {"tone-" + tone if tone else ""}"><div class="arch-label">{esc(n.get("label"))}</div><div class="arch-detail">{esc(n.get("detail"))}</div></div>')
            if idx < len(nodes)-1:
                label = ""
                if idx < len(conns): label = esc(conns[idx].get("label", "")) if isinstance(conns[idx], dict) else esc(conns[idx])
                pieces.append(f'<div class="arch-arrow">→<small>{label}</small></div>')
        data = {**common, "content": '<div class="arch-flow">' + "".join(pieces) + '</div>'}; template = "architecture.html"
    elif stype == "image_focus":
        fit = "cover" if slide.get("fit") == "cover" else "contain"
        img = f'<div class="image-stage {fit}">{image_tag(slide.get("image"), slide.get("caption") or slide.get("title"))}</div>'
        side = f'<div class="card card-strong"><h2 class="card-title">{esc(slide.get("side_title") or "Key points")}</h2>{list_items(slide.get("bullets") or [])}<div class="caption">{esc(slide.get("caption") or "")}</div></div>'
        data = {**common, "content": f'<div class="image-layout">{img}{side}</div>'}; template = "image-focus.html"
    elif stype == "three_column":
        cols = slide.get("columns") or []
        cards = []
        for idx, c in enumerate(cols[:3], 1):
            cards.append(f'<article class="card column-card"><div class="column-number">0{idx}</div><h2 class="card-title">{esc(c.get("title"))}</h2><div class="card-positioning">{esc(c.get("body"))}</div>{list_items(c.get("bullets") or [])}</article>')
        data = {**common, "content": '<div class="grid-3">' + "".join(cards) + '</div>'}; template = "three-column.html"
    elif stype == "ending":
        contact = f'<div class="ending-contact">{esc(slide.get("contact") or "")}</div>' if slide.get("contact") else ""
        qr = f'<img class="qr" src="{esc(slide.get("qr_image"))}" alt="QR code">' if slide.get("qr_image") else ""
        data = {**common, "title": text_html(slide.get("title")), "subtitle": text_html(slide.get("subtitle") or ""), "contact": contact, "qr": qr}; template = "ending.html"
    else:
        raise ValueError(f"Unsupported slide type: {stype!r}")

    raw = (ROOT / "assets" / "templates" / template).read_text(encoding="utf-8")
    return Template(raw).safe_substitute(data)


def validate_minimal(spec):
    if not isinstance(spec, dict): raise ValueError("Deck spec must be an object")
    if not isinstance(spec.get("deck"), dict): raise ValueError("Missing deck object")
    if not spec["deck"].get("title"): raise ValueError("deck.title is required")
    slides = spec.get("slides")
    if not isinstance(slides, list) or not slides: raise ValueError("slides must be a non-empty array")
    allowed = {"cover","section","product_compare","product_detail","spec_table","architecture","image_focus","three_column","ending"}
    for i, slide in enumerate(slides, 1):
        if not isinstance(slide, dict): raise ValueError(f"Slide {i} must be an object")
        if slide.get("type") not in allowed: raise ValueError(f"Slide {i}: unsupported type {slide.get('type')!r}")
        if not slide.get("title"): raise ValueError(f"Slide {i}: title is required")


def build_html(spec, output: Path):
    validate_minimal(spec)
    deck_meta = spec["deck"]
    slides = spec["slides"]
    rendered = "\n".join(render_slide(s, i, len(slides), deck_meta) for i, s in enumerate(slides, 1))
    rel_theme = Path("assets/css/theme.css")
    rel_components = Path("assets/css/components.css")
    rel_print = Path("assets/css/print.css")
    rel_js = Path("assets/js/deck.js")
    # Embed skill CSS/JS into output so generated HTML is portable from the start.
    theme = (ROOT / rel_theme).read_text(encoding="utf-8")
    components = (ROOT / rel_components).read_text(encoding="utf-8")
    print_css = (ROOT / rel_print).read_text(encoding="utf-8")
    js = (ROOT / rel_js).read_text(encoding="utf-8")
    lang = deck_meta.get("language") or "ja"
    title = esc(deck_meta.get("title"))
    doc = f'''<!doctype html>
<html lang="{esc(lang)}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>
<style>{theme}\n{components}</style>
<style media="print">{print_css}</style></head>
<body><div id="viewport"><div id="deck-stage"><main id="deck">{rendered}</main></div></div><div id="nav-hint">← → navigate · B motion</div>
<script>{js}</script></body></html>'''
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(doc, encoding="utf-8")


def main():
    global SPEC_DIR, OUTPUT_DIR
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("-o", "--output", type=Path)
    args = ap.parse_args()
    input_path = args.input.resolve()
    spec = load_spec(input_path)
    out = (args.output or input_path.with_suffix(".html")).resolve()
    SPEC_DIR = input_path.parent
    OUTPUT_DIR = out.parent
    build_html(spec, out)
    print(f"✓ Rendered {len(spec['slides'])} slides: {out.resolve()}")

if __name__ == "__main__":
    main()
