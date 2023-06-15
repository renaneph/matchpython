from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

from core.models.advisor import STATUS, file_path
from core.models.auxiliary_tables import Funding, CompanyIndustry, Region, CLevel

User = get_user_model()

REVENUE = (
    (1, "$0 - $100k"),
    (2, "$100k - $500k"),
    (3, "$500k - $1M"),
    (4, "$1M - $5M"),
    (5, "$5M - $10M"),
    (6, "$10M+")
)

PROFIT = (
    (1, "$0 - $100k"),
    (2, "$100k - $500k"),
    (3, "$500k - $1M"),
    (4, "$1M - $5M"),
    (5, "$5M+")
)

ADMIN_EVENTS = (
    (False, "No"),
    (True, "Yes")
)


class StartupUser(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS, default=0)
    who_am_I = models.CharField(max_length=20, default="Startup", blank=True)
    position = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    fintech = models.BooleanField()
    fintech_user = models.ManyToManyField(
        CompanyIndustry,
        related_name="fintech_user",
        blank=True
    )
    commerce_tech = models.BooleanField()
    commerce_tech_user = models.ManyToManyField(
        CompanyIndustry,
        related_name="commerce_tech_user",
        blank=True
    )
    gtm_strategy = models.BooleanField(default=False)
    fundraising = models.BooleanField()
    tech = models.BooleanField()
    human_capital = models.BooleanField()
    regions_user = models.ManyToManyField(
        Region,
        related_name="regions_user",
        blank=True
    )
    international = models.BooleanField()
    domestic = models.BooleanField()
    regions_international = models.ManyToManyField(
        Region,
        related_name="regions_international",
        blank=True
    )
    terms_conditions = models.BooleanField()
    admins_events = models.BooleanField(choices=ADMIN_EVENTS)
    describe_help = models.TextField()
    c_level_user = models.ManyToManyField(
        CLevel,
        related_name="c_level_user",
        blank=True
    )
    company_description = models.TextField()
    problem = models.TextField()
    solution = models.TextField()
    funding_id = models.ForeignKey(Funding, on_delete=models.CASCADE)
    annual_profit = models.IntegerField(choices=PROFIT)
    goals = models.IntegerField(choices=REVENUE)
    upload_deck = models.FileField(
        upload_to=file_path,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf'])
        ],
        null=True,
        blank=True
    )
    upload_profile_picture = models.ImageField(
        upload_to=file_path,
        null=True,
        blank=True
    )
    enable_match = models.BooleanField()
    functions_events = models.BooleanField()
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=1)

    def __str__(self):
        return f"{self.user_id.get_full_name()}"

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = StartupUser.objects.get(id=self.id)

            if this.upload_resume != self.upload_deck:
                this.upload_resume.delete(save=False)

            if this.upload_profile_picture != self.upload_profile_picture:
                this.upload_profile_picture.delete(save=False)

        except Exception as e:
            print(e)
            pass  # when new photo then we do nothing, normal case
        super(StartupUser, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # delete files from personal folder before delete your register
        try:
            if self.upload_deck:
                self.upload_deck.delete(save=False)

            if self.upload_profile_picture:
                self.upload_profile_picture.delete(save=False)

        except Exception as e:
            print(e)
            pass
        super(StartupUser, self).delete(*args, **kwargs)
