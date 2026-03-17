from django.db import models
from django.utils import timezone


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'teams'
        ordering = ['name']

    def __str__(self):
        return self.name


class FitnessUser(models.Model):
    name = models.CharField(max_length=120)
    hero_name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='members')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'users'
        ordering = ['hero_name']

    def __str__(self):
        return self.hero_name


class Activity(models.Model):
    user = models.ForeignKey(FitnessUser, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=80)
    duration_minutes = models.PositiveIntegerField()
    calories_burned = models.PositiveIntegerField()
    performed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'activities'
        ordering = ['-performed_at']

    def __str__(self):
        return f"{self.activity_type} - {self.user.hero_name}"


class LeaderboardEntry(models.Model):
    user = models.OneToOneField(FitnessUser, on_delete=models.CASCADE, related_name='leaderboard_entry')
    score = models.PositiveIntegerField(default=0)
    rank = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['rank']

    def __str__(self):
        return f"#{self.rank} {self.user.hero_name} ({self.score})"


class Workout(models.Model):
    user = models.ForeignKey(FitnessUser, on_delete=models.CASCADE, related_name='workouts')
    title = models.CharField(max_length=120)
    difficulty = models.CharField(max_length=20)
    scheduled_for = models.DateField()
    completed = models.BooleanField(default=False)

    class Meta:
        db_table = 'workouts'
        ordering = ['-scheduled_for']

    def __str__(self):
        return f"{self.title} - {self.user.hero_name}"
