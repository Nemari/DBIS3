from flask import Flask, url_for,request, send_from_directory, render_template,redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lnjmefvkshluwp:71617a7e25a670c39a8208dbced78b6e23822d2645c4fba4c5e3aa08cfa10367@ec2-54-74-35-87.eu-west-1.compute.amazonaws.com:5432/d3ok4qpdejtavb'
db = SQLAlchemy(app)

class Company(db.Model):
	__tablename__ = 'company'
	name = db.Column(db.String(50), primary_key=True, nullable=False)
	company = db.relationship('Games')



class Games(db.Model):
	__tablename__ = 'games'
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	name = db.Column(db.String(50), unique=True, nullable=False)
	rating = db.Column(db.Integer)
	year = db.Column(db.Integer)
	company = db.Column(db.String(50),db.ForeignKey('company.name'))

db.create_all()

@app.route('/<table>/', methods=['post'])
def add(table):
	if table == "Games":
		new_id = request.form.get('new_id')
		name = request.form.get('name')
		rating = request.form.get('rating')
		year = request.form.get('year')
		company = request.form.get('company')

		new = Games(id = new_id, name = name, rating = rating, year = year, company = company)
	elif table == "Company":
		name = request.form.get('name')
		new = Company(name = name)
	try:
		db.session.add(new)
		db.session.commit()
	except Exception:
		if table == "Games":
			return redirect(url_for('show_games'))
		elif table == "Company":
			return redirect(url_for('show_company'))
	if table == "Games":
		return redirect(url_for('show_games'))
	elif table == "Company":
		return redirect(url_for('show_company'))

@app.route('/<table>/Update', methods=['post'])
def update(table):
	if table == "Games":
		name = request.form.get('Name')
		rating = request.form.get('Rating')
		year = request.form.get('Year')
		company = request.form.get('Company')
		new_id = request.form.get('Id')
		new = db.session.query(Games).get(new_id)
		new.name = name
		new.rating = rating
		new.year = year
		new.company = company
	try:
		db.session.commit()
	except Exception:
		if table == "Games":
			return redirect(url_for('show_games'))
		elif table == "Company":
			return redirect(url_for('show_company'))
	if table == "Games":
		return redirect(url_for('show_games'))
	elif table == "Company":
		return redirect(url_for('show_company'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/templates/<path:path>')
def send_js(path):
    return send_from_directory('templates', path)

@app.route('/Games')
def show_games():
	data = Games.query.all()
	return render_template('index.html', data=data,table="Games")

@app.route('/Company')
def show_company():
	data = Company.query.all()
	return render_template('index_company.html', data=data,table="Company")

@app.route('/<table>/delete/<name>')
def delete(table,name):
	if table == "Games":
		data = Games.query.all()
	elif table == "Company":
		data = Company.query.all()
	else:
		return redirect(url_for('index'))
	for d in data:
		if d.name == name:
			db.session.delete(d)
			db.session.commit()
	if table == "Games":
		return redirect(url_for('show_games'))
	elif table == "Company":
		return redirect(url_for('show_company'))
	else:
		return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
