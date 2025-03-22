from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class FamilyCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyCommunity
        fields = '__all__'

class FamilyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyMember
        fields = '__all__'
        
class GarageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garage
        fields = '__all__'


class ParkingZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingZone
        fields = '__all__'


class ParkingSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSlot
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class ParkingEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingEvent
        fields = '__all__'


class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = '__all__'


class ParkingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingHistory
        fields = '__all__'


class ParkingAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingAlert
        fields = '__all__'


class ParkingSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSubscription
        fields = '__all__'


class ParkingSlotReservationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSlotReservationHistory
        fields = '__all__'


class ParkingSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSensor
        fields = '__all__'


class UserFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFeedback
        fields = '__all__'


class DiscountCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCoupon
        fields = '__all__'


class ParkingNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingNotification
        fields = '__all__'

class InvoiceSerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField()
    vehicle_plate = serializers.CharField()
    parking_slot = serializers.CharField()
    parking_zone = serializers.CharField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    total_duration = serializers.FloatField()
    amount = serializers.DecimalField(max_digits=6, decimal_places=2)
    payment_status = serializers.CharField()

    @staticmethod
    def generate_invoice(reservation):
        """Generate an invoice dictionary from a Reservation object."""
        try:
            payment = Payment.objects.get(reservation=reservation)

            return {
                "reservation_id": reservation.id,
                "vehicle_plate": reservation.vehicle.plate_number,
                "parking_slot": reservation.parking_slot.slot_number,
                "parking_zone": reservation.parking_slot.parking_zone.name,
                "start_time": reservation.start_time,
                "end_time": reservation.end_time,
                "total_duration": round((reservation.end_time - reservation.start_time).total_seconds() / 3600, 2),
                "amount": payment.amount,
                "payment_status": payment.payment_status
            }
        except Payment.DoesNotExist:
            return {"error": "Payment not found for this reservation."}

