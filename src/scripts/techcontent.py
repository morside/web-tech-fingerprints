import re


def content_target(source_data_req):
	content_dict = {"content": [], "line_code": []}
	content_req  = source_data_req.text.split()
	for line_code, content in enumerate(content_req):
		content_dict["content"].append(content)
		content_dict["line_code"].append(line_code)
	return content_dict


def content_json_re(source_data_req, tech_json):
	raw_tech_content_dict = {"tech_cats": [], "tech_name": [], "tech_desc": [], "tech_web": [], "method": [], "fingerprint": []}
	content_dict          = content_target(source_data_req)
	for tech_name in tech_json:
		if "js" in tech_json[tech_name]:
			for js_json_name in tech_json[tech_name]["js"]:
				js_json_value = tech_json[tech_name]["js"][js_json_name]
				for line_code, content in zip(content_dict["line_code"], content_dict["content"]):
					if re.findall(js_json_name, content) and re.findall(js_json_value, content):
						if tech_name not in raw_tech_content_dict["tech_name"]:
							raw_tech_content_dict["tech_cats"].append(tech_json[tech_name]["cats"])
							raw_tech_content_dict["tech_name"].append(tech_name)
							raw_tech_content_dict["tech_desc"].append(tech_json[tech_name]["description"])
							raw_tech_content_dict["tech_web"].append(tech_json[tech_name]["website"])
							raw_tech_content_dict["method"].append("js fingerprint")
							raw_tech_content_dict["fingerprint"].append(f"line {line_code}: " +  "".join(set(re.findall(js_json_name, content))))
		if "scriptSrc" in tech_json[tech_name]:
			for script_json_name in tech_json[tech_name]["scriptSrc"]:
				for line_code, content in zip(content_dict["line_code"], content_dict["content"]):
					if re.findall(script_json_name, content, re.IGNORECASE):
						if tech_name not in raw_tech_content_dict["tech_name"]:
							raw_tech_content_dict["tech_cats"].append(tech_json[tech_name]["cats"])
							raw_tech_content_dict["tech_name"].append(tech_name)
							raw_tech_content_dict["tech_desc"].append(tech_json[tech_name]["description"])
							raw_tech_content_dict["tech_web"].append(tech_json[tech_name]["website"])
							raw_tech_content_dict["method"].append("script fingerprint")
							raw_tech_content_dict["fingerprint"].append(f"line {line_code}: " +  "".join(set(re.findall(script_json_name, content, re.IGNORECASE))))
		if "meta" in tech_json[tech_name]:
			for meta_json_name in tech_json[tech_name]["meta"]:
				meta_json_value = tech_json[tech_name]["meta"][meta_json_name]
				for line_code, content in zip(content_dict["line_code"], content_dict["content"]):
					if re.findall(meta_json_name, content, re.IGNORECASE) and re.findall(meta_json_value, content, re.IGNORECASE):
						if tech_name not in raw_tech_content_dict["tech_name"]:
							raw_tech_content_dict["tech_cats"].append(tech_json[tech_name]["cats"])
							raw_tech_content_dict["tech_name"].append(tech_name)
							raw_tech_content_dict["tech_desc"].append(tech_json[tech_name]["description"])
							raw_tech_content_dict["tech_web"].append(tech_json[tech_name]["website"])
							raw_tech_content_dict["method"].append("meta fingerprint")
							raw_tech_content_dict["fingerprint"].append(f"line {line_code}: " +  "".join(set(re.findall(meta_json_name, content, re.IGNORECASE))))
	return raw_tech_content_dict