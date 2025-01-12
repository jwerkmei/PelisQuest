from simplejustwatchapi.justwatch import search as justwatch_search
import tmdbsimple as tmdb
from dotenv import load_dotenv
from os import getenv
import requests

load_dotenv()
tmdb.API_KEY = getenv('TMDB_API_KEY')
tmdb.REQUESTS_TIMEOUT = 5 

def get_trailer_link(id_movie):
    #print(f"id_movie (llamada): {id_movie}")
    api_key=getenv('TMDB_API_KEY')
    # Define la URL y los encabezados
    url = f'https://api.themoviedb.org/3/movie/{id_movie}/videos?language=en-US'
    #print(f"URL: https://api.themoviedb.org/3/movie/{id_movie}/videos?language=en-US")
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2Y2Y4NGM0ODA5MzU2NTMxMTk4ZjJhZTZlZTMwOTFkMiIsIm5iZiI6MTczNjQ2Mzc1My4wOSwic3ViIjoiNjc4MDU1ODk3NzMyMjA5ZTE3YmI0NGNlIiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9.qFMDv2F_RXZcMARtl6se-_Hvsd3yYRAdtJYnSgMA4dM',
        'accept': 'application/json',
        'api_key': api_key
    }

    response = requests.get(url, headers=headers)
    link=''

    # Comprueba si la solicitud fue exitosa
    if response.status_code == 200:
        # Convierte la respuesta en formato JSON
        data = response.json()
        #print(f"data: {data}")
        #se obtiene el link al trailer
        for video in data['results']:
            if video['type'] == 'Trailer' and video['official'] == True and video['site'] == 'YouTube':
                link = f"https://www.youtube.com/watch?v={video['key']}"
                #print(link)
                break 
    return link
    #else:
    #    print(f'Error {response.status_code}: {response.text}')


#Usa TMDB
def search(movie_name):
    search = tmdb.Search()
    print("antes de buscar en TMDB")
    response = search.multi(query=movie_name, language='es-CL')
    print("despues de buscar en TMDB")

    if not search.results:
        return None
    movie_info=search.results[0]
    print(f"resultados antes: {movie_info}")

    print(f"El id de la pelicula es: {movie_info['id']}")
    trailer_link=get_trailer_link(movie_info['id'])
    #print(f"trailer_link: {trailer_link}")
    #agregamos el link del trailer al diccionario
    movie_info['trailer_link'] = trailer_link
    print(f"resultados post: {movie_info}")

    return movie_info

#Usa TMDB
def s_company(company):
    search = tmdb.Search()
    print("antes de buscar en TMDB")
    response = search.company(query=company, language='es-CL')
    print("despues de buscar en TMDB")

    if not search.results:
        return None
    print(f"resultados: {search.results[0]}")
    return search.results[0]

#Usa JUSTWATCH
def search_platforms(movie_name):
    results = justwatch_search(movie_name, "CL", "es")
    platforms = []

    if not results:
        return platforms

    for offer in results[0].offers:
        platforms.append({
            'name': offer.package.name,
            'icon': offer.package.icon,
            'url': offer.url,
        })

    print(f"platforms: {platforms}")
    return platforms
