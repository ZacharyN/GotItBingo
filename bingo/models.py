from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class Team(models.Model):
    name = models.CharField(_('team name'), max_length=100, unique=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_teams',
        verbose_name=_('created by')
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='TeamMembership',
        related_name='bingo_teams',
        verbose_name=_('members')
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    is_active = models.BooleanField(_('active'), default=True)

    class Meta:
        verbose_name = _('team')
        verbose_name_plural = _('teams')
        ordering = ['name']

    def __str__(self):
        return self.name


class TeamMembership(models.Model):
    ROLE_CHOICES = [
        ('admin', _('Admin')),
        ('member', _('Member')),
    ]

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        verbose_name=_('team')
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('user')
    )
    role = models.CharField(
        _('role'),
        max_length=20,
        choices=ROLE_CHOICES,
        default='member'
    )
    joined_at = models.DateTimeField(_('joined at'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)

    class Meta:
        verbose_name = _('team membership')
        verbose_name_plural = _('team memberships')
        unique_together = ['team', 'user']
        ordering = ['team', 'user']

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.team.name} ({self.get_role_display()})"


class BingoCard(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bingo_cards',
        verbose_name=_('user')
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='bingo_cards',
        verbose_name=_('team')
    )
    year = models.IntegerField(
        _('year'),
        validators=[MinValueValidator(2025), MaxValueValidator(2100)]
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    is_active = models.BooleanField(_('active'), default=True)

    class Meta:
        verbose_name = _('bingo card')
        verbose_name_plural = _('bingo cards')
        unique_together = ['user', 'team', 'year']
        ordering = ['-year', 'user']

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s {self.year} card - {self.team.name}"


class Prediction(models.Model):
    CATEGORY_CHOICES = [
        ('politics', _('Politics')),
        ('economics', _('Economics')),
        ('society', _('Society')),
        ('wildcard', _('Wild Card')),
    ]

    PERIOD_CHOICES = [
        ('Q2', _('Apr-Jun 2025')),
        ('Q3', _('Jul-Sep 2025')),
        ('Q4', _('Oct-Dec 2025')),
    ]

    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('correct', _('Correct')),
        ('incorrect', _('Incorrect')),
    ]

    bingo_card = models.ForeignKey(
        BingoCard,
        on_delete=models.CASCADE,
        related_name='predictions',
        verbose_name=_('bingo card')
    )
    position = models.IntegerField(
        _('position'),
        validators=[MinValueValidator(0), MaxValueValidator(24)]
    )
    category = models.CharField(_('category'), max_length=50, choices=CATEGORY_CHOICES)
    prediction_text = models.TextField(_('prediction'))
    target_period = models.CharField(_('target period'), max_length=10, choices=PERIOD_CHOICES)
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='verified_predictions',
        verbose_name=_('verified by')
    )
    verified_at = models.DateTimeField(_('verified at'), null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('prediction')
        verbose_name_plural = _('predictions')
        unique_together = ['bingo_card', 'position']
        ordering = ['position']

    def __str__(self):
        return f"Square {self.position}: {self.prediction_text[:50]}"


class VerificationEvidence(models.Model):
    prediction = models.ForeignKey(
        Prediction,
        on_delete=models.CASCADE,
        related_name='evidence',
        verbose_name=_('prediction')
    )
    evidence_url = models.URLField(_('evidence URL'))
    evidence_text = models.TextField(_('evidence text'), blank=True)
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submitted_evidence',
        verbose_name=_('submitted by')
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('verification evidence')
        verbose_name_plural = _('verification evidence')
        ordering = ['-created_at']

    def __str__(self):
        return f"Evidence for {self.prediction}"
