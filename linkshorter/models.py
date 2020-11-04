from django.db import models


class WebSite(models.Model):
    full_link = models.TextField()
    short_link = models.CharField(max_length=10)

    def __str__(self):
        return self.short_link
