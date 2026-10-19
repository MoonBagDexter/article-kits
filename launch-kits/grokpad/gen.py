"""Builds docs/grokpad-launch-kit/index.html: the Grokpad launch pack page.

    python3 launch-kits/grokpad/gen.py docs/grokpad-launch-kit/index.html

Tone (owner, 2026-10-19): lead with "just ask Grok". Free is not the pitch, no dev details, one version of each line.
"""
import html, sys
OUT = sys.argv[1]
CA = "CvUfTWZG9cyFy2cQdK6TGypxAYu1LuEu2MgunrKzpump"
TICK = "GROKPAD"
def e(s): return html.escape(s, quote=True)
def xlen(s):  # X counts a link as 23
    return len(s) - s.count("grokpad.org") * len("grokpad.org") + s.count("grokpad.org") * 23
def text(label, body, count=None, note=None):
    c = f' <span class="n">{count}</span>' if count else ""
    nt = f'<p class="hint">{e(note)}</p>' if note else ""
    return f'<div class="block"><div class="lab">{e(label)}{c}</div><div class="card"><pre>{e(body)}</pre><button data-t="{e(body)}">Copy</button></div>{nt}</div>'
def img(src, cap, size, wide=False, checker=False):
    cls = "fig wide" if wide else "fig"
    bg = " chk" if checker else ""
    return f'<figure class="{cls}"><div class="well{bg}"><img src="img/{src}" alt="{e(cap)}" loading="lazy"></div><figcaption><span>{e(cap)}<em>{size}</em></span><span class="acts"><button data-i="img/{src}">Copy</button><a href="img/{src}" download>Download</a></span></figcaption></figure>'

bio = f"Launch coins by asking Grok.\nSay the name and ticker. It's live on pump.fun in seconds.\n\nCA: {CA}"
desc = f"Launch coins by asking Grok. Say the name and ticker, and it's live on pump.fun in seconds. ${TICK}"
tweet = f"Grok launches coins now.\n\nAdd Grokpad to Grok, say \"launch a coin called ___, ticker ___\", and it's live on pump.fun in seconds.\n\nJust ask Grok.\n\ngrokpad.org\n\nCA: {CA}"
qt = f"Grok got connectors. We built the one that launches coins.\n\nAdd Grokpad, tell Grok the name and ticker, and it's live on pump.fun in seconds.\n\ngrokpad.org\n\nCA: {CA}"
CAL = 44  # real CA length; counts below assume the real address is pasted in
def cnt(s, lim, x=False):
    n = (xlen(s) if x else len(s)) + ((CAL - len(CA)) if CA in s else 0)
    return f"{n}/{lim}"

parts = []
parts.append(f'''<section><h2>Launch video</h2><p class="sub">Post this with the launch tweet. 1920×1080, 60 fps, 19 seconds.</p>
<div class="vid"><video src="grokpad-launch-video.mp4" controls playsinline preload="metadata" poster="img/grokpad-x-header.png"></video>
<div class="vbar"><span>grokpad-launch-video.mp4<em>1080p · 60 fps · 9.4 MB</em></span><a href="grokpad-launch-video.mp4" download>Download</a></div></div></section>''')
parts.append('<section><h2>Launch tweet</h2><p class="sub">Attach the video. Grok is written without the @ on purpose: tagging @grok in a post can get a public reply from Grok.</p>'
  + text("Main post", tweet, cnt(tweet, 280, True))
  + text("Optional quote post", qt, cnt(qt, 280, True), "Quote this post: x.com/0x_kaize/status/2111528527078326732 (the Grok Bot connectors news).")
  + '</section>')
parts.append('<section><h2>X article</h2><p class="sub">Post it the same day. The article has its own page with a Copy button for every block, in paste order.</p>'
  + '<a class="art" href="../grokpad/" target="_blank"><img src="../grokpad/01-cover.png" alt="Launch coins. Just ask Grok." loading="lazy"><span><b>Launch coins. Just ask Grok.</b><em>Open the article kit →</em></span></a>'
  + '</section>')
