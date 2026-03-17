from rest_framework import viewsets

from .models import Activity, FitnessUser, LeaderboardEntry, Team, Workout
from .serializers import (
    ActivitySerializer,
    FitnessUserSerializer,
    LeaderboardEntrySerializer,
    TeamSerializer,
    WorkoutSerializer,
)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all().order_by('name')
    serializer_class = TeamSerializer


class FitnessUserViewSet(viewsets.ModelViewSet):
    queryset = FitnessUser.objects.select_related('team').all().order_by('hero_name')
    serializer_class = FitnessUserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        team_id = self.request.query_params.get('team')
        if team_id:
            queryset = queryset.filter(team_id=team_id)
        return queryset


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.select_related('user').all().order_by('-performed_at')
    serializer_class = ActivitySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset


class LeaderboardEntryViewSet(viewsets.ModelViewSet):
    queryset = LeaderboardEntry.objects.select_related('user').all().order_by('rank')
    serializer_class = LeaderboardEntrySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        top = self.request.query_params.get('top')
        if top and top.isdigit():
            return queryset[: int(top)]
        return queryset


class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.select_related('user').all().order_by('-scheduled_for')
    serializer_class = WorkoutSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user')
        completed = self.request.query_params.get('completed')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if completed in ['true', 'false']:
            target_completed = completed == 'true'
            # Djongo has limitations on some boolean SQL conversions, so keep this filter in Python.
            return [workout for workout in queryset if workout.completed == target_completed]
        return queryset
