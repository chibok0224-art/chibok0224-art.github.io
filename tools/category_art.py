"""Generate the flat illustration used on each top-category card: static/img/cat/<slug>.svg

    python tools/category_art.py

To add art for a new category, add a palette to COLORS and an icon to ICONS.
Icons are SVG fragments on a 320x180 canvas using {ink} (dark) and {acc} (accent).
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "static" / "img" / "cat"

# slug: (background, background shapes, ink, accent)
COLORS = {
    "graphics-design": ("#fde8ef", "#fbd3e1", "#7a1f45", "#e8558c"),
    "programming-tech": ("#e6effd", "#d0e1fb", "#1d3b6e", "#3b7de0"),
    "online-marketing": ("#fff0dc", "#ffe1b8", "#7a4a0c", "#f29a1f"),
    "video-animation": ("#efe8fd", "#e0d3fb", "#3d2478", "#7c55e0"),
    "writing-translation": ("#e9f6ee", "#d3eedd", "#1f5a37", "#2f9e5e"),
    "music-audio": ("#fde9e6", "#fbd4ce", "#7a2a1f", "#e0604a"),
    "business": ("#e8f1f3", "#d2e5e9", "#1d4a55", "#2f8aa0"),
    "finance": ("#eef6e3", "#ddeec9", "#3b5a14", "#7cb33a"),
    "ai-services": ("#eaeafe", "#d6d6fc", "#2b2a78", "#5a57e6"),
    "lifestyle": ("#fdf1e6", "#fae0c8", "#74401a", "#e08a3c"),
    "consulting-services": ("#f1ecf7", "#e3d9ef", "#4a2e66", "#9360c4"),
    "data": ("#e6f5f7", "#cdebef", "#174f57", "#1f9aa8"),
    "photography": ("#f3efe9", "#e6ded2", "#4a3a28", "#a07c4e"),
}

ICONS = {
    # artboard with shapes and a swatch row
    "graphics-design": """
<rect x="100" y="36" width="120" height="96" rx="10" fill="#fff" stroke="{ink}" stroke-width="3"/>
<circle cx="138" cy="76" r="22" fill="{acc}"/>
<rect x="150" y="82" width="46" height="38" rx="4" fill="{ink}" opacity=".85"/>
<circle cx="136" cy="152" r="8" fill="{acc}"/><circle cx="160" cy="152" r="8" fill="{ink}"/>
<circle cx="184" cy="152" r="8" fill="#fff" stroke="{ink}" stroke-width="2.5"/>""",
    # code window
    "programming-tech": """
