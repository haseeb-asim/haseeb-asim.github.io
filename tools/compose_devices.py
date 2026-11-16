#!/usr/bin/env python3
"""Black-stage device composites for the designed products.

Web-first work uses the existing web screen inside a laptop and the first
phone screen beside it. The gray mat around those source files is cropped
away. Output matches the shipped composites: 1600x1200 and 960x720.
"""

import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "concepts" / "composites"
ORIGIN = "http://127.0.0.1:8765"

PAIRS = [
    ("fernly", "01-fernly", "web-1-agent-console.webp", "mobile-1-inbox.webp"),
    ("crewline", "02-crewline", "web-1-dispatch-board.webp", "mobile-1-customer-booking.webp"),
    ("mendwell", "03-mendwell", "web-1-provider-schedule.webp", "mobile-1-book-visit.webp"),
    ("repharbor", "04-repharbor", "web-1-clients.webp", "mobile-1-workout.webp"),
    ("quillmere", "05-quillmere", "web-1-pipeline.webp", "mobile-1-log-call.webp"),
    ("haverlet", "06-haverlet", "web-1-payments.webp", "mobile-1-pay-rent.webp"),
    ("ibidwell", "07-ibidwell", "web-1-ask.webp", "mobile-1-answer.webp"),
    ("toquelane", "08-toquelane", "web-1-kds.webp", "mobile-1-customize.webp"),
    ("holdlark", "09-holdlark", "web-1-overview.webp", "mobile-1-home.webp"),
    ("musterwick", "10-musterwick", "web-1-overview.webp", "mobile-1-discover.webp"),
]


