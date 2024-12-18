import uuid
from django.db import models
from django.conf import settings
from projects.models import Project


class Issue(models.Model):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'

    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]

    BUG = 'BUG'
    FEATURE = 'FEATURE'
    TASK = 'TASK'

    TAG_CHOICES = [
        (BUG, 'Bug'),
        (FEATURE, 'Feature'),
        (TASK, 'Task'),
    ]

    TODO = 'To Do'
    IN_PROGRESS = 'In Progress'
    FINISHED = 'Finished'

    STATUS_CHOICES = [
        (TODO, 'To Do'),
        (IN_PROGRESS, 'In Progress'),
        (FINISHED, 'Finished'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    tag = models.CharField(max_length=20, choices=TAG_CHOICES, default=BUG)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default=LOW)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=TODO)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authored_issues')
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issues')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
