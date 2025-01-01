from rest_framework import serializers
from ..models import Team, TeamMembership, BingoCard, Prediction, VerificationEvidence


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'created_by', 'created_at', 'is_active']
        read_only_fields = ['created_by', 'created_at']


class TeamMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMembership
        fields = ['id', 'team', 'user', 'role', 'joined_at', 'is_active']
        read_only_fields = ['joined_at']


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ['id', 'position', 'category', 'prediction_text',
                  'target_period', 'status', 'verified_by', 'verified_at']
        read_only_fields = ['verified_by', 'verified_at']


class BingoCardSerializer(serializers.ModelSerializer):
    predictions = PredictionSerializer(many=True, read_only=True)

    class Meta:
        model = BingoCard
        fields = ['id', 'user', 'team', 'year', 'predictions',
                  'created_at', 'is_active']
        read_only_fields = ['created_at']


class VerificationEvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationEvidence
        fields = ['id', 'prediction', 'evidence_url', 'evidence_text',
                  'submitted_by', 'created_at']
        read_only_fields = ['submitted_by', 'created_at']