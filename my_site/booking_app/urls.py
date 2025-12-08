from django.urls import path, include
from rest_framework import routers
from .views import (CountryListAPIView, CountryDetailAPIView, UserProfileListAPIView, UserProfileDetailAPIView,
                    CityListAPIView, CityDetailAPIView, ServiceViewSet, HotelListAPIView, HotelDetailAPIView,
                    HotelImageViewSet, RoomListAPIView, RoomDetailAPIView, RoomImageViewSet, BookingViewSet,
                    ReviewCreateAPIView, ReviewDetailAPIView, ReviewEditAPIView, HotelCreateAPIView, HotelEditAPIView,
                    RegisterView, LogoutView, CustomLoginView)

router = routers.SimpleRouter()
router.register(r'service', ServiceViewSet)
router.register(r'hotel_image', HotelImageViewSet)
router.register(r'room_image', RoomImageViewSet)
router.register(r'booking', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register_list'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('country/', CountryListAPIView.as_view(), name='country-list'),
    path('country/<int:pk>/', CountryDetailAPIView.as_view(), name='country-detail'),
    path('user/', UserProfileListAPIView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user-detail'),
    path('city/', CityListAPIView.as_view(), name='city-list'),
    path('city/<int:pk>/', CityDetailAPIView.as_view(), name='city-detail'),
    path('hotel/', HotelListAPIView.as_view(), name='hotel-list'),
    path('hotel/create/', HotelCreateAPIView.as_view(), name='hotel-create'),
    path('hotel/<int:pk>/', HotelDetailAPIView.as_view(), name='hotel-detail'),
    path('review/', ReviewCreateAPIView.as_view(), name='review-create'),
    path('hotel/<int:pk>/edit/', HotelEditAPIView.as_view(), name='hotel-edit'),
    path('review/<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail'),
    path('review/<int:pk>/edit/', ReviewEditAPIView.as_view(), name='review-edit'),
    path('room/', RoomListAPIView.as_view(), name='room-list'),
    path('room/<int:pk>/', RoomDetailAPIView.as_view(), name='room-detail')
]
