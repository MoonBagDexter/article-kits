"""Builds each article picture as an HTML page in Candy or Curse's own look (src/client/ui/tot.css in the game repo):
the candy side (gingerbread, candy-cane red and white, gold) against the curse side (crypt purple, toxic slime green),
pitch-ink outlines with hard drop shadows. Taffy for candy words, Crypt for curse words, Atkinson for reading text.
The stills are frames of the game's own filmed knocks and its town map; the art is the game's brand art.
render.py shoots them to PNG."""

CANDY, PEPPER, GOLD, GRAPE, CURSE, TOXIC, CHOC, INK = '#e8262b', '#fff8ec', '#ffc93c', '#8a3dff', '#23142f', '#8fe03a', '#5a3020', '#120a10'
RIM, LILAC, SLAB = '#5d3a80', '#cbb6ea', '#2e1b40'
URL = 'web-production-7836f.up.railway.app'
WORD_R = 1000 / 530  # wordmark.webp width / height

HEAD = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Taffy;src:url(coc-taffy.woff2) format('woff2')}}
@font-face{{font-family:Crypt;src:url(coc-crypt.woff2) format('woff2')}}
@font-face{{font-family:Txt;src:url(coc-text.woff2) format('woff2');font-weight:200 800}}
html,body{{margin:0;padding:0;background:{CURSE};overflow:hidden}}
svg{{display:block}}
.tf{{font-family:Taffy}} .cr{{font-family:Crypt}}
.tx{{font-family:Txt;font-weight:600}}
.o{{paint-order:stroke;stroke:{INK};stroke-linejoin:round}}
image.px{{image-rendering:pixelated}}
</style></head><body>'''

DEFS = f'''<defs>
<pattern id="cane" width="28" height="28" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
<rect width="28" height="28" fill="{PEPPER}"/><rect width="14" height="28" fill="{CANDY}"/></pattern>
</defs>'''

_clip = [0]


def pool(cx, cy, rx, ry, k=.7):
    return (f'<radialGradient id="pl{cx}"><stop offset="0" stop-color="{INK}" stop-opacity="{k}"/>'
            f'<stop offset="1" stop-color="{INK}" stop-opacity="0"/></radialGradient>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#pl{cx})"/>')


def page(name, w, h, body, bg=CURSE):
    html = HEAD + (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}'
                   f'<rect width="{w}" height="{h}" fill="{bg}"/>{"".join(body)}</svg></body></html>')
    open(name, 'w', encoding='utf-8').write(html)


def text(x, y, s, size, fill=PEPPER, cls='tf', anchor='middle', sw=None, shadow=True):
    """A word in the game's way: an ink outline and a hard ink shadow straight down."""
    sw = sw if sw is not None else max(4, size * 0.11)
    out = ''
    if shadow:
        out += (f'<text class="{cls} o" x="{x}" y="{y + size * 0.09}" font-size="{size}" text-anchor="{anchor}" '
                f'fill="{INK}" stroke-width="{sw}">{s}</text>')
    out += f'<text class="{cls} o" x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{fill}" stroke-width="{sw}">{s}</text>'
    return out


def plain(x, y, s, size, fill=LILAC, anchor='middle', weight=600):
    return f'<text class="tx" x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">{s}</text>'


def panel(x, y, w, h, side='curse', u=6):
    """A slab: ink outline, a hard ink shadow, and a candy-cane or slime top edge."""
    fill = CHOC if side == 'candy' else SLAB
    s = f'<rect x="{x + 10}" y="{y + 12}" width="{w}" height="{h}" rx="6" fill="{INK}"/>'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{INK}"/>'
    s += f'<rect x="{x + u}" y="{y + u}" width="{w - 2 * u}" height="{h - 2 * u}" rx="3" fill="{fill}"/>'
    if side == 'candy':
        s += f'<rect x="{x + u}" y="{y + u}" width="{w - 2 * u}" height="18" fill="url(#cane)"/><rect x="{x + u}" y="{y + u + 18}" width="{w - 2 * u}" height="4" fill="{INK}"/>'
    else:
        s += f'<rect x="{x + u}" y="{y + u}" width="{w - 2 * u}" height="14" fill="{TOXIC}"/>'
        for i in range(int((w - 40) / 70)):
            dx = x + 30 + i * 70 + (i * 37) % 23
            dh = 14 + (i * 29) % 26
            s += f'<rect x="{dx}" y="{y + u + 10}" width="12" height="{dh}" rx="6" fill="{TOXIC}"/>'
    return s


def still(src, x, y, w, h, iw, ih, ox=0, oy=0, side='curse'):
    """A picture in a slab. The image is drawn iw x ih and shifted by ox, oy inside the window."""
    _clip[0] += 1
    c = f'c{_clip[0]}'
    ix, iy, cw, ch = x + 6, y + 6 + (22 if side == 'candy' else 14), w - 12, h - 12 - (22 if side == 'candy' else 14)
    return (panel(x, y, w, h, side) +
            f'<clipPath id="{c}"><rect x="{ix}" y="{iy}" width="{cw}" height="{ch}"/></clipPath>'
            f'<image href="{src}" x="{ix - ox}" y="{iy - oy}" width="{iw}" height="{ih}" clip-path="url(#{c})" preserveAspectRatio="none"/>'
            + (panel_drips(x, y, w) if side == 'curse' else ''))


def panel_drips(x, y, w):
    s = ''
    for i in range(int((w - 40) / 70)):
        dx = x + 30 + i * 70 + (i * 37) % 23
        dh = 8 + (i * 29) % 12
        s += f'<rect x="{dx}" y="{y + 16}" width="12" height="{dh}" rx="6" fill="{TOXIC}"/>'
    return f'<rect x="{x + 6}" y="{y + 6}" width="{w - 12}" height="14" fill="{TOXIC}"/>' + s


def img(src, x, y, w, h, px=False):
    return f'<image {"class=\"px\" " if px else ""}href="{src}" x="{x}" y="{y}" width="{w}" height="{h}"/>'


def headline(w, a, b, size=92, y=128, b_fill=GOLD):
    return text(w / 2, y, f'{a}<tspan fill="{b_fill}">{b}</tspan>', size)


def arrow(x, y, w=70):
    return (f'<path d="M{x} {y - 10}h{w - 30}v-18l34 28l-34 28v-18h-{w - 30}z" fill="{GOLD}" stroke="{INK}" '
            f'stroke-width="5" stroke-linejoin="round"/>')


# ---------------------------------------------------------------- 1 cover 2000x800
# The candy-or-curse street fills it; the wordmark over the moon, the promise on a slab below.
b = [img('street.webp', 0, -250, 2000, 1125, True)]
b.append(f'<rect width="2000" height="800" fill="{CURSE}" opacity=".18"/>')
ww = 820
b.append(pool(1000, 290, 620, 260, .75))
b.append(img('wordmark.webp', 1000 - ww / 2, 40, ww, ww / WORD_R))
b.append(f'<rect x="470" y="534" width="1060" height="176" rx="6" fill="{INK}"/>'
         f'<rect x="460" y="522" width="1060" height="176" rx="6" fill="{INK}"/>'
         f'<rect x="466" y="528" width="1048" height="164" rx="3" fill="{CURSE}"/>')
b.append(text(1000, 600, 'Knock for candy.', 64, GOLD))
b.append(text(1000, 670, 'Or get cursed.', 64, TOXIC, 'cr'))
page('01-cover.html', 2000, 800, b)

# ---------------------------------------------------------------- 2 knock 1600x900
b = [headline(1600, 'Knock. Then ', 'hope.')]
# Frames from the game's own clips, cropped above the clip's corner plate.
b.append(still('treat.jpg', 60, 196, 720, 470, 900, 506, 40, 8, 'candy'))
b.append(still('scare.jpg', 820, 196, 720, 470, 900, 506, 90, 62, 'curse'))
b.append(text(420, 742, 'Candy', 70, GOLD))
b.append(plain(420, 790, 'Most doors give you a treat', 30, PEPPER))
b.append(text(1180, 742, 'Curse', 76, TOXIC, 'cr'))
b.append(plain(1180, 790, 'Some doors jump scare you', 30, PEPPER))
b.append(plain(800, 862, '8 scares, each with its own monster. Get scared and your candy spills for anyone to grab.', 26))
page('02-knock.html', 1600, 900, b)

# ---------------------------------------------------------------- 3 paid 1600x900
b = [headline(1600, 'Hold $CoC. ', 'Get paid in $CoC.', 84)]
steps = [('logo.webp', 'Hold $CoC', 'One free signature', 150, 150),
         ('ic-door.webp', 'Knock', 'Some treats pay $CoC', 150, 149),
         ('ic-treat.webp', 'Paid', 'Straight to your wallet', 170, 140)]
for i, (src, a, c, iw, ih) in enumerate(steps):
    x = 70 + i * 515
    b.append(panel(x, 190, 430, 360, 'candy' if i != 1 else 'curse'))
    b.append(img(src, x + 215 - iw / 2, 250 + (150 - ih) / 2, iw, ih))
    b.append(text(x + 215, 468, a, 56, GOLD if i != 1 else PEPPER))
    b.append(plain(x + 215, 520, c, 28, PEPPER))
    if i < 2:
        b.append(arrow(x + 448, 370, 60))
# Bigger bag, bigger bucket: the five buckets, paper bag to coffin.
b.append(panel(70, 600, 1460, 220, 'curse'))
bx = 120
for i, (src, w, h) in enumerate([('bk-1.webp', 260, 290), ('bk-2.webp', 243, 317), ('bk-3.webp', 333, 358),
                                 ('bk-4.webp', 260, 344), ('bk-5.webp', 218, 324)]):
    k = (0.30 + i * 0.045) * 1.0
    dw, dh = w * k, h * k
    b.append(img(src, bx, 790 - dh, dw, dh))
    bx += dw + 26
b.append(text(1180, 706, 'Bigger bag,', 54, PEPPER))
b.append(text(1180, 770, 'up to 2x treats', 54, GOLD))
b.append(plain(800, 870, 'Paid from creator fees. Every paid treat buys $CoC.', 26))
page('03-paid.html', 1600, 900, b)

# ---------------------------------------------------------------- 4 town 1600x900
b = [headline(1600, 'Level up. ', 'Open the town.')]
# The game's own town map page, cropped to the map.
b.append(still('map-shot.png', 60, 196, 860, 600, 1978, 1112, 446, 330, 'curse'))
rows = [('1', 'Hollow Lane'), ('2', 'The Graveyard'), ('2', 'The corn maze'), ('3', 'Scream Park'), ('5', 'Witch Woods')]
for i, (lv, name) in enumerate(rows):
    y = 196 + i * 100
    b.append(f'<rect x="980" y="{y + 6}" width="560" height="80" rx="6" fill="{INK}"/>'
             f'<rect x="974" y="{y}" width="560" height="80" rx="6" fill="{INK}"/>'
             f'<rect x="980" y="{y + 6}" width="548" height="68" rx="3" fill="{CHOC if i == 0 else SLAB}"/>')
    b.append(f'<circle cx="1026" cy="{y + 40}" r="30" fill="{GOLD}" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<text class="tf" x="1026" y="{y + 54}" font-size="40" text-anchor="middle" fill="{INK}">{lv}</text>')
    b.append(text(1080, y + 54, name, 40, PEPPER, anchor='start'))
b.append(img('ic-bell.webp', 1000, 708, 92, 92))
b.append(text(1110, 752, 'The Big House', 40, GOLD, anchor='start'))
b.append(plain(1110, 790, 'Opens every 15 to 25 minutes', 26, PEPPER, anchor='start'))
b.append(plain(800, 862, 'Fly over all of it on a broom.', 26))
page('04-town.html', 1600, 900, b)

# ---------------------------------------------------------------- 5 close 1600x900
b = [img('porch.webp', 0, 0, 1600, 900, True)]
b.append(f'<rect width="1600" height="900" fill="{CURSE}" opacity=".12"/>')
b.append(pool(300, 760, 340, 190, .8))
b.append(img('wordmark.webp', 50, 640, 470, 470 / WORD_R))
b.append(f'<rect x="560" y="664" width="1000" height="190" rx="6" fill="{INK}"/>'
         f'<rect x="550" y="652" width="1000" height="190" rx="6" fill="{INK}"/>'
         f'<rect x="556" y="658" width="988" height="178" rx="3" fill="{CURSE}"/>')
b.append(text(1050, 728, 'Free in your browser', 56, GOLD))
b.append(plain(1050, 796, URL, 38, PEPPER, weight=700))
page('05-close.html', 1600, 900, b)
