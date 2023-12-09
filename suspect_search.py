import requests, json
import sys, os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "D:/THE SNAKE")))

from Config import *
from db_manager import *

def suspect_search(query):
	user = random.choice([
		["sa1001", "7000"], 
		["sa1002", "1458"], 
		["sa1003", "1458"]
	])


	url = "https://tcsdscan.ies2k.com"

	payload = {
		"username": user[0], 
		"password": user[1], 
		"next": ""
	}

	with requests.Session() as session:
		s = session.post(url + "/post_login", data = payload)
		cookie = session.cookies.get_dict()
		cookie = "arrest_warrant={}".format(cookie["arrest_warrant"])
		
		headers = {"Cookie": cookie}

		params = {
			"name": "",
			"cid": "",
			"startdate": "2020-01-01 00:00:01",
			"enddate": "2023-12-30 23:59:59",
			"project_id": "0",
			"start": "1",
			"end": "99"
		}
		
		if query.isdigit() and len(query) == 13:
			params["cid"] = query
		else:
			params["name"] = query

		s = session.get(url + "/api_universal", headers = headers, params = params)
		if s.status_code == 200:
			data = s.json()
			report_data = "ผลการค้นหา : {}\n\n".format(query)

			scanin_data = "ประวัติการเข้างาน : ไม่พบข้อมูล\n\n"
			if len(data["scanin"]) != 0:
				scanin_data = "ประวัติการเข้างาน : {}\n\n".format(len(data["scanin"]))
				for scanin in data["scanin"]:
					print(scanin)

			suspect_found_data = "ข้อมูลบุคคลเฝ้าระวัง : ไม่พบประวัติการเข้างาน\n\n"
			if len(data["suspect_found"]) != 0:
				print(data["suspect_found"])

			suspect_data = "บุคคลเฝ้าระวัง : ไม่พบข้อมูล"
			if len(data["suspect"]) != 0:
				with sqlite_manager(sqlite_path["local_db"]) as sqlite_db:
					count = 1

					suspect_data = "บุคคลเฝ้าระวัง : พบข้อมูล {} รายการ\n\n".format(len(data["suspect"]))
					#image_url = 'https://tcsdscan.ies2k.com/static/picture_suspect_found/{}'.format(data['scanin'][0]['picture_file_name']) 
			
					for suspect in data['suspect']:
						suspect_data += "ลำดับ : {}\n".format(count)
						suspect_data += "เลขประจำตัวประชาชน : {}\n".format(suspect["cid"])
						suspect_data += "ชื่อ - สกุล : {}\n".format(suspect["suspect_name"])
						suspect_data += "ประเภทบุคคล : {}\n".format(suspect["aw_desc"])
						suspect_data += "ประเภทเฝ้าระวัง : {}\n".format(suspect["typex"])
						suspect_data += "รายละเอียด : {}\n".format(suspect["suspect_desc"])
						suspect_data += "หน่วยงานที่บันทึก : {}\n".format(suspect["sourcex"])
						suspect_data += "ผู้บันทึก : {}\n\n".format(suspect["record_officer"])
						count += 1
		
						insert_data = (
							suspect["id"], suspect["cid"], suspect["suspect_name"], 
							suspect["suspect_desc"], suspect["aw_desc"], suspect["typex"], 
							suspect["record_officer"], suspect["sourcex"]
						)

						if suspect["record_officer"] != "TCSD System":	
							if sqlite_db.fetchone("SELECT id FROM db_suspect WHERE id = ?", (insert_data[0],)) is None:
								sqlite_insert_string = "INSERT INTO db_suspect (id, cid, suspect_name, suspect_desc, aw_desc, record_officer, sourcex, typex) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
								sqlite_db.insert(sqlite_insert_string, insert_data)

		report_data += scanin_data + suspect_data
		print(report_data)



suspect_search('ภัทร อุ่นเอิบ')
