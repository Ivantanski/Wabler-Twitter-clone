import unittest
from models import db, User, Message, Likes
from app import app

class UserModelTestCase(unittest.TestCase):
    """Test model for Users."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.signup("test1", "test1@test.com", "password", None)
        u2 = User.signup("test2", "test2@test.com", "password", None)
        db.session.commit()

        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        u = User.query.get(self.u1_id)
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_user_likes(self):
        """Test the likes relationship."""

        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        m = Message(text="Hello World", user_id=self.u2_id)
        db.session.add(m)
        db.session.commit()

        u1.likes.append(m)
        db.session.commit()

        self.assertEqual(len(u1.likes), 1)
        self.assertEqual(u1.likes[0].text, "Hello World")

if __name__ == '__main__':
    unittest.main()
