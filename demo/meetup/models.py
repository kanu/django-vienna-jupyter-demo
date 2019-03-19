from django.db import models
from django_pandas.managers import DataFrameManager


class MeetupGroup(models.Model):
    uid = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255)
    urlname = models.CharField(max_length=255, unique=True)
    link = models.URLField()
    members_count = models.PositiveSmallIntegerField(default=0)
    description = models.TextField(null=True)

    objects = DataFrameManager()

    def __str__(self):
        return self.urlname

    def _repr_html_(self):
        return f"<h3>{self.name}</h3>"


class MeetupMember(models.Model):
    uid = models.PositiveIntegerField(db_index=True)
    name = models.CharField(max_length=255)
    photo = models.URLField(null=True)

    objects = DataFrameManager()

    def __str__(self):
        return self.name or self.uid

    def _repr_html_(self):
        return f'<span>{self.name}</span><img src="{self.photo}" alt="{self.name}" >'


class MeetupEvent(models.Model):
    uid = models.PositiveIntegerField(db_index=True)
    group = models.ForeignKey(
        MeetupGroup, on_delete=models.CASCADE, related_name="events"
    )

    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    event_date = models.DateField()
    rsvp_count = models.PositiveSmallIntegerField()
    link = models.URLField()
    venue = models.CharField(max_length=255)

    attendants = models.ManyToManyField(MeetupMember, related_name="events")

    objects = DataFrameManager()

    def __str__(self):
        return self.name

    def _repr_html_(self):
        return f'<a href="{self.link}" >{self.name}</a>'
