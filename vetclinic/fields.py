from rest_framework import serializers

from .models import Species


class SpeciesField(serializers.PrimaryKeyRelatedField):

    def to_representation(self, value):
        return Species.objects.get(id=value)
