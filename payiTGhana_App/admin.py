from django.contrib import admin
from .models import Department
from .models import Faculty
from import_export import resources
from import_export.admin import ImportExportModelAdmin

admin.site.register(Department)
admin.site.register(Faculty)



class DepartmentResource(ImportExportModelAdmin):

    class Meta:
        model = Department
        fields = ('id', 'name', 'year', 'faculty')
        export_order = ('id', 'name', 'year', 'faculty',)


class DepartmentAdmin(ImportExportModelAdmin):
    resource_class = DepartmentResource