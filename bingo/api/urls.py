from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, BingoCardViewSet

router = DefaultRouter()
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'bingo-cards', BingoCardViewSet, basename='bingocard')

urlpatterns = [
    path('', include(router.urls)),
]