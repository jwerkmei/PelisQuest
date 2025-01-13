from flask import Flask, render_template, request, flash, jsonify, redirect, url_for
from flask_bootstrap import Bootstrap5
#from flask import Flask, render_template, request, redirect, url_for
from openai import OpenAI
from dotenv import load_dotenv
from db import db, db_config
from models import User, Message
from forms import ProfileForm, SignUpForm, LoginForm
from flask_wtf.csrf import CSRFProtect
from os import getenv
import json
import utiles
import re
from bot import search_movie_or_tv_show, where_to_watch, search_company
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from flask_bcrypt import Bcrypt

load_dotenv()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Inicia sesión para continuar'

client = OpenAI()
app = Flask(__name__)
app.secret_key = getenv('SECRET_KEY')
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)
login_manager.init_app(app)
bcrypt = Bcrypt(app)
db_config(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

tools = [
    {
        'type': 'function',
        'function': {
            "name": "where_to_watch",
            "description": "Returns a list of platforms where a specified movie can be watched.",
            "parameters": {
                "type": "object",
                "required": [
                    "name"
                ],
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the movie to search for"
                    }
                },
                "additionalProperties": False
            }
        },
    },
    {
        'type': 'function',
        'function': {
            "name": "search_movie_or_tv_show",
            "description": "Returns information about a specified movie or TV show.",
            "parameters": {
                "type": "object",
                "required": [
                    "name"
                ],
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the movie/tv show to search for"
                    }
                },
                "additionalProperties": False
            }
        },
    },
    {
        'type': 'function',
        'function': {
            "name": "search_company",
            "description": "Returns information about a company that produces a movie",
            "parameters": {
                "type": "object",
                "required": [
                    "name"
                ],
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the company that produces a movie"
                    }
                },
                "additionalProperties": False
            }
        },
    }
]

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    user = db.session.query(User).get(current_user.id)
    nombre = user.nombre or ""
    user_id  = user.id
    generos_preferidos = user.generos_preferidos or ""
    peliculas_favoritas = user.peliculas_favoritas or ""
    directores_favoritos = user.directores_favoritos or ""

    # print(f"El metodo es:{request.method}")
    # print(f"Mensaje recibido: {request.form.get('message')}")
    

    if request.method == 'GET':
        return render_template('chat.html', messages=user.messages, nombre=nombre, generos_preferidos=generos_preferidos, peliculas_favoritas=peliculas_favoritas, directores_favoritos=directores_favoritos, user_id=user_id)

    #intent = request.form.get('intent')

    # Capturar el mensaje del usuario o el valor del botón
    user_message = request.form.get('message')

    if not user_message:  # Si no hay mensaje capturado
        return jsonify({'error': 'No se recibió ningún mensaje'}), 400
   
    #if user_message == "":
    #    user_message = intent

    # Guardar nuevo mensaje en la BD
    db.session.add(Message(content=user_message, author="user", user=user))
    db.session.commit()

    messages_for_llm = [{
        "role": "system",
        "content": f'''
                    Eres PeliQuest, un chatbot experto en cine, creado para recomendar películas a cinéfilos y profesionales del cine. 
                    Debes proporcionar recomendaciones de manera breve, concisa y especializada, sin repetir nunca las sugerencias. 
                    Debes recordar el nombre del usuario ({nombre}), sus géneros preferidos ({generos_preferidos}), 
                    sus peliculas favoritas ({peliculas_favoritas}) y sus directores favoritos ({directores_favoritos}) todo el tiempo.
                    Si vienen links retornalos siempre.
                    Si vienen direcciones a imagenes retornalas siempre.
                    Si te preguntan o solicitan el trailer de una pelicula tienes que ir a buscar y usar la información a TMDB. 
                    Si te preguntan o solicitan películas similares tienes que ir a buscar y usar la información a TMDB. 
                    Si te preguntan por popularidad la popularidad de una pelicula tienes que ir a buscar y usar la información a TMDB.
                    ''',
    }]

    for message in user.messages:
        messages_for_llm.append({
            "role": message.author,
            "content": message.content,
        })

    chat_completion = client.chat.completions.create(
        messages=messages_for_llm,
        model="gpt-4o",
        temperature=1,
        tools=tools,
    )

    if chat_completion.choices[0].message.tool_calls:
        tool_call = chat_completion.choices[0].message.tool_calls[0]
        print(f"tool_call: {tool_call}")
        if tool_call.function.name == 'where_to_watch':
            arguments = json.loads(tool_call.function.arguments)
            # Muchas veces viene el año despues de la pelicula, se ha notado que cuando viene el año no encuentra nada 
            # (o puede venir "de AÑO"), asi que lo removemos antes de la llamada
            nombre = re.sub(r'\s*(de\s*)?\b\d{4}\b$', '', arguments['name'], flags=re.IGNORECASE).strip()
            #name = arguments['name']
            model_recommendation = where_to_watch(client, nombre, user)
            print(model_recommendation)
            model_recommendation = utiles.convertir_html(model_recommendation)

        elif tool_call.function.name == 'search_movie_or_tv_show':
            arguments = json.loads(tool_call.function.arguments)
            nombre = re.sub(r'\s*(de\s*)?\b\d{4}\b$', '', arguments['name'], flags=re.IGNORECASE).strip()
            #name = arguments['name']
            model_recommendation = search_movie_or_tv_show(client, nombre, user)
            model_recommendation = utiles.convertir_html(model_recommendation)

        elif tool_call.function.name == 'search_company':
            arguments = json.loads(tool_call.function.arguments)
            name = arguments['name']
            model_recommendation = search_company(client, name, user)
            model_recommendation = utiles.convertir_html(model_recommendation)

    else:
        model_recommendation = chat_completion.choices[0].message.content


    db.session.add(Message(content=model_recommendation, author="assistant", user=user))
    db.session.commit()

    accept_header = request.headers.get('Accept')
    if accept_header and 'application/json' in accept_header:
        last_message = user.messages[-1]
        return jsonify({
            'author': last_message.author,
            'content': last_message.content,
        })
    
    return render_template('chat.html', messages=user.messages, nombre=nombre, generos_preferidos=generos_preferidos, peliculas_favoritas=peliculas_favoritas, directores_favoritos=directores_favoritos, user_id=user_id)


@app.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    user = db.session.query(User).get(current_user.id)
    form = ProfileForm(obj=user)

    if request.method == 'POST':
        if form.validate_on_submit():
            user.nombre = form.nombre.data
            user.email = form.email.data
            user.generos_preferidos = form.generos_preferidos.data
            user.peliculas_favoritas = form.peliculas_favoritas.data
            user.directores_favoritos = form.directores_favoritos.data
            db.session.commit()

            # Agregar un mensaje flash
            flash('Tus datos han sido actualizados correctamente.', 'success')

            # Redireccionar para evitar reenvíos de formulario
            return redirect(url_for('perfil'))

    return render_template('perfil.html', form=form)


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            nombre = form.nombre.data
            password = form.password.data
            user = User(email=email, nombre=nombre, password_hash=bcrypt.generate_password_hash(password).decode('utf-8'))
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('chat'))
    return render_template('sign-up.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = db.session.query(User).filter_by(email=email).first()
            if user and bcrypt.check_password_hash(user.password_hash, password):
                login_user(user)
                return redirect('chat')

            flash("El correo o la contraseña es incorrecta.", "error")

    return render_template('log-in.html', form=form)


@app.get('/logout')
def logout():
    logout_user()
    return redirect('/')
