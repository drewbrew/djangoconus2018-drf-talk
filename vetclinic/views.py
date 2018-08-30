from rest_framework.views import ModelViewSet

from . import models
from . import serializers


class ClientViewSet(ModelViewSet):
    serializer_class = serializers.ClientSerializer
    queryset = models.Client.objects.all()


class SpeciesViewSet(ModelViewSet):
    serializer_class = serializers.SpeciesSerializer
    queryset = models.Species.objects.prefetch_related('technicians')


class BreedViewSetWithWritablePK(ModelViewSet):
    serializer_class = serializers.BreedSerializerWithWritablePK
    queryset = models.Breed.objects.select_related('species')


class BreedViewSetWithWritableNestedField(ModelViewSet):
    serializer_class = serializers.BreedSerializerWithWritableSerializer
    queryset = models.Breed.objects.select_related('species')


class BreedViewSetWithSeparateIDField(ModelViewSet):
    serializer_class = serializers.BreedSerializerWithSeparateWritablePK
    queryset = models.Breed.objects.select_related('species')
