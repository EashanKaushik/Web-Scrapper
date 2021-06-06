from flask import render_template, request, Flask, url_for, send_file, redirect
from models import model

web_path = 'd:\\Users\\Eashan\\Desktop\\Scrapper\\static\\output\\web\\'
api_path = 'd:\\Users\\Eashan\\Desktop\\Scrapper\\static\\output\\api\\'
# file = ['Output']

def home():
    return render_template('base.html', pagename='Base')


def web_scrapper():
	dataupload = False

	if request.method == 'POST':
		global file
		dataupload=True
		url = request.form['url']
		# file[0] = request.form['project_name']
		# sheet_name = request.form['sheet_name']
		extract = request.form['extract']
		model.web_scrapper(url, extract, web_path + 'Output.xlsx')
		# return redirect(url_for('download_file', file_name=file_name))
		return render_template('web_scrapper.html',
			pagename='Web Scrapper Download',
			dataupload=dataupload)
	return render_template('web_scrapper.html',
		pagename='Web Scrapper',
		dataupload=dataupload)

def api_format():
	dataupload = False

	if request.method == 'POST':
		global file
		dataupload=True
		api = request.form['api']
		# file[0] = request.form['file_name']
		model.api_format(api, api_path + 'Output.txt')
		return render_template('api_format.html', 
			pagename='API Format Download', 
			dataupload=dataupload)
	return render_template('api_format.html',
		pagename='API Format',
		dataupload=dataupload)

def api_scrapper():
	dataupload = False

	if request.method == 'POST':
		global file
		dataupload=True
		api = request.form['api']
		# file[0] = request.form['project_name']
		# sheet_name = request.form['sheet_name']
		contents = request.form['contents']
		tags = request.form['tags']
		model.api_scrapper(api, contents, tags, api_path + 'Output.xlsx')
		return render_template('api_scrapper.html',
			pagename='API Scrapper Download',
			dataupload=dataupload)
	return render_template('api_scrapper.html',
		pagename='API Scrapper', 
		dataupload=dataupload)

def download_file_web():
	return send_file(web_path + 'Output.xlsx', attachment_filename='Output.xlsx',as_attachment=True)

def download_file_format():
	return send_file(api_path + 'Output.txt', attachment_filename='Output.txt',as_attachment=True)

def download_file_api():
	return send_file(api_path + 'Output.xlsx', attachment_filename='Output.xlsx' ,as_attachment=True)