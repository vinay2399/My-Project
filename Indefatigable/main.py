from typing import Any, Union

from flask import Flask,render_template,request,url_for,redirect,session
import time
import datetime

from werkzeug.utils import secure_filename
import pymysql

from mylib import *
import os
conn = pymysql.connect(passwd='', host='localhost', user='root', port=3306, db='project', autocommit=True)
cur = conn.cursor()


app=Flask(__name__)
app.secret_key="super secret key"
app.config['UPLOAD_FOLDER']='./static/photos'

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        #collect form data and save it
        email=request.form['T1']
        password=request.form['T2']
        confpwd=request.form['T3']

        #connectivity
        conn=pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='project',autocommit=True)
        cur=conn.cursor()
        if password==confpwd:
            sql="insert into signup values('"+email+"','"+password+"','"+confpwd+"')"
            sql2="insert into logindata values('"+email+"','"+password+"')"
            sql3 = "insert into test_link(email) values('" + email + "')"

            cur.execute(sql)
            n=cur.rowcount

            cur.execute(sql2)
            m=cur.rowcount

            cur.execute(sql3)

            msg="Error: Cannot save data try again"
            if n==1 and m==1 :
                msg='Data saved and login created'
            elif n==1:
                msg='Data saved but login not created'
            elif m==1:
                msg='Login created but data not saved'
            #send response
            return render_template('signup.html',kota=msg)
        else:
            msg='Password does not match'
            return render_template('signup.html',kota=msg)
    else:
        return render_template('signup.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['T1']
        password = request.form['T2']
        cur = userdb()


        sql = "select * from logindata where email='" + email + "' and password='" + password + "'"

        cur.execute(sql)
        n = cur.rowcount
        if n == 1:
            data = cur.fetchone()
            usertype = data[0]

            # session creating
            session["email"] = usertype
            session["password"] = password
            if email=='recruiter@gmail.com':
                return redirect(url_for('recruiterhome'))
            elif email=='admin@gmail.com':
                return render_template('adminhome.html')




            return redirect(url_for('applicanthome'))
        else:
            return render_template('login.html', msg="Incorrect email or password")
    else:
        return render_template('login.html')



@app.route('/')
def sample():
    return render_template('sample.html')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/applicanthome')
def applicanthome():
    if 'email' in session:
        return render_template('applicanthome.html')
    else:
        return redirect(url_for('auth_error'))
@app.route('/create_profile',methods=['GET','POST'])
def create_profile():
    if 'email' in session:
        e1 = session['email']
        if request.method=='POST':
            #collect form data and save it
            name=request.form["T1"]

            address=request.form["T2"]
            qualification=request.form["T3"]
            skills=request.form['T4']
            twlthmarks=request.form["T5"]
            tenthmarks=request.form["T6"]
            file=request.files["F1"]

            path = os.path.basename(file.filename)
            file_ext = os.path.splitext(path)[1][1:]
            filename = str(int(time.time())) + '.' + file_ext
            filename = secure_filename(filename)

            #connectivity
            conn=pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='project',autocommit=True)
            cur=conn.cursor()

            sql="insert into create_profile values('"+name+"','"+address+"','"+qualification+"','"+skills+"','"+twlthmarks+"','"+tenthmarks+"','"+e1+"')  "
            sql2="insert into profile values('"+name+"','"+address+"','"+qualification+"','"+skills+"','"+twlthmarks+"','"+tenthmarks+"','"+e1+"','"+filename+"') "
            if name!="" and address!="" and qualification!="" and twlthmarks!="" and tenthmarks!="" and filename!="":
                cur.execute(sql)
                n=cur.rowcount

                cur.execute(sql2)
                m=cur.rowcount

                msg="Error: Cannot save data try again"
                if n==1 and m==1 :
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    msg='Data saved and profile created'
                elif n==1:
                    msg='Data saved but profile not created'
                elif m==1:
                    msg='profile created but data not saved'
                #send response


                return render_template('create_profile.html',data=msg)
            else:
                msg = 'Incorrect input'

                return render_template('create_profile.html', data=msg)

        else:
            return render_template('create_profile.html')
    else:
        return redirect(url_for('auth_error'))

