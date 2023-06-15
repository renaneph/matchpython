from django.db import models


class Testimonials(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField()
    upload_profile_picture = models.ImageField(
        upload_to='uploads/testimonials_picture/',
        null=True,
        blank=True,
        default=None,
    )
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
