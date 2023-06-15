from django.db import models
from django.core.validators import FileExtensionValidator


class TermsConditions(models.Model):
    name = models.CharField(max_length=100)
    upload_termsconditions = models.FileField(
        upload_to='uploads/terms_conditions/',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf'])
        ],
        null=True,
        blank=True
    )
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
