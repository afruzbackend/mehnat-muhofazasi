"""«Materiallar» bo'limi: har bir mavzuga tarqatma (PDF), umumiy lug'at, savollar, mustaqil ta'lim va rasmiy manbalar.

    python manage.py materiallar                 # asosiy darslik (lectures/fan.py)
    python manage.py materiallar boshqa-darslik  # manbalar ro'yxatisiz, faqat PDF'lar

Avvalgi avtomatik materiallar yangisi bilan almashtiriladi; o'qituvchi o'zi yuklaganlariga tegilmaydi.
"""
from django.core.management.base import BaseCommand, CommandError

from lectures import fan
from lectures.materiallar import make_all
from lectures.models import Course
from lectures.taqdimot import FontMissing


class Command(BaseCommand):
    help = 'Darslik matnidan o‘quv materiallari (PDF) va rasmiy manbalar havolalarini qo‘shadi.'

    def add_arguments(self, parser):
        parser.add_argument('slug', nargs='?', default=fan.SLUG)

    def handle(self, *args, **opts):
        course = Course.objects.filter(slug=opts['slug']).first()
        if not course:
            raise CommandError(f"Darslik topilmadi: {opts['slug']}")
        links = getattr(fan, 'MATERIAL_LINKS', []) if course.slug == fan.SLUG else []
        try:
            n = make_all(course, links)
        except FontMissing as e:
            raise CommandError(str(e)) from None
        self.stdout.write(self.style.SUCCESS(f'«{course.title}»: {n} ta material.'))
