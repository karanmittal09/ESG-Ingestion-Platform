from django.db import models
from organizations.models import Organization
from ingestion.models import RawRecord


class EmissionRecord(models.Model):

    SCOPE_CHOICES = [
        ('SCOPE1', 'SCOPE1'),
        ('SCOPE2', 'SCOPE2'),
        ('SCOPE3', 'SCOPE3'),
    ]

    REVIEW_STATUS = [
        ('PENDING', 'PENDING'),
        ('APPROVED', 'APPROVED'),
        ('REJECTED', 'REJECTED'),
    ]

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='emission_records'
    )

    raw_record = models.ForeignKey(
        RawRecord,
        on_delete=models.CASCADE,
        related_name='emission_records'
    )

    scope = models.CharField(
        max_length=20,
        choices=SCOPE_CHOICES
    )

    activity_type = models.CharField(
        max_length=100
    )

    quantity = models.FloatField()

    normalized_unit = models.CharField(
        max_length=50
    )

    emission_factor = models.FloatField()

    co2e = models.FloatField()

    suspicious_flag = models.BooleanField(
        default=False
    )

    review_status = models.CharField(
        max_length=20,
        choices=REVIEW_STATUS,
        default='PENDING'
    )

    locked = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.activity_type} - {self.co2e} kgCO2e"