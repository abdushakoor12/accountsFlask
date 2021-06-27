import re
import json
import logging
from cassandra.cluster import Cluster
from flask import Flask, render_template, url_for, request, redirect, session, Response, jsonify


app = Flask(__name__)

app.secret_key = 'walnutfish774'

@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == "POST":
        
        if request.form.get('loginButton') == 'Login':
            return render_template('login.html')
        
        elif request.form.get('registerButton') == 'Register':
            return render_template('register.html')
        
        else:
            return render_template('index.html')
    
    else:
        return render_template('index.html')



##################### LOGIN PAGE ROUTE #####################
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == "POST":
        
        if request.form.get('homeButton') == 'backToHome':
            return render_template('index.html')
        
        elif request.form.get('loginButtonFinal') == 'loginButton':

            uname_email = request.form['uname_email']
            password = request.form['password']


            cluster = Cluster(['192.168.1.236'], port=9042)
            keyspace_connect = cluster.connect('accounts')
            rows_username_status = keyspace_connect.execute("select status from loginusername where username='" + uname_email + "'")

            
            row_status_username = []


            for row in rows_username_status:
                row_status_username.append(row.status)

            keyspace_connect.shutdown()
            cluster.shutdown()

            if len(row_status_username) == 0:
                
                cluster = Cluster(['192.168.1.236'], port=9042)
                keyspace_connect = cluster.connect('accounts')
                rows_email_status = keyspace_connect.execute("select status from loginemail where email='" + uname_email + "'")

                keyspace_connect.shutdown()
                cluster.shutdown()

                row_status_email = []


                for row in rows_email_status:
                    row_status_email.append(row.status)

                if len(row_status_email) == 0:

                    msg = "No Such Username or Email in Records"
                    return render_template('login.html', msg=msg)

                elif len(row_status_email) > 0:
                    
                    row_status_email = jsonify(row_status_email)
                    row_status_email = str(row_status_email.data)
                    row_status_email = row_status_email[8:]
                    row_status_email = row_status_email[:-7]

                    if row_status_email == 'inactive':

                        msg = "Email Depreciated"
                        return render_template('login.html', msg=msg)
                    
                    elif row_status_email == 'active':
                        
                        cluster = Cluster(['192.168.1.236'], port=9042)
                        keyspace_connect = cluster.connect('accounts')
                        rows_email_password = keyspace_connect.execute("select password from loginemail where email='" + uname_email + "'")

                        keyspace_connect.shutdown()
                        cluster.shutdown()

                        row_password_email = []


                        for row in rows_email_password:
                            row_password_email.append(row.password)


                        row_password_email = jsonify(row_password_email)
                        row_password_email = str(row_password_email.data)
                        row_password_email = row_password_email[8:]
                        row_password_email = row_password_email[:-7]

                        if password == row_password_email:

                            cluster = Cluster(['192.168.1.236'], port=9042)
                            keyspace_connect = cluster.connect('accounts')
                            rows_email_password = keyspace_connect.execute("select * from loginemail where email='" + uname_email + "'")

                            keyspace_connect.shutdown()
                            cluster.shutdown()

                            row_email_email = []
                            row_email_username = []

                            for row in rows_email_password:
                                row_email_email.append(row.email)
                                row_email_username.append(row.username)


                            row_email_email = jsonify(row_email_email)
                            row_email_email = str(row_email_email.data)
                            row_email_email = row_email_email[8:]
                            row_email_email = row_email_email[:-7]
                            
                            row_email_username = jsonify(row_email_username)
                            row_email_username = str(row_email_username.data)
                            row_email_username = row_email_username[8:]
                            row_email_username = row_email_username[:-7]
                            
                            session['loggedin'] = True
                            session['id'] = row_email_email
                            session['username'] = row_email_username


                            return redirect(url_for('tutorial'))
                            #return render_template('tutorial.html', uname_email=uname_email, password=password)
                            #Start Session

                        else:

                            msg = "Incorrect Password"
                            return render_template('login.html', msg=msg)

            elif len(row_status_username) > 0:

                row_status_username = jsonify(row_status_username)
                row_status_username = str(row_status_username.data)
                row_status_username = row_status_username[8:]
                row_status_username = row_status_username[:-7]

                if row_status_username == 'inactive':

                        msg = "Username Depreciated"
                        return render_template('login.html', msg=msg)
                    
                elif row_status_username == 'active':
                        
                    cluster = Cluster(['192.168.1.236'], port=9042)
                    keyspace_connect = cluster.connect('accounts')
                    rows_username_password = keyspace_connect.execute("select password from loginusername where username='" + uname_email + "'")

                    keyspace_connect.shutdown()
                    cluster.shutdown()

                    row_password_username = []

                    for row in rows_username_password:
                        row_password_username.append(row.password)


                    row_password_username = jsonify(row_password_username)
                    row_password_username = str(row_password_username.data)
                    row_password_username = row_password_username[8:]
                    row_password_username = row_password_username[:-7]

                    if password == row_password_username:

                        cluster = Cluster(['192.168.1.236'], port=9042)
                        keyspace_connect = cluster.connect('accounts')
                        rows_username_password = keyspace_connect.execute("select * from loginusername where username='" + uname_email + "'")

                        keyspace_connect.shutdown()
                        cluster.shutdown()

                        row_username_email = []
                        row_username_username = []

                        for row in rows_username_password:
                            row_username_email.append(row.email)
                            row_username_username.append(row.username)


                        row_username_email = jsonify(row_username_email)
                        row_username_email = str(row_username_email.data)
                        row_username_email = row_username_email[8:]
                        row_username_email = row_username_email[:-7]
                         
                        row_username_username = jsonify(row_username_username)
                        row_username_username = str(row_username_username.data)
                        row_username_username = row_username_username[8:]
                        row_username_username = row_username_username[:-7]
                           
                        session['loggedin'] = True
                        session['id'] = row_username_email
                        session['username'] = row_username_username

                        return redirect(url_for('tutorial'))
                    
                    else:
                        
                        msg = "Incorrect Password"
                        return render_template('login.html', msg=msg)

        else:
            return render_template('login.html')
    else:
        return render_template('login.html')


