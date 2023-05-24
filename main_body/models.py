from django.db import models
from django.urls import reverse, reverse_lazy


class Menu(models.Model):
    name = models.CharField("Name", max_length=100)
    url = models.CharField("Url", max_length=255, blank=True, unique=True)
    parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="child"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("pk",)
        verbose_name = verbose_name_plural = "Menu"

    def get_absolute_url(self):
        return reverse(self.url) if self.url else reverse_lazy("home")

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
        *args,
        **kwargs,
    ) -> None:
        super().save(*args, **kwargs)
        if self.parent:
            self.set_relation()
        return

    def set_relation(self) -> None:
        relations_of_parent = MenuRelation.objects.filter(
            from_parent=self.parent
        ).values_list("to_child_id")
        relations = []
        for to_child_id in relations_of_parent:
            relations.append(MenuRelation(to_child_id=to_child_id[0], from_parent=self))
        relations.append(MenuRelation(to_child=self.parent, from_parent=self))
        MenuRelation.objects.bulk_create(relations)


class MenuRelation(models.Model):
    to_child = models.ForeignKey(
        "Menu", on_delete=models.CASCADE, related_name="relations_with_parent"
    )
    from_parent = models.ForeignKey(
        "Menu", on_delete=models.CASCADE, related_name="relations_with_child"
    )

    class Meta:
        verbose_name = "MenuRelation"
        verbose_name_plural = "MenuRelations"

    def __str__(self):
        return f"From {self.from_parent} to {self.to_child}"


class Weather(models.Model):
    ip = models.CharField(max_length=50, default="unavailable")
    address = models.CharField(max_length=250, default="unavailable")
    temp = models.IntegerField(default=0)
    feels_like = models.IntegerField(default=0)
    humidity = models.IntegerField(default=0)
    wind = models.IntegerField(default=0)
    clouds = models.CharField(max_length=25, default="unavailable")

    def __str__(self):
        return (
            f"Location: {self.address} {self.temp} {chr(176)}C | \n"
            f"Feels: {self.feels_like} {chr(176)}C | \n"
            f"Humidity: {self.humidity}% | \n"
            f"Wind: {self.wind}m/s | \n"
            f"Clouds: {self.clouds}"
        )

    class Meta:
        verbose_name_plural = "weather"


class PageVisits(models.Model):
    url = models.CharField(max_length=255, unique=True, default=None)
    count = models.PositiveIntegerField(default=0)
    session_id = models.CharField(max_length=150, db_index=True)

    class Meta:
        verbose_name_plural = "Page Visits"

    def __str__(self):
        return f"Count of visits to page: {self.url} - {self.count}"
