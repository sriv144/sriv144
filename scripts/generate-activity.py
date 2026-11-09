"""Render a contribution city from the real, locally generated snk calendar."""
from __future__ import annotations

import argparse
import re
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NS = {"s": "http://www.w3.org/2000/svg"}


def read_calendar() -> list[tuple[int, int, int]]:
    source = ET.parse(ROOT / "assets/contributions-light-static.svg").getroot()
    styles = "".join(source.find("s:style", NS).itertext())
    # snk retains the original fills in .c.cN rules after animation is removed.
    levels = dict(re.findall(
        r"\.c\.([\w-]+)\s*\{[^{}]*?fill\s*:\s*var\(--c([0-4])\)", styles))
    rects = [node for node in source.findall(".//s:rect", NS)
             if "c" in node.get("class", "").split()]
    if not 350 <= len(rects) <= 380:
        raise ValueError(f"Unexpected calendar size: {len(rects)} days")
    xs = sorted({float(node.attrib["x"]) for node in rects})
    ys = sorted({float(node.attrib["y"]) for node in rects})
    if not 50 <= len(xs) <= 54 or len(ys) != 7:
        raise ValueError("Expected a year of weekly columns and seven weekdays")
    cells = []
    for node in rects:
        classes = node.get("class", "").split()
        specific = [name for name in classes if name != "c"]
        if specific and specific[0] not in levels:
            raise ValueError(f"Cannot resolve contribution fill: {classes}")
        level = int(levels[specific[0]]) if specific else 0
        cells.append((xs.index(float(node.attrib["x"])),
                      ys.index(float(node.attrib["y"])), level))
    if len({(week, day) for week, day, _ in cells}) != len(cells):
        raise ValueError("Duplicate calendar cells")
    return cells


def points(*vertices: tuple[float, float]) -> str:
    return " ".join(f"{x:.2f},{y:.2f}" for x, y in vertices)


