import replicate
import os

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from djangokeshe1 import settings

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
                'source_image': open(settings.IMG_ROOT+imgname, "rb"),

                # Choose a micromotion.
                'driving_video': open(settings.VIDEO_ROOT+videoname, "rb"),

                # Choose a dataset.
                'dataset_name': "vox",
            }

            # https://replicate.com/yoyo-nb/thin-plate-spline-motion-model/versions/382ceb8a9439737020bad407dec813e150388873760ad4a5a83a2ad01b039977#output-schema
            output = version.predict(**inputs)
            print(output)
            return JsonResponse({'status': 'success','videosrc': output})
        else:
            return JsonResponse({'status': 'error', 'message': '视频、图片不存在'})
    else:
        return JsonResponse({'status': 'error', 'message': '非法请求'})




