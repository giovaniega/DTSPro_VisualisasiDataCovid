import sqlite3

conn = sqlite3.connect('covid19.db')
print ("Opened database successfully")

conn.execute('''CREATE TABLE KASUS_COVID
         (ID              INT PRIMARY KEY   NOT NULL,
         TANGGAL          TEXT              NOT NULL,
         L_ID           VARCHAR(255)        NOT NULL,
         LOKASI         VARCHAR(255)        NOT NULL,
         KASUS            INT               NOT NULL,
         MENINGGAL        INT               NOT NULL,
         SEMBUH           INT               NOT NULL,
         T_KASUS          INT               NOT NULL,
         T_MENINGGAL      INT               NOT NULL,
         T_SEMBUH         INT               NOT NULL);''')

print ("Table created successfully")