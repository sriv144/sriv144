"""Generate repository-owned cozy header and space contribution animation."""
import argparse
import base64
from pathlib import Path
import xml.etree.ElementTree as ET
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('calendar_art', ROOT/'scripts/generate-activity.py')
calendar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calendar)


def scene(static=False):
    image = base64.b64encode((ROOT/'assets/cozy-workspace.png').read_bytes()).decode()
    style = '''.firefly{animation:float 7s ease-in-out infinite}.star{animation:twinkle 4s ease-in-out infinite}.steam{animation:steam 5s ease-in-out infinite}@keyframes float{0%,100%{transform:translate(0,0);opacity:.25}50%{transform:translate(13px,-24px);opacity:.9}}@keyframes twinkle{0%,100%{opacity:.15}50%{opacity:.9}}@keyframes steam{0%{transform:translateY(12px);opacity:0}40%{opacity:.55}100%{transform:translateY(-22px);opacity:0}}'''
    if static: style=''
    style += '@media(prefers-reduced-motion:reduce){*{animation:none!important}.steam{opacity:.25}}'
    stars=''.join(f'<circle class="star" cx="{x}" cy="{y}" r="{r}" fill="#fff1b7" style="animation-delay:-{i*.7}s"/>' for i,(x,y,r) in enumerate([(180,200,3),(300,250,2),(390,130,3),(500,220,2),(610,170,2)]))
    flies=''.join(f'<g class="firefly" style="animation-delay:-{i*.9}s"><circle cx="{x}" cy="{y}" r="10" fill="#ffd574" opacity=".09"/><circle cx="{x}" cy="{y}" r="2.5" fill="#ffdc83"/></g>' for i,(x,y) in enumerate([(145,660),(320,730),(460,640),(570,790),(620,520)]))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1536" height="1024" viewBox="0 0 1536 1024" role="img" aria-labelledby="title desc"><title id="title">Srivaths — suit up, the next build awaits</title><desc id="desc">An illustrated back-view developer coding in a cozy attic beside a robot, tea, and an open window under a starry sky. Gentle fireflies and steam animate the scene.</desc><defs><linearGradient id="shade" x2="0" y2="1"><stop offset=".45" stop-color="#101d2b" stop-opacity="0"/><stop offset="1" stop-color="#101d2b" stop-opacity=".85"/></linearGradient><clipPath id="frame"><rect width="1536" height="1024" rx="28"/></clipPath></defs><style>{style}</style><g clip-path="url(#frame)"><image width="1536" height="1024" href="data:image/png;base64,{image}"/><rect width="1536" height="1024" fill="url(#shade)"/>{stars}{flies}<path class="steam" d="M1345 652q-18-20 0-36t0-38" fill="none" stroke="#fff7dc" stroke-width="4" stroke-linecap="round" opacity=".35"/><text x="82" y="860" fill="#fff5da" font-family="Georgia,serif" font-size="116" font-weight="700">Srivaths.</text><text x="88" y="917" fill="#eee5cd" font-family="Segoe UI,Arial,sans-serif" font-size="34">Legen—await for it—dary.</text></g></svg>'''


def space_shots(cells, count=10):
    """Target only the lowest surviving tile in each selected calendar column."""
    columns={week:sorted([(day,level) for w,day,level in cells if w==week],reverse=True)
             for week in sorted({week for week,_,_ in cells})}
    targets=[]
    # First sweep visits real active tiles with a clear path from below.
    for week,rows in columns.items():
        if rows and rows[0][1]>0 and len(targets)<count:
            day,level=rows.pop(0)
            targets.append((week,day,level))
    while len(targets)<count:
        available=[(week,rows[0][0],rows[0][1]) for week,rows in columns.items() if rows]
        if not available:break
        active=[target for target in available if target[2]>0]
        if active:
            week,day,level=min(active,key=lambda target:(-target[1],-target[2],target[0]))
        else:
            # Future calendars may need an empty bottom tile cleared first.
            # Every painted tile is treated as a collision, including level zero.
            def clearance(target):
                rows=columns[target[0]]
                distance=next((i for i,(_,level) in enumerate(rows) if level>0),len(rows)+7)
                return distance,target[0]
            week,day,level=min(available,key=clearance)
        columns[week].pop(0)
        targets.append((week,day,level))
    shots=[]
    for index,(week,day,level) in enumerate(targets):
        fire=1.0+index*2.25
        impact_y=120+day*22+13
        hit=fire+(312-impact_y)/130
        shots.append(dict(index=index,week=week,day=day,level=level,
                          x=50+week*20.8+6.5,impact_y=impact_y,
                          fire=fire,hit=hit,burn=hit+.2))
    return shots