<rect x="80" y="38" width="160" height="104" rx="10" fill="#fff" stroke="{ink}" stroke-width="3"/>
<path d="M90 38h140a10 10 0 0 1 10 10v10H80V48a10 10 0 0 1 10-10z" fill="{ink}"/>
<circle cx="95" cy="48" r="3.5" fill="#fff"/><circle cx="107" cy="48" r="3.5" fill="#fff"/><circle cx="119" cy="48" r="3.5" fill="#fff"/>
<path d="M140 84l-18 16 18 16M180 84l18 16-18 16M166 78l-12 44" fill="none" stroke="{acc}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>""",
    # megaphone with sound arcs
    "online-marketing": """
<path d="M112 78L184 48v88l-72-30z" fill="{acc}"/>
<rect x="92" y="76" width="22" height="30" rx="5" fill="{ink}"/>
<rect x="112" y="104" width="13" height="30" rx="4" fill="{ink}"/>
<path d="M198 72q14 20 0 40M212 58q26 34 0 68" fill="none" stroke="{ink}" stroke-width="5" stroke-linecap="round"/>""",
    # video player
    "video-animation": """
<rect x="85" y="42" width="150" height="96" rx="12" fill="{ink}"/>
<path d="M148 66l34 22-34 22z" fill="#fff"/>
<rect x="100" y="122" width="120" height="5" rx="2.5" fill="#fff" opacity=".35"/>
<rect x="100" y="122" width="55" height="5" rx="2.5" fill="{acc}"/>
<circle cx="155" cy="124.5" r="5" fill="#fff"/>""",
    # document with a pen
    "writing-translation": """
<rect x="106" y="32" width="100" height="122" rx="8" fill="#fff" stroke="{ink}" stroke-width="3"/>
<rect x="121" y="50" width="52" height="9" rx="4" fill="{acc}"/>
<rect x="121" y="70" width="70" height="6" rx="3" fill="{ink}" opacity=".3"/>
<rect x="121" y="84" width="62" height="6" rx="3" fill="{ink}" opacity=".3"/>
<rect x="121" y="98" width="70" height="6" rx="3" fill="{ink}" opacity=".3"/>
<rect x="121" y="112" width="44" height="6" rx="3" fill="{ink}" opacity=".3"/>
<g transform="rotate(35 222 100)"><rect x="215" y="52" width="14" height="72" rx="3" fill="{acc}"/>
<path d="M215 124h14l-7 15z" fill="{ink}"/></g>""",
    # headphones with a waveform
    "music-audio": """
<path d="M115 108V92a45 45 0 0 1 90 0v16" fill="none" stroke="{ink}" stroke-width="10" stroke-linecap="round"/>
<rect x="101" y="98" width="28" height="44" rx="11" fill="{acc}"/>
<rect x="191" y="98" width="28" height="44" rx="11" fill="{acc}"/>
<rect x="141" y="108" width="7" height="22" rx="3.5" fill="{ink}"/>
<rect x="151" y="98" width="7" height="42" rx="3.5" fill="{ink}"/>
<rect x="161" y="90" width="7" height="58" rx="3.5" fill="{ink}"/>
<rect x="171" y="104" width="7" height="30" rx="3.5" fill="{ink}"/>""",
    # briefcase
    "business": """
<path d="M140 66V54a7 7 0 0 1 7-7h26a7 7 0 0 1 7 7v12" fill="none" stroke="{ink}" stroke-width="7"/>
<rect x="98" y="64" width="124" height="82" rx="10" fill="{ink}"/>
<rect x="98" y="96" width="124" height="7" fill="{acc}"/>
<rect x="151" y="90" width="18" height="18" rx="3" fill="{acc}" stroke="#fff" stroke-width="2"/>""",
    # coin stacks and a rising line
    "finance": """
<ellipse cx="130" cy="140" rx="30" ry="9" fill="{acc}" stroke="{ink}" stroke-width="2.5"/>
<ellipse cx="130" cy="128" rx="30" ry="9" fill="{acc}" stroke="{ink}" stroke-width="2.5"/>
<ellipse cx="130" cy="116" rx="30" ry="9" fill="{acc}" stroke="{ink}" stroke-width="2.5"/>
<ellipse cx="188" cy="140" rx="30" ry="9" fill="{acc}" stroke="{ink}" stroke-width="2.5"/>
<ellipse cx="188" cy="128" rx="30" ry="9" fill="{acc}" stroke="{ink}" stroke-width="2.5"/>
<polyline points="98,78 134,58 164,68 214,36" fill="none" stroke="{ink}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M220 32l-17 1 10 13z" fill="{ink}"/>""",
    # chip with a sparkle
    "ai-services": """
<g stroke="{ink}" stroke-width="4" stroke-linecap="round">
<path d="M108 68h12M108 84h12M108 100h12M108 116h12M200 68h12M200 84h12M200 100h12M200 116h12"/>
<path d="M136 38v12M152 38v12M168 38v12M184 38v12M136 134v12M152 134v12M168 134v12M184 134v12"/></g>
<rect x="120" y="50" width="80" height="84" rx="12" fill="{ink}"/>
<rect x="136" y="66" width="48" height="52" rx="7" fill="{acc}"/>
<text x="160" y="100" text-anchor="middle" font-family="system-ui,Segoe UI,sans-serif" font-size="20" font-weight="800" fill="#fff">AI</text>
<path d="M232 28q3 13 16 16q-13 3-16 16q-3-13-16-16q13-3 16-16z" fill="{acc}"/>""",
    # potted plant and a heart
    "lifestyle": """
<path d="M160 118V84" stroke="{ink}" stroke-width="4"/>
<ellipse cx="146" cy="92" rx="12" ry="26" transform="rotate(-32 146 92)" fill="{ink}"/>
<ellipse cx="174" cy="92" rx="12" ry="26" transform="rotate(32 174 92)" fill="{ink}"/>
<ellipse cx="160" cy="72" rx="11" ry="27" fill="{ink}" opacity=".75"/>
<path d="M134 116h52l-7 34h-38z" fill="{acc}"/>
<path d="M226 72l-15-15a9 9 0 0 1 15-11a9 9 0 0 1 15 11z" fill="{acc}"/>""",
    # two speech bubbles
    "consulting-services": """
<rect x="84" y="40" width="104" height="62" rx="15" fill="{ink}"/>
<path d="M104 100v18l18-18z" fill="{ink}"/>
<circle cx="116" cy="71" r="6" fill="#fff"/><circle cx="136" cy="71" r="6" fill="#fff"/><circle cx="156" cy="71" r="6" fill="#fff"/>
<rect x="148" y="84" width="92" height="54" rx="15" fill="{acc}"/>
<path d="M220 136v16l-17-16z" fill="{acc}"/>
<rect x="163" y="101" width="60" height="6" rx="3" fill="#fff"/>
<rect x="163" y="115" width="42" height="6" rx="3" fill="#fff"/>""",
    # bar chart and a database
    "data": """
<rect x="92" y="100" width="22" height="42" rx="4" fill="{ink}" opacity=".55"/>
<rect x="120" y="78" width="22" height="64" rx="4" fill="{ink}" opacity=".8"/>
<rect x="148" y="56" width="22" height="86" rx="4" fill="{ink}"/>
<rect x="84" y="142" width="96" height="4" rx="2" fill="{ink}"/>
<path d="M186 64v64a26 9 0 0 0 52 0V64z" fill="{acc}"/>
<ellipse cx="212" cy="64" rx="26" ry="9" fill="{ink}" opacity=".85"/>
<path d="M186 86a26 9 0 0 0 52 0M186 108a26 9 0 0 0 52 0" fill="none" stroke="#fff" stroke-width="3"/>""",
    # camera
    "photography": """
<rect x="132" y="46" width="42" height="20" rx="6" fill="{ink}"/>
<rect x="94" y="60" width="132" height="82" rx="14" fill="{ink}"/>
<circle cx="160" cy="101" r="29" fill="#fff"/>
<circle cx="160" cy="101" r="21" fill="{acc}"/>
<circle cx="160" cy="101" r="8" fill="{ink}"/>
<rect x="198" y="72" width="16" height="8" rx="2" fill="{acc}"/>""",
}

TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" role="img" aria-hidden="true">
<rect width="320" height="180" fill="{bg}"/>
<circle cx="276" cy="24" r="62" fill="{bg2}"/>
<circle cx="30" cy="172" r="54" fill="{bg2}"/>
{icon}
</svg>
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, (bg, bg2, ink, acc) in COLORS.items():
        icon = ICONS[slug].strip().replace("{ink}", ink).replace("{acc}", acc)
        (OUT / f"{slug}.svg").write_text(TEMPLATE.format(bg=bg, bg2=bg2, icon=icon), encoding="utf-8")
    print(f"wrote {len(COLORS)} images to {OUT}")


if __name__ == "__main__":
    main()
