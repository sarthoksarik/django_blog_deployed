from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # upvotes will be similar to 'like' in facebook and toggleable
    upvotes = models.ManyToManyField(
        User, related_name='upvoter', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    # def get_total_likes(self):
    #     return self.upvotes.count()


class Announcements(models.Model):
    """ Model for announcements on the sidebar."""
    title = models.CharField(max_length=100)
    detail = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
