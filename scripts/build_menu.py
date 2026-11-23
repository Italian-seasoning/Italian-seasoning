#!/usr/bin/env python3
"""Regenerate the menu-line images in assets/menu from scripts/menu.json.

Edit menu.json (descriptions, versions), then run:  python3 scripts/build_menu.py
"""
import base64, json, pathlib
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
SERIF = "'Iowan Old Style', 'Palatino', 'Book Antiqua', Georgia, serif"
GRAIN = ('<filter id="g"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch"/>'
         '<feColorMatrix values="0 0 0 0 .2  0 0 0 0 .12  0 0 0 0 .05  0 0 0 .08 0"/></filter>')
W, H = 1200, 120

def slip(i, app):
    icon = base64.b64encode((ROOT / "assets/icons" / f"{app['icon']}.png").read_bytes()).decode()
    name, desc = escape(app["name"]), escape(app["desc"])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{name}, version {app['version']}: {desc}">
<defs>{GRAIN}</defs>
<rect width="{W}" height="{H}" rx="6" fill="#fbf5e8"/><rect width="{W}" height="{H}" rx="6" filter="url(#g)"/>
<rect x="8" y="8" width="{W-16}" height="{H-16}" rx="3" fill="none" stroke="#7a1f17" stroke-width="1"/>
<text x="44" y="70" font-family="{SERIF}" font-size="22" fill="#7a1f17" opacity=".7">{i:02d}</text>
<image href="data:image/png;base64,{icon}" x="96" y="22" width="76" height="76"/>
<line x1="196" y1="56" x2="1040" y2="56" stroke="#7a1f17" stroke-width="2" stroke-dasharray="1 9" stroke-linecap="round"/>
<text x="196" y="58" font-family="{SERIF}" font-size="30" fill="#2b1a10" stroke="#fbf5e8" stroke-width="40" stroke-linejoin="round" paint-order="stroke">{name}</text>
<text x="196" y="90" font-family="{SERIF}" font-style="italic" font-size="19" fill="#6b5640">{desc}</text>
<text x="1156" y="62" text-anchor="end" font-family="{SERIF}" font-size="26" fill="#7a1f17">v{escape(app['version'])}</text>
</svg>
'''

apps = json.loads((ROOT / "scripts/menu.json").read_text())
for i, app in enumerate(apps, 1):
    (ROOT / "assets/menu" / f"{app['icon']}.svg").write_text(slip(i, app))
print(f"Wrote {len(apps)} menu lines to assets/menu/")
