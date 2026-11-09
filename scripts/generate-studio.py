#!/usr/bin/env python3
"""Generate original, self-contained SVG assets for Srivaths's GitHub profile.

Run with --check to validate that the committed assets match their source.
Technology symbols are original simplified illustrations, not official logos.
"""
from __future__ import annotations

import argparse
from html import escape
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BG = "#080d1a"
FG = "#f1f5ff"
MUTED = "#a7b4ce"
LINE = "#263149"


def wrap(title: str, description: str, body: str, *, width: int = 800,
         height: int = 360, accent: str = "#a78bfa", static: bool = False,
         extra_css: str = "") -> str:
    reset = ".moving,.scan,.arm,.hauling,.chartline,.network,.typed,.cursor{animation:none!important}.typed{clip-path:none!important}"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<defs><pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="{LINE}" stroke-width=".6" opacity=".5"/></pattern><radialGradient id="glow"><stop stop-color="{accent}" stop-opacity=".15"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient></defs>
<style>
text{{font-family:'Segoe UI',Arial,sans-serif;fill:{FG}}}.mono{{font-family:Consolas,'Liberation Mono',monospace}}.muted{{fill:{MUTED}}}.accent{{fill:{accent}}}
.moving{{animation:travel 5s linear infinite}}.scan{{animation:scan 3.4s ease-in-out infinite alternate}}.arm{{animation:arm 3.8s ease-in-out infinite alternate;transform-origin:0 0}}.hauling{{animation:haul 4s ease-in-out infinite alternate}}.chartline{{animation:chart 5.8s linear infinite}}.network{{animation:network 3s ease-in-out infinite}}.delay{{animation-delay:-1.5s}}
@keyframes travel{{to{{stroke-dashoffset:-120}}}}@keyframes scan{{to{{transform:translateY(138px)}}}}@keyframes arm{{to{{transform:rotate(-24deg)}}}}@keyframes haul{{to{{transform:translate(-34px,-18px)}}}}@keyframes chart{{0%{{stroke-dashoffset:600}}70%,100%{{stroke-dashoffset:0}}}}@keyframes network{{0%,100%{{opacity:.22}}50%{{opacity:1}}}}
{extra_css}
@media(prefers-reduced-motion:reduce){{{reset}}}
{reset if static else ''}
</style>
<rect width="{width}" height="{height}" rx="20" fill="{BG}"/><rect x="1" y="1" width="{width-2}" height="{height-2}" rx="19" fill="url(#grid)" stroke="{LINE}"/><ellipse cx="{width*.79:g}" cy="{height*.5:g}" rx="{width*.35:g}" ry="{height*.8:g}" fill="url(#glow)"/>
{body}
</svg>
'''


def finlens_visual() -> str:
    rows = ''.join(f'<path d="M535 {y}h{w}" stroke="#a78bfa" stroke-width="4" opacity=".45"/>' for y, w in [(139,65),(157,87),(175,75),(207,57),(225,82),(243,61)])
    return f'''<g><rect x="492" y="80" width="145" height="206" rx="12" fill="#121a30" stroke="#4a3d72" transform="rotate(-9 565 183)"/>
