#!/usr/bin/env python3
"""Generates the SVG preview screens embedded in the README.

These are illustrative mockups drawn from the game's real palette and layout
(they are not captures of a live WebGL run). Regenerate with:

    python3 docs/make_screens.py
"""
import math, os, random

random.seed(7)
OUT = os.path.join(os.path.dirname(__file__), "screens")
os.makedirs(OUT, exist_ok=True)

# Palette lifted from index.html
PINK, ORANGE, BLUE, YELLOW = "#ff6ec7", "#ffb340", "#41d6ff", "#ffd23c"
GRASS1, GRASS2 = "#8ce05e", "#7ad04f"
HOLE, RIM = "#1b1033", "#120a26"
CONFETTI = [PINK, YELLOW, BLUE, "#7cff6e", "#ff9040", "#b98bff"]
FONT = "font-family='Segoe UI, Arial, sans-serif'"


def gradient(gid, stops, x2="1", y2="1"):
    s = "".join(f"<stop offset='{o}' stop-color='{c}'/>" for o, c in stops)
    return f"<linearGradient id='{gid}' x1='0' y1='0' x2='{x2}' y2='{y2}'>{s}</linearGradient>"


def confetti_rects(w, h, n, colors=CONFETTI):
    # rotated rectangles emitted as polygons (no transforms — renders everywhere)
    out = []
    for _ in range(n):
        cx, cy = random.uniform(0, w), random.uniform(0, h)
        rw, rh = random.uniform(6, 13), random.uniform(8, 16)
        a = math.radians(random.uniform(-60, 60))
        ca, sa = math.cos(a), math.sin(a)
        pts = []
        for dx, dy in [(-rw/2, -rh/2), (rw/2, -rh/2), (rw/2, rh/2), (-rw/2, rh/2)]:
            pts.append(f"{cx+dx*ca-dy*sa:.0f},{cy+dx*sa+dy*ca:.0f}")
        out.append(f"<polygon points='{' '.join(pts)}' fill='{random.choice(colors)}' opacity='.9'/>")
    return "".join(out)


def checker(x0, y0, w, h, cell, c1=GRASS1, c2=GRASS2):
    out = [f"<rect x='{x0}' y='{y0}' width='{w}' height='{h}' fill='{c1}'/>"]
    for r in range(math.ceil(h / cell)):
        for c in range(math.ceil(w / cell)):
            if (r + c) % 2:
                out.append(f"<rect x='{x0+c*cell}' y='{y0+r*cell}' width='{cell}' height='{cell}' fill='{c2}'/>")
    return "".join(out)


def hole(cx, cy, rx, ry):
    return (f"<ellipse cx='{cx}' cy='{cy}' rx='{rx+6}' ry='{ry+4}' fill='{RIM}'/>"
            f"<ellipse cx='{cx}' cy='{cy}' rx='{rx}' ry='{ry}' fill='{HOLE}'/>"
            f"<ellipse cx='{cx}' cy='{cy+ry*0.25}' rx='{rx*0.72}' ry='{ry*0.6}' fill='#0a0618'/>")


def donut(cx, cy, r):
    return (f"<circle cx='{cx}' cy='{cy}' r='{r}' fill='#c98a4b'/>"
            f"<circle cx='{cx}' cy='{cy-r*0.12}' r='{r*0.92}' fill='#f7a2d4'/>"
            f"<circle cx='{cx}' cy='{cy}' r='{r*0.34}' fill='{HOLE}'/>" +
            "".join(f"<rect x='{cx+math.cos(a)*r*0.62-4:.0f}' y='{cy+math.sin(a)*r*0.55-2:.0f}' width='9' height='4' rx='2' "
                    f"fill='{random.choice(['#ff4d6d','#4dd2ff','#fff34d','#7cff4d'])}'/>"
                    for a in [i * math.pi / 4 for i in range(8)]))


def cone(cx, cy, s):
    return (f"<rect x='{cx-s*0.55}' y='{cy-s*0.08}' width='{s*1.1}' height='{s*0.16}' rx='3' fill='#ff6a13'/>"
            f"<polygon points='{cx},{cy-s} {cx-s*0.42},{cy} {cx+s*0.42},{cy}' fill='#ff6a13'/>"
            f"<rect x='{cx-s*0.28}' y='{cy-s*0.55}' width='{s*0.56}' height='{s*0.18}' fill='#fff'/>")


def crate(cx, cy, s):
    return (f"<rect x='{cx-s/2}' y='{cy-s/2}' width='{s}' height='{s}' rx='3' fill='#d8a04a'/>"
            f"<rect x='{cx-s/2}' y='{cy-s*0.08}' width='{s}' height='{s*0.16}' fill='#b37f30'/>")


