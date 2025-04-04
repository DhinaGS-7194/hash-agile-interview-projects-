import csv
from math import floor
import psycopg2 as pg
cur=pg.connect(host="localhost",dbname="postgres",user="postgres",password="1234",port=5432).cursor()

file=open(r"others\csv\data.csv",'r')
# writer=csv.writer(file, delimiter=' ',lineterminator='\n')
# writer.writerow(["user"]*3)
reader=[]
for rows in csv.reader(file, delimiter=' ', lineterminator='\n'):
    row=[]
    for i in rows:
        try:
            float(i)
            try:
                int(i)
                row.append(int(i))
            except ValueError:
                row.append(float(i))
        except ValueError:
            row.append(i)
    reader.append(row)
print(reader)

table="csv1"
field_set=True
for row in reader:
    if field_set:
        cur.execute(f"CREATE TABLE {table}();")

        data_types=[]
        for data in reader[-1]:
            if isinstance(data,float):
                data_types.append('FLOAT')
            elif isinstance(data,int):
                data_types.append('INTEGER')
            else:
                data_types.append('TEXT')

        for i in range(len(row)):
            cur.execute(f"ALTER TABLE {table} ADD {row[i]} {data_types[i]};")

        cur.execute("COMMIT;")
        field_set=False
    else:
        cur.execute(f"INSERT INTO csv1 VALUES{tuple(row)};")
    
cur.execute("COMMIT;")

file.close()




