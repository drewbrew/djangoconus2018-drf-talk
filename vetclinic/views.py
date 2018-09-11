import datetime

from django.db.models import Prefetch
from django.utils.timezone import now
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
        if self.request.user.has_perm(
                'vetclinic.see_animal_appointments_with_animal',
        ):
            timestamp = now()
            # tack on appointments, but filter to only within +/- 30 days
            queryset = queryset.prefetch_related(
                Prefetch(
                    'appointments',
                    queryset=models.Appointment.objects.filter(
                        time__gte=timestamp - datetime.timedelta(days=30),
                        time__lte=timestamp - datetime.timedelta(days=30),
                    ).select_related('veterinarian'),
                ),
            )
        if self.action in ['retrieve', 'update', 'partial']:
            # we're dealing with a single instance. Select the extra fields
            # present in the detail serializer
            return queryset.select_related('breed')
        return queryset

    def get_serializer_class(self):
        if self.request.user.has_perm(
                'vetclinic.see_animal_appointments_with_animal',
        ):
            return serializers.AnimalWithAppointmentsSerializer
        return super().get_serializer_class()

    # This is slightly counterintuitive, but you want to give the viewset the
    # *DETAIL* serializer. The serializer will take care of subbing in the
    # list serializer.
    serializer_class = serializers.AnimalDetailSerializer
    queryset = models.Animal.objects.select_related('species', 'client')
