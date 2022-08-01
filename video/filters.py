from django_filters import rest_framework as filters
from .models import Video


class VideoFilter(filters.FilterSet):
    tags = filters.CharFilter(method='filter_tag')
    rating_from = filters.NumberFilter(field_name='fhv_rating', lookup_expr='gte')
    rating_to = filters.NumberFilter(field_name='fhv_rating', lookup_expr='lte')

    def filter_tag(self, queryset, field_name, value):
        tags = value.split(',')
        return queryset.filter(video_tag__tag_id__in=tags)

    class Meta:
        model = Video
        fields = '__all__'
