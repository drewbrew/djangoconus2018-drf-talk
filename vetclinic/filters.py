"""Filters for vet clinic"""

from rest_framework_filters.filterset import FilterSet
from rest_framework_filters import RelatedFilter

from . import models

# some handy defaults I like to use
DEFAULT_NUMERIC_FILTER_OPERATORS = [
    'exact', 'lte', 'gte', 'lt', 'gt', 'isnull', 'in',
]

DEFAULT_STRING_FILTER_OPERATORS = [
    'iexact', 'icontains', 'istartswith', 'iendswith', 'startswith',
    'endswith', 'contains', 'exact', 'regex', 'iregex', 'isnull', 'in',
]


class SpeciesFilter(FilterSet):

    class Meta:
        model = models.Species
        fields = {
            'id': DEFAULT_NUMERIC_FILTER_OPERATORS,
            'name': DEFAULT_STRING_FILTER_OPERATORS,
        }


class BreedFilter(FilterSet):
    species = RelatedFilter(
        SpeciesFilter,
        name='species',
        queryset=models.Species.objects.all(),
    )

    class Meta:
        model = models.Breed
        fields = {
            'id': DEFAULT_NUMERIC_FILTER_OPERATORS,
            'species': DEFAULT_NUMERIC_FILTER_OPERATORS,
            'name': DEFAULT_STRING_FILTER_OPERATORS,
        }


class AnimalFilter(FilterSet):
    breed = RelatedFilter(
        BreedFilter,
        name='breed',
        queryset=models.Breed.objects.all(),
    )

    class Meta:
        model = models.Animal
        fields = {
            'id': DEFAULT_NUMERIC_FILTER_OPERATORS,
            'breed': DEFAULT_NUMERIC_FILTER_OPERATORS,
            'name': DEFAULT_STRING_FILTER_OPERATORS,
        }
