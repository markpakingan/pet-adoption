from flask import Flask, render_template, flash, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

# from forms import AddSnackForm
# from forms import UserForm

app = Flask(__name__)
app.app_context().push()


app.config["SECRET_KEY"] = "oh-so-secret"

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///pet_adoption"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()


@app.route("/")
def homepage():
    """Shows name, photo, availability"""
    pets = Pet.query.all()
    return render_template("index.html", pets = pets)


# @app.route("/add", methods = ["GET"])
# def show_new_pet_form():
#     """show forms for adding a pet"""
#     return render_template("add_new_pet.html")



# @app.route("/add", methods = ["POST"])
# def add_new_pets():
#     """show forms for adding a pet"""
    
#     new_pet = Pet(
#     name = request.form["pet_name"], 
#     species = request.form["species"],
#     photo_url = request.form["photo_url"],
#     age = request.form["age"],
#     notes = request.form["notes"])


#     db.session.add(new_pet)
#     db.session.commit()

#     return redirect ("/add")



@app.route("/add", methods = ["GET", "POST"])
def add_pet():

    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.age.data

        pet = Pet(name = name, species = species, photo_url = photo_url, age = age, notes = notes)
        db.session.add(pet)
        db.session.commit()

        flash(f" Created a new pet: name is {name}, species is {species}")
        return redirect("/")
    
    else: 
        return render_template("add_new_pet.html", form = form)


@app.route("/<int:pet_id>", methods = ["GET", "POST"])
def edit_pet(pet_id):
     """Edit Pet"""

     pet = Pet.query.get_or_404(pet_id)
     form = EditPetForm(obj = pet)

     if form.validate_on_submit():
         pet.notes = form.notes.data
         pet.available = form.available.data
         pet.photo_url = form.photo_url.data

         db.session.commit()
         flash(f"{pet.name} updated")
         return redirect("/")
     
     else: 
         return render_template("pet_edit_form.html", form=form, pet=pet)
     

# @app.route("/api/pets/<int:pet_id>", methods=['GET'])
# def api_get_pet(pet_id):
#     """Return basic info about pet in JSON."""

#     pet = Pet.query.get_or_404(pet_id)
#     info = {"name": pet.name, "age": pet.age}

#     return jsonify(info)