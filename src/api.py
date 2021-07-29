import os
import requests


class Apis:
    api_key = os.environ.get("SLACK_BOT_TOKEN")

    @staticmethod
    def get_movie_details(movie_id, language):
        params = {
            'api_key': Apis.api_key,
            'language': language
        }
        r = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}', params)
