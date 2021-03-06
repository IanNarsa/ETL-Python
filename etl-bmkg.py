from kamus import kamus_cuaca
import bonobo
import requests as req
import xmltodict
import json
def input_data():
    _input = input("Masukan Nama Wilayah : ")
    return _input

def scrape_bmkg(wilayah):
    try:
        print("scrape ",wilayah)
        #wilayah = 'DIYogyakarta'
        url = 'http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-'+wilayah+'.xml'
        body = req.get(url)
        parse_data = xmltodict.parse(body.text,attr_prefix='')
        print(parse_data)
        hasil = json.dumps(parse_data)
        final = json.loads(hasil)
        dt = final['data']['forecast']
        return dt, wilayah
    except :
        return None
    
    
def extract(x):
    try:
        print("extract ",x)
        yield scrape_bmkg(x)[0]
    except :
        print("Data Tidak Ditemukan")
    

def transform(dt):
    try:
        dCuaca = kamus_cuaca()
        _data = []
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
                        kd = y['value']['#text']
                        ketCuaca = dCuaca[int(kd)]
                        y['value']['#text'] = ketCuaca
                        weather.append(y)
            temp = {
                'weather':weather
            }
            area.update(temp)
            _data.append(area)
        
        yield _data
    except :
        None
    

def load(xyz):
    try:
        nama = xyz[0]['propinsi']
        nama = nama.replace(' ','')
        with open(nama+'.json', 'w') as fp:
            json.dump(xyz, fp)
    except :
        print("Tidak Dapat Menampilkan Hasil")
    

if __name__ == '__main__':
    x = input_data()
    graph = bonobo.Graph(
        extract(x),
        transform,
        load
    )
    bonobo.run(graph)