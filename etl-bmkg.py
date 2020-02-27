import bonobo
import requests as req
import xmltodict
import json
def input_data():
    _input = input("Masukan Nama Wilayah : ")
    return _input

def scrape_bmkg(wilayah):
    print("scrape ",wilayah)
    #wilayah = 'DIYogyakarta'
    url = 'http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-'+wilayah+'.xml'
    body = req.get(url)
    parse_data = xmltodict.parse(body.text,attr_prefix='')
    hasil = json.dumps(parse_data)
    final = json.loads(hasil)
    dt = final['data']['forecast']
    return dt, wilayah
    
def extract(x):
    #yield input_data()
    print("extract ",x)
    yield scrape_bmkg(x)[0]

def transform(dt):
    _data = []
    db = {}    
    for i in dt['area']:
        x =  i['domain']
        weather = []
        area = {
            'source': 'BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)',
            'id': i['id'],
            'latitude': i['latitude'],
            'longitude': i['longitude'],
            'coordinate': i['coordinate'],
            'kabupaten': i['description'],
            'propinsi': i['domain'],
            'waktu': dt['issue']
        }
        for x in i['parameter']:
            if x['id'] == 'weather':
                for y in x['timerange']:
                    if y['value']['#text'] == "0":
                        y['value']['#text'] = "Cerah"
                    elif y['value']['#text'] == "1":
                        y['value']['#text'] = "Cerah Berawan"
                    elif y['value']['#text'] == "2":
                        y['value']['#text'] = "Cerah Berawan"
                    elif y['value']['#text'] == "3":
                        y['value']['#text'] = "Berawan"
                    elif y['value']['#text'] == "4":
                        y['value']['#text'] = "Berawan Tebal"
                    elif y['value']['#text'] == "5":
                        y['value']['#text'] = "Udara Kabur"
                    elif y['value']['#text'] == "10":
                        y['value']['#text'] = "Asap"
                    elif y['value']['#text'] == "45":
                        y['value']['#text'] = "Kabut"
                    elif y['value']['#text'] == "60":
                        y['value']['#text'] = "Hujan Ringan"
                    elif y['value']['#text'] == "61":
                        y['value']['#text'] = "Hujan Sedang"
                    elif y['value']['#text'] == "63":
                        y['value']['#text'] = "Hujan Lebat"
                    elif y['value']['#text'] == "80":
                        y['value']['#text'] = "Hujan Lokal"
                    elif y['value']['#text'] == "95":
                        y['value']['#text'] = "Hujan Petir"
                    elif y['value']['#text'] == "97":
                        y['value']['#text'] = "Hujan Petir"
                    else:
                        continue
                    weather.append(y)
        temp = {
            'weather':weather
        }
        area.update(temp)
        _data.append(area)
    
    
    return _data

def load(xyz):
    #nama = input_data()
    nama = xyz[0]['propinsi']
    nama = nama.replace(' ','')
    with open(nama+'.json', 'w') as fp:
        json.dump(xyz, fp)

if __name__ == '__main__':
    x = input_data()
    graph = bonobo.Graph(
        extract(x),
        transform,
        load
    )
    bonobo.run(graph)