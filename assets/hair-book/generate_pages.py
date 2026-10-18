import base64
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageOps


PAGES = [
    ("THE SCHÖNHEITT HAIR EDIT", ["One destination,", "every kind of style."], "HAIR STYLING & PRECISION GROOMING", "braided-woman.webp", "Salon craft meets barber precision", ["Creative salon styling, luxury treatments and detailed", "barbering come together in one all-inclusive hair", "destination, with care for the whole family."], "SALON  +  BARBERSHOP"),
    ("HAIR SALON  ·  01", ["Professional", "salon care"], "A considered approach to every strand.", "natural-hair-profile.webp", "L'Oréal Professionnel + Mizani", ["Professional treatments and styling, with premium lines", "including L'Oréal Professionnel and Mizani. Tell us about", "your hair goals and the finish you have in mind."], "CARE  ·  STYLE  ·  FINISH"),
    ("HAIR SALON  ·  02", ["Styling & finish"], "Looks for everyday and occasion.", "braided-woman.webp", "Make your style your own", ["From a polished finish to a bold new look, our salon", "team can help you find a style that fits your texture,", "routine and the moment."], "CREATIVE SALON STYLING"),
    ("HAIR SALON  ·  03", ["Braids & weaving"], "Protective styles, shaped around you.", "braided-man.webp", "Braiding, weaving and more", ["Explore braiding and weaving options, with a style plan", "built around your preferred look and maintenance", "routine."], "BRAIDS  ·  WEAVING"),
    ("HAIR SALON  ·  04", ["Extensions & colour"], "Length, dimension and expression.", "braided-woman.webp", "A new way to wear your hair", ["Ask about extensions and professional colour services.", "Our team can talk through your preferred look, upkeep", "and the options available for your hair."], "EXTENSIONS  ·  COLOUR"),
    ("BARBERSHOP  ·  01", ["Precision barbering"], "A sharp cut starts with the details.", "joyful-man.webp", "Cuts shaped to suit you", ["From a clean refresh to a new silhouette, our barbers", "focus on shape, balance and a finish that feels right", "for you."], "PRECISION HAIRCUTS"),
    ("BARBERSHOP  ·  02", ["Fades & detail"], "Clean lines. A confident finish.", "natural-hair-profile.webp", "Precision fades", ["Choose a fade and cut that work with your hair texture", "and personal style. We finish with careful detailing and", "a look tailored to you."], "FADES  ·  FINISHING"),
    ("BARBERSHOP  ·  03", ["Beard grooming"], "Bring the whole look together.", "joyful-man.webp", "Shape, tidy and refine", ["Beard grooming and styling, from a neat tidy-up to a", "more defined shape, delivered with attention to your", "preferred length and finish."], "BEARD CARE"),
    ("FOR MEN & CHILDREN", ["A good cut for", "every generation."], "Comfortable, considered and personal.", "natural-hair-profile.webp", "Kids' styling, too", ["Our barbershop welcomes men and children for styling", "and cuts. We take time to understand the look you want", "and help make the appointment feel easy."], "MEN  ·  KIDS  ·  FAMILY"),
    ("SCHÖNHEITT  ·  HAIR", ["Your style,", "your way."], "Find your next look with us.", "braided-man.webp", "Explore the full hair menu", ["From salon treatments, braids and colour to precision", "cuts, fades and beard care, discover a hair service for", "you and your family."], "SALON CRAFT  ·  BARBER PRECISION"),
]


def make_page(number, page):
    eyebrow, title_lines, subtitle, image, section, body_lines, note = page
    image_y = 223 if len(title_lines) == 1 else 255
    image_h = 288 if len(title_lines) == 1 else 256
    subtitle_y = 180 if len(title_lines) == 1 else 210
    section_y = image_y + image_h + 54
    body_y = section_y + 45
    title = "".join(
        f'<text x="48" y="{128 + n * 47}" class="title">{escape(line)}</text>'
        for n, line in enumerate(title_lines)
    )
    body = "".join(
        f'<text x="48" y="{body_y + n * 32}" class="body">{escape(line)}</text>'
        for n, line in enumerate(body_lines)
    )
    with Image.open(Path(__file__).parent.parent / "lummi-hair" / image) as source:
        focal_x = {"braided-woman.webp": 0.5, "natural-hair-profile.webp": 0.64, "braided-man.webp": 0.5, "joyful-man.webp": 0.5}[image]
        thumbnail = ImageOps.fit(source.convert("RGB"), (956, image_h * 2), centering=(focal_x, 0.5))
        image_buffer = BytesIO()
        thumbnail.save(image_buffer, "WEBP", quality=78, method=6)
    embedded_photo = base64.b64encode(image_buffer.getvalue()).decode("ascii")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 574 800" role="img" aria-label="{escape(' '.join(title_lines))}">
<defs><clipPath id="photo"><rect x="48" y="{image_y}" width="478" height="{image_h}" rx="3"/></clipPath><linearGradient id="wash" x1="0" x2="1"><stop offset="0" stop-color="#34261d" stop-opacity=".38"/><stop offset=".55" stop-color="#34261d" stop-opacity=".04"/><stop offset="1" stop-color="#34261d" stop-opacity="0"/></linearGradient></defs>
<rect width="574" height="800" fill="#f5eee4"/><rect width="574" height="12" fill="#5c392c"/>
<text x="48" y="58" class="eyebrow">{escape(eyebrow)}</text><text x="526" y="58" text-anchor="end" class="page-no">{number:02d} / 10</text><path d="M48 78H526" stroke="#b88c59"/>
{title}<text x="48" y="{subtitle_y}" class="subtitle">{escape(subtitle)}</text>
<image x="48" y="{image_y}" width="478" height="{image_h}" preserveAspectRatio="xMidYMid slice" clip-path="url(#photo)" xlink:href="data:image/webp;base64,{embedded_photo}"/><rect x="48" y="{image_y}" width="478" height="{image_h}" fill="url(#wash)" clip-path="url(#photo)"/>
<text x="48" y="{section_y}" class="section">{escape(section)}</text>{body}<path d="M48 717H526" stroke="#d8c7b5"/>
<text x="48" y="748" class="note">{escape(note)}</text><text x="526" y="748" text-anchor="end" class="brand">SCHÖNHEITT</text>
<style>.eyebrow,.page-no,.note,.brand{{font:600 15px Arial,sans-serif;letter-spacing:2px;fill:#674b3d}}.title{{font:42px Georgia,'Times New Roman',serif;letter-spacing:-1px;fill:#241d19}}.subtitle{{font:italic 21px Georgia,'Times New Roman',serif;fill:#79583f}}.section{{font:600 23px Arial,sans-serif;fill:#35281f}}.body{{font:20px Arial,sans-serif;fill:#51463e}}.note{{font-size:12px;letter-spacing:1.15px;fill:#79583f}}.brand{{font-size:12px;letter-spacing:1.6px;fill:#917d6c}}</style></svg>'''


ROOT = Path(__file__).parent
for number, page in enumerate(PAGES, 1):
    (ROOT / f"page{number}.svg").write_text(make_page(number, page), encoding="utf-8")
