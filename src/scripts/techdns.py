import re
import dns.resolver
import urllib.parse


def dns_target(source_data):
	dns_records = ["NS", "SOA", "MX", "CNAME"]
	dns_dict    = {"dns_name": [], "dns_value": []}
	for dns_record in dns_records:
		try:
			source_data = urllib.parse.urlparse(source_data).netloc
			answers     = dns.resolver.resolve(source_data, dns_record)
			for rdata in answers:
				dns_dict["dns_name"].append(dns_record)
				dns_dict["dns_value"].append(str(rdata))
		except Exception as error: pass
	return dns_dict


def dns_json_re(source_data, tech_json):
	raw_tech_dns_dict = {"tech_cats": [], "tech_name": [], "tech_desc": [], "tech_web": [], "method": [], "fingerprint": []}
	dns_dict          = dns_target(source_data)
	for tech_name in tech_json:
		if "dns" in tech_json[tech_name]:
			for dns_json_name in tech_json[tech_name]["dns"]:
				dns_json_value = tech_json[tech_name]["dns"][dns_json_name]
				for dns_name, dns_value in zip(dns_dict["dns_name"], dns_dict["dns_value"]):
					if dns_json_name.lower() == dns_name.lower() and re.findall(dns_json_value, dns_value, re.IGNORECASE):
						if tech_name not in raw_tech_dns_dict["tech_name"]:
							raw_tech_dns_dict["tech_cats"].append(tech_json[tech_name]["cats"])
							raw_tech_dns_dict["tech_name"].append(tech_name)
							raw_tech_dns_dict["tech_desc"].append(tech_json[tech_name]["description"])
							raw_tech_dns_dict["tech_web"].append(tech_json[tech_name]["website"])
							raw_tech_dns_dict["method"].append("dns fingerprint")
							raw_tech_dns_dict["fingerprint"].append(f"{dns_name}: {dns_value}")
	return raw_tech_dns_dict