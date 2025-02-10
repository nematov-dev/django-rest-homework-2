from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class PostsModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="posts")
    slug = models.SlugField(unique=True, null=True)
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, **kwargs):
        if not self.slug:
            original_slug = slugify(self.title)
            slug = original_slug
            count = 0
            while PostsModel.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(**kwargs)

    def __str__(self):
        return self.title
