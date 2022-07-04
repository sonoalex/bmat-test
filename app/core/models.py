from django.db import models
import uuid

class Task(models.Model):
    '''
    Task Model hold related info
    '''
    celery_task_uuid = models.UUIDField(default = uuid.uuid4)
    type = models.CharField(max_length=255)
    raw_filename = models.CharField(max_length=255)
    raw_internal_filename = models.CharField(max_length=255)
    out_filename = models.CharField(max_length=255, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.raw_filename

    class Meta:
        db_table = "task"


