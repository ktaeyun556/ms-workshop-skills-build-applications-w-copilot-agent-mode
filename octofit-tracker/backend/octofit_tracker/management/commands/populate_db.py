from datetime import date, timedelta

from django.core.management.base import BaseCommand

from octofit_tracker.models import Activity, FitnessUser, LeaderboardEntry, Team, Workout


class Command(BaseCommand):
    help = 'octofit_db 데이터베이스에 테스트 데이터를 입력합니다.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('기존 테스트 데이터를 정리합니다...'))
        LeaderboardEntry.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        FitnessUser.objects.all().delete()
        Team.objects.all().delete()

        marvel_team = Team.objects.create(name='marvel 팀', description='마블 히어로 팀')
        dc_team = Team.objects.create(name='dc 팀', description='DC 히어로 팀')

        users = [
            FitnessUser.objects.create(
                name='Tony Stark',
                hero_name='Iron Man',
                email='ironman@octofit.dev',
                team=marvel_team,
            ),
            FitnessUser.objects.create(
                name='Steve Rogers',
                hero_name='Captain America',
                email='captain@octofit.dev',
                team=marvel_team,
            ),
            FitnessUser.objects.create(
                name='Natasha Romanoff',
                hero_name='Black Widow',
                email='widow@octofit.dev',
                team=marvel_team,
            ),
            FitnessUser.objects.create(
                name='Clark Kent',
                hero_name='Superman',
                email='superman@octofit.dev',
                team=dc_team,
            ),
            FitnessUser.objects.create(
                name='Bruce Wayne',
                hero_name='Batman',
                email='batman@octofit.dev',
                team=dc_team,
            ),
            FitnessUser.objects.create(
                name='Diana Prince',
                hero_name='Wonder Woman',
                email='wonderwoman@octofit.dev',
                team=dc_team,
            ),
        ]

        for idx, user in enumerate(users, start=1):
            Activity.objects.create(
                user=user,
                activity_type='Running',
                duration_minutes=30 + idx,
                calories_burned=250 + idx * 10,
            )
            Activity.objects.create(
                user=user,
                activity_type='Strength Training',
                duration_minutes=40 + idx,
                calories_burned=300 + idx * 10,
            )
            Workout.objects.create(
                user=user,
                title='Power Circuit',
                difficulty='Hard' if idx % 2 == 0 else 'Medium',
                scheduled_for=date.today() + timedelta(days=idx),
                completed=idx % 3 == 0,
            )

        scores = [980, 940, 910, 890, 860, 830]
        for rank, (user, score) in enumerate(zip(users, scores), start=1):
            LeaderboardEntry.objects.create(user=user, score=score, rank=rank)

        self.stdout.write(self.style.SUCCESS('테스트 데이터 적재가 완료되었습니다.'))
