import base64
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageOps


PAGES = [
    ("THE SCHÖNHEITT WELLNESS EDIT", ["Whole-body care,", "made personal."], "SPA, MASSAGE & BODY CARE", "radiant-afro-portrait.webp", "Wellness with room to exhale", ["Massage therapy and body waxing come together in one", "considered care experience: time to unwind, restore", "and enjoy a smooth, cared-for finish."], "MASSAGE  +  BODY WAXING"),
    ("MASSAGE THERAPY  ·  01", ["Swedish massage"], "A gentler rhythm for your body.", "brown-skin-lotion-care.webp", "Slow down and unwind", ["A flowing massage using lighter, rhythmic strokes,", "created to encourage relaxation and ease everyday", "tension. Let your therapist know what feels comfortable."], "RELAXATION  ·  REST"),
    ("MASSAGE THERAPY  ·  02", ["Deep tissue"], "Focused pressure, at your pace.", "radiant-afro-portrait.webp", "A more focused massage", ["A firmer-pressure option for areas that need focused", "attention. Your therapist can adjust pressure and focus", "throughout the session to suit your comfort."], "FOCUSED  ·  PERSONAL"),
    ("MASSAGE THERAPY  ·  03", ["Prenatal massage"], "Comfort comes first.", "brown-skin-lotion-care.webp", "Care during pregnancy", ["A tailored massage session with your comfort in mind.", "Discuss suitability, positioning and any concerns with", "your therapist before your appointment."], "GENTLE  ·  CONSIDERED"),
    ("MASSAGE THERAPY  ·  04", ["Targeted", "therapeutic massage"], "Attention where you need it.", "radiant-afro-portrait.webp", "Focused on your needs", ["A targeted session planned around areas of tension", "or discomfort you would like to address. Your therapist", "will agree on the focus and pressure with you."], "TARGETED  ·  TAILORED"),
    ("YOUR MASSAGE  ·  YOUR MOMENT", ["Settle into", "your own rhythm."], "A session shaped around you.", "brown-skin-lotion-care.webp", "Tell us what feels right", ["Share your goals, preferred pressure and areas to focus", "on. Your therapist will adapt the session to your", "comfort and the time you have."], "LISTEN  ·  ADJUST  ·  RESTORE"),
    ("BODY WAXING  ·  01", ["Smooth body care"], "A polished finish, with care.", "brown-skin-lotion-care.webp", "Body waxing services", ["Explore full-body and intimate waxing in a professional", "setting. Your therapist can explain the service and", "help you feel comfortable before you begin."], "SMOOTH  ·  CONFIDENT"),
    ("BODY WAXING  ·  02", ["Full-body waxing"], "A smooth finish from head to toe.", "radiant-afro-portrait.webp", "Choose the areas that suit you", ["Discuss the areas you would like treated and any", "preferences before your appointment. Our team will", "guide you through preparation and aftercare."], "FULL-BODY OPTIONS"),
    ("BODY WAXING  ·  03", ["Intimate waxing"], "Professional, discreet and guided by you.", "brown-skin-lotion-care.webp", "Your comfort and boundaries matter", ["Your therapist will explain each step and check in with", "you throughout. Share any preferences or concerns so", "the service can feel as comfortable as possible."], "PRIVATE  ·  RESPECTFUL  ·  PERSONAL"),
    ("SCHÖNHEITT  ·  BODY CARE", ["Leave feeling", "lighter and smooth."], "Make space for your next reset.", "radiant-afro-portrait.webp", "Choose your body-care ritual", ["Unwind with Swedish, deep tissue, prenatal or targeted", "therapeutic massage, or explore body waxing services", "for a smooth, cared-for finish."], "RESTORE  ·  UNWIND  ·  FEEL RENEWED"),
]


def source_image(name):
    if name == "brown-skin-lotion-care.webp":
        return Path(__file__).parent.parent / "lummi-body" / name
    return Path(__file__).parent.parent / "lummi" / name


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
    with Image.open(source_image(image)) as source:
        focal_x = 0.68 if image == "brown-skin-lotion-care.webp" else 0.56
        thumbnail = ImageOps.fit(source.convert("RGB"), (956, image_h * 2), centering=(focal_x, 0.5))
        image_buffer = BytesIO()
        thumbnail.save(image_buffer, "WEBP", quality=78, method=6)
    embedded_photo = base64.b64encode(image_buffer.getvalue()).decode("ascii")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 574 800" role="img" aria-label="{escape(' '.join(title_lines))}">
<defs><clipPath id="photo"><rect x="48" y="{image_y}" width="478" height="{image_h}" rx="3"/></clipPath><linearGradient id="wash" x1="0" x2="1"><stop offset="0" stop-color="#34261d" stop-opacity=".38"/><stop offset=".55" stop-color="#34261d" stop-opacity=".04"/><stop offset="1" stop-color="#34261d" stop-opacity="0"/></linearGradient></defs>
<rect width="574" height="800" fill="#f5f0e4"/><rect width="574" height="12" fill="#755c31"/>
<text x="48" y="58" class="eyebrow">{escape(eyebrow)}</text><text x="526" y="58" text-anchor="end" class="page-no">{number:02d} / 10</text><path d="M48 78H526" stroke="#c9ab70"/>
{title}<text x="48" y="{subtitle_y}" class="subtitle">{escape(subtitle)}</text>
<image x="48" y="{image_y}" width="478" height="{image_h}" preserveAspectRatio="xMidYMid slice" clip-path="url(#photo)" xlink:href="data:image/webp;base64,{embedded_photo}"/><rect x="48" y="{image_y}" width="478" height="{image_h}" fill="url(#wash)" clip-path="url(#photo)"/>
<text x="48" y="{section_y}" class="section">{escape(section)}</text>{body}<path d="M48 717H526" stroke="#d9ccb1"/>
<text x="48" y="748" class="note">{escape(note)}</text><text x="526" y="748" text-anchor="end" class="brand">SCHÖNHEITT</text>
<style>.eyebrow,.page-no,.note,.brand{{font:600 15px Arial,sans-serif;letter-spacing:2px;fill:#6b5433}}.title{{font:42px Georgia,'Times New Roman',serif;letter-spacing:-1px;fill:#241e16}}.subtitle{{font:italic 21px Georgia,'Times New Roman',serif;fill:#765f39}}.section{{font:600 23px Arial,sans-serif;fill:#352c20}}.body{{font:20px Arial,sans-serif;fill:#4e473a}}.note{{font-size:12px;letter-spacing:1.15px;fill:#796038}}.brand{{font-size:12px;letter-spacing:1.6px;fill:#8c7b5d}}</style></svg>'''


ROOT = Path(__file__).parent
for number, page in enumerate(PAGES, 1):
    (ROOT / f"page{number}.svg").write_text(make_page(number, page), encoding="utf-8")
