#!/usr/bin/env python3
"""Inline local HTML assets into a standalone file.
Handles img/source/srcset, CSS url(), local stylesheets, local scripts and favicon-like hrefs.
Also exposes ``inline_html`` for browser-based validation/export without file:// navigation.
"""
from __future__ import annotations
import argparse, base64, mimetypes, re
from pathlib import Path

REMOTE_PREFIXES=("data:","http://","https://","//","mailto:","tel:","#","javascript:")

def is_local(ref:str)->bool:
    ref=(ref or "").strip()
    return bool(ref) and not ref.startswith(REMOTE_PREFIXES)

def strip_q(ref): return ref.split('#',1)[0].split('?',1)[0]

def data_uri(path:Path):
    mime,_=mimetypes.guess_type(str(path)); mime=mime or "application/octet-stream"
    if path.suffix.lower()=='.svg': mime='image/svg+xml'
    return f"data:{mime};base64,"+base64.b64encode(path.read_bytes()).decode('ascii')

def resolve(base:Path, ref:str): return (base / strip_q(ref)).resolve()

def inline_css_urls(css:str, base:Path, stats):
    pat=re.compile(r"url\(\s*(['\"]?)([^)'\"]+)\1\s*\)",re.I)
    def repl(m):
        ref=m.group(2).strip()
        if not is_local(ref): return m.group(0)
        p=resolve(base,ref)
        if not p.exists(): stats['missing'].append(str(p)); return m.group(0)
        stats['embedded']+=1
        return f'url("{data_uri(p)}")'
    return pat.sub(repl,css)

def inline_html(input_html:Path):
    input_html=Path(input_html).resolve()
    html=input_html.read_text(encoding='utf-8'); base=input_html.parent; stats={'embedded':0,'missing':[]}

    link_pat=re.compile(r'<link\b([^>]*?)href=["\']([^"\']+)["\']([^>]*)>',re.I)
    def link_repl(m):
        attrs=(m.group(1)+m.group(3)).lower(); ref=m.group(2)
        if 'stylesheet' in attrs and is_local(ref):
            p=resolve(base,ref)
            if not p.exists(): stats['missing'].append(str(p)); return m.group(0)
            css=inline_css_urls(p.read_text(encoding='utf-8'),p.parent,stats); stats['embedded']+=1
            return '<style data-inlined-from="'+ref+'">'+css+'</style>'
        if is_local(ref):
            p=resolve(base,ref)
            if p.exists(): stats['embedded']+=1; return m.group(0).replace(ref,data_uri(p))
            stats['missing'].append(str(p))
        return m.group(0)
    html=link_pat.sub(link_repl,html)

    script_pat=re.compile(r'<script\b([^>]*?)src=["\']([^"\']+)["\']([^>]*)>\s*</script>',re.I)
    def script_repl(m):
        ref=m.group(2)
        if not is_local(ref): return m.group(0)
        p=resolve(base,ref)
        if not p.exists(): stats['missing'].append(str(p)); return m.group(0)
        stats['embedded']+=1
        return '<script data-inlined-from="'+ref+'">\n'+p.read_text(encoding='utf-8')+'\n</script>'
    html=script_pat.sub(script_repl,html)

    attr_pat=re.compile(r'(?P<attr>src|poster)=(?P<q>["\'])(?P<ref>[^"\']+)(?P=q)',re.I)
    def attr_repl(m):
        ref=m.group('ref')
        if not is_local(ref): return m.group(0)
        p=resolve(base,ref)
        if not p.exists(): stats['missing'].append(str(p)); return m.group(0)
        stats['embedded']+=1
        return f"{m.group('attr')}={m.group('q')}{data_uri(p)}{m.group('q')}"
    html=attr_pat.sub(attr_repl,html)

    srcset_pat=re.compile(r'srcset=(["\'])([^"\']+)\1',re.I)
    def srcset_repl(m):
        out=[]
        for entry in m.group(2).split(','):
            bits=entry.strip().split()
            if not bits: continue
            ref=bits[0]
            if is_local(ref):
                p=resolve(base,ref)
                if p.exists(): bits[0]=data_uri(p); stats['embedded']+=1
                else: stats['missing'].append(str(p))
            out.append(' '.join(bits))
        return 'srcset='+m.group(1)+', '.join(out)+m.group(1)
    html=srcset_pat.sub(srcset_repl,html)

    html=inline_css_urls(html,base,stats)

    unresolved=[]
    for ref in re.findall(r'(?:src|href|poster)=["\']([^"\']+)["\']',html,re.I):
        if is_local(ref): unresolved.append(ref)
    for ref in re.findall(r'url\(\s*["\']?([^\)"\']+)',html,re.I):
        if is_local(ref): unresolved.append(ref.strip())
    stats['missing']=sorted(set(stats['missing'])); stats['unresolved']=sorted(set(unresolved))
    return html, stats

def process(input_html:Path, output:Path, strict=False):
    html, stats=inline_html(input_html)
    output.parent.mkdir(parents=True,exist_ok=True); output.write_text(html,encoding='utf-8')
    print(f"✓ Standalone HTML: {output.resolve()}")
    print(f"  Embedded assets: {stats['embedded']}")
    print(f"  Missing local files: {len(stats['missing'])}")
    print(f"  Unresolved local references: {len(stats['unresolved'])}")
    if stats['missing']:
        for x in stats['missing']: print('  MISSING:',x)
    if stats['unresolved']:
        for x in stats['unresolved']: print('  UNRESOLVED:',x)
    if strict and (stats['missing'] or stats['unresolved']): raise SystemExit(2)
    return stats

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('input',type=Path); ap.add_argument('-o','--output',type=Path); ap.add_argument('--strict',action='store_true'); args=ap.parse_args()
    out=args.output or args.input.with_name(args.input.stem+'_standalone.html')
    process(args.input.resolve(),out.resolve(),args.strict)
if __name__=='__main__': main()
