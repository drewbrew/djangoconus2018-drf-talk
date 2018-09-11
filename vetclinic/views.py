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


class AnimalViewSet(ModelViewSet):

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action in ['retrieve', 'update', 'partial']:
            # we're dealing with a single instance. Select the extra fields
            # present in the detail serializer
            return queryset.select_related('breed')
        return queryset

    # This is slightly counterintuitive, but you want to give the viewset the
    # *DETAIL* serializer. The serializer will take care of subbing in the
    # list serializer.
    serializer_class = serializers.AnimalDetailSerializer
    queryset = models.Animal.objects.select_related('species', 'client')
