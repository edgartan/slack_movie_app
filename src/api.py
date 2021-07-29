import os
import requests
import json


class MovieApis:
    api_key = os.environ.get("API_KEY")

    @staticmethod
    def get_movie_details(movie_id, language):
        params = {
            'api_key': MovieApis.api_key,
            'language': language
        }
        r = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}', params)

    @staticmethod
    def get_list_of_movies(language, pages):
        movie_list = []
        params = {
            'api_key': MovieApis.api_key,
            'language': language,
            'page': []
        }
        for pages in range(pages):
            params['page'].append(pages + 1)
            r = requests.get(
                'https://api.themoviedb.org/3/movie/popular', params)
            data = json.loads(r.text)
            for item in data['results']:
                movie = {'text': {'type': 'plain_text',
                                  'text': item['original_title']}, 'value': str(item['id'])}
                movie_list.append(movie)
        return movie_list


# # Start your app
# if __name__ == "__main__":
#     MovieApis.get_list_of_movies('en-US', 3)
