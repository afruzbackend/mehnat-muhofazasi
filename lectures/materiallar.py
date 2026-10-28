"""Darslik matnidan chop etiladigan o'quv materiallari (PDF, A4) — «Materiallar» bo'limi uchun.

    make_all(course)   # har bir mavzuga tarqatma material + umumiy: atamalar lug'ati, savollar, mustaqil ta'lim

Hammasi docx dan olingan matndan yig'iladi (yangi ma'lumot qo'shilmaydi): qoidalar ro'yxatlari, jadvallar,
mustahkamlash savollari va topshiriqlar. Qayta ishga tushirilsa avvalgi avtomatik materiallar almashtiriladi,
o'qituvchi o'zi yuklaganlariga tegilmaydi. Shriftlar taqdimotdagi kabi: Georgia va Segoe UI.
"""
import html
import io
import re

from .taqdimot import INK, LINE, MUTED, PAPER2, TERRA, _pdf_fonts

AUTO_NOTE = 'Darslik matnidan tayyorlangan'
FIRUZA = '#0E7C7B'


# ------------------------------------------------------------------ matn
def para_html(s):
    """docx html -> reportlab Paragraph belgilashi (<b>, <br/> qoladi, qolgan teglar olib tashlanadi)."""
    s = re.sub(r'<br\s*/?>', '<br/>', s or '')
    s = re.sub(r'</?code>', '', s)
    s = re.sub(r'<(?!/?b>|br/>)[^>]+>', '', s)
    return s.replace('&nbsp;', ' ')


def plain(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s or '')).strip()


# ------------------------------------------------------------------ sahifa uslubi
def _styles():
    from reportlab.lib.colors import HexColor
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.pdfbase.pdfmetrics import registerFontFamily

    f = _pdf_fonts()
    serif, serif_b, sans, sans_b = f[('serif', False)], f[('serif', True)], f[('sans', False)], f[('sans', True)]
    registerFontFamily(sans, normal=sans, bold=sans_b, italic=sans, boldItalic=sans_b)
    registerFontFamily(serif, normal=serif, bold=serif_b, italic=serif, boldItalic=serif_b)
    ink, muted = HexColor(INK), HexColor(MUTED)
    return {
        'eyebrow': ParagraphStyle('eyebrow', fontName=sans_b, fontSize=8.5, leading=11, textColor=HexColor(TERRA),
                                  spaceAfter=4),
        'title': ParagraphStyle('title', fontName=serif_b, fontSize=19, leading=23, textColor=ink, spaceAfter=8),
        'h2': ParagraphStyle('h2', fontName=serif_b, fontSize=13.5, leading=17, textColor=ink, spaceBefore=12,
                             spaceAfter=5),
        'h3': ParagraphStyle('h3', fontName=sans_b, fontSize=10.5, leading=13, textColor=HexColor(FIRUZA),
                             spaceBefore=7, spaceAfter=3),
        'body': ParagraphStyle('body', fontName=sans, fontSize=10, leading=14, textColor=ink, spaceAfter=4),
        'small': ParagraphStyle('small', fontName=sans, fontSize=8.5, leading=11, textColor=muted),
        'cell': ParagraphStyle('cell', fontName=sans, fontSize=8.8, leading=11.5, textColor=ink),
        'cellh': ParagraphStyle('cellh', fontName=sans_b, fontSize=8.8, leading=11.5, textColor=HexColor('#FBF6EC')),
        'box': ParagraphStyle('box', fontName=sans, fontSize=9.6, leading=13.5, textColor=ink),
    }


def _bullets(items, st, numbered=False):
    from reportlab.platypus import ListFlowable, ListItem, Paragraph
    from reportlab.lib.colors import HexColor
    return ListFlowable(
        [ListItem(Paragraph(para_html(x), st['body']), leftIndent=14) for x in items],
        bulletType='1' if numbered else 'bullet', start='1' if numbered else '•',
        bulletFontName=st['body'].fontName, bulletFontSize=9.5, bulletColor=HexColor(TERRA), leftIndent=14)


def _table(rows, st, widths=None):
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import Paragraph, Table, TableStyle
    rows = [r for r in rows if any(plain(c) for c in r)]
    if not rows:
        return None
    n = max(len(r) for r in rows)
    data = [[Paragraph(para_html(c), st['cellh' if i == 0 else 'cell']) for c in r + [''] * (n - len(r))]
            for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(FIRUZA)),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#FBF6EC'), HexColor(PAPER2)]),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor(LINE)),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    return t


