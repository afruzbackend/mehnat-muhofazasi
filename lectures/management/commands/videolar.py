"""Asosiy darslikning har bir mavzusiga YouTube'dan tanlangan 2-3 ta video dars (ro'yxat: lectures/fan.py).

    python manage.py videolar            # qo'shadi (borlarini takrorlamaydi)
    python manage.py videolar --tekshir  # faqat videolar ochilishini tekshiradi

Har bir video YouTube oEmbed orqali tekshiriladi: o'chirilgan yoki saytga joylashtirish taqiqlangan
videolar qo'shilmaydi.
"""
import json
import urllib.error
import urllib.parse
import urllib.request

from django.core.management.base import BaseCommand

from lectures import fan
from lectures.models import Course, Resource

LANG = {'uz': 'o‘zbek tilida', 'ru': 'rus tilida', 'en': 'ingliz tilida'}


def oembed(vid):
    """(nomi, kanali) yoki xato matni. 401/403 — joylashtirish taqiqlangan, 404 — video yo'q."""
    url = 'https://www.youtube.com/oembed?format=json&url=' + urllib.parse.quote(f'https://www.youtube.com/watch?v={vid}')
    try:
        d = json.load(urllib.request.urlopen(url, timeout=20))
        return d['title'], d.get('author_name', ''), None
    except urllib.error.HTTPError as e:
        return None, None, {401: 'joylashtirish taqiqlangan', 403: 'joylashtirish taqiqlangan', 404: 'video topilmadi'}.get(e.code, f'HTTP {e.code}')
    except OSError as e:
        return None, None, f'internet xatosi: {e}'


class Command(BaseCommand):
    help = "Asosiy darslik mavzulariga YouTube video darslarini qo'shadi (lectures/fan.py)."

    def add_arguments(self, parser):
        parser.add_argument('--tekshir', action='store_true', help='Faqat tekshirish, bazaga yozmaslik')

    def handle(self, *args, **opts):
        course = Course.objects.get(slug=fan.SLUG)
        added = skipped = failed = 0
        for n, items in fan.VIDEOS.items():
            topic = course.topics.get(number=n)
            for vid, lang in items:
                url = f'https://www.youtube.com/watch?v={vid}'
                title, channel, err = oembed(vid)
                if err:
                    failed += 1
                    self.stderr.write(self.style.WARNING(f'  {n}-mavzu {vid}: {err}'))
                    continue
                if opts['tekshir']:
                    continue
                if Resource.objects.filter(course=course, kind='video', url__contains=vid).exists():
                    skipped += 1
                    continue
                Resource.objects.create(course=course, topic=topic, kind='video', title=title[:200], url=url,
                                        note=f'{channel} · {LANG[lang]}'[:300])
                added += 1
        total = sum(len(v) for v in fan.VIDEOS.values())
        self.stdout.write(self.style.SUCCESS(
            f'Jami {total} ta: qo‘shildi {added}, oldin bor edi {skipped}, ishlamadi {failed}.'))
