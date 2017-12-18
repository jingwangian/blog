from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # The Dahl-specific manager.

    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.strftime('%m'),
                                                 self.publish.strftime('%d'),
                                                 self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=True)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)

# Statistic visit times by client address


class VisitorStat(models.Model):
    ip_addr = models.CharField(max_length=60, db_index=True)
    user_agent = models.CharField(max_length=255)
    referrer = models.CharField(max_length=255)
    total_visit_count = models.IntegerField()
    today_visit_count = models.IntegerField()
    last_visit_date = models.DateTimeField()

    def __str__(self):
        return '{}---{}---{}---{}'.format(self.ip_addr,
                                       self.total_visit_count,
                                       self.today_visit_count,
                                       self.last_visit_date)

# Statistic visit times by title


class TitleStat(models.Model):
    title = models.CharField(max_length=250, db_index=True)
    request_path = models.CharField(max_length=255)
    total_visit_count = models.IntegerField()
    today_visit_count = models.IntegerField()
    last_visit_date = models.DateTimeField()

    def __str__(self):
        return '{}---{}---{}---{}'.format(self.title,
                                       self.total_visit_count,
                                       self.today_visit_count,
                                       self.last_visit_date)
