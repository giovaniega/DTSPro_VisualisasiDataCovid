import csv
import sqlite3
from datetime import datetime

conn = sqlite3.connect('covid19.db')

filename = 'covid_19_indonesia_time_series_all.csv'
data = csv.reader(open(filename))

i = 0
for x in data:
    if(i==0):
        pass
    else:
        id              = i
        tanggal         = str(datetime.strptime(x[0],'%m/%d/%Y'))
        id_lokasi       = x[1]
        lokasi          = x[2]
        kasus           = int(x[3])
        meninggal       = int(x[4])
        sembuh          = int(x[5])
        totalKasus      = int(x[7])
        totalMeninggal  = int(x[8])
        totalSembuh     = int(x[9])

        conn.execute("INSERT INTO KASUS_COVID (ID,TANGGAL,L_ID,LOKASI,KASUS,MENINGGAL,SEMBUH,T_KASUS,T_MENINGGAL,T_SEMBUH) \
                VALUES (?, datetime(?), ?, ?, ?, ?, ?, ?, ?, ?)",(id,tanggal,id_lokasi,lokasi,kasus,meninggal,sembuh,totalKasus,totalMeninggal,totalSembuh))

        conn.commit()

    i+=1
    print(i)

conn.close()