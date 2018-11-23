import requests,time, urllib, urllib2, httplib, json, pymongo
from bs4 import BeautifulSoup
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')

req=requests.get('https://www.meneame.net/')
soup=BeautifulSoup(req.text,"html5lib")
container_clics=soup.body.find_next('div', {'id': 'container'})
newswrap_clics=container_clics.find_next('div',{'id':'newswrap'})
newsummary_clics=newswrap_clics.find_next('div', {'class':'news-summary'})
newsbody_clics=newsummary_clics.find_next('div', {'class':'news-body'})
newsshakeit_clics=newsbody_clics.find_next('div', {'class':'news-shakeit mnm-published'})
clics_string=newsshakeit_clics.find_next('div', {'class':'clics'})
clics_words=clics_string.text.split(" ")
print(clics_words[2])

variable_meneos=soup.body.find_next('div', {'id': 'variable'})
wrap_meneos=variable_meneos.find_next('div', {'id': 'wrap'})
container_meneos=wrap_meneos.find_next('div', {'id': 'container'})
newswrap_meneos=container_meneos.find_next('div',{'id':'newswrap'})
newsummary_meneos=newswrap_meneos.find_next('div', {'class':'news-summary'})
newsbody_meneos=newsummary_meneos.find_next('div', {'class':'news-body'})
newsshakeit_meneos=newsbody_meneos.find_next('div', {'class':'news-shakeit mnm-published'})
meneos_string=newsshakeit_meneos.find_next('div', {'class':'votes'})
meneos_words=meneos_string.text.split(" ")
print(meneos_words[1])

center_content_titulo=newsbody_meneos.find_next('div', {'class':'center-content'})
titulo_string_ascii=center_content_titulo.find_next('a')
titulo_string=titulo_string_ascii.text.encode('utf8')
print(titulo_string)

hora=time.strftime("%H:%M:%S") 
print(hora)
fecha=time.strftime("%d/%m/%y")
print(fecha)
#WRITE API KEY: UOXSWX0IVFY9O3Y9
#READ API KEY: XPS2IBDDGV9QU4G2

write_key="UOXSWX0IVFY9O3Y9"
params=urllib.urlencode({'field1':titulo_string,'field2':clics_words[2],'field3':meneos_words[1],'field4':hora, 'field5':fecha,'key':write_key})
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
conn = httplib.HTTPConnection("api.thingspeak.com:80")
conn.request("POST", "/update", params, headers)
response = conn.getresponse()
data=response.read()
conn.close()


mongo_client=pymongo.MongoClient()
mongo_database=mongo_client["meneame"]
col_mongo=mongo_database["Noticia"]
noticia={"Titulo:":titulo_string, "Clics:":clics_words[2],"Meneos:":meneos_words[1], "Hora:": hora, "Fecha": fecha}
col_mongo.insert_one(noticia)

