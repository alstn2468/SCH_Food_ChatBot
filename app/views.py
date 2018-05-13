from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pytz import timezone
from bs4 import BeautifulSoup
import requests, os, re
import datetime
import json

# 데이터 목록
# menu/SnowFlowerOne.json     향설1 생활관
# menu/SnowFlowerTwo.json     향설2 생활관
# menu/SnowFlowerThree.json   향설3 생활관
# menu/StudentUnion.json      학생 회관
# menu/FacultyRestaurant.json 교직원 식당

# 개발자 정보 메세지
dev_info = '''[*] 컴퓨터소프트웨어공학과
[*] 17학번 김민수
[*] Github : alstn2468
[*] KakaoTalk : alstn2468
[*] 새로운 기능 문의 환영
[*] 에러 발견 문의 환영'''

# 연속 동일 요청 메세지
stop_message = '''[*] 연속 동일 요청입니다.
[*] 나중에 다시 시도해주세요.'''

# 선택한 버튼이 학식 메뉴일 경우 메세지 포매팅
select_button = '[*] 선택한 버튼 : {0}\n[*] {1}의\n[*] {0} 메뉴입니다.\n'

# 데이터를 보기 좋게 출력하기 위한 문자열 처리 함수
def char_replace(meal) :

	meal = meal.translate({ ord('['): '', ord(']'): '', ord('{'): '', ord('}'): '', ord("'"): '', ord(','): '\n', ord(':'): '\n',ord(' '): ''})
	meal = meal.replace('\n', '\n·')
	meal = meal.replace('-중식/석식-', '\n[중식/석식]')
	meal = meal.replace('-조식-', '\n[조식]')
	meal = meal.replace('-컵밥-', '\n[컵밥]')
	meal = meal.replace('-중식-', '\n[중식]')
	meal = meal.replace('-석식-', '\n[석식]')
	meal = meal.replace('-한식-', '\n[한식]')
	meal = meal.replace('-덮밥-', '\n[덮밥]')
	meal = meal.replace('-양식-', '\n[양식]')
	meal = meal.replace('-도시락-', '\n[도시락]')
	meal = meal.replace('-스페셜메뉴-', '\n[스페셜메뉴]')
	meal = meal.replace('-돈까스-', '\n[돈까스]')
	meal = meal.replace('-라면-', '\n[라면]')
	meal = meal.replace('-메뉴-', '\n[메뉴]')
	meal = meal.replace('-부대라면-', '\n[부대라면]')
	meal = meal.replace('-한정메뉴-', '\n[한정메뉴]')
	meal = meal.replace('-샐러드바-', '\n[샐러드바]')
	meal = meal.replace('\n·\n', '\n\n')

	return meal

# 사용자의 과도한 접근을 차단하기 위한 클래스
class user_chk() :

    def __init__(self) :
        self.pre_key = "" #이전 user_key값
        self.now_key = "" #현재 user_key값

    def check(self, key) :
        self.now_key = key # now_key값에 현재 user_key값 대입

        if self.pre_key == self.now_key : # 비교 하여 같으면 1을 반환
            passcode = 1

        else :
            self.pre_key = self.now_key # 다를 경우 pre_key값에 now_key값을 덮어쓰고 0 반환
            passcode = 0

        return passcode

# 조건별 다르게 사용
user0 = user_chk()
user1 = user_chk()
user2 = user_chk()
user3 = user_chk()
user4 = user_chk()
user5 = user_chk()
user6 = user_chk()
user7 = user_chk()
user8 = user_chk()

# 결과를 출력하고 다시 입력을 받기 위한 함수
def re_process(output) :

    return JsonResponse (
		{
            'message':
			{
                'text': output
            },
            'keyboard':
			{
                'type': 'buttons',
                'buttons' : ['향설1 생활관', '향설2 생활관', '향설3 생활관', '학생회관', '교직원 식당', '종강', '학사 일정', '개발자 정보']
            }
        }
	)

def keyboard(request) :

	return JsonResponse (
		{
		'type' : 'buttons',
		'buttons' : ['향설1 생활관', '향설2 생활관', '향설3 생활관', '학생회관', '교직원 식당', '종강', '학사 일정' '개발자 정보']
		}
	)

