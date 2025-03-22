from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class FamilyCommunityViewSet(viewsets.ModelViewSet):
    queryset = FamilyCommunity.objects.all()
    serializer_class = FamilyCommunitySerializer

class FamilyMemberViewSet(viewsets.ModelViewSet):
    queryset = FamilyMember.objects.all()
    serializer_class = FamilyMemberSerializer

class GarageViewSet(viewsets.ModelViewSet):
    queryset = Garage.objects.all()
    serializer_class = GarageSerializer


class ParkingZoneViewSet(viewsets.ModelViewSet):
    queryset = ParkingZone.objects.all()
    serializer_class = ParkingZoneSerializer


class ParkingSlotViewSet(viewsets.ModelViewSet):
    queryset = ParkingSlot.objects.all()
    serializer_class = ParkingSlotSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class ParkingEventViewSet(viewsets.ModelViewSet):
    queryset = ParkingEvent.objects.all()
    serializer_class = ParkingEventSerializer


class PricingViewSet(viewsets.ModelViewSet):
    queryset = Pricing.objects.all()
    serializer_class = PricingSerializer


class ParkingHistoryViewSet(viewsets.ModelViewSet):
    queryset = ParkingHistory.objects.all()
    serializer_class = ParkingHistorySerializer


class ParkingAlertViewSet(viewsets.ModelViewSet):
    queryset = ParkingAlert.objects.all()
    serializer_class = ParkingAlertSerializer


class ParkingSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = ParkingSubscription.objects.all()
    serializer_class = ParkingSubscriptionSerializer


class ParkingSlotReservationHistoryViewSet(viewsets.ModelViewSet):
    queryset = ParkingSlotReservationHistory.objects.all()
    serializer_class = ParkingSlotReservationHistorySerializer


class ParkingSensorViewSet(viewsets.ModelViewSet):
    queryset = ParkingSensor.objects.all()
    serializer_class = ParkingSensorSerializer


class UserFeedbackViewSet(viewsets.ModelViewSet):
    queryset = UserFeedback.objects.all()
    serializer_class = UserFeedbackSerializer


class DiscountCouponViewSet(viewsets.ModelViewSet):
    queryset = DiscountCoupon.objects.all()
    serializer_class = DiscountCouponSerializer


class ParkingNotificationViewSet(viewsets.ModelViewSet):
    queryset = ParkingNotification.objects.all()
    serializer_class = ParkingNotificationSerializer
