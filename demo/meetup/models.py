from django.db import models


class MeetupGroup(models.Model):
    uid = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255)
    urlname = models.CharField(max_length=255, unique=True)
    link = models.URLField()
    members_count = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.urlname

    def _repr_html_(self):
        return f"<h1>{self.name}</h1>"

class MeetupMember(models.Model):
    uid = models.PositiveIntegerField(db_index=True)
    name = models.CharField(max_length=255)
    photo = models.URLField(null=True)

    def __str__(self):
        return self.name or self.uid


class MeetupEvent(models.Model):
    uid = models.PositiveIntegerField(db_index=True)
    group = models.ForeignKey(MeetupGroup, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    event_date = models.DateField()
    rsvp_count = models.PositiveSmallIntegerField()
    link = models.URLField()
    venue = models.CharField(max_length=255)

    attendants = models.ManyToManyField(MeetupMember, related_name="events")

    def __str__(self):
        return self.name
