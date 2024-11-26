import requests
from content_manager import Content
import csv
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()
# API to TMDb
API_KEY = os.getenv('API_KEY')


def get_geners(content_type: str, language_code="en") -> dict:
    """
    Function to get list of the genres and their ID
    EXAMPLE: get_movies_geners("tv"/"movie", "he"/"en"/NONE(default=en))
    """
    url = f"https://api.themoviedb.org/3/genre/{content_type}/list?language={language_code}&api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    # Transform the data into clean dict by id keys and name values
    new_dict = {var["id"]: var["name"] for var in data["genres"]}
    return new_dict


def get_genre_type(genre_id: int) -> str:
    """
    Check genre if for tv, movie or both
    """
    genre_dict_movies = get_geners("movie")
    genre_dict_tv = get_geners("tv")
    if (genre_id in genre_dict_movies) and (genre_id in genre_dict_tv):
        return "both"
    elif genre_id in genre_dict_movies:
        return "movie"
    elif genre_id in genre_dict_tv:
        return "tv"
    else:
        return "ERROR: not existing genre id"


def get_tvshows_onair(from_page=1, to_page=1, language_code="en") -> list:
    """
    Function to get the most popular tv shows that are still on-air
    EXAMPLE: get_tvshows_onair(pages=(how many pages of shows you want to get),
    language_code=(lang code like "he" or "en"))
    """
    returned_list = []
    for page in range(from_page, to_page + 1):
        url = f"https://api.themoviedb.org/3/tv/on_the_air?language=en-US&page=1" \
              f"&api_key={API_KEY}&with_original_language={language_code}&page={page}"
        response = requests.get(url)
        data = response.json()
        shows = data["results"]
        us_air = [var for var in shows if (var["original_language"] == "en" or var["original_language"] == "he")]
        returned_list.extend(us_air)

    return convert_into_content_list(returned_list, "tv", "onair")


def get_popular_tvshows(from_page=1, to_page=1, language_code="en") -> list:
    """
    Function to get the most popular tv shows
    EXAMPLE: get_tvshows(pages=(how many pages of shows you want to get),
    language_code=(lang code like "he" or "en")
    """
    returned_list = []
    for page in range(from_page, to_page + 1):

        url = f"https://api.themoviedb.org/3/discover/tv?include_adult=true" \
              f"&include_null_first_air_dates=false&language=en-US&page={page}" \
              f"&sort_by=popularity.desc&with_original_language={language_code}&api_key={API_KEY}"
        response = requests.get(url)
        data = response.json()
        shows = data["results"]
        # us_shows = [var for var in shows if var["original_language"] == "en"]
        returned_list.extend(shows)

    return convert_into_content_list(returned_list, "tv", "popular")


def get_popular_movies(from_page=1, to_page=1, language_code="en"):
    """
        Function to get the most popular movies
        EXAMPLE: get_movies(pages=(how many pages of shows you want to get),
        language_code=(lang code like "he" or "en")
    """
    returned_list = []
    for page in range(from_page, to_page + 1):
        url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&" \
              f"include_video=false&language=en-US&page={page}&sort_by=popularity.desc&" \
              f"with_original_language={language_code}&api_key={API_KEY}"
        response = requests.get(url)
        data = response.json()
        movies = data["results"]
        returned_list.extend(movies)

    return convert_into_content_list(returned_list, "movie", "popular")


def get_rated_content(content_type: str, from_page=1, to_page=1, language_code="en") -> list:
    """
    Function to get the most rated content
    EXAMPLE: get_rated_content(content_type=(movie/tv), pages=(how many pages of shows you want to get),
     language_code=(lang code like "he" or "en")
    """
    min_votes = 5000
    if language_code != "en":
        min_votes = 100
    returned_list = []
    for page in range(from_page, to_page + 1):
        url = f"https://api.themoviedb.org/3/discover/{content_type}?api_key={API_KEY}" \
              f"&sort_by=vote_average.desc&vote_count.gte={min_votes}&" \
              f"with_original_language={language_code}&page={page}"
        response = requests.get(url)
        data = response.json()
        print(data)
        movies = data["results"]
        returned_list.extend(movies)

    return convert_into_content_list(returned_list, content_type, "rated")


def get_poster(content: Content, saving_file="images", width=500) -> str:
    """
    Function to download the content poster and return his path.
    EXAMPLE: get_poster(poster_path(of the content),original_name(name of the content),
    saving_file(default name- images),width(default 500))
    """
    poster_path = content.info["poster_path"]
    original_name = content.info["title"]

    img_url = f'https://image.tmdb.org/t/p/w{width}{poster_path}'
    img_data = requests.get(img_url).content

    # Downloading and saving show poter
    with open(f'./{saving_file}/{original_name}.jpg', 'wb') as image_file:
        image_file.write(img_data)

    return f'{saving_file}/{original_name}.jpg'


def get_content_by_genre(content_type: str, genres: set, from_page=1, to_page=1, language_code="en"):
    # transform set into string
    genres_str = ",".join(str(genre_id) for genre_id in genres)

    returned_list = []
    for page in range(from_page, to_page + 1):
        url = f"https://api.themoviedb.org/3/discover/{content_type}?api_key={API_KEY}&with_genres={genres_str}&" \
              f"with_original_language={language_code}&page={page}&sort_by=popularity.desc"
        response = requests.get(url)
        data = response.json()
        content = data["results"]
        returned_list.extend(content)

    return convert_into_content_list(returned_list, content_type, "by_genre")


def get_cast_and_crew(content_dict: dict, content_type: str) -> dict:
    """
    Function to get the cast and the crew of the movie.
    return in dict which have the keys: "cast" (Actors)
    and "crew" (Production team)
    """
    url = f'https://api.themoviedb.org/3/{content_type}/{content_dict["id"]}/credits?api_key={API_KEY}'
    response = requests.get(url)
    return response.json()


def convert_into_content_list(list_to_convert: list, content_type: str, content_origin: str) -> list:
    """
    Convert list of content (movie or show) into uniform object: Content
    """
    new_content_list = [Content(content_type, content_origin, var, get_cast_and_crew(var, content_type)) for var in
                        list_to_convert]
    return new_content_list

def get_available_langs():
    csv_file_path = "sources/language_codes.csv"

    languages = []
    with open(csv_file_path, mode="r", newline="") as file:
        reader = csv.reader(file)
        next(reader)  # דילוג על כותרת העמודות
        for row in reader:
                languages.append(row[0])  # קריאת עמודת השפות
    return languages

def get_lang_code(lang_name: str):
    csv_file_path = "sources/language_codes.csv"

    languages = {}
    with open(csv_file_path, mode="r", newline="") as file:
        reader = csv.reader(file)
        next(reader)  # דילוג על כותרת העמודות
        for row in reader:
                languages[row[0]] = row[1]  # קריאת עמודת השפות

    return languages[lang_name]


