import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import defaultdict
import json


def display_json(data, path):
	out_file = open(path, "w")
	json.dump(data, out_file,indent=4)
	# print('File Written, File Name is:', file_name + '.txt\n', sep=' ')

# def extract_tagnames(extract):

# 	tags_dict = defaultdict(list)
# 	# tags_dict = dict()
# 	name = None
# 	name_list = list()
# 	tag_list = list()

# 	for tags in extract.split(','):
# 		if len(tags.split(' ')) == 2:
# 			name = str()
# 			tag, name  = tuple(tags.split(' '))
# 		elif len(tags.split(' ')) == 1:
# 			name = str()
# 			name = tag = tuple(tags.split(' '))

# 		name_list.append(name)
# 		tag_list.append(tag)
# 		tags_dict[tag].append(name)

# 	return tags_dict, tag_list, name_list

def extract_tagnames(extract):

	tags_dict = defaultdict(list)
	# tags_dict = dict()
	name = None
	name_list = list()
	tag_list = list()

	for tags in extract.split(','):
		if len(tags.split(' ')) == 3:
			name = str()
			tag, class_name, name  = tuple(tags.split(' '))
		elif len(tags.split(' ')) == 1:
			name = str()
			class_name = name = tag = tuple(tags.split(' '))

		name_list.append(name)
		tag_list.append(tag)
		tags_dict[tag].append([class_name, name])

	return tags_dict, tag_list, name_list

def create_dataframe(path, column_list):
	writer = pd.ExcelWriter(path, engine='xlsxwriter')
	output_dataframe = pd.DataFrame(columns=column_list)

	return writer, output_dataframe

def web_scrapper(url, extract, path):
	
	tags_dict = dict()
	name_list = list()
	data_scrap_list = list()

	# url = input('Enter URL of Website: ')
	# project_name = input('Input Name of Project: ')
	# sheet_name = input('Input Sheet Name: ')


	
	# tags_dict, _, name_list = extract_tagnames(input("""Enter tags and their names example:\
	# 													div car-name,p car-desc,h5,h3 price-car\
	# 													\n\nNote: No whitespaces between commas.\n""").strip())
	
	tags_dict, _, name_list = extract_tagnames(extract)

	# print(f'ONE: {tags_dict} \n TWO: {name_list}')

	writer, output_dataframe = create_dataframe(path, name_list)

	r = requests.get(url)
	htmlContent = r.content
	soup = BeautifulSoup(htmlContent, 'html.parser')

	# count = 0
	for tag, names in tags_dict.items():
		# print(f'THREE: {tag} - {names} - {count}')
		# count = count + 1

		for name in names:
			data_list = list()
			if tag is not name[1]:
				# find_all("tr",  {"class": ["abc", "xyz"]})
				# data_scrap_list = soup.find_all(tag, {"class": name})
				if name[0] == 'class':
					data_scrap_list = soup.find_all(tag, class_=name[1])
				elif name[0] == 'itemprop':
					data_scrap_list = soup.find_all(tag, itemprop=name[1])
				elif name[0] == 'id':
					data_scrap_list = soup.find_all(tag, id=name[1])
			elif tag is name[1]:
				data_scrap_list = soup.find_all(tag)

			# print(f'FOUR: {data_scrap_list}')

			for data in data_scrap_list:
				data_list.append(data.text)

			# print(f'FIVE: {data_list}')

			# print(f'SIX: {pd.Series(data_list)}')
			output_dataframe[name[1]] = pd.Series(data_list)


	output_dataframe.to_excel(writer, sheet_name='sheet_name')
	writer.save()
	writer.close()
	# print('complete')

def api_format(api, path):
	display_json(requests.get(api).json(), path)

def api_scrapper(api, contents, tags, path):

	# api = input('Enter API to Extract Data: ')
	# project_name = input('Input Name of Project: ')
	# sheet_name = input('Input Sheet Name: ')

	data = requests.get(api).json()
	# display_json(data, sheet_name)

	not_reached = True

	while(not_reached):
		# contents = input('Give Direction to Content example: data->content\n')

		for index, content in enumerate(contents.split('->')):
			if index == 0:
				if content in data:
					not_reached = False
					main_data = data[content]
				continue

			if content in main_data:
				not_reached = False
				main_data = main_data[content]
			else:
				not_reached = True

			if not_reached:
				print('Could not find the given path please try again...\n\n')
				return 'Error'
				# TODO: Error

	# tags = input('Input the tags in comma seperated format example: carname,price,kms\n\nNote: No whitespaces between commas\n')
	
	writer, output_dataframe = create_dataframe(path, tags.split(','))

	columns = defaultdict(list)

	for inner_data in main_data:
		for tag in tags.split(','):
			if tag in inner_data:
				columns[tag].append(inner_data[tag])
			else:
				pass
				# TODO: Error

	for tag, inner in columns.items():
		output_dataframe[tag] = pd.Series(inner)

	output_dataframe.to_excel(writer, sheet_name='sheet_name')
	writer.save()
	writer.close()
	# print('complete')