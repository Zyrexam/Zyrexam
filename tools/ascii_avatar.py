"""Convert an avatar portrait into Neofetch-compatible ASCII art."""
from collections import deque
import sys
from PIL import Image, ImageEnhance

CHARS = "@%#*+=-:. "  # dark -> dense, light -> sparse


def flood_white_bg(img, threshold=240):
    """Mark near-white pixels connected to image borders as background."""
    rgb = img.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    bg = [[False] * h for _ in range(w)]
    q = deque()

    def is_bg(r, g, b):
        return r > threshold and g > threshold and b > threshold

    for x in range(w):
        for y in (0, h - 1):
            if is_bg(*px[x, y]) and not bg[x][y]:
                bg[x][y] = True
                q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if is_bg(*px[x, y]) and not bg[x][y]:
                bg[x][y] = True
                q.append((x, y))

    while q:
        cx, cy = q.popleft()
        for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
            if 0 <= nx < w and 0 <= ny < h and not bg[nx][ny] and is_bg(*px[nx, ny]):
                bg[nx][ny] = True
                q.append((nx, ny))
    return bg


def render(path, rows=27, max_cols=46, gamma=0.75, contrast=1.05):
    """Render an image file into aspect-corrected ASCII art lines."""
    img = Image.open(path)
    w, h = img.size
    bg = flood_white_bg(img)

    xs = [x for x in range(w) for y in range(h) if not bg[x][y]]
    ys = [y for x in range(w) for y in range(h) if not bg[x][y]]
    x0, x1 = max(0, min(xs) - 2), min(w, max(xs) + 3)
    y0, y1 = max(0, min(ys) - 2), min(h, max(ys) + 3)

    bw, bh = x1 - x0, y1 - y0
    # Monospace glyphs at 13px are ~7.9px wide and 15px tall
    cols = min(max_cols, round((rows * 15 / 7.9) * (bw / bh)))

    mask = Image.new("L", (w, h), 255)
    mpx = mask.load()
    for x in range(w):
        for y in range(h):
            if bg[x][y]:
                mpx[x, y] = 0

    gray_fit = img.convert("L").crop((x0, y0, x1, y1)).resize((cols, rows), Image.LANCZOS)
    if contrast != 1.0:
        gray_fit = ImageEnhance.Contrast(gray_fit).enhance(contrast)
    mask_fit = mask.crop((x0, y0, x1, y1)).resize((cols, rows), Image.LANCZOS)

    n = len(CHARS) - 1
    gp = gray_fit.load()
    mp = mask_fit.load()
    lines = []
    for y in range(rows):
        row = []
        for x in range(cols):
            if mp[x, y] < 128:
                row.append(" ")
            else:
                v = (gp[x, y] / 255) ** gamma
                row.append(CHARS[min(n, int(v * n + 0.5))])
        lines.append("".join(row).rstrip())
    return "\n".join(lines).strip("\n")


if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else "assets/Mohit.jpg"
    r = int(sys.argv[2]) if len(sys.argv) > 2 else 27
    print(render(p, rows=r))
