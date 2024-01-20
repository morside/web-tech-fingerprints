import re


def http_header_target(source_data_req):
	http_header_dict = {"http_header_name": [], "http_header_value": []}
	http_header_req  = source_data_req.headers
	for http_header_name in http_header_req:
		http_header_dict["http_header_name"].append(http_header_name)
		http_header_dict["http_header_value"].append(http_header_req[http_header_name])
	return http_header_dict


def http_header_json_re(source_data_req, tech_json):
	raw_tech_http_header_dict = {"tech_cats": [], "tech_name": [], "tech_desc": [], "tech_web": [], "method": [], "fingerprint": []}
	http_header_dict          = http_header_target(source_data_req)
	for tech_name in tech_json:
		if "headers" in tech_json[tech_name]:
			for http_header_json_name in tech_json[tech_name]["headers"]:
				http_header_json_value = tech_json[tech_name]["headers"][http_header_json_name]
				for http_header_name, http_header_value in zip(http_header_dict["http_header_name"], http_header_dict["http_header_value"]):
					if http_header_json_name.lower() == http_header_name.lower() and re.findall(http_header_json_value, http_header_value, re.IGNORECASE):
						if tech_name not in raw_tech_http_header_dict["tech_name"]:
							raw_tech_http_header_dict["tech_cats"].append(tech_json[tech_name]["cats"])
							raw_tech_http_header_dict["tech_name"].append(tech_name)
							raw_tech_http_header_dict["tech_desc"].append(tech_json[tech_name]["description"])
							raw_tech_http_header_dict["tech_web"].append(tech_json[tech_name]["website"])
							raw_tech_http_header_dict["method"].append("hheader fingerprint")
							raw_tech_http_header_dict["fingerprint"].append(f"{http_header_name}: {http_header_value}")
	return raw_tech_http_header_dict