# ETL-Python

## Extract Transform Load With Bonobo Python

Untuk menjalan program aktifkan terlebih dahulu virtual environment yang telah ada dengan perintah
```bash
source ETL/bin/activate
```
kemudian jalankan file etl-bmkg.py

Masukan wilayah yang akan diambil datanya, untuk nama wilayah bisa dilihat pada link BMKG yang tertera.

Pada aplikasi ini data yang digunakan berasal dari Data Prakiraan Cuaca Terbuka BMKG yang bisa diakses melalui link di bawah berikut :

[http://data.bmkg.go.id/prakiraan-cuaca/](http://data.bmkg.go.id/prakiraan-cuaca/)

Untuk alur kerjanya sendiri dimulai dari mengakses API BMKG dengan keyword nama Propinsi, data yang didapat ditransform.

Hasil transform
```json
{
    "source": "BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)",
    "id": "501186",
    "latitude": "-7.916666669",
    "longitude": "110.3167",
    "coordinate": "110.3167 -7.916666669",
    "kabupaten": "Bantul",
    "propinsi": "DI Yogyakarta",
    "waktu": 
            {
                "timestamp": "20200227034108",
                "year": "2020",
                "month": "02",
                "day": "27",
                "hour": "03",
                "minute": "41",
                "second": "08"
            },
    "weather": 
                [
                    {
                        "type": "hourly",
                        "h": "0",
                        "datetime": "202002270000",
                        "value": 
                                {
                                    "unit": "icon",
                                    "#text": "Berawan"
                                }
                    }
                ]
}
```

Setelah ditransform kemudian data disimpan dalam file json dengan nama sesuai dengan nama propinsi yang dicari.