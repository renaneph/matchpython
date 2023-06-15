from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=30)
    points = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class CompanyDomain(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class CompanyIndustry(models.Model):
    name = models.CharField(max_length=30)
    domain = models.ForeignKey(CompanyDomain, on_delete=models.CASCADE)
    points = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Funding(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class CLevel(models.Model):
    name = models.CharField(max_length=30)
    points = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class MatchKeysPoints(models.Model):
    gtm_name = models.CharField(max_length=30, default="GTM-Strategy")
    gtm_points = models.DecimalField(max_digits=5, decimal_places=2, default=5.0)
    tech_name = models.CharField(max_length=30, default="Tech")
    tech_points = models.DecimalField(max_digits=5, decimal_places=2, default=10.0)
    fundraising_name = models.CharField(max_length=30, default="Fundraising")
    fundraising_points = models.DecimalField(max_digits=5, decimal_places=2, default=15.0)

    def __str__(self):
        return self.gtm_name, self.tech_name, self.fundraising_name
