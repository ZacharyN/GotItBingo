from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
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
        return BingoCard.objects.filter(user=self.request.user).prefetch_related('predictions')

    def perform_create(self, serializer):
        # When creating a new card, initialize with empty predictions
        card = serializer.save(user=self.request.user)
        # Create 25 empty predictions
        predictions = [
            Prediction(
                bingo_card=card,
                position=i,
                category='pending',
                prediction_text='',
                target_period='Q2'  # Default to Q2
            ) for i in range(25)
        ]
        Prediction.objects.bulk_create(predictions)
        return card

    def validate_predictions(self, predictions, is_final=False):
        # Skip strict validation if not final
        if not is_final:
            return

        category_counts = {
            'politics': 0,
            'economics': 0,
            'society': 0,
            'wildcard': 0
        }

        for prediction in predictions:
            if prediction.get('target_period') == 'Q1':
                raise ValidationError(
                    "Predictions cannot be made for Q1 (January-March)"
                )

            category = prediction.get('category')
            if category in category_counts:
                category_counts[category] += 1

        # Only check minimum requirements if this is a final save
        if is_final:
            for category, count in category_counts.items():
                if count < 4:
                    raise ValidationError(
                        f"Need at least 4 {category} predictions. Current: {count}"
                    )

    @action(detail=True, methods=['post'])
    def update_prediction(self, request, pk=None):
        """Update a single prediction on the card"""
        card = self.get_object()
        position = request.data.get('position')
        prediction_text = request.data.get('prediction_text')
        category = request.data.get('category')

        try:
            prediction = card.predictions.get(position=position)
            prediction.prediction_text = prediction_text
            prediction.category = category
            prediction.save()
            return Response(PredictionSerializer(prediction).data)
        except Prediction.DoesNotExist:
            return Response(
                {'error': 'Prediction not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def finalize(self, request, pk=None):
        """Finalize the card and validate all requirements"""
        card = self.get_object()
        predictions = card.predictions.all()
        try:
            self.validate_predictions(predictions, is_final=True)
            card.is_finalized = True
            card.save()
            return Response({'status': 'card finalized'})
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

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