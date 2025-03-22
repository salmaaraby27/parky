from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils import timezone
from datetime import timedelta
class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True ,  unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, null=False )
    subscription_type  = models.CharField(max_length=20, default='Regular')
    license_id = models.PositiveIntegerField(blank=False ,null=False, unique=True, default=False)
    Wallet_Balance = models.PositiveIntegerField(blank=True, null=True, unique=True)
    Registration_Date = models.DateTimeField(default=False)

    # groups = models.ManyToManyField(
    #     'auth.Group',
    #     related_name='custom_user_groups',  # Prevents clash
    #     blank=True
    # )
    # user_permissions = models.ManyToManyField(
    #     'auth.Permission',
    #     related_name='custom_user_permissions',  # Prevents clash
    #     blank=True
    # )


    def __str__(self):
        return self.username

class FamilyCommunity(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Family name
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name="family_creator")  # Admin of the family
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Family Community: {self.name}"

class FamilyMember(models.Model):
    family = models.ForeignKey(FamilyCommunity, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[('Admin', 'Admin'), ('Member', 'Member')], default='Member')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role} in {self.family.name}"

class Garage(models.Model):
    name = models.CharField(max_length=100 , unique=True)
    location = models.CharField(max_length=255)  # Can be an address or coordinates
    total_capacity = models.PositiveIntegerField()  # Total number of parking spots in the garage
    available_capacity = models.PositiveIntegerField()  # Number of available parking spots
    opening_hours = models.TimeField()
    closing_hours = models.TimeField()
    no_of_floors = models.CharField(max_length=255, default=1)

    def __str__(self):
        return f"Garage: {self.name} at {self.location}"

    def update_available_capacity(self):
        # Logic to update available capacity based on occupied parking slots
        self.available_capacity = self.total_capacity - self.parkingzone_set.aggregate(models.Sum('total_slots'))['total_slots__sum']
        self.save()

class ParkingZone(models.Model):
    garage = models.ForeignKey('Garage', on_delete=models.CASCADE, related_name='parking_zones')
    name = models.CharField(max_length=100)
    total_slots = models.PositiveIntegerField()
    available_slots = models.PositiveIntegerField()
    zone_type = models.CharField(max_length=50, choices=[('Regular', 'Regular'), ('VIP', 'VIP')])

    def __str__(self):
        return f"Zone: {self.name} in {self.garage.name}"

    def update_available_slots(self):
        # Update available slots based on the occupied ones
        self.available_slots = self.total_slots - self.parkingslot_set.filter(is_occupied=True).count()
        self.save()

class ParkingSlot(models.Model):
    parking_zone = models.ForeignKey('ParkingZone', on_delete=models.CASCADE, related_name='parking_slots')
    slot_number = models.CharField(max_length=20)  # Unique number or identifier for the slot
    is_occupied = models.BooleanField(default=False)
    is_reserved = models.BooleanField(default=False)
    vehicle = models.ForeignKey('Vehicle', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Slot {self.slot_number} in Zone {self.parking_zone.name}"

    def occupy(self, vehicle):
        self.is_occupied = True
        self.vehicle = vehicle
        self.save()

    def vacate(self):
        self.is_occupied = False
        self.vehicle = None
        self.save()

class Vehicle(models.Model):
    plate_number = models.CharField(max_length=15, unique=True)
    vehicle_type = models.CharField(max_length=20)  # e.g., Car, Bike, Truck
    owner_name = models.ForeignKey('user',on_delete=models.CASCADE)
    vehicle_model = models.CharField(max_length=20, default=False)
    vehicle_color = models.CharField(max_length=20,default=False)


    def __str__(self):
        return f"{self.vehicle_type} - {self.plate_number}"


class Reservation(models.Model):
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    parking_slot = models.ForeignKey('ParkingSlot', on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, default='Reserved')  # Reserved, Cancelled, Completed
    total_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # New field
    family = models.ForeignKey('FamilyCommunity', on_delete=models.SET_NULL, null=True, blank=True)  # Link reservation to family


    def calculate_total_cost(self):
        """Calculate the total cost of the reservation based on parking duration."""
        if not self.start_time or not self.end_time:
            return None

        duration = (self.end_time - self.start_time).total_seconds() / 3600  # Convert to hours
        pricing = Pricing.objects.filter(parking_zone=self.parking_slot.parking_zone,
                                         vehicle_type=self.vehicle.vehicle_type).first()

        if pricing:
            cost = duration * pricing.hourly_rate
            return round(cost, 2)
        return None

    def save(self, *args, **kwargs):
        """Automatically calculate the total cost before saving."""
        self.total_cost = self.calculate_total_cost()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reservation for {self.vehicle.plate_number} in Slot {self.parking_slot.slot_number}"


class Payment(models.Model):
    reservation = models.OneToOneField('Reservation', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    payment_time = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')],
        default='Pending'
    )
    payer = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)  # Who paid
    family = models.ForeignKey('FamilyCommunity', on_delete=models.SET_NULL, null=True, blank=True)  # Link to family

    def save(self, *args, **kwargs):
        """Ensure payment amount matches the reservation total cost."""
        if self.amount is None and self.reservation and self.reservation.total_cost is not None:
            self.amount = self.reservation.total_cost
        elif self.amount is None:
            self.amount = 0  # Fallback to avoid NULL
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment for {self.reservation.vehicle.plate_number} - Amount: {self.amount}"


