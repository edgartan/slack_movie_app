from unittest import TestCase
from unittest.mock import patch
from faker import Faker
from api import MovieApis

class TestApp(TestCase):
    def setUp(self) -> None:
        self.fake = Faker()
        self.addCleanup(patch.stopall)
        return super().setUp()
