from django.contrib import admin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Category, Year, MSRSeasonYear, Style, Image, Employee

def delete_all_entries(modeladmin, request, queryset):
    model = modeladmin.model
    count, _ = model.objects.all().delete()
    messages.success(request, _(f"Successfully deleted {count} entries from {model._meta.verbose_name_plural}."))

delete_all_entries.short_description = "Delete all entries"

# Custom Admin for Employee
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'created_at', 'updated_at')
    search_fields = ('username', 'email')

# Admin for Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'section','order_priority','cover_image','created_at', 'updated_at')
    list_filter = ('section',)
    search_fields = ('name',)
    ordering = ('parent', 'order_priority')  # Ordering categories based on parent and order priority

# Admin for Year
class YearAdmin(admin.ModelAdmin):
    list_display = ('year', 'created_at', 'updated_at')
    search_fields = ('year',)

# Admin for MSRSeasonYear
class MSRSeasonYearAdmin(admin.ModelAdmin):
    list_display = ('season', 'year', 'created_at', 'updated_at')
    search_fields = ('season__name', 'year__year')
    list_filter = ('season', 'year')

# Admin for Style
class StyleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('category',)

# Admin for Image
class ImageAdmin(admin.ModelAdmin):
    list_display = ('style','image', 'is_cover', 'uploaded_by', 'last_updated_by', 'created_at', 'updated_at')
    search_fields = ('style__name')
    list_filter = ('is_cover', 'uploaded_by', 'last_updated_by')

# Register models with admin interface
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Year, YearAdmin)
admin.site.register(MSRSeasonYear, MSRSeasonYearAdmin)
admin.site.register(Style, StyleAdmin)
admin.site.register(Image, ImageAdmin)