def _box(text, st):
    """Ajratilgan quti (maqsad, eslatma)."""
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import Paragraph, Table, TableStyle
    t = Table([[Paragraph(para_html(text), st['box'])]], hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor(PAPER2)),
        ('LINEBEFORE', (0, 0), (0, -1), 3, HexColor(TERRA)),
        ('LEFTPADDING', (0, 0), (-1, -1), 10), ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
    ]))
    return t


def _render(course, title, story):
    """A4 hujjat: yuqorida fan nomi, pastda sahifa raqami va muallif."""
    from reportlab.lib.colors import HexColor
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate

    f = _pdf_fonts()
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=1.8 * cm, rightMargin=1.8 * cm, topMargin=2 * cm,
                            bottomMargin=1.8 * cm, title=title, author=course.author, subject=course.title)
    w, h = A4

    def frame(c, d):
        c.saveState()
        c.setFillColor(HexColor(TERRA))
        c.rect(0, h - 0.35 * cm, w, 0.35 * cm, fill=1, stroke=0)
        c.setFont(f[('sans', True)], 8)
        c.setFillColor(HexColor(MUTED))
        c.drawString(1.8 * cm, h - 1.15 * cm, course.title.upper())
        c.drawRightString(w - 1.8 * cm, h - 1.15 * cm, course.college or '')
        c.setStrokeColor(HexColor(LINE))
        c.line(1.8 * cm, 1.3 * cm, w - 1.8 * cm, 1.3 * cm)
        c.setFont(f[('sans', False)], 8)
        c.drawString(1.8 * cm, 0.85 * cm, f'{course.author} · elektron darslik')
        c.drawRightString(w - 1.8 * cm, 0.85 * cm, f'{d.page}-bet')
        c.restoreState()

    doc.build(story, onFirstPage=frame, onLaterPages=frame)
    return buf.getvalue()


# ------------------------------------------------------------------ hujjatlar
def topic_handout(topic):
    """Mavzu bo'yicha tarqatma: maqsad, reja, har bir bo'limning qoidalari va jadvallari, savollar, topshiriqlar."""
    from reportlab.platypus import KeepTogether, Paragraph, Spacer

    st = _styles()
    s = [Paragraph(f'{topic.number}-MAVZU · {topic.kind.upper()} · TARQATMA MATERIAL', st['eyebrow']),
         Paragraph(html.escape(topic.title), st['title'])]
    if topic.goal:
        s += [_box(f'<b>Mashg‘ulot maqsadi.</b> {topic.goal}', st), Spacer(0, 6)]
    sections = list(topic.sections.all())
    s += [Paragraph('Reja', st['h2']), _bullets([html.escape(x.title) for x in sections], st, numbered=True)]

    for i, sec in enumerate(sections, 1):
        s.append(Paragraph(f'{i}. {html.escape(sec.title)}', st['h2']))
        blocks = sec.blocks
        has_key = any(b['t'] in ('ul', 'table') for b in blocks)
        for j, b in enumerate(blocks):
            if b['t'] == 'h':
                # sarlavhadan keyin ro'yxat yoki jadval bo'lsagina — aks holda bo'sh sarlavha qoladi
                nxt = next((x for x in blocks[j + 1:] if x['t'] != 'p'), None)
                if nxt and nxt['t'] in ('ul', 'table') or not has_key:
                    s.append(Paragraph(html.escape(b['text']), st['h3']))
            elif b['t'] == 'ul':
                s.append(_bullets(b['items'], st))
            elif b['t'] == 'table':
                t = _table(b['rows'], st)
                if t:
                    s += [Spacer(0, 3), t, Spacer(0, 5)]
            elif b['t'] == 'p' and not has_key:
                s.append(Paragraph(para_html(b['html']), st['body']))
            elif b['t'] == 'note':
                s.append(_box(b.get('html') or b.get('text', ''), st))

    if topic.questions:
        s.append(KeepTogether([Paragraph('Mustahkamlash uchun savollar', st['h2']),
                               _bullets([html.escape(q) for q in topic.questions], st, numbered=True)]))
    if topic.self_study:
        s.append(KeepTogether([Paragraph('Mustaqil ta’lim topshiriqlari', st['h2']),
                               _bullets(topic.self_study, st)]))
    return _render(topic.course, f'{topic.number}-mavzu. {topic.title} — tarqatma material', s)


