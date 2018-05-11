from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pytz import timezone
import datetime
import json

# Create your views here.

def keyboard(request) :

	return JsonResponse (
		{
		'type' : 'buttons',
		'buttons' : ['학식', '내일의 학식', '시간별 학식']
		}
	)

@csrf_exempt
def message(request) :

	json_str = (request.body).decode('utf-8')
	received_json = json.loads(json_str)
	content_name = received_json['content']
	type_name = received_json['type']
	user_name = received_json['user_key']

	# 오늘
	today = datetime.datetime.today()

	local_date1 = today.strftime('%Y년 %m월 %d일')
	local_weekday1 = today.weekday()

	# 내일
	tomorrow = datetime.datetime.today() + datetime.timedelta(days = 1)

	local_date2 = tomorrow.strftime('%Y년 %m월 %d일')
	local_weekday2 = tomorrow.weekday()

	if content_name == '학식' :
		return JsonResponse (
			{
				'message' :
				{
					'text' : '선택한 버튼 : ' + content_name + '\n' + '오늘은 ' + today + '입니다.'
				},
				'keyboard' :
				{
					'type' : 'button',
					'buttons' : ['학식', '내일의 학식', '시간별 학식']
				}
			}
		)

	elif content_name == '내일의 학식' :
		return JsonResponse (
			{
				'message' :
				{
					'text' : '선택한 버튼 : ' + content_name + '\n' + '오늘은 ' + today + '입니다.'
				},
				'keyboard' :
				{
					'type' : 'button',
					'buttons' : ['학식', '내일의 학식', '시간별 학식']
				}
			}
		)

	elif content_name == '시간별 학식' :
		return JsonResponse (
			{
				'message' :
				{
					'text' : '선택한 버튼 : ' + content_name + '\n' + '오늘은 ' + today + '입니다.'
				},
				'keyboard' :
				{
					'type' : 'button',
					'buttons' : ['학식', '내일의 학식', '시간별 학식']
				}
			}
		)

	else :
		mess = '심각한 오류입니다. 개발자에게 알려주세요'

		if type_name == 'photo' :
			mess = '사진 보내도 기능이 없네요. 버튼을 눌러주세요!'

		elif type_name == 'video' :
			mess = '영상을 보내도 기능이 없네요. 버튼을 눌러주세요!'

		elif type_name == 'audio' :
			mess = '녹음 파일을 보내도 기능이 없네요. 버튼을 눌러주세요!'

		return JsonResponse (
			{
				'message' :
				{
					'text' : mess
				},
				'keyboard' :
				{
					'type' : 'button',
					'buttons' : ['학식', '내일의 학식', '시간별 학식']
				}
			}
		)
