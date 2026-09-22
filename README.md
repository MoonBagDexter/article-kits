# X article kits

Copy-paste kits for X articles. Each one is a page with a Copy button per block, in paste order.

Live: https://moonbagdexter.github.io/article-kits/

- `kits/<slug>/article.json`: the title, text blocks and picture order
- `kits/<slug>/art/`: the pages the pictures are drawn from (`gen.py` writes them)
- `tools/render.py <slug>`: shoots `art/*.html` to PNGs at exact size with headless Chrome
- `tools/build.py`: builds `docs/`, which GitHub Pages serves

Made with the `x-article-kit` Claude skill.
