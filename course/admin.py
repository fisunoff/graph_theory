from django.contrib import admin
from django.db.models import TextField
from martor.widgets import AdminMartorWidget

from course import models


class StepAdmin(admin.ModelAdmin):
    formfield_overrides = {
        TextField: {'widget': AdminMartorWidget},
    }


admin.site.register(models.Course)
admin.site.register(models.Lesson)
admin.site.register(models.Step, StepAdmin)
admin.site.register(models.Task)
admin.site.register(models.HomeWork)

