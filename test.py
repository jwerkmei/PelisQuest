import requests
from os import getenv
from dotenv import load_dotenv

load_dotenv()


def get_trailer_link(id_movie):
    print(f"id_movie: {id_movie}")
    api_key=getenv('TMDB_API_KEY')
    print(f"api_key: {api_key}")

    # Define la URL y los encabezados
    url = f'https://api.themoviedb.org/3/movie/{id_movie}/videos?api_key={api_key}&language=en-US'
    print(f"url: {url}")
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2Y2Y4NGM0ODA5MzU2NTMxMTk4ZjJhZTZlZTMwOTFkMiIsIm5iZiI6MTczNjQ2Mzc1My4wOSwic3ViIjoiNjc4MDU1ODk3NzMyMjA5ZTE3YmI0NGNlIiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9.qFMDv2F_RXZcMARtl6se-_Hvsd3yYRAdtJYnSgMA4dM',
        'accept': 'application/json',
        'api_key': api_key
    }

    # headers = {
    #     #'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2Y2Y4NGM0ODA5MzU2NTMxMTk4ZjJhZTZlZTMwOTFkMiIsIm5iZiI6MTczNjQ2Mzc1My4wOSwic3ViIjoiNjc4MDU1ODk3NzMyMjA5ZTE3YmI0NGNlIiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9.qFMDv2F_RXZcMARtl6se-_Hvsd3yYRAdtJYnSgMA4dM',
    #     'accept': 'application/json'
    # }

    # Realiza la solicitud GET
    response = requests.get(url, headers=headers)
    #response = requests.get(url)
    print(f"response.json():{response.json()}")

    link=''
    # Comprueba si la solicitud fue exitosa
    if response.status_code == 200:
        # Convierte la respuesta en formato JSON
        data = response.json()
        print(data)
        for video in data['results']:
            if video['type'] == 'Trailer' and video['official'] == True and video['site'] == 'YouTube':
                link = f"https://www.youtube.com/watch?v={video['key']}"
                print(link)
                break 
    #else:
    #    print(f'Error {response.status_code}: {response.text}')
    return link

print(get_trailer_link(762509))