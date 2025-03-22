from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'FamilyMember', FamilyMemberViewSet)
router.register(r'FamilyCommunity', FamilyCommunityViewSet)
router.register(r'garages', GarageViewSet)
router.register(r'parking-zones', ParkingZoneViewSet)
router.register(r'parking-slots', ParkingSlotViewSet)
router.register(r'vehicles', VehicleViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'parking-events', ParkingEventViewSet)
router.register(r'pricing', PricingViewSet)
router.register(r'parking-history', ParkingHistoryViewSet)
router.register(r'parking-alerts', ParkingAlertViewSet)
router.register(r'parking-subscriptions', ParkingSubscriptionViewSet)
router.register(r'parking-slot-reservation-history', ParkingSlotReservationHistoryViewSet)
router.register(r'parking-sensors', ParkingSensorViewSet)
router.register(r'user-feedbacks', UserFeedbackViewSet)
router.register(r'discount-coupons', DiscountCouponViewSet)
router.register(r'parking-notifications', ParkingNotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
