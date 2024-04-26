import datetime
import json
import re
from django.http import JsonResponse
from rest_framework.views import APIView
from YUTA.settings import MEDIA_ROOT
from services.photo_cropper import crop_photo
from services.utils import authorize_user, edit_user_data, update_user_data, is_team_name_unique, get_project_info
from projects.models import Project
from projects.serializers import ProjectSerializer
from teams.models import Team
from teams.serializers import TeamSerializer
from users.models import User
from users.serializers import FullUserSerializer, ShortUserSerializer


class AuthorizationView(APIView):
    def get(self, request):
        return JsonResponse({
            'status': 'failed',
            'error': 'invalid request'
        })

    def post(self, request):
        if 'login' in request.data and 'password' in request.data and len(request.data) == 2:
            login = request.data['login']
            password = request.data['password']
            user = authorize_user(login, password)

            return JsonResponse({
                'status': 'OK' if user else 'failed',
                'error': None if user else 'invalid credentials',
                'user_id': user.id if user else None
            })

        return JsonResponse({
            'status': 'failed',
            'error': 'invalid request'
        })


class SearchView(APIView):
    def get(self, request):
        if 'user_name' in request.query_params and len(request.query_params) == 1:
            return JsonResponse({
                'status': 'OK',
                'error': None,
                'users': [ShortUserSerializer(user).data for user in User.objects.search(request.query_params['user_name'])]
            })

        return JsonResponse({
            'status': 'failed',
            'error': 'invalid request'
        })


class ProfileView(APIView):
    def get(self, request):
        if 'user_id' in request.query_params and len(request.query_params) == 1:
            user_id = request.query_params['user_id']
            if not User.objects.filter(id=user_id).exists():
                return JsonResponse({
                    'status': 'failed',
                    'error': 'invalid user id',
                    'user': None
                })

            user = User.objects.get(id=user_id)
            return JsonResponse({
                'status': 'OK',
                'error': None,
                'user': FullUserSerializer(user).data
            })

        return JsonResponse({
            'status': 'failed',
            'error': 'invalid request'
        })

    def post(self, request):
        if 'user_id' in request.data and len(request.data) == 1:
            user_id = request.data['user_id']
            if not User.objects.filter(id=user_id).exists():
                return JsonResponse({
                    'status': 'failed',
                    'error': 'invalid user id'
                })

            user = User.objects.get(id=user_id)
            user.photo = 'images/default-user-photo.png'
            user.cropped_photo = 'images/cropped-default-user-photo.png'
            user.save()

            return JsonResponse({
                'status': 'OK',
                'error': None
            })

        if 'user_id' in request.data and 'photo' in request.data and len(request.data) == 2:
            user_id = request.data['user_id']
            if not User.objects.filter(id=user_id).exists():
                return JsonResponse({
                    'status': 'failed',
                    'error': 'invalid user id'
                })

            photo = request.data['photo']
            extension = photo.name.split('.')[-1]
            if extension not in ('jpg', 'jpeg', 'png'):
                return JsonResponse({
                    'status': 'failed',
                    'error': 'invalid photo extension'
                })

            user = User.objects.get(id=user_id)
            user.photo = photo
            user.cropped_photo = photo
            user.save()

            return JsonResponse({
                'status': 'OK',
                'error': None
            })

        if 'user_id' in request.data and 'container_width' in request.data and 'container_height' in request.data \
                and 'width' in request.data and 'height' in request.data and 'delta_x' in request.data \
                and 'delta_y' in request.data and len(request.data) == 7:
            user_id = request.data['user_id']
            if not User.objects.filter(id=user_id).exists():
                return JsonResponse({
                    'status': 'failed',
                    'error': 'invalid user id'
                })

            user = User.objects.get(id=user_id)
            photo_path = user.photo.name
            cropped_photo_path = f"images/users_photos/cropped-{photo_path.replace('images/users_photos/', '')}"

            crop_photo(
                f'{MEDIA_ROOT}/{photo_path}',
                f'{MEDIA_ROOT}/{cropped_photo_path}',
                int(request.data['width']),
                int(request.data['height']),
                int(request.data['delta_x']),
                int(request.data['delta_y']),
                (int(request.data['container_width']), int(request.data['container_height']))
            )

            return JsonResponse({
                'status': 'OK',
                'error': None
            })

        if 'user_id' in request.data and 'biography' in request.data and 'phone_number' in request.data and \
                'e_mail' in request.data and 'vk' in request.data and len(request.data) == 5:
            user_id = request.data['user_id']
            if not User.objects.filter(id=user_id).exists():
                return JsonResponse({
                    'status': 'failed',
                    'error': 'invalid user id'
                })

            phone_number = request.data['phone_number']
            if phone_number.strip():
                pattern = r'\+7\s\(\d{3}\)\s\d{3}-\d{2}-\d{2}'
                if re.fullmatch(pattern, phone_number) is None:
                    return JsonResponse({
                        'status': 'failed',
                        'error': 'invalid phone number format'
                    })

            vk = request.data['vk']
            if vk.strip():
                pattern = r'https://vk\.com/'
                if re.match(pattern, vk) is None:
                    return JsonResponse({
                        'status': 'failed',
                        'error': 'invalid vk url format'
                    })

            data = {
                'biography': request.data['biography'],
                'phone_number': phone_number,
                'e_mail': request.data['e_mail'],
                'vk': vk
            }

            edit_user_data(User.objects.get(id=user_id), data)
            return JsonResponse({
                'status': 'OK',
                'error': None
            })

        if 'user_id' in request.data and 'password' in request.data and len(request.data) == 2:
            user_id = request.data['user_id']
            if not User.objects.filter(id=user_id).exists():
                return JsonResponse({
                    'status': 'failed',
                    'error': 'invalid user id'
                })

            password = request.data['password']
            user = User.objects.get(id=user_id)
            success = update_user_data(user, password)
            return JsonResponse({
                'status': 'OK' if success else 'failed',
                'error': None if success else 'invalid credentials'
            })

        return JsonResponse({
            'status': 'failed',
            'error': 'invalid request'
        })


