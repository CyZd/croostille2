from django.db import models

from django.urls import reverse

from memberships.models import Membership

# Create your models here.
class Challenge(models.Model):
    slug=models.SlugField()
    title=models.CharField(max_length=120)
    description=models.TextField()
    allowed_memberships=models.ManyToManyField(Membership)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("courses:detail", kwargs={"slug": self.slug})

    @property
    def weeks(self):
        return self.week_set.all().order_by('position')

class Week(models.Model):
    slug=models.SlugField()
    title=models.CharField(max_length=120)
    challenge=models.ForeignKey(Challenge, on_delete=models.SET_NULL, null=True)
    position=models.IntegerField()
    description=models.TextField()
    video_url=models.CharField(max_length=200)
    thumbnail=models.ImageField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("courses:week_detail", kwargs={
            'challenge_slug': self.challenge.slug,
            'week_slug':self.slug
        })

class Module(models.Model):
    slug=models.SlugField()
    title=models.CharField(max_length=120)
    week=models.ForeignKey(Week, on_delete=models.SET_NULL, null=True)
    position=models.IntegerField()
    description=models.TextField()
    video_url=models.CharField(max_length=200)
    thumbnail=models.ImageField()

    def __str__(self):
        return self.title