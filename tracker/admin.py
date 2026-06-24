from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Project, Bug, BugAttachment, ActivityLog

# Registering the custom User model
admin.site.register(User, UserAdmin)

# Registering the rest of the BugTracker models
admin.site.register(Project)
admin.site.register(Bug)
admin.site.register(BugAttachment)
admin.site.register(ActivityLog)