class ProjectsView(APIView):
    def get(self, request):
        if 'user_id' in request.query_params and len(request.query_params) == 1:
            user_id = request.query_params['user_id']
            if not User.objects.filter(id=user_id).exists():
                return JsonResponse({
                    'status': 'failed',
                    'error': 'invalid user id',
                    'managed_projects': None,
                    'others_projects': None,
                })

            user = User.objects.get(id=user_id)
            managed_projects = user.manager_projects.all()
            others_projects = [project for team in user.teams.all() for project in team.team_projects.all()]

            return JsonResponse({
                'status': 'OK',
                'error': None,
                'managed_projects': [ProjectSerializer(project).data for project in managed_projects],
                'others_projects': [ProjectSerializer(project).data for project in others_projects],
            })

        if 'project_id' in request.query_params and len(request.query_params) == 1:
            project_id = request.query_params['project_id']
            if not Project.objects.filter(id=project_id).exists():
                return JsonResponse({
                    'status': 'failed',
                    'error': 'invalid project id',
                    'project': None
                })

            return JsonResponse({
                'status': 'OK',
                'error': None,
                'project': get_project_info(project_id)
            })

        if 'team_name' in request.query_params and 'leader_id' in request.query_params:
            leader_id = request.query_params['leader_id']
            if not User.objects.filter(id=leader_id).exists():
                return JsonResponse({
                    'status': 'failed',
                    'error': 'invalid leader id',
                    'teams': None
                })

            team_name = request.query_params['team_name'].strip()
            leader = User.objects.get(id=leader_id)
            teams = Team.objects.filter(name__icontains=team_name) & Team.objects.filter(leader=leader)

            if 'project_team_id' in request.query_params:
                project_team_id = request.query_params['project_team_id']
                if not Team.objects.filter(id=project_team_id):
                    return JsonResponse({
                        'status': 'failed',
                        'error': 'invalid project team id',
                        'teams': None
                    })
                teams = teams.exclude(id=project_team_id)

            return JsonResponse({
                'status': 'OK',
                'error': None,
                'teams': [
                    {
                        'id': team.id,
                        'name': team.name,
                    }
                    for team in teams
                ]
            })

        return JsonResponse({
            'status': 'failed',
            'error': 'invalid request'
        })

    def post(self, request):
        if 'manager_id' in request.data and 'project_name' in request.data and 'project_description' in request.data \
                and 'project_deadline' in request.data:
            manager_id = request.data['manager_id']
            if not User.objects.filter(id=manager_id).exists():
                return JsonResponse({
                    'status': 'failed',
                    'error': 'invalid manager id'
                })

            deadline = request.data['project_deadline']
            if datetime.datetime.strptime(deadline, '%Y-%m-%d').date() < datetime.date.today():
                return JsonResponse({
                    'status': 'failed',
                    'error': 'invalid deadline'
                })

            project_team_id = request.data.get('project_team_id')
            if project_team_id is not None:
                if not Team.objects.filter(id=project_team_id).exists():
                    return JsonResponse({
                        'status': 'failed',
                        'error': 'invalid project team id'
                    })

            Project.objects.create(
                name=request.data['project_name'].strip(),
                description=request.data['project_description'].strip(),
                technical_task=request.data.get('project_technical_task'),
                deadline=deadline,
                manager_id=manager_id,
                team_id=project_team_id
            )

            return JsonResponse({
                'status': 'OK',
                'error': None
            })

        if 'project_id' in request.data and 'project_name' in request.data and 'project_description' in request.data \
                and 'project_deadline' in request.data and 'project_status' in request.data:
            project_id = request.data['project_id']
            if not Project.objects.filter(id=project_id).exists():
                return JsonResponse({
                    'status': 'failed',
                    'error': 'invalid project id'
                })

            deadline = request.data['project_deadline']
            if datetime.datetime.strptime(deadline, '%Y-%m-%d').date() < datetime.date.today():
                return JsonResponse({
                    'status': 'failed',
                    'error': 'invalid deadline'
                })

            status = request.data['project_status']
            if status not in ('в работе', 'приостановлен', 'завершен'):
                return JsonResponse({
                    'status': 'failed',
                    'error': 'invalid status'
                })

            project_team_id = request.data.get('project_team_id')
            if project_team_id is not None:
                if not Team.objects.filter(id=project_team_id).exists():
                    return JsonResponse({
                        'status': 'failed',
                        'error': 'invalid project team id'
                    })

            project = Project.objects.get(id=project_id)
            project.name = request.data['project_name'].strip()
            project.description = request.data['project_description'].strip()
            project.technical_task = request.data.get('project_technical_task')
            project.deadline = deadline
            project.status = status
            project.team_id = project_team_id
            project.save()

            return JsonResponse({
                'status': 'OK',
                'error': None
            })

        if 'project_id' in request.data and len(request.data) == 1:
            project_id = request.data['project_id']
            if not Project.objects.filter(id=project_id).exists():
                return JsonResponse({
                    'status': 'failed',
                    'error': 'invalid project id'
                })

            Project.objects.get(id=project_id).delete()
            return JsonResponse({
                'status': 'OK',
                'error': None
            })

        return JsonResponse({
            'status': 'failed',
            'error': 'invalid request'
        })


