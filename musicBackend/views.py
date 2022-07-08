from pygame.mixer import music as pm
from django.shortcuts import render
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
import os
import mutagen


# Create your views here.

@csrf_exempt
@require_http_methods(["POST"])
def switch_album(request):
    response = {}
    try:
        assets_dir = "/root/assets/"
        album_list = os.listdir(assets_dir)
        old_index = json.loads(request.body)['album_index']
        cur_index = (old_index + 1) % len(album_list)

        album_dir = assets_dir + album_list[cur_index]+"/"
        music_list = os.listdir(album_dir)
        for index, file_name in enumerate(music_list):
            if not file_name.endswith(("mp3", "wav", "flac")):
                music_list.pop(index)
        music_file = album_dir + music_list[0]
        info = mutagen.File(music_file)
        for k, v in info.items():
            response[k] = " ".join(v)
        response['index'] = 0
        response['album_index'] = cur_index
        response['msg'] = 'success'
        response['error_num'] = 0

        pm.load(music_file)
        print(music_file)
        pm.play()
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def play_next(request):
    response = {}
    try:
        album_dir = "/root/assets/"+json.loads(request.body)['album']+"/"
        music_list = os.listdir(album_dir)
        for index, file_name in enumerate(music_list):
            if not file_name.endswith(("mp3", "wav", "flac")):
                music_list.pop(index)
        old_index = json.loads(request.body)['index']
        cur_index = (old_index + 1) % len(music_list)
        music_file = album_dir + music_list[cur_index]
        info = mutagen.File(music_file)
        for k, v in info.items():
            response[k] = " ".join(v)
        response['index'] = cur_index
        response['msg'] = 'success'
        response['error_num'] = 0

        pm.load(music_file)
        print(music_file)
        pm.play()
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
        print(e)

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def play_prev(request):
    response = {}
    try:
        album_dir = "/root/assets/"+json.loads(request.body)['album']+"/"
        music_list = os.listdir(album_dir)
        for index, file_name in enumerate(music_list):
            if not file_name.endswith(("mp3", "wav", "flac")):
                music_list.pop(index)
        old_index = json.loads(request.body)['index']
        cur_index = (old_index - 1) % len(music_list)
        music_file = album_dir+music_list[cur_index]
        info = mutagen.File(music_file)
        for k, v in info.items():
            response[k] = " ".join(v)
        response['index'] = cur_index
        response['msg'] = 'success'
        response['error_num'] = 0

        pm.load(music_file)
        print(music_file)
        pm.play()
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["GET"])
def pause(request):
    response = {}
    try:
        pm.pause()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["GET"])
def resume(request):
    response = {}
    try:
        pm.unpause()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["GET"])
def volume_increase(request):
    response = {}
    try:
        pm.set_volume((pm.get_volume()+0.01) * 1.5)
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["GET"])
def volume_decrease(request):
    response = {}
    try:
        pm.set_volume(pm.get_volume() / 1.5)
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)
