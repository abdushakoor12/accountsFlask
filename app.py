from flask import Flask, render_template, url_for, request

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