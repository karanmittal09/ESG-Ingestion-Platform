from django.db import models
from organizations.models import Organization


class DataSource(models.Model):

    SOURCE_TYPES = [
        ('SAP', 'SAP'),
        ('UTILITY', 'UTILITY'),
        ('TRAVEL', 'TRAVEL'),
    ]

    INGESTION_METHODS = [
        ('CSV', 'CSV'),
        ('API', 'API'),
        ('MANUAL', 'MANUAL'),
    ]

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='data_sources'
    )

    source_type = models.CharField(
        max_length=50,
        choices=SOURCE_TYPES
    )

    ingestion_method = models.CharField(
        max_length=50,
        choices=INGESTION_METHODS
    )

    uploaded_by = models.CharField(max_length=255)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    file_name = models.CharField(
        max_length=255,
        blank=True
    )

    def __str__(self):
        return f"{self.organization.name} - {self.source_type}"


class RawRecord(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'PENDING'),
        ('PROCESSED', 'PROCESSED'),
        ('FAILED', 'FAILED'),
    ]

    datasource = models.ForeignKey(
        DataSource,
        on_delete=models.CASCADE,
        related_name='raw_records'
    )

    raw_payload = models.JSONField()

    row_number = models.IntegerField()

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    parse_errors = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Row {self.row_number} - {self.status}"