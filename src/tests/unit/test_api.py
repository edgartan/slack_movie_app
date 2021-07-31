import os
from unittest import TestCase
from unittest.mock import patch
from faker import Faker
from api import MovieApis


class TestApp(TestCase):
    def setUp(self) -> None:
        self.fake = Faker()
        self.addCleanup(patch.stopall)
        return super().setUp()

    def test_get_movie_details_calls_requests(self):
        expected_movie_id = self.fake.word()
        expected_region = "en-US"
        expected_url = f"https://api.themoviedb.org/3/movie/{expected_movie_id}"
        mock_get = patch("requests.get").start()
        patch("json.loads").start()
        expected_params = {
            # Import happens before any patching, so keeping this in line with api.py
            "api_key": os.environ.get("API_KEY"),
            "region": expected_region
        }

        MovieApis.get_movie_details(expected_movie_id, expected_region)

        mock_get.assert_called_once_with(expected_url, expected_params)

    def test_get_movie_details_returns_data(self):
        expected_movie_id = self.fake.word()
        expected_region = "en-US"
        expected_data = self.fake.word()
        mock_loads = patch("json.loads").start()
        mock_loads.return_value = expected_data

        actual = MovieApis.get_movie_details(
            expected_movie_id, expected_region)

        self.assertEqual(actual, expected_data)

    def test_get_list_of_movies_call_requests_x_times(self):
        expected_pages = 4
        patch("json.loads").start()
        mock_get = patch("requests.get").start()

        MovieApis.get_list_of_movies(expected_pages)

        self.assertEqual(mock_get.call_count, expected_pages)

    def test_get_list_of_movies_returns_movie_list(self):
        expected_pages = 1
        patch("requests.get").start()
        mock_loads = patch("json.loads").start()
        expected_title = self.fake.word()
        expected_id = self.fake.pyint()
        mock_loads.return_value = {"results": [
            {"original_title": expected_title, "id": expected_id}]}
        expected_movie_list = [{
            "text": {
                "type": "plain_text",
                        "text": expected_title
            },
            "value": str(expected_id)
        }]

        actual = MovieApis.get_list_of_movies(expected_pages)

        self.assertEqual(actual, expected_movie_list)
