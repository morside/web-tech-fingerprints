

def history_read(method):
	if method == "source_data":
		with open("src/history.txt", "r") as file:
			return file.read()
	elif method == "lookup_data":
		with open("src/lookup_history.txt", "r") as file:
			return file.read()


def history_remove(method):
	line_list = []
	if method == "source_data":
		with open("src/history.txt", "r") as file:
			for line in file.readlines():
				line_list.append(line)
		line_list.remove(line_list[0])
		with open("src/history.txt", "w") as file:
			for line in line_list:
				file.writelines(line)
	elif method == "lookup_data":
		with open("src/lookup_history.txt", "r") as file:
			for line in file.readlines():
				line_list.append(line)
		line_list.remove(line_list[0])
		with open("src/lookup_history.txt", "w") as file:
			for line in line_list:
				file.writelines(line)


def history_clear(method):
	if method == "source_data":
		with open("src/history.txt", "w") as file:
			file.write("")
	elif method == "lookup_data":
		with open("src/lookup_history.txt", "w") as file:
			file.write("")


def history_write(data, method):
	if method == "source_data":
		with open("src/history.txt", "a") as file:
			file.writelines(f"{data}\n")
	elif method == "lookup_data":
		with open("src/lookup_history.txt", "a") as file:
			file.writelines(f"{data}\n")