@app.route('/candidate_profile',methods=['GET','POST'])
def candidate_profile():
    if 'email' in session:

        e1 = session['email']


        conn = pymysql.connect(host='localhost', user='root', db='project', passwd='', autocommit=True)
        cur = conn.cursor()
        sql = "select * from profile where email='"+e1+"'"

        cur.execute(sql)
        n = cur.rowcount
        if n>0:
            image = checkphoto(e1)
            data = cur.fetchone()
            return render_template('candidate_profile.html',photo=image,jpr=data)
        else:
            msg="Nothing to show...some error"
            return render_template('candidate_profile.html', kota=msg)
    else:
        return redirect(url_for('auth_error'))




@app.route('/applicantprofile',methods=['GET','POST'])
def applicantprofile():
    if 'email' in session:
        if request.method == 'POST':

            e1 = request.form['T1']


            conn = pymysql.connect(host='localhost', user='root', db='project', passwd='', autocommit=True)
            cur = conn.cursor()
            sql = "select * from profile where email='"+e1+"'"

            cur.execute(sql)
            n = cur.rowcount
            if n>0:
                image = checkphoto(e1)
                data = cur.fetchone()
                return render_template('applicantprofile.html',photo=image,jpr=data)
            else:
                msg="Nothing to show...Error"
                return render_template('applicantprofile.html', kota=msg)
        else:
            return render_template('applicantprofile.html')
    else:
        return redirect(url_for('auth_error'))

@app.route('/faq')
def faq():
    if 'email' in session:
        return render_template('faq.html')
    else:
        return redirect(url_for('auth_error'))
@app.route('/forgotpassword',methods=['GET','POST'])
def forgotpassword():

    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='project', autocommit=True)
    cur = conn.cursor()
    if request.method=='POST':
        email = request.form['T1']
        msg='Nothing Entered'
        if email!="":
            sql = "insert into forgot_password values('" + email + "')"
            cur.execute(sql)
            n = cur.rowcount
            if n==1:
                msg=" Request submitted ! We will get back to you with in 24hrs."
                return render_template('forgotpassword.html',msg=msg)
            else:
                msg = " Error !"
                return render_template('forgotpassword.html', msg=msg)

        else:
            return render_template('forgotpassword.html', msg=msg)
    else:
        return render_template('forgotpassword.html')




@app.route('/schedule',methods=['GET','POST'])
def schedule():
    if 'email' in session:
        e1 = session["email"]
        if e1 == "recruiter@gmail.com" or e1 == "admin@gmail.com":
            if request.method=='POST':
                timing=request.form['T1']
                date=request.form['T2']
                venue=request.form['T3']
                email=request.form['T4']
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='project', autocommit=True)
                cur = conn.cursor()


                sql = "insert into schedule values('" + timing + "','" + date + "','" + venue + "','"+ email +"') "
                if timing != "" and date != "" and venue != "" and email != "":
                    cur.execute(sql)
                    n = cur.rowcount
                    msg="Incorrect input"

                    if n == 1:
                        msg="Done"
                        return render_template('schedule.html',kota=msg)
                    else:

                        return render_template('schedule.html', kota=msg)
                else:
                    msg = "Incorrect input"
                    return render_template('schedule.html', kota=msg)

            else:
                msg="Nothing posted"
                return render_template('schedule.html', kota=msg)
        else:
            msg = 'You are not authorized..!'
            # send response
            return render_template('schedule.html', kota=msg)
    else:
        return redirect(url_for('auth_error'))

@app.route('/show_schedule')
def show_schedule():
    if 'email' in session:
        e1=session["email"]
        cur=userdb()
        sql = "select * from schedule where email='"+e1+"'"

        cur.execute(sql)
        n = cur.rowcount
        if n>0:
            data=cur.fetchone()
            return render_template('show_schedule.html',a=data)
        else:
            msg="No data found"
            return render_template('show_schedule.html',kota=msg)
    else:
        return redirect(url_for('auth_error'))


