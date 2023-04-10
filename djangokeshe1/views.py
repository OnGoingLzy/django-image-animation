import os

from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from djangokeshe1 import settings
from djangokeshe1.model import User
import random
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from datetime import date, timedelta, datetime
from .model import ChatCount
# 要实现未登录时只能访问登录和注册页面，而其他页面拦截并跳转到登录页面，可以使用Django的装饰器来实现
# 。在views.py中定义一个装饰器，检查用户是否登录，如果没有登录，则重定向到登录页面。
from django.shortcuts import redirect


def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('sign-in')  # 跳转到登录页面
        else:
            return view_func(request, *args, **kwargs)

    return wrapper


def index(request):
    context = {}
    context['webname'] = '图像动画在线生成!'
    return render(request, 'test.html', context)


def generation(request):
    return render(request, 'generation.html')


@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        video = request.FILES.get('video1')
        print(video)
        img = request.FILES.get('img1')
        print(img)
        if video and img:
            print("已使用uploadfile")
            video_name = video.name
            img_name = img.name
            video_path = os.path.join(settings.VIDEO_ROOT, video_name)
            img_path = os.path.join(settings.IMG_ROOT, img_name)
            print(settings.VIDEO_ROOT)
            print(img_path)
            with open(video_path, 'wb+') as destination:
                for chunk in video.chunks():
                    destination.write(chunk)
            with open(img_path, 'wb+') as destination:
                for chunk in img.chunks():
                    destination.write(chunk)
            return JsonResponse({'status': 'success', 'videoName': video_name, 'imgName': img_name})
        else:
            return JsonResponse({'status': 'error', 'message': '请上传两个文件'})
    else:
        return JsonResponse({'status': 'error', 'message': '非法请求'})


# 以下为chat的views
def sign_in(request):
    return render(request, "sign-in.html")


# @login_required需要验证登录的网页
@login_required
def dashboard(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    context = {'user': user}
    return render(request, "dashboard.html", context)


@login_required
def price(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    context = {'user': user}
    return render(request, "price.html", context)


def register(request):
    return render(request, "register.html")


# pip install aliyun-python-sdk-core
# pip install aliyun-python-sdk-dysmsapi 阿里云短信服务
@csrf_exempt
def send_sms(req):
    phone_number = req.POST['phone_number']
    access_key_id = 'x'
    access_key_secret = 'x'
    sign_name = 'x'
    template_code = 'x'
    acs_client = AcsClient(access_key_id, access_key_secret, 'cn-hangzhou')
    code = ''.join(random.sample('0123456789', 6))
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')
    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', phone_number)
    request.add_query_param('SignName', sign_name)
    request.add_query_param('TemplateCode', template_code)
    request.add_query_param('TemplateParam', json.dumps({'code': code}))
    response = acs_client.do_action_with_exception(request)
    print(response)
    print("生成" + code)
    return JsonResponse({'success': True, 'message': '验证码发送成功', 'code': code})


@login_required
@csrf_exempt
def chat_count_data(request):
    user_id = request.session.get('user_id')  # 从session中获取用户ID
    today = datetime.today()
    days = []
    counts = []
    for i in range(30):
        # 计算30天内每天的聊天次数
        date1 = today - timedelta(days=i)
        count = ChatCount.objects.filter(user_id=user_id, chat_date=date1).aggregate(Sum('count'))['count__sum'] or 0
        days.append(date1.strftime('%Y-%m-%d'))
        counts.append(count)
    data = dict(zip(days, counts))
    return JsonResponse(data)
