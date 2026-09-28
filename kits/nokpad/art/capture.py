"""Shoots the real NOKPAD phone in the states the article shows. Needs the site running (npm run dev +
npm run server in nokia-phone). The PNGs it writes are kept in art/, so gen.py rebuilds without it."""
import sys
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:5233/'
HIDE = '''body{background:transparent!important}
.ticker,.panel,.hint,footer,.mute{visibility:hidden!important}
.phone{filter:none!important}'''


def shoot(page, name):
    page.wait_for_timeout(350)
    page.locator('.phone').screenshot(path=f'phone-{name}.png', omit_background=True)
    print(name)


def taps(page, seq, gap=90, pause=1300):
    """Multi-tap text: seq like '22 777 444' — groups of the same key, a pause between letters."""
    for group in seq.split(' '):
        for ch in group:
            page.keyboard.press(ch)
            page.wait_for_timeout(gap)
        page.wait_for_timeout(pause)


with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome')
    page = b.new_page(viewport={'width': 1600, 'height': 1300}, device_scale_factor=3)
    page.goto(URL)
    page.add_style_tag(content=HIDE)
    page.wait_for_timeout(4500)
    shoot(page, 'standby')
    page.keyboard.press('Enter')
    shoot(page, 'menu')
    page.keyboard.press('Enter')  # New coin
    page.wait_for_timeout(500)
    # "BRICK" then one tap into the next letter, so the multi-tap highlight shows
    taps(page, '22 777 444 222 55')
    page.keyboard.press('0'); page.wait_for_timeout(1300)
    for ch in '222':
        page.keyboard.press(ch); page.wait_for_timeout(90)
    shoot(page, 'typing')
    page.wait_for_timeout(1300)
    taps(page, '666 444 66')
    page.keyboard.press('Enter')  # name -> ticker (suggested)
    page.wait_for_timeout(500)
    shoot(page, 'ticker')
    page.keyboard.press('Enter')  # ticker -> about
    page.wait_for_timeout(400)
    page.keyboard.press('Enter')  # skip about -> logo
    page.wait_for_timeout(1200)
    shoot(page, 'logo')
    page.keyboard.press('Enter')  # auto logo -> checking -> rewards
    page.wait_for_selector('text=Holder rewards', timeout=60000)
    shoot(page, 'rewards')
    page.keyboard.press('Enter')
    page.wait_for_selector('text=Send?', timeout=10000)
    shoot(page, 'review')

    # the incoming-call screen, from the made-up ?demo events
    page.goto(URL + '?demo')
    page.add_style_tag(content=HIDE)
    page.wait_for_selector('.phone.ringing', timeout=30000)
    page.wait_for_timeout(600)
    page.evaluate("document.querySelector('.phone').style.animation='none'")
    shoot(page, 'call')
    b.close()