<path d="M523 88h95l33 34v167H523Z" fill="#111a30" stroke="#a78bfa" stroke-width="2"/><path d="M618 88v34h33" fill="none" stroke="#a78bfa" stroke-width="2"/>{rows}
<rect class="scan" x="529" y="132" width="115" height="5" rx="2" fill="#c4b5fd"/><circle cx="689" cy="183" r="43" fill="#151b32" stroke="#c4b5fd" stroke-width="3"/><path d="m718 214 28 30" stroke="#c4b5fd" stroke-width="9" stroke-linecap="round"/><path d="m671 183 12 12 23-26" fill="none" stroke="#a78bfa" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
<path class="moving" d="M651 150h27M651 231h39" fill="none" stroke="#a78bfa" stroke-width="3" stroke-dasharray="6 10"/>
<rect x="532" y="301" width="175" height="27" rx="5" fill="#1c2340"/><text x="619" y="321" text-anchor="middle" class="mono accent" font-size="17">RETRIEVE → REASON</text></g>'''


def block(x: int, y: int, scale: float = 1) -> str:
    return f'''<g transform="translate({x} {y}) scale({scale})"><path d="M0-31 52-5 0 22-52-5Z" fill="#67e8f9" fill-opacity=".5" stroke="#67e8f9"/><path d="M-52-5 0 22v45l-52-26Z" fill="#164b63" stroke="#67e8f9"/><path d="m0 22 52-27v46L0 67Z" fill="#20778b" stroke="#67e8f9"/></g>'''


def robot(x: int, y: int, *, moving: bool = False) -> str:
    return f'''<g transform="translate({x} {y})"><g class="{'hauling' if moving else ''}"><ellipse cy="17" rx="24" ry="10" fill="#07111e"/><rect x="-23" y="-10" width="46" height="26" rx="9" fill="#18364a" stroke="#67e8f9" stroke-width="2"/><circle cx="-12" cy="17" r="5" fill="#67e8f9"/><circle cx="12" cy="17" r="5" fill="#67e8f9"/><circle cy="-11" r="10" fill="#67e8f9"/><g class="arm"><path d="M0-13 8-42 28-51" fill="none" stroke="#a5f3fc" stroke-width="5" stroke-linecap="round"/><circle cx="8" cy="-42" r="5" fill="#080d1a" stroke="#67e8f9" stroke-width="2"/></g></g></g>'''


def embodied_visual() -> str:
    return f'''<g><path d="m462 244 149-92 149 82-149 91Z" fill="#0b1a2c" stroke="#22526a"/><path class="moving" d="m476 250 135-83 134 74-134 77Z" fill="none" stroke="#67e8f9" stroke-width="2" stroke-dasharray="8 12"/>
{block(584,182,.75)}{block(647,216,.75)}{block(584,140,.75)}
{robot(493,223)}{robot(719,224)}{robot(603,302, moving=True)}
<path d="M579 80h79M618 41v78" stroke="#67e8f9" opacity=".35"/><circle class="network" cx="618" cy="80" r="24" fill="none" stroke="#67e8f9"/><circle cx="618" cy="80" r="5" fill="#67e8f9"/></g>'''


def aegis_visual() -> str:
    candles = []
    for i, (y, h, up) in enumerate([(207,30,1),(184,35,1),(171,22,0),(187,35,0),(154,46,1),(129,39,1),(146,24,0),(109,45,1)]):
        x = 487+i*34
        color = '#6ee7b7' if up else '#6885a4'
        candles.append(f'<path d="M{x} {y-12}v{h+24}" stroke="{color}" stroke-width="2"/><rect x="{x-8}" y="{y}" width="16" height="{h}" rx="2" fill="{color}"/>')
    return f'''<g><rect x="462" y="69" width="300" height="240" rx="12" fill="#0c1825" stroke="#254b43"/><path d="M478 119h268M478 164h268M478 209h268M478 254h268" stroke="#234238" stroke-dasharray="3 7"/>{''.join(candles)}
<path class="chartline" d="m478 263 34-20 34 8 34-37 34 11 34-47 34 14 34-44 29-19" fill="none" stroke="#a7f3d0" stroke-width="3" stroke-dasharray="600"/>
<rect x="563" y="282" width="184" height="28" rx="5" fill="#133329"/><text x="655" y="302" text-anchor="middle" class="mono accent" font-size="17">PAPER TRADING ONLY</text></g>'''


def kube_visual() -> str:
    return '''<g><path d="m612 70 94 54v109l-94 54-94-54V124Z" fill="#211e21" stroke="#fbbf24" stroke-width="2"/><path class="moving" d="m612 92 74 43v86l-74 43-74-43v-86Z" fill="none" stroke="#fbbf24" stroke-dasharray="7 13" opacity=".7"/>
<path d="M612 178 518 124M612 178l94-54M612 178v109M612 178l-94 55M612 178l94 55M612 178V70" fill="none" stroke="#ad8739" stroke-width="2"/>
<circle class="network" cx="612" cy="70" r="15" fill="#fbbf24" fill-opacity=".2" stroke="#fbbf24"/><circle class="network delay" cx="518" cy="233" r="15" fill="#fbbf24" fill-opacity=".2" stroke="#fbbf24"/><circle class="network" cx="706" cy="233" r="15" fill="#fbbf24" fill-opacity=".2" stroke="#fbbf24"/>
<circle cx="518" cy="124" r="8" fill="#fbbf24"/><circle cx="706" cy="124" r="8" fill="#fbbf24"/><circle cx="612" cy="287" r="8" fill="#fbbf24"/>
<rect x="576" y="142" width="72" height="72" rx="15" fill="#342d22" stroke="#fbbf24" stroke-width="2"/><path d="m591 178 14 14 29-31" fill="none" stroke="#fde68a" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M468 177h66M690 177h65" stroke="#fbbf24" stroke-width="2" stroke-dasharray="4 9" class="moving"/></g>'''


