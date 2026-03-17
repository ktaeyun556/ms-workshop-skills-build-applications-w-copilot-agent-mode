from django.contrib import admin

from .models import Activity, FitnessUser, LeaderboardEntry, Team, Workout


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(FitnessUser)
class FitnessUserAdmin(admin.ModelAdmin):
    list_display = ('hero_name', 'name', 'email', 'team', 'created_at')
    list_filter = ('team',)
    search_fields = ('hero_name', 'name', 'email')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'duration_minutes', 'calories_burned', 'performed_at')
    list_filter = ('activity_type',)
    search_fields = ('user__hero_name', 'activity_type')


@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ('rank', 'user', 'score')
    list_editable = ('score',)
    ordering = ('rank',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'difficulty', 'scheduled_for', 'completed')
    list_filter = ('difficulty', 'completed')
    search_fields = ('title', 'user__hero_name')
