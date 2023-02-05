from django.contrib import admin
# We do this so that all these models can be seen in the admin panel
from .models import Syllabus, FollowersCount, Assignment

# Register your models here.
admin.site.register(Syllabus)
admin.site.register(Assignment)
admin.site.register(FollowersCount)