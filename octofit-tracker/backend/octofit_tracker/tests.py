from datetime import date

from django.test import TestCase
from rest_framework.test import APIClient

from .models import Activity, FitnessUser, LeaderboardEntry, Team, Workout


class OctofitCollectionsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.team = Team.objects.create(name='Alpha Team', description='Core training team')
        self.user = FitnessUser.objects.create(
            name='Peter Parker',
            hero_name='Spider-Man',
            email='spiderman@example.com',
            team=self.team,
        )
        Activity.objects.create(
            user=self.user,
            activity_type='Running',
            duration_minutes=35,
            calories_burned=320,
        )
        LeaderboardEntry.objects.create(user=self.user, score=1200, rank=1)
        Workout.objects.create(
            user=self.user,
            title='Leg Day Blast',
            difficulty='medium',
            scheduled_for=date(2026, 3, 18),
            completed=False,
        )

    def _results(self, payload):
        if isinstance(payload, dict):
            return payload.get('results', payload)
        return payload

    def test_api_root_lists_supported_collections(self):
        response = self.client.get('/api/')

        self.assertEqual(response.status_code, 200)
        self.assertIn('collections', response.json())
        self.assertIn('users', response.json()['collections'])
        self.assertIn('teams', response.json()['collections'])
        self.assertIn('activities', response.json()['collections'])
        self.assertIn('leaderboard', response.json()['collections'])
        self.assertIn('workouts', response.json()['collections'])

    def test_users_collection_returns_data(self):
        response = self.client.get('/api/users/')

        self.assertEqual(response.status_code, 200)
        results = self._results(response.json())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['hero_name'], 'Spider-Man')

    def test_teams_collection_returns_data(self):
        response = self.client.get('/api/teams/')

        self.assertEqual(response.status_code, 200)
        results = self._results(response.json())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'Alpha Team')

    def test_activities_collection_can_filter_by_user(self):
        response = self.client.get(f'/api/activities/?user={self.user.pk}')

        self.assertEqual(response.status_code, 200)
        results = self._results(response.json())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['activity_type'], 'Running')

    def test_leaderboard_collection_supports_top_filter(self):
        response = self.client.get('/api/leaderboard/?top=1')

        self.assertEqual(response.status_code, 200)
        results = self._results(response.json())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['rank'], 1)

    def test_workouts_collection_can_filter_by_completion(self):
        response = self.client.get('/api/workouts/?completed=false')

        self.assertEqual(response.status_code, 200)
        results = self._results(response.json())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Leg Day Blast')
