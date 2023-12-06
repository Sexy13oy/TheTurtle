from oauth2client.service_account import ServiceAccountCredentials
import gspread
from urllib.parse import unquote
import requests, json
import time

def social_search(query):
	url = "https://google.serper.dev/search"

	payload = {"q": query}

	headers = {
	  'X-API-KEY': 'a5dcefdebefd6a8c08fc8d3cb8c66b689b1e97f9',
	  'Content-Type': 'application/json'
	}

	results = {
		"facebook": ["-", "-"], 
		"instagram": ["-", "-"], 
		"twitter": ["-", "-"], 
		"youtube": ["-", "-"]
	}

	if query not in [None, "", "-", "- -"]:
		r = requests.post(url, headers = headers, data = json.dumps(payload))
		if r.status_code == 200:
			data = json.loads(r.text)
			for d in data["organic"]:
				title = d["title"]
				link = unquote(d["link"])	

				if query.lower() in title.lower() and "facebook" in link:
					results["facebook"] = [title, link]
				elif query.lower() in title.lower() and "instagram" in link:
					results["instagram"] = [title, link]
				elif query.lower() in title.lower() and "twitter" in link:
					results["twitter"] = [title, link]
				elif query.lower() in title.lower() and "youtube" in link:
					results["youtube"] = [title, link]

	return results

scope = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("D:/THE SNAKE/credentials.json", scope)
client = gspread.authorize(credentials)
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1bRcJxr-YsptFGL4KJG1n8gMqLFO4wh2Ts1CBy79_E7M/edit#gid=0")
sheet = spreadsheet.worksheet("ตรวจประวัติ")
src_data = sheet.get_all_values()[1:]
end_row = int(2 + len(src_data) - 1)

# Define the data to update 
facebook_name, facebook_url = [], []
instagram_name, instagram_url = [], [] 
twitter_name, twitter_url = [], [] 
youtube_name, youtube_url = [], [] 

results = {
	"facebook": ["-", "-"], 
	"instagram": ["-", "-"], 
	"twitter": ["-", "-"], 
	"youtube": ["-", "-"]
}

for src in src_data:
	th_fullname = src[1]
	en_fullname = src[2]

	print("[x] ลำดับ :", src[0])
	print("[x] ชื่อ - สกุล (TH) :", th_fullname)
	print("[x] ชื่อ - สกุล (EN) :", en_fullname)
	print("=" * 25)

	for query in [th_fullname, en_fullname]:
		data = social_search(query)
		for key in ["facebook", "instagram", "twitter", "youtube"]:
			if data[key][0] != "-":
				results[key] = data[key]

	facebook_name.append([results["facebook"][0]])
	facebook_url.append([results["facebook"][1]])
	instagram_name.append([results["instagram"][0]])
	instagram_url.append([results["instagram"][1]])
	twitter_name.append([results["twitter"][0]])
	twitter_url.append([results["twitter"][1]])
	youtube_name.append([results["youtube"][0]])
	youtube_url.append([results["youtube"][1]])

	print("[=>] Facebook Name :", results["facebook"][0])
	print("[=>] Facebook URL :", results["facebook"][1])
	print("[=>] Instagram Name :", results["instagram"][0])
	print("[=>] Instagram URL :", results["instagram"][1])
	print("[=>] Twitter Name :", results["twitter"][0])
	print("[=>] Twitter URL :", results["twitter"][1])
	print("[=>] Youtube Name :", results["youtube"][0])
	print("[=>] Youtube URL :", results["youtube"][1])
	print("-" * 25)
	
sheet.update(f"D2:D{end_row}", facebook_name)
sheet.update(f"E2:E{end_row}", facebook_url)
sheet.update(f"F2:F{end_row}", instagram_name)
sheet.update(f"G2:G{end_row}", instagram_url)
sheet.update(f"H2:H{end_row}", twitter_name)
sheet.update(f"I2:I{end_row}", twitter_url)
sheet.update(f"J2:J{end_row}", youtube_name)
sheet.update(f"K2:K{end_row}", youtube_url)









