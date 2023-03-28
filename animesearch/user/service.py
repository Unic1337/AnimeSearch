import django_filters

from anime.models import Anime


class AnimeFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Anime
        fields = ['score', 'scored_by', ]
