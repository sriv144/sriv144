"""Render the profile's quiet, grouped workbench in dark/light and mobile layouts."""
from __future__ import annotations

import argparse
from html import escape
import importlib.util
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('studio_symbols', ROOT/'scripts/generate-studio.py')
studio = importlib.util.module_from_spec(spec)
spec.loader.exec_module(studio)

GROUPS = [
    ('Languages', ('Python', 'TypeScript', 'SQL')),
    ('AI & retrieval', ('PyTorch', 'LangGraph', 'RAG')),
    ('Web & APIs', ('FastAPI', 'React', 'Three.js')),
    ('Data & infrastructure', ('PostgreSQL', 'Docker', 'Kubernetes')),
]


def icon(label: str) -> str:
    if label == 'RAG':
        return '<path d="M-23-26h29l12 12v14M6-26v13h12M-23-26v49h21M-14-8H3M-14 1H0M-14 10h8" fill="none" stroke="#b9c99e" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="9" r="11" fill="none" stroke="#e6cf9e" stroke-width="3"/><path d="m20 17 10 10" stroke="#e6cf9e" stroke-width="4" stroke-linecap="round"/>'
    if label == 'Three.js':
        return '<path d="m-21-28 49 13L-8 29Z M-21-28-14 0 3-21M-14 0 15 7-2-8-8 29M-2-8 28-15M15 7 3-21" fill="none" stroke="#e6dfc9" stroke-width="2.2" stroke-linejoin="round"/>'
    return studio.symbol(label)


def render(theme: str, mobile: bool) -> str:
    dark = theme == 'dark'
    p = dict(bg='#111f2b', edge='#35494f', fg='#f6edd9', muted='#a5b9b8', accent='#e6c894', texture='#b7c9c1') if dark else dict(bg='#faf6ed', edge='#d8d5c6', fg='#263d42', muted='#607575', accent='#84613c', texture='#698c83')
    w, h = (680, 850) if mobile else (1280, 480)
    title_size, label_size = (28, 28) if mobile else (23, 24)
    description = '; '.join(f'{group}: {", ".join(tools)}' for group, tools in GROUPS)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
           '<title id="title">Srivaths’ toolbox — from idea to working software</title>',
           f'<desc id="desc">{escape(description)}. Original simplified technology symbols. Tools are grouped by use, with no proficiency ratings.</desc>',
           f'<defs><pattern id="grain" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".65" fill="{p["texture"]}" opacity=".13"/></pattern></defs>',
           '<style>text{font-family:"Segoe UI",Arial,sans-serif}.mono{font-family:Consolas,monospace}</style>',
           f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="24" fill="{p["bg"]}" stroke="{p["edge"]}"/>',
           f'<rect x="2" y="2" width="{w-4}" height="{h-4}" rx="23" fill="url(#grain)"/>',
           f'<text x="36" y="{49 if mobile else 53}" fill="{p["fg"]}" font-size="{32 if mobile else 32}" font-family="Georgia,serif" font-weight="600">The workbench</text>',
           f'<text x="36" y="{87 if mobile else 89}" fill="{p["muted"]}" font-size="{22 if mobile else 21}">Avengers, assemble. Utility functions included.</text>',
           f'<path d="M36 113H{w-36}" stroke="{p["edge"]}"/>']
    # A small botanical flourish echoes the studio plants without competing with the icons.
    leaf_x, leaf_y = w-62, 56
    out.append(f'<g transform="translate({leaf_x} {leaf_y})" fill="none" stroke="{p["accent"]}" stroke-width="1.6" opacity=".75"><path d="M-8 23Q10 5 11-24M3 5Q-24-1-17-20Q2-20 3 5M9-7Q30-12 27-27Q10-27 9-7"/></g>')
    for i, (group, tools) in enumerate(GROUPS):
        x = 36 + (i % 2)*320 if mobile else 36+i*312
        y = 157+(i//2)*319 if mobile else 165
        out.append(f'<text class="mono" x="{x}" y="{y}" fill="{p["accent"]}" font-size="13" letter-spacing="2">0{i+1}</text>')
        if mobile and i == 3:
            heading = [('Data &', y+35), ('infrastructure', y+68)]
        elif not mobile and i == 3:
            heading = [('Data & infrastructure', y+39)]
        else:
            heading = [(group, y+35 if mobile else y+39)]
        for text, ty in heading:
            out.append(f'<text x="{x}" y="{ty}" fill="{p["fg"]}" font-size="{title_size if not (i==3 and not mobile) else 22}" font-weight="600">{escape(text)}</text>')
        first_row_y = y+117 if mobile else y+100
        for j, label in enumerate(tools):
            cy = first_row_y+j*(65 if mobile else 69)
            out.append(f'<g transform="translate({x+25} {cy})"><rect x="-27" y="-27" width="54" height="54" rx="17" fill="{"#1b303b" if dark else "#203641"}"/><g transform="scale(.59)" fill="#f4edda">{icon(label)}</g></g>')
            out.append(f'<text x="{x+67}" y="{cy+9}" fill="{p["fg"]}" font-size="{label_size}">{escape(label)}</text>')
    if mobile:
        out.append(f'<path d="M340 145V752M36 441H644" stroke="{p["edge"]}"/>')
    else:
        for x in (330,642,954):
            out.append(f'<path d="M{x} 151V417" stroke="{p["edge"]}" stroke-dasharray="2 7"/>')
    out += [f'<path d="M36 {h-47}H{w-36}" stroke="{p["edge"]}"/>',
            f'<text x="36" y="{h-20}" fill="{p["muted"]}" font-size="{18 if mobile else 15}" letter-spacing="1">BUILD · TEST · LEARN · REPEAT</text>', '</svg>\n']
    return '\n'.join(out)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    for theme in ('dark','light'):
        for mobile in (False,True):
            text=render(theme,mobile)
            xml=ET.fromstring(text)
            for node in xml.iter():
                assert node.tag.rsplit('}',1)[-1] not in {'script','foreignObject','image','animate'}
                assert not any(key.rsplit('}',1)[-1]=='href' for key in node.attrib)
            path=ROOT/'assets'/f'toolbox-{"mobile-" if mobile else ""}{theme}.svg'
            if args.check:
                assert path.read_text(encoding='utf8')==text, f'Outdated asset: {path}'
            else:
                path.write_text(text,encoding='utf8')
    print('PASS: four themed toolbox assets, XML, self-contained resources, deterministic output')


if __name__=='__main__':main()
