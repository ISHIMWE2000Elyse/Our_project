from django.db import models
from django.utils import timezone

class Report(models.Model):
    REPORT_TYPES = [
        ('production_summary', 'Production Summary'),
        ('quality_grading', 'Quality Grading'),
        ('order_performance', 'Order Performance'),
    ]
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES, unique=True)
    last_generated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.report_type} ({self.last_generated})"


class ProductionOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_production', 'In Production'),
        ('completed', 'Completed'),
    ]

    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.product_name} - {self.status}"

class QualityGrading(models.Model):
    product_name = models.CharField(max_length=100)
    graded_percentage = models.FloatField(default=0.0)
    graded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.product_name} - {self.graded_percentage}%"

class Order(models.Model):
    quality_grade = models.PositiveIntegerField(null=True, blank=True)
    inspector = models.CharField(max_length=100, null=True, blank=True)
