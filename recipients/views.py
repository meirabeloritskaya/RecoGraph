from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Recipients
from .serializers import RecipientsSerializer


class RecipientsViewSet(viewsets.ModelViewSet):
    queryset = Recipients.objects.all()
    serializer_class = RecipientsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
