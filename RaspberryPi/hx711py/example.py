#! /usr/bin/python2

import time
import sys
import requests
import threading
import json
from datetime import datetime
from pytz import timezone

door = 0
user = ""
password = 0
weight = 0
RFID = []
now = ""
ok ='1'
check = [0,0,0]
opentime = '0'
def httprequest(second = 3.0):
	global door, user, password
	
	url = "http://114.71.221.47:7579/Mobius/control/door/la"

	payload = {}
	headers = {
  	'Accept': 'application/json',
  	'X-M2M-RI': '12345',
  	'X-M2M-Origin': 'C'
	}

	response = requests.request("GET", url, headers=headers, data = payload)
#	print(response.text.encode('utf8'))	
	door  = response.text.encode("utf8")
	door = json.loads(door)
	door = door["m2m:cin"]["con"]
	door = door.split('_')
	if(door[0] == "1"):
		print("door:{0} user: {1} passwrod: {2}".format(door[0], door[1], door[2]))
		user = door[1]
		password = door[2]
	door = door[0]
	threading.Timer(second, httprequest, [second]).start()	

def security():
	global RFID
	url = "http://114.71.221.47:7579/Mobius/control/RFID?rcn=4&ty=4&cra=" + now
	print(now)
	payload = {}
	headers = {
  	'Accept': 'application/json',
  	'X-M2M-RI': '12345',
  	'X-M2M-Origin': 'C',
	}
	response = requests.request("GET", url, headers=headers, data = payload)
#	print(response.text.encode('utf8'))
	list  = response.text.encode("utf8")
	list = json.loads(list)
	try: 
		list = list["m2m:rsp"]["m2m:cin"]
		list = list[0]["con"]
		list = list.split('_')
		RFID = list
		print("RFID:{0}".format(RFID[0]))
	except:
		RFID = ["3","0","0"]
	
	return RFID

def weghithttp():
	global weight
	url = "http://114.71.221.47:7579/Mobius/control/weight/la"
	payload = {}
	headers = {
        'Accept': 'application/json',
        'X-M2M-RI': '12345',
        'X-M2M-Origin': 'C'
	}
	response = requests.request("GET", url, headers=headers, data = payload)
	weight = json.loads(response.text.encode('utf8'))
	weight = weight["m2m:cin"]["con"]
	print("weght:{0}".format(weight[0]))
	return float(weight)

def errorhttp():
	url = "http://114.71.221.47:7579/Mobius/control/security"

	payload = "{\n    \"m2m:cin\": {\n        \"con\": \"1," +user+ "," + password +"\"\n    }\n}"
	headers = {
  	'Accept': 'application/json',
  	'X-M2M-RI': '12345',
  	'X-M2M-Origin': 'C',
  	'Content-Type': 'application/vnd.onem2m-res+json; ty=4'
	}
	response = requests.request("POST", url, headers=headers, data = payload)
#	print(response.text.encode('utf8'))
	
	url = "http://114.71.221.47:7579/Mobius/" + user + "/security"

	payload = "{\n    \"m2m:cin\": {\n        \"con\": \"1\"\n    }\n}"
	headers = {
  	'Accept': 'application/json',
  	'X-M2M-RI': '12345',
  	'X-M2M-Origin': str(password),
  	'Content-Type': 'application/vnd.onem2m-res+json; ty=4'
	}

	response = requests.request("POST", url, headers=headers, data = payload)
#	print(response.text.encode('utf8'))
	
	

def weightchange():
	global weight
	print(weight)
	url = "http://114.71.221.47:7579/Mobius/control/weight"

	payload = "{\n    \"m2m:cin\": {\n        \"con\": \"" + str(weight) +"\"\n    }\n}"
	headers = {
  	'Accept': 'application/json',
  	'X-M2M-RI': '12345',
  	'X-M2M-Origin': 'C',
  	'Content-Type': 'application/vnd.onem2m-res+json; ty=4'
	}

	response = requests.request("POST", url, headers=headers, data = payload)

#	print(response.text.encode('utf8'))
	