@app.route('/provide_test_link',methods=['GET','POST'])
def provide_test_link():
    if 'email' in session:
        e1 = session["email"]
        if e1 == "recruiter@gmail.com" or e1 == "admin@gmail.com":
            if request.method=='POST':
                #collect form data and save it
                link1=request.form['T1']
                email=request.form['T2']

                #connectivity
                conn=pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='project',autocommit=True)
                cur=conn.cursor()

                sql="update test_link set link='"+link1+"' where email='"+email+"'"
                #sql2="insert into logindata values('"+email+"','"+password+"')"
                if link1!="" and email!="":
                    cur.execute(sql)
                    n=cur.rowcount

                    msg="Error: Cannot save data try again"
                    if n>0:
                        msg='Link provided..!'
                        return render_template('provide_test_link.html', kota=msg)
                    #send response
                    return render_template('provide_test_link.html',kota=msg)
                else:
                    msg = 'Incomplete Entry!'
                    return render_template('provide_test_link.html', kota=msg)

            else:
                return render_template('provide_test_link.html')
        else:
            msg = 'You are not authorized..!'
            # send response
            return render_template('provide_test_link.html', kota=msg)
    else:
        return redirect(url_for('auth_error'))
@app.route('/recruiterhome')
def recruiterhome():
    if 'email' in session:
        return render_template('recruiterhome.html')
    else:
        return redirect(url_for('auth_error'))
@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/show_link')
def show_link():
    if 'email' in session:
        e1=session["email"]
        cur=userdb()
        sql = "select link from test_link where email='"+e1+"'"

        cur.execute(sql)
        n = cur.rowcount
        if n>0:
            data=cur.fetchall()
            return render_template('show_link.html',jpr=data)
        else:
            msg="No data found"
            return render_template('show_link.html',kota=msg)
    else:
        return redirect(url_for('auth_error'))



@app.route('/post_notification',methods=['GET','POST'])
def post_notification():
    if 'email' in session:
        e1=session["email"]
        if e1=="recruiter@gmail.com" or e1=="admin@gmail.com":
            if request.method=='POST':
                #collect form data and save it
                msg=request.form['T1']
                email=request.form['T2']
                ct = datetime.datetime.now()
                time = str(ct)

                #connectivity
                conn=pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='project',autocommit=True)
                cur=conn.cursor()

                sql="insert into notification (msg,email,timestamp) values('"+msg+"','"+email+"','"+ time +"')"
                #sql2="insert into logindata values('"+email+"','"+password+"')"
                if msg!="" and email!="":

                    cur.execute(sql)


                    n=cur.rowcount

                    msg="Error: Cannot save data try again"
                    if n>0:
                        msg='Msg sent..!'
                    #send response
                    return render_template('post_notification.html',kota=msg)
                else:
                    msg = 'Incomplete Entry !'
                    return render_template('post_notification.html', kota=msg)

            else:
                return render_template('post_notification.html')
        else:
            msg = 'You are not authorized..!'
            # send response
            return render_template('post_notification.html', kota=msg)
    else:
        return redirect(url_for('auth_error'))


@app.route('/show_notification')
def show_notification():
    if 'email' in session:
        e1=session["email"]
        cur=userdb()
        sql = "select msg,timestamp from notification where email='"+e1+"' order by timestamp desc"

        cur.execute(sql)
        n = cur.rowcount
        if n>0:
            data=cur.fetchall()
            return render_template('show_notification.html',jpr=data)
        else:
            msg="No data found"
            return render_template('show_notification.html',kota=msg)
    else:
        return redirect(url_for('auth_error'))



@app.route('/post_vaccancies',methods=['GET','POST'])
def post_vaccancies():
    if 'email' in session:
        e1 = session["email"]
        if e1 == "recruiter@gmail.com" or e1 == "admin@gmail.com":
            if request.method=='POST':
                #collect form data and save it
                #session wala code
                jobname=request.form['T1']
                skills = request.form['T2']
                process=request.form['T3']
                testlink=request.form['T4']
                #connectivity
                conn=pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='project',autocommit=True)
                cur=conn.cursor()
                sql = "insert into vaccancies values('" + jobname + "','" + skills + "', '" + process + "','" + testlink + "')"


                if jobname!="" and skills!="" and process!="" and testlink!="":

                    cur.execute(sql)
                    n=cur.rowcount

                    msg="Error: Cannot save data try again"
                    if n==1:
                        msg='Job Posted..!'
                    #send response
                    return render_template('post_vaccancies.html',kota=msg)
                else:
                    msg = "Error: Cannot save data try again"
                    return render_template('post_vaccancies.html', kota=msg)
            else:
                return render_template('post_vaccancies.html')
        else:
            msg = 'You are not authorized..!'
            # send response
            return render_template('provide_test_link.html', kota=msg)
    else:
        return redirect(url_for('auth_error'))
