from django_filters import rest_framework
from django.db.models import Q, F, QuerySet

from .models import Anime, Review

EMPTY_VALUES = ([], (), {}, "", None)


class TitleFilter(rest_framework.Filter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        title_starts_with_queryset = qs.filter(
            Q(title__istartswith=value) |
            Q(title_english__istartswith=value)
        )
        if title_starts_with_queryset.exists():
            return title_starts_with_queryset.order_by(F('scored_by').desc(nulls_last=True))[:25]

        title_contains_queryset = qs.filter(
            Q(title__icontains=value) |
            Q(title_english__icontains=value)
        )
        if title_contains_queryset.exists():
            return title_contains_queryset.order_by(F('scored_by').desc(nulls_last=True))[:25]

        return qs.filter(
            synopsis__icontains=value
        ).order_by(F('scored_by').desc(nulls_last=True))[:25]


class OrderByFieldNameFilter(rest_framework.Filter):
    def filter(self, qs, value):
        if self.validate_field_name(value):
            if value[0] == '-':
                return qs.order_by(F(value[1:]).desc(nulls_last=True))
            return qs.order_by(F(value).asc(nulls_last=True))
        return qs

    @staticmethod
    def validate_field_name(name):
        allowed_names = ['title', 'type', 'rating', 'score', 'scored_by', 'favorites', 'season', 'status',
                         '-title', '-type', '-rating', '-score', '-scored_by', '-favorites', '-season', '-status']
        return name in allowed_names


class FilterByFieldName(rest_framework.Filter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        if self.distinct:
            qs = qs.distinct()
        values_list = [int(char.strip()) for char in value.split(',')]
        lookup = f'{self.field_name}__id__in'
        qs = qs.filter(**{lookup: values_list})
        return qs

    @staticmethod
    def check_field_name(name):
        allowed_names = ['title', 'type', 'rating', 'score', 'scored_by', 'favorites', 'season', 'status',
                         '-title', '-type', '-rating', '-score', '-scored_by', '-favorites', '-season', '-status']
        return name in allowed_names


class AnimeFilter(rest_framework.FilterSet):
    title = TitleFilter()
    order_by = OrderByFieldNameFilter()
    type = FilterByFieldName(field_name='type')
    rating = FilterByFieldName(field_name='rating')
    source = FilterByFieldName(field_name='source')
    genres = FilterByFieldName(field_name='genres')
    studios = FilterByFieldName(field_name='studios')
    status = rest_framework.CharFilter(field_name='status', lookup_expr='istartswith')
    season = rest_framework.CharFilter(field_name='season', lookup_expr='istartswith')

    class Meta:
        model = Anime
        fields = {
            'score': ['exact', 'gt', 'lt'],
            'scored_by': ['exact', 'gt', 'lt'],
            'year': ['exact', 'gt', 'lt'],
        }


class ReviewFilter(rest_framework.FilterSet):
    class Meta:
        model = Review
        fields = {
            'user': ['exact'],
            'anime': ['exact'],
        }
