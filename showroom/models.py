from django.db import models
from django.contrib.auth.models import AbstractUser

# Abstract Base Model for Timestamp Fields
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Custom User Model for Employees
class Employee(AbstractUser, TimeStampedModel):
    is_active = models.BooleanField(default=True)
        # Add custom related names for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='employee_set',  # Custom related_name for groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='employee_permissions',  # Custom related_name for user_permissions
        blank=True
    )

# Categories Model
class Category(TimeStampedModel):
    SECTION_CHOICES = [
        ('Apparel', 'Apparel'),
        ('MSR', 'MSR'),
    ]

    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories'
    )
    section = models.CharField(max_length=100, choices=SECTION_CHOICES)
    order_priority = models.IntegerField(default=0)
    cover_image = models.ImageField(upload_to="category_cover_images", null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.parent.name})" if self.parent else f"{self.name} Highest Level"

# Years Model
class Year(TimeStampedModel):
    year = models.PositiveIntegerField()

    def __str__(self):
        return str(self.year)

# MSR Season-Year Model
class MSRSeasonYear(TimeStampedModel):
    season = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='msr_seasons')
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='msr_seasons')

# Styles Model
class Style(TimeStampedModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='styles')

    def __str__(self):
        return self.name

# Images Model
class Image(TimeStampedModel):
    image = models.ImageField(upload_to="style_images")
    style = models.ForeignKey(Style, on_delete=models.CASCADE, related_name='images')
    is_cover = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='uploaded_images')
    last_updated_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='updated_images')

    def __str__(self):
        return f"{self.style.name} Image"

# Relationships and Integrity
# - ForeignKey in Category for self-referencing hierarchy (parent-child relationship)
# - ForeignKey relationships in Style, Image, MSRSeasonYear for proper linking