PROJECTS = {
    'finlens': ('FinLens', 'DOCUMENT INTELLIGENCE', '#a78bfa', ['FinLens'], ['SEC filings. Source retrieval.', 'Answers with context.'], finlens_visual),
    'embodied': ('Embodied Skill Composer', 'ROBOTICS / SIMULATION', '#67e8f9', ['Embodied', 'Skill Composer'], ['Multi-robot coordination.', 'A construction digital twin.'], embodied_visual),
    'aegisquant': ('AegisQuant', 'QUANTITATIVE RESEARCH', '#6ee7b7', ['AegisQuant'], ['Point-in-time research.', 'Execution gates. Audit trails.'], aegis_visual),
    'kubesentient': ('KubeSentient', 'AGENTS / INFRASTRUCTURE', '#fbbf24', ['KubeSentient'], ['Investigate Kubernetes alerts.', 'Retrieve. Reason. Plan.'], kube_visual),
}


def project(key: str, static: bool) -> str:
    title, category, accent, titles, lines, visual = PROJECTS[key]
    size = 49 if len(titles[0]) > 10 else 59
    heading = ''.join(f'<text x="36" y="{131+i*55}" font-size="{48 if len(titles)>1 else size}" font-weight="700" letter-spacing="-1.5">{escape(line)}</text>' for i, line in enumerate(titles))
    capability = ''.join(f'<text x="36" y="{258+i*31}" font-size="23" class="muted">{escape(line)}</text>' for i, line in enumerate(lines))
    body = f'<rect x="36" y="38" width="30" height="4" rx="2" fill="{accent}"/><text x="36" y="77" class="mono accent" font-size="19" letter-spacing=".8">{escape(category)}</text>{heading}{capability}<path d="M36 320h370" stroke="{LINE}"/>{visual()}'
    return wrap(title, f'{title}. {" ".join(lines)} Decorative illustration; no performance statistics.', body, accent=accent, static=static)


def terminal(static: bool) -> str:
    code = [
        '<tspan fill="#c4b5fd">const</tspan> <tspan fill="#67e8f9">srivaths</tspan> = {',
        '  role: <tspan fill="#a7f3d0">"AI &amp; systems builder"</tspan>,',
        '  focus: [<tspan fill="#fbbf24">"agents", "retrieval", "robotics"</tspan>],',
        '  stack: [<tspan fill="#a7f3d0">"Python", "TypeScript", "SQL"</tspan>],',
        '  mindset: <tspan fill="#a7f3d0">"build → test → learn → repeat"</tspan>',
        '};',
    ]
    lines = ''.join(f'<text x="46" y="{91+i*35}" class="mono" font-size="27" xml:space="preserve">{line}</text>' for i, line in enumerate(code))
    body = f'''<path d="M1 49h1198" stroke="{LINE}"/><circle cx="28" cy="25" r="6" fill="#fb7185"/><circle cx="50" cy="25" r="6" fill="#fbbf24"/><circle cx="72" cy="25" r="6" fill="#6ee7b7"/><text x="600" y="31" text-anchor="middle" class="mono muted" font-size="17">srivaths@dev-lab ~ profile.ts</text>{lines}
<g class="typed"><text x="46" y="326" class="mono accent" font-size="25">$ turning curiosity into working code<tspan class="cursor">_</tspan></text></g>'''
    css = '.typed{animation:typing 4.2s steps(43,end) .6s both}.cursor{animation:cursor 1.4s steps(1,end) 4.8s infinite}@keyframes typing{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}@keyframes cursor{50%{opacity:0}}'
    return wrap('Srivaths — developer terminal', 'Code profile: AI and systems builder; focus on agents, retrieval, and robotics; Python, TypeScript, SQL; build, test, learn, repeat.', body, width=1200, accent='#67e8f9', static=static, extra_css=css)


def project_mobile(key: str, static: bool) -> str:
    title, category, accent, titles, _, visual = PROJECTS[key]
    short = {
        'finlens': 'Financial document intelligence',
        'embodied': 'Multi-robot simulation',
        'aegisquant': 'Research + paper trading',
        'kubesentient': 'Kubernetes investigation',
    }[key]
    heading = ''.join(f'<text x="24" y="{110+i*47}" font-size="40" font-weight="700" letter-spacing="-1.2">{escape(line)}</text>' for i, line in enumerate(titles))
    capability_y = 191 if len(titles) > 1 else 161
    body = f'''<rect x="24" y="24" width="30" height="4" rx="2" fill="{accent}"/><text x="24" y="62" class="mono accent" font-size="22">{escape(category)}</text>{heading}<text x="24" y="{capability_y}" class="muted" font-size="22">{escape(short)}</text><g transform="translate(-290 174) scale(.8)">{visual()}</g>'''
    return wrap(title, f'{title}. {short}. Decorative illustration; no performance statistics.', body, width=400, height=440, accent=accent, static=static)


