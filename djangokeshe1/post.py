import replicate
import os

from django.http import JsonResponse, HttpResponseRedirect
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from djangokeshe1 import settings
from djangokeshe1.forms import MyUserCreationForm
from djangokeshe1.model import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


@csrf_exempt
def generation_file(request):
    if request.method == 'POST':
        videoname = request.POST.get('videoName')
        print(videoname)
        imgname = request.POST.get('imgName')
        print(imgname)
        if videoname and imgname:
            # api_token = os.environ.get('REPLICATE_API_TOKEN')

            print("正在生成...")
            client = replicate.Client(api_token='r8_Z9HpRSLErn5TJEdrogLTYK8Tdwff9c54YMLIC')

            model = client.models.get("yoyo-nb/thin-plate-spline-motion-model")
            version = model.versions.get("382ceb8a9439737020bad407dec813e150388873760ad4a5a83a2ad01b039977")

            # https://replicate.com/yoyo-nb/thin-plate-spline-motion-model/versions/382ceb8a9439737020bad407dec813e150388873760ad4a5a83a2ad01b039977#input
            inputs = {
                # Input source image.
                'source_image': open(settings.IMG_ROOT + imgname, "rb"),

                # Choose a micromotion.
                'driving_video': open(settings.VIDEO_ROOT + videoname, "rb"),

                # Choose a dataset.
                'dataset_name': "vox",
            }

            # https://replicate.com/yoyo-nb/thin-plate-spline-motion-model/versions/382ceb8a9439737020bad407dec813e150388873760ad4a5a83a2ad01b039977#output-schema
            output = version.predict(**inputs)
            print(output)
            return JsonResponse({'status': 'success', 'videosrc': output})
        else:
            return JsonResponse({'status': 'error', 'message': '视频、图片不存在'})
    else:
        return JsonResponse({'status': 'error', 'message': '非法请求'})


# 以下为chat的post
def get_users(request):
    # 从数据库中获取所有用户信息
    users = User.objects.all()

    # 将用户信息转换为 JSON 格式，并返回给客户端
    response_data = {
        'users': list(users.values()),
    }
    return JsonResponse(response_data)


def login_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        try:
            user = User.objects.get(phone_number=phone_number)
            print(user)
            if user.check_password(password):
                request.session['user_id'] = user.id
                if remember == '1':
                    # 7天过期=604800
                    request.session.set_expiry(604800)
                    return JsonResponse({'success': True, 'message': '登录成功'})
                else:
                    request.session.set_expiry(10)
                    return JsonResponse({'success': True, 'message': '登录成功'})
            else:
                return JsonResponse({'success': False, 'message': '电话号码或密码错误'})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': '该用户不存在'})
    else:
        return JsonResponse({'success': False, 'message': '请使用POST方法'})


def logout_view(request):
    request.session.flush()  # 清空该用户的所有session信息
    # 重定向到登录页面，并添加时间戳参数
    return redirect("http://127.0.0.1:8000/sign-in/")


def register(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        username = request.POST.get('username')
        email = request.POST.get('email')
        # 检查是否已存在相同电话号码的用户
        if User.objects.filter(phone_number=phone_number).exists():
            return JsonResponse({'success': False, 'message': '注册失败,账号已存在'})  # 如果存在，返回False表示创建失败
        user = User.objects.create(
            phone_number=phone_number,
            username=username,
            password=password,
            email=email,
            chat_count=0,
            is_premium=0,
        )
        user.save()
        return JsonResponse({'success': True, 'message': '注册成功'})



