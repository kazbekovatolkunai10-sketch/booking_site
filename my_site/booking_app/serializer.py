from rest_framework import serializers
from .models import (Country, UserProfile, City, Service, Hotel,
                     HotelImage, Room, RoomImage, Booking, Review)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id','country_name', 'country_image']

class CountrySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']

class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']

class UserProfileDetailSerializer(serializers.ModelSerializer):
    country = CountrySimpleSerializer()
    class Meta:
        model = UserProfile
        fields = ['id','first_name', 'last_name', 'user_image', 'country', 'age', 'role']

class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id','city_name', 'city_image']

class CitySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['service_image', 'service_name']

class ReviewListSerializer(serializers.ModelSerializer):
    user = UserProfileListSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ['user', 'comment']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewDetailSerializer(serializers.ModelSerializer):
    user = UserProfileListSerializer(read_only=True)
    created_date = serializers.DateTimeField(format='%d-%m-%Y')
    class Meta:
        model = Review
        fields = ['user', 'comment', 'stars', 'created_date']

class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['hotel', 'hotel_image']

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

class HotelListSerializer(serializers.ModelSerializer):
    country = CountrySimpleSerializer()
    city = CitySimpleSerializer()
    avg_review = serializers.SerializerMethodField()
    get_count_person = serializers.SerializerMethodField()
    hotel_image = HotelImageSerializer(many=True, read_only=True)
    class Meta:
        model = Hotel
        fields = ['id', 'hotel_stars', 'hotel_name', 'country', 'city', 'avg_review', 'get_count_person', 'hotel_image']

    def get_avg_review(self, obj):
        return obj.get_avg_rating()

    def get_count_person(self):
        review = self.hotel_review.obj.all()

class CountryDetailSerializer(serializers.ModelSerializer):
    hotel_country = HotelListSerializer(many=True)
    country_city = CityListSerializer(read_only=True, many=True)
    class Meta:
       model = Country
       fields = ['id','country_name', 'country_image', 'hotel_country', 'country_city']

class CityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id','city_name', 'city_image', 'country']

class HotelDetailSerializer(serializers.ModelSerializer):
    hotel_review = ReviewListSerializer(read_only=True, many=True)
    service = ServiceSerializer(read_only=True, many=True)
    city = CityDetailSerializer()
    country = CountryListSerializer()
    avg_review = serializers.SerializerMethodField()
    hotel_image = HotelImageSerializer(many=True, read_only=True)
    class Meta:
        model = Hotel
        fields = ['id','hotel_name', 'country', 'city', 'street', 'avg_review', 'get_count_person',
                  'hotel_review', 'service', 'description', 'hotel_image']

    def get_avg_review(self, obj):
        return obj.get_avg_rating()

    def get_count_person(self):
        review = self.hotel_review.obj.all()

class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_number', 'room_type', 'price', 'room_status']

class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ['room_image']

class RoomDetailSerializer(serializers.ModelSerializer):
    image_room = RoomImageSerializer(many=True, read_only=True)
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'price', 'room_status', 'room_description', 'image_room']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