def render(cells: list[tuple[int, int, int]], theme: str, animated: bool) -> str:
    dark = theme == "dark"
    bg, bg2 = ("#060b1b", "#101531") if dark else ("#fafaff", "#eaf2ff")
    fg, muted, border = ("#e9efff", "#899bbd", "#28314f") if dark else ("#172344", "#52658a", "#c8d3eb")
    cyan, violet = ("#5de4ff", "#ab8cff") if dark else ("#007caa", "#6750c8")
    tops = ["#121d34", "#254775", "#345ba0", "#6256bb", "#9470eb"] if dark else ["#e5eaf7", "#a5d5ed", "#72b7dd", "#a59ce9", "#8170d9"]
    fronts = ["#10182b", "#153355", "#234475", "#403c83", "#6350a4"] if dark else ["#d6deee", "#7fb4d1", "#5293bc", "#8178c6", "#6254ad"]
    sides = ["#10172a", "#1b294d", "#2a3465", "#36316e", "#4c3a89"] if dark else ["#cbd5e8", "#7199bf", "#4674a5", "#6b60aa", "#50438e"]
    heights = [0, 15, 32, 54, 82]
    week_count = max(week for week, _, _ in cells) + 1
    spacing = 873.6 / max(week_count - 1, 1)
    styles = f"""text{{font-family:'Segoe UI',Arial,sans-serif}}.mono{{font-family:Consolas,'Courier New',monospace}}.roof{{stroke-linejoin:round}}"""
    if animated:
        styles += """.scan{stroke-dasharray:100 1000;animation:sweep 12s linear infinite}.city-light{animation:glow 7s ease-in-out infinite}@keyframes sweep{from{stroke-dashoffset:1100}to{stroke-dashoffset:-1100}}@keyframes glow{0%,100%{opacity:.65}50%{opacity:1}}@media(prefers-reduced-motion:reduce){*{animation:none!important}.motion{display:none}}"""
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="380" viewBox="0 0 1200 380" role="img" aria-labelledby="activity-title activity-desc">',
           '<title id="activity-title">Srivaths — a year in public code</title>',
           '<desc id="activity-desc">An isometric city built from the actual GitHub contribution calendar for sriv144. Each tile is one recorded calendar day. Building height represents contribution intensity from zero to four, not a commit count.</desc>',
           f'<defs><linearGradient id="canvas" x2="1" y2="1"><stop stop-color="{bg}"/><stop offset="1" stop-color="{bg2}"/></linearGradient><linearGradient id="signal"><stop stop-color="{violet}"/><stop offset="1" stop-color="{cyan}"/></linearGradient><clipPath id="city-clip"><rect x="70" y="88" width="1060" height="252"/></clipPath></defs>',
           f'<style>{styles}</style>',
           f'<rect x="1" y="1" width="1198" height="378" rx="20" fill="url(#canvas)" stroke="{border}"/>',
           f'<text class="mono" x="46" y="31" fill="{cyan}" font-size="11" letter-spacing="2.5">BUILD LOG</text>',
           f'<text x="44" y="65" fill="{fg}" font-size="27" font-weight="700" letter-spacing="1.5">A YEAR IN PUBLIC CODE</text>',
           f'<text class="mono" x="1153" y="32" fill="{violet}" font-size="11" text-anchor="end" letter-spacing="1.2">SRIVATHS / SRIV144</text>',
           f'<text class="mono" x="1153" y="55" fill="{muted}" font-size="10" text-anchor="end">ONE TILE / ONE CALENDAR DAY</text>',
           f'<path d="M46 82H1154" stroke="{border}"/>',
           '<g clip-path="url(#city-clip)">']
    for week, day, level in sorted(cells, key=lambda c: (c[0] * 1.75 + c[1] * 7, c[0])):
        x, y = 208 + week * spacing - day * 12, 190 + week * 1.75 + day * 7
        h = heights[level]
        a, b, c, d = (x, y - h), (x + 14.5, y + 1.55 - h), (x + 4.3, y + 7.5 - h), (x - 10.2, y + 5.95 - h)
        stroke = (cyan if level <= 2 else violet) if level else border
        out.append(f'<g data-week="{week}" data-day="{day}" data-level="{level}"><title>Contribution intensity {level} of 4</title>')
        if level:
            out.append(f'<polygon points="{points(b, c, (c[0], c[1]+h), (b[0], b[1]+h))}" fill="{sides[level]}" stroke="{stroke}" stroke-opacity=".36" stroke-width=".6"/>')
            out.append(f'<polygon points="{points(d, c, (c[0], c[1]+h), (d[0], d[1]+h))}" fill="{fronts[level]}" stroke="{stroke}" stroke-opacity=".48" stroke-width=".6"/>')
            if h > 30:
                for window in range(12, h - 7, 13):
                    out.append(f'<path class="city-light" d="M{x-5:.2f} {y-window+4:.2f}l9 1.4" fill="none" stroke="{cyan}" stroke-opacity=".45" stroke-width="1"/>')
        out.append(f'<polygon class="roof" points="{points(a,b,c,d)}" fill="{tops[level]}" stroke="{stroke}" stroke-opacity="{.8 if level else .55}" stroke-width=".75"/></g>')
    if animated:
        out.append(f'<path class="scan motion" d="M124 225L1108 325" fill="none" stroke="url(#signal)" stroke-width="2" opacity=".8"/>')
    out.extend(['</g>',
                f'<path d="M46 344H1154" stroke="{border}"/>',
                f'<text class="mono" x="46" y="365" fill="{muted}" font-size="11">Height = contribution intensity</text>',
                f'<text class="mono" x="1153" y="365" fill="{muted}" font-size="10" text-anchor="end">PUBLIC GITHUB CALENDAR / SRIV144</text>'])
    for level, color in enumerate(tops):
        out.append(f'<rect x="{347+level*20}" y="354" width="12" height="12" rx="2" fill="{color}" stroke="{border}"/>')
    out.append('</svg>\n')
    return "\n".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate XML and check committed output equality")
    args = parser.parse_args()
    cells = read_calendar()
    for theme in ("dark", "light"):
        for animated in (True, False):
            path = ROOT / f"assets/activity-{theme}{'' if animated else '-static'}.svg"
            content = render(cells, theme, animated)
            document = ET.fromstring(content)
            rendered = document.findall(".//s:g[@data-level]", NS)
            actual = [(int(node.attrib["data-week"]), int(node.attrib["data-day"]),
                       int(node.attrib["data-level"])) for node in rendered]
            if sorted(actual) != sorted(cells):
                raise ValueError("Rendered calendar positions or intensities changed")
            if not animated and any(token in content for token in ("@keyframes", "animation:", "<animate")):
                raise ValueError("Static output contains animation")
            if args.check:
                if not path.exists() or path.read_bytes() != content.encode("utf-8"):
                    raise SystemExit(f"Outdated activity asset: {path.name}")
            else:
                path.write_text(content, encoding="utf-8", newline="\n")
    print(f"Activity assets {'verified' if args.check else 'generated'}: {len(cells)} real calendar days, {week_count(cells)} weeks.")


def week_count(cells: list[tuple[int, int, int]]) -> int:
    return max(week for week, _, _ in cells) + 1


if __name__ == "__main__":
    main()
