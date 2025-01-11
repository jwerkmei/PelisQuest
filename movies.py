from simplejustwatchapi.justwatch import search as justwatch_search
import tmdbsimple as tmdb
from dotenv import load_dotenv
from os import getenv

load_dotenv()
tmdb.API_KEY = getenv('TMDB_API_KEY')
tmdb.REQUESTS_TIMEOUT = 5 

#Usa TMDB
def search(movie_name):
    search = tmdb.Search()
    print("antes de buscar en TMDB")
    response = search.multi(query=movie_name, language='es-CL')
    print("despues de buscar en TMDB")

    if not search.results:
        return None
    print(f"resultados: {search.results[0]}")
    return search.results[0]

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
