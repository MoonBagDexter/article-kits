"""Builds each article picture as an HTML page in Pair Pond's own look (docs/ui-identity.md in the game repo):
navy pixel frames with stepped corners and hard navy shadows, flag yellow for the one phrase that matters,
Jersey 15 for titles, Instrument Sans for the rest. No gradients, glows or blur. The stills are the game's own
filmed key art, the logo is the pixel bobber traced from src/client/ui/logo.ts. render.py shoots them to PNG."""

NAVY, YELLOW, SKY, TINT, PAPER, RED, TEAL = '#08103a', '#ffd21f', '#80dcf8', '#e3f4fb', '#f8f8f8', '#f83a2c', '#177178'
MARK_R = 68 / 57   # mark.svg width / height
WORD_R = 83 / 18   # wordmark.svg width / height

HEAD = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:PP;src:url(pp-jersey.woff2) format('woff2')}}
@font-face{{font-family:MPS;src:url(mp-sans.woff2) format('woff2');font-weight:100 900}}
html,body{{margin:0;padding:0;background:{TEAL};overflow:hidden}}
svg{{display:block}}
.px{{font-family:PP;fill:#fff}}
.pxn{{font-family:PP;fill:{NAVY}}}
.y{{fill:{YELLOW}}}
.t{{font-family:MPS;font-weight:600;fill:{NAVY}}}
.tw{{font-family:MPS;font-weight:600;fill:#fff}}
.dim{{font-family:MPS;font-weight:500;fill:#4a5178}}
</style></head><body>'''

_clip = [0]


def page(name, w, h, body, bg=TEAL):
    html = HEAD + (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns:xlink="http://www.w3.org/1999/xlink">'
                   f'<rect width="{w}" height="{h}" fill="{bg}"/>{"".join(body)}</svg></body></html>')
    open(name, 'w', encoding='utf-8').write(html)


def box(x, y, w, h, fill=PAPER, u=6, shadow=True):
    """A pixel frame: navy outline one unit thick, stepped corners, a hard navy shadow down and right."""
    s = ''
    if shadow:
        s += (f'<rect x="{x + 2 * u}" y="{y + u}" width="{w - 2 * u}" height="{h}" fill="{NAVY}"/>'
              f'<rect x="{x + u}" y="{y + 2 * u}" width="{w}" height="{h - 2 * u}" fill="{NAVY}"/>')
    s += (f'<rect x="{x + u}" y="{y}" width="{w - 2 * u}" height="{h}" fill="{NAVY}"/>'
          f'<rect x="{x}" y="{y + u}" width="{w}" height="{h - 2 * u}" fill="{NAVY}"/>')
    if fill:
        s += (f'<rect x="{x + 2 * u}" y="{y + u}" width="{w - 4 * u}" height="{h - 2 * u}" fill="{fill}"/>'
              f'<rect x="{x + u}" y="{y + 2 * u}" width="{w - 2 * u}" height="{h - 4 * u}" fill="{fill}"/>')
    return s


def still(src, x, y, w, h, iw, ih, ox=0, oy=0, u=6):
    """A game still in a pixel frame. The image is drawn iw x ih and shifted by ox, oy inside the window."""
    _clip[0] += 1
    c = f'c{_clip[0]}'
    ix, iy, cw, ch = x + u, y + u, w - 2 * u, h - 2 * u
    return (box(x, y, w, h, None, u) +
            f'<clipPath id="{c}"><rect x="{ix + u}" y="{iy}" width="{cw - 2 * u}" height="{ch}"/><rect x="{ix}" y="{iy + u}" width="{cw}" height="{ch - 2 * u}"/></clipPath>'
            f'<image href="{src}" x="{ix - ox}" y="{iy - oy}" width="{iw}" height="{ih}" clip-path="url(#{c})" preserveAspectRatio="none"/>')


def chip(x, y, text, size=30, fill=YELLOW, cls='t', u=4, pad=18, w=None):
    w = w or int(len(text) * size * 0.56 + 2 * pad)
    h = int(size * 1.7)
    return box(x, y, w, h, fill, u, shadow=False) + f'<text class="{cls}" x="{x + w / 2}" y="{y + h / 2 + size * 0.36}" font-size="{size}" text-anchor="middle">{text}</text>'


def header(w, text, size=92, h=160):
    return (f'<rect width="{w}" height="{h}" fill="{NAVY}"/>'
            f'<text class="px" x="{w / 2}" y="{h / 2 + size * 0.33}" font-size="{size}" text-anchor="middle">{text}</text>')


def lockup(x, y, h):
    """Mark and wordmark side by side, like the title screen. Returns the markup and its width."""
    mh = h * 1.35
    mw = mh * MARK_R
    ww = h * WORD_R
    return (f'<image href="mark.svg" x="{x}" y="{y + h / 2 - mh / 2}" width="{mw}" height="{mh}"/>'
            f'<image href="wordmark.svg" x="{x + mw + h * 0.25}" y="{y}" width="{ww}" height="{h}"/>'), mw + h * 0.25 + ww


def tick(x, y, s=40):
    return (f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{YELLOW}" stroke="{NAVY}" stroke-width="4"/>'
            f'<path d="M{x + s * .22} {y + s * .52}L{x + s * .42} {y + s * .72}L{x + s * .8} {y + s * .3}" fill="none" stroke="{NAVY}" stroke-width="6" stroke-linecap="square"/>')


def cross(x, y, s=40):
    return (f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{RED}" stroke="{NAVY}" stroke-width="4"/>'
            f'<path d="M{x + s * .28} {y + s * .28}L{x + s * .72} {y + s * .72}M{x + s * .72} {y + s * .28}L{x + s * .28} {y + s * .72}" stroke="{NAVY}" stroke-width="6"/>')


def coin(cx, cy, r, letters, fill):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{NAVY}" stroke-width="5"/>'
            f'<text class="t" x="{cx}" y="{cy + r * 0.3}" font-size="{r * 0.85}" text-anchor="middle">{letters}</text>')


# ---------------------------------------------------------------- 1 cover 2000x800
# The lighthouse still fills the right; the left is the title panel.
b = []
b.append(f'<image href="lighthouse.webp" x="560" y="0" width="1440" height="810" preserveAspectRatio="none"/>')
b.append(f'<rect x="0" y="0" width="600" height="800" fill="{SKY}"/><rect x="600" y="0" width="12" height="800" fill="{NAVY}"/>')
b.append(box(56, 190, 800, 420, PAPER, 8))
lk, lw = lockup(0, 0, 110)
b.append(f'<g transform="translate({456 - lw / 2} 270)">{lk}</g>')
b.append(f'<text class="pxn" x="456" y="520" font-size="66" text-anchor="middle">Every fish is a <tspan fill="{RED}">real coin</tspan></text>')
page('01-cover.html', 2000, 800, b)

# ---------------------------------------------------------------- 2 the catch 1600x900
b = [header(1600, f'Land a fish. <tspan class="y">Get the coin.</tspan>')]
b.append(still('catch.webp', 50, 205, 930, 560, 1014, 570, 42, 0))
b.append(box(1030, 205, 520, 560, PAPER, 6))
rows = [('fish-bass.png', 'Picked coins', 'Chosen by the Fish Finder'),
        ('fish-koi.png', 'Staples', 'Always in the harbour'),
        ('fish-gold.png', 'Golden fish', 'Stocks, on Solana')]
for i, (img, a, c) in enumerate(rows):
    y = 240 + i * 172
    b.append(f'<rect x="1058" y="{y}" width="160" height="140" fill="{TINT}"/>')
    b.append(f'<image href="{img}" x="1058" y="{y + 30}" width="160" height="80"/>')
    b.append(f'<text class="t" x="1244" y="{y + 60}" font-size="34">{a}</text>')
    b.append(f'<text class="dim" x="1244" y="{y + 102}" font-size="23">{c}</text>')
b.append(f'<text class="tw" x="800" y="850" font-size="30" text-anchor="middle">Hold the pond\'s coin and every fish you land pays you that coin.</text>')
page('02-catch.html', 1600, 900, b)

# ---------------------------------------------------------------- 3 every catch pays 1600x900
b = [header(1600, f'Every catch <tspan class="y">pays you.</tspan>')]
steps = [('fish-marlin.png', 300, 150, 'Land a fish'), ('money-coin-stack.png', 190, 190, 'Fees buy that coin'),
         ('money-bag.png', 190, 190, 'Sent to your wallet')]
for i, (img, iw, ih, label) in enumerate(steps):
    x = 50 + i * 530
    b.append(box(x, 196, 440, 330, PAPER, 6))
    b.append(f'<image href="{img}" x="{x + 220 - iw / 2}" y="{362 - ih / 2 - 20}" width="{iw}" height="{ih}"/>')
    b.append(f'<text class="t" x="{x + 220}" y="492" font-size="34" text-anchor="middle">{label}</text>')
    if i < 2:
        ax = x + 452
        b.append(f'<path d="M{ax} 361H{ax + 44}" stroke="{NAVY}" stroke-width="12"/><path d="M{ax + 44} 343L{ax + 68} 361L{ax + 44} 379Z" fill="{NAVY}"/>')
b.append(box(50, 566, 1500, 300, PAPER, 6))
b.append(f'<text class="pxn" x="96" y="650" font-size="54">Hold more,</text>')
b.append(f'<text class="pxn" x="96" y="712" font-size="54">fish <tspan fill="{RED}">luckier.</tspan></text>')
b.append(f'<text class="dim" x="96" y="770" font-size="24">Rarer bites and bigger catches.</text>')
b.append(f'<text class="dim" x="96" y="804" font-size="24">No coin? You still fish for silver.</text>')
rar = ['common', 'uncommon', 'rare', 'epic', 'legendary']
for i, r in enumerate(rar):
    cx = 640 + i * 200
    sz = 120 + i * 12
    b.append(f'<image href="badge-rarity-{r}.png" x="{cx - sz / 2}" y="{730 - sz}" width="{sz}" height="{sz}"/>')
    b.append(f'<text class="t" x="{cx}" y="772" font-size="26" text-anchor="middle">{r.capitalize()}</text>')
b.append(f'<path d="M560 812H1480" stroke="{NAVY}" stroke-width="8"/><path d="M1480 798L1504 812L1480 826Z" fill="{NAVY}"/>')
page('03-pays.html', 1600, 900, b)

# ---------------------------------------------------------------- 4 silver, streaks, frenzies 1600x900
b = [header(1600, f'Sell for silver. <tspan class="y">Stack it up.</tspan>')]
b.append(still('frenzy.webp', 50, 196, 1500, 310, 1500, 437, 0, 90))
b.append(chip(88, 430, 'Frenzy: bites come fast, every fish sells for 50% more', 28, fill=YELLOW, u=4, pad=22))
cards = [('money-coin-stack-silver.png', 'Fish market', 'Sell your catch', 'for silver'),
         ('badge-streak.png', 'Streaks', 'Fish in a row', 'sell for more'),
         ('badge-perfect.png', 'Perfect hooks', 'Hook it on the bite', 'for more silver'),
         ('badge-medal-gold.png', 'Events', 'Tournaments, hunts', 'and cash drops')]
for i, (img, a, l1, l2) in enumerate(cards):
    x = 50 + i * 383
    b.append(box(x, 548, 350, 320, PAPER, 6))
    b.append(f'<image href="{img}" x="{x + 175 - 70}" y="572" width="140" height="140"/>')
    b.append(f'<text class="t" x="{x + 175}" y="760" font-size="34" text-anchor="middle">{a}</text>')
    b.append(f'<text class="dim" x="{x + 175}" y="800" font-size="24" text-anchor="middle">{l1}</text>')
    b.append(f'<text class="dim" x="{x + 175}" y="832" font-size="24" text-anchor="middle">{l2}</text>')
page('04-silver.html', 1600, 900, b)

# ---------------------------------------------------------------- 5 the Fish Finder 1600x900
b = [header(1600, f'Watch the Fish Finder <tspan class="y">pick.</tspan>')]
# a coin comes in
b.append(box(50, 330, 260, 300, PAPER, 6))
b.append(coin(180, 440, 70, '?', SKY))
b.append('<text class="t" x="180" y="570" font-size="28" text-anchor="middle">A coin moving</text>')
b.append('<text class="t" x="180" y="604" font-size="28" text-anchor="middle">today</text>')
b.append(f'<path d="M322 480H392" stroke="{NAVY}" stroke-width="12"/><path d="M392 462L416 480L392 498Z" fill="{NAVY}"/>')
# the checks, one at a time
b.append(box(430, 196, 560, 616, PAPER, 6))
b.append(f'<text class="pxn" x="710" y="262" font-size="46" text-anchor="middle">Checked live</text>')
checks = ['Real buyers', 'No wash trading', 'Not bundled', 'Enough liquidity', 'Market cap floor',
          'Survived its launch', 'Holders spread out', 'Not dumping']
for i, c in enumerate(checks):
    y = 290 + i * 62
    if i % 2 == 0:
        b.append(f'<rect x="448" y="{y - 4}" width="524" height="60" fill="{TINT}"/>')
    b.append(tick(474, y + 6))
    b.append(f'<text class="t" x="536" y="{y + 38}" font-size="30">{c}</text>')
# the two ends
b.append(f'<path d="M1002 400H1062" stroke="{NAVY}" stroke-width="12"/><path d="M1062 382L1086 400L1062 418Z" fill="{NAVY}"/>')
b.append(f'<path d="M1002 660H1062" stroke="{NAVY}" stroke-width="12"/><path d="M1062 642L1086 660L1062 678Z" fill="{NAVY}"/>')
b.append(box(1100, 250, 450, 290, PAPER, 6))
b.append(chip(1130, 280, 'Chosen', 32))
b.append(f'<image href="fish-marlin.png" x="1185" y="336" width="280" height="140"/>')
b.append('<text class="t" x="1325" y="516" font-size="28" text-anchor="middle">Swims in the harbour</text>')
b.append(box(1100, 560, 450, 220, PAPER, 6))
b.append(chip(1130, 590, 'Thrown back', 32, fill=TINT))
b.append(cross(1140, 680))
b.append('<text class="t" x="1200" y="712" font-size="28">Bundled at launch</text>')
b.append('<text class="dim" x="1140" y="752" font-size="22">The reason is shown on screen</text>')
b.append('<text class="tw" x="800" y="868" font-size="28" text-anchor="middle">Every check runs in the open. Anyone can watch.</text>')
page('05-finder.html', 1600, 900, b)

# ---------------------------------------------------------------- 6 boats 1600x900
b = [header(1600, f'Bigger bag, <tspan class="y">bigger boat.</tspan>')]
b.append(box(50, 200, 1500, 360, TINT, 6))
tiers = ['dinghy', 'skiff', 'fisher', 'sportfisher', 'yacht', 'superyacht']
names = ['Dinghy', 'Skiff', 'Fisher', 'Sportfisher', 'Yacht', 'Superyacht']
for i, (t, n) in enumerate(zip(tiers, names)):
    w = 200 + i * 18
    h = w * 400 / 640
    cx = 170 + i * 252
    b.append(f'<image href="boat-{t}.png" x="{cx - w / 2}" y="{448 - h}" width="{w}" height="{h}"/>')
    b.append(f'<text class="t" x="{cx}" y="484" font-size="26" text-anchor="middle">{n}</text>')
b.append(f'<path d="M110 520H1450" stroke="{NAVY}" stroke-width="10"/><path d="M1450 504L1480 520L1450 536Z" fill="{NAVY}"/>')
b.append(f'<rect x="690" y="500" width="220" height="40" fill="{TINT}"/><text class="t" x="800" y="530" font-size="28" text-anchor="middle">Hold more</text>')
b.append(still('trip.webp', 50, 600, 1500, 270, 1500, 437, 0, 110))
b.append(chip(88, 800, 'Boat trips pay holders by bag size', 28, fill=YELLOW, u=4, pad=20))
page('06-boats.html', 1600, 900, b)

# ---------------------------------------------------------------- 7 closing 1600x900
b = []
b.append('<image href="bonk.webp" x="0" y="-40" width="1600" height="900" preserveAspectRatio="none"/>')
b.append(f'<rect x="0" y="730" width="1600" height="170" fill="{NAVY}"/>')
b.append(f'<text class="px" x="70" y="842" font-size="84">Bring a bat.</text>')
b.append(chip(1110, 762, 'pairpond.fun', 50, fill=YELLOW, cls='t', u=6, pad=28, w=440))
page('07-close.html', 1600, 900, b)
print('built')
