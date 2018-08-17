from django.db import models

from drfdemo.users.models import User
# NOTE: In a real-world setup, these models would be split into multiple apps
# based on need/usage. In trying to keep this small, I'm restricting myself
# to one app


class Client(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    # I'm making this model US-centric for simplicity. In a real app,
    # I'd make this far more flexible
    city = models.CharField(max_length=50)
    # Use django-localflavor if you want some validation here.
    state = models.CharField(max_length=2)
    # django-localflavor offers a zip code field too
    zip = models.CharField(max_length=10)
    phone = models.CharField(max_length=50)
    email = models.EmailField(blank=True)


class Species(models.Model):
    technicians = models.ManyToManyField(User)
    name = models.CharField(max_length=50, unique=True)


class Breed(models.Model):
    name = models.CharField(max_length=50)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('name', 'species'), )


class Veterinarian(models.Model):
    # NOTE: add other fields here as needed
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Animal(models.Model):
    name = models.CharField(max_length=50)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    species = models.ForeignKey(Species, on_delete=models.DO_NOTHING)
    # breeds primarily make sense for dogs and cats, not cockatoos or guinea
    # pigs
    breed = models.ForeignKey(Breed, blank=True, on_delete=models.DO_NOTHING)
    approx_year_of_birth = models.PositiveSmallIntegerField()
    first_visit_date = models.DateField(blank=True, null=True)


class Appointment(models.Model):
    time = models.DateTimeField()
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    # NOTE: Real vet clinics have vet and tech appointments as separate
    # scheduling options
    veterinarian = models.ForeignKey(Veterinarian, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = (
            ('time', 'veterinarian'),
            ('time', 'animal'),
        )
