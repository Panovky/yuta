import datetime
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from services.utils import is_team_name_unique
from users.models import User
from users.serializers import ShortUserSerializer
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
            return JsonResponse(data={
                'users': [ShortUserSerializer(user).data for user in User.objects.search(user_name, leader_id, members_id)]
            })

        if 'user_name' in request.GET and len(request.GET) == 1:
            return JsonResponse(data={
                'users': [ShortUserSerializer(user).data for user in User.objects.search(request.GET['user_name'])]
            })

    def post(self, request):
        if not request.session['user_id']:
            return redirect('main')

        if 'team_name' in request.POST and 'members_id' in request.POST and len(request.POST) == 2:
            Team.objects.create_team(
                name=request.POST['team_name'].strip(),
                leader_id=request.session['user_id'],
                members_id=json.loads(request.POST['members_id'])
            )
            return redirect('teams')

        if 'team_id' in request.POST and 'team_name' in request.POST and 'members_id' in request.POST and \
                len(request.POST) == 3:
            Team.objects.update_team(
                id=request.POST['team_id'],
                name=request.POST['team_name'].strip(),
                members_id=json.loads(request.POST['members_id'])
            )
            return redirect('teams')

        if 'team_id' in request.POST and len(request.POST) == 2:
            Team.objects.get(id=request.POST['team_id']).delete()
            return redirect('teams')
