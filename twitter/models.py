from django.db import models

# Create your models here.

class twitter_available_trends(models.Model):
    place = models.CharField(max_length=100)
    placetype_code = models.IntegerField()
    placetype_name = models.CharField(max_length=100)
    parentid = models.IntegerField()
    country = models.CharField(max_length=100)
    woeid = models.IntegerField()
    countrycode = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "twitter_available_trends"


class twitter_trends_place(models.Model):
    trend_name = models.CharField(max_length=500)
    trend_url = models.CharField(max_length=10000)
    trend_query = models.CharField(max_length=500)
    trend_count = models.IntegerField(null=True)
    trend_woeid = models.IntegerField()
    trend_created_at = models.DateTimeField()
    trend_as_of = models.DateTimeField()

    class Meta:
        db_table = "twitter_trends_place"
