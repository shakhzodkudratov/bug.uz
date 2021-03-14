from datetime import date, timedelta

from django.conf import settings
from django.db import models
import random
import uuid


chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'


def generate_name():
    name = ''
    for i in range(6):
        index = random.randint(0, len(chars))
        name += chars[index]
    return name


class Url(models.Model):
    private_name = models.CharField('Statistika ID', max_length=36, null=False, blank=False)  # b.uz/stats/<uuid>
    name = models.CharField('Qisqa havola', max_length=6, null=False, blank=False)  # b.uz/<123456>
    url = models.CharField('Havola', max_length=1024, null=False, blank=False)
    created_at = models.DateTimeField(auto_now=True)

    @property
    def short_url(self):
        return f'{settings.HOST}/{self.name}'

    @property
    def stats_total(self):
        return self.urlstat_set.count()

    @property
    def stats_week(self):
        week_ago = date.today() - timedelta(days=7)
        return self.urlstat_set.filter(created_at__gte=week_ago).count()

    @property
    def stats_day(self):
        day_ago = date.today() - timedelta(days=1)
        return self.urlstat_set.filter(created_at__gte=day_ago).count()

    def save(self, *args, **kwargs):
        if not self.private_name:
            name = str(uuid.uuid4())

            while Url.objects.filter(private_name=name).exists():
                name = str(uuid.uuid4())

            self.private_name = name

        if not self.name:
            name = generate_name()

            while Url.objects.filter(name=name).exists():
                name = generate_name()

            self.name = name

        super().save(*args, **kwargs)

    def __str__(self):
        return f'[{self.id}] {self.name} - - - {self.private_name}'


class UrlStat(models.Model):
    url = models.ForeignKey(Url, on_delete=models.CASCADE)
    ip_address = models.CharField('IP manzili', max_length=15, null=False, blank=False)
    referer = models.CharField('Referal manzili', help_text='Qaysi manzildan kelganligi', max_length=512, null=True,
                               blank=True)
    user_agent = models.CharField('User agent', max_length=256, null=False, blank=False)
    created_at = models.DateTimeField(auto_now=True)
