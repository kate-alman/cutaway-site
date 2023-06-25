from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


User._meta.get_field("email")._unique = True   # when registering a new user, it monitors the uniqueness of mail


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, blank=True, unique=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(
        upload_to="user_photos/%Y/%m/%d/",
        blank=True,
        default="/user_photos/non_photo.png",
    )
    favorites = models.ManyToManyField(
        "self",
        through="FavoriteRelationship",
        symmetrical=False,
        related_name="favorite_relationship",
    )

    def __str__(self):
        return self.nickname

    def add_relationship(self, user: "Profile") -> "FavoriteRelationship":
        relationship, created = FavoriteRelationship.objects.get_or_create(
            from_user=self, to_user=user
        )
        return created

    def remove_relationship(self, user: "Profile") -> None:
        FavoriteRelationship.objects.filter(from_user=self, to_user=user).delete()
        return


class FavoriteRelationship(models.Model):
    """Many-to-many relationship to store blog user subscriptions."""
    from_user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="from_people"
    )
    to_user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="to_people"
    )

    def __str__(self):
        return f"From {self.from_user} to {self.to_user}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Automatically creates a profile when a new user is created."""
    if created:
        Profile.objects.create(user=instance, nickname=instance.username)
    instance.profile.save()
