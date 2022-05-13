from pandas import DataFrame
from tkinter import *
from tkcalendar import Calendar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta, date
import matplotlib.pyplot as plt
import sqlite3

def ambilData(awal, akhir):
        conn = sqlite3.connect('covid19.db')

        tanggalAwal = datetime.strptime(awal,"%m/%d/%y").date()
        tanggalAkhir = datetime.strptime(akhir,"%m/%d/%y").date()

        data_kasus, data_sembuh, data_daerah, data_total, data_tanggal = [], [], [], [], []

        if(tanggalAwal.month==tanggalAkhir.month and tanggalAwal.year==tanggalAkhir.year):
                parameter = 'Tanggal'

                delta = tanggalAkhir - tanggalAwal
                for i in range(delta.days+1):
                        tanggal = tanggalAwal + timedelta(days=i)
                        tanggal_int = int(tanggal.day)

                        var = str(tanggal)+' 00:00:00'
                        raw = conn.execute("SELECT * FROM KASUS_COVID WHERE TANGGAL = (?) ORDER BY KASUS DESC",(var,))
                        kasus = 0
                        sembuh = 0
                        for x in raw:
                                kasus += x[4]
                                sembuh += x[6]

                        if(i==delta.days):
                                raw = conn.execute("SELECT * FROM KASUS_COVID WHERE TANGGAL = (?) AND (L_ID = 'ID-JK' OR L_ID = 'ID-JB' OR L_ID = 'ID-JT' OR L_ID = 'ID-JI' OR L_ID = 'ID-KI')",(var,))
                                for x in raw:
                                        data_daerah.append(x[2])
                                        data_total.append(x[7])
                        data_kasus.append(kasus)
                        data_sembuh.append(sembuh)
                        data_tanggal.append(tanggal_int)

        elif(tanggalAwal.year==tanggalAkhir.year):
                parameter = 'Bulan'

                delta = tanggalAkhir.month - tanggalAwal.month
                for i in range(delta+1):
                        kasus = 0
                        bulan = int(tanggalAwal.month + i)

                        tanggalAwal_ = date(tanggalAwal.year, bulan, 1)
                        if(bulan!=2):
                                tanggalAkhir_ = date(tanggalAkhir.year, bulan, 30)
                        else:
                                tanggalAkhir_ = date(tanggalAkhir.year, bulan, 28)

                        delta = tanggalAkhir_ - tanggalAwal_
                        print(delta)
                        for j in range(delta.days+1):
                                tanggal = tanggalAwal_ + timedelta(days=j)

                                var = str(tanggal)+' 00:00:00'
                                raw = conn.execute("SELECT * FROM KASUS_COVID WHERE TANGGAL = (?)",(var,))
                                for x in raw:
                                        kasus += x[4]
                        
                                # print(kasus)
                        print(kasus)

                        data_kasus.append(kasus)
                        data_tanggal.append(bulan)
                

        else:
                pass

        conn.close()

        output = {'kasus':data_kasus, 'sembuh':data_sembuh, 'tanggal':data_tanggal, 'parameter':parameter}
        return output

def pilih_tanggal(ax2, cal1, cal2):
        tanggal_awal = cal1.get_date()
        tanggal_akhir = cal2.get_date()
        tanggal.config(text = "Tanggal " + tanggal_awal + ' s.d ' + tanggal_akhir, bg='white')

        data = ambilData(tanggal_awal,tanggal_akhir)
        print(data)

        data_kasus = {data['parameter']: data['tanggal'],
        'Jumlah Kasus Baru': data['kasus']
        }  
        df2 = DataFrame(data_kasus,columns=[data['parameter'],'Jumlah Kasus Baru'])

        ax2.clear()
        df2 = df2[[data['parameter'],'Jumlah Kasus Baru']].groupby(data['parameter']).sum()
        df2.plot(kind='line', legend=True, ax=ax2, color='r',marker='o', fontsize=10)
        line2.draw()

def GUI():
        global tanggal, line2
        
        root= Tk()
        root.configure(bg='white')

        # Grafik
        data2={}
        df2=DataFrame(data2, columns=['Bulan','Jumlah Kasus Baru'])
        figure2 = plt.Figure(figsize=(10,4), dpi=100)
        ax2 = figure2.add_subplot(111)
        line2 = FigureCanvasTkAgg(figure2, root)
        line2.get_tk_widget().pack(side=RIGHT, fill=BOTH)
        df2 = df2[['Bulan','Jumlah Kasus Baru']].groupby('Bulan').sum()
        ax2.set_title('Bulan Vs. Jumlah Kasus Baru')

        # Tanggal awal
        cal1 = Calendar(root, selectmode = 'day', facecolor='white')
        cal1.pack(side=TOP, fill=NONE, expand=True)

        # Tanggal akhir
        cal2 = Calendar(root, selectmode = 'day', facecolor='white')
        cal2.pack(side=TOP, fill=NONE, expand=True)
        cal1.pack(pady = 70)

        # Tombol
        Button(root, text = "Pilih Tanggal",
                command = lambda: pilih_tanggal(ax2, cal1, cal2)).pack(pady = 20)

        # Tanggal
        tanggal = Label(root, text = "")
        tanggal.pack(pady = 20)

        # Label Judul
        judul = Label(root,text ='Visualisasi Data Covid-19 berbasis Waktu', font=('Verdana',15), bg='white')
        judul.place(relx = 0.6, rely = 0.0, anchor ='ne')

        # Label Developer
        developed = Label(root,text ='Developed by team T', 
                                font=('Verdana',10), bg='white')
        developed.place(relx = 0.6, rely = 1.0, anchor ='sw')

        root.mainloop()

if __name__ == "__main__":
        GUI()