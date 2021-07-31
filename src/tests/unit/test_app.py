from logging import Logger
import os
import pytest
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, AsyncMock
from faker import Faker
import app
from slack_sdk import WebClient


class TestApp(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        patch("os.environ.get").start()
        self.fake = Faker()
        self.addCleanup(patch.stopall)
        self.client = AsyncMock()
        self.logger = AsyncMock(spec=Logger)
        self.ack = AsyncMock()
        self.event = AsyncMock()
        self.body = AsyncMock()
        return super().setUp()

    async def test_update_home_tab_publishes_view(self):
        expected_home = self.fake.word()
        mock_home = patch("json.load").start()
        mock_home.return_value = expected_home

        await app.update_home_tab(self.client, self.event, self.logger)

        self.client.views_publish.assert_called_once_with(
            user_id=self.event["user"], view=expected_home)

    async def test_action_button_click_opens_view(self):
        expected_movie_modal = self.fake.word()
        mock_movie_modal = patch("json.load").start()
        mock_movie_modal.return_value = expected_movie_modal

        await app.action_button_click(self.ack, self.client, self.body, self.logger)

        self.client.views_open.assert_called_once_with(
            trigger_id=self.body["trigger_id"], view=expected_movie_modal)

    async def test_show_list_of_movies_calls_movie_list(self):
        mock_get_list_of_movies = patch(
            "api.MovieApis.get_list_of_movies").start()
        pages_of_movies = 5

        await app.show_list_of_movies(self.ack)

        mock_get_list_of_movies.assert_called_once_with(pages_of_movies)

    async def test_handle_movie_submission_calls_movie_details_with_params(self):
        mock_get_movie_details = patch(
            "api.MovieApis.get_movie_details").start()
        patch("utils.convert_date").start()
        mock_user = self.fake.word()
        expected_movie_id = self.fake.word()
        expected_region = "en-US"
        self.body = {"view": {"state": {"values": {"movie_selection": {"movie_search": {
            "selected_option": {"value": expected_movie_id}}}}}}, "user": {"id": mock_user}}

        await app.handle_movie_submission(
            self.ack, self.body, self.client, self.logger)

        mock_get_movie_details.assert_called_once_with(
            expected_movie_id, expected_region)

    async def test_handle_movie_submission_calls_convert_date_with_release_date(self):
        mock_get_movie_details = patch(
            "api.MovieApis.get_movie_details").start()
        expected_date = self.fake.date()
        expected_details = {"release_date": expected_date,
                            "poster_path": "a_good_url",
                            "original_title": "Buffy: The Vampire Slayer",
                            "overview": "Slays Vampires, Saves the World"}
        mock_get_movie_details.return_value = expected_details
        mock_convert_date = patch("utils.convert_date").start()

        await app.handle_movie_submission(
            self.ack, self.body, self.client, self.logger)

        mock_convert_date.assert_called_once_with(expected_date)

    async def test_handle_movie_submission_posts_message(self):
        patch("api.MovieApis.get_movie_details").start()
        expected_blocks = self.fake.word()
        mock_create_message_blocks = patch(
            "utils.create_message_blocks").start()
        mock_create_message_blocks.return_value = expected_blocks
        expected_payload = "Movie info sent"

        await app.handle_movie_submission(
            self.ack, self.body, self.client, self.logger)

        self.client.chat_postMessage.assert_called_once_with(
            blocks=expected_blocks, channel=self.body["expected_user"]["expected_id"], text=expected_payload)

    async def test_show_list_of_movies_calls_ack_with_options(self):
        expected_movie_list = self.fake.word()
        mock_get_list_of_movies = patch(
            "api.MovieApis.get_list_of_movies").start()
        mock_get_list_of_movies.return_value = expected_movie_list

        await app.show_list_of_movies(self.ack)

        self.ack.assert_called_once_with(options=expected_movie_list)

    async def test_handle_action_calls_ack(self):

        await app.handle_action(self.ack)

        self.ack.assert_called_once()
