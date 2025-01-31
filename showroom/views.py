from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .models import Category, Year, MSRSeasonYear, Style, Image, Employee
from .serializers import CategorySerializer, YearSerializer, MSRSeasonYearSerializer, StyleSerializer, ImageSerializer
from django.db.models import Q

# Filters for categories, styles, and images
class CategoryFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    section = filters.ChoiceFilter(choices=Category.SECTION_CHOICES)
    parent = filters.NumberFilter(field_name='parent__id')
    order_priority = filters.NumberFilter(field_name='order_priority')

    class Meta:
        model = Category
        fields = ['name', 'section', 'parent', 'order_priority']


class StyleFilter(filters.FilterSet):
    category = filters.NumberFilter(field_name='category__id')
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Style
        fields = ['category', 'name']


class ImageFilter(filters.FilterSet):
    style = filters.NumberFilter(field_name='style__id')
    is_cover = filters.BooleanFilter()
    uploaded_by = filters.NumberFilter(field_name='uploaded_by__id')
    last_updated_by = filters.NumberFilter(field_name='last_updated_by__id')

    class Meta:
        model = Image
        fields = ['style', 'is_cover', 'uploaded_by', 'last_updated_by']


# ViewSet for Category
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('parent', 'order_priority')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_class = CategoryFilter

    # Custom action to retrieve all subcategories for a category
    @action(detail=True, methods=['get'])
    def subcategories(self, request, pk=None):
        category = self.get_object()
        subcategories = category.subcategories.all()
        serializer = CategorySerializer(subcategories, many=True)
        return Response(serializer.data)


# ViewSet for Year
class YearViewSet(viewsets.ModelViewSet):
    queryset = Year.objects.all()
    serializer_class = YearSerializer
    permission_classes = [permissions.IsAuthenticated]


# ViewSet for MSRSeasonYear
class MSRSeasonYearViewSet(viewsets.ModelViewSet):
    queryset = MSRSeasonYear.objects.all()
    serializer_class = MSRSeasonYearSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Filtering seasons by year
    @action(detail=False, methods=['get'])
    def filter_by_year(self, request):
        year = request.query_params.get('year', None)
        if year:
            msr_seasons = MSRSeasonYear.objects.filter(year__year=year)
            serializer = MSRSeasonYearSerializer(msr_seasons, many=True)
            return Response(serializer.data)
        return Response({"detail": "Year parameter is required"}, status=400)


# ViewSet for Style
class StyleViewSet(viewsets.ModelViewSet):
    queryset = Style.objects.all()
    serializer_class = StyleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_class = StyleFilter

    # Custom action to list all images associated with a style
    @action(detail=True, methods=['get'])
    def images(self, request, pk=None):
        style = self.get_object()
        images = style.images.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)


# ViewSet for Image
class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_class = ImageFilter

    # Custom action to get cover image
    @action(detail=True, methods=['get'])
    def cover_image(self, request, pk=None):
        image = self.get_object()
        if image.is_cover:
            return Response({"cover_image_url": image.image})
        return Response({"detail": "This is not a cover image."}, status=400)