class ParkingEvent(models.Model):
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    parking_slot = models.ForeignKey('ParkingSlot', on_delete=models.CASCADE)
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)  # Duration of the parking event (calculated later)
    event_type = models.CharField(max_length=20, choices=[('Parked', 'Parked'), ('Exited', 'Exited')], default='Parked')

    def save(self, *args, **kwargs):
        if self.exit_time:
            self.duration = self.exit_time - self.entry_time
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Event for {self.vehicle.plate_number} in Slot {self.parking_slot.slot_number}"

class Pricing(models.Model):
    vehicle_type = models.CharField(max_length=20, choices=[('Car', 'Car'), ('Bike', 'Bike'), ('Truck', 'Truck')])
    parking_zone = models.ForeignKey('ParkingZone', on_delete=models.CASCADE)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)  # Price per hour
    daily_rate = models.DecimalField(max_digits=6, decimal_places=2)  # Price per day
    weekly_rate = models.DecimalField(max_digits=6, decimal_places=2)  # Price per week

    def __str__(self):
        return f"Pricing for {self.vehicle_type} in {self.parking_zone.name}"


class ParkingHistory(models.Model):
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    parking_slot = models.ForeignKey('ParkingSlot', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=6, decimal_places=2)
    parking_zone = models.ForeignKey('ParkingZone', on_delete=models.CASCADE)

    def __str__(self):
        return f"History for {self.vehicle.plate_number} in Slot {self.parking_slot.slot_number}"



class ParkingAlert(models.Model):
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    parking_slot = models.ForeignKey('ParkingSlot', on_delete=models.CASCADE)
    alert_time = models.DateTimeField(default=timezone.now)  # When the alert was created
    message = models.CharField(max_length=255)
    resolved = models.BooleanField(default=False)  # Whether the alert has been resolved

    def __str__(self):
        return f"Alert for {self.vehicle.plate_number} in Slot {self.parking_slot.slot_number}"

class ParkingSubscription(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    parking_zone = models.ForeignKey('ParkingZone', on_delete=models.CASCADE)  # Which zone the subscription is for
    start_date = models.DateField()
    end_date = models.DateField()
    subscription_type = models.CharField(max_length=20, choices=[('Monthly', 'Monthly'), ('Yearly', 'Yearly')])
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s {self.subscription_type} Subscription for {self.parking_zone.name}"

class ParkingSlotReservationHistory(models.Model):
    parking_slot = models.ForeignKey('ParkingSlot', on_delete=models.CASCADE)
    reserved_by = models.ForeignKey('User', on_delete=models.CASCADE)  # The user who reserved the slot
    reservation_start = models.DateTimeField()
    reservation_end = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('Reserved', 'Reserved'), ('Cancelled', 'Cancelled'), ('Completed', 'Completed')])

    def __str__(self):
        return f"History for Slot {self.parking_slot.slot_number} reserved by {self.reserved_by.username}"


class ParkingSensor(models.Model):
    parking_slot = models.OneToOneField('ParkingSlot', on_delete=models.CASCADE)
    sensor_status = models.CharField(max_length=20,
                                     choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Faulty', 'Faulty')],
                                     default='Active')
    last_maintenance = models.DateTimeField(null=True, blank=True)
    last_check = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sensor for Slot {self.parking_slot.slot_number} - {self.sensor_status}"

class UserFeedback(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    parking_slot = models.ForeignKey('ParkingSlot', on_delete=models.SET_NULL, null=True, blank=True)
    feedback_text = models.TextField()
    rating = models.PositiveIntegerField(default=1, choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username} - Rating: {self.rating}"

class DiscountCoupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    usage_count = models.PositiveIntegerField(default=0)
    max_usage_count = models.PositiveIntegerField()

    def __str__(self):
        return f"Coupon Code: {self.code} - {self.discount_percentage}% off"

class ParkingNotification(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=100, choices=[('Reservation Reminder', 'Reservation Reminder'), ('Payment Reminder', 'Payment Reminder'), ('General Alert', 'General Alert')])
    message = models.TextField()
    notification_time = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.notification_type}"

