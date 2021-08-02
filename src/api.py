import sys
sys.path.insert(1, "lib/")
# This going against PEP-8 will refactor once we have a build pipeline
import os
import json
import logging
import requests
import cachetools.func


class MovieApis:
    api_key = os.environ.get("API_KEY")

    # instance method
    @cachetools.func.ttl_cache(maxsize=20, ttl=300)
    def get_movie_details(movie_id: str, region: str) -> dict:
        params = {
            "api_key": MovieApis.api_key,
            "region": region
        }
        try:
            r = requests.get(
                f"https://api.themoviedb.org/3/movie/{movie_id}", params)
            r.raise_for_status()
        except Exception as e:
            logging.exception(f"Error getting movie details: {e}")

        data = json.loads(r.text)

        return data

    # instance method
    @cachetools.func.ttl_cache(maxsize=5, ttl=300)
    def get_list_of_movies(pages: int) -> list:
        movie_list = []
        params = {
            "api_key": MovieApis.api_key,
            "region": "US",
            "page": []
        }
        for pages in range(pages):
            params["page"].append(pages + 1)
            try:
                r = requests.get(
                    "https://api.themoviedb.org/3/movie/now_playing", params)
                r.raise_for_status()
            except requests.exceptions.RequestException as e:
                logging.exception(f"Error getting list of movies: {e}")
            data = json.loads(r.text)
            for item in data["results"]:
                movie = {
                    "text": {
                        "type": "plain_text",
                        "text": item["original_title"]
                    },
                    "value": str(item["id"])
                }

                movie_list.append(movie)
        return movie_list


# Start your app
if __name__ == "__main__":
    MovieApis.get_list_of_movies("en-US", 3)