def plushttp(weight, time, RFID):
	url = "http://114.71.221.47:7579/Mobius/" +user+ "/food"
	payload = "{\n  \"m2m:cnt\": {\n    \"rn\": \"" + str(RFID) +"\",\n    \"lbl\": [\"" + str(time) +"\"],\n    \"mbs\": "+ str(weight) + "\n  }\n}"
	headers = {
  	'Accept': 'application/json',
  	'X-M2M-RI': '12345',
  	'X-M2M-Origin': str(password),
  	'Content-Type': 'application/vnd.onem2m-res+json; ty=3'
	}

	response = requests.request("POST", url, headers=headers, data = payload)
	
	url = "http://114.71.221.47:7579/Mobius/" + user +"/lastRFID"

	payload = "{\n  \"m2m:cnt\": {\n    \"rn\": \"" + str(RFID) + "\",\n    \"lbl\": [\"" + str(time) + "\"],\n    \"mbs\": " + str(weight) + "\n  }\n}"
	headers = {
  	'Accept': 'application/json',
  	'X-M2M-RI': '12345',
  	'X-M2M-Origin': str(password),
  	'Content-Type': 'application/vnd.onem2m-res+json; ty=3'
	}

	response = requests.request("POST", url, headers=headers, data = payload)
	
	print("plusehttp")

	
def search(RFID):
	global check
	url = "http://114.71.221.47:7579/Mobius/" + user + "/lastRFID/" + str(RFID)

	payload = {}
	headers = {
  	'Accept': 'application/json',
  	'X-M2M-RI': '12345',
  	'X-M2M-Origin': str(password)
	}

	response = requests.request("GET", url, headers=headers, data = payload)

	
	respon  = response.text.encode("utf8")
	respon = json.loads(respon)

	try:
                check[0] = "0"
                check[1] = respon["m2m:cnt"]["lbl"][0]
                check[2] = respon["m2m:cnt"]["mbs"]
                print("RFID:{0}".format(check[0]))
	except:
                check[0] = "1"

	print("search")

	return check

def update(weight, time, RFID):

	url = "http://114.71.221.47:7579/Mobius/" +user+ "/food"
        payload = "{\n  \"m2m:cnt\": {\n    \"rn\": \"" + str(RFID) +"\",\n    \"lbl\": [\"" + str(time) +"\"],\n    \"mbs\": "+ str(weight) + "\n  }\n}"
        headers = {
        'Accept': 'application/json',
        'X-M2M-RI': '12345',
        'X-M2M-Origin': str(password),
        'Content-Type': 'application/vnd.onem2m-res+json; ty=3'
        }

        response = requests.request("POST", url, headers=headers, data = payload)


	url = "http://114.71.221.47:7579/Mobius/" + user + "/lastRFID/" + str(RFID)

	payload = "{\n  \"m2m:cnt\": {\n    \"lbl\": [\"" + str(time) + "\"],\n    \"mbs\": " +  str(weight) + "\n  }\n}"
	headers = {
  	'Accept': 'application/json',
  	'X-M2M-RI': '12345',
  	'X-M2M-Origin': str(password),
  	'Content-Type': 'application/vnd.onem2m-res+json'
	}

	response = requests.request("PUT", url, headers=headers, data = payload)

	print(response.text.encode('utf8'))
	
	

def nohttp(RFID, RE):
	url = "http://114.71.221.47:7579/Mobius/" + user + "/foodRFID"

	payload = "{\n    \"m2m:cin\": {\n        \"con\": \"" + str(RE)+ "_" + str(RFID)+ "\"\n    }\n}"
	headers = {
  	'Accept': 'application/json',
  	'X-M2M-RI': '12345',
  	'X-M2M-Origin': str(password),
  	'Content-Type': 'application/vnd.onem2m-res+json; ty=4'
	}

	response = requests.request("POST", url, headers=headers, data = payload)
	print("cansel")

	print(response.text.encode('utf8'))
	

