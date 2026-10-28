"""Shu nusxadagi darslik (fan) ma'lumotlari.

Boshqa fan uchun sayt yasashda loyiha nusxalanadi va faqat shu fayl hamda data/maruza.docx almashtiriladi:
bo'limlar, har bir mavzuning 3D ko'rgazmasi, muallif va YouTube video darslari shu yerda.
"""
from pathlib import Path

SLUG = 'mehnat-muhofazasi'   # docx dagi fan nomidan: «Mehnat muhofazasi va texnika xavfsizligi»
AUTHOR = 'Oydin Tashtemirova'

IMG = Path(__file__).resolve().parent / 'static' / 'lectures' / 'img'
PHOTO = IMG / 'muallif.jpg'   # ustoz (portret)
COVER = IMG / 'muqova.jpg'    # bosh sahifa foni: ustoz dars o'tayotgan payt

# docx muqovasida yo'q ma'lumotlar (har bir mavzu 80 daqiqa = 2 soat; 18 nazariy, 2 amaliy)
COURSE = {
    'module': '3-malaka darajasi · 40 soat',
    'direction': 'Kompyuter grafikasi va dizayn',
    'hours_theory': 36,
    'hours_practice': 4,
    'subtitle': 'Interaktiv elektron darslik: ma’ruzalar, 3D ko‘rgazmalar, video darslar, taqdimotlar va testlar.',
}

# (bo'lim nomi, birinchi mavzu, oxirgi mavzu, rang, belgi)
PARTS = [
    ('Sanitariya, elektr va yong‘in xavfsizligi', 1, 3, '#C2562D', 'fire'),
    ('Xavfsiz mehnat usullari', 4, 5, '#0E7C7B', 'wrench'),
    ('Favqulodda vaziyatlar va evakuatsiya', 6, 7, '#9E2A3A', 'exit'),
    ('Birinchi tibbiy yordam', 8, 10, '#24508F', 'aid'),
    ('Shaxsiy himoya vositalari', 11, 13, '#B07D1E', 'helmet'),
    ('Mehnat xavfsizligi va profilaktika', 14, 15, '#3F7D4E', 'shield'),
    ('Raqamli qurilmalar va kiberxavfsizlik', 16, 18, '#2F68B8', 'monitor'),
    ('Elektr xavfsizligi talablari', 19, 20, '#D86A3E', 'bolt'),
]

# mavzu raqami -> 3D ko'rgazma (lectures/scenes.py)
SCENES = {
    1: 'fan', 2: 'plug', 3: 'fire', 4: 'tools', 5: 'monitor', 6: 'siren', 7: 'exit', 8: 'aid', 9: 'aid',
    10: 'heart', 11: 'helmet', 12: 'helmet', 13: 'gear', 14: 'safety', 15: 'siren', 16: 'printer', 17: 'tower',
    18: 'shield', 19: 'safety', 20: 'plug',
}

FINAL_SCENE = 'safety'   # yakuniy test sahifasidagi 3D ko'rgazma

# mavzu raqami -> [(YouTube video ID, tili)]   tanlov: mavzuga mosligi, o'zbek tilidagilar birinchi
VIDEOS = {
    1: [('NBWIhU_-ta0', 'uz'), ('TCoW2u_fbGo', 'uz'), ('GuHw_aCoPGo', 'uz')],
    2: [('qBNTr7CgpZk', 'uz'), ('_gSKdaozykI', 'uz'), ('NRDiP31Te5g', 'uz')],
    3: [('d2Tze77Y63U', 'uz'), ('QWJqSGKfyaY', 'uz'), ('CgNzLxruH4k', 'uz')],
    4: [('BP_6Tdl9Hhk', 'uz'), ('8h4N-vtWuD0', 'uz'), ('sVBp-cVP6I4', 'uz')],
    5: [('ndIc4K4JdGE', 'uz'), ('Vo3kGOweK6s', 'uz'), ('3aJYc2wQv98', 'uz')],
    6: [('WUCYMNQnDuM', 'uz'), ('dQyTQ6meKGE', 'uz'), ('mTMxQmvBaTY', 'uz')],
    7: [('Oxb90Ce3dvg', 'uz'), ('cbhaXRWHQNI', 'uz'), ('x3DbVwCaIPE', 'uz')],
    8: [('DuMEjPm_nGQ', 'uz'), ('sWVhaynSRPE', 'uz'), ('KOORO_y7b1g', 'uz')],
    9: [('EmmSJxAWVKM', 'uz'), ('rDuUJ0Fxmtc', 'uz'), ('5YguL3kP9GU', 'uz')],
    10: [('mLjtMGpkS90', 'uz'), ('pzAJPFGPmJo', 'uz'), ('0svDPK2LPS4', 'uz')],
    11: [('S1eDVGL7Irc', 'uz'), ('132Crzcgmew', 'uz'), ('0NjcV-CFYtw', 'uz')],
    12: [('rptamMLd_Po', 'uz'), ('YIevApC37pM', 'uz'), ('DqNFq5puNgU', 'uz')],
    13: [('OuX2u1qut7U', 'uz'), ('JLfe4Julaic', 'uz'), ('6tj9RQogD6c', 'uz')],
    14: [('EECt2NIpQy4', 'uz'), ('sD2eQ083kyo', 'uz'), ('GWIqk_uqo-4', 'uz')],
    15: [('qSiAqNZQIcg', 'uz'), ('-LU8-d0Be_w', 'uz'), ('vlsxPUk2DlU', 'uz')],
    16: [('s97gmY2xq38', 'uz'), ('PpMESRSMby0', 'uz'), ('Q-1XPeGVgkE', 'uz')],
    17: [('-I0XBYdynto', 'uz'), ('3daSe4tyuFI', 'uz'), ('PKRFdbQhBaM', 'uz')],
    18: [('BBt0lBldnLQ', 'uz'), ('7eIJO1q7UWw', 'uz'), ('hvTPXsZPnrk', 'uz')],
    19: [('eufz_NiU5xQ', 'uz'), ('Nd62DqvTrwA', 'uz'), ('d9pWPcvVPLA', 'uz')],
    20: [('9LYgLaDoVgg', 'uz'), ('zDhivm2Pw1U', 'uz'), ('kUkrgkSFSuE', 'uz')],
}

# «Materiallar» bo'limidagi rasmiy manbalar (docx dagi adabiyotlar ro'yxatidan; havolalar tekshirilgan)
# (nomi, havola, izoh, mavzu raqami — None bo'lsa butun darslik uchun)
MATERIAL_LINKS = [
    ('O‘zbekiston Respublikasining Mehnat kodeksi', 'https://lex.uz/docs/-6257288',
     'Rasmiy matn · lex.uz · mehnat muhofazasi, xodim va ish beruvchining huquq va majburiyatlari', 14),
    ('«Mehnatni muhofaza qilish to‘g‘risida»gi Qonun (O‘RQ-410, 22.09.2016)', 'https://lex.uz/docs/-3031427',
     'Rasmiy matn · lex.uz', 14),
    ('«Yong‘in xavfsizligi to‘g‘risida»gi Qonun (O‘RQ-226, 30.09.2009)', 'https://lex.uz/docs/-1521661',
     'Rasmiy matn · lex.uz', 3),
    ('ZiyoNET — ta’lim axborot tarmog‘i', 'https://ziyonet.uz/uz',
     'O‘quv qo‘llanmalar, darsliklar va qo‘shimcha adabiyotlar', None),
]
