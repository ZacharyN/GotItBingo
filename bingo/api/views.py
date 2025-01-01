from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from ..models import Team, TeamMembership, BingoCard, Prediction
from .serializers import (TeamSerializer, TeamMembershipSerializer,
                          BingoCardSerializer, PredictionSerializer)


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Team.objects.filter(members=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        team = self.get_object()
        TeamMembership.objects.get_or_create(
            team=team,
            user=request.user,
            defaults={'role': 'member'}
        )
        return Response({'status': 'joined team'})


class BingoCardViewSet(viewsets.ModelViewSet):
    serializer_class = BingoCardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BingoCard.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def verify_prediction(self, request, pk=None):
        card = self.get_object()
        prediction_id = request.data.get('prediction_id')
        is_correct = request.data.get('is_correct', False)

        prediction = card.predictions.get(id=prediction_id)
        prediction.status = 'correct' if is_correct else 'incorrect'
        prediction.verified_by = request.user
        prediction.verified_at = timezone.now()
        prediction.save()

        return Response({'status': 'prediction verified'})