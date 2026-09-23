"""Builds each article picture as an HTML page in Scanny's look. tools/render.py shoots them to PNG.

Scanny's rules: square corners, 3px black outlines, hard stepped shadows, nothing blurred or glowing.
Tiny5 headings (one weight), Archivo for reading, IBM Plex Mono only under barcode bars.
"""

HEAD = '''<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Tiny5&family=Archivo:wght@400;600;700&family=IBM+Plex+Mono:wght@500&display=block" rel="stylesheet">
<style>
html,body{margin:0;padding:0;background:#121214;overflow:hidden}
svg{display:block}
image{image-rendering:pixelated}
.disp{font-family:Tiny5;fill:#f6f0e3}
.txt{font-family:Archivo;font-weight:600;fill:#f6f0e3}
.dim{font-family:Archivo;fill:#aaa598}
.blk{font-family:Archivo;font-weight:700;fill:#000}
.mono{font-family:'IBM Plex Mono';font-weight:500;fill:#000}
.shelf{fill:#ffdd00}
</style></head><body>'''

PAPER, ROLL, INK, FADED = '#121214', '#1c1c21', '#f6f0e3', '#aaa598'
SHELF, SHELF_DEEP, CREAM, CREAM_SHADE, LABEL = '#ffdd00', '#d9b800', '#efe6d2', '#c9bda3', '#fffbe8'
LASER, STRIP, GOLD = '#e0131f', '#2a2a31', '#e0a912'

L = ["0001101", "0011001", "0010011", "0111101", "0100011", "0110001", "0101111", "0111011", "0110111", "0001011"]
R = ["".join('1' if c == '0' else '0' for c in code) for code in L]
G = [code[::-1] for code in R]
PARITY = ["LLLLLL", "LLGLGG", "LLGGLG", "LLGGGL", "LGLLGG", "LGGLLG", "LGGGLL", "LGLGLG", "LGLGGL", "LGGLGL"]


def ean13_modules(code):
    p = PARITY[int(code[0])]
    left = "".join((L if p[i] == 'L' else G)[int(d)] for i, d in enumerate(code[1:7]))
    right = "".join(R[int(d)] for d in code[7:])
    return "101" + left + "01010" + right + "101"


def page(name, w, h, body):
    html = HEAD + f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="{PAPER}"/>{"".join(body)}</svg></body></html>'
    open(name, 'w', encoding='utf-8').write(html)


def box(x, y, w, h, fill=ROLL, shadow=6, stroke=3):
    """A square panel with a hard stepped shadow, the site's .receipt / .key look."""
    return (f'<rect x="{x}" y="{y + shadow}" width="{w}" height="{h}" fill="#000"/>'
            f'<rect x="{x + stroke / 2}" y="{y + stroke / 2}" width="{w - stroke}" height="{h - stroke}" fill="{fill}" stroke="#000" stroke-width="{stroke}"/>')


def barcode(code, x, y, module=4, bar_h=150):
    """A real EAN-13, whole-pixel modules, on a light label with digits underneath."""
    mods = ean13_modules(code)
    quiet = 11 * module
    w = len(mods) * module + 2 * quiet
    h = bar_h + 70
    out = [box(x, y, w, h, LABEL)]
    bx = x + quiet
    for i, m in enumerate(mods):
        if m == '1':
            guard = i < 3 or 45 <= i < 50 or i >= 92
            out.append(f'<rect x="{bx + i * module}" y="{y + 22}" width="{module}" height="{bar_h + (18 if guard else 0)}" fill="#000"/>')
    fs = module * 7
    ty = y + 22 + bar_h + fs + 4
    out.append(f'<text class="mono" x="{x + quiet - 6}" y="{ty}" font-size="{fs}" text-anchor="end">{code[0]}</text>')
    out.append(f'<text class="mono" x="{bx + 3 * module + 21 * module}" y="{ty}" font-size="{fs}" text-anchor="middle" letter-spacing="{module * 1.4}">{code[1:7]}</text>')
    out.append(f'<text class="mono" x="{bx + 50 * module + 21 * module}" y="{ty}" font-size="{fs}" text-anchor="middle" letter-spacing="{module * 1.4}">{code[7:]}</text>')
    return "".join(out), w, h


def logo(x, y, scale=2):
    return f'<image href="logo.png" x="{x}" y="{y}" width="{221 * scale}" height="{256 * scale}"/>'


def wordmark(x, y, scale=3):
    return f'<image href="wordmark.png" x="{x}" y="{y}" width="{328 * scale}" height="{112 * scale}"/>'


def art(name, x, y, size=256):
    return f'<image href="{name}.webp" x="{x}" y="{y}" width="{size}" height="{size}"/>'


