from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Team, TeamMembership, BingoCard, Prediction, VerificationEvidence


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by_link', 'member_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'created_by__email', 'created_by__username')
    date_hierarchy = 'created_at'

    def created_by_link(self, obj):
        url = reverse('admin:users_appuser_change', args=[obj.created_by.id])
        return format_html('<a href="{}">{} {}</a>',
                         url, obj.created_by.first_name, obj.created_by.last_name)
    created_by_link.short_description = 'Created By'

    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Members'


@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'team_link', 'role', 'is_active', 'joined_at')
    list_filter = ('role', 'is_active', 'joined_at')
    search_fields = ('user__email', 'user__username', 'team__name')
    date_hierarchy = 'joined_at'

    def user_link(self, obj):
        url = reverse('admin:users_appuser_change', args=[obj.user.id])
        return format_html('<a href="{}">{} {}</a>',
                         url, obj.user.first_name, obj.user.last_name)
    user_link.short_description = 'User'

    def team_link(self, obj):
        url = reverse('admin:bingo_team_change', args=[obj.team.id])
        return format_html('<a href="{}">{}</a>', url, obj.team.name)
    team_link.short_description = 'Team'


@admin.register(BingoCard)
class BingoCardAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'team_link', 'year', 'prediction_count', 'is_active')
    list_filter = ('year', 'is_active', 'created_at')
    search_fields = ('user__email', 'user__username', 'team__name')
    date_hierarchy = 'created_at'

    def user_link(self, obj):
        url = reverse('admin:users_appuser_change', args=[obj.user.id])
        return format_html('<a href="{}">{} {}</a>',
                         url, obj.user.first_name, obj.user.last_name)
    user_link.short_description = 'User'

    def team_link(self, obj):
        url = reverse('admin:bingo_team_change', args=[obj.team.id])
        return format_html('<a href="{}">{}</a>', url, obj.team.name)
    team_link.short_description = 'Team'

    def prediction_count(self, obj):
        return obj.predictions.count()
    prediction_count.short_description = 'Predictions'


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('prediction_preview', 'card_link', 'category', 'target_period',
                   'status', 'verified_by_link')
    list_filter = ('category', 'target_period', 'status', 'created_at')
    search_fields = ('prediction_text', 'bingo_card__user__email', 'bingo_card__team__name')
    date_hierarchy = 'created_at'

    def prediction_preview(self, obj):
        return obj.prediction_text[:50] + '...' if len(obj.prediction_text) > 50 else obj.prediction_text
    prediction_preview.short_description = 'Prediction'

    def card_link(self, obj):
        url = reverse('admin:bingo_bingocard_change', args=[obj.bingo_card.id])
        return format_html('<a href="{}">{}</a>', url, str(obj.bingo_card))
    card_link.short_description = 'Bingo Card'

    def verified_by_link(self, obj):
        if obj.verified_by:
            url = reverse('admin:users_appuser_change', args=[obj.verified_by.id])
            return format_html('<a href="{}">{} {}</a>',
                             url, obj.verified_by.first_name, obj.verified_by.last_name)
        return '-'
    verified_by_link.short_description = 'Verified By'


@admin.register(VerificationEvidence)
class VerificationEvidenceAdmin(admin.ModelAdmin):
    list_display = ('prediction_link', 'submitted_by_link', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('prediction__prediction_text', 'evidence_text',
                    'submitted_by__email')
    date_hierarchy = 'created_at'

    def prediction_link(self, obj):
        url = reverse('admin:bingo_prediction_change', args=[obj.prediction.id])
        return format_html('<a href="{}">{}</a>', url, str(obj.prediction))
    prediction_link.short_description = 'Prediction'

    def submitted_by_link(self, obj):
        url = reverse('admin:users_appuser_change', args=[obj.submitted_by.id])
        return format_html('<a href="{}">{} {}</a>',
                         url, obj.submitted_by.first_name, obj.submitted_by.last_name)
    submitted_by_link.short_description = 'Submitted By'
