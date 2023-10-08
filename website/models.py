from django.db import models


# Create your models here.
class Record(models.Model):
    year = models.IntegerField()
    attorney = models.CharField(max_length=50)
    client_description = models.CharField(max_length=500)
    matter_desc = models.CharField(max_length=500)
    matter_only = models.BooleanField(max_length=2)
    client_num = models.IntegerField()
    matter_num = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=50)

    class Meta:
        ordering = ['-timestamp', '-matter_num']

    def __str__(self):
        return f"{self.client_num} - {self.matter_num} - {self.client_description} - {self.matter_desc}"