def shelf_label(x, y, w, h, text, free=True, fs=40):
    fill = SHELF if free else '#8b8778'
    return box(x, y, w, h, fill, shadow=5) + f'<text class="disp" style="fill:#000" x="{x + w / 2}" y="{y + h / 2 + fs * 0.36}" font-size="{fs}" text-anchor="middle">{text}</text>'


def plate(x, y, size, product):
    return box(x, y, size, size, CREAM) + art(product, x + (size - 256) / 2, y + (size - 256) / 2)


def headline(w, y, plain, gold, size=64):
    return f'<text class="disp" x="{w / 2}" y="{y}" font-size="{size}" text-anchor="middle">{plain}<tspan class="shelf">{gold}</tspan></text>'


def caption(w, y, text):
    return f'<text class="dim" x="{w / 2}" y="{y}" font-size="28" text-anchor="middle">{text}</text>'


def steps(x1, x2, y, n=5, size=14):
    """A row of pixel squares standing in for an arrow: no lines, no beams."""
    gap = (x2 - x1 - n * size) / (n - 1)
    return "".join(f'<rect x="{x1 + i * (size + gap)}" y="{y - size / 2}" width="{size}" height="{size}" fill="{SHELF}"/>' for i in range(n))


def shelves(w, h):
    """The site's shelf art along the top and bottom edge, tiled to the width."""
    out = []
    for name, y, sw in (('shelf-top', 0, 2376), ('shelf-bottom', h - 190, 2248)):
        s = 190 / 289
        tile = sw * s
        x = 0
        while x < w:
            out.append(f'<image href="{name}.webp" x="{x}" y="{y}" width="{tile}" height="190" style="image-rendering:auto"/>')
            x += tile
    return "".join(out)


# ---------------------------------------------------------------- 1 cover 2000x800
b = [shelves(2000, 800)]
lg_s, wm_s = 1.4, 2.6
lw, lh = 221 * lg_s, 256 * lg_s
ww, wh = 328 * wm_s, 112 * wm_s
tot = lw + 40 + ww
x0 = 1000 - tot / 2
b.append(f'<image href="logo.png" x="{x0}" y="{400 - lh / 2}" width="{lw}" height="{lh}"/>')
b.append(f'<image href="wordmark.png" x="{x0 + lw + 40}" y="{400 - wh / 2 - 34}" width="{ww}" height="{wh}"/>')
b.append(f'<text class="disp" x="{x0 + lw + 40 + ww / 2}" y="{400 + wh / 2 + 20}" font-size="46" text-anchor="middle">Scan any barcode. <tspan class="shelf">Launch its coin.</tspan></text>')
page('01-cover.html', 2000, 800, b)

# ---------------------------------------------------------------- 2 scan it 1600x900
b = [headline(1600, 130, 'Point. Scan. ', 'Launch.')]
b.append(logo(110, 300, 1.4))
bc, bw, bh = barcode('5449000000996', 470, 380, module=3, bar_h=120)
b.append(bc)
b.append(steps(470 + bw + 30, 1010, 470))
b.append(plate(1050, 260, 360, 'coca-cola'))
b.append(shelf_label(1050, 640, 360, 70, 'Free'))
b.append(f'<text class="txt" x="1230" y="775" font-size="30" text-anchor="middle">Coca-Cola, 330 ml</text>')
b.append(caption(1600, 850, 'Point your phone at it, or type the number.'))
page('02-scan.html', 1600, 900, b)

# ---------------------------------------------------------------- 3 one barcode, one coin 1600x900
b = [headline(1600, 130, 'One barcode. ', 'One coin. Forever.', size=60)]
bc, bw, bh = barcode('5449000000996', 110, 330, module=3, bar_h=150)
b.append(bc)
b.append(steps(110 + bw + 30, 700, 450))
# the coin: a gold ring holding the product
cx, cy, r = 870, 450, 150
b.append(f'<circle cx="{cx}" cy="{cy + 6}" r="{r}" fill="#000"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="{GOLD}" stroke="#000" stroke-width="3"/>')
b.append(f'<circle cx="{cx}" cy="{cy}" r="{r - 22}" fill="{CREAM}" stroke="#000" stroke-width="3"/>')
b.append(art('coca-cola', cx - 100, cy - 100, 200))
# two launch attempts
rows = [(300, 'First launch', 'Lands. Yours for good.', True), (520, 'Second launch', 'Refused by the chain.', False)]
for y, head, sub, ok in rows:
    b.append(box(1100, y, 400, 150, ROLL))
    fill = SHELF if ok else LASER
    b.append(f'<rect x="1130" y="{y + 45}" width="56" height="56" fill="{fill}" stroke="#000" stroke-width="3"/>')
    mark = (f'<path d="M1142 {y + 73}l11 11l22 -22" fill="none" stroke="#000" stroke-width="7" stroke-linecap="square"/>' if ok else
            f'<path d="M1145 {y + 60}l26 26M1171 {y + 60}l-26 26" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="square"/>')
    b.append(mark)
    b.append(f'<text class="disp" x="1210" y="{y + 68}" font-size="34">{head}</text>')
    b.append(f'<text class="dim" x="1210" y="{y + 108}" font-size="26">{sub}</text>')
