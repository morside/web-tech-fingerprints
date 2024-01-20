

def formatted_data_dict(raw_tech_target_dict):
	for key in raw_tech_target_dict:
		for i, value in enumerate(raw_tech_target_dict[key]):
			if not value:
				raw_tech_target_dict[key][i] = None
			if value:
				raw_tech_target_dict[key][i] = value
	return raw_tech_target_dict


def tech_cats_update(raw_tech_target_dict, tech_cats_json):
	for i, tech_cats in enumerate(raw_tech_target_dict["tech_cats"]):
		for j, tech_cat in enumerate(tech_cats):
			for k, count_cats in enumerate(tech_cat):
				count_cats = str(count_cats)
				if count_cats in tech_cats_json:
					if int(count_cats) > 1:
						raw_tech_target_dict["tech_cats"][i][j][k] = tech_cats_json[count_cats]["name"]
					if int(count_cats) == 1:
						raw_tech_target_dict["tech_cats"][i][j][0] = tech_cats_json[count_cats]["name"]
	return raw_tech_target_dict