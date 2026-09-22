H = '<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css"></head><body>'
F = '</body></html>'


def svg(w, h, body):
    return H + f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>' + F


def save(name, w, h, parts):
    open(name, 'w', encoding='utf-8').write(svg(w, h, ''.join(parts)))




def mountain(x, base, cols=(18, 36, 54, 90, 72, 36, 54, 36, 18), cw=18):
    return ''.join(f'<rect class="w" x="{x + i * cw}" y="{base - h}" width="{cw}" height="{h}"/>' for i, h in enumerate(cols))


def sparkle(cx, cy, s):
    # pixel four-point star: fat core, thin arms
    out = [f'<rect class="w" x="{cx - s}" y="{cy - s}" width="{2 * s}" height="{2 * s}"/>']
    out.append(f'<rect class="w" x="{cx - s / 2}" y="{cy - 3 * s}" width="{s}" height="{6 * s}"/>')
    out.append(f'<rect class="w" x="{cx - 3 * s}" y="{cy - s / 2}" width="{6 * s}" height="{s}"/>')
    return ''.join(out)

MOUNTAIN = 'h{w} v-18 h-18 v-18 h-18 v-18 h-18 v18 h-18 v-36 h-18 v-18 h-18 v36 h-18 v18 h-{r} z'

# 1 header 2000x800: wordmark + hourglass
wm_h = 500; wm_w = round(1242 * wm_h / 613); lg_h = 540; lg_w = round(434 * lg_h / 715); gap = 140
x0 = (2000 - (wm_w + gap + lg_w)) // 2
save('01-header.html', 2000, 800, [
    f'<image href="wordmark-crop.png" x="{x0}" y="{(800 - wm_h) // 2}" width="{wm_w}" height="{wm_h}"/>',
    f'<image href="logo-crop.png" x="{x0 + wm_w + gap}" y="{(800 - lg_h) // 2}" width="{lg_w}" height="{lg_h}"/>',
])

# 2 device: the file stays, only the fingerprint leaves
b = []
b.append('<rect class="l" x="250" y="110" width="360" height="680"/>')
b.append('<line class="l" x1="390" y1="145" x2="470" y2="145"/>')
b.append('<path class="l" d="M330 200 H480 L530 250 V440 H330 Z"/><path class="l" d="M480 200 V250 H530"/>')
b.append(mountain(349, 422))
b.append('<rect class="w" x="468" y="285" width="22" height="22"/>')
for y in (478, 506, 534):
    b.append(f'<rect class="w" x="425" y="{y}" width="10" height="10"/>')
for i, t in enumerate(['3f a9 0c e1', '7b 2d 4f c8', '91 e0 5a 6c']):
    b.append(f'<text class="t" x="430" y="{610 + i * 46}" font-size="32" text-anchor="middle">{t}</text>')
b.append('<text class="dim" x="430" y="840" font-size="32" text-anchor="middle">your device</text>')
b.append('<text class="dim" x="645" y="330" font-size="32">&#8592; the file stays here</text>')
b.append('<line class="d" x1="640" y1="656" x2="1170" y2="656"/>')
b.append('<path class="w" d="M1170 638 l30 18 l-30 18 z"/>')
b.append('<text class="t" x="905" y="618" font-size="34" text-anchor="middle">3f a9 0c e1 … 6c b2</text>')
b.append('<text class="dim" x="905" y="712" font-size="32" text-anchor="middle">only the fingerprint leaves</text>')
b.append('<line class="l" x1="1290" y1="480" x2="1290" y2="560"/>')
b.append('<rect class="y" x="1235" y="560" width="110" height="190"/>')
b.append('<text class="dim" x="1290" y="450" font-size="32" text-anchor="middle">zcash</text>')
save('02-device.html', 1600, 900, b)

# 3 merkle tree, redrawn crisp at 16:9
b = []
xs = [360 + i * (880 / 7) for i in range(8)]
top = 170; r = 27; step = 80
for x in xs:
    b.append(f'<circle class="l" cx="{x:.1f}" cy="{top}" r="{r}"/>')
y = top + r + 25
lvl = xs
while len(lvl) > 1:
    nxt = []
    for i in range(0, len(lvl), 2):
        a, c = lvl[i], lvl[i + 1]
        b.append(f'<path class="l" d="M{a:.1f} {y} V{y + step} H{c:.1f} V{y}"/>')
        nxt.append((a + c) / 2)
    y += step
    lvl = nxt
    if len(lvl) > 1:
        # stems from each join down; next bracket's verticals start where they end
        y_next = y + step
        for m in lvl:
            b.append(f'<line class="l" x1="{m:.1f}" y1="{y}" x2="{m:.1f}" y2="{y_next}"/>')
        y = y_next
