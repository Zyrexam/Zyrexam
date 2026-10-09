"""Rebuild tech-stack.svg with official Devicon logo paths, our own tiles."""
import re, urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0"}

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
OUT = REPO / "assets" / "tech-stack.svg"
TMP = REPO / ".tmp-icons"

BASE = "https://raw.githubusercontent.com/devicons/devicon/master/icons"
ICONS = [
    ("java", f"{BASE}/java/java-original.svg", "Java", "rise", "d1", "sq"),
    ("python", f"{BASE}/python/python-original.svg", "Python", "tilt", "d2", "sq"),
    ("ts", f"{BASE}/typescript/typescript-original.svg", "TypeScript", "thump", "d3", "sq"),
    ("pg", f"{BASE}/postgresql/postgresql-original.svg", "PostgreSQL", "rise", "d4", "sq"),
    ("redis", f"{BASE}/redis/redis-original.svg", "Redis", "tilt", "d5", "sq"),
    ("aws", f"{BASE}/amazonwebservices/amazonwebservices-original-wordmark.svg", "AWS", "thump", "d1", "wide"),
    ("docker", f"{BASE}/docker/docker-original.svg", "Docker", "rise", "d2", "sq"),
    ("react", f"{BASE}/react/react-original.svg", "React", "tilt", "d3", "sq"),
    ("kafka", f"{BASE}/apachekafka/apachekafka-original.svg", "Kafka", "thump", "d4", "sq"),
]

def inner(svg_text, key):
    m = re.search(r"<svg[^>]*>(.*)</svg>", svg_text, re.S)
    body = m.group(1)
    body = re.sub(r'\bid="', f'id="{key}-', body)
    body = re.sub(r"url\(#", f"url(#{key}-", body)
    body = re.sub(r"href=\"#", f'href="#{key}-', body)
    if key == "aws":
        body = body.replace("<path ", '<path class="dark-aws" ', 1)
    if key == "kafka":
        body = body.replace('fill="#231f20"/></', 'fill="#231f20" class="dark-kafka"/></')
    if key == "ts":
        body = body.replace('fill="#fff" d="M22.67 47h99.67v73.67H22.67z"',
                            'fill="#fff" class="dark-ts-bg" d="M22.67 47h99.67v73.67H22.67z"')
    return body.strip()

tiles = []
for i, (key, url, label, anim, delay, kind) in enumerate(ICONS):
    src = TMP / f"{key}.svg"
    if not src.exists():
        req = urllib.request.Request(url, headers=UA)
        TMP.mkdir(exist_ok=True)
        with urllib.request.urlopen(req, timeout=30) as r, open(src, "wb") as f:
            f.write(r.read())
    body = inner(src.read_text(encoding="utf-8"), key)
    if kind == "wide":
        logo = f'<g transform="translate(16 16) scale(0.53)">{body}</g>'
    else:
        logo = f'<g transform="translate(26 26) scale(0.375)">{body}</g>'
    tiles.append(
        f'  <g transform="translate({i * 100})">\n'
        f'    <rect class="tile" x="8" y="8" width="84" height="84" rx="22" filter="url(#soft)"/>\n'
        f'    <g class="{anim} {delay}">{logo}</g>\n'
        f'    <text class="label" x="50" y="118">{label}</text>\n'
        f"  </g>"
    )

svg = """<svg xmlns="http://www.w3.org/2000/svg" width="900" height="132" viewBox="0 0 900 132" role="img" aria-labelledby="title desc">
  <title id="title">Mohit Kumar technology stack</title>
  <desc id="desc">Official logos for Java, Python, TypeScript, PostgreSQL, Redis, AWS, Docker, React, and Kafka.</desc>
  <defs>
    <filter id="soft" x="-30%" y="-30%" width="160%" height="170%">
      <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#0D1117" flood-opacity=".16"/>
    </filter>
  </defs>
  <style>
    .tile { fill:#FFFFFF; stroke:#D8DEE4; stroke-width:1; }
    .label { fill:#57606A; font:700 11px Verdana, Geneva, DejaVu Sans, sans-serif; text-anchor:middle; letter-spacing:.2px; }
    .rise,.tilt,.thump { transform-box:fill-box; transform-origin:center; }
    .rise { animation:rise 3.2s ease-in-out infinite; }
    .tilt { animation:tilt 4s ease-in-out infinite; }
    .thump { animation:thump 3.8s ease-in-out infinite; }
    .d1 { animation-delay:-.5s; } .d2 { animation-delay:-1.2s; } .d3 { animation-delay:-1.9s; }
    .d4 { animation-delay:-2.6s; } .d5 { animation-delay:-3.1s; }
    @keyframes rise { 0%,100% { transform:translateY(3px); } 50% { transform:translateY(-4px); } }
    @keyframes tilt { 0%,100% { transform:rotate(-4deg); } 50% { transform:rotate(4deg); } }
    @keyframes thump { 0%,100% { transform:scale(.95); } 50% { transform:scale(1.06); } }
    @media (prefers-color-scheme:dark) {
      .tile { fill:#0D1117; stroke:#30363D; }
      .label { fill:#9BA3AB; }
      .dark-aws { fill:#EDEDED; }
      .dark-kafka { fill:#EDEDED; }
      .dark-ts-bg { fill:#0D1117; }
    }
    @media (prefers-reduced-motion:reduce) {
      .rise,.tilt,.thump { animation:none; }
    }
  </style>
""" + "\n".join(tiles) + "\n</svg>\n"

OUT.write_text(svg, encoding="utf-8")
print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")
