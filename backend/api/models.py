from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import json

class DatasetUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dataset_uploads', null=True, blank=True)
    filename = models.CharField(max_length=255)
    upload_date = models.DateTimeField(default=timezone.now)
    file_size = models.IntegerField()
    equipment_count = models.IntegerField()
    summary_data = models.JSONField()
    
    class Meta:
        ordering = ['-upload_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.filename} - {self.upload_date.strftime('%Y-%m-%d %H:%M')}"
    
    @classmethod
    def cleanup_old_records_for_user(cls, user):
        user_records = cls.objects.filter(user=user)
        if user_records.count() > 5:
            old_records = user_records[5:]
            for record in old_records:
                record.delete()
    
    def get_summary_stats(self):
        if self.summary_data and 'summary_metrics' in self.summary_data:
            return self.summary_data['summary_metrics']
        return None