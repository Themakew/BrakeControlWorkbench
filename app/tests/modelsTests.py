import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(__file__ + "/../.."))
from models import User


class TestModels(unittest.TestCase):

    def test_get_id_when_email_is_informed(self):
        self.user = User("test@test.com")
        self.assertEqual(self.user.get_id(), "test@test.com")

    def test_get_id_when_email_is_not_informed(self):
        self.user = User("")
        self.assertEqual(self.user.get_id(), "")

    def test_is_active(self):
        self.user = User("test@test.com")
        self.assertTrue(self.user.is_active())

    def test_is_anonymous(self):
        self.user = User("test@test.com")
        self.assertFalse(self.user.is_anonymous())

    def test_is_authenticated(self):
        self.user = User("test@test.com")
        self.assertTrue(self.user.is_authenticated())


if __name__ == '__main__':
    unittest.main()