####################### REGISTER PAGE ROUTE ###################

@app.route('/register', methods=['GET', 'POST'])
def register():
        if request.method == "POST":
            if request.form.get('homeButton') == 'backToHome':
                return render_template('index.html')
            else:
                return render_template('register.html')
        else:
            return render_template('register.html')

###################### TUTORIAL PAGE ROUTE ####################

@app.route('/tutorial', methods=['GET', 'POST'])
def tutorial():
    
    if 'loggedin' in session:

        cluster = Cluster(['192.168.1.236'], port=9042)
        keyspace_connect = cluster.connect('accounts')
        rows_email_data = keyspace_connect.execute("select * from loginemail where email='" + session['id'] + "'")

        keyspace_connect.shutdown()
        cluster.shutdown()

        row_email_username2 = []

        for row in rows_email_data:
            row_email_username2.append(row.username)

        row_email_username2 = jsonify(row_email_username2)
        row_email_username2 = str(row_email_username2.data)
        row_email_username2 = row_email_username2[8:]
        row_email_username2 = row_email_username2[:-7]

        return render_template('tutorial.html', row_email_username2=row_email_username2)

        if request.method == "POST":

            if request.form.get('logoutButton') == 'logout':

                session.pop('loggedin', None)
                session.pop('id', None)
                session.pop('username', None)
                
                return redirect(url_for('/'))
                #change this to logout session later
            
            elif request.form.get('tutorialButton') == 'tutorial':
                    
                    if 'loggedin' in session:
                        
                        cluster = Cluster(['192.168.1.236'], port=9042)
                        keyspace_connect = cluster.connect('accounts')
                        rows_email_data2 = keyspace_connect.execute("select * from loginemail where email='" + session['id'] + "'")

                        keyspace_connect.shutdown()
                        cluster.shutdown()

                        row_email_username3 = []

                        for row in rows_email_data2:
                            row_email_username3.append(row.username)

                        row_email_username3 = jsonify(row_email_username3)
                        row_email_username3 = str(row_email_username3.data)
                        row_email_username3 = row_email_username3[8:]
                        row_email_username3 = row_email_username3[:-7]

                        return render_template('tutorial.html', row_email_username3=row_email_username3)
            
            elif request.form.get('addRecordButton') == 'addRecord':
                return render_template('addRecords.html')

            elif request.form.get('checkRecordButton') == 'checkRecord':
                return render_template('checkRecords.html')

            elif request.form.get('dataPolicyButton') == 'dataPolicy':
                return render_template('dataPolicy.html')

            elif request.form.get('profileButton') == 'profile':
                return render_template('profile.html')

            else:
                return redirect(url_for('tutorial'))
        else:
            return redirect(url_for('tutorial'))

    else:
        return redirect(url_for('/'))



