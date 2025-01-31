from rest_framework import serializers
from .models import Category, Year, MSRSeasonYear, Style, Image, Employee

# Employee Serializer
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'username', 'email', 'is_active', 'created_at', 'updated_at')


# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'section', 'order_priority', 'cover_image', 'created_at', 'updated_at')


# Year Serializer
class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = ('id', 'year', 'created_at', 'updated_at')


# MSRSeasonYear Serializer
class MSRSeasonYearSerializer(serializers.ModelSerializer):
    season = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    year = serializers.PrimaryKeyRelatedField(queryset=Year.objects.all())

    class Meta:
        model = MSRSeasonYear
        fields = ('id', 'season', 'year', 'created_at', 'updated_at')


# Style Serializer
class StyleSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Style
        fields = ('id', 'name', 'category', 'created_at', 'updated_at')


# Image Serializer
class ImageSerializer(serializers.ModelSerializer):
    style = serializers.PrimaryKeyRelatedField(queryset=Style.objects.all())
    uploaded_by = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=False)
    last_updated_by = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=False)

    class Meta:
        model = Image
        fields = ('id', 'image', 'style', 'is_cover', 'uploaded_by', 'last_updated_by', 'created_at', 'updated_at')


# Nested Category Serializer (for listing subcategories)
class NestedCategorySerializer(serializers.ModelSerializer):
    parent = CategorySerializer(read_only=True)
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'section', 'order_priority', 'cover_image', 'created_at', 'updated_at')


# Nested Style Serializer (for listing associated images)
class NestedStyleSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Style
        fields = ('id', 'name', 'category', 'images', 'created_at', 'updated_at')
