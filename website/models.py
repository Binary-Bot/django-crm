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

    def __str__(self):
        return(f"{self.client_description} {self.client_num}")