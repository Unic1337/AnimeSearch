import django_filters
from django.db.models import Q, F

from .models import Anime, Review


class AnimeFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', method='title_filter')
    score_sort = django_filters.CharFilter(field_name='score', method='sort_by_field_name')
    scored_by_sort = django_filters.CharFilter(field_name='scored_by', method='sort_by_field_name')
    year_sort = django_filters.CharFilter(field_name='year', method='sort_by_field_name')

    class Meta:
        model = Anime
        fields = {
            'score': ['exact', 'gt', 'lt'],
            'scored_by': ['exact', 'gt', 'lt'],
            'year': ['exact', 'gt', 'lt'],
        }

    def title_filter(self, queryset, name, value):
        title_starts_with_queryset = queryset.filter(
            Q(title__istartswith=value) |
            Q(title_english__istartswith=value)
        )
        if title_starts_with_queryset.exists():
            return title_starts_with_queryset.order_by(F('scored_by').desc(nulls_last=True))[:25]

        title_contains_queryset = queryset.filter(
            Q(title__icontains=value) |
            Q(title_english__icontains=value)
        )
        if title_contains_queryset.exists():
            return title_contains_queryset.order_by(F('scored_by').desc(nulls_last=True))[:25]

        return queryset.filter(
            synopsis__icontains=value
        ).order_by(F('scored_by').desc(nulls_last=True))[:25]

    def sort_by_field_name(self, queryset, name, value):
        if value == 'asc':
            return queryset.order_by(F(name).asc(nulls_last=True))
        if value == 'desc':
            return queryset.order_by(F(name).desc(nulls_last=True))


class ReviewFilter(django_filters.FilterSet):
    class Meta:
        model = Review
        fields = {
            'user': ['exact'],
            'anime': ['exact'],
        }