@app.route('/addrecords', methods=['GET', 'POST'])
def addrecord():
        if request.method == "POST":
            if request.form.get('logoutButton') == 'logout':
                return render_template('index.html')
                #change this to logout session later
            elif request.form.get('tutorialButton') == 'tutorial':
                return render_template('tutorial.html')
            elif request.form.get('addRecordButton') == 'addRecord':
                return render_template('addrecords.html')
            elif request.form.get('checkRecordButton') == 'checkRecord':
                return render_template('checkrecords.html')
            elif request.form.get('dataPolicyButton') == 'dataPolicy':
                return render_template('datapolicy.html')
            elif request.form.get('profileButton') == 'profile':
                return render_template('profile.html')
            #All other Elif Statements with Form Validation and Cassandra Input
            else:
                return render_template('addrecords.html')
        else:
            return render_template('addrecords.html')

@app.route('/checkrecords', methods=['GET', 'POST'])
def checkrecord():
        if request.method == "POST":
            if request.form.get('logoutButton') == 'logout':
                return render_template('index.html')
                #change this to logout session later
            elif request.form.get('tutorialButton') == 'tutorial':
                return render_template('tutorial.html')
            elif request.form.get('addRecordButton') == 'addRecord':
                return render_template('addrecords.html')
            elif request.form.get('checkRecordButton') == 'checkRecord':
                return render_template('checkrecords.html')
            elif request.form.get('dataPolicyButton') == 'dataPolicy':
                return render_template('datapolicy.html')
            elif request.form.get('profileButton') == 'profile':
                return render_template('profile.html')
            #All other Elif Statements with Form Validation and Cassandra Input
            else:
                return render_template('addrecords.html')
        else:
            return render_template('addrecords.html')

@app.route('/datapolicy', methods=['GET', 'POST'])
def datapolicy():
    if request.method == "POST":
        if request.form.get('logoutButton') == 'logout':
            return render_template('index.html')
            #change this to logout session later
        elif request.form.get('tutorialButton') == 'tutorial':
            return render_template('tutorial.html')
        elif request.form.get('addRecordButton') == 'addRecord':
            return render_template('addrecords.html')
        elif request.form.get('checkRecordButton') == 'checkRecord':
            return render_template('checkrecords.html')
        elif request.form.get('dataPolicyButton') == 'dataPolicy':
            return render_template('datapolicy.html')
        elif request.form.get('profileButton') == 'profile':
            return render_template('profile.html')
        #All other Elif Statements with Form Validation and Cassandra Input
        else:
            return render_template('addrecords.html')
    else:
        return render_template('addrecords.html')

@app.route('/profile', methods=['GET', 'POST'])
def profiley():
    if request.method == "POST":
        if request.form.get('logoutButton') == 'logout':
            return render_template('index.html')
            #change this to logout session later
        elif request.form.get('tutorialButton') == 'tutorial':
            return render_template('tutorial.html')
        elif request.form.get('addRecordButton') == 'addRecord':
            return render_template('addrecords.html')
        elif request.form.get('checkRecordButton') == 'checkRecord':
            return render_template('checkrecords.html')
        elif request.form.get('dataPolicyButton') == 'dataPolicy':
            return render_template('datapolicy.html')
        elif request.form.get('profileButton') == 'profile':
            return render_template('profile.html')
        #All other Elif Statements with Form Validation and Cassandra Input
        else:
            return render_template('profile.html')
    else:
        return render_template('profile.html')


if __name__ == '__main__':
    app.run(debug=True)