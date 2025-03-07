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
	alumnos = Alumnos.query.all()

	return render_template("index.html", form=create_form, alumnos=alumnos)

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

@app.route("/registro", methods=["GET", "POST"])
def registro():
    form = f.UserForm2(request.form)
    
    if request.method == 'POST':
        print(f"Nombre: {form.nombre.data}, Apellido: {form.apaterno.data}, Email: {form.email.data}")

        # Agrega el ID por defecto
        if not form.id.data:
            form.id.data = 1

        if form.validate():
            nombre = form.nombre.data
            apaterno = form.apaterno.data
            email = form.email.data

            alumno = Alumnos(
                nombre=nombre,
                apaterno=apaterno,
                email=email
            )

            db.session.add(alumno)
            db.session.commit()
            
            return redirect(url_for("index"))
        else:
            print("El formulario no pasó la validación:", form.errors)

    return render_template("registro.html", form=form)

@app.route("/eliminar", methods=["GET"])
def eliminar():
    id_usuario = request.args.get("id")
    confirmed = request.args.get("confirmed")

    if not id_usuario:
        flash("ID no proporcionado", "danger")
        return redirect(url_for("index"))
    
    # Buscar usuario en la BD
    usuario = Alumnos.query.get(id_usuario)

    if not usuario:
        return redirect(url_for("index"))

    if confirmed == "1":
        db.session.delete(usuario)
        db.session.commit()
        return redirect(url_for("index"))

    if confirmed == "0":
        return redirect(url_for("index"))

    return render_template("eliminar.html", usuario=usuario)

@app.route("/editar", methods=["GET", "POST"])
def editar():
    id_usuario = request.args.get("id")

    if not id_usuario:
        return redirect(url_for("index"))

    alumno = Alumnos.query.get(id_usuario)

    if not alumno:
        return redirect(url_for("index"))

    form = f.UserForm2(request.form)

    # GET
    if request.method == "GET":
        form.id.data = alumno.id
        form.nombre.data = alumno.nombre
        form.apaterno.data = alumno.apaterno
        form.email.data = alumno.email

    # POST
    if request.method == "POST" and form.validate():
        alumno.nombre = form.nombre.data
        alumno.apaterno = form.apaterno.data
        alumno.email = form.email.data

        db.session.commit()
        return redirect(url_for("index"))

    return render_template("editar.html", form=form)

if __name__ == '__main__':
	csrf.init_app(app)
	db.init_app(app)
	with app.app_context():
		db.create_all()
	app.run()

