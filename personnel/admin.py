from django.contrib import admin

from personnel.models import *


class EmployeInline(admin.TabularInline):
    model = Employe
    extra = 0
    verbose_name = "Employé"
    verbose_name_plural = "Employés"


class EmployePhotoInline(admin.TabularInline):
    model = EmployePhoto
    extra = 1
    verbose_name = "Photo"
    verbose_name_plural = "Photos"


@admin.register(Employe)
class ProductAdmin(admin.ModelAdmin):
    inlines = [EmployePhotoInline, ]
    list_display = ['name', 'departement', 'poste', 'code_qr', 'visuel']
    list_filter = ['departement', 'poste']
    search_fields = ['name', 'departement', 'poste']


@admin.register(Departement)
class CategorieAdmin(admin.ModelAdmin):
    inlines = [EmployeInline, ]


@admin.register(EmployePhoto)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['employe', 'visuel']
    list_filter = ['employe']
    list_per_page = 12
    list_max_show_all = 20
