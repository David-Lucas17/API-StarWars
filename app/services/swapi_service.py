import requests
from functools import lru_cache
import time

BASE_URL = "https://swapi.dev/api"

@lru_cache(maxsize=128)
def cached_fetch(url, params=None):
    """Cache para evitar chamadas repetidas à SWAPI"""
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def fetch_data(resource, search=None, page=None):
    """Busca dados da SWAPI com suporte a paginação"""
    url = f"{BASE_URL}/{resource}/"
    params = {}
    
    if search:
        params["search"] = search
    if page:
        params["page"] = page
    
    cache_key = (url, tuple(sorted(params.items())) if params else None)
    data = cached_fetch(cache_key[0], cache_key[1])
    return data

def fetch_all_data(resource, search=None):
    """Busca TODOS os dados paginados da SWAPI"""
    all_results = []
    page = 1
    
    while True:
        try:
            data = fetch_data(resource, search, page)
            results = data.get("results", [])
            all_results.extend(results)
            
            if data.get("next"):
                page += 1
                time.sleep(0.1) 
            else:
                break
        except requests.exceptions.RequestException:
            break
    
    return all_results

def fetch_film_characters(film_id):
    """Busca todos os personagens de um filme"""
    film_url = f"{BASE_URL}/films/{film_id}/"
    
    try:
        film_data = cached_fetch(film_url)
        characters_urls = film_data.get("characters", [])
        
        characters = []
        for url in characters_urls:
            char_data = cached_fetch(url)
            characters.append(char_data)
        
        return characters
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError(f"Film with id {film_id} not found")
        raise