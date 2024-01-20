import re


def cookie_target(source_data_req):
	cookie_dict = {"cookie_name": []}
	cookie_req  = source_data_req.cookies
	for cookie_name in cookie_req:
		cookie_dict["cookie_name"].append(cookie_name.name)
	return cookie_dict


def cookie_json_re(source_data_req, tech_json):
	raw_tech_cookie_dict = {"tech_cats": [], "tech_name": [], "tech_desc": [], "tech_web": [], "method": [], "fingerprint": []}
	cookie_dict          = cookie_target(source_data_req)
	for tech_name in tech_json:
		if "cookies" in tech_json[tech_name]:
			for cookie_json_name in tech_json[tech_name]["cookies"]:
				for cookie_name in cookie_dict["cookie_name"]:
					if cookie_json_name.lower() == cookie_name.lower():
						if tech_name not in raw_tech_cookie_dict["tech_name"]:
							raw_tech_cookie_dict["tech_cats"].append(tech_json[tech_name]["cats"])
							raw_tech_cookie_dict["tech_name"].append(tech_name)
							raw_tech_cookie_dict["tech_desc"].append(tech_json[tech_name]["description"])
							raw_tech_cookie_dict["tech_web"].append(tech_json[tech_name]["website"])
							raw_tech_cookie_dict["method"].append("cookie fingerprint")
							raw_tech_cookie_dict["fingerprint"].append(cookie_name)
	return raw_tech_cookie_dict