class TasksView(APIView):
    def get(self, request):
        return JsonResponse({
            'status': 'failed',
            'error': 'invalid request'
        })

    def post(self, request):
        return JsonResponse({
            'status': 'failed',
            'error': 'invalid request'
        })


class TeamsView(APIView):
    def get(self, request):
        if 'user_id' in request.query_params and len(request.query_params) == 1:
            user_id = request.query_params['user_id']
            if not User.objects.filter(id=user_id).exists():
                return JsonResponse({
                    'status': 'failed',
                    'error': 'invalid user id',
                    'managed_teams': None,
                    'others_teams': None,
                })

            user = User.objects.get(id=user_id)
            return JsonResponse({
                'status': 'OK',
                'error': None,
                'managed_teams': [TeamSerializer(team).data for team in user.leader_teams.all()],
                'others_teams': [TeamSerializer(team).data for team in user.teams.all()],
            })

        if 'team_id' in request.query_params and len(request.query_params) == 1:
            team_id = request.query_params['team_id']
            if not Team.objects.filter(id=team_id).exists():
                return JsonResponse({
                    'status': 'failed',
                    'error': 'invalid team id',
                    'team': None
                })

            return JsonResponse({
                'status': 'OK',
                'error': None,
                'team': TeamSerializer(Team.objects.get(id=team_id)).data
            })

        if 'team_name' in request.query_params and len(request.query_params) == 1:
            return JsonResponse({
                'status': 'OK',
                'error': None,
                'unique': is_team_name_unique(request.query_params['team_name'].strip())
            })

        if 'team_name' in request.query_params and 'team_id' in request.query_params and len(request.query_params) == 2:
            team_id = request.query_params['team_id']
            if not Team.objects.filter(id=team_id).exists():
                return JsonResponse({
                    'status': 'failed',
                    'error': 'invalid team id',
                    'unique': None
                })

            return JsonResponse({
                'status': 'OK',
                'error': None,
                'unique': is_team_name_unique(request.query_params['team_name'].strip(), team_id)
            })

        if 'user_name' in request.query_params and 'leader_id' in request.query_params and \
                'members_id' in request.query_params and len(request.query_params) == 3:

            leader_id = request.query_params['leader_id']
            if not User.objects.filter(id=leader_id).exists():
                return JsonResponse({
                    'status': 'failed',
                    'error': 'invalid user id',
                    'users': None
                })

            members_id = json.loads(request.query_params['members_id'])
            for member_id in members_id:
                if not User.objects.filter(id=member_id).exists():
                    return JsonResponse({
                        'status': 'failed',
                        'error': 'invalid member id',
                        'users': None
                    })

            user_name = request.query_params['user_name']
            return JsonResponse({
                'status': 'OK',
                'error': None,
                'users': [ShortUserSerializer(user).data for user in User.objects.search(user_name, leader_id, members_id)]
            })

        return JsonResponse({
            'status': 'failed',
            'error': 'invalid request'
        })

    def post(self, request):
        if 'leader_id' in request.data and 'team_name' in request.data and 'members_id' in request.data and \
                len(request.data) == 3:
            leader_id = request.data['leader_id']
            if not User.objects.filter(id=leader_id).exists():
                return JsonResponse({
                    'status': 'failed',
                    'error': 'invalid leader id'
                })

            team_name = request.data['team_name'].strip()
            if not is_team_name_unique(team_name):
                return JsonResponse({
                    'status': 'failed',
                    'error': 'non-unique team name'
                })

            members_id = request.data['members_id']
            for member_id in members_id:
                if not User.objects.filter(id=member_id).exists():
                    return JsonResponse({
                        'status': 'failed',
                        'error': 'invalid member id'
                    })

            Team.objects.create_team(
                name=team_name,
                leader_id=leader_id,
                members_id=members_id
            )

            return JsonResponse({
                'status': 'OK',
                'error': None
            })

        if 'team_id' in request.data and 'team_name' in request.data and 'members_id' in request.data and \
                len(request.data) == 3:
            team_id = request.data['team_id']
            if not Team.objects.filter(id=team_id).exists():
                return JsonResponse({
                    'status': 'failed',
                    'error': 'invalid team id'
                })

            team_name = request.data['team_name'].strip()
            if not is_team_name_unique(team_name, team_id):
                return JsonResponse({
                    'status': 'failed',
                    'error': 'non-unique team name'
                })

            members_id = request.data['members_id']
            for member_id in members_id:
                if not User.objects.filter(id=member_id).exists():
                    return JsonResponse({
                        'status': 'failed',
                        'error': 'invalid member id'
                    })

            Team.objects.update_team(
                id=team_id,
                name=team_name,
                members_id=members_id
            )

            return JsonResponse({
                'status': 'OK',
                'error': None
            })

        if 'team_id' in request.data and len(request.data) == 1:
            team_id = request.data['team_id']
            if not Team.objects.filter(id=team_id).exists():
                return JsonResponse({
                    'status': 'failed',
                    'error': 'invalid team id'
                })

            Team.objects.get(id=team_id).delete()
            return JsonResponse({
                'status': 'OK',
                'error': None
            })

        return JsonResponse({
            'status': 'failed',
            'error': 'invalid request'
        })
