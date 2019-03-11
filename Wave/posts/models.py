from django.db import models
from django.conf import settings
from django.urls import reverse
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from users.models import User
# Create your models here.



def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


class PostManager(models.Manager):
    def all(self, *args, **kwargs):
        query_set = super(PostManager, self).order_by("-timestamp")
        return query_set
    
    def filter_by_public(self, *args, **kwargs):
        query_set = super(PostManager, self).filter(privacy=0).order_by("-timestamp")
        return query_set

    # def filter_by_private(self, *args, **kwargs):
    #     query_set = super(PostManager, self).filter(privacy=1).order_by("-timestamp")
    #     return query_set

    def filter_by_friends(self, *args, **kwargs):
        followers = User.objects.filter(follower__user2=user.id, is_active=True)
        following = User.objects.filter(followee__user1=user.id, is_active=True)
        friends = following & followers
        query_set = super(PostManager, self).filter(privacy=2, user__in=friends).order_by("-timestamp")
        return query_set

    def filter_by_foaf(self, *args, **kwargs):
        friends_followers = User.objects.filter(follower__user2__in=friends, is_active=True)
        friends_following = User.objects.filter(followee__user1__in=friends, is_active=True)
        friends_of_friends = friends_followers &  friends_following
        query_set = super(PostManager, self).filter(privacy=3, user__in=friends_of_friends).order_by("-timestamp")
        return query_set

    def filter_by_only_me(self, *args, **kwargs):
        user = kwargs.pop('user')
        print("This is a user", user)
        query_set = super(PostManager, self).filter(privacy=5, user=user).order_by("-timestamp")
        return query_set
    

    def filter_user_visible_posts(self, user, *args, **kwargs):
        only_me_posts = super(PostManager, self).filter(privacy=5, user=user)
        public_posts = super(PostManager, self).filter(privacy=0)


        private_posts = user.accessible_posts.all()

        followers = User.objects.filter(follower__user2=user.id, is_active=True)
        following = User.objects.filter(followee__user1=user.id, is_active=True)
        friends = following & followers
        friends_posts = super(PostManager, self).filter(privacy=2, user__in=friends)



        friends_followers = User.objects.filter(follower__user2__in=friends, is_active=True)
        friends_following = User.objects.filter(followee__user1__in=friends, is_active=True)
        friends_of_friends = friends_followers &  friends_following
        friends_of_friends_posts = super(PostManager, self).filter(privacy=3, user__in=friends_of_friends)

        server_only_posts =  super(PostManager, self).filter(privacy=4, user = user)


        all_posts = only_me_posts | public_posts | friends_posts | friends_of_friends_posts | private_posts | server_only_posts
        all_posts = all_posts.filter(unlisted=False)
        return all_posts.order_by('-timestamp')

    def filter_server_posts(self, user, *args, **kwargs):
        all_posts = self.filter_user_visible_posts(user)
        all_posts = all_posts.exclude(privacy=4)
        return all_posts.order_by('-timestamp')

    

class Post(models.Model):

    PUBLIC = 0
    PRIVATE = 1
    FRIENDS = 2
    FOAF = 3
    ONLY_SERVER = 4
    ONLY_ME = 5

    Privacy = (
        (PUBLIC, 'PUBLIC'),
        (PRIVATE, 'PRIVATE'),
        (FRIENDS, 'ONLY FRIENDS'),
        (FOAF, 'FRIEND OF A FRIEND'),
        (ONLY_SERVER, 'SERVER ONLY'),
        (ONLY_ME, 'ONLY ME')
    )

    POST = "Post"
    Status = {
        (POST, 'Post')
    }

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    status = models.CharField(max_length=6, choices=Status, default=POST)
    content = models.TextField()
    image = models.FileField(upload_to=upload_location, null=True, blank=True)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    privacy = models.IntegerField(choices=Privacy, default=PUBLIC)
    unlisted = models.BooleanField(default=False)
    accessible_users =  models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="accessible_posts", blank=True)
    objects = PostManager()


    def __str__(self):
        return str(self.user.username)

    """
        Redirects to the individaul posts.
    """
    def get_detail_absolute_url(self):
        return reverse("posts-detail", kwargs={"id": self.id})
        # return "/posts/%s/" % (self.id)

    def get_delete_absolute_url(self):
        return reverse("posts-delete", kwargs={"id": self.id})

    def get_absolute_url(self):
        return reverse("home")
    
    def get_edit_absolute_url(self):
        return reverse("posts-update", kwargs={"id": self.id})

    # Images
    def decodeImage(self, image):
        pass
    
    def encodeImage(self, image):
        pass

    @property
    def comments(self):
        instance = self
        query_set = Comment.objects.filter_by_instance(instance)
        return query_set

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type
         