def tree(cx, cy, s):
    return (f"<rect x='{cx-s*0.08}' y='{cy-s*0.45}' width='{s*0.16}' height='{s*0.5}' fill='#8a5a2b'/>"
            f"<circle cx='{cx}' cy='{cy-s*0.72}' r='{s*0.42}' fill='#2fae4e'/>"
            f"<circle cx='{cx+s*0.25}' cy='{cy-s*0.55}' r='{s*0.28}' fill='#3bc75e'/>")


def car(cx, cy, s):
    return (f"<rect x='{cx-s}' y='{cy-s*0.34}' width='{s*2}' height='{s*0.5}' rx='6' fill='#ff4d6d'/>"
            f"<rect x='{cx-s*0.55}' y='{cy-s*0.66}' width='{s*1.05}' height='{s*0.42}' rx='6' fill='#ff4d6d'/>"
            f"<rect x='{cx-s*0.45}' y='{cy-s*0.58}' width='{s*0.85}' height='{s*0.28}' rx='4' fill='#bfe8ff'/>"
            f"<circle cx='{cx-s*0.55}' cy='{cy+s*0.2}' r='{s*0.2}' fill='#222'/>"
            f"<circle cx='{cx+s*0.55}' cy='{cy+s*0.2}' r='{s*0.2}' fill='#222'/>")


def chip(x, y, label, count, dot):
    w = 24 + len(label) * 10 + len(count) * 10 + 40
    return (f"<rect x='{x}' y='{y}' width='{w}' height='36' rx='14' fill='rgba(0,0,0,.4)'/>"
            f"<circle cx='{x+20}' cy='{y+18}' r='9' fill='{dot}'/>"
            f"<text x='{x+36}' y='{y+24}' {FONT} font-size='17' font-weight='800' fill='#fff'>{label}</text>"
            f"<text x='{x+w-14}' y='{y+24}' {FONT} font-size='17' font-weight='800' fill='#fff' text-anchor='end'>{count}</text>")


def title_block(cx, y, size, text="HOLEY MOLEY 3D"):
    return (f"<text x='{cx}' y='{y+5}' {FONT} font-size='{size}' font-weight='900' fill='#7a3f10' opacity='0.35' "
            f"text-anchor='middle'>{text}</text>"
            f"<text x='{cx}' y='{y}' {FONT} font-size='{size}' font-weight='900' fill='#ffffff' "
            f"text-anchor='middle'>{text}</text>")


def svg(name, w, h, body):
    doc = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}' width='{w}' height='{h}'>"
           f"{body}</svg>")
    with open(os.path.join(OUT, name), "w") as f:
        f.write(doc)
    print("wrote", name)


# ---------------------------------------------------------------- hero banner
W, H = 1280, 400
body = f"<defs>{gradient('bg', [(0, PINK), (0.45, ORANGE), (1, BLUE)])}</defs>"
body += f"<rect width='{W}' height='{H}' fill='url(#bg)' rx='14'/>"
body += confetti_rects(W, H * 0.55, 40)
body += hole(W / 2, H - 60, 260, 52)
body += donut(W / 2 - 150, H - 92, 40) + cone(W / 2 + 130, H - 96, 44) + car(W / 2 + 300, H - 110, 40)
body += tree(180, H - 100, 90) + crate(310, H - 90, 44)
body += title_block(W / 2, 150, 84)
body += (f"<text x='{W/2}' y='215' {FONT} font-size='24' font-weight='700' fill='#fff' "
         f"text-anchor='middle'>Eat everything. Grow huge. Beat the clock!</text>")
svg("hero.svg", W, H, body)

# ---------------------------------------------------------------- menu screen
W, H = 1200, 750
body = f"<defs>{gradient('bg2', [(0, PINK), (0.45, ORANGE), (1, BLUE)])}</defs>"
body += f"<rect width='{W}' height='{H}' fill='url(#bg2)' rx='14'/>"
body += title_block(W / 2, 170, 76)
body += (f"<text x='{W/2}' y='230' {FONT} font-size='22' font-weight='700' fill='#fff' "
         f"text-anchor='middle'>Eat everything. Grow huge. Beat the clock!</text>")
cards = [("Level 1", "Donut Park", donut(0, 0, 26)),
         ("Level 2", "Furniture Frenzy",
          "<rect x='-22' y='-26' width='44' height='10' rx='4' fill='#ff8f3c'/>"
          "<rect x='-22' y='-26' width='10' height='46' rx='4' fill='#ff8f3c'/>"
          "<rect x='-18' y='-16' width='8' height='38' fill='#b35b1a'/><rect x='10' y='-16' width='8' height='38' fill='#b35b1a'/>"),
         ("Level 3", "City Chaos",
          "<rect x='-24' y='-18' width='16' height='30' rx='4' fill='#9aa3ad'/>"
          "<circle cx='-16' cy='-14' r='9' fill='#9aa3ad'/><rect x='-19' y='-6' width='6' height='10' fill='#6b7480'/>")]
