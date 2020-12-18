import pymysql

conn=pymysql.connect(host='localhost',user='root',db='project',passwd='',autocommit=True)
cur=conn.cursor()
sql="select * from profile"
print(sql)
cur.execute(sql)
n=cur.rowcount
if(n>0):
    data=cur.fetchall()
    print(data)
else:
    print("Try again..!!")
