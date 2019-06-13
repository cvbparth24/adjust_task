from django.db import models


# Create your models here.
class PerformanceMetrics(models.Model):
    recorded_date = models.DateField(verbose_name='Recorded Date', null=True, blank=True, default=None)
    channel = models.CharField(verbose_name='Channel', null=True, blank=True, max_length=200, default=None)
    country = models.CharField(verbose_name='Country Name', null=True, blank=True, max_length=20, default=None)
    os = models.CharField(verbose_name='Channel', null=True, blank=True, max_length=20, default=None)
    impressions = models.IntegerField(default=None, null=True, blank=True)
    clicks = models.IntegerField(default=None, null=True, blank=True)
    installs = models.IntegerField(default=None, null=True, blank=True)
    spend = models.FloatField(verbose_name='Spend', null=True, blank=True, default=None)
    revenue = models.FloatField(verbose_name='Revenue', null=True, blank=True, default=None)
