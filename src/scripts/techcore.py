import json
import random
import datetime
import requests
import urllib.parse
# methods
from src.scripts.techhttp import http_header_json_re
from src.scripts.techcookie import cookie_json_re
from src.scripts.techdns import dns_json_re
from src.scripts.techcontent import content_json_re
# core
from src.scripts.wwodd import tech_cats_update


tech_json      = json.load(open("src/tech_json.json", "r"))
tech_cats_json = json.load(open("src/tech_cats_json.json", "r"))


def ruser_agents_file():
	with open("src/ruser_agents.txt", "r") as file:
		return random.choice(file.read().split("\n"))


def tech_target_update(raw_tech_target_dict, rthhd, rtcd, rtdd, rtctd):
	for key, value in rthhd.items():
		raw_tech_target_dict[key].append(value)
	for key, value in rtcd.items():
		raw_tech_target_dict[key].append(value)
	for key, value in rtdd.items():
		raw_tech_target_dict[key].append(value)
	for key, value in rtctd.items():
		raw_tech_target_dict[key].append(value)
	return raw_tech_target_dict


def tech_core_lookup(source_data):
	raw_tech_target_dict = {"target": [], "datetime": [], "tech_cats": [], "tech_name": [], "tech_desc": [], "tech_web": [], "method": [], "fingerprint": []}
	raw_tech_target_dict["target"].append(urllib.parse.urlparse(source_data).netloc)
	raw_tech_target_dict["datetime"].append(datetime.datetime.now().strftime("%Y-%m-%d~%H:%M:%S"))
	# user agent / random
	ruser_agent = ruser_agents_file()
	# target source / req
	source_data_req = requests.get(source_data, headers={"user-agents": ruser_agent})
	# http header / method
	raw_tech_http_header_dict = http_header_json_re(source_data_req, tech_json)
	# cookie / method
	raw_tech_cookie_dict = cookie_json_re(source_data_req, tech_json)
	# dns record / method
	raw_tech_dns_dict = dns_json_re(source_data, tech_json)
	# content / menthod
	raw_tech_content_dict = content_json_re(source_data_req, tech_json)

	raw_tech_target_dict = tech_target_update(raw_tech_target_dict, raw_tech_http_header_dict, raw_tech_cookie_dict, raw_tech_dns_dict, raw_tech_content_dict)
	raw_tech_target_dict = tech_cats_update(raw_tech_target_dict, tech_cats_json)
	return raw_tech_target_dict