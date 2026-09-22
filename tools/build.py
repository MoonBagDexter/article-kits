"""Builds the public site in docs/ from every kits/<slug>/article.json.

    python tools/build.py

Each article becomes docs/<slug>/index.html plus its pictures, and docs/index.html
lists them all, newest first. GitHub Pages serves docs/ as the live site.
"""
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://moonbagdexter.github.io/article-kits'
TEMPLATE = (ROOT / 'tools' / 'kit-template.html').read_text(encoding='utf-8')


def step(n, tag, inner, buttons):
    return (f'<div class="step"><div class="num">{n}</div><div class="card">'
            f'<div class="head"><span class="tag">{tag}</span><span class="sp"></span>{buttons}</div>{inner}</div></div>')


def meta(title, blurb, slug, cover):
    t, b = html.escape(title), html.escape(blurb)
    img = f'{SITE}/{slug}/{cover}'
    return (f'<meta name="description" content="{b}">'
            f'<meta property="og:title" content="{t}"><meta property="og:description" content="{b}">'
            f'<meta property="og:image" content="{img}"><meta name="twitter:card" content="summary_large_image">'
            f'<meta name="twitter:image" content="{img}">')


def build_kit(kit: Path):
    art = json.loads((kit / 'article.json').read_text(encoding='utf-8'))
    out = ROOT / 'docs' / kit.name
    out.mkdir(parents=True, exist_ok=True)

    steps = [step(1, 'Title', f'<div class="body title">{html.escape(art["title"])}</div>',
                  '<button onclick="copyText(this)">Copy</button>')]
    cover = None
    for n, part in enumerate(art['parts'], start=2):
        if part['type'] == 'text':
            steps.append(step(n, 'Text', f'<div class="body">{part["html"]}</div>',
                              '<button onclick="copyText(this)">Copy</button>'))
            continue
        name = part['file']
        shutil.copy2(kit / name, out / name)
        cover = cover or name
        hint = f'<div class="hint">{part["note"]}</div>' if part.get('note') else ''
        steps.append(step(n, 'Cover image' if n == 2 else 'Image', f'<img src="{name}" alt="">{hint}',
                          f'<a class="btn ghost" download="{name}" href="{name}">Download</a>'
                          '<button onclick="copyImage(this)">Copy image</button>'))

    page = (TEMPLATE.replace('%%PROJECT%%', html.escape(art['project']))
            .replace('%%META%%', meta(art['title'], art.get('blurb', ''), kit.name, cover))
            .replace('%%STEPS%%', ''.join(steps)))
    (out / 'index.html').write_text(page, encoding='utf-8')
    return {**art, 'slug': kit.name, 'cover': cover}


def build_index(arts):
    cards = ''.join(
        f'<a class="kit" href="{a["slug"]}/"><img src="{a["slug"]}/{a["cover"]}" alt="">'
        f'<div class="info"><div class="proj">{html.escape(a["project"])} · {a["date"]}</div>'
        f'<div class="t">{html.escape(a["title"])}</div></div></a>'
        for a in arts)
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>X article kits</title>
<style>
*{{box-sizing:border-box}}
body{{margin:0;background:#0b0b0c;color:#E7E9EA;font-family:Inter,"Segoe UI",system-ui,sans-serif;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:720px;margin:0 auto;padding:28px 16px 80px}}
h1{{font-size:20px;margin:0 0 6px}}
p{{color:#8b8f94;font-size:14px;line-height:1.5;margin:0 0 20px}}
.kit{{display:block;margin-top:16px;background:#141517;border:1px solid #26282c;border-radius:14px;overflow:hidden;color:inherit;text-decoration:none}}
.kit:hover{{border-color:#5a4a12}}
.kit img{{display:block;width:100%;aspect-ratio:5/2;object-fit:cover}}
.info{{padding:12px 16px 14px}}
.proj{{font:600 11px ui-monospace,monospace;letter-spacing:.06em;text-transform:uppercase;color:#8b8f94}}
.t{{font-size:18px;font-weight:800;margin-top:4px}}
</style></head><body><div class="wrap">
<h1>X article kits</h1>
<p>Open one, then copy each block into the X article editor, top to bottom.</p>
{cards}
</div></body></html>'''
    (ROOT / 'docs' / 'index.html').write_text(page, encoding='utf-8')


if __name__ == '__main__':
    arts = [build_kit(k) for k in sorted((ROOT / 'kits').iterdir()) if (k / 'article.json').exists()]
    arts.sort(key=lambda a: a['date'], reverse=True)
    build_index(arts)
    (ROOT / 'docs' / '.nojekyll').write_text('', encoding='utf-8')
    for a in arts:
        print(f'{SITE}/{a["slug"]}/')