for i, (lvl, nm, icon) in enumerate(cards):
    x = W / 2 - 290 + i * 200
    locked = i == 2
    body += (f"<g opacity='{0.6 if locked else 1}'>"
             f"<rect x='{x}' y='300' width='180' height='150' rx='20' fill='#fff'/>"
             f"<rect x='{x}' y='442' width='180' height='8' rx='4' fill='rgba(0,0,0,.15)'/>"
             f"<g transform='translate({x+90} 355)'>{icon}</g>"
             f"<text x='{x+90}' y='412' {FONT} font-size='20' font-weight='800' fill='#333' text-anchor='middle'>{lvl}</text>"
             f"<text x='{x+90}' y='436' {FONT} font-size='14' font-weight='700' fill='#777' text-anchor='middle'>{nm}</text></g>")
body += ("<rect x='300' y='510' width='600' height='104' rx='16' fill='rgba(255,255,255,.92)'/>"
         f"<text x='600' y='550' {FONT} font-size='19' font-weight='600' fill='#444' text-anchor='middle'>Move with WASD / arrows or drag anywhere.</text>"
         f"<text x='600' y='580' {FONT} font-size='19' font-weight='600' fill='#444' text-anchor='middle'>Grow until you can swallow the target items before time runs out!</text>")
svg("menu.svg", W, H, body)

# ------------------------------------------------------------- gameplay screen
W, H = 1200, 750
body = f"<rect width='{W}' height='{H}' fill='#87e0ff' rx='14'/>"
body += checker(0, 120, W, H - 120, 60)
# cone drawn first so the hole covers its base — reads as "being swallowed"
body += cone(650, 480, 44)
body += hole(560, 470, 130, 62)
# scattered items
body += donut(880, 320, 44) + donut(220, 560, 44)
body += cone(360, 300, 40) + cone(980, 560, 40) + crate(760, 620, 46) + crate(300, 430, 42)
body += tree(1060, 320, 100) + tree(140, 300, 84) + car(900, 660, 46)
# carrot (point-down triangle) + hydrant
body += "<polygon points='480,296 462,250 498,250' fill='#ff8b1f'/><circle cx='480' cy='246' r='8' fill='#3ecf4a'/>"
body += "<rect x='640' y='230' width='26' height='40' rx='8' fill='#e23b3b'/><circle cx='653' cy='228' r='13' fill='#ffd23c'/>"
# HUD
body += chip(24, 20, "Giant Donut", "2/5", "#f7a2d4")
body += (f"<text x='{W/2}' y='58' {FONT} font-size='42' font-weight='900' fill='#fff' text-anchor='middle'>2:14</text>"
         f"<rect x='{W-190}' y='22' width='166' height='38' rx='14' fill='rgba(0,0,0,.4)'/>"
         f"<text x='{W-107}' y='48' {FONT} font-size='18' font-weight='800' fill='#fff' text-anchor='middle'>Hole: 2.6 m</text>"
         f"<text x='30' y='{H-24}' {FONT} font-size='16' font-weight='800' fill='rgba(255,255,255,.95)'>Level 1 - Donut Park</text>"
         f"<text x='{W-30}' y='{H-24}' {FONT} font-size='14' font-weight='700' fill='rgba(255,255,255,.9)' text-anchor='end'>WASD / drag to move</text>")
svg("gameplay.svg", W, H, body)

# ------------------------------------------------------------------ win screen
W, H = 1200, 750
body = f"<rect width='{W}' height='{H}' fill='#87e0ff' rx='14'/>"
body += checker(0, 0, W, H, 60)
body += f"<rect width='{W}' height='{H}' fill='rgba(20,10,40,.55)' rx='14'/>"
body += confetti_rects(W, H, 90)
body += ("<rect x='300' y='215' width='600' height='320' rx='26' fill='#fff'/>"
         f"<text x='600' y='300' {FONT} font-size='46' font-weight='900' fill='{ORANGE}' text-anchor='middle'>LEVEL COMPLETE!</text>"
         f"<text x='600' y='345' {FONT} font-size='19' font-weight='700' fill='#666' text-anchor='middle'>You ate 27 things and grew to 3.4 m wide"
         f" with 0:42 left!</text>")
btns = [("Next Level", PINK, 340), ("Retry", BLUE, 545), ("Menu", "#b9b9c9", 700)]
widths = [185, 135, 130]
for (label, col, x), bw in zip(btns, widths):
    body += (f"<rect x='{x}' y='405' width='{bw}' height='58' rx='16' fill='{col}'/>"
             f"<rect x='{x}' y='455' width='{bw}' height='8' rx='4' fill='rgba(0,0,0,.18)'/>"
             f"<text x='{x+bw/2}' y='442' {FONT} font-size='21' font-weight='800' fill='#fff' text-anchor='middle'>{label}</text>")
svg("win.svg", W, H, body)

print("done ->", OUT)
