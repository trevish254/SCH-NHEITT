import base64
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageOps


PAGES = [
    ("THE SCHONHEITT BEAUTY EDIT", ["Beauty, finished", "with intention."], "NAILS, MAKEUP, LASHES & BROWS", "signature-portrait.webp", "A finishing touch, your way", ["Nails & Makeup meet Lashes & Brows in one considered", "beauty destination for hands, face and eyes, balancing", "personal style with thoughtful detail."], "NAILS  +  MAKEUP  +  LASHES  +  BROWS"),
    ("NAILS & MAKEUP  ·  01", ["Gel manicures"], "A polished look with lasting shine.", "mirror-manicure.webp", "A neat, glossy finish", ["Choose a gel manicure for a smooth, polished look in", "your preferred shade. We will help you select a finish", "that feels right for your style."], "NAILS  ·  COLOUR  ·  FINISH"),
    ("NAILS & MAKEUP  ·  02", ["Acrylic nails"], "Shape and length, thoughtfully tailored.", "makeup-nails.webp", "Your preferred nail shape", ["Acrylic enhancements can add length and definition.", "Choose your shape and colour with your nail artist, and", "follow the recommended care between appointments."], "SHAPE  ·  LENGTH  ·  DETAIL"),
    ("NAILS & MAKEUP  ·  03", ["French manicure"], "A timeless detail, made personal.", "mirror-manicure.webp", "Classic or contemporary", ["A clean French tip brings a refined touch to your", "manicure. Keep it classic or personalise the shape,", "tip colour and finish with your nail artist."], "A CLASSIC WITH YOUR OWN TWIST"),
    ("NAILS & MAKEUP  ·  04", ["Luxury pedicure"], "A little time set aside for you.", "signature-portrait.webp", "Care from heel to toe", ["Enjoy a considered pedicure with nail shaping, care and", "your choice of polish. Your therapist can discuss the", "available options when you book."], "PAUSE  ·  CARE  ·  POLISH"),
    ("NAILS & MAKEUP  ·  05", ["Professional", "makeup"], "A look shaped around your occasion.", "makeup-nails.webp", "Makeup that feels like you", ["From softly defined features to a more glamorous look,", "your makeup artist will tailor the application to your", "occasion, preferences and skin tone."], "SOFT  ·  DEFINED  ·  GLAMOROUS"),
    ("LASHES & BROWS  ·  01", ["Classic lashes"], "Subtle definition, lash by lash.", "lash-profile.webp", "A light, defined look", ["Classic extensions add definition while keeping the", "look understated. Your lash artist can help choose a", "style suited to your eyes and natural lashes."], "LASH EXTENSIONS  ·  CLASSIC"),
    ("LASHES & BROWS  ·  02", ["Hybrid & volume"], "From softly textured to fuller-looking.", "lash-profile.webp", "Choose your level of fullness", ["Hybrid and volume styles offer different levels of", "texture and fullness. Discuss your preferred look and", "lash care with your artist before your appointment."], "HYBRID  ·  VOLUME  ·  PERSONAL"),
    ("LASHES & BROWS  ·  03", ["Lashes & brows"], "Tinting, shaping and style, tailored to you.", "lash-profile.webp", "A considered finishing touch", ["Explore lash tinting and professional brow shaping", "and styling. Your artist will discuss your preferred", "look, suitability and aftercare before treatment."], "TINTING  ·  SHAPING  ·  STYLING"),
    ("SCHONHEITT  ·  SIGNATURE BEAUTY", ["Your details,", "beautifully finished."], "Make time for the details that feel like you.", "signature-portrait.webp", "Find your signature", ["Explore gel, acrylic and French manicures, luxury", "pedicures and makeup, alongside lash extensions, tinting", "and professional brow shaping and styling."], "ENHANCE  ·  EXPRESS  ·  FEEL YOURSELF"),
]

ROOT = Path(__file__).parent
IMAGE_ROOT = ROOT.parent / "lummi-signature"


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
    with Image.open(IMAGE_ROOT / image) as source:
        focal_x = 0.5 if image == "lash-profile.webp" else 0.55
        thumbnail = ImageOps.fit(source.convert("RGB"), (956, image_h * 2), centering=(focal_x, 0.5))
        image_buffer = BytesIO()
        thumbnail.save(image_buffer, "WEBP", quality=78, method=6)
    photo = base64.b64encode(image_buffer.getvalue()).decode("ascii")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 574 800" role="img" aria-label="{escape(' '.join(title_lines))}">
<defs><clipPath id="photo"><rect x="48" y="{image_y}" width="478" height="{image_h}" rx="3"/></clipPath><linearGradient id="wash" x1="0" x2="1"><stop offset="0" stop-color="#34261d" stop-opacity=".34"/><stop offset=".55" stop-color="#34261d" stop-opacity=".04"/><stop offset="1" stop-color="#34261d" stop-opacity="0"/></linearGradient></defs>
<rect width="574" height="800" fill="#f5f0e4"/><rect width="574" height="12" fill="#805b38"/>
<text x="48" y="58" class="eyebrow">{escape(eyebrow)}</text><text x="526" y="58" text-anchor="end" class="page-no">{number:02d} / 10</text><path d="M48 78H526" stroke="#c9ab70"/>
{title}<text x="48" y="{subtitle_y}" class="subtitle">{escape(subtitle)}</text>
<image x="48" y="{image_y}" width="478" height="{image_h}" preserveAspectRatio="xMidYMid slice" clip-path="url(#photo)" xlink:href="data:image/webp;base64,{photo}"/><rect x="48" y="{image_y}" width="478" height="{image_h}" fill="url(#wash)" clip-path="url(#photo)"/>
<text x="48" y="{section_y}" class="section">{escape(section)}</text>{body}<path d="M48 717H526" stroke="#d9ccb1"/>
<text x="48" y="748" class="note">{escape(note)}</text><text x="526" y="748" text-anchor="end" class="brand">SCHONHEITT</text>
<style>.eyebrow,.page-no,.note,.brand{{font:600 15px Arial,sans-serif;letter-spacing:2px;fill:#6b5433}}.title{{font:42px Georgia,'Times New Roman',serif;letter-spacing:-1px;fill:#241e16}}.subtitle{{font:italic 21px Georgia,'Times New Roman',serif;fill:#765f39}}.section{{font:600 23px Arial,sans-serif;fill:#352c20}}.body{{font:20px Arial,sans-serif;fill:#4e473a}}.note{{font-size:12px;letter-spacing:1.15px;fill:#796038}}.brand{{font-size:12px;letter-spacing:1.6px;fill:#8c7b5d}}</style></svg>'''


for number, page in enumerate(PAGES, 1):
    (ROOT / f"page{number}.svg").write_text(make_page(number, page), encoding="utf-8")
