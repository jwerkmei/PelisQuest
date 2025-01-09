from db import db
from app import app
from models import User, Message

with app.app_context():
    db.create_all()
    
    user = User(email="test@example.org",nombre="Eugenio",generos_preferidos="Ciencia ficcion, Romance, Historico",peliculas_favoritas="Blade Runner,Orgullo y Prejuicio, Napoleon",directores_favoritos="Martin Scorsese, Quentin Tarantino, Maite Alberdi")
    message = Message(content="Hola! Soy PeliQuest, un recomendador de películas. ¿En qué te puedo ayudar?", author="assistant", user=user)

    db.session.add(user)
    db.session.add(message)
    db.session.commit()

    print("Usuario y Mensaje creado!")