def terminal_mobile(static: bool) -> str:
    code = [
        '<tspan fill="#c4b5fd">const</tspan> <tspan fill="#67e8f9">srivaths</tspan> = {',
        '  role: <tspan fill="#a7f3d0">"AI &amp; systems builder"</tspan>,',
        '  focus: [<tspan fill="#fbbf24">"agents", "retrieval"</tspan>,',
        '          <tspan fill="#fbbf24">"robotics"</tspan>],',
        '  stack: [<tspan fill="#a7f3d0">"Python", "TypeScript", "SQL"</tspan>],',
        '  mindset: <tspan fill="#a7f3d0">"build → test → learn → repeat"</tspan>',
        '};',
    ]
    lines = ''.join(f'<text x="28" y="{103+i*47}" class="mono" font-size="24" xml:space="preserve">{line}</text>' for i, line in enumerate(code))
    body = f'''<path d="M1 49h678" stroke="{LINE}"/><circle cx="26" cy="25" r="6" fill="#fb7185"/><circle cx="48" cy="25" r="6" fill="#fbbf24"/><circle cx="70" cy="25" r="6" fill="#6ee7b7"/><text x="383" y="31" text-anchor="middle" class="mono muted" font-size="22">srivaths@dev-lab ~ profile.ts</text>{lines}<g class="typed"><text x="28" y="476" class="mono accent" font-size="27">$ turning curiosity into</text><text x="28" y="516" class="mono accent" font-size="27">working code<tspan class="cursor">_</tspan></text></g>'''
    css = '.typed{animation:typing 4.2s steps(43,end) .6s both}.cursor{animation:cursor 1.4s steps(1,end) 4.8s infinite}@keyframes typing{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}@keyframes cursor{50%{opacity:0}}'
    return wrap('Srivaths — developer terminal', 'AI and systems builder: agents, retrieval, robotics. Python, TypeScript, SQL. Build, test, learn, repeat.', body, width=680, height=560, accent='#67e8f9', static=static, extra_css=css)


def symbol(kind: str) -> str:
    # Original tiny diagrams keep all artwork offline and dependency-free.
    if kind == 'Python':
        return '<path d="M-19-3v-17q0-9 10-9H8q10 0 10 9v12H-4v11h-15Z" fill="#60a5fa"/><path d="M19 3v17q0 9-10 9H-8q-10 0-10-9V8H4V-3h15Z" fill="#fbbf24"/><circle cx="-8" cy="-21" r="2.4" fill="#080d1a"/><circle cx="8" cy="21" r="2.4" fill="#080d1a"/>'
    if kind == 'TypeScript':
        return '<rect x="-27" y="-27" width="54" height="54" rx="8" fill="#3178c6"/><text x="0" y="11" text-anchor="middle" font-size="27" font-weight="700">TS</text>'
    if kind == 'PyTorch':
        return '<path d="M0-27-17-10a24 24 0 1 0 34 0" fill="none" stroke="#fb795e" stroke-width="6"/><circle cx="18" cy="-23" r="4" fill="#fb795e"/>'
    if kind == 'React':
        return '<g fill="none" stroke="#67e8f9" stroke-width="2.5"><ellipse rx="30" ry="11"/><ellipse rx="30" ry="11" transform="rotate(60)"/><ellipse rx="30" ry="11" transform="rotate(120)"/></g><circle r="5" fill="#67e8f9"/>'
    if kind == 'FastAPI':
        return '<circle r="29" fill="#0a7f72"/><path d="m5-22-21 27H-2l-4 18L18-5H3Z" fill="#a7f3d0"/>'
    if kind == 'PostgreSQL':
        return '<g fill="#173d5f" stroke="#93c5fd" stroke-width="2"><ellipse cy="-18" rx="27" ry="10"/><path d="M-27-18v37c0 13 54 13 54 0v-37"/><ellipse cy="-18" rx="27" ry="10"/><path d="M-27 0c0 13 54 13 54 0M-27 17c0 13 54 13 54 0" fill="none"/></g>'
    if kind == 'Docker':
        return '<g fill="#60a5fa"><rect x="-27" y="-7" width="12" height="11"/><rect x="-12" y="-7" width="12" height="11"/><rect x="3" y="-7" width="12" height="11"/><rect x="-12" y="-21" width="12" height="11"/><rect x="3" y="-21" width="12" height="11"/><path d="M-32 8h53q8 0 13-7 3 14-13 17-8 14-24 13-25 0-29-23Z"/></g>'
    if kind == 'Kubernetes':
        return '<path d="m0-30 25 14v29L0 29-25 13v-29Z" fill="#326ce5"/><g fill="none" stroke="#eff6ff" stroke-width="3"><circle r="13"/><path d="M0-22v44M-19-11l38 22M-19 11l38-22"/></g>'
    if kind == 'SQL':
        return '<rect x="-29" y="-25" width="58" height="50" rx="10" fill="#174638" stroke="#6ee7b7"/><text x="0" y="9" text-anchor="middle" class="mono" font-size="23" font-weight="700">SQL</text>'
    return '<g fill="none" stroke="#c4b5fd" stroke-width="3"><circle cx="-22" cy="-14" r="7"/><circle cx="21" cy="-14" r="7"/><circle cy="23" r="7"/><path d="M-15-14h29M-18-8-4 17M18-8 4 17"/></g>'


