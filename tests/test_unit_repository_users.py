import unittest
from datetime import date
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas import UserModel
from src.repository.users import (create_user, get_user_by_email, update_token, confirmed_email)


class TestUsers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(
            id=1,
            username="test_user_1",
            email="test@example.ua",
            password="qwerty",
            avatar="",
            role="user",
            confirmed=True,
        )

    async def test_create_user(self):
        pass



