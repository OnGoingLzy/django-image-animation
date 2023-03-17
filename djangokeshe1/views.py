import os

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from djangokeshe1 import settings


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

