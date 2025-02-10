from django.contrib import admin

# Register your models here.
# adminle alakalı işlemler burada

from .models import Todos, Projects
admin.site.register(Todos)
admin.site.register(Projects)