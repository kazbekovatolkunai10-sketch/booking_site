from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class Country(models.Model):
    country_name = models.CharField(max_length=68, unique=True)
    country_image = models.ImageField(upload_to='country_image/', null=True, blank=True)

    def __str__(self):
        return f'{self.country_name}'

class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18), MaxValueValidator(90)],
                                           null=True, blank=True)
    user_image = models.ImageField(upload_to='user_image/', null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    ROLE_CHOICES = (
        ('client', 'client'),
        ('owner', 'owner')
    )
    role = models.CharField(max_length=20, choices = ROLE_CHOICES, default='client')
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

class City(models.Model):
    city_name = models.CharField(max_length=30, unique=True)
    city_image = models.ImageField(upload_to='city_image/')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country_city')


    def __str__(self):
        return f'{self.city_name}, {self.city_image}'

class Service(models.Model):
    service_image = models.ImageField(upload_to='service_image/')
    service_name = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.service_image}, {self.service_name}'

class Hotel(models.Model):
    hotel_name = models.CharField(max_length=64)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='hotel_city')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='hotel_country')
    hotel_stars = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    street = models.CharField(max_length=100)
    postal_index = models.PositiveSmallIntegerField()
    service = models.ManyToManyField(Service)
    description = models.TextField()
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def get_avg_rating(self):
        reviews = self.hotel_review.all()
        if reviews.exists():
            return round(sum([r.stars for r in reviews]) / reviews.count(), 1)
        return 0

    def get_count_person(self):
        review = self.hotel_review.all()
        if review.exists():
            return review.count()
        return 0

    def __str__(self):
        return f'{self.hotel_name}'

class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_image')
    hotel_image = models.ImageField(upload_to='hotel_image/')

    def __str__(self):
        return f'{self.hotel}, {self.hotel_image}'

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_number = models.IntegerField()
    TYPE_ROOM = (
        ('люкс', 'люкс'),
        ('полулюкс', 'полулюкс'),
        ('эконом', 'эконом'),
        ('семейный', 'семейный'),
        ('одноместный', 'одноместный'),
    )
    room_type = models.CharField(max_length=30, choices=TYPE_ROOM)
    STATUS_CHOICES = (
        ('свободен', 'свободен'),
        ('забронирован', 'забронирован'),
        ('занят', 'занят'),
    )
    room_status = models.CharField(max_length=60, choices=STATUS_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    room_description = models.TextField()

    def __str__(self):
        return f'{self.room_number}, {self.hotel}'

class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='image_room')
    room_image = models.ImageField(upload_to='room_image/')

    def __str__(self):
        return f'{self.room_image}, {self.room}'

class Booking(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.hotel}, {self.room}'

class Review(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_review')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.TextField()
    stars = models.PositiveSmallIntegerField(choices = [(i, str(i)) for i in range(1,11)])
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.hotel}, {self.user}'

