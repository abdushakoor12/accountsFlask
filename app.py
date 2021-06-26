import re
import json
import logging
from cassandra.cluster import Cluster
from flask import Flask, render_template, url_for, request, redirect, session, Response, jsonify


app = Flask(__name__)

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
                            return render_template('tutorial.html', uname_email=uname_email, password=password)
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
                        
                        return render_template('tutorial.html', uname_email=uname_email, password=password)
                        #Start Session 
                    
                    else:
                        
                        msg = "Incorrect Password"
                        return render_template('login.html', msg=msg)

        else:
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
        if request.method == "POST":
            if request.form.get('homeButton') == 'backToHome':
                return render_template('index.html')
            else:
                return render_template('register.html')
        else:
            return render_template('register.html')

@app.route('/tutorial', methods=['GET', 'POST'])
def tutorial():
    if request.method == "POST":
        if request.form.get('logoutButton') == 'logout':
            return render_template('index.html')
            #change this to logout session later
        elif request.form.get('tutorialButton') == 'tutorial':
            return render_template('tutorial.html')
        elif request.form.get('addRecordButton') == 'addRecord':
            return render_template('addRecords.html')
        elif request.form.get('checkRecordButton') == 'checkRecord':
            return render_template('checkRecords.html')
        elif request.form.get('dataPolicyButton') == 'dataPolicy':
            return render_template('dataPolicy.html')
        else:
            return render_template('tutorial.html')
    else:
        return render_template('tutorial.html')


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
        #All other Elif Statements with Form Validation and Cassandra Input
        else:
            return render_template('addrecords.html')
    else:
        return render_template('addrecords.html')


if __name__ == '__main__':
    app.run(debug=True)