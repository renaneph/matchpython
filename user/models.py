from django.contrib.auth import get_user_model
from django.db import models

from core.models.advisor import file_path

User = get_user_model()


class AdminUser(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    who_am_I = models.CharField(max_length=20, default="Admin", blank=True)
    permissions = models.BooleanField(default=False)
    position = models.CharField(max_length=30)
    upload_profile_picture = models.ImageField(
        upload_to=file_path,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user_id.get_full_name()

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = AdminUser.objects.get(id=self.id)

            if this.upload_profile_picture != self.upload_profile_picture:
                this.upload_profile_picture.delete(save=False)

        except Exception as e:
            print(e)
            pass  # when new photo then we do nothing, normal case
        super(AdminUser, self).save(*args, **kwargs)
