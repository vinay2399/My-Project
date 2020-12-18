import pymysql

def userdb():
    conn = pymysql.connect(passwd='', host='localhost', user='root', port=3306, db='project', autocommit=True)
    cur = conn.cursor()
    return cur


def checkphoto(email):
    cur = userdb()
    cur.execute("select * from profile where email='"+email+"'")
    n=cur.rowcount
    photo="NO"
    if n>0:
        row=cur.fetchone()
        photo=row[6]
    return photo


def check(a,b):
    c=a
    d=str(b).split(',')
    for i in range(len(c)):
        for j in range(len(d)):
            if (c[i] == d[j]):

                return str(d)
            else:
                pass


    return str(d)