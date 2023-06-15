import os

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

from core.models.auxiliary_tables import Region, CLevel, CompanyIndustry

User = get_user_model()

STATUS = (
    (0, "New"),
    (1, "Pending Review"),
    (2, "Active"),
    (3, "Pending Update"),
    (4, "Inactive")
)

HOURS_INVEST = (
    (1, "1-2hrs/week"),
    (2, "3-5hrs/week"),
    (3, "5+hrs/week")
)

START_AT = (
    (1, "Immediately"),
    (2, "Between 1-2 months"),
    (3, "3+ months")
)

FRACTIONAL_C_LEVEL = (
    (False, "No"),
    (True, "Yes")
)


def file_path(instance, filename: str) -> str:
    """
    This function will save the user files
    @param instance: AdminUser, AdvisorUser or StartupUser
    @param filename: a string with name from the file
    @return: like 'uploads/Admin/9_rigel_cobb/profile_picture.png'
    """
    _, file_extension = os.path.splitext(filename)

    username = instance.user_id.get_full_name().replace(" ", "_").lower()

    dir_name = f'{instance.user_id_id}_{username}'
    file_name = 'document' if file_extension == '.pdf' else 'profile_picture'

    return f'uploads/{instance.who_am_I}/{dir_name}/{file_name}{file_extension}'


class AdvisorUser(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS, default=1)
    who_am_I = models.CharField(max_length=20, default="Advisor", blank=True)
    title = models.CharField(max_length=144)
    linkedin = models.CharField(max_length=50)
    commerce_tech = models.BooleanField()
    commerce_tech_user = models.ManyToManyField(
        CompanyIndustry,
        related_name="advisor_commerce_tech_user",
        blank=True
    )
    fintech = models.BooleanField()
    fintech_user = models.ManyToManyField(
        CompanyIndustry,
        related_name="advisor_fintech_user",
        blank=True
    )
    gtm_strategy = models.BooleanField(default=False)
    domestic = models.BooleanField()
    international = models.BooleanField()
    tech = models.BooleanField()
    fundraising = models.BooleanField()
    human_capital = models.BooleanField()
    regions_international = models.ManyToManyField(
        Region,
        related_name="advisor_regions_international",
        blank=True
    )
    description = models.TextField()
    terms_conditions = models.BooleanField()
    regions_user = models.ManyToManyField(Region, related_name="advisor_regions_user")
    highlight_profile_1 = models.CharField(max_length=500, default="")
    highlight_profile_2 = models.CharField(max_length=500, default="")
    highlight_profile_3 = models.CharField(max_length=500, default="")
    hours_invest = models.IntegerField(choices=HOURS_INVEST)
    fractional_c_level = models.BooleanField(choices=FRACTIONAL_C_LEVEL)
    c_level_user = models.ManyToManyField(CLevel, related_name="advisor_c_level_user", blank=True)
    start_at = models.IntegerField(choices=START_AT)
    upload_resume = models.FileField(
        upload_to=file_path,
        validators=[
            FileExtensionValidator(allowed_extensions=["pdf"])
        ],
        null=True,
        blank=True,
    )
    upload_profile_picture = models.ImageField(
        upload_to=file_path,
        null=True,
        blank=True
    )
    enable_match = models.BooleanField()
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=1)

    def __str__(self):
        return f"{self.user_id.get_full_name()}"

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = AdvisorUser.objects.get(id=self.id)

            if this.upload_resume != self.upload_resume:
                this.upload_resume.delete(save=False)

            if this.upload_profile_picture != self.upload_profile_picture:
                this.upload_profile_picture.delete(save=False)

        except Exception as e:
            print(e)
            pass  # when new photo then we do nothing, normal case
        super(AdvisorUser, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # delete files from personal folder before delete your register
        try:
            if self.upload_resume:
                self.upload_resume.delete(save=False)

            if self.upload_profile_picture:
                self.upload_profile_picture.delete(save=False)

        except Exception as e:
            print(e)
            pass
        super(AdvisorUser, self).delete(*args, **kwargs)