def delhttp(RFID):
	url = "http://114.71.221.47:7579/Mobius/" + user + "/food/" + str(RFID)

	payload  = {}
	headers = {
  	'Accept': 'application/json',
  	'locale': 'ko',
  	'X-M2M-RI': '12345',
  	'X-M2M-Origin': str(password)
	}

	response = requests.request("DELETE", url, headers=headers, data = payload)

#	print(response.text.encode('utf8'))
	

	
EMULATE_HX711=False

referenceUnit = -441

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()

hx = HX711(5, 6)

# I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
# Still need to figure out why does it change.
# If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
# There is some code below to debug and log the order of the bits and the bytes.
# The first parameter is the order in which the bytes are used to build the "long" value.
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
hx.set_reading_format("MSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
#hx.set_reference_unit(113)
hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

print("Tare done! Add weight now...")

# to use both channels, you'll need to tare them both
#hx.tare_A()
#hx.tare_B()

httprequest(2.0)
while True:
    try:
	print("door close")
        # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
        # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
        # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment these three lines to see what it prints.
        
        # np_arr8_string = hx.get_np_arr8_string()
        # binary_string = hx.get_binary_string()
        # print binary_string + " " + np_arr8_string
        
        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
	if door == "1":
		opentime = time.time()
		print("door open") 
		totalwieght = weghithttp()	
      		val = hx.get_weight(5)
#                print("total:{0} nowweight: {1}".format(totalwieght, val))
		if val > -100:
#			print("change weight : {0}".format(val))
			nownow = datetime.now(timezone('UTC'))
			now= nownow.strftime("%Y%m%dT%H%M%S")
			while True:
				val = hx.get_weight(5)
				totalwieght = weghithttp()
				RFID = security()
				nowRFID = RFID[1]
				timeRFID= RFID[2]
				print(totalwieght, val)
				print(time.time() - opentime)
				if door == '1' and RFID[0] == '1':
					print("plusfood")
				     	while True:
						val = hx.get_weight(5)
						RFID = security()
						print(door)
						print(totalwieght, val)
					#	httprequest()
						if door == '0' or RFID[0] == '0':
							print("close or RFID0")
							print(totalwieght, val)
							if val > totalwieght + 5:
								search(nowRFID)
								print(check[0])
								if check[0] == '1':
									w = val - totalwieght
									plushttp(w,timeRFID,nowRFID)
									weight = val
									weightchange()
									print("pluscomplete")
									break
								elif check[0] == '0':
									w = val  - totalwieght
									update(w, check[1], nowRFID)
									weight = val
									weightchange()
									print("updatecomplete")
									break
							else:
								nohttp(nowRFID, "1")
								print("reset")
								break

				elif door == '1' and RFID[0] == '0':
					while True:
						val = hx.get_weight(5)
                                                RFID = security()
						print(totalwieght, val)
						if door == '0' or RFID[0] == '1':
							print(totalwieght, val)
							if val < totalwieght - 5:
								search(nowRFID)
								print(check[2])
								w = totalwieght - val
								print(w)
								if check[2] - 100 < w < check[2] + 100:
									delhttp(nowRFID)
									weight = val
									weightchange()
									print("delete food")
									break
								else:
									ok = '0'
									print("not your food")
									break
							else:
								nohttp(nowRFID, "0")
								print("reset")
								break			
				elif door == '0' and (float(totalwieght) - 10 < val < float(totalwieght) + 10) and ok=='1' : 
					RFID[0] = "3"
					ok = '1'
					print("success")			
					break
				elif door == '0' and (ok == '0' or (float(totalwieght) - 10 >  val) or (val > float(totalwieght) + 10)):
					errorhttp()
                                        RFID[0] = '3'
                                        print("danger")
                                        break
				elif time.time() - opentime > 600:
					errorhttp()
					RFID[0] = '3'
					print("timeout")
					break
        	

        # To get weight from both channels (if you have load cells hooked up 
        # to both channel A and B), do something like this
        #val_A = hx.get_weight_A(5)
        #val_B = hx.get_weight_B(5)
        #print "A: %s  B: %s" % ( val_A, val_B )

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()