def glossary_pdf(course):
    from reportlab.lib.units import cm
    from reportlab.platypus import Paragraph

    st = _styles()
    terms = sorted(course.glossary.select_related('topic'), key=lambda g: g.term.strip('«»').lower())
    rows = [['Atama', 'Ta’rif', 'Mavzu']] + [
        [f'<b>{html.escape(g.term)}</b>', html.escape(g.definition), str(g.topic.number) if g.topic else '']
        for g in terms]
    s = [Paragraph('ATAMALAR LUG‘ATI', st['eyebrow']),
         Paragraph(f'{html.escape(course.title)}: asosiy atamalar', st['title']),
         Paragraph(f'Darslik matnidagi {len(terms)} ta atama va ularning ta’rifi. Oxirgi ustunda — atama '
                   'tushuntirilgan mavzu raqami.', st['body']),
         _table(rows, st, widths=[4.4 * cm, 11.2 * cm, 1.8 * cm])]
    return _render(course, f'{course.title} — atamalar lug‘ati', s)


def questions_pdf(course):
    from reportlab.platypus import KeepTogether, Paragraph

    st = _styles()
    topics = list(course.topics.all())
    total = sum(len(t.questions) + len(t.prev_questions) for t in topics)
    s = [Paragraph('SAVOLLAR TO‘PLAMI', st['eyebrow']),
         Paragraph('Takrorlash va mustahkamlash uchun savollar', st['title']),
         Paragraph(f'Har bir mavzu bo‘yicha jami {total} ta savol: dars boshida o‘tgan mavzuni takrorlash va '
                   'dars oxirida yangi mavzuni mustahkamlash uchun. Og‘zaki so‘rov va yozma ish uchun qulay.',
                   st['body'])]
    for t in topics:
        block = [Paragraph(f'{t.number}. {html.escape(t.title)}', st['h2'])]
        if t.prev_questions:
            block += [Paragraph('O‘tgan mavzuni takrorlash', st['h3']),
                      _bullets([html.escape(q) for q in t.prev_questions], st, numbered=True)]
        if t.questions:
            block += [Paragraph('Mustahkamlash', st['h3']),
                      _bullets([html.escape(q) for q in t.questions], st, numbered=True)]
        s.append(KeepTogether(block))
    return _render(course, f'{course.title} — savollar to‘plami', s)


def self_study_pdf(course):
    from reportlab.platypus import KeepTogether, Paragraph

    st = _styles()
    topics = list(course.topics.all())
    s = [Paragraph('MUSTAQIL TA’LIM', st['eyebrow']),
         Paragraph('Mustaqil ta’lim topshiriqlari va adabiyotlar', st['title'])]
    for t in topics:
        if t.self_study:
            s.append(KeepTogether([Paragraph(f'{t.number}. {html.escape(t.title)}', st['h2']),
                                   _bullets(t.self_study, st)]))
    books = []
    for t in topics:
        for b in t.literature:
            if b not in books:
                books.append(b)
    if books:
        s += [Paragraph('Adabiyotlar va manbalar', st['h2']),
              _bullets([html.escape(b) for b in books], st, numbered=True)]
    return _render(course, f'{course.title} — mustaqil ta’lim', s)


# ------------------------------------------------------------------ darslikka qo'shish
def make_all(course, links=()):
    """Avtomatik materiallarni (qayta) yaratish. links: [(nomi, url, izoh, mavzu raqami yoki None)]."""
    from django.core.files.base import ContentFile

    from .models import Resource

    for old in course.resources.filter(kind='material', note__startswith=AUTO_NOTE):
        if old.file:
            old.file.delete(save=False)
        old.delete()

    def add(title, note, topic=None, pdf=None, name=None, url=''):
        r = Resource(course=course, topic=topic, kind='material', title=title, url=url, note=f'{AUTO_NOTE} · {note}')
        if pdf:
            r.file.save(name, ContentFile(pdf), save=True)
        else:
            r.save()
        return r

    n = 0
    slug = course.slug
    add('Atamalar lug‘ati', f'{course.glossary.count()} ta atama va ta’rif · chop etish uchun',
        pdf=glossary_pdf(course), name=f'{slug}-atamalar-lugati.pdf')
    add('Savollar to‘plami', 'takrorlash va mustahkamlash savollari · barcha mavzular',
        pdf=questions_pdf(course), name=f'{slug}-savollar-toplami.pdf')
    add('Mustaqil ta’lim topshiriqlari va adabiyotlar', 'barcha mavzular bo‘yicha',
        pdf=self_study_pdf(course), name=f'{slug}-mustaqil-talim.pdf')
    n += 3
    for t in course.topics.prefetch_related('sections'):
        add(f'{t.number}-mavzu: tarqatma material', 'asosiy qoidalar, jadvallar va savollar · A4, chop etish uchun',
            topic=t, pdf=topic_handout(t), name=f'{slug}-{t.number:02d}-tarqatma.pdf')
        n += 1
    topics = {t.number: t for t in course.topics.all()}
    for title, url, note, num in links:
        add(title, note, topic=topics.get(num), url=url)
        n += 1
    return n
