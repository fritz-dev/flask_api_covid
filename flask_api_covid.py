from flask import Flask, request
from flask_restful import Resource, Api
import pandas as pd
import json
import requests
import io

#df = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/08-17-2020.csv",usecols= ['Province_State','Country_Region','Confirmed','Deaths','Recovered','Active','Combined_Key'])

#result = df.to_json(orient="split")
#print(data.head())

app = Flask(__name__)
api = Api(app)

class HelloWrold(Resource):
	def get(self):
		#return {'about':'Hello World!'}
		return result

	def post(self):
		some_json = request.get_json()
		return {'you sent': some_json},201

class Multi(Resource):
	def get(self, num):
		return {'result': num * 10}


class DataHandlerFunction(Resource):

	def get(self):
		getCountry = request.args.get('country') #get parameter from HTTP request
		getDate = request.args.get('date') #get parameter from HTTP request, format DD-MM-YYYY

		result_status, result_data = CSVReaderToJson(getCountry,getDate)
		return {'Date ' : getDate,'Country ': getCountry , 'Message': result_data}

def CSVReaderToJson(country,date):
	result_status = 'FAILURE'
	result_data = []
	str_date = str(date)
	csv_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/" + str_date +".csv"
	try:
		url_content = requests.get(csv_url).content
		raw_csv = pd.read_csv(io.StringIO(url_content.decode('utf-8')),usecols= ['Province_State','Country_Region','Confirmed','Deaths','Recovered','Active','Combined_Key'])
		
		filter_csv = raw_csv['Country_Region'].str.contains(country, na=False)
		csv_data = raw_csv[filter_csv]

		final_row_data = []
		for index,rows in csv_data.iterrows():
			final_row_data.append(rows.to_dict())

		json_result = {'FinalData':final_row_data}
		result_data.append(json_result)
		result_status = 'SUCCESS'

	except:
		result_data.append({'message': 'Unable to process the request, sample request : http://localhost:5000/?country=Japan&date=08-18-2020'})


	return result_status, result_data


api.add_resource(HelloWrold,'/a')
api.add_resource(Multi,'/multi/<int:num>')
api.add_resource(DataHandlerFunction,'/')

if __name__== '__main__':
    app.run(debug=True)
