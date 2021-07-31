from unittest import TestCase
from unittest.mock import patch
from faker import Faker
from api import MovieApis


class TestApp(TestCase):
    def setUp(self) -> None:
        patch("os.environ.get")
        self.fake = Faker()
        self.addCleanup(patch.stopall)
        return super().setUp()

    def test_get_movie_details_calls_requests(self):
        expected_movie_id = self.fake.word()
        expected_region = 'en-US'
        expected_url = f"https://api.themoviedb.org/3/movie/{expected_movie_id}"
        mock_get = patch("requests.get").start()
        patch("json.loads").start()
        expected_params = {
            "api_key": None,
            "region": expected_region
        }

        MovieApis.get_movie_details(expected_movie_id, expected_region)

        mock_get.assert_called_once_with(expected_url, expected_params)

    def test_get_movie_details_returns_data(self):
        expected_movie_id = self.fake.word()
        expected_region = 'en-US'
        expected_data = self.fake.word()
        patch("requests.get").start()
        mock_loads = patch("json.loads").start()
        mock_loads.return_value = expected_data

        actual = MovieApis.get_movie_details(
            expected_movie_id, expected_region)

        self.assertEqual(actual, expected_data)

    def test_get_list_of_movies_call_requests_x_times(self):
        expected_pages = 4
        mock_loads = patch("json.loads").start()
        mock_get = patch("requests.get").start()

        MovieApis.get_list_of_movies(expected_pages)

        self.assertEqual(mock_get.call_count, expected_pages)
        self.assertEqual(mock_loads.call_count, expected_pages)
