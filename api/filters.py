import django_filters
from catalog.models import House, BUILDING_TYPE_CHOICES


class HouseFilter(django_filters.FilterSet):
    area = django_filters.RangeFilter()
    building_type = django_filters.MultipleChoiceFilter(choices=BUILDING_TYPE_CHOICES)
    price = django_filters.RangeFilter()

    class Meta:
        model = House
        fields = ['area', 'building_type', 'price']