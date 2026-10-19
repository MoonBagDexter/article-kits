"""Builds each article picture as an HTML page in Grokpad's look. tools/render.py shoots them to PNG.

Colours, fonts and logos come from the grok-launcher redesign (frontend worktree: globals.css, docs/BRAND.md,
public/brand): LED white on true black, Urbanist + Doto + JetBrains Mono (the Grokpad font kit), the logo's lime as the one accent.
"""

HEAD = '''<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Urbanist:wght@400;500;600;700&family=Doto:ROND,wght@0..100,100..900&family=JetBrains+Mono:wght@400;500;700&display=block" rel="stylesheet">
<style>
html,body{margin:0;padding:0;background:#000000;overflow:hidden}
svg{display:block}
.disp{font-family:Urbanist;font-weight:700;fill:#f4f6ee;letter-spacing:-0.03em}
.txt{font-family:Urbanist;fill:#f4f6ee}
.muted{font-family:Urbanist;fill:rgb(244 246 238 / 0.6)}
.dim{font-family:Urbanist;fill:rgb(244 246 238 / 0.38)}
.mono{font-family:'JetBrains Mono';fill:#f4f6ee}
.lime{fill:#a6ec0d}
.led{fill:#f4f6ee;font-family:Doto;font-variation-settings:'ROND' 100;font-weight:900}
.led.lime{fill:#a6ec0d}
.pct{font-family:Urbanist;font-weight:700;font-variation-settings:normal}
.glow{filter:drop-shadow(0 0 10px #5aab04)}
.panel{fill:#0a0a0a;stroke:rgb(255 255 255 / 0.15);stroke-width:2}
.panel-lit{fill:#0d1306;stroke:#a6ec0d;stroke-width:3}
.wire{fill:none;stroke:#a6ec0d;stroke-width:5;stroke-linecap:round}
.wire-dim{fill:none;stroke:rgb(255 255 255 / 0.22);stroke-width:4;stroke-linecap:round}
.dash{fill:none;stroke:#a6ec0d;stroke-width:5;stroke-dasharray:2 16;stroke-linecap:round}
</style></head><body>'''

DEFS = '''<defs>
<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#5aab04" stop-opacity="0.22"/><stop offset="1" stop-color="#a6ec0d" stop-opacity="0"/></radialGradient>
<pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="14" cy="14" r="1.4" fill="#ffffff" fill-opacity="0.075"/></pattern>
</defs>'''

LIME = '#a6ec0d'
URL = 'grokpad.org'


def page(name, w, h, body):
    html = HEAD + f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}<rect width="{w}" height="{h}" fill="url(#dots)"/>{"".join(body)}</svg></body></html>'
    open(name, 'w', encoding='utf-8').write(html)


def mark(cx, cy, size, glow=True):
    g = f'<circle cx="{cx}" cy="{cy}" r="{size * 0.85}" fill="url(#glow)"/>' if glow else ''
    return g + f'<image href="logo.png" x="{cx - size / 2}" y="{cy - size / 2}" width="{size}" height="{size}"/>'


def panel(x, y, w, h, r=20, lit=False):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" class="{"panel-lit" if lit else "panel"}"/>'


def lockup(cx, cy, h, glow=True):
    """The real logo + LED wordmark (public/brand/lockup.png, 1511x406), centred."""
    w = h * 1511 / 406
    g = f'<ellipse cx="{cx}" cy="{cy}" rx="{w * 0.62}" ry="{h * 0.95}" fill="url(#glow)"/>' if glow else ''
    return g + f'<image href="lockup.png" x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}"/>'


# ---------------------------------------------------------------- 1 cover 2000x800
b = [lockup(1000, 350, 340)]
b.append('<text class="muted" x="1000" y="640" font-size="52" text-anchor="middle" font-weight="500">Free coin launches. <tspan class="lime">Just ask Grok.</tspan></text>')
page('01-cover.html', 2000, 800, b)

# ---------------------------------------------------------------- 2 set it up 1600x900
b = ['<text class="disp" x="800" y="132" font-size="62" text-anchor="middle">Set it up <tspan class="lime">once.</tspan></text>']
xs = [300, 800, 1300]
cy = 450
for a, c in zip(xs, xs[1:]):
    b.append(f'<path class="dash" d="M{a + 175} {cy}H{c - 175}"/>')
