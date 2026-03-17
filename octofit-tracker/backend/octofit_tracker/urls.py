"""octofit_tracker URL Configuration."""
import os

from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ActivityViewSet,
    FitnessUserViewSet,
    LeaderboardEntryViewSet,
    TeamViewSet,
    WorkoutViewSet,
)

codespace_name = os.environ.get('CODESPACE_NAME')
if codespace_name:
    codespace_base_url = f"https://{codespace_name}-8000.app.github.dev"
else:
    codespace_base_url = "http://localhost:8000"

router = DefaultRouter()
router.register(r'users', FitnessUserViewSet, basename='users')
router.register(r'teams', TeamViewSet, basename='teams')
router.register(r'activities', ActivityViewSet, basename='activities')
router.register(r'leaderboard', LeaderboardEntryViewSet, basename='leaderboard')
router.register(r'workouts', WorkoutViewSet, basename='workouts')


def api_root(request):
    return JsonResponse(
        {
            "message": "OctoFit API Root",
            "collections": ["users", "teams", "activities", "leaderboard", "workouts"],
            "admin": f"{codespace_base_url}/admin/",
            "users": f"{codespace_base_url}/api/users/",
            "teams": f"{codespace_base_url}/api/teams/",
            "activities": f"{codespace_base_url}/api/activities/",
            "leaderboard": f"{codespace_base_url}/api/leaderboard/",
            "workouts": f"{codespace_base_url}/api/workouts/",
        }
    )

urlpatterns = [
    path('', api_root, name='root-api'),
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/', include(router.urls)),
]
