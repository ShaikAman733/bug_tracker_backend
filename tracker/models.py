from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMINISTRATOR', 'Administrator'),
        ('DEVELOPER', 'Developer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='DEVELOPER')
    designation = models.CharField(max_length=100, blank=True, null=True)
    
    # Django's AbstractUser already includes email, password, and is_active

    def __str__(self):
        return self.username

class Project(models.Model):
    PRIORITY_CHOICES = [('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')]
    STATUS_CHOICES = [('Planning', 'Planning'), ('Active', 'Active'), ('Completed', 'Completed')]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    repository_url = models.URLField(max_length=255, blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Planning')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Bug(models.Model):
    SEVERITY_CHOICES = [('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'), ('Critical', 'Critical')]
    PRIORITY_CHOICES = [('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')]
    STATUS_CHOICES = [('Open', 'Open'), ('In Progress', 'In Progress'), ('Resolved', 'Resolved'), ('Closed', 'Closed')]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='bugs')
    developer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_bugs')
    
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='Medium')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Open')
    
    due_date = models.DateField(blank=True, null=True)
    resolution_comment = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class BugAttachment(models.Model):
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name='attachments')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    file_url = models.URLField(max_length=500)
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action_type = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)