def stack() -> str:
    labels = ['Python','TypeScript','SQL','PyTorch','LangGraph','FastAPI','React','PostgreSQL','Docker','Kubernetes']
    body = ''.join(f'<g transform="translate({60+i*120} 54)">{symbol(label)}<text x="0" y="62" text-anchor="middle" font-size="16" font-weight="600">{label}</text></g>' for i, label in enumerate(labels))
    return wrap('Tools Srivaths works with', 'Python, TypeScript, SQL, PyTorch, LangGraph, FastAPI, React, PostgreSQL, Docker, Kubernetes. Original simplified technology symbols.', body, width=1200, height=150, accent='#a78bfa', static=True)


def stack_mobile() -> str:
    labels = ['Python','TypeScript','SQL','PyTorch','LangGraph','FastAPI','React','PostgreSQL','Docker','Kubernetes']
    body = ''.join(f'<g transform="translate({64+(i%5)*128} {74+(i//5)*172})">{symbol(label)}<text x="0" y="65" text-anchor="middle" font-size="22" font-weight="600">{label}</text></g>' for i, label in enumerate(labels))
    return wrap('Tools Srivaths works with', 'Python, TypeScript, SQL, PyTorch, LangGraph, FastAPI, React, PostgreSQL, Docker, Kubernetes. Original simplified technology symbols.', body, width=640, height=360, accent='#a78bfa', static=True)


def validate(svg: str, *, static: bool) -> None:
    root = ET.fromstring(svg)
    assert root.tag == '{http://www.w3.org/2000/svg}svg'
    assert 'prefers-reduced-motion:reduce' in svg
    assert 'Srivatsan' not in svg
    for node in root.iter():
        assert node.tag.rsplit('}',1)[-1] not in {'script','foreignObject','image','animate','animateTransform'}
        assert not any(key.rsplit('}',1)[-1] == 'href' for key in node.attrib)
    if static:
        assert svg.rsplit('</style>',1)[0].rstrip().endswith('.typed{clip-path:none!important}')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    assets: dict[str, tuple[str, bool]] = {'stack.svg': (stack(), True), 'stack-mobile.svg': (stack_mobile(), True)}
    for static in (False, True):
        suffix = '-static' if static else ''
        for key in PROJECTS:
            assets[f'project-{key}{suffix}.svg'] = (project(key, static), static)
            assets[f'project-{key}-mobile{suffix}.svg'] = (project_mobile(key, static), static)
        assets[f'terminal{suffix}.svg'] = (terminal(static), static)
        assets[f'terminal-mobile{suffix}.svg'] = (terminal_mobile(static), static)
    stale = []
    for name, (svg, static) in assets.items():
        validate(svg, static=static)
        path = ROOT / 'assets' / name
        if args.check:
            if not path.exists() or path.read_bytes() != svg.encode('utf-8'):
                stale.append(name)
        else:
            path.parent.mkdir(exist_ok=True)
            path.write_bytes(svg.encode('utf-8'))
    if stale:
        print('Regenerate outdated studio assets: ' + ', '.join(stale), file=sys.stderr)
        return 1
    print(f'{"Checked" if args.check else "Generated"} {len(assets)} studio SVGs; XML and static-motion checks passed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
