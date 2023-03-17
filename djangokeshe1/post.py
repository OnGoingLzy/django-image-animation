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
            print("正在生成...")
            client = replicate.Client(api_token='e1e0eb0081c3f30f76a15da808bbf814592c5dc7')

            model = replicate.models.get("yoyo-nb/thin-plate-spline-motion-model")
            version = model.versions.get("382ceb8a9439737020bad407dec813e150388873760ad4a5a83a2ad01b039977")

            # https://replicate.com/yoyo-nb/thin-plate-spline-motion-model/versions/382ceb8a9439737020bad407dec813e150388873760ad4a5a83a2ad01b039977#input
            inputs = {
                # Input source image.
                'source_image': open("F:\学习/2023毕设\keshe\Real_Time_Image_Animation\Inputs/"+imgname, "rb"),

                # Choose a micromotion.
                'driving_video': open("F:\学习/2023毕设\keshe\Real_Time_Image_Animation/video_input/"+videoname, "rb"),

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




