from rest_framework import generics, permissions
from .models import Train
from .serializers import TrainSerializer

from config.utils.mongo import log_train_search
import time
# Admin: Create Train
class TrainCreateView(generics.CreateAPIView):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    permission_classes = [permissions.IsAdminUser]


# Search Trains
class TrainSearchView(generics.ListAPIView):
    serializer_class = TrainSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        start_time = time.time()

        source = self.request.query_params.get('source')
        destination = self.request.query_params.get('destination')

        queryset = Train.objects.all()

        if source:
            queryset = queryset.filter(source__iexact=source)

        if destination:
            queryset = queryset.filter(destination__iexact=destination)

        execution_time = time.time() - start_time

        log_train_search(
            user_id=self.request.user.id,
            source=source,
            destination=destination,
            execution_time=execution_time
        )

        return queryset