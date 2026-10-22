#!/usr/bin/env python3
"""Generate deterministic, dependency-free SVG artwork for the profile README."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PALETTES = {
    "dark": {
        "bg": "#080f18",
        "surface": "#0c1821",
        "fg": "#edf5f5",
        "muted": "#9caeb8",
        "soft": "#6d8592",
        "line": "#203641",
        "grid": "#7796a5",
        "accent": "#5eead4",
    },
    "light": {
        "bg": "#f6faf9",
        "surface": "#ffffff",
        "fg": "#112b34",
        "muted": "#49636c",
        "soft": "#617d85",
        "line": "#c8dddb",
        "grid": "#668c8b",
        "accent": "#0f766e",
    },
}


def styles(p: dict[str, str], *, static: bool = False) -> str:
    reset = """
    .enter, .flow, .flow-slow, .rotor, .rotor-reverse, .pulse, .signal {
      animation: none !important;
    }
    .enter { opacity: 1 !important; }
    .rotor, .rotor-reverse { transform: none !important; }
    .pulse { opacity: .5 !important; }
    """
    return f"""<style>
    text {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; }}
    .mono {{ font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', monospace; }}
    .ink {{ fill: {p['fg']}; }}
    .muted {{ fill: {p['muted']}; }}
    .soft {{ fill: {p['soft']}; }}
    .accent {{ fill: {p['accent']}; }}
    .enter {{ animation: reveal 1.3s ease-out both; }}
    .flow {{ animation: flow 4.5s ease-out 1 forwards; }}
    .flow-slow {{ animation: flow 4.5s ease-out reverse 1 forwards; }}
    .rotor {{ transform-origin: 0px 0px; animation: orbit 4.5s ease-out 1 forwards; }}
    .rotor-reverse {{ transform-origin: 0px 0px; animation: orbit 4.5s ease-out reverse 1 forwards; }}
    .pulse {{ animation: pulse 4s ease-in-out 1 forwards; }}
    .pulse-two {{ animation-delay: -1.3s; }}
    .pulse-three {{ animation-delay: -2.6s; }}
    .signal {{ animation: signal 4.5s linear 1 forwards; }}
    @keyframes reveal {{ from {{ opacity: .85; }} to {{ opacity: 1; }} }}
    @keyframes flow {{ to {{ stroke-dashoffset: -400; }} }}
    @keyframes orbit {{ to {{ transform: rotate(80deg); }} }}
    @keyframes pulse {{ 0%, 100% {{ opacity: .25; }} 45% {{ opacity: .9; }} }}
    @keyframes signal {{ to {{ stroke-dashoffset: -1000; }} }}
    @media (prefers-reduced-motion: reduce) {{{reset}}}
    {reset if static else ''}
  </style>"""


def defs(p: dict[str, str]) -> str:
    return f"""<defs>
    <pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse">
      <path d="M 36 0 L 0 0 0 36" fill="none" stroke="{p['grid']}" stroke-width=".65" opacity=".11"/>
    </pattern>
    <radialGradient id="glow">
      <stop offset="0" stop-color="{p['accent']}" stop-opacity=".1"/>
      <stop offset="1" stop-color="{p['accent']}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="edge" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0" stop-color="{p['accent']}" stop-opacity=".65"/>
      <stop offset="1" stop-color="{p['accent']}" stop-opacity=".03"/>
    </linearGradient>
  </defs>"""


def background(p: dict[str, str], width: int, height: int) -> str:
    return f"""<rect width="{width}" height="{height}" rx="20" fill="{p['bg']}"/>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="19" fill="url(#grid)"/>
  <ellipse cx="{width * .76:g}" cy="{height * .47:g}" rx="{width * .35:g}" ry="{height * .64:g}" fill="url(#glow)"/>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="19" fill="none" stroke="{p['line']}" stroke-width="1"/>"""


def diagram(p: dict[str, str], *, mobile: bool) -> str:
    # An outer positioning group keeps animation transforms independent of layout.
    x, y = (320, 418) if mobile else (928, 213)
    scale = ".88" if mobile else "1"
    label_size = 21 if mobile else 15
    core_size = 44 if mobile else 33
    return f"""<g transform="translate({x} {y}) scale({scale})" class="enter">
    <circle r="184" fill="none" stroke="{p['line']}" stroke-width="1" stroke-dasharray="2 10"/>
    <circle r="148" fill="none" stroke="{p['line']}" stroke-width="1"/>
    <path d="M-199 0H199 M0-192V192" stroke="{p['line']}" stroke-width="1" opacity=".55"/>
    <g transform="rotate(-28)">
      <ellipse rx="207" ry="94" fill="none" stroke="{p['accent']}" stroke-width="1" opacity=".36"/>
      <ellipse class="flow" rx="207" ry="94" fill="none" stroke="{p['accent']}" stroke-width="1.8" stroke-dasharray="38 362" opacity=".8"/>
    </g>
    <g transform="rotate(40)">
      <ellipse rx="181" ry="79" fill="none" stroke="{p['accent']}" stroke-width="1" opacity=".2"/>
      <ellipse class="flow-slow" rx="181" ry="79" fill="none" stroke="{p['accent']}" stroke-width="1.5" stroke-dasharray="16 384" opacity=".6"/>
    </g>
    <path d="M0 0L101-118 M0 0L-138 65 M0 0L91 127" fill="none" stroke="{p['accent']}" stroke-width="1" opacity=".23"/>
    <path class="signal" d="M0 0L101-118 M0 0L-138 65 M0 0L91 127" fill="none" stroke="{p['accent']}" stroke-width="2" stroke-dasharray="5 195" opacity=".6"/>
    <g class="rotor">
      <circle cy="-148" r="4" fill="{p['accent']}"/>
      <circle cy="-148" r="9" fill="none" stroke="{p['accent']}" opacity=".18"/>
    </g>
    <g class="rotor-reverse">
      <circle cx="184" r="3" fill="{p['accent']}" opacity=".75"/>
    </g>
    <circle r="59" fill="{p['bg']}" stroke="{p['line']}" stroke-width="1.4"/>
    <circle r="48" fill="{p['surface']}" stroke="{p['accent']}" stroke-width="1" stroke-opacity=".28"/>
    <text x="0" y="{16 if mobile else 12}" text-anchor="middle" class="mono accent" font-size="{core_size}" font-weight="500" letter-spacing="-3">&lt;/&gt;</text>
    <g transform="translate(101 -118)">
      <circle class="pulse" r="16" fill="none" stroke="{p['accent']}" stroke-width="1"/>
      <circle r="5" fill="{p['accent']}"/>
      <rect x="-60" y="-54" width="120" height="32" rx="5" fill="{p['bg']}"/>
      <text y="-30" text-anchor="middle" class="mono muted" font-size="{label_size}" letter-spacing="1.2">AGENTS</text>
    </g>
    <g transform="translate(-138 65)">
      <circle class="pulse pulse-two" r="15" fill="none" stroke="{p['accent']}" stroke-width="1"/>
      <circle r="5" fill="{p['accent']}"/>
      <rect x="-63" y="21" width="82" height="32" rx="5" fill="{p['bg']}"/>
      <text x="-22" y="44" text-anchor="middle" class="mono muted" font-size="{label_size}" letter-spacing="1.2">DATA</text>
    </g>
    <g transform="translate(91 127)">
      <circle class="pulse pulse-three" r="15" fill="none" stroke="{p['accent']}" stroke-width="1"/>
      <circle r="5" fill="{p['accent']}"/>
      <rect x="13" y="5" width="132" height="32" rx="5" fill="{p['bg']}"/>
      <text x="78" y="28" text-anchor="middle" class="mono muted" font-size="{label_size}" letter-spacing="1.2">SYSTEMS</text>
    </g>
  </g>"""


def hero(theme: str, *, mobile: bool, static: bool = False) -> str:
    p = PALETTES[theme]
    width, height = (640, 600) if mobile else (1200, 430)
    if mobile:
        content = """<g class="enter">
    <text x="40" y="58" class="mono accent" font-size="15" letter-spacing="2">APPLIED AI / DATA / SYSTEMS</text>
    <text x="36" y="134" class="ink" font-size="70" font-weight="650" letter-spacing="-3.5">Srivatsan<tspan class="accent">.</tspan></text>
    <text x="41" y="174" class="mono muted" font-size="21">@sriv144</text>
    <text x="40" y="222" class="ink" font-size="25" letter-spacing="-.4">From models to useful systems.</text>
    <path d="M40 251H600" stroke="url(#edge)"/>
  </g>"""
    else:
        content = """<g class="enter">
    <text x="64" y="78" class="mono accent" font-size="15" letter-spacing="2.1">APPLIED AI / DATA / SYSTEMS</text>
    <text x="59" y="181" class="ink" font-size="86" font-weight="650" letter-spacing="-4.8">Srivatsan<tspan class="accent">.</tspan></text>
    <text x="65" y="225" class="mono muted" font-size="21">@sriv144</text>
    <text x="64" y="283" class="ink" font-size="27" letter-spacing="-.5">From models to useful systems.</text>
    <path d="M64 320H636" stroke="url(#edge)"/>
    <circle cx="69" cy="357" r="3.5" class="accent"/>
    <text x="85" y="362" class="mono soft" font-size="13" letter-spacing="1.8">THINK. BUILD. ITERATE.</text>
  </g>"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="{p['fg']}" role="img" aria-labelledby="title desc">
  <title id="title">Srivatsan — Applied AI, Data, Systems</title>
  <desc id="desc">@sriv144. From models to useful systems. An orbital diagram connects agents, data, and systems around a code core.</desc>
  {defs(p)}
  {styles(p, static=static)}
  {background(p, width, height)}
  {content}
  {diagram(p, mobile=mobile)}
</svg>
"""


def validate(svg: str) -> None:
    element = ET.fromstring(svg)
    assert element.tag == "{http://www.w3.org/2000/svg}svg"
    assert "prefers-reduced-motion: reduce" in svg
    for node in element.iter():
        assert node.tag.rsplit("}", 1)[-1] not in {"script", "foreignObject", "image"}
        assert not any(key.rsplit("}", 1)[-1] == "href" for key in node.attrib)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check tracked assets without writing files")
    args = parser.parse_args()
    assets = {}
    for theme in PALETTES:
        for static in (False, True):
            suffix = "-static" if static else ""
            assets[f"hero-{theme}{suffix}.svg"] = hero(theme, mobile=False, static=static)
            assets[f"hero-mobile-{theme}{suffix}.svg"] = hero(theme, mobile=True, static=static)
    failed = []
    if not args.check:
        (ROOT / "assets").mkdir(parents=True, exist_ok=True)
    for name, svg in assets.items():
        validate(svg)
        destination = ROOT / "assets" / name
        if args.check:
            if not destination.exists() or destination.read_bytes() != svg.encode("utf-8"):
                failed.append(name)
        else:
            destination.write_bytes(svg.encode("utf-8"))
    if failed:
        print("Regenerate outdated assets: " + ", ".join(failed), file=sys.stderr)
        return 1
    print(f"{'Checked' if args.check else 'Generated'} {len(assets)} SVG assets; XML validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
