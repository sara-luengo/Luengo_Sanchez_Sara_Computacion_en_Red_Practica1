import  urllib, urllib2, json, pymongo
from flask import Flask, render_template, redirect, url_for, request
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')
app = Flask(__name__)

data=[
	{
		'created_at':'0',
		'entry_id': '0',
		'field1': '0',
		'field2': '0',
		'field3': '0',
		'field4': '0',
		'field5':'0'
	}
]
tipo=[
	{
		'tipo':''
	}
]

valor_medio=[
	{
		'valor': '',
		'database':''
	}
]
READ_API_KEY='XPS2IBDDGV9QU4G2'
CHANNEL_ID= '622947'
ENTRIES=100
database='MongoDB'
@app.route('/',methods = ['POST', 'GET'])
def home():
	global data
	global tipo
	global database
	global valor_medio
	if request.method == 'POST':
		if "umbral" in request.form:
			tipo=[{'tipo':'Registros que superan el umbral:'}]
			while len(valor_medio) > 0 : valor_medio.pop()
			while len(data) > 1 : data.pop()
			umbral = request.form['nm']
			read_data = urllib2.urlopen("https://api.thingspeak.com/channels/%s/feeds.json?api_key=%s&results=%d" \
									%(CHANNEL_ID,READ_API_KEY,ENTRIES))
			response_read = read_data.read()
			data_total=json.loads(response_read)
			data_feeds=data_total['feeds']
			contador=0;
			data=[{'created_at':'0','entry_id': '0','field1': '0','field2': '0','field3': '0','field4': '0','field5':'0'}]
			for dato in data_feeds:
				if dato['field2']>umbral:
					if contador==0:
						data[0]=dato
					else:
						data.append(dato)
					contador=contador+1	
					if contador==10:
						break
			read_data.close()
			return redirect(url_for('home'))

		elif "vmedio" in request.form:
			valor_medio=[{'valor': '','database':''}]
			while len(data) > 0 : data.pop()
			if database=='MongoDB':
				mongo_client=pymongo.MongoClient()
				mongo_database=mongo_client["meneame"]
				col_mongo=mongo_database["Noticia"]
				n_clics=0
				contador=0
				for entrada_mongo in col_mongo.find({},{'Clics:':True}):
					clics_mongo=int(entrada_mongo['Clics:'])
					n_clics=n_clics+clics_mongo
					contador=contador+1
				media=n_clics/float(contador)
				valor_medio=[{'valor': media,'database':database}]
				database='ThingSpeak'

			elif database=='ThingSpeak':
				read_data = urllib2.urlopen("https://api.thingspeak.com/channels/%s/feeds.json?api_key=%s&results=%d" \
									%(CHANNEL_ID,READ_API_KEY,ENTRIES))
				response_read = read_data.read()
				data_total=json.loads(response_read)
				data_feeds=data_total['feeds']
				n_clics=0
				contador=0
				for dato in data_feeds:
					clics_ts=int(dato['field2'])
					n_clics=n_clics+clics_ts
					contador=contador+1
				media=n_clics/float(contador)	
				valor_medio=[{'valor': media,'database':database}]
				dato['field2']
				read_data.close()
				database='MongoDB'
			tipo=[{'tipo':'Valor medio del numero de clics:'}]
			return redirect(url_for('home'))
		elif "graficas" in request.form:
			return redirect("https://thingspeak.com/channels/622947")
	elif request.method =='GET':
		return render_template('home.html', tipo=tipo, data=data,valor_medio=valor_medio)
	return render_template('home.html', tipo=tipo, data=data,valor_medio=valor_medio)


if __name__== '__main__':
	app.run(debug=True)
