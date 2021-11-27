from flask import render_template, request, redirect, url_for
import requests
from app import app
from .forms import LoginForm, RegisterForm, PokemonForm
from .models import User
from flask_login import login_user, logout_user, current_user, login_required

@app.route("/")
def index():
    return render_template('index.html.j2')

@app.route('/pokemon', methods=['GET', 'POST'])
@login_required
def pokemon():  #what appears on navbar
    form= PokemonForm()
    if request.method== 'POST':
        pokemon = request.form.get('pokemon')
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
        response = requests.get(url)
        if response.ok:  ##means it worked
            if not response.json():
                return "We had an error loading your data, please try again"
            data = response.json()
            my_pokemon=[]
            for pokemon in data:
                pokemon_dict= {
                "name": data["forms"][0]["name"],
                "ability_name": data["abilities"][0]["ability"]["name"],
                "base_experience": data["base_experience"],
                'sprite': data["sprites"]["front_shiny"],
                }
            my_pokemon.append(pokemon_dict)
            print(my_pokemon)
            return render_template("pokemon.html.j2", pokemons=my_pokemon)     
        else:
            return "Please try your search again"

    return render_template("pokemon.html.j2")

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data={
                "first_name": form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email": form.email.data.lower(),
                "password": form.password.data
            }
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
        except:
            error_string="There was a problem creating your account. Please try again"
            return render_template('register.html.j2',form=form, error=error_string)
        return redirect(url_for('login'))

    return render_template('register.html.j2',form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        u = User.query.filter_by(email=email).first()
        print(u)
        # if u is not None and u.check_hashed_password(password):
        #     login_user(u)
        #     return redirect(url_for('pokemon'))
        # else:
        return redirect(url_for('pokemon'))
    return render_template("login.html.j2", form=form)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user is not None:
        logout_user()
        return redirect(url_for('login'))