parts.append('<section><h2>X profile</h2>'
  + text("Bio", bio, cnt(bio, 160))
  + text("Website", "https://grokpad.org")
  + '<div class="grid">' + img("grokpad-x-header.png", "Header", "1500×500", wide=True) + img("grokpad-pfp.png", "Profile picture", "1024×1024") + '</div>'
  + '</section>')
parts.append('<section><h2>Coin on pump.fun</h2><p class="sub">The description also goes in DEX Screener\'s token info.</p>'
  + '<div class="pair">' + text("Name", "Grokpad") + text("Ticker", TICK, note="Type it without the $.") + '</div>'
  + text("Description", desc, cnt(desc, 500))
  + text("Website", "https://grokpad.org")
  + '<div class="grid">' + img("grokpad-pfp.png", "Coin image", "1024×1024") + '</div>'
  + '</section>')
parts.append('<section><h2>Logos</h2><p class="sub">Transparent PNGs, for posts and graphics. Keep them on black.</p><div class="grid">'
  + img("grokpad-lockup.png", "Logo + name", "1511×406", wide=True, checker=True)
  + img("grokpad-logo-transparent.png", "Logo, transparent", "1024×1024", checker=True)
  + img("grokpad-wordmark.png", "Name only", "1600×406", checker=True)
  + '</div></section>')

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>Grokpad launch kit</title><link rel="icon" href="img/grokpad-pfp.png">
<meta property="og:title" content="Grokpad launch kit"><meta property="og:description" content="Video, banner, logos and copy for the Grokpad launch.">
<meta property="og:image" content="https://moonbagdexter.github.io/article-kits/grokpad-launch-kit/img/grokpad-x-header.png"><meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Urbanist:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
:root{{--bg:#000;--panel:#0a0a0a;--panel2:#121212;--line:rgba(255,255,255,.08);--line2:rgba(255,255,255,.15);--text:#f4f6ee;--muted:rgba(244,246,238,.62);--faint:rgba(244,246,238,.38);--lime:#a6ec0d;--hot:#d1fa2b}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--text);font:16px/1.5 Urbanist,system-ui,sans-serif;-webkit-font-smoothing:antialiased;background-image:radial-gradient(rgba(255,255,255,.075) 1px,transparent 1px);background-size:22px 22px}}
.wrap{{max-width:980px;margin:0 auto;padding:28px 16px 90px}}
header{{display:flex;align-items:center;gap:14px;margin-bottom:6px}}header img{{height:44px;width:auto}}
h1{{font-size:clamp(30px,6vw,46px);letter-spacing:-.03em;margin:18px 0 6px;font-weight:700}}h1 span{{color:var(--lime)}}
.intro{{color:var(--muted);margin:0 0 14px;max-width:640px}}
.note{{border:1px solid var(--line2);background:var(--panel);border-radius:12px;padding:12px 14px;font-size:14px;color:var(--muted)}}.note b{{color:var(--text)}}.note code{{color:var(--lime)}}
section{{margin-top:44px;padding-top:26px;border-top:1px solid var(--line)}}
h2{{font-size:26px;letter-spacing:-.03em;margin:0 0 4px}}.sub{{color:var(--muted);margin:0 0 16px;font-size:15px}}
.block{{margin:14px 0}}.lab{{font:600 11px/1 "JetBrains Mono",monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);margin-bottom:7px}}.lab .n{{color:var(--lime);margin-left:6px}}
.card{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:14px 16px;display:flex;gap:14px;align-items:flex-start}}
pre{{flex:1;min-width:0;margin:0;white-space:pre-wrap;overflow-wrap:anywhere;font:16px/1.55 Urbanist,system-ui,sans-serif}}
.hint{{color:var(--faint);font-size:13px;margin:6px 2px 0}}
button,a[download]{{appearance:none;flex:none;cursor:pointer;font:600 13px Urbanist,system-ui,sans-serif;border-radius:8px;padding:8px 14px;text-decoration:none;border:1px solid var(--line2);background:var(--panel2);color:var(--text);white-space:nowrap}}
.card button{{background:var(--text);color:#000;border-color:var(--text)}}
a[download]{{background:var(--lime);color:#000;border-color:var(--lime)}}button:hover,a[download]:hover{{filter:brightness(1.1)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;margin:14px 0}}.wide{{grid-column:1/-1}}
.fig{{margin:0;background:var(--panel);border:1px solid var(--line);border-radius:14px;overflow:hidden}}
.well{{background:#000;display:flex;align-items:center;justify-content:center;padding:0}}.well img{{display:block;width:100%;height:auto;max-height:420px;object-fit:contain}}
.chk{{padding:22px}}
figcaption{{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:10px 12px;border-top:1px solid var(--line);font-weight:600;font-size:14px;flex-wrap:wrap}}
figcaption em,.vbar em{{font:400 12px "JetBrains Mono",monospace;font-style:normal;color:var(--faint);margin-left:8px}}.acts{{display:flex;gap:8px}}
.vid{{background:var(--panel);border:1px solid var(--line);border-radius:14px;overflow:hidden}}video{{display:block;width:100%;background:#000;aspect-ratio:16/9}}
.vbar{{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:10px 12px;border-top:1px solid var(--line);font-weight:600;font-size:14px;flex-wrap:wrap}}
.art{{display:block;background:var(--panel);border:1px solid var(--line);border-radius:14px;overflow:hidden;color:var(--text);text-decoration:none}}.art img{{display:block;width:100%;height:auto}}.art span{{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:12px 14px;border-top:1px solid var(--line);flex-wrap:wrap}}.art em{{font-style:normal;color:var(--lime);font-weight:600;font-size:14px}}.art:hover{{border-color:var(--line2)}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:0 12px}}@media(max-width:560px){{.art{{display:block;background:var(--panel);border:1px solid var(--line);border-radius:14px;overflow:hidden;color:var(--text);text-decoration:none}}.art img{{display:block;width:100%;height:auto}}.art span{{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:12px 14px;border-top:1px solid var(--line);flex-wrap:wrap}}.art em{{font-style:normal;color:var(--lime);font-weight:600;font-size:14px}}.art:hover{{border-color:var(--line2)}}
.pair{{grid-template-columns:1fr}}.card{{flex-direction:column}}.card button{{align-self:flex-start}}}}
details{{margin-top:10px}}summary{{cursor:pointer;color:var(--muted);font-weight:600;font-size:14px}}
footer{{margin-top:56px;color:var(--faint);font-size:13px}}footer a{{color:var(--muted)}}
</style></head><body><div class="wrap">
<header><img src="img/grokpad-lockup.png" alt="Grokpad"></header>
<h1>Launch kit. <span>Copy, paste, post.</span></h1>
<p class="intro">Everything for launch day in one place: the video, the launch tweet, the X article, the X profile, the pump.fun listing and the logos. <b>Copy</b> puts it on your clipboard. <b>Download</b> saves the full-quality file.</p>
<p class="note"><b>CA</b> <code>{CA}</code> <button data-t="{CA}" style="margin-left:6px;padding:4px 10px">Copy</button><br>Already filled into every post below.</p>
{"".join(parts)}
<footer>Site: <a href="https://grokpad.org" target="_blank">grokpad.org</a></footer>
</div>
<script>
const flash=(b,t)=>{{const o=b.textContent;b.textContent=t;setTimeout(()=>b.textContent=o,1400)}};
function copyText(t){{if(navigator.clipboard&&window.isSecureContext)return navigator.clipboard.writeText(t);const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();document.execCommand('copy');a.remove();return Promise.resolve()}}
document.addEventListener('click',async e=>{{const b=e.target.closest('button');if(!b)return;
 if(b.dataset.t!=null){{copyText(b.dataset.t).then(()=>flash(b,'Copied'),()=>flash(b,'Failed'))}}
 if(b.dataset.i){{try{{await navigator.clipboard.write([new ClipboardItem({{'image/png':fetch(b.dataset.i).then(r=>r.blob())}})]);flash(b,'Copied')}}catch(err){{flash(b,'Use Download')}}}}}});
</script></body></html>'''
open(OUT, "w").write(page)
print("ok", cnt(bio,160), cnt(tweet,280,True), cnt(qt,280,True), cnt(desc,500))
