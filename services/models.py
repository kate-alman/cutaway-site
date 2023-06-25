import random
import string

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class News(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL"
    )
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="photos/%Y/%m/%d/",
        blank=True,
        null=True,
        default="/photos/non_poster.png",
    )
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    tag = models.ForeignKey("Tag", on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)

    class Meta:
        ordering = ["-time_create"]
        verbose_name_plural = "news"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})

    def validate_slug(self) -> None:
        """Checks that the new link is unique or changes it."""
        symbols = string.ascii_letters + "".join(map(str, range(0, 10)))
        already_exist = News.objects.filter(slug=self.slug).last()
        # if the new reference is not unique, then changes it
        while already_exist:
            self.slug = (
                self.slug
                if not already_exist
                else (
                    self.slug + "".join(random.choice(symbols) for _ in range(10))
                    if self.slug == already_exist.slug
                    else self.slug
                )
            )
            already_exist = News.objects.filter(slug=self.slug).last()

    def save(self, *args, **kwargs):
        if self.pk:
            new_post, create = News.objects.get_or_create(pk=self.pk)
        else:
            value = self.title
            # creates a link for a new post
            self.slug = slugify(
                value.translate(
                    str.maketrans(
                        "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
                        "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA",
                    )
                )
            )
            # checks that the new link is unique
            self.validate_slug()
        super().save(*args, **kwargs)

    def get_delete_url(self):
        return reverse("post:delete", args=(self.pk,))


class Tag(models.Model):
    name = models.CharField(
        max_length=100, db_index=True, unique=True, verbose_name="Tag"
    )

    def __str__(self):
        return self.name