def space(static=False):
    cells=calendar.read_calendar()
    colors=['#15253e','#385b72','#508d9c','#75c3c4','#f4d58b']
    shots=space_shots(cells)
    targets={(shot['week'],shot['day']):shot for shot in shots}
    cycle=26
    initial_x=shots[0]['x'] if shots else 130
    percent=lambda time:f'{time/cycle*100:.6f}%'
    out=['''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="430" viewBox="0 0 1200 430" role="img" aria-labelledby="title desc" data-cycle-seconds="26" data-projectile-speed="130" data-muzzle-y="312"><title id="title">Commit Cosmos — Srivaths' contribution flight</title><desc id="desc">An autoplay space-shooter scene. Each star tile is a real public contribution-calendar day; its brightness shows contribution intensity, not a game score. The ship targets ten tiles from below. A tile flashes orange when struck, then stays burned until the 26-second scene resets.</desc><defs><radialGradient id="nebula"><stop stop-color="#273451"/><stop offset="1" stop-color="#0b1424"/></radialGradient></defs><rect width="1200" height="430" rx="22" fill="url(#nebula)"/><style>text{font-family:Consolas,monospace}.laser,.impact{opacity:0}''']
    if not static:
        out.append('''.ship{animation:patrol 26s linear infinite}.glint{animation:glint 6s ease-in-out infinite}.flame{animation:flame .6s ease-in-out infinite alternate}@keyframes glint{0%,100%{opacity:.4}50%{opacity:1}}@keyframes flame{to{transform:scaleY(.65);opacity:.6}}@keyframes patrol{''')
        stops=[(0,initial_x)]
        for shot in shots:
            stops.extend([(shot['fire']-.32,shot['x']),(shot['hit']+.28,shot['x'])])
        stops.extend([(25.2,initial_x),(26,initial_x)])
        out.append(''.join(f'{percent(time)}{{transform:translateX({x-initial_x:.1f}px)}}' for time,x in stops)+'}')
        for shot in shots:
            i=shot['index']; fire=shot['fire']; hit=shot['hit']; burn=shot['burn']
            travel=312-shot['impact_y']; color=colors[shot['level']]
            out.append(f'''.shot-{i}{{animation:shot-{i} {cycle}s linear infinite}}.hit-{i},.hit-{i} .contribution-tile{{animation:burn-{i} {cycle}s linear infinite}}.impact-{i}{{animation:impact-{i} {cycle}s linear infinite;transform-box:fill-box;transform-origin:center}}
@keyframes shot-{i}{{0%,{percent(fire-.0003)}{{opacity:0;transform:translateY(0)}}{percent(fire)}{{opacity:1;transform:translateY(0)}}{percent(hit-.0003)}{{opacity:1;transform:translateY(-{travel}px)}}{percent(hit)},100%{{opacity:0;transform:translateY(-{travel}px)}}}}
@keyframes burn-{i}{{0%,{percent(hit-.0003)}{{opacity:1;fill:{color}}}{percent(hit)},{percent(hit+.12)}{{opacity:1;fill:#ff793f}}{percent(burn)},99.999999%{{opacity:0;fill:#ff793f}}100%{{opacity:1;fill:{color}}}}}
@keyframes impact-{i}{{0%,{percent(hit-.0003)}{{opacity:0;transform:scale(.3)}}{percent(hit)}{{opacity:1;transform:scale(.3)}}{percent(hit+.3)},100%{{opacity:0;transform:scale(1.6)}}}}''')
    out.append('@media(prefers-reduced-motion:reduce){*{animation:none!important}.laser,.impact{display:none}.calendar-tile,.contribution-tile{opacity:1!important}}</style>')
    out.append('<text x="44" y="46" fill="#f4d58b" font-size="15" letter-spacing="3">01 / COMMIT COSMOS</text><text x="44" y="80" fill="#edf2f5" font-size="25">I can do this all day. One commit at a time.</text>')
    for week,day,level in cells:
        x,y=50+week*20.8,120+day*22
        shot=targets.get((week,day))
        hit_class=f" hit-{shot['index']}" if shot else ''
        hit_data=(f' data-shot="{shot["index"]}" data-fire-time="{shot["fire"]:.6f}" data-hit-time="{shot["hit"]:.6f}" data-burn-time="{shot["burn"]:.6f}"' if shot else '')
        out.append(f'<g class="calendar-tile{hit_class}" data-week="{week}" data-day="{day}"{hit_data}><rect class="contribution-tile" data-level="{level}" x="{x:.1f}" y="{y}" width="13" height="13" rx="3" fill="{colors[level]}"/>')
        if level>2:out.append(f'<path class="glint" d="M{x+6.5:.1f} {y-4}v21m-10-10h20" stroke="{colors[level]}" opacity=".4" style="animation-delay:-{week%7}s"/>')
        out.append('</g>')
    for shot in shots:
        i=shot['index']; x=shot['x']; impact_y=shot['impact_y']
        out.append(f'<g class="projectile" data-shot="{i}" data-target-week="{shot["week"]}" data-target-day="{shot["day"]}" data-shot-x="{x:.1f}" data-impact-y="{impact_y}" data-fire-time="{shot["fire"]:.6f}" data-hit-time="{shot["hit"]:.6f}" data-burn-time="{shot["burn"]:.6f}"><rect class="laser shot-{i}" x="{x-1.5:.1f}" y="312" width="3" height="12" fill="#f4d58b"/><circle class="impact impact-{i}" cx="{x:.1f}" cy="{impact_y}" r="9" fill="none" stroke="#ff793f" stroke-width="2"/></g>')
    out.append(f'<g transform="translate({initial_x:.1f} 344)"><g class="ship"><path class="flame" d="M-8 18L0 32 8 18" fill="#eebf76"/><path d="M0-28L-24 22-9 15 0 21 9 15 24 22Z" fill="#b6e5df" stroke="#fff4ce" stroke-width="2"/><path d="M0-16L-6 7 6 7Z" fill="#2d5d70"/></g></g><path d="M44 381H1156" stroke="#304258"/><text x="44" y="409" font-size="12" fill="#9bafc1">REAL PUBLIC CONTRIBUTION DATA / AUTOPLAY SCENE</text><text x="1156" y="409" text-anchor="end" font-size="12" fill="#9bafc1">BRIGHTER TILE = MORE ACTIVITY</text></svg>')
    return ''.join(out)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--space-only',action='store_true',help='Refresh calendar art without rebuilding the header')
    args=parser.parse_args()
    for name,fn in [('cozy-header',scene),('space-contributions',space)]:
        if args.space_only and name=='cozy-header':continue
        for static in (False,True):
            svg=fn(static)
            ET.fromstring(svg)
            target=ROOT/'assets'/f'{name}{"-static" if static else ""}.svg'
            if args.check:
                assert target.read_text(encoding='utf-8')==svg, f'Stale {target}'
            else: target.write_text(svg,encoding='utf-8')
    print('PASS: four arcade/header assets, XML, and deterministic generation')


if __name__=='__main__':main()
