from django.db import models


class Server(models.Model):
    url = models.CharField(max_length=255, null=False, blank=False)
    name = models.CharField(max_length=50, null=True, blank=False)
    order = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Server"
        verbose_name_plural = "Servers"