# 1: the link
b.append(panel(xs[0] - 175, cy - 150, 350, 300))
b.append(f'<rect x="{xs[0] - 125}" y="{cy - 40}" width="250" height="80" rx="16" fill="#f4f6ee"/>')
b.append(f'<text class="txt" x="{xs[0]}" y="{cy + 12}" font-size="28" font-weight="600" text-anchor="middle" style="fill:#000000">Get my Grok link</text>')
b.append(f'<text class="mono" x="{xs[0]}" y="{cy - 82}" font-size="22" text-anchor="middle" style="fill:rgb(244 246 238 / 0.38)">grokpad</text>')
b.append(f'<text class="mono lime" x="{xs[0]}" y="{cy + 100}" font-size="22" text-anchor="middle">/mcp/••••••••</text>')
# 2: Grok connectors
b.append(panel(xs[1] - 175, cy - 150, 350, 300))
b.append(f'<text class="mono" x="{xs[1] - 135}" y="{cy - 88}" font-size="22" style="fill:rgb(244 246 238 / 0.38)">Connectors</text>')
b.append(f'<rect x="{xs[1] - 135}" y="{cy - 56}" width="270" height="64" rx="12" fill="#121212" stroke="rgb(255 255 255 / 0.15)" stroke-width="2"/>')
b.append(f'<text class="mono lime" x="{xs[1] - 115}" y="{cy - 15}" font-size="21">https://…/mcp/•••</text>')
b.append(f'<rect x="{xs[1] - 135}" y="{cy + 30}" width="270" height="64" rx="12" fill="none" stroke="{LIME}" stroke-width="3"/>')
b.append(f'<text class="txt" x="{xs[1]}" y="{cy + 71}" font-size="26" font-weight="600" text-anchor="middle">+ Add Connector</text>')
# 3: launch free
b.append(panel(xs[2] - 175, cy - 150, 350, 300, lit=True))
b.append(f'<text class="mono" x="{xs[2]}" y="{cy - 82}" font-size="22" text-anchor="middle" style="fill:rgb(244 246 238 / 0.38)">launch cost</text>')
b.append(f'<text class="led lime glow" x="{xs[2]}" y="{cy + 30}" font-size="84" text-anchor="middle">FREE</text>')
b.append(f'<text class="mono" x="{xs[2]}" y="{cy + 98}" font-size="22" text-anchor="middle" style="fill:rgb(244 246 238 / 0.6)">nothing to deposit</text>')
steps = [('Get your link', 'one tap, no sign-up'), ('Add it to Grok', 'paste it in Connectors'), ('Launch free', 'no deposit, no wallet pop-ups')]
for x, (a, c) in zip(xs, steps):
    b.append(f'<text class="txt" x="{x}" y="{cy + 228}" font-size="36" font-weight="600" text-anchor="middle">{a}</text>')
    b.append(f'<text class="muted" x="{x}" y="{cy + 274}" font-size="27" text-anchor="middle">{c}</text>')
page('02-setup.html', 1600, 900, b)

# ---------------------------------------------------------------- 3 then ask 1600x900
b = ['<text class="disp" x="800" y="132" font-size="62" text-anchor="middle">Then just <tspan class="lime">ask.</tspan></text>']
px, py, pw, ph = 230, 210, 1140, 560
b.append(panel(px, py, pw, ph, 28))
lx = px + 60
b.append(f'<text class="mono" x="{lx}" y="{py + 80}" font-size="26" style="fill:rgb(244 246 238 / 0.38)">you</text>')
b.append(f'<text class="mono" x="{lx}" y="{py + 128}" font-size="31">launch a coin called Moon Cat, ticker MCAT,</text>')
b.append(f'<text class="mono" x="{lx}" y="{py + 172}" font-size="31">about a cat that lives on the moon</text>')
b.append(f'<text class="mono" x="{lx}" y="{py + 256}" font-size="26" style="fill:rgb(244 246 238 / 0.38)">grok</text>')
b.append(f'<text class="mono" x="{lx}" y="{py + 304}" font-size="31" font-weight="700">Moon Cat ($MCAT) is live</text>')
b.append(f'<text class="mono" x="{lx}" y="{py + 348}" font-size="31" style="fill:rgb(244 246 238 / 0.6)">Grokpad page: <tspan class="lime">grokpad.org/coins/7xKp…pump</tspan></text>')
b.append(f'<text class="mono" x="{lx}" y="{py + 392}" font-size="31" style="fill:rgb(244 246 238 / 0.6)">Contract address: <tspan style="fill:#f4f6ee">7xKp…pump</tspan></text>')
chips = ['“buy 0.1 SOL of $MCAT”', '“sell my MCAT”', '“withdraw to my wallet”']
cw = [360, 260, 380]
gap = 24
x = px + (pw - (sum(cw) + gap * 2)) / 2
for c, w in zip(chips, cw):
    b.append(f'<rect x="{x}" y="{py + 450}" width="{w}" height="64" rx="12" fill="#121212" stroke="rgb(255 255 255 / 0.15)" stroke-width="2"/>')
    b.append(f'<text class="mono" x="{x + w / 2}" y="{py + 491}" font-size="23" text-anchor="middle" style="fill:rgb(244 246 238 / 0.6)">{c}</text>')
    x += w + gap
