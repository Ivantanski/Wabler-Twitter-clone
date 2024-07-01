import unittest
from models import db, User, Message
from app import app

class MessageModelTestCase(unittest.TestCase):
    """Test model for Messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u = User.signup("test", "test@test.com", "password", None)
        db.session.commit()

        self.u_id = u.id

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_message_model(self):
        """Does basic model work?"""

        m = Message(text="Hello World", user_id=self.u_id)
        db.session.add(m)
        db.session.commit()

        self.assertEqual(m.text, "Hello World")
        self.assertEqual(m.user_id, self.u_id)

if __name__ == '__main__':
    unittest.main()
