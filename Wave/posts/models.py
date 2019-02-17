from django.db import models
from django.conf import settings
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    content = models.TextField()
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    # TODO: Images
    # height_field = models.IntegerField(default=0)
    # width_field = models.IntegerField(default=0)
    # image = models.ImageField(upload_to=upload_location,
    #                           null=True,
    #                           blank=True,
    #                           height_field="height_field",
    #                           width_field="width_field")

    def __str__(self):
        return str(self.content)
