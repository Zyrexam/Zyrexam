"""Rebuild assets/streak.svg from live streak-stats numbers, in repo theme."""
import os
import re
import html
from pathlib import Path

TOTAL = os.environ.get("TOTAL", "298").strip() or "298"
CURRENT = os.environ.get("CURRENT", "0").strip() or "0"
LONGEST = os.environ.get("LONGEST", "5").strip() or "5"

# Current/Longest may be "0" or "5" or "5 days" already.
def as_days(value: str) -> str:
    value = value.strip()
    if re.fullmatch(r"\d[\d,]*", value):
        return f"{value} day{'s' if value.strip(',') != '1' else ''}"
    return value

CURRENT_DAYS = as_days(CURRENT)
LONGEST_DAYS = as_days(LONGEST)

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="560" height="105" viewBox="0 0 900 170" role="img" aria-labelledby="title desc">
  <title id="title">Contribution streaks</title>
  <desc id="desc">Total contributions, current streak, and longest streak.</desc>
  <defs>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#22D3EE"/>
      <stop offset=".5" stop-color="#0891B2"/>
      <stop offset="1" stop-color="#7C3AED"/>
    </linearGradient>
    <linearGradient id="hot" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F59E0B"/>
      <stop offset="1" stop-color="#EF4444"/>
    </linearGradient>
    <filter id="card" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#0D1117" flood-opacity=".16"/>
    </filter>
  </defs>
  <style>
    .frame {{ fill:#FFFFFF; stroke:url(#edge); stroke-width:2; }}
    .inner {{ fill:none; stroke:#E6E9EF; stroke-width:1; }}
    .big {{ fill:#0D1117; font:800 44px Verdana, Geneva, DejaVu Sans, sans-serif; text-anchor:middle; }}
    .name {{ fill:#57606A; font:700 13px Verdana, Geneva, DejaVu Sans, sans-serif; text-anchor:middle; letter-spacing:1.4px; }}
    .range {{ fill:#8B949E; font:400 12px Verdana, Geneva, DejaVu Sans, sans-serif; text-anchor:middle; }}
    .pop {{ transform-box:fill-box; transform-origin:center; animation:pop 3.6s ease-in-out infinite; }}
    @keyframes pop {{ 0%,100% {{ transform:scale(.97); }} 50% {{ transform:scale(1.03); }} }}
    @media (prefers-color-scheme:dark) {{
      .frame {{ fill:#0D1117; }}
      .inner {{ stroke:#21262D; }}
      .big {{ fill:#F0F6FC; }}
      .name {{ fill:#9BA3AB; }}
      .range {{ fill:#6E7681; }}
    }}
    @media (prefers-reduced-motion:reduce) {{ .pop {{ animation:none; }} }}
  </style>

  <g filter="url(#card)">
    <rect class="frame" x="8" y="8" width="274" height="154" rx="22"/>
    <rect class="inner" x="16" y="16" width="258" height="138" rx="16"/>
    <text class="name" x="145" y="52">TOTAL</text>
    <text class="big pop" x="145" y="104">{html.escape(TOTAL)}</text>
    <text class="range" x="145" y="132">Contributions</text>
  </g>

  <g filter="url(#card)">
    <rect class="frame" x="313" y="8" width="274" height="154" rx="22"/>
    <rect class="inner" x="321" y="16" width="258" height="138" rx="16"/>
    <g transform="translate(450 30)">
      <path fill="url(#hot)" d="M0-12c1 4 4 6 4 10a4 4 0 0 1-8 0c0-1.4.5-2.6 1.2-3.6C-2  -3-1 0 0 1c-.3-2.5.6-5 2.4-6.6C2 -3.6 1.4-1.6 0 0c1.8-1.6 3-4 3-7 3 2.5 5 6 5 10a8 8 0 0 1-16 0C-8-3-4-8 0-12z"/>
    </g>
    <text class="name" x="450" y="72">CURRENT STREAK</text>
    <text class="big pop" x="450" y="116">{html.escape(CURRENT_DAYS)}</text>
    <text class="range" x="450" y="140">days in a row</text>
  </g>

  <g filter="url(#card)">
    <rect class="frame" x="618" y="8" width="274" height="154" rx="22"/>
    <rect class="inner" x="626" y="16" width="258" height="138" rx="16"/>
    <text class="name" x="755" y="52">LONGEST STREAK</text>
    <text class="big pop" x="755" y="104">{html.escape(LONGEST_DAYS)}</text>
    <text class="range" x="755" y="132">personal best</text>
  </g>
</svg>
"""

out = Path(__file__).resolve().parents[2] / "assets" / "streak.svg"
out.write_text(svg, encoding="utf-8")
print(f"Wrote {out} ({out.stat().st_size} bytes)")
