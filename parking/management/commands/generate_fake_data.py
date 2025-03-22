import random
from faker import Faker
from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand
from parking.models import (
    User,FamilyCommunity, FamilyMember, Garage, ParkingZone, ParkingSlot, Vehicle, Reservation,
    Payment, ParkingEvent, Pricing, ParkingHistory, ParkingAlert,
    ParkingSubscription, ParkingSlotReservationHistory, ParkingSensor,
    UserFeedback, DiscountCoupon, ParkingNotification
)
from django.utils import timezone
from datetime import timedelta

fake = Faker()


class Command(BaseCommand):
    help = "Generate fake data for all models"

    def handle(self, *args, **kwargs):
        self.stdout.write("Generating fake data...")
        fake.unique.clear()

        # Create Users
        users = []
        for _ in range(1):
            users = []
            for _ in range(1000):
                try:
                    user = User.objects.create(
                        username=fake.unique.user_name()[:255],  # Ensure unique username
                        email=fake.unique.email(),  # Ensure unique email
                        phone_number=fake.unique.phone_number()[:15],
                        address=fake.address()[:255],
                        password="password123",  # Ideally, hash this
                        subscription_type=random.choice(['Basic', 'Premium']),
                        license_id=random.randint(100000, 999999),
                        Wallet_Balance=random.randint(0, 5000),
                        Registration_Date=timezone.now()
                    )
                    users.append(user)
                except IntegrityError:
                    fake.unique.clear()  # Clear Faker's uniqueness cache to prevent repeating
                    self.stdout.write("Skipping duplicate user")

        # Ensure there are users before creating FamilyCommunity
        if not users:
            self.stdout.write("No users found. Skipping FamilyCommunity creation.")
        else:
            # Create Family Communities
            # Create Family Communities
            family_communities = []
            for _ in range(100):
                try:
                    family_community = FamilyCommunity.objects.create(
                        name=fake.unique.company()[:100],
                        created_at=timezone.now(),
                        created_by=random.choice(users)
                    )
                    family_communities.append(family_community)
                except IntegrityError:
                    fake.unique.clear()
                    self.stdout.write("Skipping duplicate FamilyCommunity")

            # Ensure there are family communities before creating Family Members
            if not family_communities:
                self.stdout.write("No family communities found. Skipping FamilyMember creation.")
            else:
                # Create Family Members
                family_members = []
                for _ in range(500):  # Adjust the number as needed
                    member = FamilyMember.objects.create(
                        user=random.choice(users),
                        family=random.choice(family_communities)  # Corrected variable name
                    )
                    family_members.append(member)

        # Create Garages

        garages = []
        for _ in range(100):
            try:
                garage = Garage.objects.create(
                    name=fake.unique.company()[:100],  # Ensure uniqueness
                    location=fake.address()[:255],
                    total_capacity=random.randint(50, 200),
                    available_capacity=random.randint(0, 50),
                    opening_hours=fake.time_object(),
                    closing_hours=fake.time_object(),
                    no_of_floors=str(random.randint(1, 10))
                )
                garages.append(garage)
            except IntegrityError:
                fake.unique.clear()  # Reset Faker's uniqueness tracking
                self.stdout.write("Skipping duplicate Garage")

        # Create Parking Zones
        zones = []
        for garage in garages:
            for _ in range(5):
                zone = ParkingZone.objects.create(
                    garage=garage,
                    name=fake.word().capitalize()[:100],
                    total_slots=random.randint(10, 50),
                    available_slots=random.randint(0, 10),
                    zone_type=random.choice(['Regular', 'VIP'])
                )
                zones.append(zone)

        # Create Parking Slots
        slots = []
        for zone in zones:
            for i in range(zone.total_slots):
                slot = ParkingSlot.objects.create(
                    parking_zone=zone,
                    slot_number=f"{zone.name[:2]}-{i + 1}",
                    is_occupied=random.choice([True, False]),
                    is_reserved=random.choice([True, False]),
                    vehicle=None
                )
                slots.append(slot)

        # Create Vehicles
        vehicles = []
        for user in users:
            vehicle = Vehicle.objects.create(
                plate_number=fake.unique.license_plate(),
                vehicle_type=random.choice(['Car', 'Bike', 'Truck']),
                owner_name=user,
                vehicle_model=fake.word()[:20],
                vehicle_color=fake.color_name()
            )
            vehicles.append(vehicle)

        # Create Reservations
        reservations = []
        for vehicle in vehicles:
            slot = random.choice(slots)
            start_time = timezone.now()
            end_time = start_time + timedelta(hours=random.randint(1, 24))
            reservation = Reservation.objects.create(
                vehicle=vehicle,
                parking_slot=slot,
                start_time=start_time,
                end_time=end_time,
                status=random.choice(['Reserved', 'Cancelled', 'Completed']),
                total_cost=random.uniform(5, 50)
            )
            reservations.append(reservation)

        # Create Payments
        families = list(FamilyCommunity.objects.all())

        for reservation in reservations:
            amount = reservation.total_cost if reservation.total_cost is not None else random.uniform(5, 50)

        Payment.objects.create(
            reservation=reservation,
            amount=amount,  # Ensure non-null amount
            payment_status=random.choice(['Pending', 'Completed', 'Failed']),
            payer=random.choice(users),
            family=random.choice(families) if families and random.choice([True, False]) else None
        )


        # Create Parking Events
        for vehicle in vehicles:
            slot = random.choice(slots)
            entry_time = timezone.now() - timedelta(hours=random.randint(1, 24))
            exit_time = entry_time + timedelta(hours=random.randint(1, 5)) if random.choice([True, False]) else None
            ParkingEvent.objects.create(
                vehicle=vehicle,
                parking_slot=slot,
                entry_time=entry_time,
                exit_time=exit_time,
                event_type='Parked' if not exit_time else 'Exited'
            )

        # Create Pricing
        for zone in zones:
            Pricing.objects.create(
                vehicle_type=random.choice(['Car', 'Bike', 'Truck']),
                parking_zone=zone,
                hourly_rate=random.uniform(2, 10),
                daily_rate=random.uniform(10, 50),
                weekly_rate=random.uniform(50, 200)
            )
        # Create Parking History
        for vehicle in vehicles:
            slot = random.choice(slots)
            start_time = timezone.now() - timedelta(days=random.randint(1, 30))
            end_time = start_time + timedelta(hours=random.randint(1, 12))
            ParkingHistory.objects.create(
                vehicle=vehicle,
                parking_slot=slot,
                start_time=start_time,
                end_time=end_time,
                total_amount=random.uniform(5, 100),
                parking_zone=slot.parking_zone
            )

        # Create Alerts
        for _ in range(5):
            ParkingAlert.objects.create(
                vehicle=random.choice(vehicles),
                parking_slot=random.choice(slots),
                message=fake.sentence()[:255],
                resolved=random.choice([True, False])
            )

        # Create Subscriptions
        for user in users:
            ParkingSubscription.objects.create(
                user=user,
                parking_zone=random.choice(zones),
                start_date=timezone.now().date(),
                end_date=timezone.now().date() + timedelta(days=30),
                subscription_type='Monthly',
                active=True
            )

        # Create Parking Slot Reservation History
        for _ in range(5):
            ParkingSlotReservationHistory.objects.create(
                parking_slot=random.choice(slots),
                reserved_by=random.choice(users),
                reservation_start=timezone.now() - timedelta(days=random.randint(1, 30)),
                reservation_end=timezone.now(),
                status=random.choice(['Reserved', 'Cancelled', 'Completed'])
            )

        # Create Parking Sensors
        for slot in slots:
            ParkingSensor.objects.create(
                parking_slot=slot,
                sensor_status=random.choice(['Active', 'Inactive', 'Faulty'])
            )

        # Create User Feedback
        for user in users:
            UserFeedback.objects.create(
                user=user,
                parking_slot=random.choice(slots) if random.choice([True, False]) else None,
                feedback_text=fake.text(),
                rating=random.randint(1, 5)
            )

        # Create Discount Coupons
        for _ in range(5):
            DiscountCoupon.objects.create(
                code=fake.unique.lexify(text="?????-#####"),
                discount_percentage=random.uniform(5, 50),
                valid_from=timezone.now(),
                valid_until=timezone.now() + timedelta(days=30),
                max_usage_count=random.randint(1, 10)
            )

        # Create Parking Notifications
        for user in users:
            ParkingNotification.objects.create(
                user=user,
                notification_type=random.choice(['Reservation Reminder', 'Payment Reminder', 'General Alert']),
                message=fake.text()
            )

        self.stdout.write(self.style.SUCCESS("Fake data successfully generated! 🚀"))
