import datetime
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from services.utils import is_team_name_unique
from users.models import User
from .models import Team
from .serializers import TeamSerializer


class TeamsView(View):
    def get(self, request):
        if not request.session['user_id']:
            return redirect('main')

        if len(request.GET) == 0:
            session_user_id = request.session['user_id']
            user = User.objects.get(id=session_user_id)
            return render(
                request,
                'teams.html',
                context={
                    'managed_teams': user.leader_teams.all(),
                    'others_teams': user.teams.all(),
                    'timestamp': int(datetime.datetime.now().timestamp()),
                    'menu_user_id': session_user_id
                }
            )

        if 'team_id' in request.GET and len(request.GET) == 1:
            return JsonResponse(data=TeamSerializer(Team.objects.get(id=request.GET['team_id'])).data)

        if 'team_name' in request.GET and len(request.GET) == 1:
            return JsonResponse({'unique': is_team_name_unique(request.GET['team_name'].strip())})

        if 'team_name' in request.GET and 'team_id' in request.GET and len(request.GET) == 2:
            return JsonResponse({'unique': is_team_name_unique(request.GET['team_name'].strip(), request.GET['team_id'])})

        if 'user_name' in request.GET and 'members_id' in request.GET and len(request.GET) == 2:
            user_name = request.GET['user_name']
            leader_id = request.session['user_id']
            members_id = json.loads(request.GET['members_id'])
            return JsonResponse(data=User.objects.search(user_name, leader_id, members_id).as_found())

        if 'user_name' in request.GET and len(request.GET) == 1:
            return JsonResponse(data=User.objects.search(request.GET['user_name']).as_found())

    def post(self, request):
        if not request.session['user_id']:
            return redirect('main')
        action = request.POST['action']

        if action == 'delete_team':
            team_id = request.POST['team_id']
            Team.objects.get(id=team_id).delete()
            return redirect('teams')

        if action == 'create_team':
            team_name = request.POST['team_name'].strip()
            team_leader = User.objects.get(id=request.session['user_id'])

            team = Team.objects.create(
                name=team_name,
                leader=team_leader
            )

            team_members_id = json.loads(request.POST['members_id'])
            for member_id in team_members_id:
                member = User.objects.get(id=member_id)
                team.members.add(member)
                member.teams.add(team)

            return redirect('teams')

        if action == 'edit_team':
            team_id = request.POST['team_id']
            team_name = request.POST['team_name'].strip()
            team = Team.objects.get(id=team_id)
            team.name = team_name

            team.members.clear()
            team_members_id = json.loads(request.POST['members_id'])
            for member_id in team_members_id:
                member = User.objects.get(id=member_id)
                team.members.add(member)
                member.teams.add(team)

            team.save()
            return redirect('teams')
