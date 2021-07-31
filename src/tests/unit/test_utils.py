from unittest import TestCase
from unittest.mock import patch
from faker import Faker
import utils


class TestApp(TestCase):
    def setUp(self) -> None:
        self.fake = Faker()
        self.addCleanup(patch.stopall)
        return super().setUp()

    def test_convert_date_returns_date(self):
        test_date = '1986-08-08'
        expected_date = 'Aug 08, 1986'

        actual = utils.convert_date(test_date)

        self.assertEqual(actual, expected_date)

    def test_create_message_blocks_returns_message(self):
        expected_poster_url = self.fake.word()
        expected_date = self.fake.date()
        expected_overview = self.fake.word()
        expected_title = self.fake.word()
        mock_date = patch("utils.convert_date").start()
        mock_date.return_value = expected_date
        expected_blocks = [
            {
                "type": "section",
                "text": {
                        "type": "mrkdwn",
                        "text": "Here's is the movie info you requested!"
                }
            },
            {
                "type": "header",
                "text": {
                        "type": "plain_text",
                        "text": expected_title
                }
            },
            {
                "type": "section",
                "text": {
                        "type": "mrkdwn",
                        "text": "*Release date:* " + expected_date + " \n" + expected_overview
                },
                "accessory": {
                    "type": "image",
                    "image_url": expected_poster_url,
                    "alt_text": "movie poster"
                }
            }
        ]

        actual = utils.create_message_blocks(
            expected_title, expected_date, expected_overview, expected_poster_url)

        self.assertEqual(actual, expected_blocks)

    def test_create_message_blocks_calls_convert_date_with_date(self):
        expected_poster_url = self.fake.word()
        expected_date = self.fake.date()
        expected_overview = self.fake.word()
        expected_title = self.fake.word()
        mock_date = patch("utils.convert_date").start()
        mock_date.return_value = expected_date

        utils.create_message_blocks(
            expected_title, expected_date, expected_overview, expected_poster_url)

        mock_date.assert_called_once_with(expected_date)