@csrf_exempt
def answer(request) :

	json_str = (request.body).decode('utf-8')
	received_json = json.loads(json_str)
	content_name = received_json['content']
	type_name = received_json['type']
	user_key = received_json['user_key']

	# 오늘
	today = datetime.datetime.now()
	today_info = today.strftime('%Y년 %m월 %d일')
	today_weekday = today.weekday()

	if content_name == '향설1 생활관' :
		if user0.check(user_key) :
			return re_process(stop_message)

		try :
			with open('app/menu/SnowFlowerOne.json', 'rb') as f :
				datas = json.load(f)

			if today_weekday == 0 :
				meal = str(datas.get('월'))
				meal = char_replace(meal)

			elif today_weekday == 1 :
				meal = str(datas.get('화'))
				meal = char_replace(meal)

			elif today_weekday == 2 :
				meal = str(datas.get('수'))
				meal = char_replace(meal)

			elif today_weekday == 3 :
				meal = str(datas.get('목'))
				meal = char_replace(meal)

			elif today_weekday == 4 :
				meal = str(datas.get('금'))
				meal = char_replace(meal)

			elif today_weekday == 5 :
				meal = str(datas.get('토'))
				meal = char_replace(meal)

			else :
				meal = '\n일요일에 ' + content_name + ' 식당은\n운영하지 않습니다.'

		except Exception as e:
			meal = str(e) + '\n에러메세지가 보이면 관리자에게 알려주세요.'

		send_message = select_button.format(content_name, today_info) + meal

		return re_process(send_message)

	elif content_name == '향설2 생활관' :
		if user1.check(user_key) :
			return re_process(stop_message)

		try :
			with open('app/menu/SnowFlowerTwo.json', 'rb') as f :
				datas = json.load(f)

			if today_weekday >= 0 or today_weekday <= 4  :
				meal = str(datas.get('향2'))
				meal = char_replace(meal)

			else :
				meal = '\n주말에 ' + content_name + ' 식당은\n운영하지 않습니다.'

		except Exception as e:
			meal = str(e) + '\n에러메세지가 보이면 관리자에게 알려주세요.'

		send_message = select_button.format(content_name, today_info) + meal

		return re_process(send_message)

	elif content_name == '향설3 생활관' :
		if user2.check(user_key) :
			return re_process(stop_message)

		try :
			with open('app/menu/SnowFlowerThree.json', 'rb') as f :
				datas = json.load(f)

			if today_weekday == 0 :
				meal = str(datas.get('월'))
				meal = char_replace(meal)

			elif today_weekday == 1 :
				meal = str(datas.get('화'))
				meal = char_replace(meal)

			elif today_weekday == 2 :
				meal = str(datas.get('수'))
				meal = char_replace(meal)

			elif today_weekday == 3 :
				meal = str(datas.get('목'))
				meal = char_replace(meal)

			elif today_weekday == 4 :
				meal = str(datas.get('금'))
				meal = char_replace(meal)

			else :
				meal = str(datas.get('주말'))
				meal = char_replace(meal)

		except Exception as e:
			meal = str(e) + '\n에러메세지가 보이면 관리자에게 알려주세요.'

		send_message = select_button.format(content_name, today_info) + meal

		return re_process(send_message)

	elif content_name == '학생회관' :
		if user3.check(user_key) :
			return re_process(stop_message)

		try :
			with open('app/menu/StudentUnion.json', 'rb') as f :
				datas = json.load(f)

			if today_weekday == 0 :
				meal = str(datas.get('월'))
				meal = char_replace(meal)

			elif today_weekday == 1 :
				meal = str(datas.get('화'))
				meal = char_replace(meal)

			elif today_weekday == 2 :
				meal = str(datas.get('수'))
				meal = char_replace(meal)

			elif today_weekday == 3 :
				meal = str(datas.get('목'))
				meal = char_replace(meal)

			elif today_weekday == 4 :
				meal = str(datas.get('금'))
				meal = char_replace(meal)

			else :
				meal = '\n주말에 ' + content_name + ' 식당은\n운영하지 않습니다.'

		except Exception as e:
			meal = str(e) + '\n에러메세지가 보이면 관리자에게 알려주세요.'

		send_message = select_button.format(content_name, today_info) + meal

		return re_process(send_message)

	elif content_name == '교직원 식당' :
		if user4.check(user_key) :
			return re_process(stop_message)

		try :
			with open('app/menu/FacultyRestaurant.json', 'rb') as f :
				datas = json.load(f)

			if today_weekday == 0 :
				meal = str(datas.get('월'))
				meal = char_replace(meal)

			elif today_weekday == 1 :
				meal = str(datas.get('화'))
				meal = char_replace(meal)

			elif today_weekday == 2 :
				meal = str(datas.get('수'))
				meal = char_replace(meal)

			elif today_weekday == 3 :
				meal = str(datas.get('목'))
				meal = char_replace(meal)

			elif today_weekday == 4 :
				meal = str(datas.get('금'))
				meal = char_replace(meal)

			else :
				meal = '\n주말에 '+ content_name + '은\n운영하지 않습니다.'

		except Exception as e:
			meal = str(e) + '\n에러메세지가 보이면 관리자에게 알려주세요.'

		send_message = select_button.format(content_name, today_info) + meal

		return re_process(send_message)

	elif content_name == '종강' :
		if user5.check(user_key) :
			return re_process(stop_message)

		# 종강 일
		finish = datetime.datetime(2018, 6, 22)
		finish_info = finish.strftime('%Y년 %m월 %d일')
		date_dif = finish - today

		send_message = '[*] 선택한 버튼 : ' + content_name + '\n[*] 오늘 : ' + today_info + '\n[*] 종강 : ' + finish_info + '\n[*] 종강까지 %d일 남았습니다.' % date_dif.days

		return re_process(send_message)

	elif content_name == '학사 일정' :
		if user6.check(user_key) :
			return re_process(stop_message)

		# Location of parser.py
		BASE_DIR = os.path.dirname(os.path.abspath(__file__))

		# HTTP GET Request
		request =  requests.get('https://homepage.sch.ac.kr/sch/05/05010000.jsp')

		# GET HTML Source
		html = request.text

		# Use BeautifulSoup, From HTML Source to Python Object
		# First Parameter is HTML Source, Second Parameter is the parser to be used
		soup = BeautifulSoup(html, 'html.parser')

		# HTML element using CSS Selector
		schedules = soup.find_all('a', {'class' : 'schedule'})

		schedule_day = []
		schedule_list = []

		for schedule in schedules:
		    # 날짜 가져오기
		    schedule_day.append(schedule.text)
		    # 세부 내용 가져오기
		    schedule_list.append(schedule.get('title'))

		idx = 0

		today_info = today.strftime('%Y년 %m월')

		result_message = '의 학사일정\n'

		for schedule in schedule_day :
			schedule_message = '\n[*] ' + str(schedule) + '일 일정\n' + '[*] ' + schedule_list[idx]
			result_message = str(result_message) + schedule_message
			idx += 1

		# GET HTTP Header
		header = request.headers

		# GET HTTP Status ( 200 : normal )
		status = request.status_code

		# Check HTTP ( TRUE / FALSE )
		is_HTTP_OK = request.ok

		send_message = '[*] 선택한 버튼 : ' + content_name + '\n[*] ' + today_info + result_message

		return re_process(send_message)

	elif content_name == '개발자 정보' :
		if user7.check(user_key) :
			return re_process(stop_message)

		send_message = '[*] 선택한 버튼 : ' + content_name + '\n' + dev_info

		return re_process(send_message)

	else :
		if user8.check(user_key) :
			return re_process(stop_message)

		error_message = '[*] 심각한 오류입니다.\n[*] 개발자에게 알려주세요'

		if type_name == 'photo' :
			error_message = '[*] 사진을 보내도 기능이 없네요.\n[*] 버튼을 눌러주세요!'

		elif type_name == 'video' :
			error_message = '[*] 영상을 보내도 기능이 없네요.\n[*] 버튼을 눌러주세요!'

		elif type_name == 'audio' :
			error_message = '[*] 녹음 파일을 보내도 기능이 없네요.\n[*] 버튼을 눌러주세요!'

		return re_process(error_message)