b.append(caption(1600, 820, 'The coin’s address is built from the barcode’s digits.'))
page('03-one-coin.html', 1600, 900, b)

# ---------------------------------------------------------------- 4 half the fees 1600x900
b = [headline(1600, 130, 'Half the fees. ', 'For life.')]
# trades feeding in
b.append(box(110, 250, 380, 400, ROLL))
b.append(f'<text class="disp" x="140" y="310" font-size="34">Every trade</text>')
for i, amt in enumerate(['0.42', '1.10', '0.08', '2.35', '0.61']):
    y = 360 + i * 60
    b.append(f'<rect x="140" y="{y - 30}" width="320" height="46" fill="{STRIP}"/>')
    b.append(f'<text class="txt" x="160" y="{y + 2}" font-size="26">Buy</text>' if i % 2 == 0 else f'<text class="txt" x="160" y="{y + 2}" font-size="26">Sell</text>')
    b.append(f'<text class="txt" x="440" y="{y + 2}" font-size="26" text-anchor="end">{amt} SOL</text>')
b.append(steps(520, 640, 465, n=4))
# the split bar
bx, by, bw2, bh2 = 670, 360, 820, 210
b.append(f'<rect x="{bx}" y="{by + 7}" width="{bw2}" height="{bh2}" fill="#000"/>')
b.append(f'<rect x="{bx + 1.5}" y="{by + 1.5}" width="{bw2 / 2}" height="{bh2 - 3}" fill="{SHELF}" stroke="#000" stroke-width="3"/>')
b.append(f'<rect x="{bx + bw2 / 2}" y="{by + 1.5}" width="{bw2 / 2 - 1.5}" height="{bh2 - 3}" fill="{STRIP}" stroke="#000" stroke-width="3"/>')
b.append(f'<text class="disp" style="fill:#000" x="{bx + bw2 / 4}" y="{by + 120}" font-size="86" text-anchor="middle">50%</text>')
b.append(f'<text class="blk" x="{bx + bw2 / 4}" y="{by + 175}" font-size="28" text-anchor="middle">The first scanner</text>')
b.append(f'<text class="disp" style="fill:{FADED}" x="{bx + bw2 * 3 / 4}" y="{by + 120}" font-size="86" text-anchor="middle">50%</text>')
b.append(f'<text class="dim" x="{bx + bw2 * 3 / 4}" y="{by + 175}" font-size="28" text-anchor="middle">Scanny</text>')
b.append(f'<text class="txt" x="{bx}" y="{by - 40}" font-size="30">Each coin’s creator fee, split:</text>')
b.append(f'<text class="txt" x="{bx}" y="{by + bh2 + 70}" font-size="30">Paid by pump.fun, <tspan class="shelf">straight to your wallet.</tspan></text>')
b.append(caption(1600, 820, 'Locked into the coin at launch. Nobody can change it, us included.'))
page('04-fees.html', 1600, 900, b)

# ---------------------------------------------------------------- 5 close 1600x900
b = [shelves(1600, 900)]
s = 1.1
x0 = 800 - (221 * s + 20 + 328 * 2.2) / 2
wx = x0 + 221 * s + 20
b.append(f'<image href="logo.png" x="{x0}" y="{300 - 20}" width="{221 * s}" height="{256 * s}"/>')
b.append(wordmark(wx, 300, 2.2))
b.append(f'<text class="disp" x="{wx}" y="{300 + 112 * 2.2 + 30}" font-size="64" style="fill:{SHELF}">scanny.fun</text>')
b.append(box(260, 610, 1080, 80, ROLL, shadow=5))
b.append(f'<text class="disp" x="290" y="663" font-size="34" style="fill:{SHELF}">$SCANNY</text>')
b.append(f'<text class="txt" x="1310" y="661" font-size="27" text-anchor="end" style="font-family:\'IBM Plex Mono\';font-weight:500">G8TTWtBR6AqxzMC8nSwdVt7NCUDGvqjUEWRr5SXdpump</text>')
page('05-close.html', 1600, 900, b)