def content_box(path):
    probe = subprocess.check_output(
        [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height", "-of", "csv=p=0", str(path),
        ],
        text=True,
    ).strip()
    width, height = map(int, probe.split(","))
    raw = subprocess.check_output(
        ["ffmpeg", "-v", "error", "-i", str(path), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    )
    bg = raw[0], raw[1], raw[2]
    minx, miny, maxx, maxy = width, height, 0, 0
    step = 2
    for y in range(0, height, step):
        row = y * width * 3
        for x in range(0, width, step):
            i = row + x * 3
            if abs(raw[i] - bg[0]) > 18 or abs(raw[i + 1] - bg[1]) > 18 or abs(raw[i + 2] - bg[2]) > 18:
                minx = min(minx, x)
                miny = min(miny, y)
                maxx = max(maxx, x)
                maxy = max(maxy, y)
    # Pull in a couple of pixels so the matte does not peek at the rounded corners.
    pad = 8
    return (
        width,
        height,
        minx + pad,
        miny + pad,
        max(1, maxx - minx - pad * 2),
        max(1, maxy - miny - pad * 2),
    )


def placed(src, box_w, img_w, img_h, x, y, cw, ch, radius):
    box_h = box_w * ch / cw
    disp_w = box_w * img_w / cw
    disp_h = box_h * img_h / ch
    left = -box_w * x / cw
    top = -box_h * y / ch
    return f"""<div class="clip" style="width:{box_w:.1f}px;height:{box_h:.1f}px;overflow:hidden;border-radius:{radius}px">
      <img src="{src}" alt="" style="width:{disp_w:.1f}px;height:{disp_h:.1f}px;margin:{top:.1f}px 0 0 {left:.1f}px;display:block">
    </div>"""


def html(web_src, phone_src, web_box, phone_box):
    ww, wh, wx, wy, wc, hc = web_box
    pw, ph, px, py, pc, hc_p = phone_box
    screen_w = 1000
    phone_w = 318
    screen = placed(web_src, screen_w, ww, wh, wx, wy, wc, hc, 2)
    phone = placed(phone_src, phone_w, pw, ph, px, py, pc, hc_p, 44)
    screen_h = screen_w * hc / wc
    laptop_h = 12 + screen_h + 26 + 16
    phone_h = phone_w * hc_p / pc
    group_w = (12 * 2 + screen_w) + phone_w - 96
    left = (1600 - group_w) / 2
    top = max(70, (1200 - max(laptop_h, phone_h + 30)) / 2)
    phone_left = left + 24 + screen_w - 96
    phone_top = top + laptop_h - phone_h + 18
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; width: 1600px; height: 1200px; background: #000; overflow: hidden; }}
  .stage {{ position: relative; width: 1600px; height: 1200px; background: #000; }}
  .laptop {{
    position: absolute;
    left: {left:.1f}px;
    top: {top:.1f}px;
    width: {screen_w + 24:.1f}px;
    filter: drop-shadow(0 26px 28px rgb(0 0 0 / 0.55));
  }}
  .lid {{
    background: linear-gradient(180deg, #e6e6e2, #c2c2be);
    border-radius: 16px 16px 4px 4px;
    padding: 12px 12px 0;
  }}
  .chin {{
    height: 26px;
    background: linear-gradient(180deg, #deded9, #b4b4b0);
    border-radius: 0 0 8px 8px;
    position: relative;
  }}
  .chin::after {{
    content: "";
    position: absolute;
    left: 50%;
    top: 8px;
    width: 78px;
    height: 5px;
    transform: translateX(-50%);
    border-radius: 4px;
    background: #8a8a86;
  }}
  .deck {{
    height: 16px;
    margin: 0 64px;
    background: linear-gradient(180deg, #f3f3ef, #c9c9c4);
    border-radius: 0 0 16px 16px;
  }}
  .phone {{
    position: absolute;
    left: {phone_left:.1f}px;
    top: {phone_top:.1f}px;
    z-index: 2;
    filter: drop-shadow(0 18px 22px rgb(0 0 0 / 0.6));
  }}
  .phone .clip {{ box-shadow: inset 0 0 0 3px #000; }}
</style>
</head>
<body>
  <div class="stage">
    <div class="laptop">
      <div class="lid">{screen}<div class="chin"></div></div>
      <div class="deck"></div>
    </div>
    <div class="phone">{phone}</div>
  </div>
</body>
</html>
"""


def encode(png, dest, width, height):
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(png),
            "-vf", f"scale={width}:{height}:flags=lanczos",
            "-c:v", "libwebp", "-quality", "80", "-compression_level", "6",
            str(dest),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main(only=None):
    OUT.mkdir(parents=True, exist_ok=True)
    pairs = [item for item in PAIRS if not only or item[0] in only]
    with sync_playwright() as play:
        browser = play.chromium.launch(
            executable_path="/usr/bin/google-chrome",
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        pg = browser.new_page(viewport={"width": 1600, "height": 1200}, device_scale_factor=1)
        for slug, folder, web_name, phone_name in pairs:
            web_path = ROOT / "assets" / "concepts" / folder / web_name
            phone_path = ROOT / "assets" / "concepts" / folder / phone_name
            web_box = content_box(web_path)
            phone_box = content_box(phone_path)
            web = f"{ORIGIN}/assets/concepts/{folder}/{web_name}"
            phone = f"{ORIGIN}/assets/concepts/{folder}/{phone_name}"
            pg.set_content(html(web, phone, web_box, phone_box), wait_until="networkidle")
            pg.evaluate("() => Promise.all([...document.images].map(img => img.decode().catch(() => {})))")
            png = OUT / f"{slug}.png"
            pg.screenshot(path=str(png), type="png")
            encode(png, OUT / f"{slug}.webp", 1600, 1200)
            encode(png, OUT / f"{slug}-sm.webp", 960, 720)
            png.unlink()
            full = (OUT / f"{slug}.webp").stat().st_size // 1024
            small = (OUT / f"{slug}-sm.webp").stat().st_size // 1024
            print(f"{slug}: {full} KB, sm {small} KB")
        browser.close()


if __name__ == "__main__":
    main(set(sys.argv[1:]) or None)
