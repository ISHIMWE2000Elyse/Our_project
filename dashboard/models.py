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
    
    