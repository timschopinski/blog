from django.db import models
from django.urls import reverse
from datetime import date
from django.utils.text import slugify
# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="posts", null=True, blank=True)
    date = models.DateField(default=date.today(), editable=False)
    author = models.CharField(max_length=100, null=True)
    slug = models.SlugField(blank=True, null=False, db_index=True)
    description = models.CharField(max_length=200)
    content = models.CharField(max_length=500)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} {self.author}"

    def get_absolute_url(self):
        return reverse("post-detail-page", args=[self.slug])

class Comment(models.Model):
    user_name = models.CharField(max_length=120)
    user_email = models.EmailField()
    text = models.TextField(max_length=400)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")