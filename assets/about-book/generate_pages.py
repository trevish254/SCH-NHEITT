import base64
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageOps


PAGES = [
    ("THE SCH\u00d6NHEITT WELCOME", ["Self-care is", "a necessity."], "At Schönheitt, care begins with you.", "reception.webp", "Care begins with a pause", ["We believe self-care is not a luxury, but a", "necessity: time to pause, feel cared for and reconnect", "with yourself."], "A PLACE TO PAUSE  ·  A MOMENT FOR YOU"),
    ("A CALM ESCAPE", ["Room to exhale."], "Step away from the pace of daily life.", "Massage room.jpg", "A calm, elegant space", ["Our space is designed as a calm, elegant escape", "from daily stress, with room to rest, reset and", "enjoy a moment that belongs to you."], "SLOW DOWN  ·  SETTLE IN"),
    ("PROFESSIONAL CARE", ["Thoughtful care."], "Beauty and wellness, delivered with attention.", "Massage bed.jpg", "Care from our team", ["We bring professional beauty and wellness services", "together in one welcoming space, with attention to", "your comfort and the details that matter to you."], "PROFESSIONAL  ·  PERSONAL"),
    ("YOUR WELLNESS MOMENT", ["Find your rhythm."], "Make room for rest and renewal.", "sauna 1.jpg", "A restorative pause", ["Take time for a sauna, massage or body-care ritual.", "Choose the experience that suits your moment and", "let yourself settle into a slower rhythm."], "REST  ·  RESET  ·  RECONNECT"),
    ("CARE FOR BODY & SELF", ["A softer pace."], "Let care become part of your routine.", "sauna 2.jpg", "Feel at ease", ["From the welcome at reception to time set aside", "for yourself, each visit is an invitation to slow", "down and enjoy being cared for."], "WELLNESS WITH ROOM TO BREATHE"),
    ("BEAUTY & WELLNESS", ["One welcoming", "destination."], "A considered place for your self-care.", "reception.webp", "Care for skin, body and beauty", ["Explore skincare, hair, massage, body care and", "finishing touches in one elegant destination, with", "services shaped around what you are looking for."], "SKIN  ·  BODY  ·  BEAUTY"),
    ("A MOMENT FOR YOU", ["You deserve", "the best care."], "Because your wellbeing matters.", "supplements.jpg", "Attention in every detail", ["We want every visit to feel warm, considered and", "professional. Share what you need, and our team", "will help you find a service that feels right."], "WELCOMING  ·  CONSIDERED  ·  PROFESSIONAL"),
    ("THE SCH\u00d6NHEITT PHILOSOPHY", ["Beauty begins", "with self-love."], "Let self-care be a way to honour yourself.", "sauna 1.jpg", "Care is time well spent", ["A moment of care can be a reminder to listen to", "yourself, make space to recharge and feel at home", "in your own skin."], "SELF-CARE  ·  SELF-LOVE"),
    ("A PLACE TO RETURN", ["Come as you are."], "Your next moment of care is waiting.", "Massage room.jpg", "We are here to welcome you", ["Whether you are here to unwind or enjoy a beauty", "ritual, we look forward to making your time with", "us feel thoughtful and personal."], "YOUR SPACE  ·  YOUR RITUAL"),
    ("SCH\u00d6NHEITT  ·  YOUR BEAUTY, OUR PASSION", ["Your beauty,", "our passion."], "Because you deserve the best care.", "reception.webp", "Let us care for you", ["Step into Schönheitt for a calm, elegant escape", "and professional beauty and wellness services.", "Make time for the care you deserve."], "WE LOOK FORWARD TO WELCOMING YOU"),
]

ROOT = Path(__file__).parent
ASSETS = ROOT.parent
GALLERY = next(path for path in ASSETS.iterdir() if path.is_dir() and path.name.lower().startswith("sch"))


def optimize_cover():
    with Image.open(GALLERY / "reception.webp") as source:
        source.thumbnail((1000, 1400))
        source.convert("RGB").save(ROOT / "cover.webp", "WEBP", quality=84, method=6)


def make_page(number, page):
    eyebrow, title_lines, subtitle, image_name, section, body_lines, note = page
    image_y = 224 if len(title_lines) == 1 else 255
    image_h = 286 if len(title_lines) == 1 else 255
    subtitle_y = 180 if len(title_lines) == 1 else 210
    section_y = image_y + image_h + 52
    body_y = section_y + 42
    title = "".join(
        f'<text x="48" y="{128 + index * 46}" class="title">{escape(line)}</text>'
        for index, line in enumerate(title_lines)
    )
    body = "".join(
        f'<text x="48" y="{body_y + index * 29}" class="body">{escape(line)}</text>'
        for index, line in enumerate(body_lines)
    )
    with Image.open(GALLERY / image_name) as source:
        image = ImageOps.fit(source.convert("RGB"), (956, image_h * 2), centering=(0.5, 0.5))
        buffer = BytesIO()
        image.save(buffer, "WEBP", quality=78, method=6)
    photo = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 574 800" role="img" aria-label="{escape(' '.join(title_lines))}">
<defs><clipPath id="photo"><rect x="48" y="{image_y}" width="478" height="{image_h}" rx="3"/></clipPath><linearGradient id="wash" x1="0" x2="1"><stop offset="0" stop-color="#34261d" stop-opacity=".3"/><stop offset=".56" stop-color="#34261d" stop-opacity=".035"/><stop offset="1" stop-color="#34261d" stop-opacity="0"/></linearGradient></defs>
<rect width="574" height="800" fill="#f5f0e4"/><rect width="574" height="12" fill="#80633b"/>
<text x="48" y="58" class="eyebrow">{escape(eyebrow)}</text><text x="526" y="58" text-anchor="end" class="page-no">{number:02d} / 10</text><path d="M48 78H526" stroke="#c9ab70"/>
{title}<text x="48" y="{subtitle_y}" class="subtitle">{escape(subtitle)}</text>
<image x="48" y="{image_y}" width="478" height="{image_h}" preserveAspectRatio="xMidYMid slice" clip-path="url(#photo)" xlink:href="data:image/webp;base64,{photo}"/><rect x="48" y="{image_y}" width="478" height="{image_h}" fill="url(#wash)" clip-path="url(#photo)"/>
<text x="48" y="{section_y}" class="section">{escape(section)}</text>{body}<path d="M48 717H526" stroke="#d9ccb1"/>
<text x="48" y="748" class="note">{escape(note)}</text><text x="526" y="748" text-anchor="end" class="brand">SCH\u00d6NHEITT</text>
<style>.eyebrow,.page-no,.note,.brand{{font:600 15px Arial,sans-serif;letter-spacing:2px;fill:#6b5433}}.title{{font:42px Georgia,'Times New Roman',serif;letter-spacing:-1px;fill:#241e16}}.subtitle{{font:italic 21px Georgia,'Times New Roman',serif;fill:#765f39}}.section{{font:600 23px Arial,sans-serif;fill:#352c20}}.body{{font:20px Arial,sans-serif;fill:#4e473a}}.note{{font-size:12px;letter-spacing:1.15px;fill:#796038}}.brand{{font-size:12px;letter-spacing:1.6px;fill:#8c7b5d}}</style></svg>'''


optimize_cover()
for number, page in enumerate(PAGES, 1):
    (ROOT / f"page{number}.svg").write_text(make_page(number, page), encoding="utf-8")
