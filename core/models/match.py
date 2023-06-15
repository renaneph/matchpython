from django.db import models

from core.models.advisor import AdvisorUser
from core.models.startup import StartupUser


def file_location(instance, file):
    return f"uploads/match/{instance.match_id.id}/{file}"

class Match(models.Model):
    advisor = models.ForeignKey(AdvisorUser, on_delete=models.CASCADE)
    startup = models.ForeignKey(StartupUser, on_delete=models.CASCADE)
    score = models.FloatField(default=1.0)
    max_score = models.FloatField(default=1.0)
    cases = models.JSONField(blank=True, null=True)
    closed = models.BooleanField(default=False)
    connect_with_startup = models.BooleanField(default=False)
    connect_with_advisor = models.BooleanField(default=False)

class MatchFiles(models.Model):
    match_id = models.ForeignKey("Match", on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=file_location,
        null=True,
        blank=True
    )
    filename = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
