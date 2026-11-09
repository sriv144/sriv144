"""Render README with GitHub's API, then serve a local review canvas.

Run: python scripts/preview.py [--port 8765] [--build-only]
Optional GH_TOKEN authenticates the Markdown rendering request.
"""
from __future__ import annotations

import argparse
import json
import os
import re
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"
CSS = """
:root {color-scheme:dark;--bg:#090d17;--fg:#edf1ff;--muted:#8c97b0;--line:#253049;--link:#b7a3ff;--chip:#192039;--panel:#0e1424}
:root[data-theme=light] {color-scheme:light;--bg:#fff;--fg:#1f2334;--muted:#626b80;--line:#d9dcec;--link:#6d28d9;--chip:#f1effa;--panel:#f8f7fc}
* {box-sizing:border-box} body {margin:0;background:var(--bg);color:var(--fg);font:16px/1.65 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
button {font:inherit;color:inherit;cursor:pointer;background:var(--chip);border:1px solid var(--line);padding:5px 12px;border-radius:6px}
.reviewbar {border-bottom:1px solid var(--line);background:var(--panel)}
.reviewbar>div {max-width:1000px;margin:auto;padding:16px 24px;display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}
.reviewbar small {color:var(--muted)} .controls {display:flex;gap:8px;flex-wrap:wrap}
main {max-width:1040px;padding:28px 36px 48px;margin:28px auto;border:1px solid var(--line);border-radius:10px}
.file-label {color:var(--muted);font:12px/1.5 ui-monospace,monospace;margin:0 0 28px}
article img {max-width:100%;vertical-align:middle;height:auto} article picture {display:block}
a {color:var(--link);text-decoration:none} a:hover {text-decoration:underline}
h1,h2,h3 {font-weight:600;line-height:1.35;margin:28px 0 16px} h2 {font-size:24px;padding-bottom:9px;border-bottom:1px solid var(--line);margin-top:36px}
h3 {font-size:20px;margin:8px 0 10px} p {margin:0 0 16px} sub {font-size:11px;color:var(--muted);letter-spacing:.045em}
code {font:12px ui-monospace,SFMono-Regular,Consolas,monospace;background:var(--chip);padding:.3em .55em;border-radius:5px;white-space:normal}
table {border-collapse:collapse;display:block;max-width:100%;overflow-x:auto;font-size:14px;margin-bottom:24px;width:100%}
th,td {border:1px solid var(--line);padding:14px;text-align:left;vertical-align:top} th {background:var(--panel)} tr:nth-child(even) {background:var(--panel)}
td h3 {font-size:19px;margin-top:14px} td p {margin-bottom:14px} td picture {min-width:0} td img {display:block}
details {padding:14px 0} summary {cursor:pointer;color:var(--link)} hr {height:1px;padding:0;border:0;background:var(--line);margin:30px 0}
.markdown-heading a.anchor {display:none}
@media(max-width:600px) {main {margin:12px 8px;padding:16px 12px 28px}.reviewbar>div {padding:12px 16px}body {font-size:15px}td {padding:8px}td h3 {font-size:16px}td p {font-size:13px;line-height:1.5}td code {font-size:10px}}
"""
JS = """
const root=document.documentElement;let paused=matchMedia('(prefers-reduced-motion: reduce)').matches;
function syncPictures(){
 const dark=root.dataset.theme!=='light',mobile=matchMedia('(max-width: 600px)').matches;
 document.querySelectorAll('picture').forEach(picture=>{
  const img=picture.querySelector('img');if(!img.dataset.original)img.dataset.original=img.getAttribute('src');
  picture.querySelectorAll('source').forEach(source=>source.removeAttribute('srcset'));
  let src=img.dataset.original;
  if(src.includes('hero-'))src='/assets/hero-'+(mobile?'mobile-':'')+(dark?'dark':'light')+'.svg';
  else if(src.includes('contributions-'))src='/assets/contributions-'+(dark?'dark':'light')+'.svg';
  else if(src.includes('activity-'))src='/assets/activity-'+(dark?'dark':'light')+'.svg';
  else if(src.includes('project-'))src=src.replace('.svg',mobile?'-mobile.svg':'.svg');
  else if(src.endsWith('/terminal.svg'))src=mobile?'/assets/terminal-mobile.svg':'/assets/terminal.svg';
  else if(src.endsWith('/stack.svg'))src=mobile?'/assets/stack-mobile.svg':'/assets/stack.svg';
  else if(src.includes('/toolbox-'))src='/assets/toolbox-'+(mobile?'mobile-':'')+(dark?'dark':'light')+'.svg';
  const next=paused&&!src.includes('/stack')&&!src.includes('/toolbox-')?src.replace('.svg','-static.svg'):src;
  if(img.getAttribute('src')!==next)img.src=next;
 });
 const control=document.getElementById('motion');control.textContent=paused?'Resume motion':'Pause motion';control.setAttribute('aria-pressed',String(paused));
}
document.getElementById('dark').onclick=()=>{root.dataset.theme='dark';syncPictures()};
document.getElementById('light').onclick=()=>{root.dataset.theme='light';syncPictures()};
document.getElementById('motion').onclick=()=>{paused=!paused;syncPictures()};
root.dataset.theme=matchMedia('(prefers-color-scheme: light)').matches?'light':'dark';
document.querySelectorAll('article h2').forEach(heading=>{heading.id=heading.textContent.toLowerCase().replace(/[^a-z0-9 -]/g,'').replace(/ /g,'-')});
window.addEventListener('resize',syncPictures);syncPictures();
"""


def build_preview() -> Path:
    payload = json.dumps({"text": (ROOT / "README.md").read_text(encoding="utf-8"), "mode": "gfm"}).encode()
    headers = {"Content-Type": "application/json", "Accept": "text/html", "User-Agent": "sriv144-profile-preview"}
    if os.environ.get("GH_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GH_TOKEN"]
    request = Request("https://api.github.com/markdown", data=payload, headers=headers, method="POST")
    with urlopen(request, timeout=30) as response:
        rendered = response.read().decode("utf-8")
    rendered = re.sub(r'(src|srcset)="(?:\./)?assets/', r'\1="/assets/', rendered)
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "github-rendered.html").write_text(rendered, encoding="utf-8")
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Srivaths · GitHub profile preview</title><link rel="icon" href="data:,"><style>{CSS}</style></head>
<body><header class="reviewbar"><div><div><strong>Profile preview</strong><br><small>GitHub-rendered README · local review canvas</small></div>
<div class="controls"><button id="dark" type="button">Dark</button><button id="light" type="button">Light</button><button id="motion" type="button" aria-pressed="false">Pause motion</button></div></div></header>
<main><p class="file-label">sriv144 / README.md</p><article>{rendered}</article></main><script>{JS}</script></body></html>'''
    target = OUTPUT / "preview.html"
    target.write_text(page, encoding="utf-8")
    raw = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>Native README picture check</title><style>{CSS}</style></head><body><main><article>{rendered}</article></main></body></html>'''
    (OUTPUT / "native-preview.html").write_text(raw, encoding="utf-8")
    return target


class PreviewHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path.startswith("/?"):
            self.path = "/output/preview.html"
        return super().do_GET()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--build-only", action="store_true")
    args = parser.parse_args()
    try:
        page = build_preview()
    except (HTTPError, URLError) as error:
        parser.exit(1, f"GitHub Markdown rendering failed: {error}\n")
    print(f"Built {page}", flush=True)
    if args.build_only:
        return
    handler = partial(PreviewHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    print(f"Preview: http://127.0.0.1:{args.port}/", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()


if __name__ == "__main__":
    main()
