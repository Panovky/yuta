import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from services.photo_cropper import crop_photo
from YUTA.settings import MEDIA_ROOT
from services.utils import edit_user_data, update_user_data
from users.models import User
from users.serializers import UserSerializer


class ProfileView(View):
    def get(self, request, url_user_id):
        if not request.session['user_id']:
            return redirect('main')

        if len(request.GET) == 0:
            session_user_id = request.session['user_id']
            user = User.objects.get(id=url_user_id)

            return render(
                request,
                'profile.html',
                context={
                    **UserSerializer(user).data,
                    'menu_user_id': session_user_id,
                    'is_owner': url_user_id == session_user_id,
                    'is_default_photo': 'default-user-photo' in user.photo.url,
                    'timestamp': int(datetime.datetime.now().timestamp()),
                }
            )

        if 'user_name' in request.GET and len(request.GET) == 1:
            user_name = request.GET['user_name']
            return JsonResponse(data=User.objects.search(user_name).as_found())

    def post(self, request, url_user_id):
        if not request.session['user_id']:
            return redirect('main')
        session_user_id = request.session['user_id']
        user = User.objects.get(id=session_user_id)
        action = request.POST['action']

        if action == 'update_photo':
            photo = request.FILES['photo']
            user.photo = photo
            user.cropped_photo = photo
            user.save()
            return JsonResponse({'photo_url': user.photo.url})

        if action == 'update_miniature':
            photo_path = user.photo.name
            cropped_photo_path = f"images/users_photos/cropped-{photo_path.replace('images/users_photos/', '')}"
            crop_photo(
                f'{MEDIA_ROOT}/{photo_path}',
                f'{MEDIA_ROOT}/{cropped_photo_path}',
                int(request.POST['width']),
                int(request.POST['height']),
                int(request.POST['delta_x']),
                int(request.POST['delta_y']),
                (int(request.POST['container_width']), int(request.POST['container_height']))
            )
            return redirect('profile', session_user_id)

        if action == 'delete_photo':
            user.photo = 'images/default-user-photo.png'
            user.cropped_photo = 'images/cropped-default-user-photo.png'
            user.save()
            return redirect('profile', session_user_id)

        if action == 'edit_data':
            data = {
                'biography': request.POST['biography'],
                'phone_number': request.POST['phone_number'],
                'e_mail': request.POST['e_mail'],
                'vk': request.POST['vk']
            }
            edit_user_data(user, data)
            return redirect('profile', session_user_id)

        if action == 'update_data':
            password = request.POST['password']

            if not update_user_data(user, password):
                session_user_id = request.session['user_id']

                return render(
                    request,
                    'profile.html',
                    context={
                        **UserSerializer(user).data,
                        'menu_user_id': session_user_id,
                        'is_owner': url_user_id == session_user_id,
                        'is_default_photo': 'default-user-photo' in user.photo.url,
                        'timestamp': int(datetime.datetime.now().timestamp()),
                        'message': 'Неправильный пароль.',
                    }
                )

            return redirect('profile', session_user_id)
