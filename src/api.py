import os
import requests
import requests_cache
import json


class MovieApis:
    api_key = os.environ.get("API_KEY")
    requests_cache.install_cache(
        "movie_cache", backend="sqlite", expire_after=360)

    @staticmethod
    def get_movie_details(movie_id, region):
        params = {
            "api_key": MovieApis.api_key,
            "region": region
        }
        r = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}", params)
        data = json.loads(r.text)

        return data

    @staticmethod
    def get_list_of_movies(pages):
        movie_list = []
        params = {
            "api_key": MovieApis.api_key,
            "region": "US",
            "page": []
        }
        for pages in range(pages):
            params["page"].append(pages + 1)
            r = requests.get(
                "https://api.themoviedb.org/3/movie/now_playing", params)
            data = json.loads(r.text)
            for item in data["results"]:
                movie = {"text": {"type": "plain_text",
                                  "text": item["original_title"]}, "value": str(item["id"])}
                movie_list.append(movie)
        return movie_list


# Start your app
if __name__ == "__main__":
    MovieApis.get_list_of_movies("en-US", 3)