b.append('<text class="dim" x="800" y="850" font-size="27" text-anchor="middle">No wallet pop-ups. No forms.</text>')
page('03-ask.html', 1600, 900, b)

# ---------------------------------------------------------------- 4 live, with its own page 1600x900
b = ['<text class="disp" x="800" y="132" font-size="62" text-anchor="middle">Live in seconds. <tspan class="lime">With its own page.</tspan></text>']
px, py, pw, ph = 200, 215, 1200, 520
b.append(panel(px, py, pw, ph, 28))
# address bar
b.append(f'<rect x="{px + 30}" y="{py + 28}" width="{pw - 60}" height="62" rx="12" fill="#121212" stroke="rgb(255 255 255 / 0.15)" stroke-width="2"/>')
b.append(f'<circle cx="{px + 64}" cy="{py + 59}" r="7" fill="{LIME}"/>')
b.append(f'<text class="mono" x="{px + 90}" y="{py + 68}" font-size="26"><tspan class="lime">grokpad.org</tspan><tspan style="fill:rgb(244 246 238 / 0.6)">/coins/7xKp…pump</tspan></text>')
# coin header
ax, ay = px + 120, py + 220
b.append(f'<circle cx="{ax}" cy="{ay}" r="74" fill="#0d1306" stroke="{LIME}" stroke-width="3"/>')
b.append(f'<circle cx="{ax}" cy="{ay}" r="120" fill="url(#glow)"/>')
b.append(f'<text class="led lime" x="{ax}" y="{ay + 18}" font-size="52" text-anchor="middle">MC</text>')
b.append(f'<text class="disp" x="{ax + 112}" y="{ay - 6}" font-size="58">Moon Cat</text>')
b.append(f'<text class="mono" x="{ax + 114}" y="{ay + 44}" font-size="28" style="fill:rgb(244 246 238 / 0.6)">$MCAT</text>')
b.append(f'<rect x="{ax + 250}" y="{ay + 16}" width="246" height="40" rx="6" fill="#0d1306" stroke="{LIME}" stroke-width="2"/>')
b.append(f'<circle cx="{ax + 274}" cy="{ay + 36}" r="6" fill="{LIME}"/>')
b.append(f'<text class="mono lime" x="{ax + 290}" y="{ay + 44}" font-size="20" font-weight="700">LIVE ON PUMP.FUN</text>')
# rows
rows = [('Contract address', '<tspan class="mono" style="fill:#f4f6ee">7xKp…pump</tspan>'),
        ('pump.fun website', '<tspan class="mono lime">this page</tspan>')]
ry = py + 380
for label, val in rows:
    b.append(f'<path d="M{px + 46} {ry - 44}H{px + pw - 46}" stroke="rgb(255 255 255 / 0.08)" stroke-width="2"/>')
    b.append(f'<text class="muted" x="{px + 46}" y="{ry}" font-size="28">{label}</text>')
    b.append(f'<text x="{px + pw - 46}" y="{ry}" font-size="28" text-anchor="end">{val}</text>')
    ry += 84
# launch cost tile on the right of the header
tx, ty = px + pw - 300, py + 140
b.append(panel(tx, ty, 254, 160, 16, lit=True))
b.append(f'<text class="mono" x="{tx + 127}" y="{ty + 46}" font-size="20" text-anchor="middle" style="fill:rgb(244 246 238 / 0.38)">launch cost</text>')
b.append(f'<text class="led lime glow" x="{tx + 127}" y="{ty + 118}" font-size="64" text-anchor="middle">FREE</text>')
b.append('<text class="dim" x="800" y="835" font-size="27" text-anchor="middle">Grok sends back the page and the contract address.</text>')
page('04-live.html', 1600, 900, b)

# ---------------------------------------------------------------- 5 close 1600x900
b = [lockup(800, 370, 300)]
b.append(f'<text class="mono lime" x="800" y="650" font-size="40" font-weight="500" text-anchor="middle">{URL}</text>')
b.append('<text class="muted" x="800" y="720" font-size="32" text-anchor="middle">Say it. It’s live.</text>')
page('05-close.html', 1600, 900, b)
print('built')