@app.route('/job_available')
def job_available():
    if 'email' in session:
        e1 = session["email"]
        cur=userdb()
        sql = "select * from vaccancies"
        #sql1 = "select skills from profile where email='"+e1+"'"

        cur.execute(sql)

        n = cur.rowcount
        if n>0:
            data=cur.fetchall()
            #cur.execute(sql1)
            #data2=cur.fetchall()
            #str1=''.join(data2)
            #str2=''.join(data[1])
            #c = str1.split(',')
            #d = str2.split(',')

            #a=check(c,d)
            #sql2 = "select * from vaccancies where skills='" + a + "'"
            #cur.execute(sql2)
            #data3=cur.fetchall()
            render_template('job_available.html',jpr=data)
            return render_template('job_available.html',jpr=data)
        else:
            msg="No data found"
            return render_template('job_available.html',kota=msg)
    else:
        return redirect(url_for('auth_error'))


@app.route('/jobs_posted',methods=['GET', 'POST'])
def jobs_posted():
    if 'email' in session:
        e1=session["email"]
        if e1=="recruiter@gmail.com" or e1=="admin@gmail.com":

            cur=userdb()
            sql = "select * from vaccancies"

            cur.execute(sql)
            n = cur.rowcount
            if n>0:
                data=cur.fetchall()
                return render_template('jobs_posted.html', jpr=data)
            else:
                msg="No data found"
                return render_template('jobs_posted.html', kota=msg)
        else:
            msg="You are not Authorized!!!"
            return render_template('jobs_posted.html', kota=msg)
    else:
        return redirect(url_for('auth_error'))


@app.route('/edit_profile',methods=['GET','POST'])
def edit_profile():
    if 'email' in session:
        e1 = session['email']
        if request.method == 'POST':


            name=request.form['T1']
            address=request.form['T2']
            qualification = request.form['T3']
            skills = request.form['T4']

            file = request.files['F2']
            if file:
                path = os.path.basename(file.filename)
                file_ext = os.path.splitext(path)[1][1:]
                filename = str(int(time.time())) + '.' + file_ext
                filename = secure_filename(filename)
                cur=userdb()
                sql="update profile set name='"+name+"',address='"+address+"',qualification='"+qualification+"',skills ='"+skills+"',photo='"+filename+"' where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:

                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    return render_template('edit_profile.html',photo=image,msg="Data Saved")
                else:
                    return render_template('edit_profile.html', msg="Nothing has been changed")
            else:
                cur = userdb()
                sql = "update profile set name='" + name + "',address='" + address + "',qualification='" + qualification + "',skills ='"+skills+"' where email='" + e1 + "'"
                cur.execute(sql)
                n = cur.rowcount
                if n == 1:

                    return render_template('edit_profile.html', msg="Data Saved")
                else:
                    return render_template('edit_profile.html', msg="Nothing has been changed")

        else:
            #fetch the data of logged in admin
            sql="select * from profile where email='"+e1+"'"
            cur=userdb()
            cur.execute(sql)
            n=cur.rowcount
            if n==1:
                data=cur.fetchone()
                return render_template('edit_profile.html',data=data)
            else:
                return render_template('edit_profile.html',msg="No data found")
    else:
        return redirect(url_for('auth_error'))

@app.route('/support_recruiter')
def support_recruiter():
    return render_template('support_recruiter.html')

@app.route('/changepassword',methods=['GET','POST'])
def changepassword():
    if 'email' in session:
        e1 = session['email']
        if request.method == 'POST':
            oldpass=request.form['T1']
            newpass=request.form['T2']
            conpass=request.form['T3']
            cur=userdb()

            if oldpass==newpass:
                if newpass==conpass:
                    msg='Password Same'
                    return render_template('changepassword.html',msg=msg)
                else:
                    msg='Confirm Password Does Not Match'
                    return render_template('changepassword.html',msg=msg)

            else:
                    if newpass=="" and conpass=="":
                        msg='Password Not Change'
                        return render_template('changepassword.html',msg=msg)

                    if newpass!="" and conpass!="":
                        msg='Wrong Password'
                        if newpass==conpass:
                            sql="update logindata set password='"+newpass+"' where email='"+e1+"' AND password='"+oldpass+"'"
                            cur.execute(sql)
                            n=cur.rowcount

                            if n==1:
                                msg='Password Changed'
                        return render_template('changepassword.html',msg=msg)
        else:
            return render_template('changepassword.html')
    else:
        return redirect(url_for('auth_error'))


