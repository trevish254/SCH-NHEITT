import base64
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageOps


PAGES = [
    ("THE SCHÖNHEITT SKIN EDIT", ["Clinical care,", "with a softer touch."], "ADVANCED SKINCARE & AESTHETICS", "radiant-afro-portrait.webp", "One thoughtful approach", ["Everyday skin health meets advanced restorative care,", "with facial radiance, rejuvenation and your goals at", "the centre of every treatment conversation."], "FACIALS  +  AESTHETIC TREATMENTS"),
    ("FACIALS & SKIN CARE  ·  01", ["Hydrafacial"], "A fresh start for your skin.", "serene-skincare-close-up.webp", "Cleanse. Exfoliate. Hydrate.", ["A multi-step facial designed around a thorough cleanse,", "gentle exfoliation and a hydrated, refreshed finish.", "Your provider can tailor the session to your skin needs."], "PERSONALISED TO YOUR SKIN"),
    ("FACIALS & SKIN CARE  ·  02", ["Dermaplaning"], "A smooth, polished feel.", "skincare-application-close-up.webp", "Precise surface exfoliation", ["A professional exfoliation service that gently removes", "surface build-up and fine facial hair for a smoother feel.", "Suitability is discussed before your appointment."], "PROFESSIONAL SKIN PREP"),
    ("FACIALS & SKIN CARE  ·  03", ["Customized", "cleansing facials"], "Care that meets your skin where it is.", "serene-skincare-close-up.webp", "Made for your moment", ["Choose from cleansing and exfoliation focused facials,", "with products and steps selected to suit your skin,", "comfort and current concerns."], "A FACIAL THAT FEELS LIKE YOURS"),
    ("AESTHETIC TREATMENTS  ·  01", ["Advanced", "aesthetic care"], "Clinical expertise. Personal attention.", "radiant-afro-portrait.webp", "Enhancements, thoughtfully considered", ["Explore medical-grade options with a trained provider.", "A consultation helps clarify your goals, suitability,", "and the right next step for you."], "CONSULTATION LED"),
    ("AESTHETIC TREATMENTS  ·  02", ["PRP + GFC"], "Advanced restorative options.", "skincare-application-close-up.webp", "Discuss your options", ["PRP and GFC treatments are offered as part of our", "advanced aesthetics menu. Your practitioner will explain", "the approach and assess whether it suits your needs."], "ASK ABOUT SUITABILITY"),
    ("AESTHETIC TREATMENTS  ·  03", ["Botox +", "skin boosters"], "Subtle options, guided by expertise.", "radiant-afro-portrait.webp", "A considered consultation", ["Explore Botox and skin boosters with an experienced", "provider. Discuss your goals, expected results, aftercare", "and any questions before making a decision."], "PERSONALISED AESTHETIC CARE"),
    ("AESTHETIC TREATMENTS  ·  04", ["Vitamin drips"], "A wellbeing service, assessed individually.", "serene-skincare-close-up.webp", "Begin with a conversation", ["Ask our team about available vitamin drip options.", "A practitioner will review your needs and explain", "whether a service may be appropriate for you."], "PROVIDER ASSESSMENT REQUIRED"),
    ("YOUR SKIN, YOUR PLAN", ["Care for every", "complexion"], "Personalised to your skin and goals.", "skincare-application-close-up.webp", "Start with a skin conversation", ["Every treatment plan begins by understanding your skin,", "your priorities and your history. Your provider can help", "you choose suitable care for your complexion."], "THOUGHTFUL CARE FOR MELANATED SKIN"),
    ("SCHÖNHEITT  ·  ADVANCED SKINCARE", ["Your next chapter", "in skin care"], "Explore the options that feel right for you.", "radiant-afro-portrait.webp", "Book a consultation", ["Ask about treatment suitability, preparation, aftercare", "and recovery time. Together, you can build a considered", "plan for facial care and aesthetic treatments."], "FACIAL RADIANCE  ·  REJUVENATION  ·  CARE"),
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
    with Image.open(Path(__file__).parent.parent / "lummi" / image) as source:
        focal_x = {"serene-skincare-close-up.webp": 0.68, "skincare-application-close-up.webp": 0.51, "radiant-afro-portrait.webp": 0.56}[image]
        thumbnail = ImageOps.fit(source.convert("RGB"), (956, image_h * 2), centering=(focal_x, 0.5))
        image_buffer = BytesIO()
        thumbnail.save(image_buffer, "WEBP", quality=78, method=6)
    embedded_photo = base64.b64encode(image_buffer.getvalue()).decode("ascii")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 574 800" role="img" aria-label="{escape(' '.join(title_lines))}">
<defs><clipPath id="photo"><rect x="48" y="{image_y}" width="478" height="{image_h}" rx="3"/></clipPath><linearGradient id="wash" x1="0" x2="1"><stop offset="0" stop-color="#3d2c18" stop-opacity=".42"/><stop offset=".55" stop-color="#3d2c18" stop-opacity=".05"/><stop offset="1" stop-color="#3d2c18" stop-opacity="0"/></linearGradient></defs>
<rect width="574" height="800" fill="#f7f1e3"/><rect width="574" height="12" fill="#75531e"/>
<text x="48" y="58" class="eyebrow">{escape(eyebrow)}</text><text x="526" y="58" text-anchor="end" class="page-no">{number:02d} / 10</text><path d="M48 78H526" stroke="#c6a04a"/>
{title}<text x="48" y="{subtitle_y}" class="subtitle">{escape(subtitle)}</text>
<image x="48" y="{image_y}" width="478" height="{image_h}" preserveAspectRatio="xMidYMid slice" clip-path="url(#photo)" xlink:href="data:image/webp;base64,{embedded_photo}"/><rect x="48" y="{image_y}" width="478" height="{image_h}" fill="url(#wash)" clip-path="url(#photo)"/>
<text x="48" y="{section_y}" class="section">{escape(section)}</text>{body}<path d="M48 717H526" stroke="#d9ccb1"/>
<text x="48" y="748" class="note">{escape(note)}</text><text x="526" y="748" text-anchor="end" class="brand">SCHÖNHEITT</text>
<style>.eyebrow,.page-no,.note,.brand{{font:600 15px Arial,sans-serif;letter-spacing:2px;fill:#6a5430}}.title{{font:42px Georgia,'Times New Roman',serif;letter-spacing:-1px;fill:#231e16}}.subtitle{{font:italic 21px Georgia,'Times New Roman',serif;fill:#775e34}}.section{{font:600 23px Arial,sans-serif;fill:#312719}}.body{{font:20px Arial,sans-serif;fill:#4d4539}}.note{{font-size:12px;letter-spacing:1.15px;fill:#795b26}}.brand{{font-size:12px;letter-spacing:1.6px;fill:#8c7a5b}}</style></svg>'''


ROOT = Path(__file__).parent
for number, page in enumerate(PAGES, 1):
    (ROOT / f"page{number}.svg").write_text(make_page(number, page), encoding="utf-8")
