"""Serializers for the vet clinic app"""

from rest_framework import serializers

from drfdemo.users.serializers import UserSerializer
from drfdemo.users.models import User

from . import models
from . import fields


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Client
        fields = '__all__'


class SpeciesSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # Because we're dealing with a many-to-many, we can't
        # just pass off the PKs (even after using the right field)
        # to the serializer

        # technician_ids is a required field, so we don't
        # have to worry about KeyErrors
        technicians = validated_data.pop('technician_ids')
        instance = super().create(validated_data)
        # now save the technicians to the related field
        instance.technicians.set(technicians, clear=True)

    def update(self, instance, validated_data):
        # We have the same constraint as in create(), but we have
        # a design decision to make: what do we do if the user
        # omits `technician_ids`?

        # I personally believe good practice is to do nothing.
        # Let the user submit `[]` to declare they want to clear
        # the relation.

        # to do that, we'll use a value that the user can't submit
        # as the default value
        technicians = validated_data.pop('technician_ids', None)
        result = super().update(instance, validated_data)
        if technicians is None:
            return result
        if not technicians:
            instance.technicians.clear()
        # I find the most clear API action in this case is to do a
        # firm replace rather than just adding on. However, your
        # API needs may be different. In that case, you may want
        # to creat/e detail routes to add and remove related
        # objects.
        instance.technicians.set(technicians, clear=True)

    technicians = UserSerializer(many=True, read_only=True)
    technician_ids = serializers.PrimaryKeyRelatedField(
        # we can filter the queryset to prevent the API user from assigning
        # inactive user instances.
        queryset=User.objects.filter(is_active=True),
        write_only=True, allow_null=False, required=True,
    )

# NOTE: I'm not going to go through showing all the options for
# the species serializer since it's a ManyToManyField.
# The serializer options are identical for M2M vs direct foreign
# keys, so I'll stick with the single instance for breeds for
# simplicity.


class BreedSerializerWithWritableSerializer(serializers.ModelSerializer):
    """Breed with option 1: writing a writable nested serializer"""

    species = SpeciesSerializer()

    def create(self, validated_data):
        # species is not nullable, so I don't have to worry about KeyErrors
        # because DRF will raise a ValidationError for me if the user
        # forgets species.
        species_dict = validated_data.pop('species')

        try:
            species = models.Species.objects.get(id=species_dict['id'])
        except models.Species.DoesNotExist:
            # create one
            species = models.Species.objects.create(**species_dict)
        else:
            # need to verify that the other data matches
            for key, val in species_dict.items():
                if getattr(species, key) != val:
                    # NOTE: depending on your use case, you may want to
                    # accept whatever data is provided by the user.
                    # In that case, use setattr() and save when you're done.
                    raise serializers.ValidationError({
                        'species': {
                            key: ['Modifying species data is not supported'],
                        },
                    })
        # now drop the Species instance into the validated data, which DRF will
        # happily accept
        validated_data['species'] = species
        # and pass the data back to DRF to let it do its thing
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # this is largely the same route as create(), but we have to
        # consider the possibility that the user omitted the species dict (as
        # would be expected in a PATCH)
        species_dict = validated_data.pop('species', False)
        if species_dict is False:
            # don't worry about doing our thing; just pass it straight to DRF
            return super().update(instance, validated_data)
        # the rest of the method is identical to create()
        try:
            species = models.Species.objects.get(id=species_dict['id'])
        except models.Species.DoesNotExist:
            # create one
            species = models.Species.objects.create(**species_dict)
        else:
            # need to verify that the other data matches
            for key, val in species_dict.items():
                if getattr(species, key) != val:
                    # NOTE: depending on your use case, you may want to
                    # accept whatever data is provided by the user.
                    # In that case, use setattr() and save when you're done.
                    raise serializers.ValidationError({
                        'species': {
                            key: ['Modifying species data is not supported'],
                        },
                    })
        # now drop the Species instance into the validated data, which DRF will
        # happily accept
        validated_data['species'] = species
        # and pass off to DRF
        return super().update(instance, validated_data)

    class Meta:
        fields = '__all__'
        model = models.Breed


class BreedSerializerWithSeparateWritablePK(serializers.ModelSerializer):
    """Breed with option 2: write a separate PK field"""
    species = SpeciesSerializer(read_only=True)
    species_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Species.objects.all(),
        write_only=True, required=True, allow_null=False,
    )

    def validate(self, data):
        try:
            data['species'] = data.pop('species_id')
        except KeyError:
            # this will already have failed validation for POST and PUT;
            # if it's not provided, PATCH won't change anything.
            # Thus, nothing to do.
            pass
        return data

    class Meta:
        fields = '__all__'
        model = models.Breed


class BreedSerializerWithWritablePK(serializers.ModelSerializer):
    """Breed with option 3: write a PK, read a nested object"""
    species = fields.SpeciesField(
        queryset=models.Species.objects.all(),
        write_only=True, required=True, allow_null=False,
    )


class AnimalListSerializer(serializers.ListSerializer):
    client = serializers.StringRelatedField(read_only=True)
    species = serializers.StringRelatedField(read_only=True)

    # NOTE: To make this writable (so you can POST multiple animals at once,
    # define .create() here)

    class Meta:
        model = models.Animal
        exclude = ['breed']


class AnimalDetailSerializer(serializers.ModelSerializer):
    # NOTE: I'm just dealing with this to be read-only for brevity
    client = ClientSerializer(read_only=True)
    species = SpeciesSerializer(read_only=True)
    breed = BreedSerializerWithWritablePK(read_only=True)

    class Meta:
        model = models.Animal
        fields = '__all__'
        list_serializer_class = AnimalListSerializer


class LimitedAppoinmentSerializer(serializers.ModelSerializer):
    """Appointment without animal for embedding within animal"""
    veterinarian = serializers.StringRelatedField()

    class Meta:
        model = models.Appointment
        exclude = ['animal']


class AnimalWithAppointmentsSerializer(AnimalDetailSerializer):
    """Animal detail serializer with appointments built in"""
    # NOTE: Normally this would be something users might like to have
    # built in to the main detail view, but I'm stretching the example here.
    appointments = LimitedAppoinmentSerializer(read_only=True)
