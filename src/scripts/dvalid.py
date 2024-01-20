import requests


def user_source_data_valid(source_data):
	user_source_data = source_data
	if user_source_data == "" or not user_source_data.startswith(("http://", "https://")):
		return 1
	# user source data request
	try: requests.get(source_data, timeout=(5, 10))
	except Exception as error: return 1
	return 0