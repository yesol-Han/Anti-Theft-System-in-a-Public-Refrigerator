import sys
import time
from bluetooth import *
import threading
import dbModule
import mobiusModule
from time import sleep

import smtplib
from email.message import EmailMessage

### BLE_Setting ###
#bd_addr="98:D3:31:FC:81:DA"    #hc-05 3
bd_addr = "98:D3:31:FD:52:6C"    #hc-05 2
port=1
sock=BluetoothSocket(RFCOMM)
sock.connect((bd_addr, port))

###DB Setting ###
db_class=dbModule.Database()

### mobius_Setting  ###
mobius_class = mobiusModule.mobius()
url = mobius_class.url

### mail_Setting ###
# 보내는 메일 서버 
SMTP_SERVER = 'smtp.gmail.com' 
SMTP_PORT = 587
# 송신자, 수신자, 비밀번호 
sender = 'hys9428@gmail.com' 
recipient = 'yesol@sch.ac.kr' 
password = 'cultqninuqzshpju'
# 메시지 생성하기 
msg = EmailMessage() 
msg['Subject'] = '보안 경고' 
msg['From'] = sender 
msg['To'] = recipient 
text = '도난상황이 의심됩니다. 6층 냉장고를 확인해주세요' 
msg.set_content(text)

sock.send('Hello! HC-05/')
print ('Finished')
data=""
first = True

url_get_cin1 = url + "control/security/la"

def watch():
	#여기에 감시모드 적용
	while True:
		sleep(2)
		if (first == False):
			print('herrrrrrrr')
			status, response_data = mobius_class.response_get_cin(url_get_cin1, 'C')
			if response_data['m2m:cin']['con'][0] == "1":	# 도난상황
				db_class.mail += 1
				print('ddddd theft mode checking dddddd')
				if (db_class.mail == 1):
					# SMTP 객체 생성 후, 메시지 전송 
					sock.send('Warning')
					s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT) 
					s.ehlo() 
					s.starttls() 
					s.login(sender, password) 
					s.send_message(msg) 
					s.quit()
				db_class.set_theft(True)
				theft = True

			url_get_cin2 = url + userID + '/foodRFID/la'
			url_delete_cin = url + userID + '/foodRFID/la'
			print(url_get_cin2)
			status, response_data = mobius_class.response_get_cin(url_get_cin2, userPW)
			print(str(status) + str('11111111 server order - status check 11111111'))
			if status == 200:
				try:
					data = response_data['m2m:cin']['con']
					print(str(data) + str('222222222 server order - status check 222222222'))
					if data[0] == '1':
						db_class.insert_db(data[2:])
					elif data[0] == '0':
						db_class.delete_db(data[2:])
					mobius_class.response_delete_cin(url_delete_cin, userPW)
				except:
					print("there's no cin")
		

t1 = threading.Thread(target=watch)
t1.start()

print('start')

while True:
	recv = sock.recv(1)	#중간에 자르기 어려워 차라리 하나씩 받음

	if recv.decode() != '/':
		data += str(recv.decode())

	elif len(data) > 0:		#여기서부터 작업, 진짜 데이터는 여기임

		if (db_class.get_theft() == False):
			print("????? start ????")
			if data[0] == 'I':	#remote control
				#get cnt / ID 비교해서 가져오기
				url_get_cnt1 = url + "PIN/" + '1535_34'	#data[1:] = id,pw
				user = '1535_34' #userID parsing		data[1:14]
				userID = '1535'		#data[1:9]
				userPW = '34'
				#print (url_get_cnt, user)
				status, response_data = mobius_class.response_get_cnt(url_get_cnt1, 'P', 'application/json')
				
				try:	#답결과에 따라 open/close
					if status == 200:
						first = False
						sock.send('open/')
				except:
					sock.send('again/')
					print ('again')

			elif data[0] == 'R':	#rfid
				print ('R')
				uid = data[1:]
				if(db_class.check_uid(uid)):	#DB 목록에 있으면, mobius에 서버와 매칭해보기
					url_delete_cnt = url + userID + "/foodRFID/" + str(uid)
					print('yyyyyyyyyy delete RFID yyyyyyyyyyyyyy' + url_delete_cnt)
					status, response_data = mobius_class.response_delete_cnt(url_delete_cnt, userPW, 'application/json')
					print('jjjjjjjjjjjjjjjj delete status code is ' + str(status))
					try:
						if status == 200:	#삭제가 되면
							url_post_cin3 = url + 'control/RFID'
							mobius_class.response_post_cin(url_post_cin3, '0_' + uid + '_' + time.strftime('%Y.%m.%d.%H:%M:%S', time.localtime(time.time())) + '_' + userID, 'C')

							db_class.delete_db(uid)
							print("deleteDB")
					except:
						sock.send('Another Tag!!/')
						print('Another Tag!!')	#자기 것이 아님
				else:
					url_post_cnt1 = url + userID + "/foodRFID"
					mobius_class.response_post_cnt(url_post_cnt1, uid, userPW)

					url_post_cin3 = url + 'control/RFID'
					mobius_class.response_post_cin(url_post_cin3, '1_' + uid + '_' + time.strftime('%Y.%m.%d.%H:%M:%S', time.localtime(time.time())) + '_' + userID, 'C')
					db_class.insert_db(uid)
					print("insertDB")	#내꺼 등록

			elif data[0] == 'O':  #open=1, close=0
				url_post_cin1 = url + userID + "/opentime"
				url_post_cin2 = url + "control/door"

				open = data[1]  #open parsing

				mobius_class.response_post_cin(url_post_cin2, str(open) + '_' + user + '_' + time.strftime('%Y.%m.%d.%H:%M:%S', time.localtime(time.time())), 'C')
				
				if(open=="1"):	#문이 열렸다
					print("문이 열렸다")
				else:
					mobius_class.response_post_cin(url_post_cin1, time.strftime('%Y.%m.%d.%H:%M:%S', time.localtime(time.time())), userPW)
					user = ""
					userID = ""
					print("문이 닫혔다")

				print (userID, 'open')

			elif data[0] == 'N':	#none
				print (data)

			else:	#test부분
				print ('open')
				sock.send('open/')

			print ('Receive', data)
			data = ""

		else:
			if data[0] == 'I':	#remote control
				print("eeeeeeeeeeeeeeee theft mode eeeeeeeeeeee")
				print(data)
				if (data[1:] == '__00__'):
					url_post_cin4 = url + "control/security"
					mobius_class.response_post_cin(url_post_cin4, '0,0,0', 'C')
					db_class.set_theft(False)
					db_class.mail=0
					sock.send('ok')
			data = ""


sock.close()
