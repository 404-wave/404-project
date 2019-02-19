from django.db import models
from django.conf import settings
from django.urls import reverse
# Create your models here.


def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


class Post(models.Model):

    PUBLIC = 0
    PRIVATE = 1
    FRIENDS = 2
    FOAF = 3
    ONLY_SERVER = 4
    ONLY_ME = 5

    Privacy = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Only certain friends'),
        (FRIENDS, 'Only friends'),
        (FOAF, 'Friend of a friend'),
        (ONLY_SERVER, 'Server wide'),
        (ONLY_ME, 'Only me')
    )

    POST = "Post"
    Status = {
        (POST, 'Post')
    }

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    # Might change this. Seems like a stupid way to implement
    status = models.CharField(max_length=6, choices=Status, default=POST)
    content = models.TextField()
    image = models.FileField(upload_to=upload_location, null=True, blank=True)
    # height_field = models.IntegerField(default=0)
    # width_field = models.IntegerField(default=0)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    privacy = models.IntegerField(choices=Privacy, default=PUBLIC)
    unlisted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username)

    # {%url "detail" id=obj.id %}
    """
        Redirects to the individaul posts.
    """

    def get_detail_absolute_url(self):
        return reverse("detail", kwargs={"id": self.id})
        # return "/posts/%s/" % (self.id)

    def get_delete_absolute_url(self):
        return reverse("delete", kwargs={"id": self.id})

    def get_absolute_url(self):
        return reverse("home")
