from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
import datetime

class Administrator(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    image = models.TextField(max_length=255)

    class Meta:
        db_table = 'administrator'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        slug = slugify(self.name)
        return reverse('funds_by_administrator', kwargs={'slug': slug})

class Fund(models.Model):
    administrator = models.ForeignKey(Administrator)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'fund'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        fund_slug = slugify(self.name)
        administrator_slug = slugify(self.administrator.name)
        return reverse('fund_detail', kwargs={'administrator_slug': administrator_slug, 'slug': fund_slug})

    def get_last_day(self):
        try:
            return self.day_set.all()[0]
        except IndexError:
            return None

    def get_line_data(self, date):
        response = '{"cols":[{"id":"date","label":"Fecha","type":"date"},{"id":"nav","label":"Valor Cuota","type":"number"}],"rows":['
        rows = []
        days = self.day_set.values('date', 'value').filter(date__gte = date)
        for day in days:
            rows.append('{"c":[{"v":"%s"},{"v":%s}]}' % (day['date'], day['value']))
        response += ','.join(rows)
        response += ']}'
        return response

    def get_profitability(self):
        finish_at = self.day_set.all().aggregate(models.Max('date'))['date__max']
        start_at = finish_at - datetime.timedelta(days=365)
        start_date = self.day_set.get(date = start_at)
        finish_date = self.day_set.get(date = finish_at)
        return ((finish_date.value-start_date.value)/start_date.value) * 100

class Day(models.Model):
    date = models.DateField()
    fund = models.ForeignKey(Fund)
    value = models.FloatField()

    class Meta:
        db_table = 'day'
        ordering = ['-date']
        unique_together = ('date', 'fund')
