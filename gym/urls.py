from django.urls import path, include
from .views import UserRegistrationView, MembershipPlanViewSet, MemberViewSet, FitnessClassViewSet, BookingViewSet, UserLoginView, UserLogoutView, activate, fitness_classes_view, booking_history_view, BookingHistoryViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'membership-plans', MembershipPlanViewSet)
router.register(r'members', MemberViewSet)
router.register(r'fitness-classes', FitnessClassViewSet)
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'booking-history', BookingHistoryViewSet, basename='booking-history')
urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('activate/<str:uid64>/<str:token>/', activate, name='activate'),
    path('fitness-classes/', fitness_classes_view, name='fitness_classes'),
    path('booking-history/', booking_history_view, name='booking_history'),
]
