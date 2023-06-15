from django.db import models

from core.models.advisor import AdvisorUser
from core.models.startup import StartupUser

class InterestExpressed(models.Model):
    advisor = models.ForeignKey(AdvisorUser, on_delete=models.CASCADE)
    startup = models.ForeignKey(StartupUser, on_delete=models.CASCADE)
    reason_i_know_one = models.BooleanField(default=False)
    reason_i_am_interested = models.BooleanField(default=False)
    reason_other = models.BooleanField(default=False)
    reason_description = models.TextField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{:%B %d, %Y}'.format(self.date)
