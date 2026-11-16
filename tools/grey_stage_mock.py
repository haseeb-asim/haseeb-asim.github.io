#!/usr/bin/env python3
"""Throwaway light-mode stage mock for the Crypto and fintech shelf.

Shipped composites have no separate screen sources, so the black matte is
flood-filled and replaced. Holdlark is re-rendered from its real screens.
"""

import subprocess
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from compose_devices import content_box, html  # noqa: E402
from playwright.sync_api import sync_playwright

OUT = ROOT / "assets" / "mock" / "grey-stage"
SHIPPED = ["keeper", "fantasy", "blob"]

# A shade or two under the page (#f4f4f2), warm.
CENTER = (234, 231, 224)  # #eae7e0
EDGE = (221, 217, 208)    # #ddd9d0


def load(path):
    probe = subprocess.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", str(path)],
        text=True,
    ).strip()
    width, height = map(int, probe.split(","))
    raw = bytearray(subprocess.check_output(
        ["ffmpeg", "-v", "error", "-i", str(path), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    ))
    return width, height, raw


def is_matte(raw, i, limit):
    o = i * 3
    r, g, b = raw[o], raw[o + 1], raw[o + 2]
    return r <= limit and g <= limit and b <= limit and abs(r - g) < 16 and abs(g - b) < 16


def background_mask(width, height, raw):
    count = width * height
    bg = bytearray(count)
    queue = deque()

    def seed(i):
        if not bg[i] and is_matte(raw, i, 16):
            bg[i] = 1
            queue.append(i)

    for x in range(width):
        seed(x)
        seed((height - 1) * width + x)
    for y in range(height):
        seed(y * width)
        seed(y * width + width - 1)
    while queue:
        i = queue.popleft()
        y, x = divmod(i, width)
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= nx < width and 0 <= ny < height:
                j = ny * width + nx
                if not bg[j] and is_matte(raw, j, 16):
                    bg[j] = 1
                    queue.append(j)
    fringe = []
    for i in range(count):
        if bg[i] or not is_matte(raw, i, 46):
            continue
        y, x = divmod(i, width)
        if ((x and bg[i - 1]) or (x + 1 < width and bg[i + 1])
                or (y and bg[i - width]) or (y + 1 < height and bg[i + width])):
            fringe.append(i)
    for i in fringe:
        bg[i] = 1
    return bg


def distance_to_device(width, height, bg, radius=20):
    dist = bytearray(width * height)
    for i, flag in enumerate(bg):
        dist[i] = 0 if not flag else 255
    current = bytearray(dist)
    for _ in range(radius):
        nxt = bytearray(current)
        for y in range(height):
            row = y * width
            for x in range(width):
                i = row + x
                best = current[i]
                if x and current[i - 1] < best:
                    best = current[i - 1]
                if x + 1 < width and current[i + 1] < best:
                    best = current[i + 1]
                if y and current[i - width] < best:
                    best = current[i - width]
                if y + 1 < height and current[i + width] < best:
                    best = current[i + width]
                if best < 255 and best + 1 < nxt[i]:
                    nxt[i] = best + 1
        current = nxt
    return current


def paint(width, height, raw, bg):
    dist = distance_to_device(width, height, bg)
    pix = bytearray(raw)
    radius = 20
    for y in range(height):
        ny = y / (height - 1) - 0.5
        for x in range(width):
            i = y * width + x
            if not bg[i]:
                continue
            nx = x / (width - 1) - 0.5
            t = min(1.0, (nx * nx * 1.2 + ny * ny) ** 0.5 / 0.7)
            r = CENTER[0] + (EDGE[0] - CENTER[0]) * t
            g = CENTER[1] + (EDGE[1] - CENTER[1]) * t
            b = CENTER[2] + (EDGE[2] - CENTER[2]) * t
            d = dist[i]
            if d < radius:
                k = (1 - d / radius) ** 2 * 0.14
                r *= 1 - k
                g *= 1 - k
                b *= 1 - k
            o = i * 3
            pix[o] = int(r)
            pix[o + 1] = int(g)
            pix[o + 2] = int(b)
    return pix


def write_pair(pix, width, height, stem):
    OUT.mkdir(parents=True, exist_ok=True)
    full = OUT / f"{stem}.webp"
    small = OUT / f"{stem}-sm.webp"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{width}x{height}",
         "-i", "-", "-c:v", "libwebp", "-quality", "86", "-compression_level", "6", str(full)],
        input=bytes(pix), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(full), "-vf", "scale=960:720:flags=lanczos",
         "-c:v", "libwebp", "-quality", "84", "-compression_level", "6", str(small)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    print(stem, full.stat().st_size // 1024, "KB")


def mask_shipped():
    for stem in SHIPPED:
        width, height, raw = load(ROOT / "assets" / "projects" / f"{stem}.webp")
        bg = background_mask(width, height, raw)
        print(stem, "matte", round(100 * sum(bg) / len(bg), 1), "%")
        write_pair(paint(width, height, raw, bg), width, height, stem)


def render_holdlark():
    folder = ROOT / "assets" / "concepts" / "09-holdlark"
    web_box = content_box(folder / "web-1-overview.webp")
    phone_box = content_box(folder / "mobile-1-home.webp")
    doc = html(
        "http://127.0.0.1:8765/assets/concepts/09-holdlark/web-1-overview.webp",
        "http://127.0.0.1:8765/assets/concepts/09-holdlark/mobile-1-home.webp",
        web_box, phone_box,
    )
    stage = "radial-gradient(ellipse at center, #eae7e0 0%, #ddd9d0 78%)"
    doc = doc.replace("background: #000", f"background: {stage}")
    doc = doc.replace("inset 0 0 0 3px #000", "inset 0 0 0 3px #ddd9d0")
    OUT.mkdir(parents=True, exist_ok=True)
    png = OUT / "holdlark.png"
    with sync_playwright() as play:
        browser = play.chromium.launch(
            executable_path="/usr/bin/google-chrome", headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        page = browser.new_page(viewport={"width": 1600, "height": 1200})
        page.set_content(doc, wait_until="networkidle")
        page.evaluate("() => Promise.all([...document.images].map(img => img.decode().catch(() => {})))")
        page.screenshot(path=str(png), type="png")
        browser.close()
    for name, size in (("holdlark.webp", "1600:1200"), ("holdlark-sm.webp", "960:720")):
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(png), "-vf", f"scale={size}:flags=lanczos",
             "-c:v", "libwebp", "-quality", "84", "-compression_level", "6", str(OUT / name)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    png.unlink()
    print("holdlark", (OUT / "holdlark.webp").stat().st_size // 1024, "KB")


if __name__ == "__main__":
    mask_shipped()
    render_holdlark()
