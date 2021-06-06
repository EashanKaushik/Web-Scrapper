from flask import Flask, url_for
from app import views

app = Flask(__name__)

app.add_url_rule('/home','home',views.home)
app.add_url_rule('/web_scrapper','web_scrapper',views.web_scrapper, methods=['GET','POST'])
app.add_url_rule('/api_format','api_format',views.api_format, methods=['GET','POST'])
app.add_url_rule('/api_scrapper','api_scrapper',views.api_scrapper, methods=['GET','POST'])

app.add_url_rule('/download_file_web','download_file_web',views.download_file_web)
app.add_url_rule('/download_file_format','download_file_format',views.download_file_format)
app.add_url_rule('/download_file_api','download_file_api',views.download_file_api)


if __name__ == "__main__":
	app.run(debug=True)