from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from users.models import User
from users.serializers import ShortUserSerializer


class TasksView(View):
    def get(self, request):
        if not request.session['user_id']:
            return redirect('main')

        if len(request.GET) == 0:
            session_user_id = request.session['user_id']
            user = User.objects.get(id=session_user_id)

            return render(
                request,
                'tasks.html',
                context={
                    'user': user,
                    'menu_user_id': session_user_id
                }
            )

        if 'user_name' in request.GET and len(request.GET) == 1:
            return JsonResponse(data={
                'users': [ShortUserSerializer(user).data for user in User.objects.search(request.GET['user_name'])]
            })

    def post(self, request):
        if not request.session['user_id']:
            return redirect('main')