@app.route('/logout')
def logout():
    if 'email' in session:
        #session.pop('usertype',None)
        session.pop('email',None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/get_testlink',methods=['GET','POST'])
def get_testlink():
    if 'email' in session:
        e1 = session["email"]
        if request.method=='POST':
            #collect form data and save it
            jobname=request.form['T1']
            email=request.form['T2']

            #connectivity
            conn=pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='project',autocommit=True)
            cur=conn.cursor()

            sql="insert into applications (jobname,email) values('"+jobname+"','"+email+"')"
            sql2="select testlink from vaccancies where jobname='"+jobname+"'"
            sql3="select jobname from vaccancies"
            #sql2="insert into logindata values('"+email+"','"+password+"')"
            cur.execute(sql3)
            jobs = cur.fetchall()
            if jobname!="" and email!="" and email==e1:
                cur.execute(sql)
                n=cur.rowcount
                cur.execute(sql2)

                msg="Error: Cannot save data try again"
                if n>0:
                    data = cur.fetchone()
                    return render_template('get_testlink.html', jpr=data)
                else:
                    msg = "Nothing to show...Error"
                    return render_template('get_testlink.html', kota=msg)
            else:
                msg = 'Some Error Occured!'
                return render_template('get_testlink.html', kota=msg)

        else:

            return render_template('get_testlink.html')

    else:
        return redirect(url_for('auth_error'))

@app.route('/show_applications',methods=['GET', 'POST'])
def show_applications():
    if 'email' in session:
        e1=session["email"]
        if e1=="recruiter@gmail.com" or e1=="admin@gmail.com":

            cur=userdb()
            sql = "select * from applications"

            cur.execute(sql)
            n = cur.rowcount
            if n>0:
                data=cur.fetchall()
                return render_template('show_applications.html', jpr=data)
            else:
                msg="No data found"
                return render_template('show_applications.html', kota=msg)
        else:
            msg="You are not Authorized!!!"
            return render_template('show_applications.html', kota=msg)
    else:
        return redirect(url_for('auth_error'))

@app.route('/candidate_scorecard',methods=['GET', 'POST'])
def candidate_scorecard():
    if 'email' in session:
        e1=session["email"]
        if e1=="recruiter@gmail.com" or e1=="admin@gmail.com":

            cur=userdb()
            sql = "select * from candidate_scores"

            cur.execute(sql)
            n = cur.rowcount
            if n>0:
                data=cur.fetchall()
                return render_template('candidates_scorecard.html', jpr=data)
            else:
                msg="No data found"
                return render_template('candidates_scorecard.html', kota=msg)
        else:
            msg="You are not Authorized!!!"
            return render_template('candidates_scorecard.html', kota=msg)
    else:
        return redirect(url_for('auth_error'))

@app.route('/auth_error')
def auth_error():
    return render_template('auth_error.html')


@app.route('/uploadphoto', methods=['GET','POST'])
def uploadphoto():
    if 'email' in session:
        e1 = session['email']
        if request.method == 'POST':
            file = request.files["F1"]

            path = os.path.basename(file.filename)
            file_ext = os.path.splitext(path)[1][1:]
            filename = str(int(time.time())) + '.' + file_ext
            filename = secure_filename(filename)

            cur = userdb()
            sql="update profile set photo='"+filename+"' where email='"+e1+"'"
            cur.execute(sql)
            n=cur.rowcount
            if n==1:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                return render_template('create_profile.html',result="Success")
            else:
                return render_template('create_profile.html', result="Failure")
        else:
            return render_template("create_profile.html")
    else:
        return redirect(url_for('auth_error'))

if __name__=="__main__":
    app.run(debug=True)