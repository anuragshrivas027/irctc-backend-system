from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import transaction
from .models import Booking
from .serializers import BookingSerializer
from trains.models import Train


# ===============================
# Create Booking (Seat Validation)
# ===============================
class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        train_id = request.data.get('train')
        seats_requested = request.data.get('seats_booked')

        # Basic validation
        if not train_id or not seats_requested:
            return Response(
                {"error": "Train ID and seats_booked are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            seats_requested = int(seats_requested)
        except ValueError:
            return Response(
                {"error": "seats_booked must be a number"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Lock row for safe seat deduction
            train = Train.objects.select_for_update().get(id=train_id)
        except Train.DoesNotExist:
            return Response(
                {"error": "Train not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if train.available_seats < seats_requested:
            return Response(
                {"error": "Not enough seats available"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Deduct seats
        train.available_seats -= seats_requested
        train.save()

        # Create booking
        booking = Booking.objects.create(
            user=request.user,
            train=train,
            seats_booked=seats_requested
        )

        return Response(
            BookingSerializer(booking).data,
            status=status.HTTP_201_CREATED
        )


# ===============================
# Get Logged-in User Bookings
# ===============================
class MyBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)