m = lvl[0]
b.append(f'<line class="l" x1="{m:.1f}" y1="{y}" x2="{m:.1f}" y2="{y + 50}"/>')
b.append(f'<rect class="y" x="{m - 40:.1f}" y="{y + 50}" width="80" height="120"/>')
save('03-tree.html', 1600, 900, b)

# 4 the block that holds the first anchor
b = []
bw = 170; gap = 70; n = 5; total = n * bw + (n - 1) * gap; x0 = (1600 - total) // 2; yb = 300
heights = ['3,490,639', '3,490,640', '3,490,641', '3,490,642', '3,490,643']
mid = yb + bw // 2
b.append(f'<line class="d" x1="0" y1="{mid}" x2="{x0 - 20}" y2="{mid}"/>')
b.append(f'<line class="d" x1="{x0 + total + 20}" y1="{mid}" x2="1600" y2="{mid}"/>')
for i in range(n):
    x = x0 + i * (bw + gap)
    if i == 2:
        b.append(f'<rect class="y" x="{x}" y="{yb}" width="{bw}" height="{bw}"/>')
        b.append(f'<text class="t" x="{x + bw / 2}" y="{yb - 44}" font-size="34" font-weight="500" text-anchor="middle">{heights[i]}</text>')
    else:
        b.append(f'<rect class="l" x="{x + 3.5}" y="{yb + 3.5}" width="{bw - 7}" height="{bw - 7}"/>')
        b.append(f'<text class="dim" x="{x + bw / 2}" y="{yb - 44}" font-size="32" text-anchor="middle">{heights[i]}</text>')
    if i < n - 1:
        b.append(f'<line class="l" x1="{x + bw}" y1="{mid}" x2="{x + bw + gap}" y2="{mid}"/>')
cx = x0 + 2 * (bw + gap) + bw / 2
b.append(f'<line class="l" x1="{cx}" y1="{yb + bw}" x2="{cx}" y2="{yb + bw + 80}"/>')
b.append(f'<text class="t" x="{cx}" y="{yb + bw + 135}" font-size="30" text-anchor="middle">root 1306edaa … bd0a20</text>')
b.append(f'<text class="dim" x="{cx}" y="{yb + bw + 190}" font-size="32" text-anchor="middle">tx 48941a82 … bdb4a9  ·  fee 15,000 zats</text>')
save('04-chain.html', 1600, 900, b)

# 5 timeline: a new model can't reach back into an old block
b = []
ty = 560
years = {2026: 300, 2027: 600, 2028: 900, 2029: 1200}
b.append(f'<line class="l" x1="160" y1="{ty}" x2="1440" y2="{ty}"/>')
b.append(f'<path class="w" d="M1440 {ty - 18} l32 18 l-32 18 z"/>')
for yr, x in years.items():
    b.append(f'<line class="l" x1="{x}" y1="{ty - 18}" x2="{x}" y2="{ty + 18}"/>')
    cls = 't' if yr in (2026, 2029) else 'dim'
    b.append(f'<text class="{cls}" x="{x}" y="{ty + 74}" font-size="34" text-anchor="middle">{yr}</text>')
b.append('<rect class="l" x="210" y="220" width="180" height="140"/>')
b.append(mountain(219, 344))
b.append('<line class="l" x1="300" y1="360" x2="300" y2="400"/>')
b.append('<rect class="y" x="265" y="400" width="70" height="120"/>')
b.append('<text class="dim" x="300" y="690" font-size="32" text-anchor="middle">stamped</text>')
px, py, s = 1200, 290, 16
b.append(sparkle(px, py, s))
b.append(sparkle(px + 70, py - 60, 7))
b.append(f'<line class="l" x1="{px}" y1="{py + 70}" x2="{px}" y2="{ty - 18}"/>')
b.append('<text class="dim" x="1200" y="690" font-size="32" text-anchor="middle">new model</text>')
b.append('<line class="d" x1="1135" y1="290" x2="580" y2="290"/>')
cx, cy = 510, 290
b.append(f'<path class="l" d="M{cx - 28} {cy - 28} L{cx + 28} {cy + 28} M{cx + 28} {cy - 28} L{cx - 28} {cy + 28}"/>')
b.append('<text class="dim" x="855" y="250" font-size="32" text-anchor="middle">can&#8217;t reach back</text>')
save('05-timeline.html', 1600, 900, b)

# 6 closing: the hourglass
lh = 720; lw = round(434 * lh / 715)
save('06-logo.html', 1600, 900, [f'<image href="logo-crop.png" x="{(1600 - lw) // 2}" y="{(900 - lh) // 2}" width="{lw}" height="{lh}"/>'])
