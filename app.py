from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
import forms as f

from models import db, Alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.route("/")
@app.route("/index")
def index():
	create_form = f.UserForm2(request.form)
	alumnos = Alumnos.query.all() # SELECT * FROM alumnos

	return render_template("index.html", form=create_form, alumnos=alumnos), 404

@app.route("/detalles", methods=['GET','POST'])
def alumnoDetalle():
	create_form = f.UserForm2(request.form)
	if request.method == 'GET':
		id=request.args.get('id')
		alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
		print(alum1)
		nom = alum1.nombre
		apaterno = alum1.apaterno
		email = alum1.email

	return render_template("detalles.html", form=create_form, nombre=nom, apellido=apaterno, email=email)

@app.route("/crear", methods=['GET', 'POST'])
def crear():
	create_form = f.UserForm2(request.form)
	if request.method == "POST":
		alum = Alumnos(
			nombre=create_form.nombre.data,
			apaterno=create_form.apaterno.data,
			email = create_form.email.data
		)
		db.session.add(alum)
		db.session.commit()
		return redirect(url_for("index"))
	return render_template("crear.html", form=create_form)
	

if __name__ == '__main__':
	csrf.init_app(app)
	db.init_app(app)
	with app.app_context():
		db.create_all()
	app.run()

