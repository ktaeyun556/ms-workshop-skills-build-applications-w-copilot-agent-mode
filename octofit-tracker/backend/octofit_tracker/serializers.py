from rest_framework import serializers

from .models import Activity, FitnessUser, LeaderboardEntry, Team, Workout


class BaseObjectIdSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        return str(obj.pk)


class TeamSerializer(BaseObjectIdSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'description']


class FitnessUserSerializer(BaseObjectIdSerializer):
    team = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), required=False, allow_null=True, write_only=True
    )
    team_id = serializers.SerializerMethodField()

    def get_team_id(self, obj):
        return str(obj.team_id) if obj.team_id else None

    class Meta:
        model = FitnessUser
        fields = ['id', 'name', 'hero_name', 'email', 'team', 'team_id', 'created_at']
        read_only_fields = ['created_at']


class ActivitySerializer(BaseObjectIdSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=FitnessUser.objects.all(), write_only=True)
    user_id = serializers.SerializerMethodField()

    def get_user_id(self, obj):
        return str(obj.user_id)

    class Meta:
        model = Activity
        fields = [
            'id',
            'user',
            'user_id',
            'activity_type',
            'duration_minutes',
            'calories_burned',
            'performed_at',
        ]
        read_only_fields = ['performed_at']


class LeaderboardEntrySerializer(BaseObjectIdSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=FitnessUser.objects.all(), write_only=True)
    user_id = serializers.SerializerMethodField()

    def get_user_id(self, obj):
        return str(obj.user_id)

    class Meta:
        model = LeaderboardEntry
        fields = ['id', 'user', 'user_id', 'score', 'rank']


class WorkoutSerializer(BaseObjectIdSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=FitnessUser.objects.all(), write_only=True)
    user_id = serializers.SerializerMethodField()

    def get_user_id(self, obj):
        return str(obj.user_id)

    class Meta:
        model = Workout
        fields = ['id', 'user', 'user_id', 'title', 'difficulty', 'scheduled_for', 'completed']
